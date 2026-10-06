"""Deterministic reconnect and restart-recovery controller for EHB edge queues.

The controller never sleeps internally and never performs network I/O itself.
Callers provide an injectable ``send(payload) -> bool`` function and an aware
timestamp, which makes retry/backoff behavior deterministic and testable.

A failed or interrupted send never removes a queue item. The queue payload
fingerprint is preserved across retries; duplicate delivery after a crash is
expected to be handled idempotently by the already-merged CS1 consumer
contracts.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import math
import sqlite3
from typing import Any

from .ehb_queue import PersistentEdgeQueue

INITIAL = "INITIAL"
ONLINE = "ONLINE"
OFFLINE = "OFFLINE"


@dataclass(frozen=True)
class DeliveryConfig:
    initial_backoff_seconds: float = 1.0
    multiplier: float = 2.0
    max_backoff_seconds: float = 60.0
    device_software_version: str = "ehb-edge-runtime-v1"
    delivery_schema_version: str = "ehb-delivery-state-v1"

    def __post_init__(self) -> None:
        values = (
            self.initial_backoff_seconds,
            self.multiplier,
            self.max_backoff_seconds,
        )
        if any(not math.isfinite(value) for value in values):
            raise ValueError("backoff values must be finite")
        if self.initial_backoff_seconds <= 0:
            raise ValueError("initial_backoff_seconds must be > 0")
        if self.multiplier < 1:
            raise ValueError("multiplier must be >= 1")
        if self.max_backoff_seconds < self.initial_backoff_seconds:
            raise ValueError("max_backoff_seconds must be >= initial_backoff_seconds")
        if not self.device_software_version.strip():
            raise ValueError("device_software_version must be non-empty")
        if not self.delivery_schema_version.strip():
            raise ValueError("delivery_schema_version must be non-empty")

    def delay_for_failure_count(self, consecutive_failures: int) -> float:
        if isinstance(consecutive_failures, bool) or consecutive_failures <= 0:
            raise ValueError("consecutive_failures must be a positive integer")
        raw = self.initial_backoff_seconds * (
            self.multiplier ** (consecutive_failures - 1)
        )
        return min(raw, self.max_backoff_seconds)


def _aware(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("now must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return _aware(value).isoformat()


def _parse(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("persisted timestamp must be timezone-aware")
    return parsed.astimezone(timezone.utc)


class PersistentDeliveryController:
    """Persisted delivery/backoff state layered over ``PersistentEdgeQueue``."""

    def __init__(
        self,
        queue: PersistentEdgeQueue,
        *,
        config: DeliveryConfig | None = None,
    ) -> None:
        self.queue = queue
        self.config = config or DeliveryConfig()
        self._connection = sqlite3.connect(str(queue.database_path))
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._create_schema()

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "PersistentDeliveryController":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _create_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS edge_delivery_state (
                    singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
                    connection_state TEXT NOT NULL
                        CHECK (connection_state IN ('INITIAL', 'ONLINE', 'OFFLINE')),
                    consecutive_failures INTEGER NOT NULL DEFAULT 0
                        CHECK (consecutive_failures >= 0),
                    next_attempt_at TEXT,
                    last_success_at TEXT,
                    last_failure_at TEXT,
                    last_failure_reason TEXT,
                    device_software_version TEXT NOT NULL,
                    delivery_schema_version TEXT NOT NULL
                )
                """
            )
            self._connection.execute(
                """
                INSERT OR IGNORE INTO edge_delivery_state (
                    singleton_id,
                    connection_state,
                    consecutive_failures,
                    next_attempt_at,
                    device_software_version,
                    delivery_schema_version
                ) VALUES (1, ?, 0, NULL, ?, ?)
                """,
                (
                    INITIAL,
                    self.config.device_software_version,
                    self.config.delivery_schema_version,
                ),
            )
            self._connection.execute(
                """
                UPDATE edge_delivery_state
                SET device_software_version = ?,
                    delivery_schema_version = ?
                WHERE singleton_id = 1
                """,
                (
                    self.config.device_software_version,
                    self.config.delivery_schema_version,
                ),
            )

    def _state(self) -> sqlite3.Row:
        row = self._connection.execute(
            "SELECT * FROM edge_delivery_state WHERE singleton_id = 1"
        ).fetchone()
        if row is None:
            raise RuntimeError("delivery state row missing")
        return row

    def _record_success(self, now: datetime) -> None:
        with self._connection:
            self._connection.execute(
                """
                UPDATE edge_delivery_state
                SET connection_state = ?,
                    consecutive_failures = 0,
                    next_attempt_at = NULL,
                    last_success_at = ?,
                    last_failure_reason = NULL
                WHERE singleton_id = 1
                """,
                (ONLINE, _iso(now)),
            )

    def _record_failure(self, now: datetime, reason: str) -> float:
        state = self._state()
        failures = int(state["consecutive_failures"]) + 1
        delay = self.config.delay_for_failure_count(failures)
        next_attempt = _aware(now) + timedelta(seconds=delay)
        with self._connection:
            self._connection.execute(
                """
                UPDATE edge_delivery_state
                SET connection_state = ?,
                    consecutive_failures = ?,
                    next_attempt_at = ?,
                    last_failure_at = ?,
                    last_failure_reason = ?
                WHERE singleton_id = 1
                """,
                (
                    OFFLINE,
                    failures,
                    _iso(next_attempt),
                    _iso(now),
                    reason,
                ),
            )
        return delay

    def step(
        self,
        send: Callable[[Mapping[str, Any]], bool],
        *,
        now: datetime,
    ) -> dict[str, object]:
        current = _aware(now)
        state = self._state()
        next_attempt = _parse(state["next_attempt_at"])
        if next_attempt is not None and current < next_attempt:
            return {
                "status": "BACKOFF",
                "retry_after_seconds": max(
                    0.0, (next_attempt - current).total_seconds()
                ),
                "pending_count": self.queue.health()["pending_count"],
                "connection_state": str(state["connection_state"]),
            }

        pending = self.queue.pending(limit=1)
        if not pending:
            return {
                "status": "IDLE",
                "retry_after_seconds": 0.0,
                "pending_count": 0,
                "connection_state": str(state["connection_state"]),
            }

        record = pending[0]
        self.queue.mark_attempt(
            record.identity,
            payload_sha256=record.payload_sha256,
            attempted_at=_iso(current),
        )

        try:
            delivered = send(record.payload)
        except Exception as exc:
            reason = f"TRANSPORT_EXCEPTION_{type(exc).__name__.upper()}"
            delay = self._record_failure(current, reason)
            return {
                "status": "RETRY_SCHEDULED",
                "identity": record.identity,
                "payload_sha256": record.payload_sha256,
                "reason": reason,
                "retry_after_seconds": delay,
                "pending_count": self.queue.health()["pending_count"],
                "connection_state": OFFLINE,
            }

        if delivered is not True:
            delay = self._record_failure(current, "DELIVERY_NOT_ACKNOWLEDGED")
            return {
                "status": "RETRY_SCHEDULED",
                "identity": record.identity,
                "payload_sha256": record.payload_sha256,
                "reason": "DELIVERY_NOT_ACKNOWLEDGED",
                "retry_after_seconds": delay,
                "pending_count": self.queue.health()["pending_count"],
                "connection_state": OFFLINE,
            }

        self.queue.acknowledge(
            record.identity,
            payload_sha256=record.payload_sha256,
            acked_at=_iso(current),
        )
        self._record_success(current)
        return {
            "status": "ACKED",
            "identity": record.identity,
            "payload_sha256": record.payload_sha256,
            "retry_after_seconds": 0.0,
            "pending_count": self.queue.health()["pending_count"],
            "connection_state": ONLINE,
        }

    def health(self) -> dict[str, object]:
        state = self._state()
        queue_health = self.queue.health()
        return {
            **queue_health,
            "connection_state": str(state["connection_state"]),
            "consecutive_failures": int(state["consecutive_failures"]),
            "next_attempt_at": state["next_attempt_at"],
            "last_success_at": state["last_success_at"],
            "last_failure_at": state["last_failure_at"],
            "last_failure_reason": state["last_failure_reason"],
            "device_software_version": str(state["device_software_version"]),
            "delivery_schema_version": str(state["delivery_schema_version"]),
        }

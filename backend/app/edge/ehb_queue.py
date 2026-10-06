"""Persistent retry-safe queue for EHB edge devices.

This module is a device-side reference implementation for TrayGate and dining
count nodes. It preserves the exact JSON payload associated with a stable
anonymous identity (``captureId`` or ``eventId``) so offline retries cannot
silently mutate evidence before it reaches CS1.

The implementation uses only Python's standard library and SQLite. It makes no
claim about SD-card endurance, field reliability, power-loss immunity of a
particular filesystem, or deployment readiness; those require bench/field
evidence on the selected hardware.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

QUEUE_SCHEMA_VERSION = "ehb-edge-queue-v1"
ALLOWED_IDENTITY_FIELDS = frozenset({"eventId", "captureId"})
PENDING = "PENDING"
ACKED = "ACKED"


class QueueError(RuntimeError):
    """Base class for deterministic queue contract failures."""


class QueueReplayConflict(QueueError):
    """Raised when one stable identity is reused with a changed payload."""


class QueueFingerprintMismatch(QueueError):
    """Raised when an operation targets an identity with the wrong fingerprint."""


class QueueItemNotFound(QueueError):
    """Raised when an operation targets an unknown queue identity."""


@dataclass(frozen=True)
class QueueRecord:
    identity: str
    identity_field: str
    payload: dict[str, Any]
    payload_sha256: str
    state: str
    enqueued_at: str
    attempt_count: int
    last_attempt_at: str | None
    acked_at: str | None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_payload(payload: Mapping[str, Any]) -> tuple[str, str]:
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    try:
        canonical = json.dumps(
            dict(payload),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("payload must be JSON-serializable without NaN/Infinity") from exc
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return canonical, digest


def _identity(payload: Mapping[str, Any], identity_field: str) -> str:
    if identity_field not in ALLOWED_IDENTITY_FIELDS:
        raise ValueError(
            f"identity_field must be one of {sorted(ALLOWED_IDENTITY_FIELDS)}"
        )
    value = payload.get(identity_field)
    if value is None:
        raise ValueError(f"{identity_field} is required")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{identity_field} must be non-empty")
    return text


class PersistentEdgeQueue:
    """SQLite-backed immutable-payload queue.

    Rows are retained after ACK so the device continues to reject reuse of a
    previously acknowledged identity with a changed payload.
    """

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(str(self.database_path))
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA foreign_keys=ON")
        self._create_schema()

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "PersistentEdgeQueue":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _create_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS edge_queue (
                    queue_seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    identity TEXT NOT NULL UNIQUE,
                    identity_field TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    state TEXT NOT NULL CHECK (state IN ('PENDING', 'ACKED')),
                    enqueued_at TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
                    last_attempt_at TEXT,
                    acked_at TEXT,
                    queue_schema_version TEXT NOT NULL
                )
                """
            )
            self._connection.execute(
                """
                CREATE INDEX IF NOT EXISTS edge_queue_pending_order
                ON edge_queue(state, queue_seq)
                """
            )

    def enqueue(
        self,
        payload: Mapping[str, Any],
        *,
        identity_field: str,
        enqueued_at: str | None = None,
    ) -> dict[str, object]:
        identity = _identity(payload, identity_field)
        canonical, fingerprint = _canonical_payload(payload)
        timestamp = enqueued_at or _utc_now()

        with self._connection:
            existing = self._connection.execute(
                """
                SELECT identity_field, payload_json, payload_sha256, state
                FROM edge_queue
                WHERE identity = ?
                """,
                (identity,),
            ).fetchone()

            if existing is not None:
                same_payload = (
                    existing["identity_field"] == identity_field
                    and existing["payload_sha256"] == fingerprint
                    and existing["payload_json"] == canonical
                )
                if not same_payload:
                    raise QueueReplayConflict(
                        f"identity {identity!r} was already used with a different payload"
                    )
                return {
                    "status": "IDEMPOTENT_EXISTING",
                    "identity": identity,
                    "payload_sha256": fingerprint,
                    "state": str(existing["state"]),
                }

            self._connection.execute(
                """
                INSERT INTO edge_queue (
                    identity,
                    identity_field,
                    payload_json,
                    payload_sha256,
                    state,
                    enqueued_at,
                    queue_schema_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identity,
                    identity_field,
                    canonical,
                    fingerprint,
                    PENDING,
                    timestamp,
                    QUEUE_SCHEMA_VERSION,
                ),
            )

        return {
            "status": "ENQUEUED",
            "identity": identity,
            "payload_sha256": fingerprint,
            "state": PENDING,
        }

    def _row_to_record(self, row: sqlite3.Row) -> QueueRecord:
        return QueueRecord(
            identity=str(row["identity"]),
            identity_field=str(row["identity_field"]),
            payload=json.loads(str(row["payload_json"])),
            payload_sha256=str(row["payload_sha256"]),
            state=str(row["state"]),
            enqueued_at=str(row["enqueued_at"]),
            attempt_count=int(row["attempt_count"]),
            last_attempt_at=(
                str(row["last_attempt_at"]) if row["last_attempt_at"] is not None else None
            ),
            acked_at=str(row["acked_at"]) if row["acked_at"] is not None else None,
        )

    def get(self, identity: str) -> QueueRecord | None:
        row = self._connection.execute(
            """
            SELECT identity, identity_field, payload_json, payload_sha256, state,
                   enqueued_at, attempt_count, last_attempt_at, acked_at
            FROM edge_queue
            WHERE identity = ?
            """,
            (str(identity),),
        ).fetchone()
        return self._row_to_record(row) if row is not None else None

    def pending(self, *, limit: int = 100) -> list[QueueRecord]:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer")
        rows = self._connection.execute(
            """
            SELECT identity, identity_field, payload_json, payload_sha256, state,
                   enqueued_at, attempt_count, last_attempt_at, acked_at
            FROM edge_queue
            WHERE state = ?
            ORDER BY queue_seq ASC
            LIMIT ?
            """,
            (PENDING, limit),
        ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def mark_attempt(
        self,
        identity: str,
        *,
        payload_sha256: str,
        attempted_at: str | None = None,
    ) -> QueueRecord:
        timestamp = attempted_at or _utc_now()
        with self._connection:
            row = self._connection.execute(
                """
                SELECT payload_sha256, state
                FROM edge_queue
                WHERE identity = ?
                """,
                (identity,),
            ).fetchone()
            if row is None:
                raise QueueItemNotFound(identity)
            if str(row["payload_sha256"]) != payload_sha256:
                raise QueueFingerprintMismatch(identity)
            if str(row["state"]) != PENDING:
                raise QueueError(f"cannot mark attempt for {identity!r} in state {row['state']}")
            self._connection.execute(
                """
                UPDATE edge_queue
                SET attempt_count = attempt_count + 1,
                    last_attempt_at = ?
                WHERE identity = ?
                """,
                (timestamp, identity),
            )
        record = self.get(identity)
        assert record is not None
        return record

    def acknowledge(
        self,
        identity: str,
        *,
        payload_sha256: str,
        acked_at: str | None = None,
    ) -> QueueRecord:
        timestamp = acked_at or _utc_now()
        with self._connection:
            row = self._connection.execute(
                """
                SELECT payload_sha256, state
                FROM edge_queue
                WHERE identity = ?
                """,
                (identity,),
            ).fetchone()
            if row is None:
                raise QueueItemNotFound(identity)
            if str(row["payload_sha256"]) != payload_sha256:
                raise QueueFingerprintMismatch(identity)
            if str(row["state"]) == ACKED:
                record = self.get(identity)
                assert record is not None
                return record
            self._connection.execute(
                """
                UPDATE edge_queue
                SET state = ?, acked_at = ?
                WHERE identity = ?
                """,
                (ACKED, timestamp, identity),
            )
        record = self.get(identity)
        assert record is not None
        return record

    def health(self) -> dict[str, object]:
        rows = self._connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN state = 'PENDING' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN state = 'ACKED' THEN 1 ELSE 0 END) AS acked,
                COALESCE(SUM(attempt_count), 0) AS attempts
            FROM edge_queue
            """
        ).fetchone()
        assert rows is not None
        return {
            "queue_schema_version": QUEUE_SCHEMA_VERSION,
            "total_count": int(rows["total"]),
            "pending_count": int(rows["pending"] or 0),
            "acked_count": int(rows["acked"] or 0),
            "attempt_count": int(rows["attempts"] or 0),
        }

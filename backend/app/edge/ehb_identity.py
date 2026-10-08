"""Persistent non-secret provisioning state for EHB edge devices.

This module stores stable anonymous device/station identity, versioned
configuration metadata, and clock-readiness state. It deliberately rejects
person-identifying metadata and raw secret-bearing fields. Credentials belong
in an external secret store; only an opaque credential reference may be
recorded here.

The implementation is a software reference contract. It does not assert access
to campus networks, deployed credentials, secure elements, field hardware, or
physical tamper resistance.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

ACTIVE = "ACTIVE"
DEPROVISIONED = "DEPROVISIONED"
PROVISIONING_SCHEMA_VERSION = "ehb-provisioning-v1"

FORBIDDEN_IDENTITY_FIELDS = frozenset(
    {
        "studentid",
        "userid",
        "personid",
        "employeeid",
        "staffid",
        "bucardid",
        "cardid",
        "carduid",
        "email",
        "phone",
        "phonenumber",
        "fullname",
        "nationalid",
        "tckimlikno",
        "faceembedding",
        "biometricid",
    }
)
FORBIDDEN_SECRET_FIELDS = frozenset(
    {
        "password",
        "wifipassword",
        "passphrase",
        "secret",
        "clientsecret",
        "token",
        "accesstoken",
        "refreshtoken",
        "apikey",
        "privatekey",
        "privatekeypem",
    }
)


class ProvisioningError(RuntimeError):
    """Base class for provisioning contract failures."""


class ProvisioningConflict(ProvisioningError):
    """Raised when an explicit lifecycle operation is required."""


class ProvisioningRevisionConflict(ProvisioningError):
    """Raised when optimistic revision ownership is stale."""


class ProvisioningNotReady(ProvisioningError):
    """Raised when an operation requires an ACTIVE provisioned device."""


@dataclass(frozen=True)
class ProvisioningRecord:
    device_id: str
    station_id: str
    device_type: str
    firmware_version: str
    schema_version: str
    config_revision: int
    config: dict[str, Any]
    config_sha256: str
    credential_reference: str | None
    status: str
    provisioned_at: str
    updated_at: str


def _normalized_key(value: Any) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _text(value: Any, field: str) -> str:
    if value is None:
        raise ValueError(f"{field} is required")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must be non-empty")
    return text


def _aware_iso(value: Any, field: str) -> str:
    if isinstance(value, datetime):
        parsed = value
    else:
        text = _text(value, field)
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return parsed.astimezone(timezone.utc).isoformat()


def _forbidden_fields(value: Any) -> tuple[set[str], set[str]]:
    identity: set[str] = set()
    secrets: set[str] = set()
    seen: set[int] = set()
    pending: list[Any] = [value]
    while pending:
        current = pending.pop()
        if isinstance(current, Mapping):
            object_id = id(current)
            if object_id in seen:
                continue
            seen.add(object_id)
            for raw_key, nested in current.items():
                key = _normalized_key(raw_key)
                if key in FORBIDDEN_IDENTITY_FIELDS:
                    identity.add(key)
                if key in FORBIDDEN_SECRET_FIELDS:
                    secrets.add(key)
                pending.append(nested)
        elif isinstance(current, Sequence) and not isinstance(
            current, (str, bytes, bytearray)
        ):
            object_id = id(current)
            if object_id in seen:
                continue
            seen.add(object_id)
            pending.extend(current)
    return identity, secrets


def _canonical_config(config: Mapping[str, Any]) -> tuple[str, str]:
    if not isinstance(config, Mapping):
        raise TypeError("config must be a mapping")
    identity_fields, secret_fields = _forbidden_fields(config)
    if identity_fields:
        names = ",".join(sorted(identity_fields))
        raise ValueError(f"identity-bearing config fields are forbidden: {names}")
    if secret_fields:
        names = ",".join(sorted(secret_fields))
        raise ValueError(
            f"raw secret-bearing config fields are forbidden; store only a credential reference: {names}"
        )
    try:
        canonical = json.dumps(
            dict(config),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("config must be JSON-serializable without NaN/Infinity") from exc
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return canonical, digest


class ProvisioningStore:
    """SQLite-backed provisioning lifecycle with immutable revision history."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(str(self.database_path))
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._create_schema()

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "ProvisioningStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _create_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ehb_provisioning_current (
                    singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
                    device_id TEXT NOT NULL,
                    station_id TEXT NOT NULL,
                    device_type TEXT NOT NULL,
                    firmware_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    config_revision INTEGER NOT NULL CHECK (config_revision > 0),
                    config_json TEXT NOT NULL,
                    config_sha256 TEXT NOT NULL,
                    credential_reference TEXT,
                    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'DEPROVISIONED')),
                    provisioned_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    provisioning_schema_version TEXT NOT NULL
                )
                """
            )
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ehb_provisioning_history (
                    revision INTEGER PRIMARY KEY,
                    action TEXT NOT NULL,
                    snapshot_json TEXT NOT NULL,
                    changed_at TEXT NOT NULL
                )
                """
            )
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ehb_runtime_health (
                    singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
                    clock_valid INTEGER NOT NULL CHECK (clock_valid IN (0, 1)),
                    clock_checked_at TEXT
                )
                """
            )
            self._connection.execute(
                """
                INSERT OR IGNORE INTO ehb_runtime_health (
                    singleton_id, clock_valid, clock_checked_at
                ) VALUES (1, 0, NULL)
                """
            )

    def _current_row(self) -> sqlite3.Row | None:
        return self._connection.execute(
            "SELECT * FROM ehb_provisioning_current WHERE singleton_id = 1"
        ).fetchone()

    def _record_from_row(self, row: sqlite3.Row) -> ProvisioningRecord:
        return ProvisioningRecord(
            device_id=str(row["device_id"]),
            station_id=str(row["station_id"]),
            device_type=str(row["device_type"]),
            firmware_version=str(row["firmware_version"]),
            schema_version=str(row["schema_version"]),
            config_revision=int(row["config_revision"]),
            config=json.loads(str(row["config_json"])),
            config_sha256=str(row["config_sha256"]),
            credential_reference=(
                str(row["credential_reference"])
                if row["credential_reference"] is not None
                else None
            ),
            status=str(row["status"]),
            provisioned_at=str(row["provisioned_at"]),
            updated_at=str(row["updated_at"]),
        )

    def current(self) -> ProvisioningRecord | None:
        row = self._current_row()
        return self._record_from_row(row) if row is not None else None

    def _snapshot(
        self,
        *,
        device_id: str,
        station_id: str,
        device_type: str,
        firmware_version: str,
        schema_version: str,
        config_revision: int,
        config_json: str,
        config_sha256: str,
        credential_reference: str | None,
        status: str,
        provisioned_at: str,
        updated_at: str,
    ) -> str:
        return json.dumps(
            {
                "deviceId": device_id,
                "stationId": station_id,
                "deviceType": device_type,
                "firmwareVersion": firmware_version,
                "schemaVersion": schema_version,
                "configRevision": config_revision,
                "config": json.loads(config_json),
                "configSha256": config_sha256,
                "credentialReference": credential_reference,
                "status": status,
                "provisionedAt": provisioned_at,
                "updatedAt": updated_at,
                "provisioningSchemaVersion": PROVISIONING_SCHEMA_VERSION,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )

    def _append_history(self, revision: int, action: str, snapshot: str, changed_at: str) -> None:
        self._connection.execute(
            """
            INSERT INTO ehb_provisioning_history (
                revision, action, snapshot_json, changed_at
            ) VALUES (?, ?, ?, ?)
            """,
            (revision, action, snapshot, changed_at),
        )

    def provision(
        self,
        *,
        device_id: str,
        station_id: str,
        device_type: str,
        firmware_version: str,
        schema_version: str,
        config: Mapping[str, Any],
        provisioned_at: Any,
        credential_reference: str | None = None,
    ) -> dict[str, object]:
        device = _text(device_id, "device_id")
        station = _text(station_id, "station_id")
        kind = _text(device_type, "device_type")
        firmware = _text(firmware_version, "firmware_version")
        schema = _text(schema_version, "schema_version")
        timestamp = _aware_iso(provisioned_at, "provisioned_at")
        canonical, digest = _canonical_config(config)
        credential = (
            _text(credential_reference, "credential_reference")
            if credential_reference is not None
            else None
        )

        existing = self._current_row()
        if existing is not None:
            same = (
                str(existing["status"]) == ACTIVE
                and str(existing["device_id"]) == device
                and str(existing["station_id"]) == station
                and str(existing["device_type"]) == kind
                and str(existing["firmware_version"]) == firmware
                and str(existing["schema_version"]) == schema
                and str(existing["config_json"]) == canonical
                and str(existing["config_sha256"]) == digest
                and existing["credential_reference"] == credential
            )
            if same:
                return {
                    "status": "IDEMPOTENT_EXISTING",
                    "record": self._record_from_row(existing),
                }
            raise ProvisioningConflict(
                "device is already provisioned; use explicit update/reassign/deprovision operations"
            )

        revision = 1
        snapshot = self._snapshot(
            device_id=device,
            station_id=station,
            device_type=kind,
            firmware_version=firmware,
            schema_version=schema,
            config_revision=revision,
            config_json=canonical,
            config_sha256=digest,
            credential_reference=credential,
            status=ACTIVE,
            provisioned_at=timestamp,
            updated_at=timestamp,
        )
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO ehb_provisioning_current (
                    singleton_id, device_id, station_id, device_type,
                    firmware_version, schema_version, config_revision,
                    config_json, config_sha256, credential_reference,
                    status, provisioned_at, updated_at,
                    provisioning_schema_version
                ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    device,
                    station,
                    kind,
                    firmware,
                    schema,
                    revision,
                    canonical,
                    digest,
                    credential,
                    ACTIVE,
                    timestamp,
                    timestamp,
                    PROVISIONING_SCHEMA_VERSION,
                ),
            )
            self._append_history(revision, "PROVISION", snapshot, timestamp)

        record = self.current()
        assert record is not None
        return {"status": "PROVISIONED", "record": record}

    def _require_active(self, expected_revision: int) -> sqlite3.Row:
        row = self._current_row()
        if row is None or str(row["status"]) != ACTIVE:
            raise ProvisioningNotReady("device is not actively provisioned")
        if int(row["config_revision"]) != expected_revision:
            raise ProvisioningRevisionConflict(
                f"expected revision {expected_revision}, current is {row['config_revision']}"
            )
        return row

    def update_configuration(
        self,
        *,
        expected_revision: int,
        config: Mapping[str, Any],
        firmware_version: str,
        schema_version: str,
        updated_at: Any,
        credential_reference: str | None = None,
    ) -> ProvisioningRecord:
        row = self._require_active(expected_revision)
        canonical, digest = _canonical_config(config)
        firmware = _text(firmware_version, "firmware_version")
        schema = _text(schema_version, "schema_version")
        timestamp = _aware_iso(updated_at, "updated_at")
        credential = (
            _text(credential_reference, "credential_reference")
            if credential_reference is not None
            else None
        )
        revision = expected_revision + 1
        snapshot = self._snapshot(
            device_id=str(row["device_id"]),
            station_id=str(row["station_id"]),
            device_type=str(row["device_type"]),
            firmware_version=firmware,
            schema_version=schema,
            config_revision=revision,
            config_json=canonical,
            config_sha256=digest,
            credential_reference=credential,
            status=ACTIVE,
            provisioned_at=str(row["provisioned_at"]),
            updated_at=timestamp,
        )
        with self._connection:
            self._connection.execute(
                """
                UPDATE ehb_provisioning_current
                SET firmware_version = ?, schema_version = ?,
                    config_revision = ?, config_json = ?, config_sha256 = ?,
                    credential_reference = ?, updated_at = ?
                WHERE singleton_id = 1
                """,
                (
                    firmware,
                    schema,
                    revision,
                    canonical,
                    digest,
                    credential,
                    timestamp,
                ),
            )
            self._append_history(revision, "CONFIG_UPDATE", snapshot, timestamp)
        record = self.current()
        assert record is not None
        return record

    def reassign_station(
        self,
        *,
        expected_revision: int,
        station_id: str,
        updated_at: Any,
    ) -> ProvisioningRecord:
        row = self._require_active(expected_revision)
        station = _text(station_id, "station_id")
        timestamp = _aware_iso(updated_at, "updated_at")
        revision = expected_revision + 1
        snapshot = self._snapshot(
            device_id=str(row["device_id"]),
            station_id=station,
            device_type=str(row["device_type"]),
            firmware_version=str(row["firmware_version"]),
            schema_version=str(row["schema_version"]),
            config_revision=revision,
            config_json=str(row["config_json"]),
            config_sha256=str(row["config_sha256"]),
            credential_reference=row["credential_reference"],
            status=ACTIVE,
            provisioned_at=str(row["provisioned_at"]),
            updated_at=timestamp,
        )
        with self._connection:
            self._connection.execute(
                """
                UPDATE ehb_provisioning_current
                SET station_id = ?, config_revision = ?, updated_at = ?
                WHERE singleton_id = 1
                """,
                (station, revision, timestamp),
            )
            self._append_history(revision, "STATION_REASSIGN", snapshot, timestamp)
        record = self.current()
        assert record is not None
        return record

    def deprovision(
        self,
        *,
        expected_revision: int,
        updated_at: Any,
    ) -> ProvisioningRecord:
        row = self._require_active(expected_revision)
        timestamp = _aware_iso(updated_at, "updated_at")
        revision = expected_revision + 1
        snapshot = self._snapshot(
            device_id=str(row["device_id"]),
            station_id=str(row["station_id"]),
            device_type=str(row["device_type"]),
            firmware_version=str(row["firmware_version"]),
            schema_version=str(row["schema_version"]),
            config_revision=revision,
            config_json=str(row["config_json"]),
            config_sha256=str(row["config_sha256"]),
            credential_reference=row["credential_reference"],
            status=DEPROVISIONED,
            provisioned_at=str(row["provisioned_at"]),
            updated_at=timestamp,
        )
        with self._connection:
            self._connection.execute(
                """
                UPDATE ehb_provisioning_current
                SET status = ?, config_revision = ?, updated_at = ?
                WHERE singleton_id = 1
                """,
                (DEPROVISIONED, revision, timestamp),
            )
            self._append_history(revision, "DEPROVISION", snapshot, timestamp)
        record = self.current()
        assert record is not None
        return record

    def reprovision(
        self,
        *,
        expected_revision: int,
        station_id: str,
        firmware_version: str,
        schema_version: str,
        config: Mapping[str, Any],
        updated_at: Any,
        credential_reference: str | None = None,
    ) -> ProvisioningRecord:
        row = self._current_row()
        if row is None or str(row["status"]) != DEPROVISIONED:
            raise ProvisioningConflict("explicit reprovision requires DEPROVISIONED state")
        if int(row["config_revision"]) != expected_revision:
            raise ProvisioningRevisionConflict(
                f"expected revision {expected_revision}, current is {row['config_revision']}"
            )
        station = _text(station_id, "station_id")
        firmware = _text(firmware_version, "firmware_version")
        schema = _text(schema_version, "schema_version")
        timestamp = _aware_iso(updated_at, "updated_at")
        canonical, digest = _canonical_config(config)
        credential = (
            _text(credential_reference, "credential_reference")
            if credential_reference is not None
            else None
        )
        revision = expected_revision + 1
        snapshot = self._snapshot(
            device_id=str(row["device_id"]),
            station_id=station,
            device_type=str(row["device_type"]),
            firmware_version=firmware,
            schema_version=schema,
            config_revision=revision,
            config_json=canonical,
            config_sha256=digest,
            credential_reference=credential,
            status=ACTIVE,
            provisioned_at=str(row["provisioned_at"]),
            updated_at=timestamp,
        )
        with self._connection:
            self._connection.execute(
                """
                UPDATE ehb_provisioning_current
                SET station_id = ?, firmware_version = ?, schema_version = ?,
                    config_revision = ?, config_json = ?, config_sha256 = ?,
                    credential_reference = ?, status = ?, updated_at = ?
                WHERE singleton_id = 1
                """,
                (
                    station,
                    firmware,
                    schema,
                    revision,
                    canonical,
                    digest,
                    credential,
                    ACTIVE,
                    timestamp,
                ),
            )
            self._append_history(revision, "REPROVISION", snapshot, timestamp)
        record = self.current()
        assert record is not None
        return record

    def set_clock_valid(self, valid: bool, *, checked_at: Any) -> None:
        if not isinstance(valid, bool):
            raise TypeError("valid must be a boolean")
        timestamp = _aware_iso(checked_at, "checked_at")
        with self._connection:
            self._connection.execute(
                """
                UPDATE ehb_runtime_health
                SET clock_valid = ?, clock_checked_at = ?
                WHERE singleton_id = 1
                """,
                (1 if valid else 0, timestamp),
            )

    def history(self) -> list[dict[str, object]]:
        rows = self._connection.execute(
            """
            SELECT revision, action, snapshot_json, changed_at
            FROM ehb_provisioning_history
            ORDER BY revision ASC
            """
        ).fetchall()
        return [
            {
                "revision": int(row["revision"]),
                "action": str(row["action"]),
                "snapshot": json.loads(str(row["snapshot_json"])),
                "changed_at": str(row["changed_at"]),
            }
            for row in rows
        ]

    def health(self) -> dict[str, object]:
        current = self.current()
        runtime = self._connection.execute(
            "SELECT clock_valid, clock_checked_at FROM ehb_runtime_health WHERE singleton_id = 1"
        ).fetchone()
        assert runtime is not None
        clock_valid = bool(runtime["clock_valid"])
        active = current is not None and current.status == ACTIVE
        return {
            "provisioning_schema_version": PROVISIONING_SCHEMA_VERSION,
            "provisioning_status": current.status if current is not None else "UNPROVISIONED",
            "device_id": current.device_id if current is not None else None,
            "station_id": current.station_id if current is not None else None,
            "device_type": current.device_type if current is not None else None,
            "firmware_version": current.firmware_version if current is not None else None,
            "schema_version": current.schema_version if current is not None else None,
            "config_revision": current.config_revision if current is not None else None,
            "config_sha256": current.config_sha256 if current is not None else None,
            "credential_reference_present": bool(
                current is not None and current.credential_reference
            ),
            "clock_valid": clock_valid,
            "clock_checked_at": runtime["clock_checked_at"],
            "event_generation_ready": active and clock_valid,
        }

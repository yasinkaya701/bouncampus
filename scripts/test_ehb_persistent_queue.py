#!/usr/bin/env python3
"""Regression tests for the EHB persistent edge queue."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def load_queue_module():
    path = ROOT / "backend/app/edge/ehb_queue.py"
    assert path.exists(), f"missing production module: {path}"
    spec = importlib.util.spec_from_file_location("ehb_queue", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def count_event(index: int) -> dict:
    return {
        "eventId": f"dining-count-2026-10-06-{index:06d}",
        "deviceId": "serving-counter-north-01",
        "stationId": "north-dining-line-1",
        "timestamp": "2026-10-06T12:00:00+03:00",
        "measurementType": "SERVED_TRAY_DELTA",
        "value": 1,
        "unit": "TRAYS",
        "quality": "VALID",
        "source": "PHYSICAL_MEASUREMENT",
        "firmwareVersion": "dining-counter-fw-0.1.0",
        "schemaVersion": "dining-count-event-v1",
    }


def traygate_capture(index: int) -> dict:
    return {
        "deviceId": "traygate-01",
        "captureId": f"tg-2026-10-06-{index:06d}",
        "timestamp": "2026-10-06T12:01:00+03:00",
        "rgbFrame": f"local://captures/{index:06d}.jpg",
        "depthFrame": None,
        "trayDetected": True,
        "captureQuality": "VALID",
        "cameraCalibrationVersion": "cam-cal-v1",
        "deviceSoftwareVersion": "tg-device-v1",
    }


def test_enqueue_survives_close_and_reopen_without_mutation() -> None:
    module = load_queue_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "queue.sqlite3"
        payload = count_event(1)

        queue = module.PersistentEdgeQueue(database)
        result = queue.enqueue(payload, identity_field="eventId")
        fingerprint = result["payload_sha256"]
        queue.close()

        reopened = module.PersistentEdgeQueue(database)
        record = reopened.get(payload["eventId"])
        assert record is not None
        assert record.payload == payload
        assert record.payload_sha256 == fingerprint
        assert record.state == module.PENDING
        assert record.attempt_count == 0
        reopened.close()


def test_identical_reenqueue_is_idempotent_but_changed_payload_fails_closed() -> None:
    module = load_queue_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = module.PersistentEdgeQueue(Path(temp_dir) / "queue.sqlite3")
        payload = count_event(2)
        first = queue.enqueue(payload, identity_field="eventId")
        second = queue.enqueue(deepcopy(payload), identity_field="eventId")

        assert first["status"] == "ENQUEUED"
        assert second["status"] == "IDEMPOTENT_EXISTING"
        assert first["payload_sha256"] == second["payload_sha256"]
        assert queue.health()["total_count"] == 1

        conflict = deepcopy(payload)
        conflict["value"] = 2
        try:
            queue.enqueue(conflict, identity_field="eventId")
        except module.QueueReplayConflict:
            pass
        else:
            raise AssertionError("changed payload must fail closed under the same eventId")
        queue.close()


def test_attempt_and_ack_require_exact_fingerprint_and_persist() -> None:
    module = load_queue_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "queue.sqlite3"
        queue = module.PersistentEdgeQueue(database)
        payload = count_event(3)
        enqueued = queue.enqueue(payload, identity_field="eventId")
        fingerprint = str(enqueued["payload_sha256"])

        attempted = queue.mark_attempt(
            payload["eventId"],
            payload_sha256=fingerprint,
            attempted_at="2026-10-06T09:00:00+00:00",
        )
        assert attempted.attempt_count == 1
        assert attempted.last_attempt_at == "2026-10-06T09:00:00+00:00"

        try:
            queue.acknowledge(payload["eventId"], payload_sha256="0" * 64)
        except module.QueueFingerprintMismatch:
            pass
        else:
            raise AssertionError("ACK with a wrong fingerprint must fail closed")

        acked = queue.acknowledge(
            payload["eventId"],
            payload_sha256=fingerprint,
            acked_at="2026-10-06T09:01:00+00:00",
        )
        assert acked.state == module.ACKED
        assert queue.pending() == []
        queue.close()

        reopened = module.PersistentEdgeQueue(database)
        persisted = reopened.get(payload["eventId"])
        assert persisted is not None
        assert persisted.state == module.ACKED
        assert persisted.attempt_count == 1
        assert reopened.health() == {
            "queue_schema_version": module.QUEUE_SCHEMA_VERSION,
            "total_count": 1,
            "pending_count": 0,
            "acked_count": 1,
            "attempt_count": 1,
        }

        conflict = deepcopy(payload)
        conflict["quality"] = "SUSPECT"
        try:
            reopened.enqueue(conflict, identity_field="eventId")
        except module.QueueReplayConflict:
            pass
        else:
            raise AssertionError("ACKED identity reuse with changed payload must fail closed")
        reopened.close()


def test_fifo_pending_order_and_capture_identity_are_preserved() -> None:
    module = load_queue_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = module.PersistentEdgeQueue(Path(temp_dir) / "queue.sqlite3")
        first = traygate_capture(1)
        second = count_event(4)
        queue.enqueue(first, identity_field="captureId", enqueued_at="2026-10-06T09:00:00+00:00")
        queue.enqueue(second, identity_field="eventId", enqueued_at="2026-10-06T09:00:01+00:00")

        pending = queue.pending(limit=2)
        assert [row.identity for row in pending] == [first["captureId"], second["eventId"]]
        assert pending[0].identity_field == "captureId"
        assert pending[0].payload == first
        assert pending[1].identity_field == "eventId"
        assert pending[1].payload == second
        queue.close()


def test_invalid_identity_field_or_nonfinite_json_is_rejected() -> None:
    module = load_queue_module()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = module.PersistentEdgeQueue(Path(temp_dir) / "queue.sqlite3")
        payload = count_event(5)

        try:
            queue.enqueue(payload, identity_field="deviceId")
        except ValueError:
            pass
        else:
            raise AssertionError("unsupported identity field must be rejected")

        nonfinite = count_event(6)
        nonfinite["diagnostic"] = float("nan")
        try:
            queue.enqueue(nonfinite, identity_field="eventId")
        except ValueError:
            pass
        else:
            raise AssertionError("NaN must not enter the immutable queue payload")
        queue.close()


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} EHB persistent edge queue tests")

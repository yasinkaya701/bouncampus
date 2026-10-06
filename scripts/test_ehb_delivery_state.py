#!/usr/bin/env python3
"""Regression tests for EHB reconnect/backoff and restart recovery."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def modules():
    queue_module = importlib.import_module("backend.app.edge.ehb_queue")
    delivery_module = importlib.import_module("backend.app.edge.ehb_delivery")
    return queue_module, delivery_module


def event(index: int) -> dict:
    return {
        "eventId": f"dining-count-2026-10-06-{index:06d}",
        "deviceId": "tray-return-counter-01",
        "stationId": "north-return-line-1",
        "timestamp": "2026-10-06T12:00:00+03:00",
        "measurementType": "RETURNED_TRAY_DELTA",
        "value": 1,
        "unit": "TRAYS",
        "quality": "VALID",
        "source": "PHYSICAL_MEASUREMENT",
        "firmwareVersion": "counter-fw-v1",
        "schemaVersion": "dining-count-event-v1",
    }


def utc(hour: int, minute: int = 0, second: int = 0) -> datetime:
    return datetime(2026, 10, 6, hour, minute, second, tzinfo=timezone.utc)


def test_failure_schedules_backoff_and_does_not_drop_payload() -> None:
    queue_module, delivery_module = modules()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = queue_module.PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        payload = event(1)
        queue.enqueue(payload, identity_field="eventId")
        controller = delivery_module.PersistentDeliveryController(
            queue,
            config=delivery_module.DeliveryConfig(
                initial_backoff_seconds=2,
                multiplier=2,
                max_backoff_seconds=8,
            ),
        )

        result = controller.step(lambda _payload: False, now=utc(9))
        assert result["status"] == "RETRY_SCHEDULED"
        assert result["retry_after_seconds"] == 2
        assert queue.health()["pending_count"] == 1
        record = queue.get(payload["eventId"])
        assert record is not None and record.attempt_count == 1

        blocked = controller.step(lambda _payload: True, now=utc(9, 0, 1))
        assert blocked["status"] == "BACKOFF"
        assert blocked["retry_after_seconds"] == 1
        record = queue.get(payload["eventId"])
        assert record is not None and record.attempt_count == 1
        controller.close()
        queue.close()


def test_backoff_and_failure_state_persist_across_restart_then_success_resets() -> None:
    queue_module, delivery_module = modules()
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "edge.sqlite3"
        queue = queue_module.PersistentEdgeQueue(database)
        payload = event(2)
        queue.enqueue(payload, identity_field="eventId")
        config = delivery_module.DeliveryConfig(
            initial_backoff_seconds=2,
            multiplier=2,
            max_backoff_seconds=8,
            device_software_version="counter-runtime-v2",
        )
        first = delivery_module.PersistentDeliveryController(queue, config=config)
        first.step(lambda _payload: False, now=utc(9))
        first.close()
        queue.close()

        queue2 = queue_module.PersistentEdgeQueue(database)
        second = delivery_module.PersistentDeliveryController(queue2, config=config)
        health = second.health()
        assert health["connection_state"] == delivery_module.OFFLINE
        assert health["consecutive_failures"] == 1
        assert health["device_software_version"] == "counter-runtime-v2"

        blocked = second.step(lambda _payload: True, now=utc(9, 0, 1))
        assert blocked["status"] == "BACKOFF"

        delivered = second.step(lambda _payload: True, now=utc(9, 0, 2))
        assert delivered["status"] == "ACKED"
        health = second.health()
        assert health["pending_count"] == 0
        assert health["acked_count"] == 1
        assert health["consecutive_failures"] == 0
        assert health["connection_state"] == delivery_module.ONLINE
        assert health["next_attempt_at"] is None
        second.close()
        queue2.close()


def test_exponential_backoff_is_bounded() -> None:
    queue_module, delivery_module = modules()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = queue_module.PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        queue.enqueue(event(3), identity_field="eventId")
        controller = delivery_module.PersistentDeliveryController(
            queue,
            config=delivery_module.DeliveryConfig(
                initial_backoff_seconds=2,
                multiplier=2,
                max_backoff_seconds=5,
            ),
        )

        moments = [utc(9), utc(9, 0, 2), utc(9, 0, 6), utc(9, 0, 11)]
        expected = [2, 4, 5, 5]
        for now, delay in zip(moments, expected, strict=True):
            result = controller.step(lambda _payload: False, now=now)
            assert result["status"] == "RETRY_SCHEDULED"
            assert result["retry_after_seconds"] == delay

        assert controller.health()["consecutive_failures"] == 4
        record = queue.pending(limit=1)[0]
        assert record.attempt_count == 4
        controller.close()
        queue.close()


def test_transport_exception_remains_pending_with_explicit_reason() -> None:
    queue_module, delivery_module = modules()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = queue_module.PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        queue.enqueue(event(4), identity_field="eventId")
        controller = delivery_module.PersistentDeliveryController(queue)

        def failing_send(_payload):
            raise ConnectionError("offline")

        result = controller.step(failing_send, now=utc(10))
        assert result["status"] == "RETRY_SCHEDULED"
        assert result["reason"] == "TRANSPORT_EXCEPTION_CONNECTIONERROR"
        assert queue.health()["pending_count"] == 1
        assert controller.health()["last_failure_reason"] == "TRANSPORT_EXCEPTION_CONNECTIONERROR"
        controller.close()
        queue.close()


def test_interrupted_attempt_is_retried_after_restart_with_same_payload() -> None:
    queue_module, delivery_module = modules()
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "edge.sqlite3"
        payload = event(5)
        queue = queue_module.PersistentEdgeQueue(database)
        enqueued = queue.enqueue(payload, identity_field="eventId")
        queue.mark_attempt(
            payload["eventId"],
            payload_sha256=str(enqueued["payload_sha256"]),
            attempted_at=utc(11).isoformat(),
        )
        queue.close()

        reopened = queue_module.PersistentEdgeQueue(database)
        controller = delivery_module.PersistentDeliveryController(reopened)
        observed = []

        def send_again(actual_payload):
            observed.append(actual_payload)
            return True

        result = controller.step(send_again, now=utc(11, 0, 1))
        assert result["status"] == "ACKED"
        assert observed == [payload]
        record = reopened.get(payload["eventId"])
        assert record is not None
        assert record.attempt_count == 2
        assert record.state == queue_module.ACKED
        controller.close()
        reopened.close()


def test_empty_queue_is_idle_without_network_call() -> None:
    queue_module, delivery_module = modules()
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = queue_module.PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        controller = delivery_module.PersistentDeliveryController(queue)
        called = False

        def send(_payload):
            nonlocal called
            called = True
            return True

        result = controller.step(send, now=utc(12))
        assert result["status"] == "IDLE"
        assert called is False
        controller.close()
        queue.close()


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} EHB delivery-state tests")

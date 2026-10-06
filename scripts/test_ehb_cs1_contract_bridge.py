#!/usr/bin/env python3
"""Cross-contract regression between EHB edge delivery and CS1 consumers."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import tempfile

from backend.app.decision import dining_count_truth, traygate
from backend.app.edge.ehb_delivery import PersistentDeliveryController
from backend.app.edge.ehb_queue import PersistentEdgeQueue, QueueReplayConflict


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
        "firmwareVersion": "tray-counter-fw-v1",
        "schemaVersion": "dining-count-event-v1",
    }


def capture(index: int) -> dict:
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


def utc(hour: int, second: int = 0) -> datetime:
    return datetime(2026, 10, 6, hour, 0, second, tzinfo=timezone.utc)


def test_count_event_ack_loss_retries_exact_payload_and_cs1_counts_once() -> None:
    payload = count_event(1)
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        queue.enqueue(payload, identity_field="eventId")
        controller = PersistentDeliveryController(queue)
        received: list[dict] = []

        def first_server_receive(actual: dict) -> bool:
            received.append(deepcopy(actual))
            validation = dining_count_truth.validate_dining_count_event(actual)
            assert validation["validation_status"] == "ACCEPTED_MEASURED"
            return False  # server received it, but local ACK was lost

        first = controller.step(first_server_receive, now=utc(9))
        assert first["status"] == "RETRY_SCHEDULED"
        assert queue.health()["pending_count"] == 1

        def second_server_receive(actual: dict) -> bool:
            received.append(deepcopy(actual))
            validation = dining_count_truth.validate_dining_count_event(actual)
            assert validation["validation_status"] == "ACCEPTED_MEASURED"
            return True

        second = controller.step(second_server_receive, now=utc(9, 1))
        assert second["status"] == "ACKED"
        assert received == [payload, payload]

        aggregate = dining_count_truth.aggregate_dining_count_events(
            received,
            expected_station_id=payload["stationId"],
            window_start="2026-10-06T11:00:00+03:00",
            window_end="2026-10-06T14:00:00+03:00",
        )
        assert aggregate["aggregation_status"] == "AGGREGATED"
        assert aggregate["unique_event_count"] == 1
        assert aggregate["idempotent_replay_count"] == 1
        assert aggregate["served_trays_observed"] == 1
        assert aggregate["reconciled_service_truth"] is False
        controller.close()
        queue.close()


def test_traygate_capture_retry_preserves_capture_identity_and_cs1_admission() -> None:
    payload = capture(2)
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        queue.enqueue(payload, identity_field="captureId")
        controller = PersistentDeliveryController(queue)
        received: list[dict] = []

        def send_without_ack(actual: dict) -> bool:
            received.append(deepcopy(actual))
            validation = traygate.validate_traygate_capture(actual)
            assert validation["validation_status"] == "ACCEPTED"
            assert validation["capture_id"] == payload["captureId"]
            return False

        controller.step(send_without_ack, now=utc(10))

        def send_with_ack(actual: dict) -> bool:
            received.append(deepcopy(actual))
            validation = traygate.validate_traygate_capture(actual)
            assert validation["validation_status"] == "ACCEPTED"
            return True

        result = controller.step(send_with_ack, now=utc(10, 1))
        assert result["status"] == "ACKED"
        assert received == [payload, payload]
        assert all(row["captureId"] == payload["captureId"] for row in received)
        controller.close()
        queue.close()


def test_changed_payload_under_same_identity_is_blocked_before_transport() -> None:
    payload = count_event(3)
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        queue.enqueue(payload, identity_field="eventId")
        mutated = deepcopy(payload)
        mutated["value"] = 2

        try:
            queue.enqueue(mutated, identity_field="eventId")
        except QueueReplayConflict:
            pass
        else:
            raise AssertionError("changed payload must not enter retry transport")

        pending = queue.pending(limit=1)
        assert len(pending) == 1
        assert pending[0].payload == payload
        queue.close()


def test_identity_bearing_payload_is_never_acknowledged_by_cs1_bridge() -> None:
    payload = count_event(4)
    payload["metadata"] = {"studentId": "forbidden"}
    with tempfile.TemporaryDirectory() as temp_dir:
        queue = PersistentEdgeQueue(Path(temp_dir) / "edge.sqlite3")
        queue.enqueue(payload, identity_field="eventId")
        controller = PersistentDeliveryController(queue)

        def cs1_bridge(actual: dict) -> bool:
            validation = dining_count_truth.validate_dining_count_event(actual)
            assert validation["validation_status"] == "REJECTED"
            assert "PRIVACY_FIELD_NOT_ALLOWED_STUDENTID" in validation["reason_codes"]
            return validation["aggregation_eligible"] is True

        result = controller.step(cs1_bridge, now=utc(11))
        assert result["status"] == "RETRY_SCHEDULED"
        assert queue.health()["pending_count"] == 1
        controller.close()
        queue.close()


def test_time_source_and_quality_semantics_fail_closed_at_consumer_boundary() -> None:
    valid = count_event(5)
    assert dining_count_truth.validate_dining_count_event(valid)["validation_status"] == "ACCEPTED_MEASURED"

    naive_time = deepcopy(valid)
    naive_time["eventId"] = "dining-count-naive-time"
    naive_time["timestamp"] = "2026-10-06T12:00:00"
    naive_result = dining_count_truth.validate_dining_count_event(naive_time)
    assert naive_result["validation_status"] == "REJECTED"
    assert "TIMESTAMP_MUST_BE_TIMEZONE_AWARE" in naive_result["reason_codes"]

    nonphysical = deepcopy(valid)
    nonphysical["eventId"] = "dining-count-nonphysical"
    nonphysical["source"] = "GENERATED_SANDBOX"
    source_result = dining_count_truth.validate_dining_count_event(nonphysical)
    assert source_result["validation_status"] == "WITHHOLD"
    assert "PHYSICAL_MEASUREMENT_REQUIRED" in source_result["reason_codes"]

    low_quality = deepcopy(valid)
    low_quality["eventId"] = "dining-count-low-quality"
    low_quality["quality"] = "SUSPECT"
    quality_result = dining_count_truth.validate_dining_count_event(low_quality)
    assert quality_result["validation_status"] == "WITHHOLD"
    assert "MEASUREMENT_QUALITY_NOT_VALID" in quality_result["reason_codes"]

    bad_capture = capture(6)
    bad_capture["timestamp"] = "2026-10-06T12:01:00"
    capture_result = traygate.validate_traygate_capture(bad_capture)
    assert capture_result["validation_status"] == "REJECTED"
    assert "TIMESTAMP_MUST_BE_TIMEZONE_AWARE" in capture_result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} EHB-CS1 cross-contract tests")

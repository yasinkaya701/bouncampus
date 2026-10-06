#!/usr/bin/env python3
"""Regression tests for EHB device identity and provisioning lifecycle."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.edge.ehb_identity import (
    ACTIVE,
    DEPROVISIONED,
    ProvisioningConflict,
    ProvisioningRevisionConflict,
    ProvisioningStore,
)


def base_config() -> dict:
    return {
        "networkMode": "WIFI",
        "sampleProfile": "tray-counter-v1",
        "timezone": "Europe/Istanbul",
    }


def provision(store: ProvisioningStore):
    return store.provision(
        device_id="tray-counter-north-01",
        station_id="north-return-line-1",
        device_type="TRAY_RETURN_COUNTER",
        firmware_version="counter-fw-v1",
        schema_version="dining-count-event-v1",
        config=base_config(),
        credential_reference="secure-store:campus-network-profile",
        provisioned_at="2026-10-06T12:00:00+03:00",
    )


def test_first_provision_and_restart_preserve_stable_identity() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "edge.sqlite3"
        store = ProvisioningStore(database)
        result = provision(store)
        assert result["status"] == "PROVISIONED"
        record = result["record"]
        assert record.device_id == "tray-counter-north-01"
        assert record.station_id == "north-return-line-1"
        assert record.config_revision == 1
        assert record.status == ACTIVE
        store.close()

        reopened = ProvisioningStore(database)
        persisted = reopened.current()
        assert persisted is not None
        assert persisted.device_id == "tray-counter-north-01"
        assert persisted.station_id == "north-return-line-1"
        assert persisted.config == base_config()
        assert reopened.history()[0]["action"] == "PROVISION"
        reopened.close()


def test_identical_provision_is_idempotent_but_implicit_identity_change_fails() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = ProvisioningStore(Path(temp_dir) / "edge.sqlite3")
        first = provision(store)
        second = provision(store)
        assert first["record"].config_sha256 == second["record"].config_sha256
        assert second["status"] == "IDEMPOTENT_EXISTING"
        assert len(store.history()) == 1

        try:
            store.provision(
                device_id="different-device",
                station_id="north-return-line-1",
                device_type="TRAY_RETURN_COUNTER",
                firmware_version="counter-fw-v1",
                schema_version="dining-count-event-v1",
                config=base_config(),
                provisioned_at="2026-10-06T12:01:00+03:00",
            )
        except ProvisioningConflict:
            pass
        else:
            raise AssertionError("silent device identity replacement must fail")
        store.close()


def test_configuration_update_is_versioned_and_stale_revision_fails() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = ProvisioningStore(Path(temp_dir) / "edge.sqlite3")
        provision(store)
        updated_config = {**base_config(), "debounceProfile": "bench-v2"}
        record = store.update_configuration(
            expected_revision=1,
            config=updated_config,
            firmware_version="counter-fw-v2",
            schema_version="dining-count-event-v1",
            credential_reference="secure-store:campus-network-profile",
            updated_at="2026-10-06T12:10:00+03:00",
        )
        assert record.config_revision == 2
        assert record.firmware_version == "counter-fw-v2"
        assert record.config == updated_config
        assert [row["action"] for row in store.history()] == [
            "PROVISION",
            "CONFIG_UPDATE",
        ]

        try:
            store.update_configuration(
                expected_revision=1,
                config=base_config(),
                firmware_version="counter-fw-v3",
                schema_version="dining-count-event-v1",
                updated_at="2026-10-06T12:11:00+03:00",
            )
        except ProvisioningRevisionConflict:
            pass
        else:
            raise AssertionError("stale revision update must fail")
        store.close()


def test_station_reassignment_deprovision_and_reprovision_are_explicit() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = ProvisioningStore(Path(temp_dir) / "edge.sqlite3")
        provision(store)
        moved = store.reassign_station(
            expected_revision=1,
            station_id="south-return-line-1",
            updated_at="2026-10-06T13:00:00+03:00",
        )
        assert moved.device_id == "tray-counter-north-01"
        assert moved.station_id == "south-return-line-1"
        assert moved.config_revision == 2

        stopped = store.deprovision(
            expected_revision=2,
            updated_at="2026-10-06T13:10:00+03:00",
        )
        assert stopped.status == DEPROVISIONED
        assert stopped.config_revision == 3
        assert store.health()["event_generation_ready"] is False

        restored = store.reprovision(
            expected_revision=3,
            station_id="north-return-line-2",
            firmware_version="counter-fw-v2",
            schema_version="dining-count-event-v1",
            config={**base_config(), "installationRevision": "rev-b"},
            credential_reference="secure-store:new-network-profile",
            updated_at="2026-10-06T14:00:00+03:00",
        )
        assert restored.status == ACTIVE
        assert restored.device_id == "tray-counter-north-01"
        assert restored.station_id == "north-return-line-2"
        assert restored.config_revision == 4
        assert [row["action"] for row in store.history()] == [
            "PROVISION",
            "STATION_REASSIGN",
            "DEPROVISION",
            "REPROVISION",
        ]
        store.close()


def test_raw_secret_and_person_identity_fields_are_rejected() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = ProvisioningStore(Path(temp_dir) / "edge.sqlite3")
        for bad_config in (
            {"wifiPassword": "never-store-this"},
            {"nested": {"apiKey": "never-store-this"}},
            {"metadata": {"studentId": "not-a-device-config-field"}},
        ):
            try:
                store.provision(
                    device_id="device-01",
                    station_id="station-01",
                    device_type="TEST_NODE",
                    firmware_version="fw-v1",
                    schema_version="schema-v1",
                    config=bad_config,
                    provisioned_at="2026-10-06T12:00:00+03:00",
                )
            except ValueError:
                pass
            else:
                raise AssertionError(f"forbidden config was persisted: {bad_config!r}")
        assert store.current() is None
        store.close()


def test_clock_validity_is_required_for_event_generation_readiness() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = ProvisioningStore(Path(temp_dir) / "edge.sqlite3")
        provision(store)
        health = store.health()
        assert health["provisioning_status"] == ACTIVE
        assert health["clock_valid"] is False
        assert health["event_generation_ready"] is False

        store.set_clock_valid(
            True,
            checked_at="2026-10-06T12:05:00+03:00",
        )
        ready = store.health()
        assert ready["clock_valid"] is True
        assert ready["event_generation_ready"] is True

        store.set_clock_valid(
            False,
            checked_at="2026-10-06T12:06:00+03:00",
        )
        assert store.health()["event_generation_ready"] is False
        store.close()


def test_naive_lifecycle_timestamp_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = ProvisioningStore(Path(temp_dir) / "edge.sqlite3")
        try:
            store.provision(
                device_id="device-01",
                station_id="station-01",
                device_type="TEST_NODE",
                firmware_version="fw-v1",
                schema_version="schema-v1",
                config={},
                provisioned_at="2026-10-06T12:00:00",
            )
        except ValueError as exc:
            assert "timezone-aware" in str(exc)
        else:
            raise AssertionError("naive provisioning timestamp must fail")
        store.close()


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} EHB provisioning lifecycle tests")

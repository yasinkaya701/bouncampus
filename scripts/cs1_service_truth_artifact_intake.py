#!/usr/bin/env python3
"""Fail-closed file intake for SERVICE_TRUTH_V1 benchmark artifacts.

The CLI is a transport/package boundary only. It delegates all service-truth,
provenance, cutoff, privacy, snapshot-integrity, and source-exportability
semantics to the canonical ``app.decision.service_truth`` validator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.service_truth import (  # noqa: E402
    CONTRACT_VERSION,
    validate_service_truth_artifact,
)

EXIT_ACCEPTED = 0
EXIT_REJECTED = 2
EXIT_INVALID_PACKAGE = 3


def _print_result(result: Mapping[str, Any]) -> None:
    print(
        json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    )


def _invalid_result(
    *,
    reason_code: str,
    file_sha256: str,
    contract_version: Any = None,
) -> dict[str, Any]:
    return {
        "intake_status": "INVALID_PACKAGE",
        "eligible_for_benchmark": False,
        "contract_version": contract_version,
        "intake_file_sha256": file_sha256,
        "reason_codes": [reason_code],
    }


def _load_package(path: Path) -> tuple[Any, str, str | None]:
    try:
        raw = path.read_bytes()
    except OSError:
        return None, "", "ARTIFACT_READ_FAILED"

    file_sha256 = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, file_sha256, "ARTIFACT_MUST_BE_UTF8"

    try:
        return json.loads(text), file_sha256, None
    except json.JSONDecodeError:
        return None, file_sha256, "INVALID_JSON"


def intake_artifact(path: Path) -> tuple[dict[str, Any], int]:
    package, file_sha256, load_error = _load_package(path)
    if load_error is not None:
        return (
            _invalid_result(
                reason_code=load_error,
                file_sha256=file_sha256,
            ),
            EXIT_INVALID_PACKAGE,
        )

    if not isinstance(package, Mapping):
        return (
            _invalid_result(
                reason_code="PACKAGE_MUST_BE_OBJECT",
                file_sha256=file_sha256,
            ),
            EXIT_INVALID_PACKAGE,
        )

    contract_version = package.get("contract_version")
    if contract_version != CONTRACT_VERSION:
        return (
            _invalid_result(
                reason_code="UNSUPPORTED_CONTRACT_VERSION",
                file_sha256=file_sha256,
                contract_version=contract_version,
            ),
            EXIT_INVALID_PACKAGE,
        )

    if "rows" not in package:
        return (
            _invalid_result(
                reason_code="ROWS_REQUIRED",
                file_sha256=file_sha256,
                contract_version=contract_version,
            ),
            EXIT_INVALID_PACKAGE,
        )
    rows = package.get("rows")
    if isinstance(rows, (str, bytes)) or not isinstance(rows, Sequence):
        return (
            _invalid_result(
                reason_code="ROWS_MUST_BE_SEQUENCE",
                file_sha256=file_sha256,
                contract_version=contract_version,
            ),
            EXIT_INVALID_PACKAGE,
        )

    if "field_provenance" not in package:
        return (
            _invalid_result(
                reason_code="FIELD_PROVENANCE_REQUIRED",
                file_sha256=file_sha256,
                contract_version=contract_version,
            ),
            EXIT_INVALID_PACKAGE,
        )
    field_provenance = package.get("field_provenance")
    if not isinstance(field_provenance, Mapping):
        return (
            _invalid_result(
                reason_code="FIELD_PROVENANCE_MUST_BE_OBJECT",
                file_sha256=file_sha256,
                contract_version=contract_version,
            ),
            EXIT_INVALID_PACKAGE,
        )

    validation = validate_service_truth_artifact(
        rows,
        field_provenance=field_provenance,
    )
    eligible = bool(validation.get("eligible_for_benchmark"))
    result: dict[str, Any] = {
        "intake_status": "ACCEPTED" if eligible else "REJECTED",
        "eligible_for_benchmark": eligible,
        "contract_version": contract_version,
        "intake_file_sha256": file_sha256,
        "validation_status": validation.get("validation_status"),
        "reason_codes": list(validation.get("reason_codes", [])),
        "artifact_validation": validation,
    }
    fingerprint = validation.get("artifact_admission_fingerprint_sha256")
    if fingerprint is not None:
        result["artifact_admission_fingerprint_sha256"] = fingerprint
    return result, EXIT_ACCEPTED if eligible else EXIT_REJECTED


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifact",
        type=Path,
        required=True,
        help="path to one SERVICE_TRUTH_V1 JSON package",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result, exit_code = intake_artifact(args.artifact)
    _print_result(result)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fail CI when a merge silently drops registered BOUNCAMPUS features."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REGISTRY = Path('.github/feature-registry.json')


def fail(message: str) -> None:
    print(f'feature-preservation: ERROR: {message}', file=sys.stderr)
    raise SystemExit(1)


def load_registry_bytes(raw: bytes, source: str) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f'{source} is not valid JSON: {exc}')
    if data.get('schema_version') != 1:
        fail(f'{source} must use schema_version=1')
    features = data.get('features')
    if not isinstance(features, list):
        fail(f'{source} must contain a features array')
    return data


def feature_map(data: dict[str, Any], source: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for entry in data['features']:
        if not isinstance(entry, dict):
            fail(f'{source} contains a non-object feature entry')
        feature_id = entry.get('id')
        paths = entry.get('required_paths')
        if not isinstance(feature_id, str) or not feature_id.strip():
            fail(f'{source} contains a feature without a valid id')
        if feature_id in result:
            fail(f'{source} contains duplicate feature id {feature_id!r}')
        if not isinstance(paths, list) or not paths:
            fail(f'feature {feature_id!r} must declare at least one required path')
        normalized: set[str] = set()
        for value in paths:
            if not isinstance(value, str) or not value.strip():
                fail(f'feature {feature_id!r} contains an invalid required path')
            path = Path(value)
            if path.is_absolute() or '..' in path.parts:
                fail(f'feature {feature_id!r} contains unsafe path {value!r}')
            normalized.add(value)
        result[feature_id] = normalized
    return result


def read_base_registry(base_ref: str) -> dict[str, Any] | None:
    proc = subprocess.run(
        ['git', 'show', f'{base_ref}:{REGISTRY.as_posix()}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        print('feature-preservation: base commit has no registry; treating this as registry bootstrap')
        return None
    return load_registry_bytes(proc.stdout, f'{base_ref}:{REGISTRY}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-ref', help='Base commit/ref to compare registry guarantees against')
    args = parser.parse_args()

    if not REGISTRY.is_file():
        fail(f'missing {REGISTRY}')

    head_data = load_registry_bytes(REGISTRY.read_bytes(), REGISTRY.as_posix())
    head = feature_map(head_data, REGISTRY.as_posix())

    missing_paths: list[str] = []
    for feature_id, paths in sorted(head.items()):
        for required_path in sorted(paths):
            if not Path(required_path).is_file():
                missing_paths.append(f'{feature_id}: {required_path}')
    if missing_paths:
        fail('registered feature files are missing:\n  - ' + '\n  - '.join(missing_paths))

    if args.base_ref:
        base_data = read_base_registry(args.base_ref)
        if base_data is not None:
            base = feature_map(base_data, f'{args.base_ref}:{REGISTRY}')
            removed_features = sorted(set(base) - set(head))
            if removed_features:
                fail('registered features were removed: ' + ', '.join(removed_features))

            weakened: list[str] = []
            for feature_id, base_paths in sorted(base.items()):
                removed_paths = sorted(base_paths - head[feature_id])
                if removed_paths:
                    weakened.append(f"{feature_id}: {', '.join(removed_paths)}")
            if weakened:
                fail('registered feature guarantees were weakened:\n  - ' + '\n  - '.join(weakened))

    print(f'feature-preservation: OK ({len(head)} registered features)')


if __name__ == '__main__':
    main()

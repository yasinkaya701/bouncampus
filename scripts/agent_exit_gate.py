#!/usr/bin/env python3
"""Fail unless an accepted agent branch head is present on merged master.

This gate is intentionally local/Git-based so any engineering agent can prove that
its accepted work reached repository truth before reporting completion.

Normal BOUNCAMPUS integration uses a merge commit. Therefore the exact agent head
must be an ancestor of the verified master ref.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def resolve(ref: str) -> str:
    result = git("rev-parse", "--verify", ref, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"cannot resolve git ref {ref!r}: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Require the accepted agent branch head to be merged into verified master before exit."
    )
    parser.add_argument(
        "--branch-head",
        required=True,
        help="Exact agent branch head SHA that was validated before merge.",
    )
    parser.add_argument(
        "--master-ref",
        default="origin/master",
        help="Verified master ref after merge (default: origin/master).",
    )
    args = parser.parse_args()

    try:
        branch_head = resolve(args.branch_head)
        master_head = resolve(args.master_ref)
    except RuntimeError as exc:
        print(f"AGENT EXIT GATE: FAIL: {exc}", file=sys.stderr)
        return 2

    ancestry = git("merge-base", "--is-ancestor", branch_head, master_head, check=False)
    if ancestry.returncode != 0:
        print(
            "AGENT EXIT GATE: FAIL\n"
            f"accepted branch head {branch_head} is not an ancestor of {args.master_ref} ({master_head}).\n"
            "The work is still unmerged, was squash-rewritten, or master has not been refreshed.\n"
            "Do not report DONE or exit. Update from master, finish the integration PR, perform a normal merge, "
            "refresh master, verify it, and run this gate again.",
            file=sys.stderr,
        )
        return 1

    print(
        "AGENT EXIT GATE: PASS\n"
        f"accepted branch head: {branch_head}\n"
        f"verified master head: {master_head}\n"
        "The accepted work is contained in master. The agent may release ownership after required post-merge checks pass."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

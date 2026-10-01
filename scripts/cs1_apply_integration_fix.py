#!/usr/bin/env python3
"""Apply the deterministic CS1/master convergence edits once."""

from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor changed in {path}: {old!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    replace_once(
        "frontend/src/lib/food-waste.ts",
        "  recommendedTarget: number | null;",
        "  recommendedTarget: number;",
    )
    replace_once(
        "frontend/src/lib/food-waste.ts",
        "    recommendedTarget: abstained ? null : demand,",
        "    recommendedTarget: demand,",
    )

    page_anchor = (
        "                      <div className=\"text-[8px] font-medium text-[#778079]\">"
        "{band?.provenance ?? 'MODEL_ESTIMATE'}</div>\n"
    )
    page_disclosure = page_anchor + (
        "                      <div className=\"mt-1 text-[7px] font-semibold tracking-[0.04em] text-[#667068]\">"
        "MODEL_ESTIMATE · POLICY_HEURISTIC · PLANNING_RANGE_NOT_CALIBRATED_INTERVAL · NOT_CALIBRATED"
        "</div>\n"
    )
    replace_once("frontend/src/app/food-waste/page.tsx", page_anchor, page_disclosure)

    workflow_anchor = "      - run: npm ci --no-audit --no-fund\n      - run: npm run typecheck\n"
    workflow_targeted = """      - run: npm ci --no-audit --no-fund
      - name: Run CS1 frontend decision regressions when present
        run: |
          set -euo pipefail
          if [ -f scripts/campus-operations.test.mjs ]; then npm run test:campus-operations; fi
          if [ -f scripts/shuttle-frequency.test.mjs ]; then node --experimental-strip-types scripts/shuttle-frequency.test.mjs; fi
          if [ -f scripts/shuttle-navigation.test.mjs ]; then node --experimental-strip-types scripts/shuttle-navigation.test.mjs; fi
          if [ -f scripts/food-diagnostic-eligibility.test.mjs ]; then node --experimental-strip-types scripts/food-diagnostic-eligibility.test.mjs; fi
      - run: npm run typecheck
"""
    replace_once(".github/workflows/ci-hosted-fallback.yml", workflow_anchor, workflow_targeted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

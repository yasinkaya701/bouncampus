"""Conflict-aware hardening for the CS1 class room/slot optimizer.

The base class-assignment solver owns room capacity, room feature, room/slot
collision, and building mismatch logic. This module adds a separate hard constraint
for classes that must not overlap in time (for example, a shared instructor or
student cohort) without duplicating the room solver.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

from app.decision.class_assignment import _base, optimize_class_schedule

MAX_CONFLICT_SLOT_PLANS = 20_000


def _conflict_keys(value: Any) -> set[str] | None:
    if value is None:
        return set()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return None
    return {str(item).strip() for item in value if str(item).strip()}


def _withhold(reason: str, *, conflict_key_count: int = 0, plans_evaluated: int = 0) -> dict[str, Any]:
    return {
        **_base("CLASS_ROOM_SLOT_RECOMMENDATION"),
        "decision_readiness": "WITHHOLD",
        "assignments": [],
        "conflict_constraints_enforced": conflict_key_count > 0,
        "conflict_key_count": conflict_key_count,
        "conflict_slot_plans_evaluated": plans_evaluated,
        "reason_codes": [reason],
    }


def _assignment_signature(result: Mapping[str, Any]) -> tuple[tuple[str, str, str], ...]:
    rows = result.get("assignments") or []
    return tuple(
        sorted(
            (
                str(row.get("class_id") or ""),
                str(row.get("slot") or ""),
                str(row.get("room_id") or ""),
            )
            for row in rows
            if isinstance(row, Mapping)
        )
    )


def optimize_conflict_aware_class_schedule(
    *,
    classes: Sequence[Mapping[str, Any]],
    rooms: Sequence[Mapping[str, Any]],
    building_mismatch_weight: Any = 0.0,
) -> dict[str, Any]:
    """Optimize room/slot assignments while enforcing caller-declared conflicts.

    Each class may declare ``conflict_keys`` such as ``instructor:I1`` or
    ``cohort:CMPE-1``. Classes sharing any key may not occupy the same slot.
    Keys are opaque caller-provided identifiers; this layer does not infer them.

    To preserve one source of truth for room feasibility, this function searches
    only the conflict-constrained slot choices and delegates every candidate to
    ``class_assignment.optimize_class_schedule`` for room assignment and objective
    scoring.
    """

    if not isinstance(classes, Sequence) or isinstance(classes, (str, bytes)):
        return optimize_class_schedule(
            classes=classes,
            rooms=rooms,
            building_mismatch_weight=building_mismatch_weight,
        )

    parsed: list[dict[str, Any]] = []
    all_keys: set[str] = set()
    for index, item in enumerate(classes):
        if not isinstance(item, Mapping):
            return optimize_class_schedule(
                classes=classes,
                rooms=rooms,
                building_mismatch_weight=building_mismatch_weight,
            )

        keys = _conflict_keys(item.get("conflict_keys"))
        if keys is None:
            return _withhold("INVALID_CLASS_CONFLICT_KEYS")
        all_keys.update(keys)
        if not keys:
            continue

        class_id = str(item.get("class_id") or "").strip()
        slots = item.get("allowed_slots", [])
        if not class_id or not isinstance(slots, Sequence) or isinstance(slots, (str, bytes)):
            return optimize_class_schedule(
                classes=classes,
                rooms=rooms,
                building_mismatch_weight=building_mismatch_weight,
            )
        allowed_slots = sorted({str(slot).strip() for slot in slots if str(slot).strip()})
        if not allowed_slots:
            return optimize_class_schedule(
                classes=classes,
                rooms=rooms,
                building_mismatch_weight=building_mismatch_weight,
            )
        parsed.append(
            {
                "index": index,
                "class_id": class_id,
                "keys": keys,
                "slots": allowed_slots,
            }
        )

    if not parsed:
        result = optimize_class_schedule(
            classes=classes,
            rooms=rooms,
            building_mismatch_weight=building_mismatch_weight,
        )
        return {
            **result,
            "conflict_constraints_enforced": False,
            "conflict_key_count": 0,
            "conflict_slot_plans_evaluated": 0,
        }

    parsed.sort(key=lambda row: (len(row["slots"]), -len(row["keys"]), row["class_id"], row["index"]))
    used_by_slot: dict[str, set[str]] = {}
    selected_slots: dict[int, str] = {}
    plans_evaluated = 0
    complete_slot_plans = 0
    search_limit_hit = False
    best: tuple[float, tuple[tuple[str, str, str], ...], dict[str, Any]] | None = None

    def evaluate_slot_plan() -> None:
        nonlocal plans_evaluated, complete_slot_plans, search_limit_hit, best
        complete_slot_plans += 1
        if plans_evaluated >= MAX_CONFLICT_SLOT_PLANS:
            search_limit_hit = True
            return
        plans_evaluated += 1

        locked_classes: list[dict[str, Any]] = []
        for index, item in enumerate(classes):
            row = dict(item)
            if index in selected_slots:
                row["allowed_slots"] = [selected_slots[index]]
            locked_classes.append(row)

        candidate = optimize_class_schedule(
            classes=locked_classes,
            rooms=rooms,
            building_mismatch_weight=building_mismatch_weight,
        )
        if candidate.get("decision_readiness") == "WITHHOLD":
            return

        raw_loss = candidate.get("total_registered_loss")
        try:
            loss = float(raw_loss)
        except (TypeError, ValueError):
            return
        if not math.isfinite(loss):
            return
        signature = _assignment_signature(candidate)
        ranked = (loss, signature, candidate)
        if best is None or ranked[:2] < best[:2]:
            best = ranked

    def search(position: int) -> None:
        nonlocal search_limit_hit
        if search_limit_hit:
            return
        if position == len(parsed):
            evaluate_slot_plan()
            return

        row = parsed[position]
        keys: set[str] = row["keys"]
        index = int(row["index"])
        for slot in row["slots"]:
            bucket = used_by_slot.setdefault(slot, set())
            if bucket.intersection(keys):
                continue
            bucket.update(keys)
            selected_slots[index] = slot
            search(position + 1)
            selected_slots.pop(index, None)
            bucket.difference_update(keys)
            if not bucket:
                used_by_slot.pop(slot, None)
            if search_limit_hit:
                return

    search(0)

    if best is None:
        if search_limit_hit:
            reason = "CLASS_CONFLICT_SEARCH_LIMIT_EXCEEDED"
        elif complete_slot_plans == 0:
            reason = "NO_CONFLICT_FREE_CLASS_SCHEDULE"
        else:
            reason = "NO_CONFLICT_AND_ROOM_FEASIBLE_CLASS_SCHEDULE"
        return _withhold(
            reason,
            conflict_key_count=len(all_keys),
            plans_evaluated=plans_evaluated,
        )

    result = best[2]
    reason_codes = list(result.get("reason_codes") or [])
    if "CLASS_CONFLICT_KEYS_ENFORCED" not in reason_codes:
        reason_codes.append("CLASS_CONFLICT_KEYS_ENFORCED")
    return {
        **result,
        "conflict_constraints_enforced": True,
        "conflict_key_count": len(all_keys),
        "conflict_slot_plans_evaluated": plans_evaluated,
        "reason_codes": reason_codes,
    }
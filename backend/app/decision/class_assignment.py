"""Polynomial room/slot assignment solver for CS1 campus operations."""

from __future__ import annotations

import heapq
import math
from typing import Any, Mapping, Sequence

POLICY_VERSION = "campus-ops-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
POLICY_INPUT_PROVENANCE = "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS"


def _base(scope: str) -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": scope,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": POLICY_INPUT_PROVENANCE,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
    }


def _number(value: Any, *, minimum: float | None = None) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    if minimum is not None and numeric < minimum:
        return None
    return numeric


def _text(value: Any) -> str | None:
    normalized = str(value or "").strip()
    return normalized or None


class _Edge:
    __slots__ = ("to", "rev", "cap", "cost", "meta")

    def __init__(
        self,
        to: int,
        rev: int,
        cap: int,
        cost: float,
        meta: dict[str, Any] | None = None,
    ) -> None:
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost
        self.meta = meta


def _add_edge(
    graph: list[list[_Edge]],
    source: int,
    target: int,
    cost: float,
    *,
    meta: dict[str, Any] | None = None,
) -> None:
    forward = _Edge(target, len(graph[target]), 1, cost, meta)
    reverse = _Edge(source, len(graph[source]), 0, -cost, None)
    graph[source].append(forward)
    graph[target].append(reverse)


def _min_cost_assignment(
    candidates_by_class: Mapping[str, Sequence[tuple[float, str, str]]],
) -> tuple[float, list[dict[str, Any]]] | None:
    class_ids = sorted(candidates_by_class)
    resources = sorted(
        {
            (slot, room_id)
            for candidates in candidates_by_class.values()
            for _score, slot, room_id in candidates
        }
    )
    if len(resources) < len(class_ids):
        return None

    class_node = {cid: index + 1 for index, cid in enumerate(class_ids)}
    resource_offset = 1 + len(class_ids)
    resource_node = {
        resource: resource_offset + index for index, resource in enumerate(resources)
    }
    sink = resource_offset + len(resources)
    graph: list[list[_Edge]] = [[] for _ in range(sink + 1)]
    source = 0

    for class_id in class_ids:
        _add_edge(graph, source, class_node[class_id], 0.0)
        for score, slot, room_id in sorted(candidates_by_class[class_id]):
            _add_edge(
                graph,
                class_node[class_id],
                resource_node[(slot, room_id)],
                float(score),
                meta={
                    "class_id": class_id,
                    "slot": slot,
                    "room_id": room_id,
                    "assignment_loss": float(score),
                },
            )
    for node in resource_node.values():
        _add_edge(graph, node, sink, 0.0)

    node_count = len(graph)
    potential = [0.0] * node_count
    flow = 0
    total_cost = 0.0
    target_flow = len(class_ids)
    epsilon = 1e-12

    while flow < target_flow:
        distance = [math.inf] * node_count
        previous_node = [-1] * node_count
        previous_edge = [-1] * node_count
        distance[source] = 0.0
        queue: list[tuple[float, int]] = [(0.0, source)]

        while queue:
            current_distance, node = heapq.heappop(queue)
            if current_distance > distance[node] + epsilon:
                continue
            for edge_index, edge in enumerate(graph[node]):
                if edge.cap <= 0:
                    continue
                reduced = edge.cost + potential[node] - potential[edge.to]
                if reduced < 0 and reduced > -epsilon:
                    reduced = 0.0
                candidate_distance = current_distance + reduced
                if candidate_distance < distance[edge.to] - epsilon:
                    distance[edge.to] = candidate_distance
                    previous_node[edge.to] = node
                    previous_edge[edge.to] = edge_index
                    heapq.heappush(queue, (candidate_distance, edge.to))

        if not math.isfinite(distance[sink]):
            return None

        for node, value in enumerate(distance):
            if math.isfinite(value):
                potential[node] += value

        node = sink
        path_cost = 0.0
        while node != source:
            parent = previous_node[node]
            edge_index = previous_edge[node]
            if parent < 0 or edge_index < 0:
                return None
            edge = graph[parent][edge_index]
            path_cost += edge.cost
            edge.cap -= 1
            graph[node][edge.rev].cap += 1
            node = parent
        total_cost += path_cost
        flow += 1

    assignments: list[dict[str, Any]] = []
    for class_id in class_ids:
        node = class_node[class_id]
        selected = [
            edge.meta
            for edge in graph[node]
            if edge.meta is not None and edge.cap == 0
        ]
        if len(selected) != 1:
            return None
        assignments.append(dict(selected[0]))
    assignments.sort(key=lambda row: row["class_id"])
    return total_cost, assignments


def optimize_class_schedule(
    *,
    classes: Sequence[Mapping[str, Any]],
    rooms: Sequence[Mapping[str, Any]],
    building_mismatch_weight: Any = 0.0,
    solar_exposure_weight: Any = 0.0,
) -> dict[str, Any]:
    result = _base("CLASS_ROOM_SLOT_RECOMMENDATION")
    mismatch = _number(building_mismatch_weight, minimum=0.0)
    solar_weight = _number(solar_exposure_weight, minimum=0.0)
    if (
        mismatch is None
        or solar_weight is None
        or not isinstance(classes, Sequence)
        or isinstance(classes, (str, bytes))
        or not isinstance(rooms, Sequence)
        or isinstance(rooms, (str, bytes))
        or not classes
        or not rooms
    ):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
        }

    normalized_rooms: list[dict[str, Any]] = []
    room_ids: set[str] = set()
    for room in rooms:
        room_id = _text(room.get("room_id")) if isinstance(room, Mapping) else None
        capacity = (
            _number(room.get("capacity"), minimum=0.0)
            if isinstance(room, Mapping)
            else None
        )
        features = room.get("features", []) if isinstance(room, Mapping) else []
        if (
            room_id is None
            or room_id in room_ids
            or capacity is None
            or not isinstance(features, Sequence)
            or isinstance(features, (str, bytes))
        ):
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
            }

        solar_by_slot: dict[str, float] = {}
        if solar_weight > 0.0:
            raw_solar = room.get("solar_load_by_slot", {}) if isinstance(room, Mapping) else {}
            if not isinstance(raw_solar, Mapping):
                return {
                    **result,
                    "decision_readiness": "WITHHOLD",
                    "assignments": [],
                    "reason_codes": ["INVALID_ROOM_SOLAR_LOAD"],
                }
            for raw_slot, raw_value in raw_solar.items():
                slot = str(raw_slot).strip()
                value = _number(raw_value, minimum=0.0)
                if not slot or value is None or value > 1.0:
                    return {
                        **result,
                        "decision_readiness": "WITHHOLD",
                        "assignments": [],
                        "reason_codes": ["INVALID_ROOM_SOLAR_LOAD"],
                    }
                solar_by_slot[slot] = value

        room_ids.add(room_id)
        normalized_rooms.append(
            {
                "room_id": room_id,
                "capacity": capacity,
                "features": {
                    str(feature).strip()
                    for feature in features
                    if str(feature).strip()
                },
                "building": _text(room.get("building")),
                "solar_load_by_slot": solar_by_slot,
            }
        )

    room_by_id = {room["room_id"]: room for room in normalized_rooms}
    candidates_by_class: dict[str, list[tuple[float, str, str]]] = {}
    seen_classes: set[str] = set()
    for item in classes:
        if not isinstance(item, Mapping):
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
            }
        class_id = _text(item.get("class_id"))
        attendance = _number(item.get("planning_attendance"), minimum=0.0)
        slots = item.get("allowed_slots", [])
        features = item.get("required_features", [])
        preferred_building = _text(item.get("preferred_building"))
        if (
            class_id is None
            or class_id in seen_classes
            or attendance is None
            or not isinstance(slots, Sequence)
            or isinstance(slots, (str, bytes))
            or not isinstance(features, Sequence)
            or isinstance(features, (str, bytes))
        ):
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
            }
        seen_classes.add(class_id)
        allowed_slots = sorted(
            {str(slot).strip() for slot in slots if str(slot).strip()}
        )
        required = {
            str(feature).strip() for feature in features if str(feature).strip()
        }
        candidates: list[tuple[float, str, str]] = []
        for slot in allowed_slots:
            for room in normalized_rooms:
                if (
                    room["capacity"] + 1e-9 < attendance
                    or not required.issubset(room["features"])
                ):
                    continue
                score = room["capacity"] - attendance
                if preferred_building and room["building"] != preferred_building:
                    score += mismatch
                if solar_weight > 0.0:
                    score += solar_weight * room["solar_load_by_slot"].get(slot, 0.0)
                candidates.append((score, slot, room["room_id"]))
        if not candidates:
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["CLASS_CONSTRAINTS_INFEASIBLE"],
            }
        candidates_by_class[class_id] = candidates

    solved = _min_cost_assignment(candidates_by_class)
    if solved is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "reason_codes": ["NO_COLLISION_FREE_CLASS_SCHEDULE"],
        }
    total_loss, assignments = solved
    if solar_weight > 0.0:
        for assignment in assignments:
            room = room_by_id[assignment["room_id"]]
            exposure = room["solar_load_by_slot"].get(assignment["slot"], 0.0)
            assignment["solar_exposure_index"] = exposure
            assignment["solar_loss_component"] = solar_weight * exposure

    reason_codes = ["OPERATOR_REVIEW_REQUIRED"]
    if solar_weight > 0.0:
        reason_codes.append("SOLAR_EXPOSURE_LOSS_ACTIVE")
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "assignments": assignments,
        "total_registered_loss": total_loss,
        "solver_semantics": "MIN_COST_BIPARTITE_ROOM_SLOT_ASSIGNMENT",
        "reason_codes": reason_codes,
    }
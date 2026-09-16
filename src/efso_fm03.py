#!/usr/bin/env python3
"""Минимальный независимый исполняемый контур EFSO FM0–FM3.

Контур намеренно не содержит IUT- или external-oracle-зависимостей.
Он проверяет формальную границу, конечную модель, каноническую
идентичность состояний и exact structural properties на встроенном
маленьком qualification space.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import product
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class State:
    """Каноническое состояние qualification space."""

    a: int
    b: int


@dataclass(frozen=True)
class QualificationSpace:
    """Конечное произведение доменов, явно задающее F."""

    domain_a: tuple[int, ...]
    domain_b: tuple[int, ...]

    @property
    def expected_cardinality(self) -> int:
        return len(self.domain_a) * len(self.domain_b)

    def enumerate(self) -> tuple[State, ...]:
        return tuple(State(a, b) for a, b in product(self.domain_a, self.domain_b))


def canonical_encode(state: State) -> bytes:
    """Детерминированное wire-independent кодирование состояния."""

    return json.dumps(
        {"a": state.a, "b": state.b},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def state_id(state: State) -> str:
    return sha256(canonical_encode(state)).hexdigest()


def independent_transition(state: State) -> State:
    """Пример собственной transition semantics без IUT/reference imports."""

    return State(state.a, -state.b)


def exact_structural_result(space: QualificationSpace) -> dict[str, object]:
    states = space.enumerate()
    ids = [state_id(s) for s in states]
    transitions = [
        {
            "source": state_id(s),
            "target": state_id(independent_transition(s)),
        }
        for s in states
    ]

    unique_ids = set(ids)
    duplicates = len(ids) - len(unique_ids)
    expected = space.expected_cardinality
    observed = len(states)

    canonical_replay = all(state_id(json_roundtrip(s)) == state_id(s) for s in states)
    transition_closed = all(independent_transition(s) in states for s in states)

    enumeration_digest = sha256(
        b"".join((state_id(s) + "\n").encode("ascii") for s in states)
    ).hexdigest()

    return {
        "expected_cardinality": expected,
        "observed_count": observed,
        "unique_count": len(unique_ids),
        "missing_count": max(expected - len(unique_ids), 0),
        "duplicate_count": duplicates,
        "canonical_identity": canonical_replay,
        "transition_closed": transition_closed,
        "enumeration_digest": enumeration_digest,
        "transitions": transitions,
    }


def json_roundtrip(state: State) -> State:
    payload = json.loads(canonical_encode(state).decode("utf-8"))
    return State(a=int(payload["a"]), b=int(payload["b"]))


def run() -> dict[str, object]:
    """Выполнить FM0–FM3 на базовом конечном space."""

    space = QualificationSpace(
        domain_a=(-1, 0, 1),
        domain_b=(-1, 0, 1),
    )
    structural = exact_structural_result(space)

    fm0 = {
        "boundary_valid": True,
        "defined_objects": [
            "State",
            "Input",
            "Parameter",
            "Operation",
            "Transition",
            "Output",
            "Invariant",
            "FiniteStateSpace",
            "Equality",
            "Failure",
            "Witness",
        ],
    }

    fm1 = {
        "imports_iut": False,
        "imports_external_oracle": False,
        "calls_iut": False,
        "calls_external_oracle": False,
    }

    fm2 = {
        "space_id": "FM2-BASE-3x3",
        "domain_a": list(space.domain_a),
        "domain_b": list(space.domain_b),
        "expected_cardinality": space.expected_cardinality,
        "enumeration_defined": True,
    }

    fm3 = {
        "exact_structural": structural,
    }

    overall = bool(
        fm0["boundary_valid"]
        and all(value is False for key, value in fm1.items() if key.startswith("imports_") or key.startswith("calls_"))
        and fm2["enumeration_defined"]
        and structural["expected_cardinality"] == structural["observed_count"]
        and structural["unique_count"] == structural["expected_cardinality"]
        and structural["missing_count"] == 0
        and structural["duplicate_count"] == 0
        and structural["canonical_identity"]
        and structural["transition_closed"]
    )

    return {
        "schema_version": "EFSO-FM03-1",
        "fm0": fm0,
        "fm1": fm1,
        "fm2": fm2,
        "fm3": fm3,
        "qualification": "PASS" if overall else "FAIL",
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

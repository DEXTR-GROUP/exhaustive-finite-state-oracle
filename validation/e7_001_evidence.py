#!/usr/bin/env python3
"""E7-001: exhaustive qualification of the independent invariant engine."""

from __future__ import annotations

import json
import math
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_invariants import InvariantSpec, check_invariants
from efso_r4_evaluator import evaluate
from efso_r4_space import R4FiniteSpace, R4State, enumerate_r4_space

EXPECTED_COUNT = 59049
VALUES = frozenset((-1, 0, 1))


def valid_shape(state: R4State) -> bool:
    return (
        len(state.query) == 2
        and len(state.key) == 2
        and len(state.value) == 2
        and all(len(row) == 2 for row in state.key)
        and all(len(row) == 2 for row in state.value)
    )


def valid_domain(state: R4State) -> bool:
    scalars = tuple(state.query) + tuple(x for row in state.key for x in row) + tuple(
        x for row in state.value for x in row
    )
    return all(x in VALUES for x in scalars)


def valid_identity(state: R4State) -> bool:
    return bool(state.id()) and len(state.id()) == 64


def valid_output(state: R4State) -> bool:
    output = evaluate(state)
    return len(output) == 2 and all(math.isfinite(float(x)) for x in output)


def main() -> None:
    states = enumerate_r4_space()
    space = R4FiniteSpace()
    invariants = (
        InvariantSpec("shape", valid_shape),
        InvariantSpec("finite_domain", valid_domain),
        InvariantSpec("canonical_identity", valid_identity),
        InvariantSpec("finite_output", valid_output),
    )
    report = check_invariants(
        states,
        invariants,
        expected_count=EXPECTED_COUNT,
        replay_factory=enumerate_r4_space,
    )

    state_digest = sha256(
        b"".join(state.id().encode("ascii") + b"\n" for state in states)
    ).hexdigest()

    evidence = {
        "schema_version": "EFSO-E7-001-1",
        "check_id": "E7-001",
        "scope": "independent exhaustive invariant engine qualification",
        "finite_space": "R4-DOMAIN-3^10",
        "expected_count": EXPECTED_COUNT,
        "observed_count": report.observed_count,
        "checked_count": report.checked_count,
        "invariant_count": len(invariants),
        "invariants": [spec.name for spec in invariants],
        "exhaustive": report.exhaustive,
        "deterministic_replay": report.deterministic_replay,
        "violation_count": report.violation_count,
        "first_violation": None if report.first_violation is None else {
            "index": report.first_violation.index,
            "state_id": report.first_violation.state_id,
            "invariant": report.first_violation.invariant,
        },
        "state_digest": state_digest,
        "space_cardinality": space.expected_cardinality,
        "qualification": report.qualification,
        "source_commit": __import__("os").environ.get("GITHUB_SHA", "UNKNOWN"),
    }

    output = ROOT / "evidence" / "e7_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not report.conformant:
        raise SystemExit(f"E7-001 failed: {report.violation_count} violations")
    print(output)


if __name__ == "__main__":
    main()

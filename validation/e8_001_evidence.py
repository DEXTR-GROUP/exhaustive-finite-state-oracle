#!/usr/bin/env python3
"""E8-001: deterministic counterexample extraction and minimization."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_counterexample import first_failure, minimize_counterexample


@dataclass(frozen=True)
class State:
    value: int

    def id(self) -> str:
        return f"state-{self.value}"


def compare(actual: int, expected: int) -> tuple[bool, str, float | None]:
    if actual == expected:
        return True, "", 0.0
    return False, "numeric mismatch", float(abs(actual - expected))


def shrink(state: State):
    if state.value <= 0:
        return ()
    return (State(state.value // 2), State(max(0, state.value - 1)))


def observe(state: State) -> tuple[int, int, str, float]:
    actual = state.value
    expected = 0
    return actual, expected, "injected failure", float(abs(actual - expected))


def main() -> None:
    states = tuple(State(i) for i in range(8))
    actual = tuple(i for i in range(8))
    expected = tuple(0 if i == 7 else i for i in range(8))

    initial = first_failure(states, actual, expected, compare)
    if initial is None:
        raise SystemExit("E8-001 failed: qualification fixture produced no counterexample")

    def fails(state: State) -> bool:
        return state.value >= 4

    minimized = minimize_counterexample(
        initial,
        fails,
        shrink,
        observe=observe,
    )
    replay = minimize_counterexample(
        initial,
        fails,
        shrink,
        observe=observe,
    )
    reproducible = minimized == replay
    state_consistent = (
        minimized.actual == minimized.state.value
        and minimized.expected == 0
        and minimized.max_abs_error == float(minimized.state.value)
    )

    evidence = {
        "schema_version": "EFSO-E8-001-2",
        "check_id": "E8-001",
        "scope": "deterministic counterexample extraction and minimization engine qualification",
        "finite_fixture": {
            "state_count": len(states),
            "state_domain": [0, 7],
            "injected_failure": "state.value >= 4",
        },
        "initial_counterexample": asdict(initial),
        "minimized_counterexample": asdict(minimized),
        "reproducible_minimization": reproducible,
        "state_consistent_witness": state_consistent,
        "minimization_rule": "accept first failing shrink candidate and repeat until no candidate preserves failure",
        "randomness": False,
        "external_runtime_dependency": False,
        "qualification": "PASS"
        if reproducible and state_consistent and minimized.state.value == 4
        else "FAIL",
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }

    output = ROOT / "evidence" / "e8_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )

    if evidence["qualification"] != "PASS":
        raise SystemExit("E8-001 failed: counterexample qualification did not close")
    print(output)


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from dataclasses import dataclass

sys.path.insert(0, "src")

from efso_counterexample import Counterexample, first_failure, minimize_counterexample


@dataclass(frozen=True)
class State:
    value: int

    def id(self) -> str:
        return f"state-{self.value}"


def compare(actual: int, expected: int) -> tuple[bool, str, float | None]:
    if actual == expected:
        return True, "", 0.0
    return False, "numeric mismatch", float(abs(actual - expected))


def test_first_failure_is_deterministic() -> None:
    states = tuple(State(i) for i in range(8))
    actual = tuple(i for i in range(8))
    expected = tuple(0 if i == 3 else i for i in range(8))

    witness = first_failure(states, actual, expected, compare)

    assert witness == Counterexample(
        index=3,
        state_id="state-3",
        state=State(3),
        actual=3,
        expected=0,
        reason="numeric mismatch",
        max_abs_error=3.0,
    )


def test_minimization_reaches_smallest_failure_and_recomputes_values() -> None:
    witness = Counterexample(
        index=7,
        state_id="state-7",
        state=State(7),
        actual=7,
        expected=0,
        reason="injected failure",
        max_abs_error=7.0,
    )

    def fails(state: State) -> bool:
        return state.value >= 4

    def shrink(state: State):
        return (State(state.value // 2), State(max(0, state.value - 1)))

    def observe(state: State):
        return state.value, 0, "injected failure", float(state.value)

    minimized = minimize_counterexample(witness, fails, shrink, observe=observe)

    assert minimized.state == State(4)
    assert minimized.state_id == "state-4"
    assert minimized.actual == 4
    assert minimized.expected == 0
    assert minimized.max_abs_error == 4.0


def test_minimization_replay_is_reproducible() -> None:
    witness = Counterexample(
        index=9,
        state_id="state-9",
        state=State(9),
        actual=9,
        expected=-1,
        reason="injected failure",
        max_abs_error=10.0,
    )

    def fails(state: State) -> bool:
        return state.value >= 5

    def shrink(state: State):
        return (State(state.value - 2), State(state.value // 2))

    def observe(state: State):
        return state.value, 0, "injected failure", float(state.value)

    a = minimize_counterexample(witness, fails, shrink, observe=observe)
    b = minimize_counterexample(witness, fails, shrink, observe=observe)

    assert a == b

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar

StateT = TypeVar("StateT")


@dataclass(frozen=True)
class InvariantSpec(Generic[StateT]):
    """Named predicate that must hold for every state in a finite space."""

    name: str
    predicate: Callable[[StateT], bool]


@dataclass(frozen=True)
class InvariantViolation(Generic[StateT]):
    index: int
    state_id: str
    invariant: str
    state: StateT


@dataclass(frozen=True)
class InvariantReport(Generic[StateT]):
    expected_count: int
    observed_count: int
    checked_count: int
    violation_count: int
    first_violation: InvariantViolation[StateT] | None
    deterministic_replay: bool
    qualification: str

    @property
    def exhaustive(self) -> bool:
        return self.expected_count == self.observed_count == self.checked_count

    @property
    def conformant(self) -> bool:
        return self.exhaustive and self.violation_count == 0 and self.deterministic_replay


def check_invariants(
    states: Iterable[StateT],
    invariants: Iterable[InvariantSpec[StateT]],
    *,
    expected_count: int | None = None,
    state_id: Callable[[StateT], str] | None = None,
    replay_factory: Callable[[], Iterable[StateT]] | None = None,
) -> InvariantReport[StateT]:
    """Exhaustively evaluate independent state invariants.

    ``replay_factory`` is required to make the replay check meaningful. When
    supplied, it must independently produce the same finite enumeration.
    """
    materialized = tuple(states)
    specs = tuple(invariants)
    observed_count = len(materialized)
    expected = observed_count if expected_count is None else expected_count
    identify = state_id or (lambda state: str(getattr(state, "id")()))

    violations: list[InvariantViolation[StateT]] = []
    for index, state in enumerate(materialized):
        for spec in specs:
            if not spec.predicate(state):
                violations.append(
                    InvariantViolation(
                        index=index,
                        state_id=identify(state),
                        invariant=spec.name,
                        state=state,
                    )
                )

    if replay_factory is None:
        replay = False
    else:
        replay_ids = tuple(identify(state) for state in replay_factory())
        replay = tuple(identify(state) for state in materialized) == replay_ids

    report = InvariantReport(
        expected_count=expected,
        observed_count=observed_count,
        checked_count=observed_count,
        violation_count=len(violations),
        first_violation=violations[0] if violations else None,
        deterministic_replay=replay,
        qualification="PASS"
        if expected == observed_count and not violations and replay
        else "FAIL",
    )
    return report

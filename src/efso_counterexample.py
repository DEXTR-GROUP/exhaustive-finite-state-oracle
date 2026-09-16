#!/usr/bin/env python3
"""E8: deterministic counterexample extraction and minimization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence


@dataclass(frozen=True)
class Counterexample:
    """Minimal reproducible witness for one failed finite-state check."""

    index: int
    state_id: str
    state: Any
    actual: Any
    expected: Any
    reason: str
    max_abs_error: float | None = None


def first_failure(
    states: Sequence[Any],
    actual: Sequence[Any],
    expected: Sequence[Any],
    compare: Callable[[Any, Any], tuple[bool, str, float | None]],
    *,
    state_id: Callable[[Any], str] | None = None,
) -> Counterexample | None:
    """Return the first reproducible failure in deterministic enumeration order."""
    identify = state_id or (lambda state: str(getattr(state, "id")()))
    limit = min(len(states), len(actual), len(expected))
    for index in range(limit):
        equal, reason, error = compare(actual[index], expected[index])
        if not equal:
            return Counterexample(
                index=index,
                state_id=identify(states[index]),
                state=states[index],
                actual=actual[index],
                expected=expected[index],
                reason=reason,
                max_abs_error=error,
            )

    if len(states) != len(actual) or len(states) != len(expected):
        index = limit
        state = states[index] if index < len(states) else None
        return Counterexample(
            index=index,
            state_id=identify(state) if state is not None else "<none>",
            state=state,
            actual=actual[index] if index < len(actual) else None,
            expected=expected[index] if index < len(expected) else None,
            reason="cardinality mismatch",
            max_abs_error=None,
        )
    return None


def minimize_counterexample(
    witness: Counterexample,
    fails: Callable[[Any], bool],
    shrink: Callable[[Any], Iterable[Any]],
    *,
    state_id: Callable[[Any], str] | None = None,
) -> Counterexample:
    """Deterministically shrink a witness while the failure remains true.

    Candidates are tested in the exact order returned by ``shrink``. The first
    failing candidate is accepted and shrinking continues until no candidate
    preserves the failure. No random search or external oracle is used.
    """
    identify = state_id or (lambda state: str(getattr(state, "id")()))
    current = witness
    changed = True
    while changed:
        changed = False
        for candidate in shrink(current.state):
            if candidate == current.state:
                continue
            if fails(candidate):
                current = Counterexample(
                    index=current.index,
                    state_id=identify(candidate),
                    state=candidate,
                    actual=current.actual,
                    expected=current.expected,
                    reason=current.reason,
                    max_abs_error=current.max_abs_error,
                )
                changed = True
                break
    return current

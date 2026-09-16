#!/usr/bin/env python3
"""E8: deterministic counterexample extraction and minimization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence


@dataclass(frozen=True)
class Counterexample:
    """Reproducible witness for one failed finite-state check."""

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
    """Return the first failure in deterministic enumeration order."""
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
    observe: Callable[[Any], tuple[Any, Any, str, float | None]] | None = None,
    state_id: Callable[[Any], str] | None = None,
) -> Counterexample:
    """Deterministically shrink a witness while preserving its failure.

    ``shrink`` defines the candidate order. If ``observe`` is supplied, the
    actual/expected values in the returned witness are recomputed for every
    accepted candidate, so the final witness is internally state-consistent.
    """
    identify = state_id or (lambda state: str(getattr(state, "id")()))
    current = witness
    changed = True
    while changed:
        changed = False
        for candidate in shrink(current.state):
            if candidate == current.state or not fails(candidate):
                continue
            if observe is None:
                actual, expected, reason, error = (
                    current.actual,
                    current.expected,
                    current.reason,
                    current.max_abs_error,
                )
            else:
                actual, expected, reason, error = observe(candidate)
            current = Counterexample(
                index=current.index,
                state_id=identify(candidate),
                state=candidate,
                actual=actual,
                expected=expected,
                reason=reason,
                max_abs_error=error,
            )
            changed = True
            break
    return current

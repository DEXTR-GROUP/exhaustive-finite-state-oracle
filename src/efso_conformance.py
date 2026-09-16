#!/usr/bin/env python3
"""Универсальный exhaustive conformance comparator EFSO (E6).

Компонент не знает IUT и не вызывает внешний oracle. Он получает уже
вычисленные результаты двух независимых контуров и проверяет их на каждом
состоянии конечного пространства.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class ConformanceMismatch:
    index: int
    state_id: str
    actual: Any
    expected: Any
    reason: str
    max_abs_error: float | None = None


@dataclass(frozen=True)
class ConformanceReport:
    expected_count: int
    actual_count: int
    mismatch_count: int
    max_abs_error: float
    first_mismatch: ConformanceMismatch | None
    qualification: str

    @property
    def exhaustive(self) -> bool:
        return self.actual_count == self.expected_count

    @property
    def conformant(self) -> bool:
        return self.exhaustive and self.mismatch_count == 0


def _numeric_leaves(value: Any) -> list[float]:
    if isinstance(value, bool):
        raise TypeError("boolean is not a numeric conformance value")
    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, (tuple, list)):
        leaves: list[float] = []
        for item in value:
            leaves.extend(_numeric_leaves(item))
        return leaves
    raise TypeError(f"unsupported conformance value: {type(value).__name__}")


def _compare_values(actual: Any, expected: Any, tolerance: float) -> tuple[bool, float, str | None]:
    try:
        actual_leaves = _numeric_leaves(actual)
        expected_leaves = _numeric_leaves(expected)
    except TypeError as exc:
        return False, 0.0, str(exc)

    if len(actual_leaves) != len(expected_leaves):
        return False, 0.0, "output shape mismatch"

    errors = [abs(a - e) for a, e in zip(actual_leaves, expected_leaves)]
    maximum = max(errors, default=0.0)
    equal = all(
        math.isclose(a, e, rel_tol=tolerance, abs_tol=tolerance)
        for a, e in zip(actual_leaves, expected_leaves)
    )
    return equal, maximum, None if equal else "numeric mismatch"


def exhaustive_compare(
    states: Sequence[Any],
    actual: Iterable[Any],
    expected: Sequence[Any],
    *,
    tolerance: float = 0.0,
) -> ConformanceReport:
    """Сравнить два результата строго в порядке exhaustive enumeration."""
    actual_values = tuple(actual)
    expected_count = len(states)
    actual_count = len(actual_values)

    mismatch_count = 0
    max_abs_error = 0.0
    first_mismatch: ConformanceMismatch | None = None

    limit = min(expected_count, actual_count, len(expected))
    for index in range(limit):
        state = states[index]
        equal, error, reason = _compare_values(actual_values[index], expected[index], tolerance)
        max_abs_error = max(max_abs_error, error)
        if not equal:
            mismatch_count += 1
            if first_mismatch is None:
                first_mismatch = ConformanceMismatch(
                    index=index,
                    state_id=state.id(),
                    actual=actual_values[index],
                    expected=expected[index],
                    reason=reason or "mismatch",
                    max_abs_error=error,
                )

    if actual_count != expected_count or len(expected) != expected_count:
        mismatch_count += abs(actual_count - expected_count) + abs(len(expected) - expected_count)
        if first_mismatch is None:
            first_mismatch = ConformanceMismatch(
                index=limit,
                state_id=states[limit].id() if limit < expected_count else "<none>",
                actual=actual_values[limit] if limit < actual_count else None,
                expected=expected[limit] if limit < len(expected) else None,
                reason="cardinality mismatch",
            )

    return ConformanceReport(
        expected_count=expected_count,
        actual_count=actual_count,
        mismatch_count=mismatch_count,
        max_abs_error=max_abs_error,
        first_mismatch=first_mismatch,
        qualification="PASS" if mismatch_count == 0 else "FAIL",
    )

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_r5_space import R5FiniteSpace, enumerate_r5_space


def test_r5_shape_and_parameter_count() -> None:
    space = R5FiniteSpace()
    assert space.input_width == 1
    assert space.hidden_width == 2
    assert space.scalar_parameter_count == 7
    assert space.expected_cardinality == 2187


def test_r5_exhaustive_identity_is_unique() -> None:
    states = enumerate_r5_space()
    assert len(states) == 2187
    assert len({state.id() for state in states}) == 2187


def test_r5_enumeration_is_deterministic() -> None:
    first = [state.id() for state in enumerate_r5_space()]
    second = [state.id() for state in enumerate_r5_space()]
    assert first == second

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_r6_space import EPSILON, R6FiniteSpace, R6State, enumerate_r6_space


def test_r6_shape_and_cardinality():
    space = R6FiniteSpace()
    assert space.scalar_parameter_count == 8
    assert space.expected_cardinality == 6561
    states = enumerate_r6_space()
    assert len(states) == 6561
    assert all(len(state.input) == 4 for state in states)
    assert all(len(state.attention_update) == 4 for state in states)
    assert all(state.canonical()["epsilon"] == EPSILON for state in states)


def test_r6_ids_unique():
    states = enumerate_r6_space()
    assert len({state.id() for state in states}) == 6561


def test_r6_identity_deterministic():
    state = R6State((1.0, 0.0, -1.0, 1.0), (0.0, 1.0, -1.0, 0.0))
    assert state.id() == state.id()
    assert state.canonical() == {
        "input": [1.0, 0.0, -1.0, 1.0],
        "attention_update": [0.0, 1.0, -1.0, 0.0],
        "epsilon": EPSILON,
    }

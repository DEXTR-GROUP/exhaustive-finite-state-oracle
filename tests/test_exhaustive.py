from itertools import product
from src.efso_exhaustive import exhaustive_enumerate, verify_reproducibility
from src.efso_fm03 import State, state_id

def enumerate_space():
    return tuple(State(a, b) for a, b in product((-1, 0, 1), repeat=2))

def test_exhaustive_cardinality_uniqueness_and_replay():
    states, evidence = exhaustive_enumerate(enumerate_space(), expected_count=9, identity=state_id, repeat_enumerator=enumerate_space)
    assert len(states) == 9
    assert evidence.observed_count == 9
    assert evidence.unique_count == 9
    assert evidence.duplicate_count == 0
    assert evidence.missing_count == 0
    assert evidence.deterministic_order
    assert evidence.passed

def test_reproducibility_is_exact():
    assert verify_reproducibility(enumerate_space, identity=state_id)

def test_duplicate_is_detected():
    states = enumerate_space() + (enumerate_space()[0],)
    _, evidence = exhaustive_enumerate(states, expected_count=9, identity=state_id, repeat_enumerator=lambda: states)
    assert evidence.observed_count == 10
    assert evidence.unique_count == 9
    assert evidence.duplicate_count == 1
    assert not evidence.passed

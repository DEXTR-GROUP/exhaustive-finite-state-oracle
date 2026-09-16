from src.efso_r4_space import R4FiniteSpace, enumerate_r4_space


def test_r4_shape_matches_primitive_attention_contract():
    space = R4FiniteSpace()
    assert space.width == 2
    assert space.sequence_length == 2
    assert space.scalar_parameter_count == 10
    assert space.expected_cardinality == 3**10


def test_r4_exhaustive_space_has_exact_cardinality_and_unique_identity():
    states = enumerate_r4_space()
    ids = [state.id() for state in states]
    assert len(states) == 59049
    assert len(set(ids)) == 59049


def test_r4_state_identity_is_deterministic():
    state = enumerate_r4_space()[12345]
    assert state.id() == state.id()
    assert state.encode() == state.encode()

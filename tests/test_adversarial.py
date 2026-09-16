from __future__ import annotations

import sys

sys.path.insert(0, "src")

from efso_adversarial import default_adversarial_spaces
from efso_r4_space import enumerate_r4_space


EXPECTED = {
    "R4-ADV-ALL-ZERO": 1,
    "R4-ADV-ALL-NEGATIVE": 1,
    "R4-ADV-ALL-POSITIVE": 1,
    "R4-ADV-BOUNDARY": 1024,
    "R4-ADV-ZERO-QUERY": 6561,
    "R4-ADV-SYMMETRIC-ROWS": 729,
    "R4-ADV-MIXED-SIGN": 57002,
}


def test_adversarial_spaces_have_expected_cardinality() -> None:
    states = enumerate_r4_space()
    spaces = default_adversarial_spaces()
    assert {space.space_id for space in spaces} == set(EXPECTED)
    for space in spaces:
        selected = space.enumerate(states)
        assert len(selected) == EXPECTED[space.space_id]
        assert len({state.id() for state in selected}) == len(selected)


def test_adversarial_enumeration_is_reproducible() -> None:
    states = enumerate_r4_space()
    for space in default_adversarial_spaces():
        first = tuple(state.id() for state in space.enumerate(states))
        second = tuple(state.id() for state in space.enumerate(states))
        assert first == second

#!/usr/bin/env python3
"""E10: deterministic adversarial subspaces over the R4 finite domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from efso_r4_space import R4State


@dataclass(frozen=True)
class AdversarialSpace:
    space_id: str
    purpose: str
    predicate: Callable[[R4State], bool]

    def enumerate(self, states: Iterable[R4State]) -> tuple[R4State, ...]:
        return tuple(state for state in states if self.predicate(state))


def _scalars(state: R4State) -> tuple[int, ...]:
    return tuple(state.query) + tuple(x for row in state.key for x in row) + tuple(
        x for row in state.value for x in row
    )


def default_adversarial_spaces() -> tuple[AdversarialSpace, ...]:
    return (
        AdversarialSpace("R4-ADV-ALL-ZERO", "all scalar values are zero", lambda s: all(x == 0 for x in _scalars(s))),
        AdversarialSpace("R4-ADV-ALL-NEGATIVE", "all scalar values are negative", lambda s: all(x == -1 for x in _scalars(s))),
        AdversarialSpace("R4-ADV-ALL-POSITIVE", "all scalar values are positive", lambda s: all(x == 1 for x in _scalars(s))),
        AdversarialSpace("R4-ADV-BOUNDARY", "every scalar is at a domain boundary", lambda s: all(x in (-1, 1) for x in _scalars(s))),
        AdversarialSpace("R4-ADV-ZERO-QUERY", "degenerate zero query", lambda s: all(x == 0 for x in s.query)),
        AdversarialSpace(
            "R4-ADV-SYMMETRIC-ROWS",
            "equal key rows and equal value rows",
            lambda s: s.key[0] == s.key[1] and s.value[0] == s.value[1],
        ),
        AdversarialSpace(
            "R4-ADV-MIXED-SIGN",
            "both negative and positive values occur",
            lambda s: any(x < 0 for x in _scalars(s)) and any(x > 0 for x in _scalars(s)),
        ),
    )

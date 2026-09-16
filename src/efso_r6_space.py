"""Finite R6 Transformer Block qualification space."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass

DOMAIN = (-1.0, 0.0, 1.0)
EPSILON = 1e-6


@dataclass(frozen=True)
class R6State:
    input: tuple[float, float, float, float]
    attention_update: tuple[float, float, float, float]

    def canonical(self) -> dict[str, object]:
        return {
            "input": list(self.input),
            "attention_update": list(self.attention_update),
            "epsilon": EPSILON,
        }

    def id(self) -> str:
        payload = json.dumps(
            self.canonical(), ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


class R6FiniteSpace:
    scalar_parameter_count = 8
    expected_cardinality = 3**scalar_parameter_count

    def enumerate(self) -> list[R6State]:
        states: list[R6State] = []
        for values in itertools.product(DOMAIN, repeat=self.scalar_parameter_count):
            states.append(
                R6State(
                    input=tuple(values[:4]),
                    attention_update=tuple(values[4:]),
                )
            )
        return states


def enumerate_r6_space() -> list[R6State]:
    return R6FiniteSpace().enumerate()

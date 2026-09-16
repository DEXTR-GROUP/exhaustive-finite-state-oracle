from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import product


R5_VALUES: tuple[int, ...] = (-1, 0, 1)
R5_INPUT_WIDTH = 1
R5_HIDDEN_WIDTH = 2


@dataclass(frozen=True)
class R5State:
    """Structural finite state matching the independent R5 gated-MLP witness.

    The reference uses input[1], gate_weight[2], up_weight[2], and
    down_weight[2], for seven scalar parameters in total.
    """

    input: tuple[int]
    gate_weight: tuple[int, int]
    up_weight: tuple[int, int]
    down_weight: tuple[int, int]

    def encode(self) -> bytes:
        return json.dumps(
            {
                "down_weight": self.down_weight,
                "gate_weight": self.gate_weight,
                "input": self.input,
                "up_weight": self.up_weight,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    def id(self) -> str:
        return sha256(self.encode()).hexdigest()


@dataclass(frozen=True)
class R5FiniteSpace:
    values: tuple[int, ...] = R5_VALUES
    input_width: int = R5_INPUT_WIDTH
    hidden_width: int = R5_HIDDEN_WIDTH

    @property
    def scalar_parameter_count(self) -> int:
        return self.input_width + (self.hidden_width * self.input_width) * 2 + self.hidden_width

    @property
    def expected_cardinality(self) -> int:
        return len(self.values) ** self.scalar_parameter_count

    def enumerate(self) -> tuple[R5State, ...]:
        vectors_1 = tuple(product(self.values, repeat=self.input_width))
        vectors_2 = tuple(product(self.values, repeat=self.hidden_width))
        return tuple(
            R5State(
                input=input_value,
                gate_weight=gate_weight,
                up_weight=up_weight,
                down_weight=down_weight,
            )
            for input_value in vectors_1
            for gate_weight in vectors_2
            for up_weight in vectors_2
            for down_weight in vectors_2
        )


def enumerate_r5_space() -> tuple[R5State, ...]:
    return R5FiniteSpace().enumerate()

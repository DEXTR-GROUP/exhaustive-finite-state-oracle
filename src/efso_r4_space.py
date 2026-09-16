from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import product


R4_VALUES: tuple[int, ...] = (-1, 0, 1)
R4_WIDTH = 2
R4_SEQUENCE_LENGTH = 2


@dataclass(frozen=True)
class R4State:
    """Structural finite state matching the primitive R4 Attention shape.

    The independent reference uses one query vector and two key/value rows:
    query[2], key[2][2], value[2][2].
    """

    query: tuple[int, int]
    key: tuple[tuple[int, int], tuple[int, int]]
    value: tuple[tuple[int, int], tuple[int, int]]

    def encode(self) -> bytes:
        return json.dumps(
            {"key": self.key, "query": self.query, "value": self.value},
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    def id(self) -> str:
        return sha256(self.encode()).hexdigest()


@dataclass(frozen=True)
class R4FiniteSpace:
    values: tuple[int, ...] = R4_VALUES
    width: int = R4_WIDTH
    sequence_length: int = R4_SEQUENCE_LENGTH

    @property
    def scalar_parameter_count(self) -> int:
        return self.width + (self.sequence_length * self.width) * 2

    @property
    def expected_cardinality(self) -> int:
        return len(self.values) ** self.scalar_parameter_count

    def enumerate(self) -> tuple[R4State, ...]:
        vectors = tuple(product(self.values, repeat=self.width))
        matrices = tuple(product(vectors, repeat=self.sequence_length))
        return tuple(
            R4State(query=query, key=key, value=value)
            for query in vectors
            for key in matrices
            for value in matrices
        )


def enumerate_r4_space() -> tuple[R4State, ...]:
    return R4FiniteSpace().enumerate()

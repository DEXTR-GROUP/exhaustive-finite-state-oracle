from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Callable, Iterable, Sequence, TypeVar
T = TypeVar("T")
@dataclass(frozen=True)
class ExhaustiveEvidence:
    expected_count: int
    observed_count: int
    unique_count: int
    duplicate_count: int
    missing_count: int
    deterministic_order: bool
    digest: str
    @property
    def passed(self) -> bool:
        return (self.observed_count == self.expected_count and self.unique_count == self.expected_count and self.duplicate_count == 0 and self.missing_count == 0 and self.deterministic_order)
def _ids(states: Sequence[T], identity: Callable[[T], str]) -> tuple[str, ...]:
    return tuple(identity(state) for state in states)
def _digest(ids: Sequence[str]) -> str:
    return sha256(b"".join(x.encode("ascii") + b"\n" for x in ids)).hexdigest()
def exhaustive_enumerate(states: Iterable[T], *, expected_count: int, identity: Callable[[T], str], repeat_enumerator: Callable[[], Iterable[T]] | None = None) -> tuple[tuple[T, ...], ExhaustiveEvidence]:
    materialized = tuple(states)
    ids = _ids(materialized, identity)
    unique_ids = set(ids)
    deterministic_order = False if repeat_enumerator is None else ids == _ids(tuple(repeat_enumerator()), identity)
    evidence = ExhaustiveEvidence(expected_count, len(materialized), len(unique_ids), len(ids) - len(unique_ids), max(expected_count - len(unique_ids), 0), deterministic_order, _digest(ids))
    return materialized, evidence
def verify_reproducibility(enumerate_states: Callable[[], Sequence[T]], *, identity: Callable[[T], str]) -> bool:
    first = _ids(tuple(enumerate_states()), identity)
    second = _ids(tuple(enumerate_states()), identity)
    return first == second

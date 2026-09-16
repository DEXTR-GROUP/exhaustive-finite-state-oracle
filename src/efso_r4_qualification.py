from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import product
from pathlib import Path
from typing import Sequence

@dataclass(frozen=True)
class R4State:
    q: tuple[int, ...]
    k: tuple[int, ...]
    v: tuple[int, ...]
    def encode(self) -> bytes:
        return json.dumps({"q": self.q, "k": self.k, "v": self.v}, separators=(",", ":"), sort_keys=True).encode()
    def id(self) -> str:
        return sha256(self.encode()).hexdigest()

@dataclass(frozen=True)
class R4QualificationSpace:
    values: tuple[int, ...] = (-1, 0, 1)
    width: int = 2
    @property
    def expected_cardinality(self) -> int:
        return len(self.values) ** (self.width * 3)
    def enumerate(self) -> tuple[R4State, ...]:
        vectors = tuple(product(self.values, repeat=self.width))
        return tuple(R4State(q, k, v) for q in vectors for k in vectors for v in vectors)

def structural_digest(states: Sequence[R4State]) -> str:
    h = sha256()
    for state in states:
        h.update(state.id().encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()

def load_reference_outputs(path: Path) -> dict[str, list[float]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("reference artifact must be an object mapping state_id to output")
    return payload

def compare_outputs(actual: Sequence[float], expected: Sequence[float], *, abs_tol: float = 1e-6, rel_tol: float = 1e-6) -> tuple[bool, float]:
    if len(actual) != len(expected):
        return False, float("inf")
    max_error = 0.0
    for a, e in zip(actual, expected):
        error = abs(a - e)
        max_error = max(max_error, error)
        if error > max(abs_tol, rel_tol * abs(e)):
            return False, max_error
    return True, max_error

def run_space(reference_artifact: Path) -> dict[str, object]:
    space = R4QualificationSpace()
    states = space.enumerate()
    references = load_reference_outputs(reference_artifact)
    ids = [state.id() for state in states]
    expected = space.expected_cardinality
    structural_ok = len(states) == expected and len(set(ids)) == expected and set(ids) == set(references)
    return {
        "schema_version": "EFSO-R4-1",
        "space_id": "R4-3^6",
        "expected_cardinality": expected,
        "observed_count": len(states),
        "unique_count": len(set(ids)),
        "reference_count": len(references),
        "missing_states": sorted(set(ids) - set(references)),
        "unexpected_reference_states": sorted(set(references) - set(ids)),
        "enumeration_digest": structural_digest(states),
        "comparison_policy": {"abs_tol": 1e-6, "rel_tol": 1e-6},
        "structural_pass": structural_ok,
        "numerical_cases": 0,
        "numerical_status": "INCONCLUSIVE",
        "numerical_pass": False,
        "max_error": None,
    }

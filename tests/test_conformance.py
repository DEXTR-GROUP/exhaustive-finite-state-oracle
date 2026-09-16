from dataclasses import dataclass
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_conformance import exhaustive_compare


@dataclass(frozen=True)
class State:
    value: int

    def id(self) -> str:
        return f"state-{self.value}"


def test_exhaustive_conformance_passes_exact_results():
    states = [State(i) for i in range(4)]
    report = exhaustive_compare(states, [0, 1, 4, 9], [0, 1, 4, 9])
    assert report.exhaustive
    assert report.conformant
    assert report.mismatch_count == 0
    assert report.max_abs_error == 0.0
    assert report.first_mismatch is None
    assert report.qualification == "PASS"


def test_exhaustive_conformance_accepts_fixed_tolerance():
    states = [State(0), State(1)]
    report = exhaustive_compare(states, [(1.0, 2.0), (3.0, 4.0)], [(1.0, 2.0), (3.0 + 1e-9, 4.0)], tolerance=1e-8)
    assert report.conformant
    assert report.max_abs_error == pytest.approx(1e-9)


def test_exhaustive_conformance_emits_first_counterexample():
    states = [State(i) for i in range(3)]
    report = exhaustive_compare(states, [0, 99, 2], [0, 1, 2])
    assert not report.conformant
    assert report.mismatch_count == 1
    assert report.first_mismatch is not None
    assert report.first_mismatch.index == 1
    assert report.first_mismatch.state_id == "state-1"
    assert report.first_mismatch.reason == "numeric mismatch"
    assert report.first_mismatch.max_abs_error == 98.0
    assert report.qualification == "FAIL"


def test_exhaustive_conformance_rejects_cardinality_mismatch():
    states = [State(i) for i in range(3)]
    report = exhaustive_compare(states, [0, 1], [0, 1, 2])
    assert not report.exhaustive
    assert not report.conformant
    assert report.first_mismatch is not None
    assert report.first_mismatch.reason == "cardinality mismatch"


def test_exhaustive_conformance_detects_shape_mismatch():
    states = [State(0)]
    report = exhaustive_compare(states, [[1.0, 2.0]], [[1.0]])
    assert report.mismatch_count == 1
    assert report.first_mismatch is not None
    assert report.first_mismatch.reason == "output shape mismatch"

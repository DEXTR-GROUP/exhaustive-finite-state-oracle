from dataclasses import dataclass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_invariants import InvariantSpec, check_invariants


@dataclass(frozen=True)
class State:
    value: int

    def id(self) -> str:
        return f"state-{self.value}"


def test_invariants_pass_with_independent_replay():
    states = [State(i) for i in range(4)]
    report = check_invariants(
        states,
        [InvariantSpec("nonnegative", lambda state: state.value >= 0)],
        expected_count=4,
        replay_factory=lambda: [State(i) for i in range(4)],
    )
    assert report.exhaustive
    assert report.deterministic_replay
    assert report.violation_count == 0
    assert report.conformant
    assert report.qualification == "PASS"


def test_invariants_emit_first_violation():
    states = [State(0), State(-1), State(2)]
    report = check_invariants(
        states,
        [InvariantSpec("nonnegative", lambda state: state.value >= 0)],
        expected_count=3,
        replay_factory=lambda: [State(0), State(-1), State(2)],
    )
    assert not report.conformant
    assert report.violation_count == 1
    assert report.first_violation is not None
    assert report.first_violation.index == 1
    assert report.first_violation.state_id == "state--1"
    assert report.first_violation.invariant == "nonnegative"
    assert report.qualification == "FAIL"


def test_invariants_reject_nonreproducible_replay():
    states = [State(0), State(1)]
    report = check_invariants(
        states,
        [InvariantSpec("valid", lambda state: True)],
        expected_count=2,
        replay_factory=lambda: [State(1), State(0)],
    )
    assert not report.deterministic_replay
    assert not report.conformant


def test_invariants_require_explicit_replay_for_pass():
    states = [State(0)]
    report = check_invariants(
        states,
        [InvariantSpec("valid", lambda state: True)],
        expected_count=1,
    )
    assert not report.deterministic_replay
    assert not report.conformant


def test_invariants_reject_cardinality_mismatch():
    states = [State(0), State(1)]
    report = check_invariants(
        states,
        [InvariantSpec("valid", lambda state: True)],
        expected_count=3,
        replay_factory=lambda: [State(0), State(1)],
    )
    assert not report.exhaustive
    assert not report.conformant
    assert report.qualification == "FAIL"

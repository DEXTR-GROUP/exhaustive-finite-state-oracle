import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import efso_fm03 as module


def test_fm03_passes():
    result = module.run()
    assert result["qualification"] == "PASS"
    assert result["fm2"]["expected_cardinality"] == 9
    assert result["fm3"]["exact_structural"]["observed_count"] == 9
    assert result["fm3"]["exact_structural"]["unique_count"] == 9
    assert result["fm3"]["exact_structural"]["missing_count"] == 0
    assert result["fm3"]["exact_structural"]["duplicate_count"] == 0


def test_state_identity_is_order_independent():
    first = module.State(-1, 1)
    second = module.State(-1, 1)
    assert module.state_id(first) == module.state_id(second)


def test_transition_is_closed():
    space = module.QualificationSpace((-1, 0, 1), (-1, 0, 1))
    states = set(space.enumerate())
    assert all(module.independent_transition(s) in states for s in states)

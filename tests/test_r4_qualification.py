import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import efso_r4_qualification as module


def test_r4_space_cardinality_and_uniqueness():
    space = module.R4QualificationSpace()
    states = space.enumerate()
    ids = [s.id() for s in states]
    assert len(states) == 729
    assert len(set(ids)) == 729
    assert space.expected_cardinality == 729


def test_r4_state_identity_is_deterministic():
    state = module.R4State((1, 0), (-1, 1), (0, 1))
    assert state.id() == module.R4State((1, 0), (-1, 1), (0, 1)).id()


def test_r4_structural_digest_is_reproducible():
    space = module.R4QualificationSpace()
    states = space.enumerate()
    assert module.structural_digest(states) == module.structural_digest(states)

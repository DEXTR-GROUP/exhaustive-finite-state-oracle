import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_bridge import canonical_payload, qualify_bridge, run_witness

WITNESS = Path(__file__).resolve().parents[1] / "validation" / "witnesses" / "r4_attention_batch_oracle.py"

CASES = [
    {"query": [0, 0], "key": [[0, 0], [0, 0]], "value": [[1, -1], [-1, 1]]},
    {"query": [1, 0], "key": [[1, 0], [0, 1]], "value": [[1, 2], [3, 4]]},
    {"query": [-1, 1], "key": [[1, 1], [-1, -1]], "value": [[2, -2], [-3, 3]]},
]


def test_canonical_payload_is_stable():
    assert canonical_payload(CASES) == canonical_payload(CASES)
    assert json.loads(canonical_payload(CASES)) == CASES


def test_external_witness_is_subprocess_endpoint():
    outputs, digest = run_witness(WITNESS, CASES)
    assert len(outputs) == len(CASES)
    assert digest


def test_bridge_requires_mutation_independence_for_pass():
    failed = qualify_bridge(WITNESS, CASES, mutation_independent=False)
    assert failed.qualification == "FAIL"
    passed = qualify_bridge(WITNESS, CASES, mutation_independent=True)
    assert passed.qualification == "PASS"
    assert passed.output_count == passed.case_count


def test_missing_witness_fails_closed():
    with pytest.raises((OSError, RuntimeError)):
        run_witness(Path("/nonexistent/witness.py"), CASES)

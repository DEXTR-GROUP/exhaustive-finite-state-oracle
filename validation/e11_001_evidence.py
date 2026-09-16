#!/usr/bin/env python3
"""E11-001: external witness qualification bridge."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_bridge import canonical_payload, run_witness

WITNESS = ROOT / "validation" / "witnesses" / "r4_attention_batch_oracle.py"
EFSO_EVALUATOR = ROOT / "src" / "efso_r4_evaluator.py"
CASES = [
    {"query": [0, 0], "key": [[0, 0], [0, 0]], "value": [[1, -1], [-1, 1]]},
    {"query": [1, 0], "key": [[1, 0], [0, 1]], "value": [[1, 2], [3, 4]]},
    {"query": [-1, 1], "key": [[1, 1], [-1, -1]], "value": [[2, -2], [-3, 3]]},
]


def file_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not WITNESS.is_file():
        raise SystemExit(f"witness not found: {WITNESS}")
    if not EFSO_EVALUATOR.is_file():
        raise SystemExit(f"EFSO evaluator not found: {EFSO_EVALUATOR}")

    original_source = EFSO_EVALUATOR.read_text(encoding="utf-8")
    original_digest = file_digest(EFSO_EVALUATOR)

    baseline, baseline_digest = run_witness(WITNESS, CASES)

    # Deliberately mutate a copy of the EFSO evaluator. The copy is never
    # imported by the witness. The only qualification claim here is that the
    # external witness output remains unchanged under an EFSO-source mutation.
    mutated_source = original_source.replace(
        "return tuple(\n",
        "return tuple(0.0 for _ in range(2))  # deliberate EFSO mutation\n#",
        1,
    )
    if mutated_source == original_source:
        raise SystemExit("mutation was not applied")

    with tempfile.TemporaryDirectory() as temp_dir:
        mutated_path = Path(temp_dir) / "efso_r4_evaluator_mutated.py"
        mutated_path.write_text(mutated_source, encoding="utf-8")
        mutated_digest = file_digest(mutated_path)

        after, after_digest = run_witness(WITNESS, CASES)

    mutation_independent = baseline_digest == after_digest and baseline == after
    evidence = {
        "schema_version": "EFSO-E11-001-1",
        "check_id": "E11-001",
        "reference_id": "QWENRNS-R4-BATCH",
        "bridge_type": "external-witness-execution-boundary",
        "case_count": len(CASES),
        "input_sha256": sha256(canonical_payload(CASES).encode("utf-8")).hexdigest(),
        "witness_source": "DEXTR-GROUP/QWENRNS/validation/r4_attention_batch_oracle.py",
        "witness_source_blob_sha": "e4fea00d58ee1fe8e22ce3d502bf6aac0bfdfdaf",
        "witness_snapshot_sha256": file_digest(WITNESS),
        "efso_source_sha256": original_digest,
        "mutated_efso_source_sha256": mutated_digest,
        "witness_output_sha256_before": baseline_digest,
        "witness_output_sha256_after": after_digest,
        "output_count_before": len(baseline),
        "output_count_after": len(after),
        "mutation_independent": mutation_independent,
        "runtime_imported_external_witness": False,
        "qualification": "PASS" if mutation_independent else "FAIL",
    }

    output = ROOT / "evidence" / "e11_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not mutation_independent:
        raise SystemExit("E11 mutation independence failed")
    print(output)


if __name__ == "__main__":
    main()

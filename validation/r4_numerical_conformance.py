#!/usr/bin/env python3
"""Exhaustive R4 numerical conformance against an external-origin witness.

The witness is a pinned snapshot copied from QWENRNS. It is executed only by
this validation harness and is never imported by EFSO runtime code.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_r4_evaluator import evaluate
from efso_r4_space import enumerate_r4_space

EXPECTED_COUNT = 59049
TOLERANCE = 1e-12
LOCAL_WITNESS = ROOT / "validation" / "witnesses" / "r4_attention_batch_oracle.py"


def as_payload(state) -> dict[str, object]:
    return {
        "query": list(state.query),
        "key": [list(row) for row in state.key],
        "value": [list(row) for row in state.value],
    }


def resolve_witness() -> Path:
    witness_root = os.environ.get("QWENRNS_ROOT")
    if witness_root:
        candidate = Path(witness_root) / "validation" / "r4_attention_batch_oracle.py"
        if candidate.is_file():
            return candidate
        raise SystemExit(f"external oracle not found: {candidate}")
    if LOCAL_WITNESS.is_file():
        return LOCAL_WITNESS
    raise SystemExit(f"external-origin witness not found: {LOCAL_WITNESS}")


def main() -> None:
    oracle = resolve_witness()

    states = enumerate_r4_space()
    if len(states) != EXPECTED_COUNT:
        raise SystemExit(f"unexpected EFSO cardinality: {len(states)}")

    payload = json.dumps([as_payload(state) for state in states], separators=(",", ":"))
    completed = subprocess.run(
        [sys.executable, str(oracle)],
        input=payload,
        capture_output=True,
        text=True,
        check=True,
    )
    reference = json.loads(completed.stdout)
    if len(reference) != EXPECTED_COUNT:
        raise SystemExit(f"unexpected external cardinality: {len(reference)}")

    max_abs_error = 0.0
    mismatch_count = 0
    first_mismatch = None

    for index, (state, expected) in enumerate(zip(states, reference)):
        actual = evaluate(state)
        if len(expected) != 2:
            mismatch_count += 1
            if first_mismatch is None:
                first_mismatch = {"index": index, "reason": "wrong output width"}
            continue
        errors = [abs(actual[dimension] - float(expected[dimension])) for dimension in range(2)]
        local_max = max(errors)
        max_abs_error = max(max_abs_error, local_max)
        if any(not math.isclose(actual[dimension], float(expected[dimension]), rel_tol=TOLERANCE, abs_tol=TOLERANCE) for dimension in range(2)):
            mismatch_count += 1
            if first_mismatch is None:
                first_mismatch = {
                    "index": index,
                    "state_id": state.id(),
                    "actual": list(actual),
                    "expected": expected,
                    "errors": errors,
                }

    state_digest = sha256(
        b"".join(state.id().encode("ascii") + b"\n" for state in states)
    ).hexdigest()

    evidence = {
        "schema_version": "EFSO-R4-NUMERICAL-1",
        "check_id": "R4-NUM-001",
        "reference_id": "QWENRNS-R4-BATCH",
        "finite_space": "E4/R4-DOMAIN-3^10",
        "expected_count": EXPECTED_COUNT,
        "external_count": len(reference),
        "tolerance": TOLERANCE,
        "max_abs_error": max_abs_error,
        "mismatch_count": mismatch_count,
        "first_mismatch": first_mismatch,
        "state_digest": state_digest,
        "qualification": "PASS" if mismatch_count == 0 else "FAIL",
        "external_oracle_path": str(oracle),
        "witness_mode": "external-origin-pinned-snapshot" if oracle == LOCAL_WITNESS else "external-repository",
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }

    output = ROOT / "evidence" / "r4_numerical_conformance.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if mismatch_count:
        raise SystemExit(f"R4 numerical conformance failed: {mismatch_count} mismatches")
    print(output)


if __name__ == "__main__":
    main()

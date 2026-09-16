#!/usr/bin/env python3
"""Exhaustive R6 numerical conformance against a pinned external-origin witness."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from hashlib import sha1, sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_r6_evaluator import evaluate
from efso_r6_space import EPSILON, enumerate_r6_space

EXPECTED_COUNT = 6561
TOLERANCE = 1e-12
WITNESS = ROOT / "validation" / "witnesses" / "r6_transformer_batch_oracle.py"
SOURCE_REPOSITORY = "DEXTR-GROUP/QWENRNS"
SOURCE_PATH = "validation/r6_transformer_batch_oracle.py"
SOURCE_COMMIT = "a40bdbfd999535f2bb9c57da6f2a2e861e49c12c"
SOURCE_BLOB_SHA = "dcea89f0c6246d1f466a91f696c3091d8e9c8948"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def as_payload(state) -> dict[str, object]:
    return {
        "input": list(state.input),
        "attention_update": list(state.attention_update),
        "epsilon": EPSILON,
    }


def main() -> None:
    if not WITNESS.is_file():
        raise SystemExit(f"pinned witness not found: {WITNESS}")
    observed_blob_sha = git_blob_sha(WITNESS)
    if observed_blob_sha != SOURCE_BLOB_SHA:
        raise SystemExit(
            f"witness provenance mismatch: expected source blob {SOURCE_BLOB_SHA}, observed {observed_blob_sha}"
        )

    states = enumerate_r6_space()
    if len(states) != EXPECTED_COUNT:
        raise SystemExit(f"unexpected EFSO cardinality: {len(states)}")

    payload = json.dumps([as_payload(state) for state in states], separators=(",", ":"))
    completed = subprocess.run(
        [sys.executable, str(WITNESS)],
        input=payload,
        capture_output=True,
        text=True,
        check=True,
    )
    if completed.stderr:
        raise SystemExit("external witness wrote to stderr")
    reference = json.loads(completed.stdout)
    if len(reference) != EXPECTED_COUNT:
        raise SystemExit(f"unexpected external cardinality: {len(reference)}")

    max_abs_error = 0.0
    mismatch_count = 0
    first_mismatch = None

    for index, (state, expected) in enumerate(zip(states, reference)):
        actual = evaluate(state)
        if len(expected) != 4:
            mismatch_count += 1
            if first_mismatch is None:
                first_mismatch = {"index": index, "reason": "wrong output width"}
            continue
        errors = [abs(actual[i] - float(expected[i])) for i in range(4)]
        error = max(errors)
        max_abs_error = max(max_abs_error, error)
        if any(not math.isclose(actual[i], float(expected[i]), rel_tol=TOLERANCE, abs_tol=TOLERANCE) for i in range(4)):
            mismatch_count += 1
            if first_mismatch is None:
                first_mismatch = {
                    "index": index,
                    "state_id": state.id(),
                    "actual": list(actual),
                    "expected": expected,
                    "max_error": error,
                }

    state_digest = sha256(b"".join(state.id().encode("ascii") + b"\n" for state in states)).hexdigest()
    output_digest = sha256(completed.stdout.encode("utf-8")).hexdigest()

    evidence = {
        "schema_version": "EFSO-R6-NUMERICAL-1",
        "check_id": "R6-NUM-001",
        "reference_id": "QWENRNS-R6-BATCH",
        "finite_space": "R6-DOMAIN-3^8",
        "expected_count": EXPECTED_COUNT,
        "external_count": len(reference),
        "tolerance": TOLERANCE,
        "max_abs_error": max_abs_error,
        "mismatch_count": mismatch_count,
        "first_mismatch": first_mismatch,
        "state_digest": state_digest,
        "external_output_sha256": output_digest,
        "witness_source_repository": SOURCE_REPOSITORY,
        "witness_source_path": SOURCE_PATH,
        "witness_source_commit": SOURCE_COMMIT,
        "witness_source_blob_sha": SOURCE_BLOB_SHA,
        "witness_snapshot_sha256": sha256(WITNESS.read_bytes()).hexdigest(),
        "witness_mode": "external-origin-pinned-snapshot",
        "runtime_external_repository_access": False,
        "qualification": "PASS" if mismatch_count == 0 else "FAIL",
        "source_commit": "GITHUB_SHA_UNKNOWN_AT_LOCAL_RUN",
    }
    output = ROOT / "evidence" / "r6_numerical_conformance.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if mismatch_count:
        raise SystemExit(f"R6 numerical conformance failed: {mismatch_count} mismatches")
    print(output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E6-001: qualification of the generic exhaustive conformance contour.

The case uses the already pinned external-origin R4 witness as the second
computational path. This validates E6 machinery itself; it is not an IUT
qualification claim.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_conformance import exhaustive_compare
from efso_r4_evaluator import evaluate
from efso_r4_space import enumerate_r4_space

EXPECTED_COUNT = 59049
TOLERANCE = 1e-12
WITNESS = ROOT / "validation" / "witnesses" / "r4_attention_batch_oracle.py"


def as_payload(state) -> dict[str, object]:
    return {
        "query": list(state.query),
        "key": [list(row) for row in state.key],
        "value": [list(row) for row in state.value],
    }


def main() -> None:
    if not WITNESS.is_file():
        raise SystemExit(f"pinned external-origin witness not found: {WITNESS}")

    states = enumerate_r4_space()
    if len(states) != EXPECTED_COUNT:
        raise SystemExit(f"unexpected state count: {len(states)}")

    payload = json.dumps([as_payload(state) for state in states], separators=(",", ":"))
    completed = subprocess.run(
        [sys.executable, str(WITNESS)],
        input=payload,
        capture_output=True,
        text=True,
        check=True,
    )
    expected = json.loads(completed.stdout)
    actual = tuple(evaluate(state) for state in states)
    report = exhaustive_compare(states, actual, expected, tolerance=TOLERANCE)

    state_digest = sha256(
        b"".join(state.id().encode("ascii") + b"\n" for state in states)
    ).hexdigest()

    evidence = {
        "schema_version": "EFSO-E6-001-1",
        "check_id": "E6-001",
        "scope": "generic exhaustive conformance contour qualification",
        "qualification_target": "EFSO R4 evaluator versus pinned external-origin witness",
        "iut_claim": False,
        "finite_space": "E4/R4-DOMAIN-3^10",
        "expected_count": EXPECTED_COUNT,
        "actual_count": report.actual_count,
        "exhaustive": report.exhaustive,
        "tolerance": TOLERANCE,
        "max_abs_error": report.max_abs_error,
        "mismatch_count": report.mismatch_count,
        "first_mismatch": None if report.first_mismatch is None else {
            "index": report.first_mismatch.index,
            "state_id": report.first_mismatch.state_id,
            "actual": report.first_mismatch.actual,
            "expected": report.first_mismatch.expected,
            "reason": report.first_mismatch.reason,
            "max_abs_error": report.first_mismatch.max_abs_error,
        },
        "state_digest": state_digest,
        "qualification": report.qualification,
        "witness_mode": "external-origin-pinned-snapshot",
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }

    output = ROOT / "evidence" / "e6_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not report.conformant:
        raise SystemExit(f"E6-001 failed: {report.mismatch_count} mismatches")
    print(output)


if __name__ == "__main__":
    main()

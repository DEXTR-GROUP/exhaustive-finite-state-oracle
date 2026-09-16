#!/usr/bin/env python3
"""Generate structural evidence for FM2-R4-002.

This check validates only finite-state shape alignment. It does not execute
or import the external numerical reference.
"""

from __future__ import annotations

import json
import os
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_r4_space import R4FiniteSpace


CONTRACT_PATH = ROOT / "validation" / "r4_reference_contract.json"


def main() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    space = R4FiniteSpace()

    shape_ok = (
        contract["query_shape"] == [space.width]
        and contract["key_shape"] == [space.sequence_length, space.width]
        and contract["value_shape"] == [space.sequence_length, space.width]
        and contract["scalar_parameter_count"] == space.scalar_parameter_count
        and contract["finite_domain"] == list(space.values)
    )
    states = space.enumerate()
    ids = [state.id() for state in states]
    enumeration_digest = sha256(
        b"".join(state_id.encode("ascii") + b"\n" for state_id in ids)
    ).hexdigest()

    evidence = {
        "schema_version": "EFSO-FM2-R4-002-1",
        "check_id": "FM2-R4-002",
        "reference_id": contract["reference_id"],
        "reference_contract": str(CONTRACT_PATH.relative_to(ROOT)),
        "shape_alignment": shape_ok,
        "scalar_parameter_count": space.scalar_parameter_count,
        "expected_cardinality": space.expected_cardinality,
        "observed_count": len(states),
        "unique_count": len(set(ids)),
        "missing_count": max(space.expected_cardinality - len(set(ids)), 0),
        "duplicate_count": len(ids) - len(set(ids)),
        "enumeration_digest": enumeration_digest,
        "numerical_conformance": "NOT_EXECUTED",
        "qualification": "PASS" if shape_ok and len(states) == space.expected_cardinality and len(set(ids)) == space.expected_cardinality else "FAIL",
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }

    if evidence["qualification"] != "PASS":
        raise SystemExit("FM2-R4-002 structural evidence failed")

    output = ROOT / "evidence" / "fm2_r4_002.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

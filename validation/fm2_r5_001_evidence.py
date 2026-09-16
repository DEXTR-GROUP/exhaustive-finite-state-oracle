#!/usr/bin/env python3
"""FM2-R5-001 structural finite-space evidence."""

from __future__ import annotations

import json
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_r5_space import enumerate_r5_space, R5FiniteSpace

EXPECTED_COUNT = 2187


def main() -> None:
    space = R5FiniteSpace()
    states = enumerate_r5_space()
    ids = [state.id() for state in states]
    evidence = {
        "schema_version": "EFSO-FM2-R5-001-1",
        "check_id": "FM2-R5-001",
        "reference_id": "QWENRNS-R5-BATCH",
        "finite_domain": list(space.values),
        "scalar_parameter_count": space.scalar_parameter_count,
        "expected_cardinality": EXPECTED_COUNT,
        "observed_cardinality": len(states),
        "unique_id_count": len(set(ids)),
        "state_digest": sha256("\n".join(ids).encode("ascii")).hexdigest(),
        "enumeration_deterministic": ids == [state.id() for state in enumerate_r5_space()],
        "qualification": "PASS"
        if len(states) == EXPECTED_COUNT and len(set(ids)) == EXPECTED_COUNT
        else "FAIL",
    }
    output = ROOT / "evidence" / "fm2_r5_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if evidence["qualification"] != "PASS":
        raise SystemExit("FM2-R5-001 failed")
    print(output)


if __name__ == "__main__":
    main()

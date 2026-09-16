#!/usr/bin/env python3
"""Generate structural evidence for FM2-R6-001."""

from __future__ import annotations

import json
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_r6_space import R6FiniteSpace, enumerate_r6_space


def main() -> None:
    space = R6FiniteSpace()
    states = enumerate_r6_space()
    ids = [state.id() for state in states]
    evidence = {
        "schema_version": "EFSO-FM2-R6-001-1",
        "check_id": "FM2-R6-001",
        "scope": "finite-state model for minimal R6 Transformer Block qualification",
        "scalar_parameter_count": space.scalar_parameter_count,
        "domain": [-1.0, 0.0, 1.0],
        "expected_count": space.expected_cardinality,
        "observed_count": len(states),
        "unique_state_ids": len(set(ids)),
        "deterministic_enumeration": ids == [state.id() for state in enumerate_r6_space()],
        "state_digest": sha256(b"".join(value.encode("ascii") + b"\n" for value in ids)).hexdigest(),
        "qualification": "PASS" if len(states) == space.expected_cardinality and len(set(ids)) == len(states) else "FAIL",
    }
    output = ROOT / "evidence" / "fm2_r6_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if evidence["qualification"] != "PASS":
        raise SystemExit("FM2-R6-001 failed")
    print(output)


if __name__ == "__main__":
    main()

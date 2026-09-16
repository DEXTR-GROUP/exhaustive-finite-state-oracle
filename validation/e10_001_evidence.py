#!/usr/bin/env python3
"""E10-001: exhaustive qualification of adversarial R4 subspaces."""

from __future__ import annotations

import json
import os
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_adversarial import default_adversarial_spaces
from efso_r4_space import enumerate_r4_space

EXPECTED = {
    "R4-ADV-ALL-ZERO": 1,
    "R4-ADV-ALL-NEGATIVE": 1,
    "R4-ADV-ALL-POSITIVE": 1,
    "R4-ADV-BOUNDARY": 1024,
    "R4-ADV-ZERO-QUERY": 6561,
    "R4-ADV-SYMMETRIC-ROWS": 729,
    "R4-ADV-MIXED-SIGN": 57002,
}


def main() -> None:
    states = enumerate_r4_space()
    rows = []
    for space in default_adversarial_spaces():
        selected = space.enumerate(states)
        ids = tuple(state.id() for state in selected)
        rows.append(
            {
                "space_id": space.space_id,
                "purpose": space.purpose,
                "expected_count": EXPECTED[space.space_id],
                "observed_count": len(selected),
                "unique_count": len(set(ids)),
                "deterministic_replay": ids == tuple(state.id() for state in space.enumerate(states)),
                "state_digest": sha256(b"".join(x.encode("ascii") + b"\n" for x in ids)).hexdigest(),
            }
        )

    qualified = all(
        row["observed_count"] == row["expected_count"]
        and row["unique_count"] == row["expected_count"]
        and row["deterministic_replay"]
        for row in rows
    )

    evidence = {
        "schema_version": "EFSO-E10-001-1",
        "check_id": "E10-001",
        "scope": "adversarial exhaustive finite-space qualification",
        "base_space": "R4-DOMAIN-3^10",
        "base_cardinality": 59049,
        "spaces": rows,
        "space_count": len(rows),
        "qualification": "PASS" if qualified else "FAIL",
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }

    output = ROOT / "evidence" / "e10_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not qualified:
        raise SystemExit("E10-001 failed: adversarial finite-space qualification did not close")
    print(output)


if __name__ == "__main__":
    main()

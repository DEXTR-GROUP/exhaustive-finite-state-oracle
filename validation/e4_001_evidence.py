#!/usr/bin/env python3
"""Generate machine-readable evidence for EFSO E4-001.

The evidence is produced only from the independent EFSO exhaustive
enumerator and the explicitly defined 3x3 finite qualification space.
No IUT or external numerical oracle is imported or called.
"""

from __future__ import annotations

import json
import os
from itertools import product
from pathlib import Path

from src.efso_exhaustive import exhaustive_enumerate, verify_reproducibility
from src.efso_fm03 import State, state_id


SPACE_ID = "E4-BASE-3x3"
EXPECTED_COUNT = 9


def enumerate_space() -> tuple[State, ...]:
    return tuple(State(a, b) for a, b in product((-1, 0, 1), repeat=2))


def build_evidence() -> dict[str, object]:
    states, evidence = exhaustive_enumerate(
        enumerate_space(),
        expected_count=EXPECTED_COUNT,
        identity=state_id,
        repeat_enumerator=enumerate_space,
    )
    reproducible = verify_reproducibility(enumerate_space, identity=state_id)

    if not evidence.passed or not reproducible:
        raise SystemExit("E4-001 evidence generation failed")

    return {
        "schema_version": "EFSO-E4-001-1",
        "check_id": "E4-001",
        "space_id": SPACE_ID,
        "space_definition": {
            "domain_a": [-1, 0, 1],
            "domain_b": [-1, 0, 1],
            "cardinality_formula": "3 * 3",
        },
        "expected_count": evidence.expected_count,
        "observed_count": evidence.observed_count,
        "unique_count": evidence.unique_count,
        "duplicate_count": evidence.duplicate_count,
        "missing_count": evidence.missing_count,
        "deterministic_order": evidence.deterministic_order,
        "reproducible_replay": reproducible,
        "enumeration_digest": evidence.digest,
        "qualification": "PASS",
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }


def main() -> None:
    output = Path(os.environ.get("EFSO_E4_EVIDENCE", "evidence/e4_001.json"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_evidence(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()

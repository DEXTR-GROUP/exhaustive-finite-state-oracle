#!/usr/bin/env python3
"""E12-001 reproducible verification harness.

Runs the complete currently qualified evidence suite twice in isolated
subprocesses and requires identical return codes, stdout/stderr digests, and
machine-readable evidence digests. The harness does not import any IUT or
external numerical oracle as a runtime dependency.
"""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_reproducibility import canonical_json, digest_tree, run_command, reproducible

COMMANDS = [
    (sys.executable, "validation/e4_001_evidence.py"),
    (sys.executable, "validation/fm2_r4_002_evidence.py"),
    (sys.executable, "validation/r4_numerical_conformance.py"),
    (sys.executable, "validation/e5_001_evidence.py"),
    (sys.executable, "validation/e6_001_evidence.py"),
    (sys.executable, "validation/e7_001_evidence.py"),
    (sys.executable, "validation/e8_001_evidence.py"),
    (sys.executable, "validation/e9_001_evidence.py"),
    (sys.executable, "validation/e10_001_evidence.py"),
    (sys.executable, "validation/e11_001_evidence.py"),
]
EVIDENCE_NAMES = (
    "e4_001.json",
    "fm2_r4_002.json",
    "r4_numerical_conformance.json",
    "e5_001.json",
    "e6_001.json",
    "e7_001.json",
    "e8_001.json",
    "e9_001.json",
    "e10_001.json",
    "e11_001.json",
)


def evidence_digest() -> str:
    entries: list[tuple[str, str]] = []
    for name in EVIDENCE_NAMES:
        path = ROOT / "evidence" / name
        if not path.is_file():
            raise SystemExit(f"missing evidence: {path}")
        entries.append((name, sha256(path.read_bytes()).hexdigest()))
    return sha256(canonical_json(entries).encode("utf-8")).hexdigest()


def main() -> None:
    source_digest = digest_tree(ROOT)
    first_results = []
    for command in COMMANDS:
        result = run_command(command, ROOT)
        first_results.append(result)
        if result.return_code != 0:
            raise SystemExit(f"E12 first run failed: {' '.join(command)}")
    first_evidence_digest = evidence_digest()

    second_results = []
    for command in COMMANDS:
        result = run_command(command, ROOT)
        second_results.append(result)
        if result.return_code != 0:
            raise SystemExit(f"E12 second run failed: {' '.join(command)}")
    second_evidence_digest = evidence_digest()

    command_results = []
    all_reproducible = True
    for first, second in zip(first_results, second_results):
        same = reproducible(first, second)
        all_reproducible = all_reproducible and same
        command_results.append(
            {
                "command": list(first.command),
                "return_code_first": first.return_code,
                "return_code_second": second.return_code,
                "stdout_sha256_first": first.stdout_sha256,
                "stdout_sha256_second": second.stdout_sha256,
                "stderr_sha256_first": first.stderr_sha256,
                "stderr_sha256_second": second.stderr_sha256,
                "reproducible": same,
            }
        )

    evidence_reproducible = first_evidence_digest == second_evidence_digest
    qualification = all_reproducible and evidence_reproducible
    evidence = {
        "schema_version": "EFSO-E12-001-1",
        "check_id": "E12-001",
        "scope": "reproducible verification harness",
        "command_count": len(COMMANDS),
        "run_count": 2,
        "source_tree_sha256": source_digest,
        "first_evidence_sha256": first_evidence_digest,
        "second_evidence_sha256": second_evidence_digest,
        "evidence_reproducible": evidence_reproducible,
        "command_results": command_results,
        "qualification": "PASS" if qualification else "FAIL",
    }

    output = ROOT / "evidence" / "e12_001.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not qualification:
        raise SystemExit("E12 reproducibility qualification failed")
    print(output)


if __name__ == "__main__":
    main()

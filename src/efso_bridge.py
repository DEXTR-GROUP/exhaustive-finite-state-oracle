"""E11 external qualification bridge.

The bridge treats an external numerical witness as an execution endpoint,
not as an EFSO runtime dependency. It records provenance, canonical input
encoding, output digest, and mutation-independence observations.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from typing import Sequence


@dataclass(frozen=True)
class WitnessManifest:
    reference_id: str
    source_repository: str
    source_path: str
    source_commit_or_blob: str
    witness_path: str
    input_schema: str
    output_schema: str


@dataclass(frozen=True)
class BridgeResult:
    case_count: int
    output_count: int
    output_digest: str
    return_code: int
    stderr_empty: bool
    mutation_independent: bool
    qualification: str


def canonical_payload(cases: Sequence[dict[str, object]]) -> str:
    return json.dumps(list(cases), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"


def run_witness(witness: Path, cases: Sequence[dict[str, object]]) -> tuple[list[object], str]:
    payload = canonical_payload(cases)
    completed = subprocess.run(
        [sys.executable, str(witness)],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"external witness failed with code {completed.returncode}: {completed.stderr}")
    if completed.stderr:
        raise RuntimeError("external witness wrote to stderr")
    decoded = json.loads(completed.stdout)
    if not isinstance(decoded, list):
        raise RuntimeError("external witness output must be a JSON array")
    return decoded, sha256(completed.stdout.encode("utf-8")).hexdigest()


def qualify_bridge(
    witness: Path,
    cases: Sequence[dict[str, object]],
    expected_output_digest: str | None = None,
    mutation_independent: bool = False,
) -> BridgeResult:
    outputs, digest = run_witness(witness, cases)
    digest_ok = expected_output_digest is None or digest == expected_output_digest
    qualified = (
        len(outputs) == len(cases)
        and digest_ok
        and mutation_independent
    )
    return BridgeResult(
        case_count=len(cases),
        output_count=len(outputs),
        output_digest=digest,
        return_code=0,
        stderr_empty=True,
        mutation_independent=mutation_independent,
        qualification="PASS" if qualified else "FAIL",
    )

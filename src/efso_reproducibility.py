"""E12 reproducibility primitives.

Provides deterministic command execution and canonical hashing for verification
runs. No project-specific IUT or external numerical oracle is imported.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Sequence


@dataclass(frozen=True)
class RunResult:
    command: tuple[str, ...]
    return_code: int
    stdout_sha256: str
    stderr_sha256: str
    stdout: str
    stderr: str


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"


def digest_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def digest_tree(root: Path, *, include_prefixes: Sequence[str] = ("src", "tests", "validation")) -> str:
    entries: list[tuple[str, str]] = []
    for prefix in include_prefixes:
        base = root / prefix
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                entries.append((relative, sha256(path.read_bytes()).hexdigest()))
    return digest_text(canonical_json(entries))


def run_command(command: Sequence[str], cwd: Path) -> RunResult:
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    return RunResult(
        command=tuple(command),
        return_code=completed.returncode,
        stdout_sha256=digest_text(completed.stdout),
        stderr_sha256=digest_text(completed.stderr),
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def reproducible(first: RunResult, second: RunResult) -> bool:
    return (
        first.command == second.command
        and first.return_code == second.return_code
        and first.stdout_sha256 == second.stdout_sha256
        and first.stderr_sha256 == second.stderr_sha256
    )

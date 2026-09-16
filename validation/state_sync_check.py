#!/usr/bin/env python3
"""Validate the current operational-state synchronization contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "Journal/EXPERIMENTS/EXPERIMENTS.md": [
        "FM2-R6-001 |",
        "R6-NUM-001 |",
        "| PASS |",
    ],
    "Journal/МАЯК.md": [
        "Идентификатор: R7-NUM-001",
        "FM2-R6-001   = PASS",
        "R6-NUM-001   = PASS",
        "R7-NUM-001 = NEXT",
    ],
    "Journal/CURRENT_STATE.md": [
        "FM2-R6-001 = PASS",
        "R6-NUM-001 = PASS",
        "R7-NUM-001",
    ],
    "QUALIFICATION_NEXT.md": [
        "R7-NUM-001",
        "R6 qualification contours закрыты",
        "только после фактического CI PASS",
    ],
}

FORBIDDEN = {
    "Journal/МАЯК.md": [
        "FM2-R5-001 = RUNNING",
        "R5-NUM-001 = RUNNING",
        "FM2-R6-001 = RUNNING",
        "R6-NUM-001 = RUNNING",
    ],
}


def main() -> None:
    failures: list[str] = []

    for relative_path, required_markers in REQUIRED.items():
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"missing operational document: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in required_markers:
            if marker not in text:
                failures.append(f"missing marker in {relative_path}: {marker}")

    for relative_path, forbidden_markers in FORBIDDEN.items():
        path = ROOT / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in forbidden_markers:
            if marker in text:
                failures.append(f"stale status in {relative_path}: {marker}")

    if failures:
        print("STATE SYNCHRONIZATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("STATE SYNCHRONIZATION: PASS")
    print("confirmed frontier: R6 PASS -> R7-NUM-001 NEXT")


if __name__ == "__main__":
    main()

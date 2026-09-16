#!/usr/bin/env python3
"""Генератор machine-readable evidence для E5."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from efso_transition import IndependentTransitionEngine, Operation, SUPPORTED_OPERATORS  # noqa: E402


def imported_modules(source: str) -> set[str]:
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def main() -> None:
    source = (ROOT / "src" / "efso_transition.py").read_text(encoding="utf-8")
    modules = imported_modules(source)
    forbidden_modules = {"qwenrns", "numpy", "torch"}
    independence = {
        "forbidden_external_modules_absent": not (modules & forbidden_modules),
        "external_runtime_imports": sorted(modules & forbidden_modules),
        "efso_module_imports_only": "efso_transition" not in modules,
    }

    scalar = IndependentTransitionEngine.apply(Operation("ADD", (2, 3))).value
    product = IndependentTransitionEngine.apply(Operation("MUL", (4, 5))).value
    reduced = IndependentTransitionEngine.apply(Operation("REDUCE", ((1, 2, 3, 4),))).value
    matrix = IndependentTransitionEngine.apply(
        Operation("MatMul", (((1, 2), (3, 4)), ((5, 6), (7, 8))))
    ).value
    normalized = IndependentTransitionEngine.apply(Operation("Softmax", ((-1.0, 0.0, 1.0),))).value
    composed = IndependentTransitionEngine.compose(
        (
            Operation("ADD", (2, 3)),
            Operation("MUL", (2, 3)),
            Operation("REDUCE", ((1, 2, 3),)),
        )
    )

    checks = {
        "supported_operator_count": len(SUPPORTED_OPERATORS) == 11,
        "supported_operators": list(SUPPORTED_OPERATORS),
        "add": scalar == 5,
        "mul": product == 20,
        "reduce": reduced == 10,
        "matmul": matrix == ((19, 22), (43, 50)),
        "softmax_normalized": abs(sum(normalized) - 1.0) <= 1e-15,
        "composition_order": [r.value for r in composed] == [5, 6, 6],
        "deterministic_replay": IndependentTransitionEngine.compose(
            (Operation("ADD", (2, 3)), Operation("MUL", (2, 3)))
        ) == IndependentTransitionEngine.compose(
            (Operation("ADD", (2, 3)), Operation("MUL", (2, 3)))
        ),
        "no_external_runtime_dependency": all(independence.values()),
    }

    qualification = all(
        value for key, value in checks.items()
        if key not in {"supported_operators"}
    )

    evidence = {
        "schema_version": "EFSO-E5-001-2",
        "check_id": "E5-001",
        "scope": "independent deterministic transition engine",
        "operators": list(SUPPORTED_OPERATORS),
        "independence_audit": independence,
        "checks": checks,
        "qualification": "PASS" if qualification else "FAIL",
        "runtime_dependencies": [],
    }

    out = ROOT / "evidence" / "e5_001.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True))

    if not qualification:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

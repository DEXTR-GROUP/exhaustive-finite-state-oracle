#!/usr/bin/env python3
"""E9: machine-readable conformance and qualification coverage matrix."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable


@dataclass(frozen=True)
class CoverageRow:
    space_id: str
    operator: str
    reference_id: str
    qualification_type: str
    cardinality: int
    expected_count: int
    enumerated: bool
    unique: bool
    missing: int
    duplicates: int
    passed: int
    failed: int
    witness: str | None = None

    @property
    def qualified(self) -> bool:
        return (
            self.qualification_type in {"structural", "numerical"}
            and self.enumerated
            and self.unique
            and self.missing == 0
            and self.duplicates == 0
            and self.passed + self.failed == self.expected_count
            and self.passed == self.expected_count
            and self.failed == 0
            and self.expected_count == self.cardinality
        )


@dataclass(frozen=True)
class MatrixReport:
    row_count: int
    structural_rows: int
    numerical_rows: int
    qualified_rows: int
    failed_rows: int
    duplicate_space_rows: int
    deterministic: bool
    qualification: str

    @property
    def conformant(self) -> bool:
        return self.qualification == "PASS"


def validate_matrix(rows: Iterable[CoverageRow]) -> MatrixReport:
    """Validate coverage completeness without interpreting primary evidence."""
    materialized = tuple(rows)
    space_keys = tuple((row.space_id, row.operator, row.reference_id) for row in materialized)
    duplicate_count = len(space_keys) - len(set(space_keys))
    ordered_keys = tuple(sorted(space_keys))

    structural_rows = sum(row.qualification_type == "structural" for row in materialized)
    numerical_rows = sum(row.qualification_type == "numerical" for row in materialized)
    qualified_rows = sum(row.qualified for row in materialized)
    failed_rows = len(materialized) - qualified_rows
    deterministic = space_keys == ordered_keys

    qualification = (
        "PASS"
        if materialized
        and duplicate_count == 0
        and failed_rows == 0
        and structural_rows + numerical_rows == len(materialized)
        and deterministic
        else "FAIL"
    )
    return MatrixReport(
        row_count=len(materialized),
        structural_rows=structural_rows,
        numerical_rows=numerical_rows,
        qualified_rows=qualified_rows,
        failed_rows=failed_rows,
        duplicate_space_rows=duplicate_count,
        deterministic=deterministic,
        qualification=qualification,
    )


def serialize_matrix(rows: Iterable[CoverageRow]) -> str:
    """Serialize rows canonically for reproducible machine-readable evidence."""
    payload = [asdict(row) for row in rows]
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

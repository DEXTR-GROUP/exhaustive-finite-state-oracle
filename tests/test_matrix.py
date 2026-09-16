from __future__ import annotations

import sys

sys.path.insert(0, "src")

from efso_matrix import CoverageRow, serialize_matrix, validate_matrix


def row(space: str, operator: str, reference: str, kind: str = "numerical") -> CoverageRow:
    return CoverageRow(
        space_id=space,
        operator=operator,
        reference_id=reference,
        qualification_type=kind,
        cardinality=59049,
        expected_count=59049,
        enumerated=True,
        unique=True,
        missing=0,
        duplicates=0,
        passed=59049,
        failed=0,
    )


def test_matrix_accepts_complete_sorted_coverage() -> None:
    rows = (
        row("R4", "Attention", "QWENRNS-R4-BATCH", "numerical"),
        row("R4", "State", "EFSO-STRUCTURAL", "structural"),
    )
    report = validate_matrix(rows)
    assert report.conformant
    assert report.row_count == 2
    assert report.structural_rows == 1
    assert report.numerical_rows == 1


def test_matrix_rejects_duplicate_rows() -> None:
    duplicate = row("R4", "Attention", "QWENRNS-R4-BATCH")
    report = validate_matrix((duplicate, duplicate))
    assert not report.conformant
    assert report.duplicate_space_rows == 1


def test_matrix_rejects_unsorted_rows() -> None:
    rows = (
        row("R5", "MLP", "QWENRNS-R5"),
        row("R4", "Attention", "QWENRNS-R4-BATCH"),
    )
    report = validate_matrix(rows)
    assert not report.conformant
    assert not report.deterministic


def test_matrix_rejects_partial_coverage() -> None:
    partial = CoverageRow(
        space_id="R4",
        operator="Attention",
        reference_id="QWENRNS-R4-BATCH",
        qualification_type="numerical",
        cardinality=59049,
        expected_count=59049,
        enumerated=True,
        unique=True,
        missing=1,
        duplicates=0,
        passed=59048,
        failed=1,
    )
    assert not validate_matrix((partial,)).conformant


def test_serialization_is_stable() -> None:
    rows = (row("R4", "Attention", "QWENRNS-R4-BATCH"),)
    assert serialize_matrix(rows) == serialize_matrix(rows)

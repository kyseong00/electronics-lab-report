#!/usr/bin/env python3
"""Inspect DOCX table-cell content and enforce user/course-specific expectations.

This utility does NOT perform visual page inspection. It lists candidate empty
cells but doesn't flag all empty cells as errors because blanks can be valid.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def normalize(text: str) -> str:
    return " ".join(text.split())


def inspect(path: Path, expected_path: Path | None = None) -> dict:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("Missing dependency: pip install python-docx") from exc

    doc = Document(str(path))
    tables = []
    blank_cells = []
    text_parts = [p.text for p in doc.paragraphs]
    for ti, table in enumerate(doc.tables):
        row_lengths = [len(row.cells) for row in table.rows]
        tables.append({"table": ti, "rows": len(table.rows), "row_cell_counts": row_lengths})
        for ri, row in enumerate(table.rows):
            for ci, cell in enumerate(row.cells):
                value = normalize(cell.text)
                text_parts.append(value)
                if not value and not cell._tc.xpath(".//w:drawing | .//w:pict"):
                    blank_cells.append({"table": ti, "row": ri, "column": ci})

    full_text = normalize("\n".join(text_parts))
    failures = []
    if expected_path:
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        for idx, spec in enumerate(expected.get("required_table_cells", [])):
            ti, ri, ci = (spec[k] for k in ("table", "row", "column"))
            try:
                actual = normalize(doc.tables[ti].rows[ri].cells[ci].text)
            except (IndexError, TypeError) as exc:
                failures.append({"check": "required_table_cells", "index": idx,
                                 "error": f"missing cell at table={ti}, row={ri}, column={ci}"})
                continue
            if "equals" in spec and actual != normalize(spec["equals"]):
                failures.append({"check": "required_table_cells", "index": idx,
                                 "error": "exact content mismatch", "actual": actual,
                                 "expected": spec["equals"]})
            if "contains" in spec and normalize(spec["contains"]) not in actual:
                failures.append({"check": "required_table_cells", "index": idx,
                                 "error": "required text not found in cell", "actual": actual,
                                 "expected_substring": spec["contains"]})
        for snippet in expected.get("required_text", []):
            if normalize(snippet) not in full_text:
                failures.append({"check": "required_text", "missing": snippet})

    return {
        "file": str(path),
        "tables": tables,
        "paragraph_count": len(doc.paragraphs),
        "inline_shape_count": len(doc.inline_shapes),
        "candidate_blank_cells": blank_cells[:150],
        "candidate_blank_cell_count": len(blank_cells),
        "expectations_checked": expected_path is not None,
        "expectation_failures": failures,
        "ok": not failures,
        "caveat": "Empty cells may be intentional. This is not rendered-page visual QA."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Input DOCX file")
    parser.add_argument("--expect", type=Path, help="Optional JSON requirements file")
    args = parser.parse_args()
    try:
        result = inspect(args.file, args.expect)
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print(f"DOCX inspection failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

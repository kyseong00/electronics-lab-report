"""Minimal smoke tests for portable electronics skill utilities."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestTokenPreservation(unittest.TestCase):
    def test_preserved_and_changed_tokens(self):
        with tempfile.TemporaryDirectory() as temp:
            a, b = (Path(temp) / n for n in ("a.txt", "b.txt"))
            a.write_text("저항 R_1 = 1 kΩ, V_R = 2.40 V이었다.", encoding="utf-8")
            b.write_text("저항 R_1 = 1 kΩ이며 V_R = 2.40 V였다.", encoding="utf-8")
            ok = subprocess.run([sys.executable, str(ROOT / "scripts/check_preservation.py"), str(a), str(b)], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            b.write_text("저항 R_1 = 1 kΩ이며 V_R = 2.50 V였다.", encoding="utf-8")
            bad = subprocess.run([sys.executable, str(ROOT / "scripts/check_preservation.py"), str(a), str(b)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertTrue(json.loads(bad.stdout)["missing"])

    def test_docx_cell_assertion(self):
        try:
            from docx import Document
        except ImportError:
            self.skipTest("python-docx unavailable")
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "example.docx"
            expected = Path(temp) / "expect.json"
            doc = Document()
            doc.add_paragraph("실험 결과")
            table = doc.add_table(rows=2, cols=3)
            table.cell(1, 2).text = "2.40 mA"
            doc.save(p)
            expected.write_text(json.dumps({"required_table_cells": [{"table": 0,"row": 1,"column": 2,"contains": "2.40 mA"}], "required_text": ["실험 결과"]}, ensure_ascii=False), encoding="utf-8")
            ok = subprocess.run([sys.executable, str(ROOT / "scripts/inspect_docx.py"), str(p), "--expect", str(expected)], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            expected.write_text(json.dumps({"required_table_cells": [{"table": 0,"row": 1,"column": 2,"contains": "4.00 mA"}]}, ensure_ascii=False), encoding="utf-8")
            bad = subprocess.run([sys.executable, str(ROOT / "scripts/inspect_docx.py"), str(p), "--expect", str(expected)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2, bad.stdout + bad.stderr)


if __name__ == "__main__":
    unittest.main()

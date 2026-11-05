#!/usr/bin/env python3
"""Conservative protected-token check for before/after electronics prose edits.

Usage:
    python check_preservation.py original.txt revised.txt

Compares *tokens*, not full semantic equivalence or DOCX structure. A clean result
never proves physical/electrical correctness.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
from pathlib import Path

NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?"
    r"(?:\s*(?:%|dB|Hz|kHz|MHz|GHz|V|mV|uV|µV|A|mA|uA|µA|W|mW|"
    r"Ω|kΩ|MΩ|ohm|kohm|Mohm|F|uF|µF|nF|pF|s|ms|us|µs|°C))?"
)
IDENT_RE = re.compile(
    r"\b(?:[RCLDQJMU]\d+[A-Za-z0-9._-]*|"
    r"[A-Za-z]{1,9}\d[A-Za-z0-9._-]*|"
    r"(?:V|I|R|C|L|f|CH|GND)_[A-Za-z0-9]+|"
    r"V(?:in|out|BE|CE|CC|EE|R|ZD)?|I(?:B|C|E|R|ZD|L)?)\b"
)
LATEX_RE = re.compile(r"\$[^\n$]+\$|\\\([^\n]+?\\\)|\\\[[\s\S]+?\\\]")


def normalize(token: str) -> str:
    return re.sub(r"\s+", "", token)


def tokens(text: str) -> Counter[str]:
    # Retain counts: losing the second occurrence of 10 V is not the same as
    # preserving every occurrence. Overlaps across patterns are intentional.
    return Counter(
        normalize(match.group(0))
        for regex in (LATEX_RE, NUMBER_RE, IDENT_RE)
        for match in regex.finditer(text)
    )


def compare(original: str, revised: str) -> dict:
    before = tokens(original)
    after = tokens(revised)
    missing = [{"token": t, "count": n} for t, n in sorted((before - after).items())]
    added = [{"token": t, "count": n} for t, n in sorted((after - before).items())]
    return {
        "ok": not missing and not added,
        "before_token_count": sum(before.values()),
        "after_token_count": sum(after.values()),
        "missing": missing,
        "added": added,
        "caveat": "Token match is not a semantic, mathematical, or DOCX-layout audit."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="UTF-8 plain-text original")
    parser.add_argument("revised", type=Path, help="UTF-8 plain-text revision")
    args = parser.parse_args()
    result = compare(args.original.read_text(encoding="utf-8"),
                     args.revised.read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

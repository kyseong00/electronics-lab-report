#!/usr/bin/env python3
"""Portable DOCX to per-page PNG renderer for visual QA.

Requires LibreOffice (soffice/libreoffice) and PyMuPDF or pdftoppm. The script
renders only; a person/visual agent must inspect EVERY page image afterward.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def render(input_path: Path, output_dir: Path, dpi: int = 145,
           emit_pdf: bool = False) -> list[Path]:
    source = input_path.resolve()
    if not source.exists() or source.suffix.lower() != ".docx":
        raise RuntimeError(f"Input must be an existing DOCX: {source}")

    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("LibreOffice not found. Install LibreOffice / soffice first.")
    output = output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    pdf = output / (source.stem + ".pdf")

    # Keep LibreOffice's user-profile lock away from a running desktop instance.
    with tempfile.TemporaryDirectory(prefix="electronics-lab-report-lo-") as workspace:
        profile = (Path(workspace) / "lo-profile").resolve()
        cmd = [
            soffice,
            "-env:UserInstallation=" + profile.as_uri(),
            "--headless", "--convert-to", "pdf:writer_pdf_Export",
            "--outdir", str(output), str(source),
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if completed.returncode != 0 or not pdf.exists() or pdf.stat().st_size == 0:
            raise RuntimeError(
                f"LibreOffice conversion failed (exit {completed.returncode}).\n"
                f"stdout: {completed.stdout.strip()}\nstderr: {completed.stderr.strip()}"
            )

    # Avoid falsely reporting stale page PNGs as outputs of this invocation.
    for stale in output.glob("page-*.png"):
        stale.unlink()

    pages: list[Path] = []
    try:
        import fitz  # PyMuPDF
    except ImportError:
        fitz = None

    if fitz:
        with fitz.open(str(pdf)) as document:
            if not document.page_count:
                raise RuntimeError("PDF rendered with zero pages")
            for n, page in enumerate(document, start=1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
                dest = output / f"page-{n}.png"
                pixmap.save(str(dest))
                pages.append(dest)
    else:
        converter = shutil.which("pdftoppm")
        if not converter:
            raise RuntimeError("Install pymupdf (pip install pymupdf) or pdftoppm")
        completed = subprocess.run(
            [converter, "-png", "-r", str(dpi), str(pdf), str(output / "page")],
            capture_output=True, text=True, timeout=120,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"pdftoppm failed: {completed.stderr.strip()}")
        pages = sorted(output.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))

    if not pages or any(p.stat().st_size == 0 for p in pages):
        raise RuntimeError("No usable page images generated")
    if not emit_pdf:
        pdf.unlink(missing_ok=True)
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--output_dir", type=Path, default=Path("qa-pages"))
    parser.add_argument("--dpi", type=int, default=145)
    parser.add_argument("--emit_pdf", action="store_true")
    args = parser.parse_args()
    if not 72 <= args.dpi <= 300:
        parser.error("--dpi must be between 72 and 300")
    try:
        pages = render(args.file, args.output_dir, args.dpi, args.emit_pdf)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"Render failed: {exc}", file=sys.stderr)
        return 1
    print(f"Rendered {len(pages)} page(s):")
    for page in pages:
        print(f"  {page}")
    print("NEXT STEP: Open and visually inspect EVERY page PNG. Rendering is not inspection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

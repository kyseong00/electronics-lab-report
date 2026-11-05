# Word (`.docx`) rendering and page quality assurance

Use this workflow **only when creating, modifying, or verifying Word files**, not for prose-only answers. A valid `.docx` XML document can still have hidden text, clipped tables, missing glyphs or inappropriate page breaks; a plain-text check cannot detect those problems.

## 1. Preserve the course's layout

For existing reports, minimally edit the supplied document rather than reformatting everything. Prioritize the instructor's template, preferred page size, fonts, first-page metadata, headings, captions, tables and margins. If none are specified, use a readable consistent academic layout; do not force another school's conventions.

Check both data placement **inside the Word tables** and visible page formatting. A successful arithmetic walkthrough outside the table is not evidence that the required cells are populated.

## 2. Structural checks

Use a DOCX-aware tool, e.g. `python-docx`, to inspect paragraph/table structure and validate actual cell text. The bundled command helps enumerate possible blank cells; it intentionally does not classify all blanks as errors.

```bash
python -m pip install python-docx
python scripts/inspect_docx.py report.docx
```

When the assignment requires certain table entries, create a JSON expectation file matching `examples/expected-cells.example.json`, then run:

```bash
python scripts/inspect_docx.py report.docx --expect expected-cells.json
```

`table`, `row`, `column` are zero-based indexes. Use a different expectation JSON for each actual assignment; the bundled file is an illustration only. Explicitly confirm all required computed values appear in their table cells.

## 3. Render pages

If the environment provides a document-rendering skill/tool, use its supported rendering entrypoint (e.g. `render_docx.py`). Otherwise, on a machine with LibreOffice and either PyMuPDF or `pdftoppm` available, use the portable bundled renderer:

```bash
# Linux example: ensure LibreOffice is installed; install PyMuPDF if needed
python -m pip install pymupdf
python scripts/render_docx.py report.docx --output_dir qa-pages --emit_pdf
```

This produces `qa-pages/page-1.png`, `page-2.png`, etc. Conversion is done by LibreOffice headless; images are created by PyMuPDF (or `pdftoppm` when available). The script reports missing dependencies. The PDF/PNGs are temporary QA artifacts unless the user asks to receive them.

## 4. Visually inspect **all** pages

Open every page image at readable scale. Inspect:

- cropped or overlapping glyphs, missing Korean/math symbols, font substitution
- table text clipping, empty required result cells, column widths and header alignment
- figures too small, image/caption separated, missing labels or figure captions
- accidental blank pages, excessive gaps, split rows, disjoint captions, broken page numbering
- header/footer overlap, page margins, page orientation, unintended shifts from the reference template

For large reports, inspect **all** pages rather than a thumbnail-only sample. Use screenshots/vision or another available visual review tool. Rendering alone is **not** automatic visual inspection. Word and LibreOffice can lay out some pages differently; tell the user when verification was performed in a different renderer.

## 5. Repair and repeat

Fix the DOCX and **re-render the whole file** after every meaningful layout change. Reinspect the changed page and surrounding pages; complete a final all-page pass. Recheck the required table cell contents after final edits. Never declare a missing value fixed until it is present in the actual final Word table.

## Reporting results and limitations

- Distinguish **structural QA** (cell content) from **visual QA** (rendered pages).
- Do not say "all pages inspected" unless images were actually opened and checked.
- When LibreOffice, PDF conversion or visual inspection is unavailable, provide the best available review and say what was **not** verified.
- Do not silently alter measured data or the instructor's template in order to fix spacing.
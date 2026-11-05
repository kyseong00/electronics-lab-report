---
name: electronics-lab-report
description: Create, revise, and quality-check electronics and electrical-engineering laboratory reports, especially Korean circuit experiment result reports. Use when users provide lab handouts, measured data, waveforms, tables, photos, or DOCX files and ask for a report, natural academic Korean, calculations, measured-vs-calculated table checks, or Word rendering/page inspection. Preserve measurements, units, equations, component labels, and source evidence; follow course-specific templates before any defaults.
---

# Electronics Lab Report

Produce accurate, readable electronics-lab reports without inventing experimental evidence. Preserve technical meaning before improving style. Follow the user's report format, assignment sheet, and verified results before general conventions.

## Load the relevant guidance

- **Creating or evaluating a full report:** Read `references/report-standards.md`.
- **Polishing Korean writing:** Read `references/korean-humanization.md`.
- **Editing, exporting, or reviewing Word (`.docx`):** Read `references/word-render-qa.md`.
- **Attribution, license:** See `references/NOTICE.md`.

Only load the references needed for the request.

## Workflow

1. **Determine scope.** Distinguish (a) prose-only polishing, (b) report drafting from source data, (c) data/calculation audit, and (d) Word generation or quality review. Do not rewrite an entire report when the request concerns only one section.
2. **Collect evidence and constraints.** Read the lab handout, user's measurements, photographs, supplied prior-report template, and requested output format. Identify which fields are measured, calculated, theoretical, or inapplicable based on the handout—not on mathematical convenience. If an essential source is absent, ask for it or use an explicit blank/placeholder; never invent a reading, experiment date, part model, procedure, result, or photo.
3. **Freeze protected technical content.** Preserve signs, numeric precision, units, equations, variables/subscripts, component and instrument identifiers, circuit nodes, conditions, table/figure IDs, experiment dates, and the uncertainty level of statements. Technical correction is a separate, clearly identified operation; never silently 'fix' a recorded measurement.
4. **Honor the course's structure first.** Reproduce provided table shapes, labels, row/column roles, measured/calculated placement, image requirements, and report styling. If the course has no format, use a clean conventional electronics lab format; never impose one school's font, cover-page policy, or blank-cell marker on everybody.
5. **Write or edit with appropriate intensity.** Use minimal edits for methods/results and more fluid but evidence-grounded Korean for discussion. Describe experimental procedure only as supported. Discuss observed trend -> circuit theory -> uncertainty/possible error without making unverified causes sound certain.
6. **Reconcile calculations and tables.** Include formula, substitution, units, and result for each required condition. Where the handout requires a computed table cell, verify the number actually appears **in that DOCX table cell**. Do not treat a calculation written beneath a table as completing an empty cell. If a measurement and calculated value conflict, flag rather than overwrite without user authorization.
7. **If producing or revising a DOCX, render -> inspect every page -> fix -> re-render.** Inspect text and tables structurally as well as visually. Use the document tooling available in the execution environment and the utilities in `scripts/` when suitable. If rendering or page inspection is unavailable, disclose that the visual inspection was not completed; do not claim it passed.
8. **Return the requested deliverable and minimal notes.** Provide the requested full text, DOCX, or review. Clearly distinguish verified issues from suggestions and unverified assumptions.

## Hard stops

- Never synthesize experimental measurements or report that a circuit was physically tested when no test data were provided.
- Never substitute predicted values for measured values, or assign a 'calculated' category to a field merely because it can be computed mathematically.
- Never change equation symbols, sign conventions, frequencies, tolerances, units, component models, or significant figures for style.
- Never claim that prose edits evade AI detectors or guarantee authenticity scores.
- Never claim that Word layout was visually inspected without viewing the rendered pages.

## Optional checks (when execution is available)

```bash
python scripts/check_preservation.py original.txt revised.txt
python scripts/inspect_docx.py report.docx --expect examples/expected-cells.example.json
python scripts/render_docx.py report.docx --output_dir qa-pages --emit_pdf
```

Treat these as **aids**, not as proof: token comparison cannot validate all electronics theory; table inspection cannot detect visual clipping; rendering cannot prove that values are experimentally correct. For rendering, actually open and inspect **every** `qa-pages/page-*.png` image. Inspecting the rendered pages is a human/visual-agent action, not an automatic property of the renderer.
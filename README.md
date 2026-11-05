# Electronics Lab Report

**전자공학 실험보고서를 정확하고 자연스럽게 작성·수정·검수하는 공개용 AI Skill**  
*An AI skill for electronics laboratory reports: data fidelity, natural Korean writing, and Word page quality checks.*

## 무엇을 하나요?

**Skill name:** `electronics-lab-report` · **Display name:** Electronics Lab Report · **Version:** 1.0.0

`Electronics Lab Report`는 전자회로/전자공학 실험에 맞춘 Skill입니다. 다이오드, 제너 다이오드, 트랜지스터, OP 앰프, 필터, 전원회로 등의 실험지와 측정 결과를 기반으로 결과보고서를 작성하거나 기존 보고서의 문장을 다듬습니다. 측정값과 계산값을 구분하고, 지시된 모든 조건의 계산과 표 입력을 검수하며, Word 파일을 만든 경우 실제 페이지가 잘 표시되는지도 확인하도록 안내합니다.

핵심 원칙: **측정하지 않은 결과를 생성하지 않기, 수치·단위·식·모델명을 보존하기, 수업 양식을 우선하기.**

### Features

- **Technical preservation:** Keep measurements, equations, units, circuit labels and instrument settings intact.
- **Natural academic Korean:** Remove translationese and formulaic AI-sounding phrasing without weakening claims.
- **Lab report standards:** Respect each course's worksheet, prescribed tables and computed-vs-measured cell placement.
- **Calculation reconciliation:** Show formulas, substitutions and results for each required condition; check the numbers are in the *actual table cells*.
- **Word QA:** Render DOCX into per-page PNGs, visually inspect every page, fix layout and re-render; optional structural cell assertions.
- **Graceful degradation:** If the environment cannot render Word pages, say so instead of asserting successful QA.

## 설치 / Install

### ChatGPT (when Skills upload is available to your account)

1. Download `skill.zip` from this repository's Releases page, when available. Alternatively, download the source ZIP via **Code → Download ZIP**.
2. In ChatGPT, open **Plugins → Skills → Create → Upload from your computer**.
3. Upload `skill.zip`; review the skill contents and complete any product scan/approval steps.

Skill availability and permissions vary by plan and workspace. A public GitHub repository does **not** auto-install a skill for other users.

### Codex (local installation)

Clone this repository or download its source, then copy the **repository folder** (the one containing `SKILL.md`) to `.agents/skills/electronics-lab-report/` (project) or `~/.agents/skills/electronics-lab-report/` (user). The resulting path must contain `SKILL.md`. Consult the Codex version's Skills documentation for additional supported installation commands.

## 사용 예시 / Example prompts

```text
전자회로 실험지와 측정값을 올렸어. Electronics Lab Report 기준으로 결과보고서를 작성해줘.
수업에서 제공한 표 3-1 구조를 유지하고, 계산값은 반드시 표 안에도 채워줘.
결론 및 토의만 대학생 보고서처럼 자연스럽게 다듬어줘. 숫자와 식은 바꾸지 마.
이 DOCX 보고서를 렌더링한 다음 모든 페이지에서 표 잘림과 빈 계산칸을 확인해줘.
```

For English-speaking users:

```text
Draft an electronics-lab result report from this worksheet and my measurements.
Follow the instructor's tables exactly; do not invent readings.
Audit this DOCX for missing computed cells, render every page, and report layout defects.
```

## Requirements for optional local QA scripts

The core skill consists of Markdown guidance and works even without Python. To run the optional scripts:

- `check_preservation.py`: Python 3.10+; no third-party packages.
- `inspect_docx.py`: `python-docx`.
- `render_docx.py`: LibreOffice and **PyMuPDF** (`pip install pymupdf`) or `pdftoppm`.

```bash
python -m pip install python-docx pymupdf
python scripts/check_preservation.py before.txt after.txt
python scripts/inspect_docx.py report.docx
python scripts/render_docx.py report.docx --output_dir qa-pages --emit_pdf
```

For assignment-specific cell assertions, copy `examples/expected-cells.example.json`, replace the illustrative cell coordinates and value with your assignment's actual expectation, and run:

```bash
python scripts/inspect_docx.py report.docx --expect expected-cells.json
```

**Important:** Scripts do not automatically prove correctness. `render_docx.py` produces images, but a human or visual AI agent must open and review **every page**. `inspect_docx.py` checks document structure rather than physical layout. Do not use illustrative example values as actual report data.

## Repository layout

```text
(repository root)
├── SKILL.md                 # Skill instructions and activation description
├── README.md                # Guide (Korean + English)
├── LICENSE                  # Electronics Lab Report distribution license (MIT)
├── LICENSE-im-not-ai.txt    # Original upstream license notice
├── agents/openai.yaml
├── assets/icon.svg
├── references/
│   ├── report-standards.md
│   ├── korean-humanization.md
│   ├── word-render-qa.md
│   └── NOTICE.md
├── examples/expected-cells.example.json
├── scripts/
│   ├── check_preservation.py
│   ├── inspect_docx.py
│   └── render_docx.py
└── tests/test_tools.py
```

## Scope & limitations

- Does not replace actual bench measurements, lab attendance, or a domain expert's judgment.
- Does not guarantee that technical calculations are correct or that errors have been measured.
- Does not claim AI-detection evasion or detector scores.
- Applies your course's format (fonts, margins, cover policy, table conventions, caption style) over generic defaults. No single university's form is hard-coded.
- Rendering depends on the available operating system, fonts and office conversion tools; your instructor's Microsoft Word rendering may vary slightly from LibreOffice.

## Attribution / License

Released under MIT for the new Electronics Lab Report files; see `LICENSE`. The predecessor workflow was independently adapted for ChatGPT based on general ideas from [`epoko77-ai/im-not-ai`](https://github.com/epoko77-ai/im-not-ai). This is not an official release or endorsement of that project. The original author's MIT copyright/license text is included as `LICENSE-im-not-ai.txt`; see `references/NOTICE.md`.

Contributions are welcome. Proposed edits should preserve the prohibition on invented measurements and on silent mutation of user-supplied technical data.

## Official skills documentation

- [ChatGPT Skills: create, upload, and share](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
- [Codex documentation](https://developers.openai.com/codex/)
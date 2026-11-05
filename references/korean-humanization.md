# Korean electronics-lab writing: conservative humanization

Improve Korean fluency without reducing technical specificity or changing evidence.

## Preserve protected spans

Measurements, calculations, units, tolerances, signed values, scientific notation, equations, variables, pin names, component labels (`R_F`, `R_1`, `CH1`, `V_in`), device models, node names, setup conditions, dates, table numbers, captions, source quotations, and the level of uncertainty are immutable unless correction is explicitly requested and verified.

## Preferred edits

- Replace translationese or abstract English-like constructions with idiomatic Korean that identifies the actual measured phenomenon.
- Reduce repetitive transitions (`이를 통해`, `또한`, `따라서`) when the reasoning remains clear without them.
- Avoid successive sentences with identical frame/endings where natural variation improves reading.
- Use direct verbs instead of unnecessary nominalizations and passive voice when the actor is known.
- Replace vague evaluations (`중요성을 확인할 수 있었다`, `유의미한 결과를 도출하였다`) with the source-supported observation and circuit explanation, or remove unsupported filler.
- Avoid overly ornate professional terminology for undergraduate lab prose.
- Retain conventional electronics English abbreviations and symbol repetition when essential for interpretation.

## Editing levels

- **Conservative** (default for procedure, results, calculation): repair obvious grammar, awkward phrasing, and redundancy; preserve sentence order and all evidence.
- **Standard** (default for conclusion/discussion): improve paragraph flow and connect observed behavior to supported theory while preserving certainty.
- **Strong** (only if user asks): restructure narrative prose, never experimental data, tables, formulas or source claims.

Do not rewrite natural sentences merely to avoid similarity. Do not add newly invented reflections on oscilloscope operation, difficulties encountered, error causes or observations.

## Safety check

For any revised sentence, ask whether any claim was added, removed, strengthened, weakened, or made ambiguous. Revert if yes. For dense prose, use `scripts/check_preservation.py` and manually review its findings; a clean token check does not guarantee factual fidelity. Do not promise to fool AI detectors.
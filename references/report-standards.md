# Electronics laboratory report standards

Use these rules for electronics and electrical-engineering laboratory result reports: resistors, diode/Zener circuits, transistors, operational amplifiers, filters, oscillators, digital circuits, power electronics, and similar experiments. Adjust terminology and sections to the actual course.

## Priority of instructions

1. Explicit current user request.
2. Course handout / scoring rubric / supplied report template.
3. Verified experiment data and descriptions.
4. Optional reference report **format** (never copy its unrelated experimental readings).
5. Defaults in this reference.

Do not impose a fixed Korean font such as Gulim, a no-cover rule, an `X` blank-cell marker, or a particular table schema unless the user/course requests it. If no template exists, a conventional sequence is: objective -> components/equipment -> procedure -> results/analysis -> conclusion/discussion. Include report metadata only as required or available; leave unavailable personal fields blank rather than fabricating them.

## Components and equipment

List **only known** parts and equipment actually used. Include measurement and power/signal devices as appropriate (digital multimeter, oscilloscope, function generator, DC supply, probes, breadboard). Preserve exact models and quantities if provided. Otherwise use device category alone—do not guess a brand/model or resistor count. A compact two-column parts/equipment table is a reasonable fallback, not an overriding rubric.

## Experimental procedure

Describe actual connection topology, input and supply settings, measurement locations, and order, insofar as supported by the source. Keep inverting/non-inverting topology, feedback and input resistor roles, ground references, channel labels, probe settings, instrument range and other technical conditions intact. Do not infer that a feature or setting (AC coupling, averaging, 10x probe, auto-scale, etc.) was used just because it is common.

## Results and table fidelity

- Match the instructor's exact table structure, table numbering, column headers, conditions, measured/calculated row assignments, and units when provided.
- Distinguish **measured**, **computed**, and **theoretical** information. Only fields the assignment tells students to compute belong in formal "computed" slots. Other useful relationships may be discussed separately, if relevant, without misclassifying an entry.
- Do not guess missing measurements. Where the user wants a printable unfinished report, mark missing required values clearly and consistently as blanks or placeholders. Use `X` only where the course requires inapplicable cells to be marked that way; don't confuse `X` with unrecorded measurements.
- Carry sign conventions, units, decimal places and significant figures through every calculation. Do not round too early.
- Where the assignment requires values for several input voltages, resistor settings, frequency steps, or configurations, compute **all supported conditions** and fill the designated cells. A worked equation under a table is not a substitute for filling the table itself.
- Put each picture adjacent to a caption or explanatory sentence identifying exactly what is measured or illustrated. If a user will insert photos, put `[사진 삽입]` and a meaningful supported description without inventing a waveform observation.

## Calculation walkthrough

Explain the relationship used, show formula, substitute actual **provided** quantities, show units, and calculate. Example of purely *illustrative* arithmetic, **never to be inserted as data into a user's report**:

```
I_R = V_R / R
    = 2.40 V / 1.00 kΩ
    = 2.40 mA
```

Use the handout's notation (e.g., `V_R`, `V_ZD`, `I_ZD`) and distinguish measured `V_R` from any independently estimated `V_PS - V_ZD`. When testing for consistency, report potential discrepancies separately instead of overwriting measured readings.

## Discussion and causality

In a complete report, give at least two substantive lines, usually a paragraph or more. Tie the *observed* results or waveforms to the correct circuit principle (e.g. resistor current relationship, diode conduction, Zener breakdown, op-amp feedback, frequency response). Explain observed patterns and limitations rather than reciting figures. If differences may stem from component tolerance, supply variation, measurement resolution or contact resistance, phrase them as **possible** causes unless measured or otherwise verified. A tiny reading close to instrument resolution is not proof that the real quantity is exactly zero.

## Before delivery

Check every requested table/graph/photo, every provided experiment condition, calculation source and output unit, and every value's actual destination. If the user provided a reference DOCX, compare the layout, including section headings, font, table widths and photo caption style. If a DOCX was produced, follow `word-render-qa.md` before claiming that its pages are correctly formatted.
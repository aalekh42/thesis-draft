# SIGCSE Problem Framing Analysis Package

This reproducibility package contains the Jupyter notebook, dataset files, coding sheet, and analysis outputs used for the SIGCSE poster extended abstract:

**What Students Include and Omit When Framing Data Science Problems: Early Evidence from Course-Completion Problem Statements**

## Contents

- `notebooks/SIGCSE_problem_framing_analysis.ipynb` — executable notebook that reproduces the filtering, descriptive statistics, coding summaries, inter-rater agreement, and component-presence figure.
- `data/submissions_2026-06-18.csv` — raw early export of 21 drafts.
- `data/unaided_submissions_filtered.csv` — filtered subset with no scaffold suggestions shown or accepted.
- `data/problem_framing_coding_sheet.xlsx` — coding workbook with instructions and rater tabs.
- `data/resolved_component_codes.csv` — binary component codes used for the manuscript counts. This file is taken from the Rater 2 tab of the current coding sheet because it matches the reported resolved counts.
- `results/component_presence_summary.csv` — reproduced draft-level and participant-level counts.
- `results/inter_rater_agreement.csv` — agreement calculation from the Rater 1 and Rater 2 tabs.
- `figures/component_presence_polished.png` — final figure used in the paper.
- `paper/` — current polished TeX/PDF copy of the manuscript, when included.

## How to run

1. Unzip the package.
2. Install the dependencies in `requirements.txt`.
3. Open `notebooks/SIGCSE_problem_framing_analysis.ipynb` from the package root.
4. Run all cells.

Example:

```bash
pip install -r requirements.txt
jupyter notebook notebooks/SIGCSE_problem_framing_analysis.ipynb
```

## Method note

The notebook uses the same coding logic described in the poster. It treats participant-level counts as primary by selecting each user's longest unaided draft, breaking ties by the later draft identifier. Draft-level counts are also reported for transparency.

Before reporting inter-rater reliability in a submitted manuscript, confirm that both rater tabs represent independent human coding. If one tab was AI-assisted or used as a first-pass check, use the notebook for reproducibility but do not describe the agreement values as human inter-rater reliability.

## Reviewer-addressed paper update

The package also includes `paper/SIGCSE_problem_framing_reviewer_addressed.tex` and `.pdf`, which incorporate the later reviewer-driven changes:

- added a concise task summary;
- clarified that participant-level counts are primary;
- added a small-sample caution about broad patterns versus exact low-frequency rankings;
- added one anchored success-criteria example;
- clarified coder independence in the paper text;
- added one additional data science education reference.

As before, report the two-coder agreement only if both coding columns represent independent human coding.

## Figure and build notes (this revision)

- The component-presence figure now uses a teal palette and is generated directly
  by the notebook cell that writes `figures/component_presence_reproduced.png`.
  `figures/component_presence_polished.png` (referenced by the paper) is a copy of
  that notebook output, so the published figure is now reproducible from the notebook.
- The bundled `paper/*.pdf` in this sandbox was rebuilt without the ACM fonts
  (Linux Libertine / newtxmath), so it may render 3 pages. Compile the `.tex` in an
  environment with the ACM fonts (e.g., Overleaf) to get the intended 2-page layout.

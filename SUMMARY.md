# Project Summary

## What This Project Is

This is a **reproducibility package** for a SIGCSE (Special Interest Group on Computer Science Education) poster extended abstract titled:

> **"What Students Include and Omit When Framing Data Science Problems: Early Evidence from Course-Completion Problem Statements"**

The project examines how students frame data science problems when writing problem statements about online-learning course-completion. It captures participant expertise, task completion, AI scaffold interactions, quality ratings, and (for a coded subset) the presence of specific problem-framing components.

---

## Primary Dataset (`convertcsv.csv`)

The main dataset is a participant-level CSV with one row per session (30 participants total).

| Metric | Value |
|--------|-------|
| Total participants | 30 |
| Completers (submitted a draft) | 17 (56.7%) |
| Non-completers | 13 |
| Expertise: Beginner | 8 (27%) |
| Expertise: Intermediate | 14 (47%) |
| Expertise: Advanced | 8 (27%) |
| Mean expertise score | 9.07 |
| Mean pre-test score | 4.67 |
| Mean AI attitude score | 5.20 |

### Completer writing statistics (n=17)

| Metric | Value |
|--------|-------|
| Word count range | 22 -- 225 |
| Word count mean / median | 113.5 / 106 |
| Time spent range | 7 -- 529 seconds |
| Time spent median | 172s |
| Revision count range | 0 -- 60 |
| Revision count mean | 13.1 |

### Columns in `convertcsv.csv`

`session_id`, `ai_condition`, `expertise_level`, `expertise_score`, `pre_test_score`, `ai_attitude_score`, `completed`, `word_count`, `revision_count`, `time_spent_seconds`, `ai_suggestions_shown`, `ai_suggestions_accepted`, `ai_acceptance_rate`, `found_engaging`, `felt_motivated`, `ai_helpful`, `own_work`, `would_use_again`, `avg_creativity`, `avg_clarity`, `avg_completeness`, `avg_feasibility`, `n_raters`

---

## Completion by Expertise Level

| Level | Total | Completed | Rate |
|-------|-------|-----------|------|
| Beginner | 8 | 2 | 25.0% |
| Intermediate | 14 | 8 | 57.1% |
| Advanced | 8 | 7 | 87.5% |

Higher expertise is strongly associated with task completion.

---

## Quality Ratings (Completers, n=17)

Drafts were rated by external raters on four dimensions:

| Dimension | Mean | SD | Min | Median | Max |
|-----------|------|----|-----|--------|-----|
| Creativity | 3.44 | 0.60 | 2.00 | 3.50 | 4.50 |
| Clarity | 4.14 | 1.49 | 2.25 | 3.75 | 6.00 |
| Completeness | 3.77 | 1.40 | 2.00 | 3.25 | 6.25 |
| Feasibility | 4.53 | 1.12 | 2.50 | 4.50 | 6.00 |

### Quality by expertise level

| Level | Creativity | Clarity | Completeness | Feasibility |
|-------|------------|---------|--------------|-------------|
| Beginner | 3.00 | 3.00 | 2.88 | 3.38 |
| Intermediate | 3.66 | 4.67 | 4.30 | 4.79 |
| Advanced | 3.32 | 3.86 | 3.43 | 4.57 |

Intermediate participants scored highest on clarity and completeness; advanced participants scored comparably on feasibility but lower on clarity than intermediates.

---

## AI Scaffold Usage (Completers, n=17)

| Metric | Value |
|--------|-------|
| Completers who saw AI suggestions | 11 |
| Completers with no AI shown | 6 |
| Mean suggestions shown | 2.71 |
| Mean suggestions accepted | 1.88 |
| Mean acceptance rate | 73% |

---

## Component Presence (Coded Subset: 10 of 17 Completers)

Two raters independently coded unaided drafts for the presence (1) or absence (0) of eight problem-framing components. Component coding is available for **10 participants** (15 drafts) out of the 17 completers; the remaining 7 completers lack draft text in the available data files.

The eight components are organized into three tiers:

### Scenario-derived (given by the task prompt)
| Component | Description |
|-----------|-------------|
| **Data/features** | Mentions the data or features available |

### Prompt-named facets (explicitly asked for in the prompt)
| Component | Description |
|-----------|-------------|
| **Aligned problem** | States a problem aligned with the scenario |
| **Analytic objective** | Specifies an analytic/modeling goal |
| **Method/model** | Names or implies a method or model |
| **Explicit constraints** | States constraints or limitations |
| **Success criteria** | Defines how success would be measured |

### Extended responsible-framing indicators
| Component | Description |
|-----------|-------------|
| **Stakeholder/action** | Identifies a stakeholder or actionable use |
| **Ethics/privacy/fairness** | Raises ethics, privacy, or fairness concerns |

### Results (participant-level, n=10 coded)

| Component | Present | % |
|-----------|---------|---|
| Data/features | 9/10 | 90% |
| Aligned problem | 8/10 | 80% |
| Analytic objective | 8/10 | 80% |
| Method/model | 7/10 | 70% |
| Explicit constraints | 4/10 | 40% |
| Stakeholder/action | 4/10 | 40% |
| Success criteria | 3/10 | 30% |
| Ethics/privacy/fairness | 2/10 | 20% |

**Pattern**: Students reliably included the basic components (data, problem, objective, method) but frequently omitted the more advanced framing elements -- constraints, success criteria, stakeholder considerations, and especially ethics/privacy/fairness concerns.

### Inter-rater agreement

- **120 total coding decisions** (15 drafts x 8 components)
- **95.0% agreement** between the two raters
- **Cohen's kappa = 0.90** (near-perfect agreement)
- Only **6 disagreements**, primarily on "Analytic objective" (3 cases), "Explicit constraints" (1), "Data/features" (1), and "Method/model" (1)

The README notes a caveat: the agreement values should only be reported as human inter-rater reliability if both rater columns represent independent human coding (as opposed to AI-assisted first-pass).

---

## Project Structure

```
Code/
├── README.md                              # Original project overview
├── SUMMARY.md                             # This summary
├── requirements.txt                       # Python dependencies
├── convertcsv.csv                         # Primary dataset (30 participants, participant-level)
├── submissions_2026-06-18.csv             # Multi-phase submissions (48 rows, no draft text)
├── run_analysis.py                        # Standalone analysis script (generates analysis_output/)
│
├── data/
│   ├── DATA_DICTIONARY.md                 # Column descriptions for original CSV files
│   ├── submissions_2026-06-18.csv         # Original raw export (21 drafts, 10 participants, with draft text)
│   ├── unaided_submissions_filtered.csv   # 15 unaided drafts (filtered)
│   ├── problem_framing_coding_sheet.xlsx  # Coding workbook with Rater 1 and Rater 2 tabs
│   └── resolved_component_codes.csv       # Binary component codes (15 drafts x 8 components)
│
├── notebooks/
│   └── SIGCSE_problem_framing_analysis.ipynb  # Original notebook (works with data/ files)
│
├── results/                               # Original notebook outputs
│   ├── component_presence_summary.csv
│   ├── inter_rater_agreement.csv
│   └── coding_disagreements.csv
│
├── figures/                               # Original notebook figures
│   ├── component_presence_reproduced.png
│   └── component_presence_polished.png
│
├── paper/                                 # (empty in this copy)
│
└── analysis_output/                       # Generated by run_analysis.py
    ├── results/
    │   ├── descriptive_summary.csv        # Overall participant stats
    │   ├── completion_by_expertise.csv    # Completion rates by expertise
    │   ├── quality_ratings_summary.csv    # Quality dimension statistics
    │   ├── quality_by_expertise.csv       # Quality broken down by expertise
    │   ├── ai_scaffold_usage.csv          # Per-completer AI scaffold data
    │   ├── ai_usage_summary.csv           # Aggregate AI usage stats
    │   └── component_presence_summary.csv # Component counts (coded subset)
    └── figures/
        ├── completion_by_expertise.png    # Stacked bar: completion by expertise
        ├── expertise_distribution.png     # Pie: beginner/intermediate/advanced split
        ├── word_count_distribution.png    # Histogram with mean/median lines
        ├── time_spent_distribution.png    # Histogram with median line
        ├── quality_ratings_overall.png    # Bar chart with error bars (4 dimensions)
        ├── quality_ratings_by_expertise.png  # Grouped bars by expertise
        ├── expertise_vs_pretest.png       # Scatter: expertise score vs pre-test
        ├── ai_suggestions_shown_vs_accepted.png  # Paired bars per participant
        ├── revisions_vs_wordcount.png     # Scatter colored by expertise
        └── component_presence_polished.png  # Horizontal bar chart (coded subset)
```

---

## How to Run the Analysis

```bash
pip install -r requirements.txt
python run_analysis.py
```

This reads `convertcsv.csv` and `data/resolved_component_codes.csv`, then writes all CSVs and figures to `analysis_output/`.

The original Jupyter notebook (`notebooks/SIGCSE_problem_framing_analysis.ipynb`) can still be run separately against the files in `data/` for the original 10-participant analysis.

---

## Data File Relationships

- **`convertcsv.csv`** (30 participants) is the primary dataset used by `run_analysis.py`. One row per participant with metadata, completion status, quality ratings, and AI scaffold metrics.
- **`submissions_2026-06-18.csv`** (root-level, 48 rows) contains multi-phase data for all 30 participants (phase 1 = no-ai, phase 2 = ai-support) but no draft text.
- **`data/submissions_2026-06-18.csv`** (21 rows) is the original smaller export with draft text (`content` column) for 10 participants only.
- **`data/resolved_component_codes.csv`** (15 rows) has binary component coding for the 10 participants whose draft text was available and coded by raters.

The 7 completers present in `convertcsv.csv` but absent from the component coding lack draft text in any available file, so their components could not be coded.

---

## Dependencies

- `pandas >= 2.0`
- `numpy >= 1.24`
- `matplotlib >= 3.7`
- `openpyxl >= 3.1`
- `jupyter >= 1.0` (for the original notebook only)
- `nbclient >= 0.9` (for the original notebook only)

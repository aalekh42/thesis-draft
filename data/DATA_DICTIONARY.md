# Data dictionary

## submissions_2026-06-29.csv
Raw export with one row per submitted draft (39 rows, 19 sessions).

Key columns:
- `session_id`: anonymous session identifier.
- `phase`: task phase (`1` or `2`).
- `ai_condition`: exported condition label (`no-ai` or `ai-support`).
- `expertise_level`: descriptive expertise category (`beginner`, `intermediate`, `advanced`).
- `expertise_score`, `pre_test_score`: pre-task expertise measures.
- `word_count`, `revision_count`, `time_spent_seconds`: writing-process metadata.
- `ai_suggestions_shown`, `ai_suggestions_accepted`: scaffold activity counts used for filtering.
- `submitted_at`: submission timestamp.
- `content`: draft text.

## unaided_submissions_filtered.csv
Rows from the raw export where `ai_suggestions_shown == 0` and `ai_suggestions_accepted == 0` (26 rows, 19 sessions).

## resolved_component_codes.csv
One row per unaided draft (26 rows). Binary columns use `1 = present` and `0 = absent`.

Columns:
- `Draft`: draft identifier (D01, D02, ...).
- `User`: anonymised user label.
- `Expertise`: expertise level.
- `Words`: word count.
- `Draft text`: full draft content.
- `# present`: count of components present.
- `Notes`: optional rater notes.

Components:
- `Data/features`
- `Aligned problem`
- `Analytic objective`
- `Method/model`
- `Explicit constraints`
- `Stakeholder/action`
- `Success criteria`
- `Ethics/privacy/fairness`

## problem_framing_coding_sheet.xlsx
Coding workbook with four tabs:
- `Instructions`: coding guidelines and component definitions.
- `Rater 1`: independent coding by first rater (26 drafts).
- `Rater 2`: independent coding by second rater (26 drafts).
- `Agreement`: inter-rater agreement calculations (208 binary decisions).

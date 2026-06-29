# Data dictionary

## submissions_2026-06-18.csv
Raw early export with one row per submitted draft.

Key columns:
- `session_id`: anonymous session identifier.
- `ai_condition`: exported condition label.
- `expertise_level`: descriptive expertise category.
- `expertise_score`, `pre_test_score`: pre-task expertise measures.
- `word_count`, `revision_count`, `time_spent_seconds`: writing-process metadata.
- `ai_suggestions_shown`, `ai_suggestions_accepted`: scaffold activity counts used for filtering.
- `submitted_at`: submission timestamp.
- `content`: draft text.

## unaided_submissions_filtered.csv
Rows from the raw export where `ai_suggestions_shown == 0` and `ai_suggestions_accepted == 0`.

## resolved_component_codes.csv
One row per coded unaided draft. Binary columns use `1 = present` and `0 = absent`.

Components:
- `Data/features`
- `Aligned problem`
- `Analytic objective`
- `Method/model`
- `Explicit constraints`
- `Stakeholder/action`
- `Success criteria`
- `Ethics/privacy/fairness`

"""
Standalone analysis script for the SIGCSE Problem Framing study.

Reads convertcsv.csv (participant-level data with completion flags,
quality ratings, expertise, and AI scaffold metrics) and generates
descriptive statistics, breakdowns, and figures.

All outputs are written to analysis_output/.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ── paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "convertcsv.csv"
RESOLVED_CODES = ROOT / "data" / "resolved_component_codes.csv"
OUT_DIR = ROOT / "analysis_output"
FIG_DIR = OUT_DIR / "figures"
RESULTS_DIR = OUT_DIR / "results"

COMPONENTS = [
    "Data/features",
    "Aligned problem",
    "Analytic objective",
    "Method/model",
    "Explicit constraints",
    "Stakeholder/action",
    "Success criteria",
    "Ethics/privacy/fairness",
]

# ── palette ────────────────────────────────────────────────────────────
TEAL_DARK = "#0B6E75"
TEAL_MID = "#3C8A92"
TEAL_LIGHT = "#5FB0B7"
ORANGE = "#E85D3A"
YELLOW = "#F5A623"
GREY = "#E8E8E8"

EXPERTISE_COLORS = {
    "beginner": TEAL_LIGHT,
    "intermediate": TEAL_MID,
    "advanced": TEAL_DARK,
}

# ── setup ──────────────────────────────────────────────────────────────
OUT_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

plt.rcParams.update({"font.size": 12})

# ======================================================================
# 1. Load data
# ======================================================================
df = pd.read_csv(CSV_PATH)
completers = df[df["completed"] == 1].copy()
non_completers = df[df["completed"] == 0].copy()

QUALITY_COLS = ["avg_creativity", "avg_clarity", "avg_completeness", "avg_feasibility"]

print("=" * 60)
print("SIGCSE Problem Framing — Analysis of convertcsv.csv")
print("=" * 60)

# ======================================================================
# 2. Overall descriptive summary
# ======================================================================
summary = {
    "total_participants": len(df),
    "completers": int(df["completed"].sum()),
    "non_completers": int((df["completed"] == 0).sum()),
    "completion_rate_pct": round(100 * df["completed"].mean(), 1),
    "expertise_beginner": int((df["expertise_level"] == "beginner").sum()),
    "expertise_intermediate": int((df["expertise_level"] == "intermediate").sum()),
    "expertise_advanced": int((df["expertise_level"] == "advanced").sum()),
    "expertise_score_mean": round(df["expertise_score"].mean(), 2),
    "expertise_score_median": float(df["expertise_score"].median()),
    "pre_test_score_mean": round(df["pre_test_score"].mean(), 2),
    "ai_attitude_score_mean": round(df["ai_attitude_score"].mean(), 2),
}

# Completer-only stats
if len(completers) > 0:
    summary.update({
        "word_count_min": int(completers["word_count"].min()),
        "word_count_mean": round(float(completers["word_count"].mean()), 1),
        "word_count_median": float(completers["word_count"].median()),
        "word_count_max": int(completers["word_count"].max()),
        "time_spent_min_s": int(completers["time_spent_seconds"].min()),
        "time_spent_median_s": float(completers["time_spent_seconds"].median()),
        "time_spent_max_s": int(completers["time_spent_seconds"].max()),
        "revision_min": int(completers["revision_count"].min()),
        "revision_mean": round(float(completers["revision_count"].mean()), 1),
        "revision_max": int(completers["revision_count"].max()),
    })

pd.DataFrame([summary]).to_csv(RESULTS_DIR / "descriptive_summary.csv", index=False)

print("\n--- Overall Summary ---")
for k, v in summary.items():
    print(f"  {k}: {v}")

# ======================================================================
# 3. Completion by expertise level
# ======================================================================
expertise_order = ["beginner", "intermediate", "advanced"]
completion_by_exp = (
    df.groupby("expertise_level")
    .agg(
        total=("completed", "count"),
        completed=("completed", "sum"),
    )
    .reindex(expertise_order)
)
completion_by_exp["non_completed"] = completion_by_exp["total"] - completion_by_exp["completed"]
completion_by_exp["completion_rate_pct"] = (
    100 * completion_by_exp["completed"] / completion_by_exp["total"]
).round(1)
completion_by_exp.to_csv(RESULTS_DIR / "completion_by_expertise.csv")

print("\n--- Completion by Expertise ---")
print(completion_by_exp.to_string())

# ======================================================================
# 4. Quality ratings summary (completers only)
# ======================================================================
quality_stats = completers[QUALITY_COLS].describe().T
quality_stats = quality_stats[["count", "mean", "std", "min", "50%", "max"]]
quality_stats.columns = ["n", "mean", "std", "min", "median", "max"]
quality_stats = quality_stats.round(2)
quality_stats.to_csv(RESULTS_DIR / "quality_ratings_summary.csv")

print("\n--- Quality Ratings (completers) ---")
print(quality_stats.to_string())

# ======================================================================
# 5. Quality ratings by expertise (completers only)
# ======================================================================
quality_by_exp = (
    completers.groupby("expertise_level")[QUALITY_COLS]
    .mean()
    .reindex([e for e in expertise_order if e in completers["expertise_level"].values])
    .round(2)
)
quality_by_exp.to_csv(RESULTS_DIR / "quality_by_expertise.csv")

print("\n--- Mean Quality Ratings by Expertise ---")
print(quality_by_exp.to_string())

# ======================================================================
# 6. AI scaffold usage (completers only)
# ======================================================================
ai_usage = completers[["session_id", "expertise_level", "ai_suggestions_shown",
                        "ai_suggestions_accepted", "ai_acceptance_rate"]].copy()
ai_usage.to_csv(RESULTS_DIR / "ai_scaffold_usage.csv", index=False)

ai_summary = {
    "completers_with_ai_shown": int((completers["ai_suggestions_shown"] > 0).sum()),
    "completers_no_ai_shown": int((completers["ai_suggestions_shown"] == 0).sum()),
    "mean_suggestions_shown": round(float(completers["ai_suggestions_shown"].mean()), 2),
    "mean_suggestions_accepted": round(float(completers["ai_suggestions_accepted"].mean()), 2),
    "mean_acceptance_rate": round(float(completers["ai_acceptance_rate"].dropna().mean()), 2)
    if completers["ai_acceptance_rate"].dropna().shape[0] > 0
    else None,
}
pd.DataFrame([ai_summary]).to_csv(RESULTS_DIR / "ai_usage_summary.csv", index=False)

print("\n--- AI Scaffold Usage (completers) ---")
for k, v in ai_summary.items():
    print(f"  {k}: {v}")

# ======================================================================
# 7. Component presence analysis (from resolved_component_codes.csv)
# ======================================================================
codes = pd.read_csv(RESOLVED_CODES)
for c in COMPONENTS:
    codes[c] = codes[c].astype(int)
codes["draft_num"] = codes["Draft"].str.extract(r"(\d+)").astype(int)

# Participant-level: longest unaided draft per user, ties broken by later draft
participant_codes = (
    codes.sort_values(["User", "Words", "draft_num"], ascending=[True, False, False])
    .drop_duplicates("User", keep="first")
    .copy()
)

comp_rows = []
for c in COMPONENTS:
    dc = int(codes[c].sum())
    pc = int(participant_codes[c].sum())
    comp_rows.append({
        "component": c,
        "draft_count": dc,
        "draft_n": len(codes),
        "draft_pct": round(100 * dc / len(codes), 2),
        "participant_count": pc,
        "participant_n": len(participant_codes),
        "participant_pct": round(100 * pc / len(participant_codes), 2),
    })

component_summary = pd.DataFrame(comp_rows)
component_summary.to_csv(RESULTS_DIR / "component_presence_summary.csv", index=False)

print("\n--- Component Presence (participant level) ---")
for _, r in component_summary.iterrows():
    print(f"  {r['component']:30s}  {int(r['participant_count'])}/{int(r['participant_n'])}  ({r['participant_pct']:.0f}%)")

# ======================================================================
# FIGURES
# ======================================================================

# --- Fig 1: Completion rate by expertise (stacked bar) ----------------
fig1, ax1 = plt.subplots(figsize=(8, 5))
x = np.arange(len(completion_by_exp))
w = 0.5
ax1.bar(x, completion_by_exp["completed"], w, label="Completed", color=TEAL_DARK)
ax1.bar(x, completion_by_exp["non_completed"], w,
        bottom=completion_by_exp["completed"], label="Did not complete", color=GREY)
ax1.set_xticks(x)
ax1.set_xticklabels(completion_by_exp.index.str.capitalize(), fontsize=13)
ax1.set_ylabel("Number of Participants")
ax1.set_title("Task Completion by Expertise Level")
ax1.legend(frameon=False)
ax1.spines[["top", "right"]].set_visible(False)

for i, (_, row) in enumerate(completion_by_exp.iterrows()):
    total = int(row["total"])
    comp = int(row["completed"])
    ax1.text(i, total + 0.3, f"{comp}/{total} ({row['completion_rate_pct']:.0f}%)",
             ha="center", va="bottom", fontsize=11, color=TEAL_DARK)

fig1.tight_layout()
fig1.savefig(FIG_DIR / "completion_by_expertise.png", dpi=300, bbox_inches="tight")
plt.close(fig1)
print(f"\n[OK] {FIG_DIR / 'completion_by_expertise.png'}")

# --- Fig 2: Expertise distribution (all participants) -----------------
exp_counts = df["expertise_level"].value_counts().reindex(expertise_order)
fig2, ax2 = plt.subplots(figsize=(6, 6))
colors = [EXPERTISE_COLORS[e] for e in expertise_order]
ax2.pie(exp_counts.values, labels=[e.capitalize() for e in exp_counts.index],
        autopct="%1.0f%%", colors=colors, startangle=90,
        textprops={"fontsize": 14})
ax2.set_title("Participant Expertise Distribution", fontsize=15, pad=15)
fig2.tight_layout()
fig2.savefig(FIG_DIR / "expertise_distribution.png", dpi=300, bbox_inches="tight")
plt.close(fig2)
print(f"[OK] {FIG_DIR / 'expertise_distribution.png'}")

# --- Fig 3: Word count distribution (completers) ---------------------
fig3, ax3 = plt.subplots(figsize=(9, 5))
ax3.hist(completers["word_count"], bins=10, color=TEAL_DARK, edgecolor="white", linewidth=0.8)
mean_wc = completers["word_count"].mean()
med_wc = completers["word_count"].median()
ax3.axvline(mean_wc, color=ORANGE, linestyle="--", linewidth=1.5,
            label=f"Mean ({mean_wc:.0f})")
ax3.axvline(med_wc, color=YELLOW, linestyle="--", linewidth=1.5,
            label=f"Median ({med_wc:.0f})")
ax3.set_xlabel("Word Count")
ax3.set_ylabel("Number of Participants")
ax3.set_title("Word Count Distribution (Completers)")
ax3.legend(frameon=False)
ax3.spines[["top", "right"]].set_visible(False)
fig3.tight_layout()
fig3.savefig(FIG_DIR / "word_count_distribution.png", dpi=300, bbox_inches="tight")
plt.close(fig3)
print(f"[OK] {FIG_DIR / 'word_count_distribution.png'}")

# --- Fig 4: Time spent distribution (completers) ---------------------
fig4, ax4 = plt.subplots(figsize=(9, 5))
ax4.hist(completers["time_spent_seconds"], bins=10, color=TEAL_LIGHT, edgecolor="white", linewidth=0.8)
med_t = completers["time_spent_seconds"].median()
ax4.axvline(med_t, color=ORANGE, linestyle="--", linewidth=1.5,
            label=f"Median ({med_t:.0f}s)")
ax4.set_xlabel("Time Spent (seconds)")
ax4.set_ylabel("Number of Participants")
ax4.set_title("Time Spent Distribution (Completers)")
ax4.legend(frameon=False)
ax4.spines[["top", "right"]].set_visible(False)
fig4.tight_layout()
fig4.savefig(FIG_DIR / "time_spent_distribution.png", dpi=300, bbox_inches="tight")
plt.close(fig4)
print(f"[OK] {FIG_DIR / 'time_spent_distribution.png'}")

# --- Fig 5: Quality ratings comparison (grouped bar) ------------------
fig5, ax5 = plt.subplots(figsize=(10, 6))
pretty_labels = ["Creativity", "Clarity", "Completeness", "Feasibility"]
means = completers[QUALITY_COLS].mean()
stds = completers[QUALITY_COLS].std()
x5 = np.arange(len(QUALITY_COLS))
bars = ax5.bar(x5, means, 0.55, yerr=stds, capsize=4, color=TEAL_DARK,
               edgecolor="white", error_kw={"linewidth": 1.2})
ax5.set_xticks(x5)
ax5.set_xticklabels(pretty_labels, fontsize=13)
ax5.set_ylabel("Mean Rating")
ax5.set_title("Quality Ratings — All Completers (mean ± SD)")
ax5.set_ylim(0, 7.5)
ax5.spines[["top", "right"]].set_visible(False)
for bar, m in zip(bars, means):
    ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.35,
             f"{m:.2f}", ha="center", va="bottom", fontsize=11, color=TEAL_DARK)
fig5.tight_layout()
fig5.savefig(FIG_DIR / "quality_ratings_overall.png", dpi=300, bbox_inches="tight")
plt.close(fig5)
print(f"[OK] {FIG_DIR / 'quality_ratings_overall.png'}")

# --- Fig 6: Quality ratings by expertise (grouped bar) ----------------
if len(quality_by_exp) > 1:
    fig6, ax6 = plt.subplots(figsize=(11, 6))
    n_groups = len(QUALITY_COLS)
    n_levels = len(quality_by_exp)
    bar_w = 0.22
    x6 = np.arange(n_groups)

    for i, (level, row) in enumerate(quality_by_exp.iterrows()):
        offset = (i - n_levels / 2 + 0.5) * bar_w
        ax6.bar(x6 + offset, row.values, bar_w,
                label=level.capitalize(),
                color=EXPERTISE_COLORS.get(level, TEAL_MID))

    ax6.set_xticks(x6)
    ax6.set_xticklabels(pretty_labels, fontsize=13)
    ax6.set_ylabel("Mean Rating")
    ax6.set_title("Quality Ratings by Expertise Level")
    ax6.set_ylim(0, 7.5)
    ax6.legend(frameon=False)
    ax6.spines[["top", "right"]].set_visible(False)
    fig6.tight_layout()
    fig6.savefig(FIG_DIR / "quality_ratings_by_expertise.png", dpi=300, bbox_inches="tight")
    plt.close(fig6)
    print(f"[OK] {FIG_DIR / 'quality_ratings_by_expertise.png'}")

# --- Fig 7: Expertise score vs. pre-test score scatter ----------------
fig7, ax7 = plt.subplots(figsize=(8, 6))
for level in expertise_order:
    mask = df["expertise_level"] == level
    ax7.scatter(df.loc[mask, "expertise_score"], df.loc[mask, "pre_test_score"],
                label=level.capitalize(), color=EXPERTISE_COLORS[level],
                s=70, alpha=0.8, edgecolors="white", linewidth=0.5)
ax7.set_xlabel("Expertise Score")
ax7.set_ylabel("Pre-Test Score")
ax7.set_title("Expertise Score vs. Pre-Test Score")
ax7.legend(frameon=False)
ax7.spines[["top", "right"]].set_visible(False)
fig7.tight_layout()
fig7.savefig(FIG_DIR / "expertise_vs_pretest.png", dpi=300, bbox_inches="tight")
plt.close(fig7)
print(f"[OK] {FIG_DIR / 'expertise_vs_pretest.png'}")

# --- Fig 8: AI suggestions shown vs accepted (completers) -------------
ai_users = completers[completers["ai_suggestions_shown"] > 0].copy()
if len(ai_users) > 0:
    fig8, ax8 = plt.subplots(figsize=(9, 5))
    idx = np.arange(len(ai_users))
    w8 = 0.35
    ax8.bar(idx - w8 / 2, ai_users["ai_suggestions_shown"], w8,
            label="Shown", color=TEAL_LIGHT)
    ax8.bar(idx + w8 / 2, ai_users["ai_suggestions_accepted"], w8,
            label="Accepted", color=TEAL_DARK)
    ax8.set_xticks(idx)
    ax8.set_xticklabels([f"P{i+1}" for i in range(len(ai_users))], fontsize=11)
    ax8.set_xlabel("Participant")
    ax8.set_ylabel("Count")
    ax8.set_title("AI Suggestions: Shown vs. Accepted (Completers with AI)")
    ax8.legend(frameon=False)
    ax8.spines[["top", "right"]].set_visible(False)
    fig8.tight_layout()
    fig8.savefig(FIG_DIR / "ai_suggestions_shown_vs_accepted.png", dpi=300, bbox_inches="tight")
    plt.close(fig8)
    print(f"[OK] {FIG_DIR / 'ai_suggestions_shown_vs_accepted.png'}")

# --- Fig 9: Revision count vs word count (completers) -----------------
fig9, ax9 = plt.subplots(figsize=(8, 6))
for level in expertise_order:
    mask = completers["expertise_level"] == level
    if mask.any():
        ax9.scatter(completers.loc[mask, "revision_count"],
                    completers.loc[mask, "word_count"],
                    label=level.capitalize(),
                    color=EXPERTISE_COLORS[level],
                    s=80, alpha=0.8, edgecolors="white", linewidth=0.5)
ax9.set_xlabel("Revision Count")
ax9.set_ylabel("Word Count")
ax9.set_title("Revisions vs. Word Count (Completers)")
ax9.legend(frameon=False)
ax9.spines[["top", "right"]].set_visible(False)
fig9.tight_layout()
fig9.savefig(FIG_DIR / "revisions_vs_wordcount.png", dpi=300, bbox_inches="tight")
plt.close(fig9)
print(f"[OK] {FIG_DIR / 'revisions_vs_wordcount.png'}")

# --- Fig 10: Component presence (polished, matching notebook style) ----
plot_order = [
    "Data/features", "Aligned problem", "Analytic objective", "Method/model",
    "Explicit constraints", "Success criteria", "Stakeholder/action", "Ethics/privacy/fairness",
]

plot_df = component_summary.set_index("component").loc[plot_order].reset_index()
y = np.arange(len(plot_df))
height = 0.36

PC = "#0B6E75"   # participant level (primary)
DC = "#5FB0B7"   # draft level (transparency check)
LBL = "#3C8A92"  # readable label colour for lighter bars

total_participants = len(df)
total_completers = int(df["completed"].sum())
p_n = int(plot_df["participant_n"].iloc[0])
d_n = int(plot_df["draft_n"].iloc[0])

plt.rcParams.update({"font.size": 13})
fig10, ax10 = plt.subplots(figsize=(11, 7))
ax10.barh(y - height / 2, plot_df["participant_pct"], height, color=PC,
          label=f"Participant level (n={p_n} coded of {total_completers} completers)")
ax10.barh(y + height / 2, plot_df["draft_pct"], height, color=DC,
          label=f"Draft level (n={d_n} coded drafts)")
ax10.set_yticks(y)
ax10.set_yticklabels(plot_order)
ax10.invert_yaxis()
ax10.set_xlim(0, 100)
ax10.set_xlabel("Presence (%)")
ax10.legend(frameon=False, loc="lower right", fontsize=11)
ax10.spines[["top", "right"]].set_visible(False)

# Title with subset note
ax10.set_title(
    f"Component Presence in Problem Statements\n"
    f"(coded subset: {p_n} of {total_completers} completers, {total_participants} total participants)",
    fontsize=13, pad=12,
)

# Category separator lines and labels
ax10.axhline(0.5, color="0.75", linewidth=0.8)
ax10.axhline(5.5, color="0.75", linewidth=0.8)
ax10.text(101, 0, "Scenario-derived", va="center", color="0.45")
ax10.text(101, 3, "Prompt-named facets", va="center", color="0.45")
ax10.text(101, 6.5, "Extended indicators", va="center", color="0.45")

# Percentage labels on each bar
for i, (_, row) in enumerate(plot_df.iterrows()):
    ax10.text(row["participant_pct"] + 1.5, i - height / 2,
              f"{row['participant_pct']:.0f}%", va="center", color=PC, fontsize=11)
    ax10.text(row["draft_pct"] + 1.5, i + height / 2,
              f"{row['draft_pct']:.0f}%", va="center", color=LBL, fontsize=11)

fig10.tight_layout()
fig10.savefig(FIG_DIR / "component_presence_polished.png", dpi=300, bbox_inches="tight")
plt.close(fig10)
print(f"[OK] {FIG_DIR / 'component_presence_polished.png'}")

# ======================================================================
print(f"\nAll outputs written to: {OUT_DIR.resolve()}")

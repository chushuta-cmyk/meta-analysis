import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

DATA = Path("..")
OUT = Path("..") / "figures"

BLUE = "#1F6FB2"
RUST = "#C4622D"
INK = "#141414"
MUTED = "#5E5E5A"
TINT_BLUE = "#EDF3F9"
TINT_RUST = "#FBF2EC"
WHITE = "#FFFFFF"
RAIL = "#F4F4F1"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "text.color": INK,
    "figure.facecolor": "white",
    "mathtext.default": "regular",
    "mathtext.fontset": "dejavusans",
})

n = r"$\mathit{n}$"
k = r"$\mathit{k}$"

with open(DATA / "Figure1_prisma_flow.csv", encoding="utf-8") as fh:
    counts = {row["node"]: int(row["count"]) for row in csv.DictReader(fh)}

fig, ax = plt.subplots(figsize=(7.1, 8.6))
ax.set_xlim(0, 100)
ax.set_ylim(7, 100)
ax.axis("off")

MAIN_X, MAIN_W = 15.0, 51.0
SIDE_X, SIDE_W = 71.5, 27.0
CENTRE = MAIN_X + MAIN_W / 2


def box(x, top, w, h, lines, fill=WHITE, edge=MUTED, lw=0.8, weight="normal", size=7.6):
    ax.add_patch(FancyBboxPatch(
        (x, top - h), w, h,
        boxstyle="round,pad=0,rounding_size=0.8",
        fc=fill, ec=edge, lw=lw, zorder=2, mutation_aspect=0.55,
    ))
    ax.text(x + w / 2, top - h / 2, "\n".join(lines), ha="center", va="center",
            fontsize=size, fontweight=weight, linespacing=1.55, color=INK, zorder=3)


def down(y_from, y_to, x=CENTRE):
    ax.add_patch(FancyArrowPatch((x, y_from), (x, y_to), arrowstyle="-|>",
                                 mutation_scale=8, lw=0.8, color=MUTED,
                                 shrinkA=0, shrinkB=0, zorder=1))


def across(y, x_from=MAIN_X + MAIN_W, x_to=SIDE_X):
    ax.add_patch(FancyArrowPatch((x_from, y), (x_to, y), arrowstyle="-|>",
                                 mutation_scale=8, lw=0.8, color=MUTED,
                                 shrinkA=0, shrinkB=0, zorder=1))


def stage(top, bottom, label):
    ax.add_patch(Rectangle((2.0, bottom), 5.4, top - bottom, fc=RAIL, ec="none", zorder=0))
    ax.text(4.7, (top + bottom) / 2, label, ha="center", va="center", rotation=90,
            fontsize=7.4, fontweight="bold", color=MUTED)


stage(99.0, 79.0, "Identification")
stage(78.0, 51.5, "Screening")
stage(50.5, 9.0, "Included")

box(MAIN_X, 98.0, MAIN_W, 11.0, [
    f"Records identified from databases ({n} = {counts['records_identified']})",
    f"PubMed, {n} = {counts['pubmed']}; Scopus, {n} = {counts['scopus']};",
    f"Web of Science Core Collection, {n} = {counts['web_of_science']}",
], fill=TINT_BLUE, edge=BLUE, lw=1.0)
box(SIDE_X, 96.5, SIDE_W, 8.0, [
    "Duplicate records removed",
    f"before screening ({n} = {counts['duplicates_removed']})",
], fill=TINT_RUST, edge=RUST)
across(92.5)

down(87.0, 82.0)
box(MAIN_X, 82.0, MAIN_W, 8.0,
    [f"Records screened on title and abstract ({n} = {counts['records_screened']})"])
box(SIDE_X, 82.0, SIDE_W, 8.0,
    [f"Records excluded ({n} = {counts['records_excluded']})"], fill=TINT_RUST, edge=RUST)
across(78.0)

down(74.0, 69.0)
box(MAIN_X, 69.0, MAIN_W, 8.0,
    ["Reports assessed for eligibility", f"in full text ({n} = {counts['fulltext_assessed']})"])
box(SIDE_X, 69.0, SIDE_W, 10.5, [
    f"Reports excluded ({n} = {counts['fulltext_excluded']});",
    "did not meet full-text",
    "eligibility criteria",
], fill=TINT_RUST, edge=RUST)
across(65.0)

down(61.0, 55.0)
box(MAIN_X, 55.0, MAIN_W, 10.0, [
    "Publications included in systematic review",
    f"({n} = {counts['publications_included']}; {counts['independent_cohorts']} independent cohorts;",
    f"{n} = {counts['participants_reviewed']} participants)",
], fill=TINT_BLUE, edge=BLUE, lw=1.0)

down(45.0, 40.0)
box(MAIN_X, 40.0, MAIN_W, 8.5, [
    "Adversity-related contrasts extracted",
    f"and assessed at contrast level ({n} = {counts['contrasts_extracted']})",
])

with open(DATA / "Figure2B_attrition.csv", encoding="utf-8") as fh:
    attrition = list(csv.DictReader(fh))

short = {
    "Region-of-interest or small-volume corrected": "region-of-interest or small-\nvolume corrected",
    "Interaction only, no main effect": "interaction only",
    "Group already represented in model": "group already in model",
    "Loss-valence contrast": "loss valence",
}
reason_lines = []
for row in attrition:
    label = short[row["reason"]]
    for i, part in enumerate(label.split("\n")):
        tail = f", {n} = {row['contrasts']};" if i == len(label.split("\n")) - 1 else ""
        reason_lines.append(part + tail)
reason_lines[-1] = reason_lines[-1].rstrip(";")

box(SIDE_X, 42.5, SIDE_W, 14.5,
    ["Contrasts not eligible for",
     f"primary models ({n} = {counts['contrasts_excluded']}):"] + reason_lines,
    fill=TINT_RUST, edge=RUST, size=7.0)
across(35.25)

LEFT_C, RIGHT_C = 30.5, 78.0
ax.plot([CENTRE, CENTRE], [31.5, 25.0], color=MUTED, lw=0.8, zorder=1)
ax.plot([LEFT_C, RIGHT_C], [25.0, 25.0], color=MUTED, lw=0.8, zorder=1)
for x in (LEFT_C, RIGHT_C):
    ax.add_patch(FancyArrowPatch((x, 25.0), (x, 22.0), arrowstyle="-|>",
                                 mutation_scale=8, lw=0.8, color=MUTED,
                                 shrinkA=0, shrinkB=0, zorder=1))

box(9.5, 22.0, 42.0, 12.0, [
    "Model A: hypoactivation",
    f"{k} = {counts['modelA_experiments']} experiments; {counts['modelA_foci']} foci",
    f"{n} = {counts['modelA_participants']} participants",
], fill=TINT_BLUE, edge=BLUE, lw=1.2, weight="bold", size=7.8)
box(57.0, 22.0, 42.0, 12.0, [
    "Model B: hyperactivation",
    f"{k} = {counts['modelB_experiments']} experiments; {counts['modelB_foci']} foci",
    f"{n} = {counts['modelB_participants']} participants",
], fill=TINT_RUST, edge=RUST, lw=1.2, weight="bold", size=7.8)

fig.savefig(OUT / "Figure1_PRISMA.png", dpi=600, bbox_inches="tight", pad_inches=0.06)
fig.savefig(OUT / "Figure1_PRISMA.pdf", bbox_inches="tight", pad_inches=0.06)
plt.close(fig)

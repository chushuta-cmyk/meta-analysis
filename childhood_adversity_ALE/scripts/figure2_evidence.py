import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path("..")
OUT = Path("..") / "figures"

BLUE = "#1F6FB2"
RUST = "#C4622D"
GRAY = "#9A9A96"
INK = "#141414"
MUTED = "#5E5E5A"
RULE = "#C9C9C4"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.edgecolor": MUTED,
    "axes.linewidth": 0.8,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "mathtext.default": "regular",
    "mathtext.fontset": "dejavusans",
})


def read(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


power = read("Figure2A_statistical_power.csv")
attrition = read("Figure2B_attrition.csv")
contribution = read("Figure2C_contribution.csv")

model_colour = {"A": BLUE, "B": RUST}
k = r"$\mathit{k}$"

fig = plt.figure(figsize=(7.4, 6.5))
grid = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.15], hspace=0.62, wspace=0.62,
                        left=0.105, right=0.985, top=0.90, bottom=0.09)


def panel_letter(ax, letter, dx, dy=1.15):
    ax.text(dx, dy, letter, transform=ax.transAxes, ha="left", va="top",
            fontsize=11, fontweight="bold", color=INK)


def panel_title(ax, text):
    ax.set_title(text, fontsize=8.4, loc="left", pad=9, color=INK)


ax_power = fig.add_subplot(grid[0, 0])
labels = [f"Model {row['model']}\n{row['direction']}" for row in power]
experiments = [int(row["experiments"]) for row in power]
colours = [model_colour[row["model"]] for row in power]
benchmark = int(power[0]["recommended_minimum"])

bars = ax_power.bar(labels, experiments, color=colours, width=0.46, zorder=3)
ax_power.axhline(benchmark, color=INK, lw=1.3, ls=(0, (4.5, 2.5)), zorder=4)
ax_power.text(-0.44, benchmark + 0.7, f"Minimum for adequate power ({k} ≈ {benchmark})",
              ha="left", va="bottom", fontsize=7.3, color=INK)
for bar, row in zip(bars, power):
    ax_power.text(bar.get_x() + bar.get_width() / 2, int(row["experiments"]) + 0.6,
                  f"{k} = {row['experiments']}\n{row['percent_of_minimum']}% of minimum",
                  ha="center", va="bottom", fontsize=7.5, color=INK, linespacing=1.5)
ax_power.set_ylim(0, 26)
ax_power.set_yticks([0, 5, 10, 15, 20, 25])
ax_power.set_ylabel("Independent experiments, No.", fontsize=8)
ax_power.grid(axis="y", color=RULE, lw=0.6, zorder=0)
ax_power.set_axisbelow(True)
ax_power.tick_params(labelsize=7.8)
panel_title(ax_power, "Statistical power of each model")
panel_letter(ax_power, "A", -0.19)

ax_attrition = fig.add_subplot(grid[0, 1])
wrapped = {
    "Region-of-interest or small-volume corrected": "ROI or small-\nvolume corrected",
    "Interaction only, no main effect": "Interaction only",
    "Group already represented in model": "Group already\nin model",
    "Loss-valence contrast": "Loss valence",
}
attrition = sorted(attrition, key=lambda row: int(row["contrasts"]))
names = [wrapped[row["reason"]] for row in attrition]
values = [int(row["contrasts"]) for row in attrition]
shades = [BLUE if row["category"] == "reporting practice" else GRAY for row in attrition]

bars = ax_attrition.barh(names, values, color=shades, height=0.5, zorder=3)
for bar, value in zip(bars, values):
    ax_attrition.text(value + 0.13, bar.get_y() + bar.get_height() / 2, str(value),
                      va="center", fontsize=8, fontweight="bold", color=INK)
ax_attrition.set_xlim(0, 5)
ax_attrition.set_xticks(range(6))
ax_attrition.set_xlabel(f"Contrasts excluded, No. (of {sum(values)})", fontsize=8)
ax_attrition.grid(axis="x", color=RULE, lw=0.6, zorder=0)
ax_attrition.set_axisbelow(True)
ax_attrition.tick_params(axis="y", length=0, labelsize=7.6)
ax_attrition.tick_params(axis="x", labelsize=7.8)
panel_title(ax_attrition, "Why contrasts left the analysis")
panel_letter(ax_attrition, "B", -0.44)

ax_share = fig.add_subplot(grid[1, :])
model_a = [row for row in contribution if row["model"] == "A"][::-1]
model_b = [row for row in contribution if row["model"] == "B"][::-1]
positions = list(range(len(model_a))) + [len(model_a) + 1.5 + i for i in range(len(model_b))]
rows = model_a + model_b
shares = [float(row["share_percent"]) for row in rows]

ax_share.barh(positions, shares, color=[model_colour[row["model"]] for row in rows],
              height=0.58, zorder=3)
for y, share in zip(positions, shares):
    ax_share.text(share + 0.7, y, f"{share:.1f}", va="center", fontsize=7.4, color=INK)
ax_share.set_yticks(positions)
ax_share.set_yticklabels([row["source"].replace(" et al.,", " et al,") for row in rows], fontsize=7.6)
ax_share.set_ylim(-0.9, positions[-1] + 0.9)
ax_share.set_xlim(0, 52)
ax_share.set_xticks(range(0, 45, 5))
ax_share.set_xlabel("Share of foci entering the model, %", fontsize=8)
ax_share.grid(axis="x", color=RULE, lw=0.6, zorder=0)
ax_share.set_axisbelow(True)
ax_share.tick_params(axis="y", length=0)
ax_share.tick_params(axis="x", labelsize=7.8)
ax_share.axhline(len(model_a) + 0.75, color=RULE, lw=0.8)

top_two = sum(sorted(float(r["share_percent"]) for r in model_b)[-2:])
ax_share.text(51.5, (len(model_a) - 1) / 2, "Model A\nhypoactivation", ha="right", va="center",
              fontsize=7.8, fontweight="bold", color=BLUE, linespacing=1.5)
ax_share.text(51.5, positions[-2],
              f"Model B\nhyperactivation\n2 studies supply\n{top_two:.0f}% of foci",
              ha="right", va="center", fontsize=7.8, fontweight="bold", color=RUST, linespacing=1.5)
panel_title(ax_share, "Contribution of each experiment to its model")
panel_letter(ax_share, "C", -0.088, 1.12)

fig.savefig(OUT / "Figure2_EvidenceAdequacy.png", dpi=600, bbox_inches="tight", pad_inches=0.06)
fig.savefig(OUT / "Figure2_EvidenceAdequacy.pdf", bbox_inches="tight", pad_inches=0.06)
plt.close(fig)

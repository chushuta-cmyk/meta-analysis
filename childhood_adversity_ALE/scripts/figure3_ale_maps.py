from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from nilearn import plotting

DATA = Path("..") / "ale_maps"
OUT = Path("..") / "figures"

INK = "#141414"
MUTED = "#5E5E5A"
CUTS = (-12, -2, 8, 20, 32)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "text.color": INK,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})

PANELS = [
    ("A", "A_primary_stat.nii.gz", "Model A: hypoactivation (7 experiments, 30 foci)"),
    ("B", "B_primary_stat.nii.gz", "Model B: hyperactivation (3 experiments, 16 foci)"),
]

fig = plt.figure(figsize=(7.4, 4.4))

for i, (tag, fname, caption) in enumerate(PANELS):
    img = nib.load(DATA / fname)
    peak = float(np.nanmax(img.get_fdata()))
    ax = fig.add_axes([0.06, 0.55 - 0.47 * i, 0.90, 0.34])
    d = plotting.plot_stat_map(
        img,
        display_mode="z",
        cut_coords=CUTS,
        threshold=0.20 * peak,
        vmax=peak,
        cmap="hot",
        colorbar=True,
        black_bg=False,
        draw_cross=False,
        annotate=False,
        axes=ax,
        figure=fig,
    )
    d.annotate(left_right=False, positions=True, size=7)
    fig.text(0.02, 0.90 - 0.47 * i, tag, fontsize=11, fontweight="bold", color=INK)
    fig.text(0.06, 0.905 - 0.47 * i, caption, fontsize=8, color=MUTED)

fig.savefig(OUT / "Figure3_UnthresholdedALE.png", dpi=400, bbox_inches="tight")
fig.savefig(OUT / "Figure3_UnthresholdedALE.pdf", bbox_inches="tight")
plt.close(fig)

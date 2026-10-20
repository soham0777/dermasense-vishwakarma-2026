"""README banner for the Dermasense repository, made from our own CAD render (no stock or AI images)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]          # repository root; run: python docs/make_banner.py
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams["font.family"] = ["Segoe UI", "Segoe UI Symbol", "DejaVu Sans"]

W, H = 12.8, 4.0
fig = plt.figure(figsize=(W, H), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
grad = np.linspace(0, 1, 512)[None, :]
ax.imshow(grad, extent=[0, W, 0, H], cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    "g", ["#0B1220", "#0F2A3F", "#0B3B36"]), aspect="auto", zorder=0)
for k in range(9):                                   # faint grid, like a lab notebook
    ax.plot([0, W], [k * 0.5, k * 0.5], color="white", alpha=0.04, lw=0.8, zorder=1)
for k in range(26):
    ax.plot([k * 0.5, k * 0.5], [0, H], color="white", alpha=0.04, lw=0.8, zorder=1)

render = Image.open(ROOT / "1_presentation" / "figures" / "cad_exploded_iso.png").convert("RGBA")
arr = np.array(render).astype(float) / 255
white = (arr[..., :3].min(axis=2) > 0.97)
arr[white, 3] = 0                                    # drop the white background of the render
card = FancyBboxPatch((7.15, 0.35), 5.35, 3.3, boxstyle="round,pad=0,rounding_size=0.18", fc="white", ec="none",
                      alpha=0.06, zorder=2)
ax.add_patch(card)
ax.imshow(arr, extent=[7.25, 12.45, 0.45, 0.45 + 5.2 * render.height / render.width], zorder=3)
ax.text(12.42, 0.42, "our SolidWorks models · exploded view", color="#94A3B8", fontsize=8, ha="right", va="bottom",
        zorder=4)

ax.text(0.6, 3.25, "DERMASENSE", color="white", fontsize=40, fontweight="bold", va="center", zorder=4)
ax.text(0.62, 2.55, "Know when a covered wound dressing is full,\nwithout lifting it.", color="#CFFAFE", fontsize=17,
        va="center", linespacing=1.25, zorder=4)
ax.text(0.62, 1.72, "A laser-written two-zone strip + a clip-on reader that reads the\ndressing maker's own "
        "'change line' and says OK · CHANGE · CHECK.", color="#CBD5E1", fontsize=10.5, va="center", linespacing=1.3,
        zorder=4)
x = 0.62
for label, col in (("Vishwakarma Awards 2026–27", "#0369A1"), ("Health Tech · Remote Monitoring", "#047857"),
                   ("Stage 2 · design", "#B45309")):
    w = 0.066 * len(label) + 0.3
    ax.add_patch(FancyBboxPatch((x, 0.62), w, 0.42, boxstyle="round,pad=0,rounding_size=0.21", fc=col, ec="none",
                                zorder=4))
    ax.text(x + w / 2, 0.83, label, color="white", fontsize=9, ha="center", va="center", fontweight="bold", zorder=5)
    x += w + 0.12
fig.savefig(OUT / "banner.png", dpi=150, facecolor="#0B1220")
print("wrote", OUT / "banner.png")

"""
E2 Part B coupon: line resolution, gap isolation and laser-cut holes (DXF for LaserCAD, in mm).

Layout (x from the notch end, y across the film; default film width 20 mm):
  Row 1 (y 2..6)   5 dog-bones, drawn line width 0.3 / 0.5 / 0.8 / 1.0 / 1.5 mm, line length 16 mm, 4 x 4 mm pads
                   -> real line width (growth) and resistance vs width = smallest line we can trust
                   then 3 holes D2.00 on the CUT layer -> laser-cut hole size and fit on a 2 mm dowel
  Row 2 (y 8..18)  6 isolation pairs: two parallel 1.0 mm lines, 16 mm overlap, drawn gap 0.2 / 0.3 / 0.5 / 0.8 /
                   1.0 / 1.5 mm; each line has its own pad at the opposite end, so the probes never bridge the gap
                   -> smallest gap that stays insulating (strip v0.1 uses 1.0 mm electrode gaps, 0.95 mm minimum)
Layers: ENGRAVE (colour 3 green) = the reference LIG setting; CUT (colour 5 blue) = coupon outline, notch, holes.
Every engraved feature is ONE closed outline and nothing overlaps (overlaps can leave regions unfilled).
Usage: python make_e2_coupon.py [--width 20]   ->  e2_res_coupon.dxf, e2_res_coupon.png, e2_res_coupon_features.csv
"""
import argparse
import csv
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
WIDTHS = (0.3, 0.5, 0.8, 1.0, 1.5)          # drawn line widths, mm
GAPS = (0.2, 0.3, 0.5, 0.8, 1.0, 1.5)       # drawn isolation gaps, mm
LINE_L, PAD, ISO_W = 16.0, 4.0, 1.0          # line length, pad size, isolation line width (= strip F)
PITCH = 28.0                                 # feature pitch along x (24 mm feature + 4 mm space)
X0, HOLE_D, HOLE_PITCH = 10.0, 2.0, 6.0      # first feature x (room for the notch); test holes
ROW1_Y, ROW2_Y = 4.0, 13.0                   # row centre lines


def dog_bone(x0, yc, w):
    return unary_union([box(x0, yc - PAD / 2, x0 + PAD, yc + PAD / 2),
                        box(x0 + PAD, yc - w / 2, x0 + PAD + LINE_L, yc + w / 2),
                        box(x0 + PAD + LINE_L, yc - PAD / 2, x0 + 2 * PAD + LINE_L, yc + PAD / 2)])


def iso_pair(x0, yc, g):
    a = unary_union([box(x0, yc - g / 2 - PAD, x0 + PAD, yc - g / 2),                       # pad A (left, below)
                     box(x0 + PAD, yc - g / 2 - ISO_W, x0 + PAD + LINE_L, yc - g / 2)])     # line A
    b = unary_union([box(x0 + PAD, yc + g / 2, x0 + PAD + LINE_L, yc + g / 2 + ISO_W),      # line B
                     box(x0 + PAD + LINE_L, yc + g / 2, x0 + 2 * PAD + LINE_L, yc + g / 2 + PAD)])  # pad B (right, above)
    return a, b


def build(width):
    feats = []      # (feature id, kind, drawn value, polygon(s))
    for i, w in enumerate(WIDTHS):
        feats.append((f"W{int(round(w * 100)):03d}", "line", w, [dog_bone(X0 + i * PITCH, ROW1_Y, w)]))
    for i, g in enumerate(GAPS):
        feats.append((f"G{int(round(g * 100)):03d}", "gap", g, list(iso_pair(X0 + i * PITCH, ROW2_Y, g))))
    hx0 = X0 + len(WIDTHS) * PITCH
    holes = [(hx0 + i * HOLE_PITCH, ROW1_Y) for i in range(3)]
    length = max(X0 + len(GAPS) * PITCH - 4.0, holes[-1][0] + HOLE_D / 2) + 6.0
    top = ROW2_Y + max(GAPS) / 2 + PAD
    if top > width - 1.5:
        raise SystemExit(f"Film too narrow: need {top + 1.5:.1f} mm, got {width} mm")
    outline = box(0, 0, length, width)
    notch = Polygon([(2, width / 2 - 2), (6, width / 2), (2, width / 2 + 2)])
    return feats, holes, outline, notch


def save(feats, holes, outline, notch, width):
    doc = ezdxf.new("R2000", setup=False)
    doc.units = ezdxf.units.MM
    doc.layers.add("ENGRAVE", color=3)
    doc.layers.add("CUT", color=5)
    msp = doc.modelspace()
    for _, _, _, polys in feats:
        for p in polys:
            msp.add_lwpolyline(list(p.exterior.coords)[:-1], close=True, dxfattribs={"layer": "ENGRAVE", "color": 256})
    for x, y in holes:
        msp.add_circle((x, y), HOLE_D / 2, dxfattribs={"layer": "CUT", "color": 256})
    for p in (outline, notch):
        msp.add_lwpolyline(list(p.exterior.coords)[:-1], close=True, dxfattribs={"layer": "CUT", "color": 256})
    doc.saveas(HERE / "e2_res_coupon.dxf")

    with open(HERE / "e2_res_coupon_features.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["feature", "kind", "drawn_mm", "x_from_notch_end_mm", "line_length_mm", "note"])
        for fid, kind, val, polys in feats:
            note = "dog-bone: R pad to pad, width at 3 points" if kind == "line" else \
                "two 1.0 mm lines; measure R between pad A (lower left) and pad B (upper right)"
            wr.writerow([fid, kind, val, round(polys[0].bounds[0], 2), LINE_L, note])
        for i, (x, _) in enumerate(holes):
            wr.writerow([f"H{i + 1}", "hole", HOLE_D, round(x, 2), "", "CUT layer; measure 2 diameters; try a 2 mm dowel"])

    fig, ax = plt.subplots(figsize=(14, 2.6))
    ax.add_patch(plt.Polygon(list(outline.exterior.coords), fill=False, ec="tab:blue", lw=1))
    ax.add_patch(plt.Polygon(list(notch.exterior.coords), fill=False, ec="tab:blue", lw=1))
    for fid, kind, val, polys in feats:
        for p in polys:
            ax.add_patch(plt.Polygon(list(p.exterior.coords), fc="0.15", ec="none"))
        x = polys[0].bounds[0] + PAD + LINE_L / 2
        ax.text(x, (ROW1_Y if kind == "line" else ROW2_Y + 4.6 if val < 1.2 else ROW2_Y + 5.2) + (2.6 if kind == "line" else 0),
                f"{fid}\n{'w' if kind == 'line' else 'gap'} {val:.1f}" if val >= 1 else f"{fid}\n{'w' if kind == 'line' else 'gap'} {val:.2f}",
                ha="center", va="bottom", fontsize=6.5)
    for i, (x, y) in enumerate(holes):
        ax.add_patch(plt.Circle((x, y), HOLE_D / 2, fill=False, ec="tab:blue"))
        ax.text(x, y + 1.6, f"H{i + 1}", ha="center", fontsize=6.5)
    ax.set_xlim(-2, outline.bounds[2] + 2)
    ax.set_ylim(-2, width + 4)
    ax.set_aspect("equal")
    ax.set_title(f"E2 Part B coupon, {outline.bounds[2]:.0f} x {width:.0f} mm. Black = ENGRAVE (green layer, reference "
                 "setting). Blue = CUT. Notch = start end.", fontsize=8)
    ax.set_xlabel("mm")
    fig.tight_layout()
    fig.savefig(HERE / "e2_res_coupon.png", dpi=160)
    print(f"Saved e2_res_coupon.dxf/.png/_features.csv: {outline.bounds[2]:.0f} x {width:.0f} mm, "
          f"{len(WIDTHS)} line widths, {len(GAPS)} gaps, {len(holes)} holes")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--width", type=float, default=20.0, help="film width in mm (default 20)")
    a = ap.parse_args()
    save(*build(a.width), a.width)

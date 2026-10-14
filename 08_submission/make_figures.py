"""
Figures for the Stage 2 deck, generated from project files (no stock or AI images).
Output: 08_submission/figures/*.png, sized to the template's picture frames:
  wide  = 5.92 x 2.64 in (example-slide figure frames)
  tall  = 5.85 x 4.35 in (guideline-slide picture frames)
Run: python make_figures.py
"""
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
import schemdraw
import schemdraw.elements as elm

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)
COUPON = HERE.parent / "04_lig_lab" / "lig_test_coupon.dxf"
WIDE = (11.84, 5.28)      # 2x the 5.92 x 2.64 in frame
TALL = (11.70, 8.70)      # 2x the 5.85 x 4.35 in frame
NAVY, GREEN, GREY, AMBER = "#1e3a8a", "#15803d", "#475569", "#b45309"


def box(ax, x, y, w, h, text, fc="#eef2ff", ec=NAVY, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, wrap=True, color="#0f172a")


def arrow(ax, x0, y, x1):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))


def flow(ax, y, items, fc, ec, x0=0.25, w=2.6, gap=0.42, h=1.55, fs=10.5):
    x = x0
    for i, t in enumerate(items):
        box(ax, x, y, w, h, t, fc=fc, ec=ec, fs=fs)
        if i < len(items) - 1:
            arrow(ax, x + w + 0.03, y + h / 2, x + w + gap - 0.03)
        x += w + gap


def fig_before_after():
    fig = plt.figure(figsize=WIDE)
    ax = fig.add_axes([0.005, 0.01, 0.99, 0.98])
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 5.6); ax.axis("off")
    ax.text(0.25, 5.25, "BEFORE: today  [C, literature]", fontsize=13, weight="bold", color=NAVY)
    flow(ax, 3.35, ["Exudate soaks into\nthe dressing pad",
                    "Spread is hidden under\nbandage / secondary\ndressing",
                    "Change on a schedule,\nor after a visual check\nor leakage",
                    "Too early: 44.9 % of\nchanges at optimal\nmoisture (Milne 2016)\nToo late: leakage"],
         fc="#fef2f2", ec="#b91c1c")
    ax.text(0.25, 2.6, "AFTER: planned, NOT yet built or tested  [B]", fontsize=13, weight="bold", color=GREEN)
    flow(ax, 0.7, ["Thin LIG strip on the\nouter face of the pad\n(no wound contact)",
                   "Zones read wet/dry at\npad centre and at the\nmaker's 2 cm change line",
                   "Reader shows when\nthe front reaches\nthe change line",
                   "Change when the pad\nis actually full\n(bench validation first)"],
         fc="#f0fdf4", ec=GREEN)
    fig.savefig(OUT / "f1_before_after.png", dpi=200, bbox_inches=None)
    plt.close(fig)


def fig_system():
    fig = plt.figure(figsize=WIDE)
    ax = fig.add_axes([0.005, 0.01, 0.99, 0.98])
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 5.6); ax.axis("off")
    ax.text(0.25, 5.25, "STAGE 2: measure the material first  [B, planned E1]", fontsize=13,
            weight="bold", color=NAVY)
    flow(ax, 3.3, ["Polyimide film\n(grade & thickness\nto be measured)",
                   "100 W CO₂ laser\nLaserCAD V8.28\nsetting '12' ± 2",
                   "Test coupon\n6 cells × 3 strips\n(8/16/24 mm)",
                   "Multimeter + microscope\n→ CSV → Rs, CV\n(analyze_e1.py)"],
         fc="#eef2ff", ec=NAVY, fs=10.5)
    ax.text(0.25, 2.6, "STAGE 3: strip readout, planned after E1 passes  [B]", fontsize=13,
            weight="bold", color=GREEN)
    flow(ax, 0.65, ["LIG strip zones\n(centre / change line\n/ edge)",
                    "ESP32-C3: bipolar\nGPIO drive, idle hi-Z",
                    "ADS1115 16-bit ADC\n+ TMP117 temp. ref.",
                    "USB / BLE log\n→ plot on PC/phone"],
         fc="#f0fdf4", ec=GREEN, fs=10.5)
    fig.savefig(OUT / "f2_system.png", dpi=200)
    plt.close(fig)


def coupon_polys():
    doc = ezdxf.readfile(COUPON)
    colours = {1: "#dc2626", 2: "#eab308", 3: "#16a34a", 4: "#06b6d4", 5: "#2563eb", 6: "#c026d3", 7: "k"}
    polys = []
    for e in doc.modelspace().query("LWPOLYLINE"):
        aci = doc.layers.get(e.dxf.layer).color
        polys.append(([(p[0], p[1]) for p in e.get_points()], colours.get(aci, "k"), aci))
    return polys


def dim(ax, x0, y0, x1, y1, text, off=0.0, fs=9, color=NAVY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="<->", color=color, lw=1))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 + off, text, ha="center", va="center", fontsize=fs, color=color,
            bbox=dict(fc="white", ec="none", pad=0.5))


def fig_coupon(size, name, detail):
    fig = plt.figure(figsize=size)
    polys = coupon_polys()
    if detail:
        ax_full = fig.add_axes([0.04, 0.70, 0.92, 0.22])
        ax_det = fig.add_axes([0.06, 0.08, 0.88, 0.52])
    else:
        ax_full = fig.add_axes([0.03, 0.36, 0.94, 0.56])
        ax_det = None
    for pts, c, aci in polys:
        ax_full.add_patch(Polygon(pts, closed=True, fc="none" if aci == 7 else c, ec=c, lw=0.8))
    ax_full.set_xlim(-3, 241); ax_full.set_ylim(-4, 24); ax_full.set_aspect("equal"); ax_full.axis("off")
    dim(ax_full, 0, -2.5, 237, -2.5, "237 mm", fs=9)
    dim(ax_full, -2, 0, -2, 20, "20", fs=8)
    ax_full.set_title("Test coupon lig_test_coupon.dxf (generated by make_test_pattern.py): one colour = "
                      "one power/speed setting", fontsize=10, color=NAVY)
    if not detail:
        fig.text(0.03, 0.14, "Each cell: 3 strips, 2.00 mm wide; strip lengths 8 / 16 / 24 mm; 4 × 4 mm pads. "
                 "Every strip is one closed outline (no overlaps).\nR = Rs·L/W + R0  →  slope gives sheet "
                 "resistance Rs, intercept gives contact resistance R0, using a plain multimeter.",
                 fontsize=9.5, color="#0f172a")
    else:
        for pts, c, aci in polys:
            xs = [p[0] for p in pts]
            if aci == 3:
                ax_det.add_patch(Polygon(pts, closed=True, fc="#16a34a", ec="#14532d", lw=1))
        ax_det.set_xlim(82, 128); ax_det.set_ylim(-1, 21); ax_det.set_aspect("equal"); ax_det.axis("off")
        x0 = 86.0
        dim(ax_det, x0 + 4, 3.0 - 1.6, x0 + 12, 3.0 - 1.6, "8 mm", fs=9)
        dim(ax_det, x0 + 4, 9.0 - 1.6, x0 + 20, 9.0 - 1.6, "16 mm", fs=9)
        dim(ax_det, x0 + 4, 15.0 + 3.0, x0 + 28, 15.0 + 3.0, "24 mm", fs=9)
        dim(ax_det, x0 + 31.5, 14.0, x0 + 31.5, 16.0, "2.0", fs=8)
        dim(ax_det, x0 - 1.2, 13.0, x0 - 1.2, 17.0, "4", fs=8)
        ax_det.text(105, -0.6, "One cell (GREEN = reference setting), dimensions in mm", ha="center",
                    fontsize=10, color=NAVY)
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def schematic_png(path, which):
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.4, fontsize=12)
        if which == "tlm":
            d += elm.Dot().label("pad A", "left")
            d += elm.Resistor().right().label("LIG strip\nR(L) = Rs·L/W + R0", "top")
            d += elm.Dot().label("pad B", "right")
            d += elm.Line().down(1.4)
            d += elm.MeterOhm().left().label("Multimeter (Ω)\n3 readings per strip", "bottom")
            d += elm.Line().up(1.4)
        else:
            d += elm.Dot().label("GPIO_Z\n(ESP32-C3)", "left")
            d += elm.Resistor().right().label("Rp 1 k", "top")
            d += elm.ResistorVar().right().label("LIG zone\n(fluid) Rz", "top")
            d += elm.Resistor().right().label("Rp 1 k", "top")
            n = d.add(elm.Dot().label("N", "top"))
            d += elm.Resistor().right().label("Rref 100 k\n0.1 %", "top")
            d += elm.Dot().label("GPIO_COM", "right")
            d += elm.Line().at(n.center).down(1.6)
            d += elm.Dot(open=True).label("ADS1115 A0", "bottom")
        d.save(str(path), dpi=220)


def fig_schematic(size, name):
    a, b = OUT / "_sch_tlm.png", OUT / "_sch_readout.png"
    schematic_png(a, "tlm")
    schematic_png(b, "readout")
    fig = plt.figure(figsize=size)
    tall = size[1] / size[0] > 0.6
    if tall:
        ax1 = fig.add_axes([0.20, 0.55, 0.6, 0.36]); ax2 = fig.add_axes([0.02, 0.12, 0.96, 0.36])
        panels = ((ax1, a, "(a) E1 measurement, now: 2-wire resistance of each strip"),
                  (ax2, b, "(b) Planned zone readout (bench only, not built): bipolar ratiometric"))
    else:
        ax2 = fig.add_axes([0.02, 0.17, 0.96, 0.70])
        panels = ((ax2, b, "Planned zone readout (bench only, NOT built yet): bipolar ratiometric measurement"),)
    for ax, img, title in panels:
        ax.imshow(plt.imread(img)); ax.axis("off"); ax.set_title(title, fontsize=10.5, color=NAVY)
    note = ("Rz from both drive polarities: phase +  Rz = Rref(Vdd/VN − 1) − 2Rp;  phase −  "
            "Rz = Rref·VN/(Vdd − VN) − 2Rp.\nPins idle in high-impedance between scans (no net DC). "
            "Schematic drawn with schemdraw; KiCad capture pending (KiCad not installed).")
    fig.text(0.02, 0.02, note, fontsize=8.6, color=GREY)
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)
    a.unlink(); b.unlink()


def fig_placeholder():
    fig, ax = plt.subplots(figsize=WIDE)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0.01, 0.02), 0.98, 0.96, fc="#f1f5f9", ec=AMBER, lw=3, ls="--"))
    ax.text(0.5, 0.62, "INSERT ORIGINAL PHOTO", ha="center", fontsize=26, weight="bold", color=AMBER)
    ax.text(0.5, 0.38, "Experiment E1 at our 100 W laser: team members with institutional ID badges,\n"
            "coupon on the bed / under the microscope. Unedited phone original.\n"
            "(Placeholder: no photo exists yet; replace before submission)",
            ha="center", fontsize=12, color="#334155")
    fig.savefig(OUT / "f5_photo_placeholder.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_before_after()
    fig_system()
    fig_coupon(WIDE, "f3_coupon_wide.png", detail=False)
    fig_coupon(TALL, "f3_coupon_tall.png", detail=True)
    fig_schematic(WIDE, "f4_schematic_wide.png")
    fig_schematic(TALL, "f4_schematic_tall.png")
    fig_placeholder()
    print("figures:", ", ".join(sorted(p.name for p in OUT.glob("*.png"))))

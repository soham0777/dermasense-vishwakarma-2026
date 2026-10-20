"""
Presentation figures for the final Stage 2 deck. Every figure is drawn from project files (no stock or AI images):
geometry from 4_sensor_strip/strip_v0_1_geometry.json and the DXFs, numbers from calc_readout.py / calc_mechanical.py,
FMEA from 3_decisions/fmea_v0_1.csv, concept scores from 3_decisions/decision_matrix.md, KiCad schematic from its PDF,
CAD renders from render_cad.py, measurement path from the reader_v0_1 netlist, tool output as printed by the
re-runs of 19 Oct 2026 (fig_maker). Illustrations that are concepts are labelled as such inside the image.
Photo placeholders are plain marked boxes: the team's real photos replace them (build_deck.py, team_photos/).
Usage: python make_figures.py      (run render_cad.py first for the CAD images)
"""
import csv
import json
import textwrap
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from PIL import Image

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
ROOT = HERE.parent
G = json.loads((ROOT / "4_sensor_strip" / "strip_v0_1_geometry.json").read_text())
DPI = 220

NAVY, BLUE, GREEN, SLATE, MUTED = "#0F172A", "#0369A1", "#059669", "#334155", "#64748B"
AMBER, RED, MINT, LIGHT, LINE = "#D97706", "#DC2626", "#ECFDF5", "#F1F5F9", "#CBD5E1"
KAPTON, LIG, FOAM, PAD = "#E9A23B", "#1F2937", "#FFF7E6", "#FBE7C6"
plt.rcParams.update({"font.family": ["Segoe UI", "Segoe UI Symbol", "DejaVu Sans"], "font.size": 10, "axes.edgecolor": LINE, "axes.labelcolor": SLATE,
                     "xtick.color": SLATE, "ytick.color": SLATE, "svg.fonttype": "none"})


def save(fig, name):
    fig.savefig(FIG / name, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("wrote", name)


def box(ax, x, y, w, h, text, fc="white", ec=LINE, tc=NAVY, size=9.5, bold=False, ls="-", r=0.06, lw=1.2, wrap=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls))
    if wrap:
        text = "\n".join(textwrap.fill(t, wrap) for t in text.split("\n"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=tc, fontsize=size,
            fontweight="bold" if bold else "normal", linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.6, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=12, color=color, lw=lw, ls=ls,
                                 shrinkA=0, shrinkB=0))


def tag(ax, x, y, text, color, size=7.5):
    ax.text(x, y, text, ha="left", va="center", fontsize=size, color=color, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.3", fc="white", ec=color, lw=0.9))


def canvas(w, h, xlim=(0, 10), ylim=None):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*(ylim or (0, 10 * h / w)))
    ax.axis("off")
    return fig, ax


# ------------------------------------------------------------------ 1 problem: when is a dressing full?
def fig_problem():
    fig, ax = canvas(5.94, 3.95, (0, 170), (0, 113))
    # dressing to scale (mm): 12.5 mm border around a 75 mm pad
    cx, cy, half = 64, 58, 37.5
    ax.add_patch(Rectangle((cx - half - 12.5, cy - half - 12.5), 100, 100, fc="#F8FAFC", ec="#94A3B8", lw=1))
    ax.add_patch(Rectangle((cx - half, cy - half), 75, 75, fc=PAD, ec="#D6B98C", lw=1))
    for r, a in ((26, 0.18), (17, 0.28), (9, 0.45)):
        ax.add_patch(Circle((cx, cy), r, fc="#60A5FA", alpha=a, ec="none"))
    ax.add_patch(Rectangle((cx - 17.5, cy - 17.5), 35, 35, fc="none", ec=RED, lw=1.6, ls=(0, (4, 2))))
    ax.text(cx, cy + 20, "maker's change line ≈ 2 cm inside the pad edge²", ha="center", fontsize=7.4, color=RED)
    ax.annotate("exudate front\nspreads outward", (cx + 13, cy - 20), (cx + 30, cy - 33), fontsize=7, color=BLUE,
                ha="center", arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    x0 = cx - half - 12.5 - 10
    ax.add_patch(Rectangle((x0, cy - 5), cx + 6 - x0, 10, fc=KAPTON, ec="#B45309", lw=0.8, alpha=0.95))
    for zx, lab in ((cx - 17.5, "A"), (cx, "C")):
        ax.add_patch(Rectangle((zx - 3, cy - 2), 6, 4, fc=LIG, ec="none"))
        ax.text(zx, cy + 7.5, f"zone {lab}", ha="center", fontsize=7.4, color=NAVY, fontweight="bold")
    ax.text(x0 + 1, cy - 8, "strip on the\npad's outer face", fontsize=6.6, color="#92400E", va="top")
    ax.text(cx, 1.5, "Top view, to scale from our dressing/strip geometry (75 mm pad). Exudate shapes illustrative.",
            ha="center", fontsize=6.2, color=MUTED)
    for i, (lab, r, col, note) in enumerate((("Too early", 9, MUTED, "front far from\nthe line"),
                                             ("On time", 17.5, GREEN, "front reaches\nthe line: change"),
                                             ("Too late", 30, RED, "past the line:\nleak risk"))):
        y0 = 80 - i * 33
        s_ = 20
        ax.add_patch(Rectangle((122, y0), s_, s_, fc=PAD, ec="#D6B98C", lw=0.8))
        ax.add_patch(Circle((122 + s_ / 2, y0 + s_ / 2), min(r, 37.5) * s_ / 75, fc="#60A5FA", alpha=0.55, ec="none"))
        k = 17.5 * s_ / 75
        ax.add_patch(Rectangle((122 + s_ / 2 - k, y0 + s_ / 2 - k), 2 * k, 2 * k, fc="none", ec=RED, lw=0.9, ls=(0, (3, 1.5))))
        ax.text(145, y0 + 15, lab, fontsize=8, color=col, fontweight="bold")
        ax.text(145, y0 + 9.5, note, fontsize=6.5, color=SLATE, va="top")
    save(fig, "fig_problem.png")


# ------------------------------------------------------------------ 2/3 user journeys (decluttered 16 Oct)
def journey(name, title, steps, stat, stat_color, banner, color):
    fig, ax = canvas(5.94, 3.95, (0, 100), (0, 66.5))
    ax.text(2, 63, title, fontsize=11, color=NAVY, fontweight="bold", va="top")
    n = len(steps)
    gap = 4.0
    w = (96 - (n - 1) * gap) / n
    for i, (head, body, kind) in enumerate(steps):
        x = 2 + i * (w + gap)
        ec = {"pain": RED, "ok": GREEN, "neutral": BLUE, "warn": AMBER}[kind]
        fc = {"pain": "#FEF2F2", "ok": MINT, "neutral": "#EFF6FF", "warn": "#FFFBEB"}[kind]
        ax.add_patch(FancyBboxPatch((x, 25), w, 28, boxstyle="round,pad=0,rounding_size=1.8", fc=fc, ec=ec, lw=1.5))
        ax.add_patch(Circle((x + w / 2, 47.5), 3.1, fc=ec, ec="none"))
        ax.text(x + w / 2, 47.5, str(i + 1), ha="center", va="center", fontsize=9.5, color="white", fontweight="bold")
        ax.text(x + w / 2, 40.5, head, ha="center", va="top", fontsize=10, color=NAVY, fontweight="bold", linespacing=1.1)
        ax.text(x + w / 2, 33.0, body, ha="center", va="top", fontsize=8.6, color=SLATE, linespacing=1.15)
        if i < n - 1:
            arrow(ax, x + w + 0.4, 39, x + w + gap - 0.4, 39, color=MUTED, lw=1.4)
    ax.text(50, 15.5, stat, ha="center", va="center", fontsize=11.5, color=stat_color, fontweight="bold")
    ax.add_patch(FancyBboxPatch((2, 1.5), 96, 5.2, boxstyle="round,pad=0,rounding_size=1", fc=color, ec="none", alpha=0.12))
    ax.text(50, 4.1, banner, ha="center", va="center", fontsize=8.4, color=color, fontweight="bold")
    save(fig, name)


def fig_journeys():
    journey("fig_journey_before.png", "Today: checked by schedule or by looking",
            [("Dressing on", "under bandage\nor sock", "neutral"),
             ("Exudate\nspreads", "unseen under\nthe cover", "pain"),
             ("Guess", "clock, peek\nor leak", "pain"),
             ("Too early\nor too late", "waste, or\nwet skin", "pain")],
            "44.9 % of changes came while moisture was still optimal¹", RED,
            "Cited numbers only (References slide)", RED)
    journey("fig_journey_after.png", "Intended: the strip reads the change line",
            [("Strip on\nthe pad", "outer face,\nnot the wound", "neutral"),
             ("Reader\nclips on", "4 pins,\n2 dowels", "neutral"),
             ("Zones\nread", "centre C,\nchange line A", "ok"),
             ("Clear\nstate", "OK · CHANGE\nor CHECK, on\nLEDs + phone", "warn")],
            "Target: alert within ±10 % of the visible front (bench test E4)", GREEN,
            "INTENDED WORKFLOW · NOT CLINICALLY VALIDATED", AMBER)


# ------------------------------------------------------------------ 5 firmware data flow (decluttered)
def fig_dataflow():
    fig, ax = canvas(5.94, 4.25, (0, 100), (0, 71.5))
    ax.text(1, 70, "One scan, every 2 s  →  LEDs · USB log · BLE broadcast", fontsize=10.5, color=NAVY, fontweight="bold", va="top")
    stages = [("CHECK", "known 100 kΩ"), ("ZONE C", "pad centre"), ("ZONE A", "change line"), ("LOOP", "strip intact?")]
    for i, (s, sub) in enumerate(stages):
        x = 1 + i * 24.8
        box(ax, x, 51, 22.5, 11, f"{s}\n{sub}", fc="#EFF6FF", ec=BLUE, tc=NAVY, size=8.8, r=1.4)
        ax.plot([x + 3, x + 3, x + 11.25, x + 11.25, x + 19.5, x + 19.5], [43.5, 47.5, 47.5, 39.5, 39.5, 43.5],
                color=GREEN, lw=1.6)
        ax.plot([x + 2, x + 20.5], [43.5, 43.5], color=LINE, lw=0.8)
        if i < 3:
            arrow(ax, x + 22.8, 56.5, x + 24.6, 56.5, color=MUTED, lw=1.2)
    ax.text(50, 34.5, "each path driven + then −  →  no net DC on wet electrodes", ha="center", fontsize=8.8, color=GREEN,
            fontweight="bold")
    box(ax, 1, 3, 33, 25, "Each zone\n\nwet  < 100 kΩ\ndry  > 300 kΩ\n3 scans in a row", fc=MINT, ec=GREEN, size=9.2, r=1.6)
    arrow(ax, 34.6, 15.5, 39.4, 15.5, color=MUTED, lw=1.4)
    states = [("OK", "line dry", GREEN), ("CHANGE", "line wet", AMBER), ("CHECK", "line before centre", RED),
              ("FAULT", "strip or reader error", NAVY)]
    for i, (s, why, col) in enumerate(states):
        y = 22.5 - i * 6.6
        ax.add_patch(FancyBboxPatch((40, y), 17, 5.4, boxstyle="round,pad=0,rounding_size=1", fc=col, ec="none"))
        ax.text(48.5, y + 2.7, s, ha="center", va="center", fontsize=8.8, color="white", fontweight="bold")
        ax.text(59, y + 2.7, why, va="center", fontsize=8.6, color=SLATE)
    save(fig, "fig_dataflow.png")


# ------------------------------------------------------------------ 5 HOW IT WORKS (refinement 19 Oct): mechanism + signal path
def fig_howitworks():
    """Plain-English mechanism. Layer order from 3_decisions/sensor_selection.md; values from calc_readout_report.md;
    part names from the KiCad netlist. Concept drawing: thicknesses not to scale."""
    fig, ax = canvas(5.94, 4.25, (0, 100), (0, 71.5))
    ax.text(1, 70.6, "How it senses: wet pad → closed gap → lower resistance → state", fontsize=10.2, color=NAVY,
            fontweight="bold", va="top")
    # ---- 1. layers (side view)
    ax.text(1, 65.4, "① Side view of a dressing with the strip (not to scale)", fontsize=8, color=BLUE, fontweight="bold",
            va="top")
    X0, X1 = 34, 99
    layers = [  # y, h, colour, label (layer order: 3_decisions/sensor_selection.md)
        (57.4, 1.4, "#CBD5E1", "cover film"),
        (55.2, 2.2, KAPTON, "strip (polyimide; carbon faces down)"),
        (53.7, 1.5, "#F2A24A", "seal tape with 2 windows"),
        (46.0, 7.7, PAD, "absorbent pad"),
        (44.6, 1.4, "#E2E8F0", "wound-contact layer"),
        (42.0, 2.6, "#FBCFE8", "wound (never touched)")]
    for y, h, c, lab in layers:
        ax.add_patch(Rectangle((X0, y), X1 - X0, h, fc=c, ec="#94A3B8", lw=0.5))
        ax.plot([X0 - 1.2, X0], [y + h / 2, y + h / 2], color="#94A3B8", lw=0.6)
        ax.text(X0 - 1.6, y + h / 2, lab, fontsize=6.6, color=SLATE, ha="right", va="center")
    xc, xa = 54, 86                                         # window C over the pad centre, A on the change line
    for xw, name, where, col in ((xc, "C", "pad centre", NAVY), (xa, "A", "change line", RED)):
        ax.add_patch(Rectangle((xw - 3, 53.7), 6, 1.5, fc="white", ec="none"))
        ax.add_patch(Rectangle((xw - 3, 54.5), 6, 0.7, fc=LIG, ec="none"))
        ax.text(xw, 60.2, f"zone {name} ({where})", fontsize=7.2, color=col, fontweight="bold", ha="center")
        ax.plot([xw, xw], [59.8, 58.8], color=NAVY, lw=0.7)
    ax.add_patch(Polygon([(xc - 6, 44.6), (xc + 6, 44.6), (xc + 22, 53.6), (xc - 18, 53.6)], closed=True,
                         fc="#60A5FA", alpha=0.45, ec="none"))
    ax.annotate("", (xa - 2, 51.6), (xc + 12, 49.6), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.1))
    ax.text(xc + 13, 47.2, "exudate spreads outward", fontsize=6.8, color=BLUE)
    # ---- 2. one window, dry vs wet
    ax.text(1, 38.4, "② Inside one window (seen from below)", fontsize=8, color=BLUE, fontweight="bold", va="top")
    for k, (x0, wet) in enumerate(((3, False), (52, True))):
        ax.add_patch(FancyBboxPatch((x0, 22.5), 45, 13, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc="#EFF6FF" if wet else "#F8FAFC", ec=BLUE if wet else LINE, lw=1.1))
        ax.add_patch(Rectangle((x0 + 4, 29), 14, 3.2, fc=LIG, ec="none"))
        ax.add_patch(Rectangle((x0 + 22, 29), 14, 3.2, fc=LIG, ec="none"))
        ax.text(x0 + 11, 33.4, "sense", fontsize=6.6, color=SLATE, ha="center")
        ax.text(x0 + 29, 33.4, "common", fontsize=6.6, color=SLATE, ha="center")
        ax.annotate("", (x0 + 18.2, 27.6), (x0 + 21.8, 27.6), arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.7))
        ax.text(x0 + 20, 25.6, "1.0 mm gap", fontsize=6.4, color=MUTED, ha="center")
        if wet:
            ax.add_patch(FancyBboxPatch((x0 + 10, 28.2), 20, 4.8, boxstyle="round,pad=0,rounding_size=2.2",
                                        fc="#60A5FA", alpha=0.55, ec="none"))
        ax.text(x0 + 41, 31, "WET" if wet else "DRY", fontsize=8.2, color=BLUE if wet else MUTED, fontweight="bold",
                ha="center", va="center")
        ax.text(x0 + 22.5, 23.7, "fluid bridges the gap → ≈ 4–15 kΩ" if wet else "gap open → above 1 MΩ",
                fontsize=7.2, color=BLUE if wet else SLATE, ha="center", fontweight="bold")
    arrow(ax, 48.6, 29, 51.4, 29, color=BLUE, lw=1.4)
    # ---- 3. the reader chain (real part names)
    ax.text(1, 19.6, "③ The reader turns resistance into a state (part names from our KiCad schematic)", fontsize=8,
            color=BLUE, fontweight="bold", va="top")
    chain = [("Strip\nzones C, A", "#FFF7E6", "#D6B98C"), ("4 pogo pins\n(clamp)", "#EFF6FF", BLUE),
             ("1 kΩ + 100 kΩ\ndivider", "#EFF6FF", BLUE), ("ADS1115\n16-bit ADC", "#EFF6FF", BLUE),
             ("ESP32-C3\nrules", "#EFF6FF", BLUE), ("OK · CHANGE\nCHECK · FAULT", MINT, GREEN)]
    w, gap = 14.4, 2.2
    for i, (t, fc, ec) in enumerate(chain):
        x = 1 + i * (w + gap)
        box(ax, x, 6.2, w, 10, t, fc=fc, ec=ec, size=7.2, bold=i in (0, 5), r=1.2)
        if i < len(chain) - 1:
            arrow(ax, x + w + 0.2, 11.2, x + w + gap - 0.2, 11.2, color=MUTED, lw=1.1)
    ax.text(50, 3.4, "Output: LEDs · CSV over USB · Bluetooth broadcast (compiled; hardware test pending)", fontsize=7,
            color=SLATE, ha="center")
    ax.text(50, 0.6, "Values calculated (calc_readout.py), to be measured in E2 / E4. Concept drawing, layers not to scale.",
            fontsize=6.2, color=MUTED, ha="center")
    save(fig, "fig_howitworks.png")


# ------------------------------------------------------------------ 6 CAD (refinement 19 Oct): annotated exploded render
CAD_PARTS = [  # number, x, y on cad_exploded_iso.png (927 x 586 px), part, material / role
    (1, 118, 74, "Clamp lid", "PETG print (shown clear)"),
    (2, 330, 128, "Sensor strip", "polyimide 0.125 mm + carbon tracks"),
    (3, 228, 182, "Seal tape", "polyimide tape, 2 windows"),
    (4, 176, 232, "Pogo pins ×4", "P75-B1, 2 mm travel"),
    (5, 148, 300, "Dowels ×2", "Ø2 mm stainless"),
    (6, 128, 345, "Clamp base", "PETG print"),
    (7, 470, 235, "Reference dressing", "bordered foam, 75 mm pad"),
    (8, 420, 415, "Wound-bed spacer", "acrylic 6 mm"),
    (9, 330, 520, "Rig base", "acrylic 5 mm, rubber feet")]


def fig_cad():
    ex = Image.open(FIG / "cad_exploded_iso.png")
    iso = Image.open(FIG / "cad_assembly_iso.png")
    clo = Image.open(FIG / "cad_clamp_closeup.png")
    fig = plt.figure(figsize=(5.94, 4.25))
    a = fig.add_axes([0.0, 0.27, 0.64, 0.70], anchor="N")
    a.imshow(ex)
    a.axis("off")
    for n, x, y, _, _ in CAD_PARTS:
        a.add_patch(Circle((x, y), 15, fc=NAVY, ec="white", lw=1.2, zorder=5))
        a.text(x, y, str(n), color="white", fontsize=7.4, ha="center", va="center", fontweight="bold", zorder=6)
    a.set_title("Exploded view: our SolidWorks 2019 models (numbers = parts below)", fontsize=6.8, color=MUTED, pad=1.5)
    for im, rect, cap in ((iso, [0.655, 0.68, 0.345, 0.27], "Assembled bench rig"),
                          (clo, [0.655, 0.29, 0.345, 0.33], "Clamp: pins press on the strip pads")):
        b = fig.add_axes(rect)
        b.imshow(im)
        b.axis("off")
        b.set_title(cap, fontsize=6.8, color=MUTED, pad=1.5)
    c = fig.add_axes([0, 0, 1, 0.255])
    c.axis("off")
    c.set_xlim(0, 100)
    c.set_ylim(0, 10)
    for k, (n, _, _, part, mat) in enumerate(CAD_PARTS):
        col, row = k % 3, k // 3
        x, y = 1 + col * 33.4, 8.6 - row * 3.35
        c.add_patch(Circle((x + 1.3, y), 1.2, fc=NAVY, ec="none"))
        c.text(x + 1.3, y, str(n), color="white", fontsize=6.4, ha="center", va="center", fontweight="bold")
        c.text(x + 3.4, y + 0.55, part, fontsize=7.2, color=NAVY, fontweight="bold", va="center")
        c.text(x + 3.4, y - 1.05, mat, fontsize=6.3, color=SLATE, va="center")
    fig.savefig(FIG / "fig_cad.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    print("wrote fig_cad.png")


# ------------------------------------------------------------------ 8 schematic (refinement 19 Oct): measurement path drawn
# from the reader_v0_1 netlist (same reference designators) + the real KiCad sheet
def _res(ax, x, y, w, label, vertical=False, value=""):
    if vertical:
        ax.add_patch(Rectangle((x - 1.1, y), 2.2, w, fc="white", ec=NAVY, lw=1.1, zorder=3))
        ax.text(x + 1.8, y + w / 2 + 0.9, label, fontsize=6.8, color=NAVY, fontweight="bold", va="center")
        ax.text(x + 1.8, y + w / 2 - 1.4, value, fontsize=6.4, color=SLATE, va="center")
    else:
        ax.add_patch(Rectangle((x, y - 1.1), w, 2.2, fc="white", ec=NAVY, lw=1.1, zorder=3))
        ax.text(x + w / 2, y + 2.2, label, fontsize=6.8, color=NAVY, fontweight="bold", ha="center")
        ax.text(x + w / 2, y - 3.6, value, fontsize=6.4, color=SLATE, ha="center")


def fig_schematic():
    """Zone-C measurement path drawn from the reader_v0_1 netlist (same reference designators and pins), above the
    real KiCad sheet. Pins and values: 6_electronics/kicad/out/reader_v0_1.net, 7_firmware/reader_v0_1/config.h."""
    import pymupdf
    pg = pymupdf.open(ROOT / "6_electronics" / "kicad" / "out" / "reader_v0_1_schematic.pdf")[0]
    r = pg.rect
    pix = pg.get_pixmap(dpi=220, clip=pymupdf.Rect(r.width * 0.055, r.height * 0.07, r.width * 0.99, r.height * 0.80))
    pix.save(HERE / "_sch.png")
    sheet = Image.open(HERE / "_sch.png")
    fig, ax = canvas(5.94, 4.25, (0, 100), (0, 71.5))
    ax.text(1, 70.8, "One zone's measurement path (zone C; zone A is the same via GPIO4, R2, J4.2)", fontsize=8.2,
            color=NAVY, fontweight="bold", va="top")
    Y = 58.5
    box(ax, 0.5, Y - 4, 12, 8, "ESP32-C3\nGPIO3\nDRV_C", fc="#EFF6FF", ec=BLUE, size=6.6, r=1)
    ax.plot([12.5, 15], [Y, Y], color=NAVY, lw=1.1)
    _res(ax, 15, Y, 7, "R1", value="1 kΩ")
    ax.plot([22, 26], [Y, Y], color=NAVY, lw=1.1)
    for xp, lab in ((26.6, "J4.1"), (47.6, "J4.3")):
        ax.add_patch(Circle((xp, Y), 0.7, fc=KAPTON, ec="#92400E", lw=0.8, zorder=4))
        ax.text(xp, Y + 2.4, lab, fontsize=6.4, color="#92400E", ha="center")
    ax.add_patch(FancyBboxPatch((28.5, Y - 4.5), 17, 9, boxstyle="round,pad=0,rounding_size=1", fc="#FFF7E6",
                                ec="#D6B98C", lw=1))
    ax.add_patch(Rectangle((30, Y - 1), 5.5, 2, fc=LIG, ec="none"))
    ax.add_patch(Rectangle((38.5, Y - 1), 5.5, 2, fc=LIG, ec="none"))
    ax.add_patch(FancyBboxPatch((33.5, Y - 1.4), 7, 2.8, boxstyle="round,pad=0,rounding_size=1.2", fc="#60A5FA",
                                alpha=0.5, ec="none"))
    ax.text(37, Y + 2.6, "strip zone C = Rx", fontsize=6.6, color="#92400E", ha="center", fontweight="bold")
    ax.text(37, Y - 3.6, "wet ≈ 4–15 kΩ · dry > 1 MΩ", fontsize=6, color=SLATE, ha="center")
    ax.plot([45.5, 47], [Y, Y], color=NAVY, lw=1.1)
    ax.plot([48.3, 50], [Y, Y], color=NAVY, lw=1.1)
    _res(ax, 50, Y, 7, "R3", value="1 kΩ")
    ax.plot([57, 70], [Y, Y], color=NAVY, lw=1.1)
    NX = 62
    ax.add_patch(Circle((NX, Y), 0.9, fc=NAVY, ec="none", zorder=4))
    ax.text(NX - 1.2, Y + 2.0, "N", fontsize=7.2, color=NAVY, fontweight="bold", ha="right")
    _res(ax, 70, Y, 8, "R5", value="100 kΩ 0.1 %")
    ax.plot([78, 86], [Y, Y], color=NAVY, lw=1.1)
    box(ax, 86, Y - 4, 13.5, 8, "ESP32-C3\nGPIO10\nDRV_REF", fc="#EFF6FF", ec=BLUE, size=6.6, r=1)
    ax.plot([NX, NX], [Y, 61.5], color=NAVY, lw=1.1)                     # check resistor from above
    _res(ax, NX, 61.5, 4.2, "R6", vertical=True, value="100 kΩ check")
    ax.plot([NX, NX], [65.7, 66.6], color=NAVY, lw=1.1)
    ax.text(NX, 67.0, "GPIO20 DRV_CHK", fontsize=6.4, color=BLUE, ha="center")
    ax.plot([NX, NX], [Y, 46], color=NAVY, lw=1.1)                       # node N down to the ADC
    ax.plot([NX, 56], [51, 51], color=NAVY, lw=1.1)                      # C1 to ground
    ax.plot([56, 56], [51, 49.9], color=NAVY, lw=1.1)
    ax.plot([53.5, 58.5], [49.9, 49.9], color=NAVY, lw=1.5)
    ax.plot([53.5, 58.5], [48.7, 48.7], color=NAVY, lw=1.5)
    ax.plot([56, 56], [48.7, 47.4], color=NAVY, lw=1.1)
    for k, half in enumerate((2.2, 1.4, 0.6)):
        ax.plot([56 - half, 56 + half], [47.4 - k * 0.7, 47.4 - k * 0.7], color=NAVY, lw=1.0)
    ax.text(52.6, 49.3, "C1 10 nF", fontsize=6.2, color=NAVY, ha="right", va="center")
    box(ax, 55, 37, 20, 9, "ADS1115 (U2)\nA0 = node N\nA1 = 3V3 rail", fc="#EFF6FF", ec=BLUE, size=6.6, r=1)
    ax.plot([75, 82], [41.5, 41.5], color=NAVY, lw=1.1)
    ax.text(78.5, 42.9, "I²C 0x48", fontsize=6.2, color=SLATE, ha="center")
    box(ax, 82, 37, 17.5, 9, "ESP32-C3\nSDA GPIO6\nSCL GPIO7", fc="#EFF6FF", ec=BLUE, size=6.6, r=1)
    for k, t in enumerate(("Phase +: DRV_C high, DRV_REF low; phase −: reversed",
                           "→ no net DC on the wet strip",
                           "Loop: GPIO5 → R4 → J4.4 → strip loop → J4.3 (open = FAULT)",
                           "LEDs: GPIO0 / 1 / 21 → R7–R9 1 kΩ → D1–D3")):
        ax.text(1, 49.5 - k * 3.1, t, fontsize=6.3, color=SLATE, va="top")
    b = fig.add_axes([0.0, 0.0, 1.0, 0.46])
    b.imshow(sheet)
    b.axis("off")
    b.set_title("Our full KiCad 10 schematic (reader_v0_1.kicad_sch), ERC 0 violations", fontsize=6.8, color=MUTED, pad=1)
    fig.savefig(FIG / "fig_schematic.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    (HERE / "_sch.png").unlink()
    print("wrote fig_schematic.png")


# ------------------------------------------------------------------ 10 maker evidence gallery (refinement 19 Oct)
def _code_excerpt():
    """classify() from zone_logic.h and one of its compile-time tests; only line breaks are added. Checked against the
    source so the excerpt cannot drift from the firmware."""
    src = (ROOT / "7_firmware" / "reader_v0_1" / "zone_logic.h").read_text(encoding="utf-8")
    tests = (ROOT / "7_firmware" / "reader_v0_1" / "zone_logic_tests.h").read_text(encoding="utf-8")
    assert "fault ? State::Fault" in src and "(a == Wet::WET ? (c == Wet::WET ? State::Change : State::Check) : State::Ok)" in src
    assert 'classify(Wet::WET, Wet::WET, false) == State::Change, "front reached the change line"' in tests
    return ["// C = pad centre, A = maker's change line",
            "constexpr State classify(Wet c, Wet a,",
            "                         bool fault) {",
            "  return fault ? State::Fault",
            "    : (a == Wet::WET ? (c == Wet::WET",
            "         ? State::Change : State::Check)",
            "       : State::Ok);",
            "}",
            "static_assert(classify(Wet::WET, Wet::WET,",
            "   false) == State::Change,",
            '   "front reached the change line");']


def fig_maker():
    import pymupdf
    drw = pymupdf.open(ROOT / "5_cad" / "solidworks" / "clamp_base_v0_1_drawing.PDF")[0]
    r = drw.rect
    drw.get_pixmap(dpi=150, clip=pymupdf.Rect(0, 0, r.width, r.height)).save(HERE / "_drw.png")
    sch = pymupdf.open(ROOT / "6_electronics" / "kicad" / "out" / "reader_v0_1_schematic.pdf")[0]
    sch.get_pixmap(dpi=110).save(HERE / "_sch.png")
    e2 = pymupdf.open(ROOT / "4_sensor_strip" / "e2_experiment" / "E2_bench_sheets.pdf")[0]
    e2.get_pixmap(dpi=90).save(HERE / "_e2.png")
    tiles = [(Image.open(FIG / "sw_ui_assembly.png"), "SolidWorks: our assembly + feature tree"),
             (Image.open(HERE / "_drw.png"), "A3 drawing: clamp base (mm, first-angle)"),
             (Image.open(HERE / "_sch.png"), "KiCad 10: reader schematic"),
             (None, "Firmware: state rule + compile-time test"),
             (Image.open(ROOT / "4_sensor_strip" / "strip_v0_1_drawing.png"), "Laser file: strip v0.1 (from DXF)"),
             (Image.open(HERE / "_e2.png"), "E2 bench sheet: 72 samples fixed in advance")]
    fig = plt.figure(figsize=(5.94, 4.25))
    for k, (im, cap) in enumerate(tiles):
        col, row = k % 3, k // 3
        a = fig.add_axes([0.005 + col * 0.333, 0.665 - row * 0.335, 0.323, 0.285])
        if im is None:
            a.set_xlim(0, 10)
            a.set_ylim(0, 10)
            a.add_patch(Rectangle((0, 0), 10, 10, fc="#0F172A", ec="none"))
            for i, line in enumerate(_code_excerpt()):
                a.text(0.25, 9.55 - i * 0.86, line, fontsize=4.5, color="#86EFAC" if line.startswith(("static", "   false", "   the"))
                       else "#E2E8F0", family="Consolas", va="top")
        else:
            a.imshow(im)
        a.set_xticks([])
        a.set_yticks([])
        for s in a.spines.values():
            s.set_color(LINE)
        a.set_title(cap, fontsize=6.3, color=NAVY, pad=1.5)
    c = fig.add_axes([0, 0, 1, 0.29])
    c.axis("off")
    c.set_xlim(0, 10)
    c.set_ylim(0, 3)
    c.add_patch(FancyBboxPatch((0.05, 0.05), 9.9, 2.9, boxstyle="round,pad=0,rounding_size=0.15", fc="#0F172A", ec="none"))
    c.text(0.25, 2.75, "Checks re-run on 19 Oct 2026 (results as printed by each tool)", fontsize=6, color="#94A3B8",
           family="Consolas", va="top")
    out = [("verify_cad.py (SolidWorks)", "{'PASS': 99, 'FAIL': 0, 'BLOCKED': 5}"),
           ("kicad-cli sch erc", "Found 0 violations"),
           ("verify_laser_files.py", "35 PASS, 0 FAIL"),
           ("arduino-cli compile (esp32c3)", "Sketch uses 650349 bytes (49%)"),
           ("pytest (firmware tools)", "16 passed"),
           ("pytest (E2 analysis, synthetic data)", "3 passed")]
    for i, (cmd, res) in enumerate(out):
        y = 2.28 - i * 0.37
        c.text(0.25, y, cmd, fontsize=5.9, color="#94A3B8", family="Consolas", va="top")
        c.text(4.6, y, res, fontsize=6.1, color="#86EFAC", family="Consolas", va="top")
    fig.savefig(FIG / "fig_maker.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    for f in ("_drw.png", "_sch.png", "_e2.png"):
        (HERE / f).unlink()
    print("wrote fig_maker.png")


# ------------------------------------------------------------------ photo placeholders for the team (never fake photos)
def fig_placeholders():
    for name, (w, h), lines in (("placeholder_team.png", (3.0, 4.0), ["TEAM PHOTO", "", "replace: right-click →", "Change Picture",
                                                                       "", "(ID badge visible)"]),
                                ("placeholder_lab.png", (4.0, 2.67), ["LAB PHOTO", "team at work, ID badges visible", "",
                                                                      "replace: right-click → Change Picture"])):
        fig, ax = canvas(w, h, (0, 10), (0, 10 * h / w))
        H = 10 * h / w
        ax.add_patch(FancyBboxPatch((0.2, 0.2), 9.6, H - 0.4, boxstyle="round,pad=0,rounding_size=0.4", fc="#F1F5F9",
                                    ec="#94A3B8", lw=1.4, ls=(0, (4, 3))))
        for i, t in enumerate(lines):
            ax.text(5, H / 2 + (len(lines) / 2 - i - 0.5) * 0.9, t, ha="center", va="center",
                    fontsize=12 if i == 0 else 8.5, color=SLATE if i else NAVY, fontweight="bold" if i == 0 else "normal")
        fig.savefig(FIG / name, dpi=150, facecolor="white")
        plt.close(fig)
        print("wrote", name)


# ------------------------------------------------------------------ 7 strip layout + E2 coupon (from the real geometry)
def fig_strip():
    fig = plt.figure(figsize=(5.94, 4.25))
    ax = fig.add_axes([0.02, 0.38, 0.96, 0.60])
    ax.add_patch(Polygon(G["outline"], closed=True, fc=KAPTON, ec="#B45309", lw=0.8))
    for name, pts in G["nets"].items():
        ax.add_patch(Polygon(pts, closed=True, fc=LIG, ec="none"))
    for h in G["holes"]:
        ax.add_patch(Circle((h["x"], h["y"]), h["d"] / 2, fc="white", ec="#B45309", lw=0.6))
    for z, (x0, y0, x1, y1) in G["windows"].items():
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="#16A34A", lw=1.3, ls=(0, (2, 1))))
        ax.text((x0 + x1) / 2, 12.6, f"window {z}", ha="center", fontsize=7, color="#15803D", fontweight="bold")
    sx = min(x for x, _ in G["seal_outline"])
    ax.add_patch(Rectangle((sx, -0.6), G["tip"] - sx, 11.2, fc="none", ec="#F59E0B", lw=0.9, ls=(0, (4, 2))))
    for n, p in G["pads"].items():
        ax.text(p["x"] - 3.6, p["y"], n.replace("_", " "), fontsize=5.6, color=NAVY, ha="right", va="center")
    xp = G["x_positions"]
    for k, lab in (("dressing_edge", "dressing edge"), ("pad_edge", "pad edge")):
        ax.axvline(xp[k], color="#94A3B8", lw=0.7, ls=":")
        ax.text(xp[k] + 0.6, 19.5, lab, fontsize=6, color=MUTED, rotation=90, va="top")
    ax.annotate("", (0, -6.6), (G["tip"], -6.6), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=0.8))
    ax.text(G["tip"] / 2, -8.6, f"{G['tip']:.0f} mm", ha="center", fontsize=7, color=BLUE)
    ax.text(G["tip"] + 1, 5, "10 mm", fontsize=6.6, color=BLUE, va="center")
    ax.text(57, 17.6, "1.0 mm lines / gaps: PROVISIONAL until E2", fontsize=6.6, color=AMBER, fontweight="bold")
    ax.set_xlim(-14, 106)
    ax.set_ylim(-10.5, 21)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Strip v0.1 (from strip_v0_1.dxf): black = LIG-like, amber = polyimide, green = windows, "
                 f"orange dashes = seal tape (from x = {sx:.0f} mm)",
                 fontsize=7, color=MUTED, pad=2)
    # E2 coupon
    bx = fig.add_axes([0.02, 0.02, 0.96, 0.34])
    doc = ezdxf.readfile(ROOT / "4_sensor_strip" / "e2_experiment" / "e2_res_coupon.dxf")
    for e in doc.modelspace():
        if e.dxftype() == "LWPOLYLINE":
            pts = [tuple(p[:2]) for p in e.get_points()]
            if e.dxf.layer == "ENGRAVE":
                bx.add_patch(Polygon(pts, closed=True, fc=LIG, ec="none"))
            else:
                bx.add_patch(Polygon(pts, closed=True, fc="none", ec="#2563EB", lw=0.7))
        elif e.dxftype() == "CIRCLE":
            bx.add_patch(Circle((e.dxf.center.x, e.dxf.center.y), e.dxf.radius, fc="none", ec="#2563EB", lw=0.7))
    for row in csv.DictReader(open(ROOT / "4_sensor_strip" / "e2_experiment" / "e2_res_coupon_features.csv", encoding="utf-8")):
        x = float(row["x_from_notch_end_mm"])
        if row["kind"] == "line":
            bx.text(x + 12, -2.4, f"w {float(row['drawn_mm']):.1f}", ha="center", fontsize=6.2, color=NAVY)
        elif row["kind"] == "gap":
            bx.text(x + 12, 21.2, f"gap {float(row['drawn_mm']):.1f}", ha="center", fontsize=6.2, color=NAVY)
    bx.text(156, -2.4, "Ø2.0 cut", ha="center", fontsize=6.2, color="#2563EB")
    bx.set_xlim(-2, 182)
    bx.set_ylim(-5, 24)
    bx.set_aspect("equal")
    bx.axis("off")
    bx.set_title("E2 test coupon (e2_res_coupon.dxf, 180 × 20 mm): line widths 0.3–1.5 mm, isolation gaps 0.2–1.5 mm, "
                 "laser-cut Ø2 holes", fontsize=7, color=MUTED, pad=2)
    save(fig, "fig_strip.png")


# ------------------------------------------------------------------ 9 measurement window (calc_readout numbers)
def fig_window():
    fig = plt.figure(figsize=(5.94, 4.25))
    ax = fig.add_axes([0.06, 0.53, 0.92, 0.36])
    ax.set_xscale("log")
    ax.set_xlim(1e2, 1e8)
    ax.set_ylim(0, 4)
    ax.axvspan(4.2e3, 14.8e3, color="#60A5FA", alpha=0.35)
    ax.axvspan(1e6, 1e8, color="#FDBA74", alpha=0.45)
    ax.axvspan(1e5, 3e5, color="#FDE68A", alpha=0.6)
    ax.axvline(3e6, color=RED, lw=1.2, ls="--")
    ax.text(7.9e3, 3.4, "expected WET\n4.2–14.8 kΩ", ha="center", fontsize=7.4, color="#1D4ED8", va="top")
    ax.text(1.75e5, 3.4, "hysteresis\n100–300 kΩ", ha="center", fontsize=7.4, color="#92400E", va="top")
    ax.text(1e7, 3.4, "expected DRY\n≥ 1 MΩ", ha="center", fontsize=7.4, color="#9A3412", va="top")
    ax.text(3.3e6, 0.5, "isolation rule\n> 3 MΩ (E2)", fontsize=6.6, color=RED)
    ax.set_yticks([])
    ax.set_xlabel("reader resistance Rx (Ω), log scale", fontsize=7.5)
    ax.tick_params(labelsize=7)
    ax.set_title("Why a 100 kΩ reference: wet and dry sit > 6× either side of the alert band (calculated)",
                 fontsize=7.6, color=NAVY, pad=4)
    ax2 = fig.add_axes([0.02, 0.04, 0.96, 0.36])
    ax2.axis("off")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 30)
    chain = ["LIG pad", "pogo pin", "1 kΩ", "node N\n100 kΩ ref", "ADS1115\n16-bit", "ESP32-C3", "CSV / LEDs"]
    for i, t in enumerate(chain):
        x = 1 + i * 14.1
        box(ax2, x, 12, 12, 11, t, fc="#EFF6FF" if i in (0, 1) else "white", ec=BLUE, size=6.9, r=1.2)
        if i < len(chain) - 1:
            arrow(ax2, x + 12.1, 17.5, x + 14, 17.5, color=MUTED, lw=1)
    ax2.text(1, 8, "Ranges are calculations (calc_readout.py): Solution A conductivity, LIG Rs 20–100 Ω/sq from literature,\n"
                   "1 mm gap. Real wet and dry values will come from E2 and E4.", fontsize=6.4, color=MUTED, va="top")
    save(fig, "fig_window.png")


# ------------------------------------------------------------------ 11 design decision + iterations
def fig_decision():
    fig = plt.figure(figsize=(5.94, 4.25))
    ax = fig.add_axes([0.42, 0.62, 0.54, 0.31])
    concepts = [("S2 two-zone strip (C + change line A)", 4.36), ("S1 single zone at change line", 4.29),
                ("S3 four-zone front strip", 3.96), ("S5 capacitive, sealed electrodes", 3.46),
                ("S4 continuous resistive locator", 3.39)]
    ys = range(len(concepts))[::-1]
    ax.barh(list(ys), [s for _, s in concepts], color=[GREEN] + [LINE] * 4, height=0.62)
    for y, (n, s) in zip(ys, concepts):
        ax.text(s + 0.03, y, f"{s:.2f}", va="center", fontsize=7, color=SLATE)
    ax.set_xlim(3.0, 4.75)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([n for n, _ in concepts], fontsize=7)
    ax.get_yticklabels()[0].set_fontweight("bold")
    ax.get_yticklabels()[0].set_color(GREEN)
    ax.tick_params(labelsize=6.5)
    ax.set_title("13-criterion weighted score (decision_matrix.py)", fontsize=7.2, color=MUTED, pad=3)
    fig.text(0.02, 0.535, "S2 wins on discrimination: a real front wets C before A, so 'A before C' reveals a leak or a "
                          "misplaced strip.", fontsize=6.6, color=SLATE)
    tl = fig.add_axes([0.02, 0.02, 0.96, 0.44])
    tl.axis("off")
    tl.set_xlim(0, 100)
    tl.set_ylim(0, 40)
    tl.plot([3, 97], [30, 30], color=LINE, lw=2)
    events = [("Stage 1", "closed-loop electro-\ntherapy bandage:\ntoo broad to build", MUTED),
              ("Restart", "v1 archived; needs,\nevidence register,\nsensor options", BLUE),
              ("D-012", "5 concepts scored;\n4 zones → 2 zones\n(wider laser gaps)", GREEN),
              ("CAD check", "interference found\nseal under clamp →\nmoved to 23 mm", AMBER),
              ("Reader", "ERC 0, firmware\ncompiles, design\ncross-check 0 err", GREEN),
              ("FMEA", "hidden lead break\n(RPN 224) → v0.2:\nloop each lead", RED)]
    for i, (h, b, col) in enumerate(events):
        x = 6 + i * 17.6
        tl.add_patch(Circle((x, 30), 1.6, fc=col, ec="white", lw=1.2))
        tl.text(x, 35.5, h, ha="center", fontsize=7.4, color=col, fontweight="bold")
        tl.text(x, 26, b, ha="center", va="top", fontsize=6.4, color=SLATE, linespacing=1.15)
    tl.text(3, 2.5, "Each step is a dated git commit (from 1edae21, 14 Oct) with its decision in 3_decisions/decisions.md",
            fontsize=6.3, color=MUTED)
    save(fig, "fig_decision.png")


# ------------------------------------------------------------------ 12 FMEA RPN chart
def fig_fmea():
    rows = list(csv.DictReader(open(ROOT / "3_decisions" / "fmea_v0_1.csv", encoding="utf-8")))
    rows.sort(key=lambda r: int(r["RPN"]))
    fig = plt.figure(figsize=(3.6, 2.15))
    ax = fig.add_axes([0.40, 0.16, 0.57, 0.80])
    cols = [RED if int(r["RPN"]) >= 150 else AMBER if int(r["RPN"]) >= 100 else "#94A3B8" for r in rows]
    ax.barh(range(len(rows)), [int(r["RPN"]) for r in rows], color=cols, height=0.7)
    ax.set_yticks(range(len(rows)))
    short = {"F01": "LIG not conductive", "F02": "gap bridged", "F03": "COM loop break", "F04": "sense-lead break (hidden)",
             "F05": "pin contact on LIG", "F06": "seal misregistered", "F07": "concept: front path", "F08": "dry baseline low",
             "F09": "readout error", "F10": "DC on electrodes", "F11": "strip reversed", "F12": "laser fumes",
             "F13": "laser fire", "F14": "mains coupling", "F15": "particle shedding"}
    ax.set_yticklabels([f"{r['id']} {short[r['id']]}" for r in rows], fontsize=5.4)
    ax.axvline(100, color=SLATE, lw=0.8, ls="--")
    ax.tick_params(axis="x", labelsize=5.5)
    ax.set_xlabel("RPN = S × O × D (estimated)", fontsize=5.8)
    save(fig, "fig_fmea.png")


# ------------------------------------------------------------------ 13 roadmap gantt
def fig_roadmap():
    """Weeks from Mon 26 Oct 2026. Programme dates: vishwakarma-awards.org + Internshala listing (read 19 Oct 2026)."""
    fig = plt.figure(figsize=(12.17, 2.15))
    ax = fig.add_axes([0.235, 0.17, 0.755, 0.70])
    tasks = [("E2 laser fabrication validation", 0, 2.5, AMBER),
             ("Order parts · wire + bench-test reader (T0–T11)", 0, 3, AMBER),
             ("First strips on a dressing · 3-min prototype video", 3, 5.6, NAVY),
             ("Strip v0.2 (E2 sizes, looped leads) · print clamp", 4, 8, BLUE),
             ("E4: strips on real dressings, simulated exudate", 6, 11, GREEN),
             ("Repeatability: ≥ 5 strips × 3 runs", 9, 12.5, GREEN),
             ("Raman / SEM via partner lab (if access)", 4, 12, "#94A3B8"),
             ("Semi-final prep: 5-min live demo (virtual)", 10.5, 13, NAVY),
             ("Finale demo at IIT Indore", 13, 14, NAVY)]
    for i, (t, a, b, c) in enumerate(tasks[::-1]):
        ax.barh(i, b - a, left=a, color=c, height=0.62, alpha=0.9)
        ax.text(-0.15, i, t, ha="right", va="center", fontsize=8.4, color=NAVY)
    for g, x, lab, ha in (("G1", 2.5, "E2: Rs CV ≤ 20 %", "right"), ("G2", 3.0, "reader T0–T11 pass", "left"),
                          ("G3", 11, "E4: alert within ±10 %", "center"), ("G4", 14, "live demo", "right")):
        ax.plot(x, len(tasks) - 0.35, marker="D", color=RED, ms=6)
        ax.text(x + (-0.1 if ha == "right" else 0.1 if ha == "left" else 0), len(tasks) + 0.12, f"{g} {lab}", ha=ha,
                fontsize=6.4, color=RED)
    for x, lab in ((5.6, "video + PPT (early Dec)"), (13, "IIT Indore 26 Jan – 1 Feb")):
        ax.axvline(x, color=NAVY, lw=1.0, ls=(0, (3, 2)))
        ax.text(x - 0.1, -0.5, lab, fontsize=6.2, color=NAVY, va="bottom", ha="right", fontweight="bold")
    ax.set_xlim(0, 14.2)
    ax.set_ylim(-0.6, len(tasks) + 0.6)
    ax.set_yticks([])
    months = (0.86, 5.14, 9.57, 14.0)   # 1 Nov, 1 Dec, 1 Jan, 1 Feb in weeks from 26 Oct
    ax.set_xticks([0, *months])
    ax.set_xticklabels(["26 Oct", "Nov 2026", "Dec", "Jan 2027", "1 Feb"], fontsize=8)
    for x in months[:3]:
        ax.axvline(x, color=LINE, lw=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    save(fig, "fig_roadmap.png")


# ------------------------------------------------------------------ 14 challenge evidence: seal clash + hidden lead break
def fig_challenges():
    fig = plt.figure(figsize=(12.17, 1.65))
    a = fig.add_axes([0.01, 0.06, 0.53, 0.86])
    a.axis("off")
    a.set_xlim(-8, 100)
    a.set_ylim(-4.6, 3.8)
    for row, (sx, lab, col) in enumerate(((12, "before: seal starts at x = 12 mm → 9.0 mm³ trapped under the clamp", RED),
                                           (23, "after (D-013): seal starts at x = 23 mm → 0 interference (re-verified)", GREEN))):
        y = 1.4 - row * 3.4
        a.add_patch(Rectangle((-4, y - 1.6), 26, 1.6, fc="#2E6BC6", ec="none"))          # clamp base top region
        a.add_patch(Rectangle((0, y + 0.15), 96, 0.35, fc=KAPTON, ec="none"))            # strip
        a.add_patch(Rectangle((sx, y - 0.25), 96 - sx, 0.4, fc="#F59E0B", ec="none", alpha=0.9))  # seal (scale exaggerated)
        if sx < 22:
            a.add_patch(Rectangle((sx, y - 0.25), 22 - sx, 0.4, fc="none", ec=RED, hatch="////", lw=1))
        a.text(24, y + 1.15, lab, fontsize=7.2, color=col, fontweight="bold")
    a.text(-4, -4.3, "Side section along the strip (thickness exaggerated): clamp base (blue), strip (amber), seal tape (orange)",
           fontsize=6.3, color=MUTED)
    b = fig.add_axes([0.56, 0.06, 0.43, 0.86])
    b.axis("off")
    b.set_xlim(0, 100)
    b.set_ylim(0, 30)
    b.text(0, 28, "Hidden failure F04: a cracked sense lead reads as 'dry' forever", fontsize=7.4, color=RED, fontweight="bold",
           va="top")
    b.plot([2, 30], [18, 18], color=LIG, lw=3)
    b.plot([33, 60], [18, 18], color=LIG, lw=3)
    b.text(31.5, 18, "✕", ha="center", va="center", fontsize=11, color=RED)
    b.text(62, 18, "zone → reads open = DRY → CHANGE never shown", fontsize=6.6, color=SLATE, va="center")
    b.plot([2, 60, 60, 2], [9, 9, 5, 5], color=GREEN, lw=2.4)
    b.text(62, 7, "v0.2: lead returns to a 2nd pad → continuity\nchecked every scan → FAULT", fontsize=6.6, color=GREEN,
           va="center")
    save(fig, "fig_challenges.png")


if __name__ == "__main__":
    fig_problem()
    fig_journeys()
    fig_howitworks()
    fig_dataflow()
    fig_cad()
    fig_strip()
    fig_schematic()
    fig_window()
    fig_maker()
    fig_decision()
    fig_fmea()
    fig_roadmap()
    fig_challenges()
    fig_placeholders()

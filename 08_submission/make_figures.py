"""
Figures for the Stage 2 deck. Everything is drawn from project files or plain geometry -
no stock photos, no AI images. Concept drawings are labelled as concepts.
Each figure is sized to the picture frame it fills on its slide (width 5.92 in; heights in SIZES).
Run: python make_figures.py
"""
import configparser
import csv
import math
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle, Wedge
import schemdraw
import schemdraw.elements as elm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.png"):
    old.unlink()

FRAME_W = 5.92                      # inches on the slide
SIZES = {"problem": 3.85, "journey": 3.85, "concept": 4.15, "coupon_matrix": 3.60,
         "schematic": 4.50, "work_evidence": 3.30}
NAVY, GREEN, RED, AMBER, GREY, INK = "#1e3a8a", "#15803d", "#b91c1c", "#d97706", "#64748b", "#0f172a"
PAD, STAIN, KAPTON, LIG = "#fdf6e3", "#e9c46a", "#f2a541", "#1f2937"
W = 22.4                            # drawing units across the figure
plt.rcParams.update({"font.family": "DejaVu Sans"})


def figure(name):
    h = SIZES[name]
    fig = plt.figure(figsize=(FRAME_W * 2, h * 2))
    return fig, W * h / FRAME_W     # drawing height in units (keeps circles round)


def canvas(name):
    fig, H = figure(name)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    return fig, ax, H


def rbox(ax, x, y, w, h, fc, ec, lw=1.6, r=0.25):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))


def dressing(ax, x, y, s, stain_r, pad_frac=0.72):
    """Bordered dressing; the dashed square is the change line (0.22 x pad inside the pad edge)."""
    rbox(ax, x, y, s, s, "#eef2f7", "#94a3b8", lw=1.2, r=0.4)
    m = s * (1 - pad_frac) / 2
    px, py, ps = x + m, y + m, s * pad_frac
    ax.add_patch(Rectangle((px, py), ps, ps, fc=PAD, ec="#cbb994", lw=1.2))
    cx, cy = px + ps / 2, py + ps / 2
    ax.add_patch(Circle((cx, cy), stain_r, fc=STAIN, ec="#c08a1e", lw=1, alpha=0.85))
    c = ps * 0.22
    ax.add_patch(Rectangle((px + c, py + c), ps - 2 * c, ps - 2 * c, fc="none", ec=RED, lw=1.6, ls=(0, (4, 3))))
    return px, py, ps, cx, cy


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=200)
    plt.close(fig)


def fig_problem():
    fig, ax, H = canvas("problem")
    s = H - 2.6
    px, py, ps, cx, cy = dressing(ax, 0.4, 1.3, s, 0.28 * s * 0.72 * 0.8)
    r = 0.28 * ps * 0.8
    for ang in (25, 115, 205, 295):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        ax.annotate("", xy=(cx + 1.75 * r * dx, cy + 1.75 * r * dy), xytext=(cx + 1.08 * r * dx, cy + 1.08 * r * dy),
                    arrowprops=dict(arrowstyle="-|>", color="#a16207", lw=2))
    ax.text(cx, cy, "exudate", ha="center", va="center", fontsize=14, color="#78350f", weight="bold")
    ax.text(0.4, H - 0.75, "When is a dressing 'full'?", fontsize=18, weight="bold", color=NAVY)
    ax.annotate("maker's change line \u2248 2 cm from pad edge", xy=(px + ps * 0.5, py + ps * 0.78),
                xytext=(px, py + ps + 0.42), fontsize=13, color=RED, weight="bold",
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))
    ax.text(px, py - 0.85, "absorbent pad inside the dressing border", fontsize=11.5, color="#78716c")
    ms = (H - 2.4) / 3 - 0.35
    mp = ms * 0.72
    cd = 0.28 * mp
    states = [("Too early", 0.5 * cd, RED, "changed by the clock:\nwasted dressing,\nwound bed disturbed"),
              ("Right time", 1.08 * cd, GREEN, "front at the change line:\nchange now"),
              ("Too late", 0.62 * mp, RED, "past the pad edge: leak,\nmacerated skin")]
    for i, (name, rad, col, txt) in enumerate(states):
        y0 = H - 1.2 - (i + 1) * (ms + 0.35)
        dressing(ax, s + 1.3, y0, ms, rad)
        ax.text(s + ms + 1.75, y0 + ms * 0.62, name, fontsize=15, weight="bold", color=col)
        ax.text(s + ms + 1.75, y0 + ms * 0.12, txt, fontsize=12.5, color=INK)
    ax.text(0.4, 0.3, "Under a bandage or opaque cover, the nurse sees none of this.", fontsize=14, color=INK,
            weight="bold")
    save(fig, "problem")


def fig_journey():
    fig, ax, H = canvas("journey")
    rh = (H - 1.0) / 2 - 0.25

    def row(y, steps, col, fc, label):
        ax.add_patch(Rectangle((0.25, y), 2.0, rh, fc=col, ec="none"))
        ax.text(1.25, y + rh / 2, label, ha="center", va="center", fontsize=14, color="white", weight="bold",
                rotation=90)
        x, w, gap = 2.6, 3.6, 0.35
        for i, t in enumerate(steps):
            rbox(ax, x, y + 0.1, w, rh - 0.2, fc, col, lw=1.8)
            ax.add_patch(Circle((x + 0.5, y + rh - 0.6), 0.36, fc=col, ec="none"))
            ax.text(x + 0.5, y + rh - 0.6, str(i + 1), ha="center", va="center", fontsize=13, color="white",
                    weight="bold")
            ax.text(x + w / 2, y + rh * 0.42, t, ha="center", va="center", fontsize=13.5, color=INK)
            if i < len(steps) - 1:
                ax.annotate("", xy=(x + w + gap - 0.02, y + rh / 2), xytext=(x + w + 0.02, y + rh / 2),
                            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2))
            x += w + gap

    row(H / 2 + 0.25, ["Dressing\napplied", "Exudate\nspreads unseen\nunder bandage", "Changed by\nthe clock, or\nafter a leak",
                       "Too early:\nwound disturbed\nToo late:\nskin macerated", "Repeat every\n1\u20133 days"],
        RED, "#fef2f2", "TODAY")
    row(0.4, ["Strip on the pad,\nreader clipped\non (no wound\ncontact)", "Zones read\nwet / dry every\nfew seconds",
              "Phone shows\nOK \u00b7 SOON \u00b7\nCHANGE \u00b7 LEAK", "Change when\nthe change line\nis wet, not by\nthe clock",
              "Strip thrown\naway, reader\nreused"],
        GREEN, "#f0fdf4", "DERMASENSE")
    save(fig, "journey")


def fig_concept():
    fig, ax, H = canvas("concept")
    s = min(H - 2.9, 10.2)
    pad = s * 0.72
    px, py, ps, cx, cy = dressing(ax, 0.3, 1.3, s, 1.2 * 0.28 * pad)
    sy, sh = cy - 0.55, 1.1
    ax.add_patch(Rectangle((cx - 0.9, sy), 12.0 - (cx - 0.9), sh, fc=KAPTON, ec="#b45309", lw=1.2))
    a_x = px + ps * 0.78
    for name, zx in (("C", cx), ("M", (cx + a_x) / 2), ("A", a_x), ("E", px + ps * 0.95)):
        ax.add_patch(Rectangle((zx - 0.38, sy + 0.15), 0.76, sh - 0.30, fc=LIG, ec="none"))
        ax.text(zx, sy + sh + 0.28, name, ha="center", fontsize=15, weight="bold", color=LIG)
    rbox(ax, 11.8, cy - 1.3, 2.6, 2.6, "#334155", "#0f172a", r=0.35)
    ax.text(13.1, cy, "reader\nESP32-C3", ha="center", va="center", fontsize=12.5, color="white", weight="bold")
    for r in (0.6, 1.05, 1.5):
        ax.add_patch(Wedge((14.3, cy + 1.4), r, 25, 75, width=0.1, color=GREY))
    qx, qy = 15.6, H - 6.4
    rbox(ax, qx, qy, 2.5, 5.0, "white", INK, lw=2.2, r=0.35)
    rbox(ax, qx + 0.25, qy + 2.9, 2.0, 1.25, "#fee2e2", RED, lw=1.4, r=0.18)
    ax.text(qx + 1.25, qy + 3.52, "CHANGE", ha="center", va="center", fontsize=13, weight="bold", color=RED)
    ax.text(qx + 1.25, qy + 1.5, "C M A wet\nE dry", ha="center", va="center", fontsize=11, color=INK)
    ax.text(18.6, qy + 3.3, "phone app\n(planned)", fontsize=12, color=GREY)
    ax.text(0.3, H - 0.7, "Dermasense concept (illustration; not yet built)", fontsize=17, weight="bold", color=NAVY)
    ax.text(0.3, 0.35, "Zones wet in order:  C centre \u2192 OK    M \u2192 SOON    A change line \u2192 CHANGE    "
            "E edge \u2192 LEAK", fontsize=12.5, color=INK)
    layers = [("cover film", "#e2e8f0", 0.45), ("LIG strip (graphene side down)", KAPTON, 0.45),
              ("absorbent pad", PAD, 0.9), ("wound-contact layer", "#dbeafe", 0.7), ("wound", "#fecaca", 0.7)]
    x0, w, y = 15.0, 7.1, cy - 1.75
    ax.text(x0, y + 0.25, "Layer stack", fontsize=13.5, weight="bold", color=NAVY)
    for name, col, th in layers:
        ax.add_patch(Rectangle((x0, y - th), w, th, fc=col, ec="#94a3b8", lw=0.8))
        ax.text(x0 + w / 2, y - th / 2, name, ha="center", va="center", fontsize=11, color=INK)
        y -= th + 0.05
    ax.text(x0, cy + 0.6, "The strip never touches\nthe wound.", fontsize=12.5, color=GREEN, weight="bold")
    save(fig, "concept")


def coupon_polys():
    doc = ezdxf.readfile(ROOT / "04_lig_lab" / "lig_test_coupon.dxf")
    colours = {1: "#dc2626", 2: "#eab308", 3: "#16a34a", 4: "#06b6d4", 5: "#2563eb", 6: "#c026d3", 7: "k"}
    out = []
    for e in doc.modelspace().query("LWPOLYLINE"):
        aci = doc.layers.get(e.dxf.layer).color
        out.append(([(p[0], p[1]) for p in e.get_points()], colours.get(aci, "k"), aci))
    return out


def fig_coupon_matrix():
    fig, _ = figure("coupon_matrix")
    fig.text(0.02, 0.92, "Experiment E1: one coupon = six laser settings around our earlier 'setting 12'",
             fontsize=15, weight="bold", color=NAVY)
    ax = fig.add_axes([0.02, 0.52, 0.96, 0.34])
    for pts, c, aci in coupon_polys():
        ax.add_patch(Polygon(pts, closed=True, fc="none" if aci == 7 else c, ec=c, lw=0.9))
    ax.set_xlim(-2, 239); ax.set_ylim(-2, 22); ax.set_aspect("equal"); ax.axis("off")
    cells = [("#dc2626", "setting 10", "speed S"), ("#eab308", "setting 12", "speed 0.67 S"),
             ("#16a34a", "setting 12", "speed S (ref)"), ("#06b6d4", "setting 12", "speed 1.5 S"),
             ("#2563eb", "setting 14", "speed S"), ("#c026d3", "setting 12", "speed S (ref)")]
    ax = fig.add_axes([0.02, 0.10, 0.96, 0.38]); ax.set_xlim(0, 6); ax.set_ylim(0, 1); ax.axis("off")
    for i, (c, p, sp) in enumerate(cells):
        rbox(ax, i + 0.05, 0.08, 0.9, 0.84, "white", c, lw=2.8, r=0.06)
        ax.text(i + 0.5, 0.62, p, ha="center", fontsize=14, weight="bold", color=c)
        ax.text(i + 0.5, 0.28, sp, ha="center", fontsize=12.5, color=INK)
    fig.text(0.5, 0.025, "4 coupons over 2 days: reference measured 8 times. Strips 8 / 16 / 24 mm long give sheet "
             "resistance with a multimeter.", ha="center", fontsize=12, color=GREY)
    save(fig, "coupon_matrix")


def fig_schematic():
    tmp = OUT / "_sch.png"
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6, fontsize=15)
        d += elm.Dot().label("GPIO_Z\n(ESP32-C3)", "left")
        d += elm.Resistor().right().label("1 k\u03a9", "top")
        d += elm.ResistorVar().right().label("LIG zone\n(wet = low R)", "top")
        d += elm.Resistor().right().label("1 k\u03a9", "top")
        n = d.add(elm.Dot().label("N", "top"))
        d += elm.Resistor().right().label("Rref 100 k\u03a9\n0.1 %", "top")
        d += elm.Dot().label("GPIO_COM", "right")
        d += elm.Line().at(n.center).down(1.8)
        d += elm.Dot(open=True).label("ADS1115 (16-bit)", "bottom")
        d.save(str(tmp), dpi=230)
    fig, _ = figure("schematic")
    fig.text(0.02, 0.93, "Zone readout: drive each zone both ways, read the divider (bench design)", fontsize=15,
             weight="bold", color=NAVY)
    ax = fig.add_axes([0.02, 0.30, 0.96, 0.58]); ax.imshow(plt.imread(tmp)); ax.axis("off")
    notes = ["Each zone is driven + then \u2212, so no net DC flows through the fluid.",
             "Pins rest in high-impedance between scans; 4 zones are scanned in turn.",
             "Dry zone \u2248 open circuit; wet zone \u2248 k\u03a9, a contrast of 100\u00d7 or more (target).",
             "Phase +:  Rz = Rref (Vdd / VN \u2212 1) \u2212 2 k\u03a9      Phase \u2212:  Rz = Rref VN / (Vdd \u2212 VN) \u2212 2 k\u03a9"]
    for i, t in enumerate(notes):
        fig.text(0.04, 0.22 - i * 0.055, "\u2022 " + t, fontsize=12.5, color=INK if i < 3 else GREY)
    save(fig, "schematic")
    tmp.unlink()


def fig_work_evidence():
    fig, _ = figure("work_evidence")
    for x, t in ((0.01, "E1 data sheet: 04_lig_lab/e1_samples.csv"), (0.51, "Machine config: C:\\LaserCAD\\AWCCfg\\SysCfg.ini")):
        hdr = fig.add_axes([x, 0.84, 0.48, 0.13]); hdr.axis("off")
        hdr.add_patch(Rectangle((0, 0), 1, 1, fc=NAVY, transform=hdr.transAxes))
        hdr.text(0.5, 0.5, t, ha="center", va="center", color="white", fontsize=13, weight="bold",
                 transform=hdr.transAxes)
    ax = fig.add_axes([0.01, 0.10, 0.48, 0.70]); ax.axis("off")
    rows = [r for r in csv.DictReader(open(ROOT / "04_lig_lab" / "e1_samples.csv", encoding="utf-8"))
            if r["day"] == "1" and r["coupon"] == "1"]
    tab = ax.table(cellText=[[r["sample_id"], r["power_setting"],
                              r["speed_rule"].replace("*", "\u00b7").replace("_ref", ""), ""] for r in rows],
                   colLabels=["sample", "setting", "speed", "Rs (\u03a9/sq)"], loc="center", cellLoc="center",
                   colWidths=[0.42, 0.16, 0.18, 0.24])
    tab.auto_set_font_size(False); tab.set_fontsize(12.5); tab.scale(1, 2.3)
    fig.text(0.25, 0.03, "pre-filled for 30 cells; Rs is filled after the lab session", ha="center", fontsize=11.5,
             color=GREY)
    ax = fig.add_axes([0.51, 0.10, 0.48, 0.70]); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="#0f172a", transform=ax.transAxes))
    cfg = Path(r"C:\LaserCAD\AWCCfg\SysCfg.ini")
    text = "(config file not found on this PC)"
    if cfg.exists():
        ini = configparser.ConfigParser(strict=False)
        ini.read(cfg, encoding="latin-1")
        out = []
        for sec, keys in (("X", ("Range", "MaxSpeed")), ("Y", ("Range", "MaxSpeed")),
                          ("MachCfg", ("PWMFreq", "MaxPower", "LaserMode"))):
            out.append(f"[{sec}]")
            out += [f"  {k}={ini.get(sec, k)}" for k in keys if ini.has_option(sec, k)]
        text = "\n".join(out)
    ax.text(0.06, 0.94, text, va="top", family="monospace", fontsize=12.5, color="#a7f3d0", transform=ax.transAxes)
    fig.text(0.75, 0.03, "real values: 1200 \u00d7 900 mm bed \u00b7 20 kHz PWM \u00b7 98 % cap", ha="center",
             fontsize=11.5, color=GREY)
    save(fig, "work_evidence")


if __name__ == "__main__":
    fig_problem(); fig_journey(); fig_concept(); fig_coupon_matrix(); fig_schematic(); fig_work_evidence()
    print("figures:", ", ".join(sorted(p.name for p in OUT.glob("*.png"))))

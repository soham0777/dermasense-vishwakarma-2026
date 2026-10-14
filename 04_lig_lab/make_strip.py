"""
Two-zone moisture-front strip, design v0.1 (PROVISIONAL - conservative 1.0 mm features until E2).

Writes (all in mm):
  strip_v0_1.dxf           LIG_ENGRAVE (red, fill/scan) + OUTLINE_CUT (blue, cut incl. 2 alignment holes)
  strip_v0_1_encap.dxf     ENCAP_CUT (green): polyimide-tape seal outline + the two zone windows
  strip_v0_1_geometry.json single source of truth for SolidWorks (06_cad/sw_build.py) and the deck
  strip_v0_1_drc.txt       design-rule check report (clearances, containment, window exposure)
  strip_v0_1_drawing.png   dimensioned fabrication drawing of the laser layers

x runs along the strip from the contact paddle (x = 0) to the tip; y across the strip (0..WIDTH).
Net names: SENSE_C (pad-centre zone), SENSE_A (change-line zone), COM (common loop, ends COM_1 / COM_2).
Usage: python make_strip.py [--pad 75] [--inset 20] [--border 12.5]
"""
import argparse
import json
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
P = dict(                          # design parameters (mm)  - [DES] design choice, [PROV] provisional until E2
    WIDTH=10.0,                    # strip body width [DES]
    F=1.0,                         # LIG trace / electrode width [PROV]
    GAP=1.0,                       # electrode gap inside a window (= calc_readout GAP) [PROV]
    WIN_L=6.0,                     # window length along the strip [DES]
    PAD_PITCH=5.08, PAD_W=3.0, PAD_L=6.0, PAD_X=8.0,    # contact pads (pogo-pin targets) [DES]
    HOLE_D=2.0, HOLE_X=8.0,        # alignment holes [DES]
    PADDLE_L=16.0, NECK_END=30.0,  # paddle 0..16, neck 16..30, body from 30 [DES]
    ENTRY=10.0,                    # strip length from neck end to the dressing edge [DES]
    MIN_CLEAR=0.95,                # DRC minimum spacing between different nets [PROV]
    EDGE_CLEAR=0.4,                # DRC copper-to-outline margin [PROV]
)
# y-bands in the strip body (bottom -> top)
BANDS = {"SENSE_C": (0.5, 1.5), "SENSE_A": (2.5, 3.5), "ROW": (4.5, 5.5), "COM_1": (6.5, 7.5), "COM_2": (8.3, 9.3)}


def build(pad, inset, border):
    w = P["WIDTH"]
    x_de = P["NECK_END"] + P["ENTRY"]          # dressing edge
    x_pe = x_de + border                       # absorbent pad edge
    x_a = x_pe + inset                         # change line (zone A centre)
    x_c = x_pe + pad / 2                       # pad centre (zone C centre)
    if x_c - x_a < P["WIN_L"] + 4:
        raise SystemExit("zones overlap: pad too small for this inset")
    tip = x_c + P["WIN_L"] / 2 + 3.0
    h = P["WIN_L"] / 2

    # contact pads (centred on the paddle), order bottom->top must match the body bands
    order = ["SENSE_C", "SENSE_A", "COM_1", "COM_2"]
    pad_y = {n: w / 2 + (i - 1.5) * P["PAD_PITCH"] for i, n in enumerate(order)}
    y_lo = min(pad_y.values()) - P["PAD_W"] / 2 - 5.0
    y_hi = max(pad_y.values()) + P["PAD_W"] / 2 + 5.0
    holes = [(P["HOLE_X"], y_lo + 2.5), (P["HOLE_X"], y_hi - 2.5)]

    outline = Polygon([(0, y_lo), (P["PADDLE_L"], y_lo), (P["NECK_END"], 0), (tip, 0), (tip, w),
                       (P["NECK_END"], w), (P["PADDLE_L"], y_hi), (0, y_hi)])
    outline_cut = outline.difference(unary_union([Point(c).buffer(P["HOLE_D"] / 2, 64) for c in holes]))

    def fan(name, band):
        py = pad_y[name]
        x0 = P["PAD_X"] + P["PAD_L"] / 2
        return Polygon([(x0, py - P["F"] / 2), (P["NECK_END"], band[0]), (P["NECK_END"], band[1]), (x0, py + P["F"] / 2)])

    def pad_box(name):
        return box(P["PAD_X"] - P["PAD_L"] / 2, pad_y[name] - P["PAD_W"] / 2, P["PAD_X"] + P["PAD_L"] / 2,
                   pad_y[name] + P["PAD_W"] / 2)

    sc, sa, row = BANDS["SENSE_C"], BANDS["SENSE_A"], BANDS["ROW"]
    nets = {
        "SENSE_C": unary_union([pad_box("SENSE_C"), fan("SENSE_C", sc),
                                box(P["NECK_END"], sc[0], x_c - h, sc[1]),          # lane
                                box(x_c - h - 1.0, sc[0], x_c - h, row[1]),         # riser (outside window)
                                box(x_c - h - 1.0, row[0], x_c + h, row[1])]),      # electrode under window C
        "SENSE_A": unary_union([pad_box("SENSE_A"), fan("SENSE_A", sa),
                                box(P["NECK_END"], sa[0], x_a - h, sa[1]),
                                box(x_a - h - 1.0, sa[0], x_a - h, row[1]),
                                box(x_a - h - 1.0, row[0], x_a + h, row[1])]),
        "COM": unary_union([pad_box("COM_1"), fan("COM_1", BANDS["COM_1"]), pad_box("COM_2"),
                            fan("COM_2", BANDS["COM_2"]),
                            box(P["NECK_END"], BANDS["COM_1"][0], tip - 1.5, BANDS["COM_1"][1]),
                            box(P["NECK_END"], BANDS["COM_2"][0], tip - 1.5, BANDS["COM_2"][1]),
                            box(tip - 2.5, BANDS["COM_1"][0], tip - 1.5, BANDS["COM_2"][1])]),  # tip link = loop
    }
    win_y = ((sa[1] + row[0]) / 2, (BANDS["COM_1"][1] + BANDS["COM_2"][0]) / 2)
    windows = {"C": box(x_c - h, win_y[0], x_c + h, win_y[1]), "A": box(x_a - h, win_y[0], x_a + h, win_y[1])}
    encap = Polygon([(P["PADDLE_L"] - 4, 0), (tip, 0), (tip, w), (P["PADDLE_L"] - 4, w)])  # body + neck seal
    encap = box(P["NECK_END"] - 18, 0, tip, w).intersection(outline).buffer(0)

    # ---------------- design-rule check
    rep, ok = [], True
    names = list(nets)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = nets[names[i]].distance(nets[names[j]])
            good = d >= P["MIN_CLEAR"]
            ok &= good
            rep.append(f"clearance {names[i]}-{names[j]}: {d:.2f} mm  {'OK' if good else 'FAIL'} (min {P['MIN_CLEAR']})")
    inner = outline_cut.buffer(-P["EDGE_CLEAR"])
    for n, g in nets.items():
        good = inner.contains(g)
        ok &= good
        rep.append(f"{n} inside outline with {P['EDGE_CLEAR']} mm margin: {'OK' if good else 'FAIL'}")
    for z, win in windows.items():
        expect = "SENSE_C" if z == "C" else "SENSE_A"
        for n, g in nets.items():
            exposed = g.intersection(win).area
            should = n in (expect, "COM")
            good = (exposed > 0) == should
            ok &= good
            rep.append(f"window {z} exposes {n}: {exposed:.1f} mm2  {'OK' if good else 'FAIL'}")
        gap = nets[expect].intersection(win).distance(nets["COM"].intersection(win))
        rep.append(f"window {z} electrode gap: {gap:.2f} mm (design {P['GAP']})")
        others = [g for n, g in nets.items() if n not in (expect, "COM")]
        margin = min(win.distance(g) for g in others)
        rep.append(f"window {z} distance to nearest foreign net: {margin:.2f} mm (= sealing registration tolerance)")
    for n, g in nets.items():
        rep.append(f"{n}: {g.geom_type}, {len(getattr(g, 'geoms', [g]))} piece(s), area {g.area:.1f} mm2")
    rep.insert(0, f"DRC {'PASS' if ok else 'FAIL'} - strip v0.1 (pad {pad} mm, inset {inset} mm, border {border} mm)")
    return dict(outline=outline, outline_cut=outline_cut, nets=nets, windows=windows, encap=encap, holes=holes,
                pad_y=pad_y, tip=tip, x=dict(dressing_edge=x_de, pad_edge=x_pe, A=x_a, C=x_c), report=rep, ok=ok,
                y_lo=y_lo, y_hi=y_hi)


def rings(geom):
    for g in getattr(geom, "geoms", [geom]):
        yield list(g.exterior.coords)
        for r in g.interiors:
            yield list(r.coords)


def write_dxf(path, layers):
    doc = ezdxf.new("R2000", setup=False)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for name, (aci, geoms) in layers.items():
        doc.layers.add(name, color=aci)
        for g in geoms:
            for ring in rings(g):
                msp.add_lwpolyline(ring[:-1], close=True, dxfattribs={"layer": name, "color": 256})
    doc.saveas(path)


def drawing(d, path):
    fig, ax = plt.subplots(figsize=(14, 4.2))
    ax.add_patch(plt.Polygon(list(d["outline"].exterior.coords), fc="#f6c56b", ec="#92400e", lw=1))
    for c in d["holes"]:
        ax.add_patch(plt.Circle(c, 1.0, fc="white", ec="#92400e"))
    colors = {"SENSE_C": "#1f2937", "SENSE_A": "#374151", "COM": "#111827"}
    for n, g in d["nets"].items():
        for poly in getattr(g, "geoms", [g]):
            ax.add_patch(plt.Polygon(list(poly.exterior.coords), fc=colors[n], ec="none"))
    for z, win in d["windows"].items():
        ax.add_patch(plt.Polygon(list(win.exterior.coords), fc="none", ec="#16a34a", lw=2, ls="--"))
        ax.text(win.centroid.x, d["y_hi"] - 3, f"window {z}", ha="center", color="#15803d", fontsize=10, weight="bold")
    for n, y in d["pad_y"].items():
        ax.text(P["PAD_X"] + P["PAD_L"] / 2 + 0.6, y, n, va="center", fontsize=7.5, color="#1e3a8a")
    x = d["x"]

    def dim(x0, x1, y, txt):
        ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color="#1e3a8a", lw=0.9))
        ax.text((x0 + x1) / 2, y + 0.5, txt, ha="center", fontsize=8.5, color="#1e3a8a")

    yb = d["y_lo"] - 2.5
    dim(0, d["tip"], yb, f"{d['tip']:.1f}")
    dim(x["A"], x["C"], -2.2, f"C–A {x['C'] - x['A']:.1f}")
    dim(x["pad_edge"], x["A"], -2.2, f"inset {x['A'] - x['pad_edge']:.1f}")
    for k, lab in (("dressing_edge", "dressing edge"), ("pad_edge", "pad edge"), ("A", "change line")):
        ax.axvline(x[k], color="#9ca3af", lw=0.8, ls=":")
        ax.text(x[k], P["WIDTH"] + 4.0, lab, rotation=90, fontsize=7.5, color="#6b7280", va="bottom", ha="right")
    ax.text(d["tip"] + 1, P["WIDTH"] / 2, "10.0", fontsize=8.5, color="#1e3a8a", va="center")
    ax.set_title("Strip v0.1 fabrication drawing (laser layers, mm). PROVISIONAL: features 1.0 mm, gap 1.0 mm "
                 "until E2. Black = LIG; dashed green = seal windows; amber = Kapton.", fontsize=10)
    ax.set_xlim(-2, d["tip"] + 6); ax.set_ylim(yb - 2, d["y_hi"] + 6); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pad", type=float, default=75.0, help="absorbent pad side length of the test dressing (mm)")
    ap.add_argument("--inset", type=float, default=20.0, help="change line distance inside the pad edge (IFU)")
    ap.add_argument("--border", type=float, default=12.5, help="adhesive border width of the dressing (mm)")
    a = ap.parse_args()
    d = build(a.pad, a.inset, a.border)
    write_dxf(HERE / "strip_v0_1.dxf", {"LIG_ENGRAVE": (1, list(d["nets"].values())),
                                         "OUTLINE_CUT": (5, [d["outline_cut"]])})
    write_dxf(HERE / "strip_v0_1_encap.dxf", {"ENCAP_CUT": (3, [d["encap"].difference(unary_union(list(d["windows"].values())))])})
    geo = {
        "units": "mm", "status": "PROVISIONAL v0.1 - regenerate after E2", "parameters": P, "bands": BANDS,
        "dressing": {"pad": a.pad, "inset": a.inset, "border": a.border},
        "outline": [list(p) for p in d["outline"].exterior.coords][:-1],
        "holes": [{"x": x, "y": y, "d": P["HOLE_D"]} for x, y in d["holes"]],
        "pads": {n: {"x": P["PAD_X"], "y": y, "w": P["PAD_L"], "h": P["PAD_W"]} for n, y in d["pad_y"].items()},
        "windows": {z: [round(v, 3) for v in win.bounds] for z, win in d["windows"].items()},
        "x_positions": {k: round(v, 3) for k, v in d["x"].items()}, "tip": round(d["tip"], 3),
        "paddle_y": [round(d["y_lo"], 3), round(d["y_hi"], 3)], "thickness_film_mm": 0.125,
        "nets": {n: [[round(x, 4), round(y, 4)] for x, y in g.exterior.coords][:-1] for n, g in d["nets"].items()},
        "seal_outline": [[round(x, 4), round(y, 4)] for x, y in d["encap"].exterior.coords][:-1],
    }
    (HERE / "strip_v0_1_geometry.json").write_text(json.dumps(geo, indent=2), encoding="utf-8")
    (HERE / "strip_v0_1_drc.txt").write_text("\n".join(d["report"]) + "\n", encoding="utf-8")
    drawing(d, HERE / "strip_v0_1_drawing.png")
    print("\n".join(d["report"]))
    if not d["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

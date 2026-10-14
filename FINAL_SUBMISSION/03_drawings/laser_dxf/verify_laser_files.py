"""
Check every laser job file before it goes to LaserCAD. Writes laser_files_check.md; exit code 1 on any FAIL.

Per DXF: opens and audits cleanly, R2000 + millimetre units, only closed polylines/circles on the expected layers,
valid (non-self-intersecting) outlines, no overlapping engrave regions, no feature narrower or gap smaller than
designed, engraving inside the cut outline with margin, overall size, fits the 1200 x 900 mm bed.
strip_v0_1.dxf is also compared with strip_v0_1_geometry.json (the CAD source of truth).
What this cannot check: how LaserCAD V8.28 maps the colours to layers and whether it imports the scale correctly.
That is a physical check at the machine (procedure E2, step S0-6).
"""
import json
import sys
import time
from pathlib import Path

import ezdxf
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
BED = (1200.0, 900.0)
ROWS = []

# file: engrave layers, cut layers, expected size (x, y), min feature width, min spacing, min margin to the cut edge
FILES = {
    "lig_test_coupon.dxf": (["CELL_RED", "CELL_YELLOW", "CELL_GREEN", "CELL_CYAN", "CELL_BLUE", "CELL_MAGENTA"],
                            ["OUTLINE_CUT"], (237.0, 20.0), 2.0, 2.0, 1.0),
    "e2/e2_res_coupon.dxf": (["ENGRAVE"], ["CUT"], (180.0, 20.0), 0.3, 0.2, 1.0),
    "strip_v0_1.dxf": (["LIG_ENGRAVE"], ["OUTLINE_CUT"], (96.0, 28.24), 1.0, 0.95, 0.4),
    "strip_v0_1_encap.dxf": ([], ["ENCAP_CUT"], (73.0, 10.0), None, None, None),
}


def row(f, check, ok, detail):
    status = ok if isinstance(ok, str) else ("PASS" if ok else "FAIL")
    ROWS.append((f, check, status, detail))
    print(f"[{status}] {f}: {check} - {detail}")


def narrowest_ok(poly, w):
    """True if no part of poly is narrower than w (morphological opening keeps ~all the area)."""
    r = w / 2 - 0.01
    return poly.buffer(-r, join_style=2).buffer(r, join_style=2).area >= 0.995 * poly.area


def check_file(name, engrave_layers, cut_layers, size, min_w, min_gap, margin):
    path = HERE / name
    if not path.exists():
        row(name, "exists", False, "missing")
        return
    doc = ezdxf.readfile(path)
    aud = doc.audit()
    row(name, "opens and audits", not aud.has_errors, f"{len(aud.errors)} errors, {len(aud.fixes)} fixes")
    row(name, "DXF version / units", doc.dxfversion == "AC1015" and doc.header.get("$INSUNITS") == 4,
        f"{doc.dxfversion}, INSUNITS {doc.header.get('$INSUNITS')} (4 = mm)")
    engr, cuts, bad = {l: [] for l in engrave_layers}, [], []
    for e in doc.modelspace():
        lay = e.dxf.layer
        if e.dxftype() == "LWPOLYLINE" and e.closed:
            pts = [tuple(p[:2]) for p in e.get_points()]
            segs_ok = all(Point(a).distance(Point(b)) > 1e-6 for a, b in zip(pts, pts[1:] + pts[:1]))
            poly = Polygon(pts)
            if not (poly.is_valid and segs_ok):
                bad.append(f"invalid/zero-length outline on {lay}")
            (engr[lay] if lay in engr else cuts).append(poly) if lay in engr or lay in cut_layers else bad.append(f"layer {lay}")
        elif e.dxftype() == "CIRCLE" and lay in cut_layers:
            cuts.append(Point(e.dxf.center.x, e.dxf.center.y).buffer(e.dxf.radius, 64))
        else:
            bad.append(f"{e.dxftype()} {'open' if e.dxftype() == 'LWPOLYLINE' else ''} on {lay}")
    row(name, "only closed outlines on expected layers", not bad, "; ".join(bad) or
        f"{sum(len(v) for v in engr.values())} engrave + {len(cuts)} cut outlines")
    allg = [p for v in engr.values() for p in v] + cuts
    minx, miny = min(p.bounds[0] for p in allg), min(p.bounds[1] for p in allg)
    maxx, maxy = max(p.bounds[2] for p in allg), max(p.bounds[3] for p in allg)
    dx, dy = maxx - minx, maxy - miny
    row(name, "overall size mm", abs(dx - size[0]) < 0.05 and abs(dy - size[1]) < 0.05, f"{dx:.2f} x {dy:.2f} (expected {size[0]} x {size[1]})")
    row(name, "fits the laser bed", dx <= BED[0] and dy <= BED[1], f"{dx:.0f} x {dy:.0f} within {BED[0]:.0f} x {BED[1]:.0f}")
    polys = [p for v in engr.values() for p in v]
    if not polys:
        return
    overl = sum(polys[i].intersection(polys[j]).area for i in range(len(polys)) for j in range(i + 1, len(polys)))
    row(name, "engrave regions do not overlap", overl < 1e-9, f"overlap area {overl:.4f} mm2")
    gap = min((polys[i].distance(polys[j]) for i in range(len(polys)) for j in range(i + 1, len(polys))), default=None)
    row(name, "smallest spacing between engrave regions", gap is not None and gap >= min_gap - 1e-6, f"{gap:.3f} mm (design min {min_gap})")
    thin = [i for i, p in enumerate(polys) if not narrowest_ok(p, min_w)]
    row(name, f"no engrave feature narrower than {min_w} mm", not thin, f"{len(thin)} too-narrow outlines")
    outer = max(cuts, key=lambda p: p.area) if cuts else None
    if outer is not None:
        inner = Polygon(outer.exterior).buffer(-margin)
        holes = [c for c in cuts if c is not outer]
        ok = all(inner.contains(p) for p in polys) and all(p.distance(h) >= margin for p in polys for h in holes)
        row(name, f"engraving inside the cut outline (margin {margin} mm)", ok, "all inside" if ok else "outside or too close")
    return engr


def compare_strip_json():
    g = json.loads((HERE / "strip_v0_1_geometry.json").read_text())
    doc = ezdxf.readfile(HERE / "strip_v0_1.dxf")
    dxf_area = sum(Polygon([tuple(p[:2]) for p in e.get_points()]).area
                   for e in doc.modelspace() if e.dxf.layer == "LIG_ENGRAVE")
    json_area = sum(Polygon(n).area for n in g["nets"].values())
    row("strip_v0_1.dxf", "LIG area matches geometry JSON (CAD source)", abs(dxf_area - json_area) < 0.01,
        f"DXF {dxf_area:.2f} mm2 vs JSON {json_area:.2f} mm2")
    enc = ezdxf.readfile(HERE / "strip_v0_1_encap.dxf")
    outl = max((Polygon([tuple(p[:2]) for p in e.get_points()]) for e in enc.modelspace()), key=lambda p: p.area)
    row("strip_v0_1_encap.dxf", "seal outline matches geometry JSON", abs(outl.area - Polygon(g["seal_outline"]).area) < 0.01,
        f"DXF {outl.area:.2f} mm2 vs JSON {Polygon(g['seal_outline']).area:.2f} mm2")
    union = unary_union([Polygon(n) for n in g["nets"].values()])
    row("strip_v0_1.dxf", "nets are separate pieces", union.geom_type == "MultiPolygon" and len(union.geoms) == len(g["nets"]),
        f"{len(getattr(union, 'geoms', [union]))} pieces for {len(g['nets'])} nets")


def main():
    for name, spec in FILES.items():
        check_file(name, *spec)
    compare_strip_json()
    n_fail = sum(r[2] == "FAIL" for r in ROWS)
    lines = [f"# Laser job file check (verify_laser_files.py, {time.strftime('%Y-%m-%d %H:%M')})", "",
             f"**{sum(r[2] == 'PASS' for r in ROWS)} PASS, {n_fail} FAIL.**",
             "This checks the files only. LaserCAD's colour-to-layer mapping and import scale are checked at the "
             "machine (E2 procedure, step S0-6).", "",
             "| File | Check | Result | Detail |", "|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in ROWS]
    (HERE / "laser_files_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()

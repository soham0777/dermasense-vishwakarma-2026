"""
Independent verification of the SolidWorks CAD v0.1 (does not import sw_build.py).

Expected values are recomputed here from the two sources of truth:
  4_sensor_strip/strip_v0_1_geometry.json  and  5_cad/calc_mechanical.py DIMS.
Checks:
  1 native parts   - re-open each .SLDPRT read-only: MMGS units, volume, bounding box, custom properties
  2 STEP files     - header schema + millimetre units + solid count (text), then SolidWorks re-import volume
  3 assembly       - component count, every component position, interference detection
  4 drawings       - re-open each .SLDDRW (sheet, scale, projection, views); PDF size, title, key dimensions
  5 measured data  - compare the strip design with E2 results (4_sensor_strip/e2_experiment/measured_process.json);
                     BLOCKED until that file exists. Nothing is assumed.
Writes 5_cad/verify_cad_report.md and verify_cad_results.json. Exit code 1 if any check FAILS.
Run with SolidWorks installed:  python verify_cad.py   (add --no-sw for the file-only checks)
"""
import json
import math
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from calc_mechanical import DIMS  # noqa: E402  (numbers only)

G = json.loads((ROOT / "4_sensor_strip" / "strip_v0_1_geometry.json").read_text())
SWD = HERE / "solidworks"
MEASURED = ROOT / "4_sensor_strip" / "e2_experiment" / "measured_process.json"
RESULTS = []


def check(group, item, what, expected, actual, ok, note=""):
    status = ok if isinstance(ok, str) else ("PASS" if ok else "FAIL")
    RESULTS.append(dict(group=group, item=item, check=what, expected=expected, actual=actual, status=status, note=note))
    print(f"[{status:7}] {group} | {item} | {what}: expected {expected}, got {actual} {note}", flush=True)


# ------------------------------------------------------------------ expected geometry (mm)
def area(pts):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))) / 2


def disc(d):
    return math.pi * d * d / 4


P, D = G["parameters"], DIMS
PY0, PY1 = G["paddle_y"]
CX0, CX1 = -D["margin_x"], P["PADDLE_L"] + D["margin_x"] + 2          # clamp footprint
CY0, CY1 = PY0 - D["margin_y"], PY1 + D["margin_y"]
PAD_YS = [p["y"] for p in G["pads"].values()]
CH_X1, CH_Y0, CH_Y1 = P["PAD_X"] + 2.5, min(PAD_YS) - 2.5, max(PAD_YS) + 2.5
XC, YC = G["x_positions"]["C"], P["WIDTH"] / 2
SPACER_T = D["base_h"] - D["dressing_t"] - 0.09
LIG_T, SEAL_T = 0.02, 0.09
side = G["dressing"]["pad"] + 2 * G["dressing"]["border"]
pad = G["dressing"]["pad"]
foot = (CX1 - CX0) * (CY1 - CY0)

EXPECTED = {   # name: (volume mm3, bbox (xmin, ymin, zmin, xmax, ymax, zmax))
    "strip_v0_1": ((area(G["outline"]) - sum(disc(h["d"]) for h in G["holes"])) * D["film_t"]
                   + sum(area(n) for n in G["nets"].values()) * LIG_T,
                   (0, PY0, -LIG_T, G["tip"], PY1, D["film_t"])),
    "seal_v0_1": ((area(G["seal_outline"]) - sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in G["windows"].values())) * SEAL_T,
                  (min(x for x, _ in G["seal_outline"]), 0, 0, G["tip"], P["WIDTH"], SEAL_T)),
    "clamp_base_v0_1": (foot * D["base_h"] - 4 * disc(D["pin_hole_d"]) * D["base_h"] - 2 * disc(D["screw_clear"]) * D["base_h"]
                        - (CH_X1 - CX0) * (CH_Y1 - CH_Y0) * D["channel_h"] + 4 * disc(D["pin_hole_d"]) * D["channel_h"]
                        - 2 * disc(D["dowel_hole_base"]) * (D["dowel_len"] - 2),
                        (CX0, CY0, 0, CX1, CY1, D["base_h"])),
    "clamp_lid_v0_1": ((foot - 2 * disc(D["screw_clear"]) - 2 * disc(D["dowel_hole_lid"])) * D["lid_t"],
                       (CX0, CY0, 0, CX1, CY1, D["lid_t"])),
    "pogo_pin_P75_simplified": (disc(D["pin_d"]) * D["pin_len"],
                                (-D["pin_d"] / 2, -D["pin_d"] / 2, 0, D["pin_d"] / 2, D["pin_d"] / 2, D["pin_len"])),
    "dowel_2x12": (disc(D["dowel_d"]) * D["dowel_len"],
                   (-D["dowel_d"] / 2, -D["dowel_d"] / 2, 0, D["dowel_d"] / 2, D["dowel_d"] / 2, D["dowel_len"])),
    "rig_base_v0_1": ((70 + XC) * 120 * D["rig_t"] - (disc(2.0) + 2 * disc(2.5) + 4 * disc(4.3)) * D["rig_t"],
                      (-10, YC - 60, 0, XC + 60, YC + 60, D["rig_t"])),
    "wound_bed_spacer_v0_1": ((90 * 90 - disc(2.0)) * SPACER_T, (XC - 45, YC - 45, 0, XC + 45, YC + 45, SPACER_T)),
    "dressing_reference_bordered_foam": (pad * pad * D["dressing_t"] + (side * side - pad * pad) * 0.3,
                                         (-side / 2, -side / 2, 0, side / 2, side / 2, D["dressing_t"])),
}
BASE_TOP = -0.02
PLACEMENTS = {  # component -> origin (x, y, z) in the strip frame
    "rig_base_v0_1-1": (0, 0, BASE_TOP - D["base_h"] - D["rig_t"]),
    "wound_bed_spacer_v0_1-1": (0, 0, BASE_TOP - D["base_h"]),
    "dressing_reference_bordered_foam-1": (XC, YC, BASE_TOP - D["base_h"] + SPACER_T),
    "seal_v0_1-1": (0, 0, BASE_TOP - SEAL_T),
    "strip_v0_1-1": (0, 0, 0),
    "clamp_base_v0_1-1": (0, 0, BASE_TOP - D["base_h"]),
    "clamp_lid_v0_1-1": (0, 0, D["film_t"]),
    **{f"pogo_pin_P75_simplified-{i + 1}": (p["x"], p["y"], BASE_TOP - D["pin_len"]) for i, p in enumerate(G["pads"].values())},
    **{f"dowel_2x12-{i + 1}": (h["x"], h["y"], BASE_TOP - (D["dowel_len"] - 2)) for i, h in enumerate(G["holes"])},
}
DRAWINGS = {   # drawing: (title words, scale, key dimension strings that must appear in the PDF)
    "strip_v0_1": ("LIG sensing strip", "1:1", [f"{G['tip']:.2f}", f"{P['WIDTH']:.2f}", f"{D['film_t']:.3f}", f"{P['HOLE_D']:.2f}",
                                                f"{PY1 - PY0:.2f}", f"{P['PADDLE_L']:.2f}"]),
    "seal_v0_1": ("Seal tape", "1:1", [f"{G['tip'] - min(x for x, _ in G['seal_outline']):.2f}", f"{P['WIN_L']:.2f}",
                                       f"{G['windows']['C'][3] - G['windows']['C'][1]:.2f}", f"{SEAL_T:.3f}",
                                       f"{G['windows']['C'][0] - G['windows']['A'][0]:.2f}"]),
    "clamp_base_v0_1": ("Contact clamp", "2:1", [f"{CX1 - CX0:.2f}", f"{CY1 - CY0:.2f}", f"{D['base_h']:.2f}",
                                                 f"{D['pin_hole_d']:.2f}", f"{D['screw_clear']:.2f}", f"{P['PAD_PITCH']:.2f}"]),
    "clamp_lid_v0_1": ("Contact clamp lid", "2:1", [f"{CX1 - CX0:.2f}", f"{D['lid_t']:.2f}", f"{D['dowel_hole_lid']:.2f}"]),
    "rig_base_v0_1": ("Bench rig base", "1:2", ["160.00", "120.00", f"{D['rig_t']:.2f}", "4.30"]),
    "wound_bed_spacer_v0_1": ("Wound-bed spacer", "1:2", ["90.00", f"{SPACER_T:.2f}"]),
    "dermasense_bench_v0_1": ("Bench test", "1:2", ["ITEM NO.", "QTY."]),
}


# ------------------------------------------------------------------ file-only checks
def check_step_text():
    for f in sorted(SWD.glob("*.STEP")):
        txt = f.read_text(errors="replace")
        schema = re.search(r"FILE_SCHEMA\s*\(\s*\(\s*'([^']+)'", txt)
        mm = "SI_UNIT(.MILLI.,.METRE.)" in txt.replace(" ", "")
        solids = len(re.findall(r"MANIFOLD_SOLID_BREP", txt))
        check("2 STEP", f.name, "schema / mm units / solids", "AP2xx, mm, >=1 solid",
              f"{schema.group(1) if schema else '?'}, {'mm' if mm else 'NOT mm'}, {solids}", bool(schema) and mm and solids >= 1)


def check_pdfs():
    import pymupdf
    for name, (title, scale, dims) in DRAWINGS.items():
        f = SWD / f"{name}_drawing.PDF"
        if not f.exists():
            check("4 drawing PDF", f.name, "exists", "file", "missing", False)
            continue
        doc = pymupdf.open(f)
        pg = doc[0]
        w, h = pg.rect.width / 72 * 25.4, pg.rect.height / 72 * 25.4
        text = pg.get_text()
        flat = " ".join(text.split())
        check("4 drawing PDF", f.name, "pages / A3 size", "1 page, 420x297", f"{doc.page_count}, {w:.0f}x{h:.0f}",
              doc.page_count == 1 and abs(w - 420) < 1 and abs(h - 297) < 1)
        need = [title, name, f"SCALE:{scale}", "PROVISIONAL", "First-angle"]
        miss = [s for s in need if s not in flat]
        check("4 drawing PDF", f.name, "title block / scale / notes", ", ".join(need), "all present" if not miss else f"missing {miss}", not miss)
        miss = [s for s in dims if s not in flat]
        check("4 drawing PDF", f.name, "key dimensions shown", ", ".join(dims), "all present" if not miss else f"missing {miss}", not miss)


# ------------------------------------------------------------------ SolidWorks checks
class SWSession:
    def __init__(self):
        import glob
        import importlib
        import os
        import pythoncom
        import win32com.client
        from win32com.client import VARIANT, gencache
        self.pc, self.VARIANT = pythoncom, VARIANT
        pythoncom.CoInitialize()
        self.app = win32com.client.Dispatch("SldWorks.Application")
        self.app.Visible = True
        gp = gencache.GetGeneratePath()
        name = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(gp, "83A33D31*.py"))][0]
        self.mod = importlib.import_module("win32com.gen_py." + name)
        self.app.CloseAllDocuments(True)

    def typed(self, obj, iface):
        cls = getattr(self.mod, iface)
        return cls(obj._oleobj_.QueryInterface(cls.CLSID, self.pc.IID_IDispatch))

    def byref(self):
        return self.VARIANT(self.pc.VT_BYREF | self.pc.VT_I4, 0)

    def open(self, path, kind):
        err, warn = self.byref(), self.byref()
        doc = self.app.OpenDoc6(str(path), kind, 1 | 2, "", err, warn)    # silent + read-only
        return doc, err.value, warn.value

    def volume(self, doc):
        ext = self.typed(doc.Extension, "IModelDocExtension")
        return ext.CreateMassProperty().Volume * 1e9

    def close(self, doc):
        self.app.CloseDoc(doc.GetTitle)


def check_parts(sw):
    for name, (vol_e, box_e) in EXPECTED.items():
        path = SWD / f"{name}.SLDPRT"
        doc, err, _ = sw.open(path, 1)
        if doc is None:
            check("1 part", name, "opens in SolidWorks", "opens", f"error {err}", False)
            continue
        units = doc.Extension.GetUserPreferenceInteger(263, 0)
        check("1 part", name, "unit system", "5 (MMGS)", units, units == 5)
        vol = sw.volume(doc)
        check("1 part", name, "volume mm3", f"{vol_e:.1f}", f"{vol:.1f}", abs(vol - vol_e) <= 0.005 * vol_e + 0.05)
        box = [v * 1000 for v in sw.typed(doc, "IPartDoc").GetPartBox(True)]
        dev = max(abs(a - b) for a, b in zip(box, box_e))
        check("1 part", name, "bounding box mm", tuple(round(v, 3) for v in box_e), tuple(round(v, 3) for v in box), dev < 0.01)
        cpm = doc.Extension.CustomPropertyManager("")
        names = cpm.GetNames                     # a property under late binding
        names = list((names() if callable(names) else names) or [])
        need = ["Description", "Revision", "Material"]
        check("1 part", name, "custom properties", need, names, all(n in names for n in need))
        sw.close(doc)


def check_step_import(sw):
    tmp = Path(tempfile.mkdtemp(prefix="step_check_"))
    for name, (vol_e, _) in EXPECTED.items():
        src = SWD / f"{name}.STEP"
        dst = tmp / src.name
        shutil.copy2(src, dst)           # import from a copy so nothing is written next to the originals
        err = sw.byref()
        doc = sw.app.LoadFile4(str(dst), "r", sw.app.GetImportFileData(str(dst)), err)
        if doc is None:
            check("2 STEP", src.name, "re-imports into SolidWorks", "part", f"error {err.value}", False)
            continue
        vol = sw.volume(doc)
        check("2 STEP", src.name, "re-imported volume mm3", f"{vol_e:.1f}", f"{vol:.1f}", abs(vol - vol_e) <= 0.005 * vol_e + 0.05)
        sw.app.CloseDoc(doc.GetTitle)
    shutil.rmtree(tmp, ignore_errors=True)


def check_assembly(sw):
    doc, err, _ = sw.open(SWD / "dermasense_bench_v0_1.SLDASM", 2)
    if doc is None:
        check("3 assembly", "dermasense_bench_v0_1", "opens", "opens", f"error {err}", False)
        return
    units = doc.Extension.GetUserPreferenceInteger(263, 0)
    check("3 assembly", "dermasense_bench_v0_1", "unit system", "5 (MMGS)", units, units == 5)
    asm = sw.typed(doc, "IAssemblyDoc")
    comps = {c.Name2: c for c in (asm.GetComponents(True) or [])}
    check("3 assembly", "components", "count", len(PLACEMENTS), len(comps), len(comps) == len(PLACEMENTS))
    for cname, xyz in PLACEMENTS.items():
        c = comps.get(cname)
        if c is None:
            check("3 assembly", cname, "present", "present", "missing", False)
            continue
        t = c.Transform2.ArrayData
        got = (t[9] * 1000, t[10] * 1000, t[11] * 1000)
        rot_ok = all(abs(a - b) < 1e-9 for a, b in zip(t[:9], (1, 0, 0, 0, 1, 0, 0, 0, 1)))
        dev = max(abs(a - b) for a, b in zip(got, xyz))
        check("3 assembly", cname, "position mm (no rotation)", tuple(round(v, 3) for v in xyz),
              tuple(round(v, 3) for v in got) + (() if rot_ok else ("ROTATED",)), dev < 0.005 and rot_ok)
    try:
        idm = asm.InterferenceDetectionManager
        idm.TreatCoincidenceAsInterference = False
        idm.IncludeMultibodyPartInterferences = False
        found = []
        for itf in idm.GetInterferences() or []:
            names = sorted(x.Name2 for x in itf.Components)
            found.append((names, itf.Volume * 1e9))
        idm.Done()
        real = [(n, v) for n, v in found if v > 0.001]
        check("3 assembly", "interference", "volume clashes (coincident faces allowed)", "none",
              "; ".join(f"{' x '.join(n)}: {v:.2f} mm3" for n, v in real) or "none", not real)
    except Exception as ex:  # noqa: BLE001
        check("3 assembly", "interference", "interference detection ran", "ran", f"error {ex}", "BLOCKED")
    sw.close(doc)


def check_drawing_files(sw):
    for name, (_, scale, _) in DRAWINGS.items():
        doc, err, warn = sw.open(SWD / f"{name}.SLDDRW", 3)
        if doc is None:
            check("4 drawing", name, "opens", "opens", f"error {err}", False)
            continue
        drw = sw.typed(doc, "IDrawingDoc")
        props = sw.typed(drw.GetCurrentSheet(), "ISheet").GetProperties2()
        views, v = 0, drw.GetFirstView()
        v = sw.typed(v, "IView").GetNextView() if v is not None else None      # first "view" is the sheet
        while v is not None:
            views += 1
            v = sw.typed(v, "IView").GetNextView()
        got = f"{props[2]:g}:{props[3]:g}, {'first' if props[4] else 'third'}-angle, {views} views, sheets {drw.GetSheetCount()}"
        check("4 drawing", f"{name}.SLDDRW", "scale / projection / views", f"{scale}, first-angle, 4 views, sheets 1",
              got, got == f"{scale}, first-angle, 4 views, sheets 1")
        sw.close(doc)


# ------------------------------------------------------------------ measured-data comparison
def check_measured():
    budget_kohm = 10.0                     # [DES] lead resistance <= 10 % of the 100 kOhm wet threshold
    longest_lead = G["x_positions"]["C"] + G["parameters"]["WIN_L"] / 2 - G["parameters"]["PAD_X"]   # mm, pad -> zone C
    if not MEASURED.exists():
        for what in ("trace width F >= smallest reliable LIG line", "as-built gap >= smallest isolating gap",
                     f"lead resistance over {longest_lead:.0f} mm <= {budget_kohm:.0f} kOhm",
                     "laser-cut hole fits the 2.0 mm dowel", "LIG relief vs 0.02 mm CAD assumption"):
            check("5 measured", "strip_v0_1 vs E2", what, "E2 measurement", "no data", "BLOCKED",
                  f"(waiting for {MEASURED.relative_to(ROOT).as_posix()})")
        return
    m = json.loads(MEASURED.read_text())
    if m.get("synthetic") or not str(m.get("status", "")).startswith("MEASURED"):
        check("5 measured", "strip_v0_1 vs E2", "measured_process.json is real data", "MEASURED", m.get("status"), "BLOCKED",
              "(synthetic or incomplete file ignored)")
        return
    grow = m.get("line_growth_mm")
    lw, gap = m.get("min_reliable_line_mm"), m.get("min_isolating_gap_mm")
    F, clear = G["parameters"]["F"], G["parameters"]["MIN_CLEAR"]
    if lw is not None:
        check("5 measured", "strip_v0_1 vs E2", "trace width F >= smallest reliable LIG line", f">= {lw} mm", F, F >= lw)
    if gap is not None and grow is not None:
        built = clear - grow
        check("5 measured", "strip_v0_1 vs E2", "as-built gap >= smallest isolating gap", f">= {gap} mm",
              f"{built:.2f} mm ({clear} drawn - {grow:.2f} growth)", built >= gap)
    rs = (m.get("sheet_resistance_ohm_sq") or {}).get("median")
    if rs is not None:
        w = F + (grow or 0)
        r = rs * longest_lead / w / 1000
        check("5 measured", "strip_v0_1 vs E2", f"lead resistance over {longest_lead:.0f} mm", f"<= {budget_kohm} kOhm", f"{r:.2f} kOhm",
              r <= budget_kohm)
    hole = m.get("cut_hole_d_mm")
    if hole is not None:
        check("5 measured", "strip_v0_1 vs E2", "laser-cut hole fits the 2.0 mm dowel", "2.00 to 2.10 mm", hole, 2.0 <= hole <= 2.10)
    t = m.get("lig_relief_mm")
    if t is not None:
        check("5 measured", "strip_v0_1 vs E2", "LIG relief vs 0.02 mm CAD assumption", "update CAD if > 50 % off", t,
              "INFO" if abs(t - LIG_T) <= 0.5 * LIG_T else "FAIL")


# ------------------------------------------------------------------ report
def write_report(t0):
    counts = {s: sum(r["status"] == s for r in RESULTS) for s in ("PASS", "FAIL", "BLOCKED", "INFO")}
    (HERE / "verify_cad_results.json").write_text(json.dumps(dict(run=time.strftime("%Y-%m-%d %H:%M:%S"), counts=counts,
                                                                  results=RESULTS), indent=1, default=str))
    lines = [f"# CAD verification report (verify_cad.py, {time.strftime('%Y-%m-%d %H:%M')})", "",
             f"**{counts['PASS']} PASS · {counts['FAIL']} FAIL · {counts['BLOCKED']} BLOCKED · {counts['INFO']} INFO** "
             f"(run time {time.time() - t0:.0f} s).",
             "", "Expected values are recomputed from `strip_v0_1_geometry.json` and `calc_mechanical.DIMS`, "
             "not read from the build script. The measured-data checks stay BLOCKED until E2 data exists.", "",
             "| Status | Group | Item | Check | Expected | Actual |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['status']} | {r['group']} | {r['item']} | {r['check']} | {r['expected']} | {r['actual']} {r['note']} |"
              for r in RESULTS]
    (HERE / "verify_cad_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n{counts}")
    return counts


def main():
    t0 = time.time()
    check_step_text()
    check_pdfs()
    if "--no-sw" not in sys.argv:
        sw = SWSession()
        try:
            check_parts(sw)
            check_step_import(sw)
            check_assembly(sw)
            check_drawing_files(sw)
        finally:
            sw.app.CloseAllDocuments(True)
    check_measured()
    counts = write_report(t0)
    sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
    main()

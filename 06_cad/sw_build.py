"""
Build the bench prototype CAD natively in SolidWorks 2019 via its COM API.

Sources of truth: 04_lig_lab/strip_v0_1_geometry.json (strip, pads, holes, windows) and
06_cad/calc_mechanical.py DIMS (clamp, lid, rig). Output: 06_cad/solidworks/ (.SLDPRT/.SLDASM/.SLDDRW,
STEP, PDF drawings, JPG renders) and build_log.txt. Every part is v0.1 PROVISIONAL until E1/E2.

Frames: all manufactured parts use the strip frame (x along the strip from the paddle edge, y across, mm).
Assembly z: Kapton bottom (LIG top) = 0; LIG + seal hang below; clamp base below; lid above.
Run with SolidWorks installed:  python sw_build.py
"""
import glob
import importlib
import json
import os
import sys
import time
from pathlib import Path

import pythoncom
import win32com.client
from win32com.client import VARIANT, gencache

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from calc_mechanical import DIMS  # noqa: E402

GEO = json.loads((HERE.parent / "04_lig_lab" / "strip_v0_1_geometry.json").read_text())
OUT = HERE / "solidworks"
OUT.mkdir(exist_ok=True)
MM = 0.001
NOTHING = VARIANT(pythoncom.VT_DISPATCH, None)
LOG = []


def log(msg):
    LOG.append(msg)
    print(msg, flush=True)


def sw_module():
    gp = gencache.GetGeneratePath()
    names = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(gp, "83A33D31*.py"))]
    if not names:
        raise SystemExit("Run first: python -m win32com.client.makepy \"<SOLIDWORKS>\\sldworks.tlb\"")
    return importlib.import_module("win32com.gen_py." + names[0])


def set_mm(doc):
    """MMGS units, 2 decimals, ISO detailing (the installed template default was CGS)."""
    doc.Extension.SetUserPreferenceInteger(263, 0, 5)     # swUnitSystem = swUnitSystem_MMGS
    doc.Extension.SetUserPreferenceInteger(49, 0, 2)      # swUnitsLinearDecimalPlaces
    doc.Extension.SetUserPreferenceInteger(13, 0, 2)      # swDetailingDimensionStandard = ISO


SHEET_FORMAT = r"C:\ProgramData\SolidWorks\SOLIDWORKS 2019\lang\english\sheetformat\a3 - iso.slddrt"


class SW:
    def __init__(self):
        pythoncom.CoInitialize()
        self.app = win32com.client.Dispatch("SldWorks.Application")
        self.app.Visible = True
        self.mod = sw_module()
        self.prev_dim_dialog = self.app.GetUserPreferenceToggle(10)      # swInputDimValOnCreate
        self.app.SetUserPreferenceToggle(10, False)
        self.tpl = {k: self.app.GetUserPreferenceStringValue(v) for k, v in (("part", 8), ("asm", 9), ("drw", 10))}
        log(f"SolidWorks {self.app.RevisionNumber}; templates {self.tpl}")

    def restore(self):
        self.app.SetUserPreferenceToggle(10, self.prev_dim_dialog)


class Part:
    def __init__(self, sw, name, description, material=None, material_note=""):
        self.sw, self.name = sw, name
        self.m = sw.app.NewDocument(sw.tpl["part"], 0, 0, 0)
        set_mm(self.m)
        self.sm = self.m.SketchManager
        self.fm = self.m.FeatureManager
        self.material, self.description, self.material_note = material, description, material_note
        self.planes = 0
        self.last_sketch = None

    # ---------- sketching
    def sketch(self, plane="Front Plane", ptype="PLANE"):
        self.m.ClearSelection2(True)
        ok = self.m.Extension.SelectByID2(plane, ptype, 0, 0, 0, False, 0, NOTHING, 0)
        if not ok:
            raise RuntimeError(f"cannot select {plane}")
        self.sm.InsertSketch(True)
        self.sm.AddToDB = True

    def end_sketch(self):
        self.sm.AddToDB = False
        self.m.ClearSelection2(True)
        sk = self.sm.ActiveSketch
        self.last_sketch = sk.Name if sk is not None else None
        self.sm.InsertSketch(True)
        self.m.ClearSelection2(True)
        self.m.Extension.SelectByID2(self.last_sketch, "SKETCH", 0, 0, 0, False, 0, NOTHING, 0)

    def plane_at(self, z_mm):
        self.m.ClearSelection2(True)
        self.m.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, NOTHING, 0)
        feat = self.fm.InsertRefPlane(8, abs(z_mm) * MM, 0, 0, 0, 0)
        self.planes += 1
        if feat is None:
            raise RuntimeError("ref plane failed")
        return feat.Name

    def poly(self, pts):
        segs = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            segs.append(self.sm.CreateLine(x0 * MM, y0 * MM, 0, x1 * MM, y1 * MM, 0))
        return segs

    def rect(self, x0, y0, x1, y1):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

    def circle(self, x, y, d):
        return self.sm.CreateCircleByRadius(x * MM, y * MM, 0, d / 2 * MM)

    def hexagon(self, x, y, af):
        r_in = af / 2
        return self.sm.CreatePolygon(x * MM, y * MM, 0, x * MM, (y + r_in) * MM, 0, 6, True)

    # ---------- dimensions (sketch must be open; AddToDB off while dimensioning)
    def dim(self, ents, x, y):
        self.sm.AddToDB = False
        self.m.ClearSelection2(True)
        for i, e in enumerate(ents):
            e.Select4(i > 0, NOTHING)
        d = self.m.AddDimension2(x * MM, y * MM, 0)
        self.m.ClearSelection2(True)
        self.sm.AddToDB = True
        self.dims_ok = getattr(self, "dims_ok", 0) + (d is not None)
        self.dims_tried = getattr(self, "dims_tried", 0) + 1
        return d is not None

    # ---------- features
    def extrude(self, depth_mm, flip=False, merge=True):
        """flip=True reverses the extrusion direction (API argument 'Dir')."""
        f = self.fm.FeatureExtrusion2(True, False, flip, 0, 0, depth_mm * MM, 0, False, False, False, False, 0, 0,
                                      False, False, False, False, merge, True, True, 0, 0, False)
        if f is None:
            raise RuntimeError(f"{self.name}: extrude failed")
        return f

    def cut(self, depth_mm=None, flip=False):
        """Through-all both ways (depth None) or blind; retries the opposite direction if nothing is removed."""
        through = depth_mm is None
        before = self.volume_mm3()
        for direction in ((flip,) if through else (flip, not flip)):
            self.m.ClearSelection2(True)
            self.m.Extension.SelectByID2(self.last_sketch, "SKETCH", 0, 0, 0, False, 0, NOTHING, 0)
            f = self.fm.FeatureCut4(not through, False, direction, 1 if through else 0, 1 if through else 0,
                                    0 if through else depth_mm * MM, 0, False, False, False, False, 0, 0, False,
                                    False, False, False, False, True, True, True, True, False, 0, 0, False, True)
            if f is not None and self.volume_mm3() < before - 1e-6:
                return f
            if f is not None:
                self.m.Extension.SelectByID2(f.Name, "BODYFEATURE", 0, 0, 0, False, 0, NOTHING, 0)
                self.m.EditDelete()
        raise RuntimeError(f"{self.name}: cut removed no material in either direction")

    def volume_mm3(self):
        mod = self.sw.mod
        try:
            ext = mod.IModelDocExtension(self.m.Extension._oleobj_.QueryInterface(mod.IModelDocExtension.CLSID,
                                                                                  pythoncom.IID_IDispatch))
            mp = ext.CreateMassProperty()
            if mp is not None:
                return mp.Volume * 1e9
        except Exception:  # noqa: BLE001
            pass
        props = self.m.GetMassProperties()          # [cx, cy, cz, volume, area, mass, ...] (SI units)
        return props[3] * 1e9 if props else float("nan")

    def color(self, rgb):
        mod = self.sw.mod
        ext = mod.IModelDocExtension(self.m.Extension._oleobj_.QueryInterface(mod.IModelDocExtension.CLSID,
                                                                              pythoncom.IID_IDispatch))
        ext.SetMaterialPropertyValues([rgb[0], rgb[1], rgb[2], 1.0, 1.0, 0.5, 0.4, 0.0, 0.0], 2, None)

    def color_bodies(self, small_rgb, large_rgb, split_mm3=20.0):
        mod = self.sw.mod
        pd = mod.IPartDoc(self.m._oleobj_.QueryInterface(mod.IPartDoc.CLSID, pythoncom.IID_IDispatch))
        for b in pd.GetBodies2(0, False) or []:
            body = mod.IBody2(b._oleobj_.QueryInterface(mod.IBody2.CLSID, pythoncom.IID_IDispatch))
            vol = body.GetMassProperties(1.0)[3] * 1e9
            rgb = small_rgb if vol < split_mm3 else large_rgb
            body.MaterialPropertyValues2 = [rgb[0], rgb[1], rgb[2], 1.0, 1.0, 0.5, 0.4, 0.0, 0.0]

    def hide_planes(self):
        for i in range(1, self.planes + 1):
            self.m.ClearSelection2(True)
            if self.m.Extension.SelectByID2(f"Plane{i}", "PLANE", 0, 0, 0, False, 0, NOTHING, 0):
                self.m.BlankRefGeom()
        self.m.ClearSelection2(True)

    def finish(self, expected_volume=None):
        if self.material:
            pd = self.sw.mod.IPartDoc(self.m._oleobj_.QueryInterface(self.sw.mod.IPartDoc.CLSID, pythoncom.IID_IDispatch))
            pd.SetMaterialPropertyName2("Default", "solidworks materials.sldmat", self.material)
        cpm = self.m.Extension.CustomPropertyManager("")
        for k, v in (("Description", self.description), ("Revision", "v0.1 PROVISIONAL"),
                     ("Project", "Dermasense VK26-IITI-HT-0050"), ("DrawnBy", "sw_build.py (team repo)"),
                     ("MaterialNote", self.material_note or (self.material or ""))):
            cpm.Add3(k, 30, v, 2)
        self.m.ForceRebuild3(False)
        vol = self.volume_mm3()
        path = OUT / f"{self.name}.SLDPRT"
        e1 = self.m.SaveAs3(str(path), 0, 1)
        e2 = self.m.SaveAs3(str(OUT / f"{self.name}.STEP"), 0, 1)
        chk = ""
        if expected_volume:
            chk = f"; expected {expected_volume:.1f} mm3 -> {'OK' if abs(vol - expected_volume) / expected_volume < 0.02 else 'MISMATCH'}"
        log(f"PART {self.name}: volume {vol:.1f} mm3{chk}; sketch dims {getattr(self, 'dims_ok', 0)}/"
            f"{getattr(self, 'dims_tried', 0)}; save {e1}, STEP {e2}")
        return path


# ------------------------------------------------------------------ parts
def build_strip(sw):
    p = Part(sw, "strip_v0_1", "LIG moisture-front strip v0.1 (two-zone)", None,
             "Polyimide (Kapton-type) film 0.125 mm; LIG 0.02 mm (thickness assumed)")
    t, lig = DIMS["film_t"], 0.02
    p.sketch()
    outline = GEO["outline"]
    segs = p.poly(outline)
    holes = [p.circle(h["x"], h["y"], h["d"]) for h in GEO["holes"]]
    left = segs[-1]                    # x = 0 paddle edge
    tip = segs[3]                      # x = tip edge
    p.dim([tip], GEO["tip"] + 4, 5)                                   # body width
    p.dim([left, tip], GEO["tip"] / 2, GEO["paddle_y"][0] - 6)        # overall length
    p.dim([left], -6, 5)                                              # paddle height
    for h, c in zip(GEO["holes"], holes):
        p.dim([c], h["x"] + 4, h["y"] + 3)
        p.dim([c, left], h["x"] / 2, h["y"] + 2)
    p.end_sketch()
    p.extrude(t)
    v_kapton = p.volume_mm3()
    p.sketch()
    for name, pts in GEO["nets"].items():
        p.poly(pts)
    p.end_sketch()
    p.extrude(lig, flip=True, merge=False)
    p.color_bodies((0.08, 0.08, 0.08), (0.93, 0.62, 0.18))
    log(f"strip: Kapton volume {v_kapton:.1f} mm3; LIG bodies extruded {lig} mm down (LIG faces the pad)")
    return p.finish()


def build_seal(sw):
    p = Part(sw, "seal_v0_1", "Polyimide-tape seal with zone windows C and A", None,
             "Polyimide adhesive tape ~0.09 mm (assumed); cut from strip_v0_1_encap.dxf")
    p.sketch()
    p.poly(GEO["seal_outline"])
    for z, (x0, y0, x1, y1) in GEO["windows"].items():
        p.rect(x0, y0, x1, y1)
    p.end_sketch()
    p.extrude(0.09)
    p.color((0.85, 0.55, 0.15))
    return p.finish()


def clamp_extent():
    y_lo, y_hi = GEO["paddle_y"]
    x0, x1 = -DIMS["margin_x"], GEO["parameters"]["PADDLE_L"] + DIMS["margin_x"] + 2
    return x0, x1, y_lo - DIMS["margin_y"], y_hi + DIMS["margin_y"]


def screw_points():
    y_lo, y_hi = GEO["paddle_y"]
    xs = GEO["parameters"]["PAD_X"]
    return [(xs, y_lo - DIMS["margin_y"] / 2), (xs, y_hi + DIMS["margin_y"] / 2)]


def build_clamp_base(sw):
    d = DIMS
    p = Part(sw, "clamp_base_v0_1", "Contact clamp base: 4 pogo pins + 2 dowels", "ABS",
             "Print in PETG; ABS properties used as the closest SOLIDWORKS 2019 library material")
    x0, x1, y0, y1 = clamp_extent()
    p.sketch()
    s = p.rect(x0, y0, x1, y1)
    p.dim([s[0]], (x0 + x1) / 2, y0 - 4)
    p.dim([s[1]], x1 + 4, (y0 + y1) / 2)
    p.end_sketch()
    p.extrude(d["base_h"])
    v0 = p.volume_mm3()
    # through holes: pogo pins + M3 screws
    p.sketch()
    pins = [p.circle(pad["x"], pad["y"], d["pin_hole_d"]) for pad in GEO["pads"].values()]
    screws = [p.circle(x, y, d["screw_clear"]) for x, y in screw_points()]
    ref = p.rect(x0, y0, x1, y1)                       # construction reference for location dims
    for seg in ref:
        seg.ConstructionGeometry = True
    pc, pa = GEO["pads"]["SENSE_C"], GEO["pads"]["SENSE_A"]
    p.dim([pins[0], ref[3]], (x0 + pc["x"]) / 2, pc["y"] - 4)
    p.dim([pins[0], ref[0]], x0 - 3, (y0 + pc["y"]) / 2)
    p.dim([pins[0], pins[1]], pc["x"] - 6, (pc["y"] + pa["y"]) / 2)
    p.dim([screws[0], ref[0]], x1 + 3, (y0 + screw_points()[0][1]) / 2)
    p.dim([pins[0]], GEO["pads"]["SENSE_C"]["x"] + 3, GEO["pads"]["SENSE_C"]["y"] - 2)
    p.dim([screws[0]], screw_points()[0][0] + 5, screw_points()[0][1])
    p.end_sketch()
    p.cut(None)
    # wire channel from the bottom
    ys = [pad["y"] for pad in GEO["pads"].values()]
    p.sketch()
    p.rect(x0, min(ys) - 2.5, GEO["parameters"]["PAD_X"] + 2.5, max(ys) + 2.5)
    p.end_sketch()
    p.cut(d["channel_h"])
    # dowel blind holes from the top
    plane = p.plane_at(d["base_h"])
    p.sketch(plane)
    for h in GEO["holes"]:
        p.circle(h["x"], h["y"], d["dowel_hole_base"])
    p.end_sketch()
    p.cut(d["dowel_len"] - 2.0, flip=True)
    p.color((0.20, 0.45, 0.75))
    p.hide_planes()
    log(f"clamp base: block {v0:.0f} mm3 before cuts")
    return p.finish()


def build_lid(sw):
    d = DIMS
    p = Part(sw, "clamp_lid_v0_1", "Contact clamp lid (presses paddle onto pins)", "ABS",
             "Print in PETG; ABS properties used as stand-in")
    x0, x1, y0, y1 = clamp_extent()
    p.sketch()
    s = p.rect(x0, y0, x1, y1)
    p.dim([s[0]], (x0 + x1) / 2, y0 - 4)
    p.dim([s[1]], x1 + 4, (y0 + y1) / 2)
    for x, y in screw_points():
        c = p.circle(x, y, d["screw_clear"])
    p.dim([c], x + 5, y)
    p.dim([c, s[3]], (x0 + x) / 2, y + 3)
    p.dim([c, s[2]], x1 + 3, (y + y1) / 2)
    for h in GEO["holes"]:
        c2 = p.circle(h["x"], h["y"], d["dowel_hole_lid"])
    p.dim([c2], GEO["holes"][-1]["x"] + 4, GEO["holes"][-1]["y"] + 2)
    p.dim([c2, s[2]], x1 + 6, (GEO["holes"][-1]["y"] + y1) / 2)
    p.end_sketch()
    p.extrude(d["lid_t"])
    p.color((0.20, 0.45, 0.75))
    return p.finish()


def build_pin(sw):
    d = DIMS
    p = Part(sw, "pogo_pin_P75_simplified", "Spring probe P75-B1 (purchased; simplified envelope)", None,
             "Purchased part: Probots/Hubtronics P75-B1; dims per seller listing (verify)")
    p.sketch(); c = p.circle(0, 0, d["pin_d"]); p.dim([c], 2, 2); p.end_sketch()
    p.extrude(d["pin_len"])
    p.color((0.85, 0.75, 0.30))
    return p.finish()


def build_dowel(sw):
    d = DIMS
    p = Part(sw, "dowel_2x12", "Dowel pin 2 m6 x 12 (purchased)", "AISI 304", "ISO 8734 / ISO 2338 stainless")
    p.sketch(); c = p.circle(0, 0, d["dowel_d"]); p.dim([c], 2, 2); p.end_sketch()
    p.extrude(d["dowel_len"])
    return p.finish()


def rig_frame():
    xc, yc = GEO["x_positions"]["C"], GEO["parameters"]["WIDTH"] / 2
    return xc, yc


def build_rig_base(sw):
    d = DIMS
    xc, yc = rig_frame()
    p = Part(sw, "rig_base_v0_1", "Bench dressing rig base plate (laser-cut acrylic)",
             "Acrylic (Medium-high impact)", "Cast acrylic 5 mm, laser-cut")
    x0, x1, y0, y1 = -10.0, xc + 60.0, yc - 60.0, yc + 60.0
    p.sketch()
    s = p.rect(x0, y0, x1, y1)
    p.dim([s[0]], (x0 + x1) / 2, y0 - 6)
    p.dim([s[1]], x1 + 6, yc)
    inlet = p.circle(xc, yc, 2.0)
    p.dim([inlet], xc + 6, yc + 4)
    p.dim([inlet, s[3]], (x0 + xc) / 2, yc + 6)
    for x, y in screw_points():
        tap = p.circle(x, y, 2.5)               # M3 tap drill
    p.dim([tap], x + 5, y + 4)
    p.dim([tap, s[3]], (x0 + x) / 2, y + 6)
    p.dim([tap, s[0]], x - 8, (y0 + y) / 2)
    for x, y in ((x0 + 6, y0 + 6), (x1 - 6, y0 + 6), (x1 - 6, y1 - 6), (x0 + 6, y1 - 6)):
        p.circle(x, y, 4.3)                     # M4 feet
    p.end_sketch()
    p.extrude(d["rig_t"])
    return p.finish()


def spacer_t():
    """Spacer top = dressing bottom, so the dressing top meets the seal (z = -0.11) and the clamp top (z = -0.02)."""
    return DIMS["base_h"] - DIMS["dressing_t"] - 0.09


def build_spacer(sw):
    xc, yc = rig_frame()
    p = Part(sw, "wound_bed_spacer_v0_1", "Wound-bed spacer under the dressing (2 x 6 mm acrylic)",
             "Acrylic (Medium-high impact)", "Two laser-cut 6 mm acrylic sheets; shim to dressing thickness")
    p.sketch()
    s = p.rect(xc - 45, yc - 45, xc + 45, yc + 45)
    p.dim([s[0]], xc, yc - 50)
    p.dim([s[1]], xc + 50, yc)
    c = p.circle(xc, yc, 2.0)
    p.dim([c], xc + 5, yc + 5)
    p.dim([c, s[3]], xc - 20, yc + 4)
    p.dim([c, s[0]], xc + 4, yc - 20)
    p.end_sketch()
    p.extrude(spacer_t())
    return p.finish()


def build_dressing(sw):
    pad, border = GEO["dressing"]["pad"], GEO["dressing"]["border"]
    side = pad + 2 * border
    p = Part(sw, "dressing_reference_bordered_foam", "Reference geometry of a bordered foam dressing (not ours)", None,
             "Purchased dressing; pad/border sizes = test dressing (confirm)")
    p.sketch(); p.rect(-side / 2, -side / 2, side / 2, side / 2); p.end_sketch(); p.extrude(0.3)
    p.sketch(); p.rect(-pad / 2, -pad / 2, pad / 2, pad / 2); p.end_sketch(); p.extrude(DIMS["dressing_t"])
    p.color((0.97, 0.94, 0.86))
    return p.finish()


# ------------------------------------------------------------------ assembly
def build_assembly(sw, parts):
    a = sw.app.NewDocument(sw.tpl["asm"], 0, 0, 0)
    title = a.GetTitle
    asm = sw.mod.IAssemblyDoc(a._oleobj_.QueryInterface(sw.mod.IAssemblyDoc.CLSID, pythoncom.IID_IDispatch))
    err = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    xc, yc = rig_frame()
    base_top = -0.02
    placements = [  # (part key, x, y, z of the part origin in the strip frame)
        ("rig_base_v0_1", 0, 0, base_top - DIMS["base_h"] - DIMS["rig_t"]),
        ("wound_bed_spacer_v0_1", 0, 0, base_top - DIMS["base_h"]),
        ("dressing_reference_bordered_foam", xc, yc, base_top - DIMS["base_h"] + spacer_t()),
        ("seal_v0_1", 0, 0, -0.11),
        ("strip_v0_1", 0, 0, 0.0),
        ("clamp_base_v0_1", 0, 0, base_top - DIMS["base_h"]),
        ("clamp_lid_v0_1", 0, 0, DIMS["film_t"]),
    ] + [("pogo_pin_P75_simplified", pad["x"], pad["y"], base_top - DIMS["pin_len"]) for pad in GEO["pads"].values()] \
      + [("dowel_2x12", h["x"], h["y"], base_top - (DIMS["dowel_len"] - 2.0)) for h in GEO["holes"]]
    report = []
    for i, (key, x, y, z) in enumerate(placements):
        path = str(parts[key])
        sw.app.OpenDoc6(path, 1, 1, "", err, err)
        sw.app.ActivateDoc3(title, False, 0, err)
        comp = asm.AddComponent5(path, 0, "", False, "", x * MM, y * MM, z * MM)
        if comp is None:
            report.append(f"{key}: insert FAILED")
            continue
        cname = comp.Name2
        if i == 0:                                   # SolidWorks fixes the first component; let mates place it
            a.ClearSelection2(True)
            comp.Select4(False, None, False)
            a.UnfixComponent()
            a.ClearSelection2(True)
        mates, mate_objs = 0, {}
        for plane, axis, val in (("Right Plane", 0, x), ("Top Plane", 1, y), ("Front Plane", 2, z)):
            a.ClearSelection2(True)
            ok1 = a.Extension.SelectByID2(f"{plane}@{cname}@{title.replace('.SLDASM', '')}", "PLANE", 0, 0, 0, False, 1, NOTHING, 0)
            ok2 = a.Extension.SelectByID2(plane, "PLANE", 0, 0, 0, True, 1, NOTHING, 0)
            if not (ok1 and ok2):
                continue
            if abs(val) < 1e-9:
                mate = asm.AddMate5(0, 0, False, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0)
            else:
                mate = asm.AddMate5(5, 0, False, abs(val) * MM, abs(val) * MM, abs(val) * MM, 0, 0, 0, 0, 0,
                                    False, False, 0)
            if isinstance(mate, tuple):
                mate = mate[0]
            if mate is not None:
                mates += 1
                if abs(val) >= 1e-9:
                    mate_objs[axis] = mate
        a.ClearSelection2(True)
        a.ForceRebuild3(False)
        t = comp.Transform2.ArrayData
        got = (t[9] / MM, t[10] / MM, t[11] / MM)
        fixed = ""
        for k, (g, w) in enumerate(zip(got, (x, y, z))):
            if abs(g - w) > 0.01 and k in mate_objs:
                mobj = sw.mod.IMate2(mate_objs[k]._oleobj_.QueryInterface(sw.mod.IMate2.CLSID, pythoncom.IID_IDispatch))
                mobj.Flipped = not mobj.Flipped
                fixed += f" flipped axis {k};"
        if fixed:
            a.ForceRebuild3(False)
            t = comp.Transform2.ArrayData
            got = (t[9] / MM, t[10] / MM, t[11] / MM)
        if max(abs(g - w) for g, w in zip(got, (x, y, z))) > 0.01:
            fixed += " STILL OFF TARGET"
        report.append(f"{cname}: {mates} mates; position {tuple(round(v, 3) for v in got)} vs target "
                      f"{(round(x, 3), round(y, 3), round(z, 3))}{fixed}")
    a.ForceRebuild3(False)
    a.ShowNamedView2("*Isometric", 7)
    a.ViewZoomtofit2()
    path = OUT / "dermasense_bench_v0_1.SLDASM"
    e = a.SaveAs3(str(path), 0, 1)
    a.SaveAs3(str(OUT / "dermasense_bench_v0_1.STEP"), 0, 1)
    for r in report:
        log("  " + r)
    log(f"ASSEMBLY saved {e}: {path.name}")
    return a, path, report


# ------------------------------------------------------------------ drawings and renders
def make_drawing(sw, model_path, name, scale=(1, 1)):
    err = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    doc_type = 2 if str(model_path).upper().endswith(".SLDASM") else 1
    model = sw.app.OpenDoc6(str(model_path), doc_type, 1, "", err, err)
    d = sw.app.NewDocument(sw.tpl["drw"], 8, 0.420, 0.297)
    set_mm(d)
    drw = sw.mod.IDrawingDoc(d._oleobj_.QueryInterface(sw.mod.IDrawingDoc.CLSID, pythoncom.IID_IDispatch))
    fmt_ok = drw.SetupSheet5("Sheet1", 8, 12, scale[0], scale[1], False, SHEET_FORMAT, 0.420, 0.297, "Default", True)
    ok = d.Create3rdAngleViews2(str(model_path))
    try:
        d.CreateDrawViewFromModelView3(str(model_path), "*Isometric", 0.33, 0.20, 0)
    except Exception as ex:  # noqa: BLE001
        log(f"  iso view failed for {name}: {ex}")
    anns = d.InsertModelAnnotations3(0, 32768, True, True, False, False)
    n = 0 if anns is None else len(anns)
    d.ForceRebuild3(False)
    e1 = d.SaveAs3(str(OUT / f"{name}.SLDDRW"), 0, 1)
    e2 = d.SaveAs3(str(OUT / f"{name}_drawing.PDF"), 0, 1)
    log(f"DRAWING {name}: A3 ISO sheet {fmt_ok}, scale {scale[0]}:{scale[1]}, views {ok}, "
        f"imported dimensions {n}, save {e1}, PDF {e2}")
    sw.app.CloseDoc(d.GetTitle)
    if model is not None:
        sw.app.CloseDoc(model.GetTitle)
    return n


def render(sw, doc, name, side=False):
    import math
    doc.ShowNamedView2("*Front", 1)
    view = doc.ActiveView
    view.RotateAboutCenter(math.radians(-55), 0)
    view.RotateAboutCenter(0, math.radians(-35))
    doc.ViewZoomtofit2()
    e = doc.SaveAs3(str(OUT / f"{name}_iso.JPG"), 0, 1)
    log(f"RENDER {name}_iso.JPG: {e}")
    if side:
        doc.ShowNamedView2("*Front", 1)
        doc.ActiveView.RotateAboutCenter(math.radians(-90), 0)
        doc.ViewZoomtofit2()
        e = doc.SaveAs3(str(OUT / f"{name}_side.JPG"), 0, 1)
        log(f"RENDER {name}_side.JPG: {e}")


PART_BUILDERS = (build_strip, build_seal, build_clamp_base, build_lid, build_pin, build_dowel, build_rig_base,
                 build_spacer, build_dressing)
DRAWN = ("strip_v0_1", "seal_v0_1", "clamp_base_v0_1", "clamp_lid_v0_1", "rig_base_v0_1", "wound_bed_spacer_v0_1")


def main(stages=("parts", "drawings", "assembly")):
    t0 = time.time()
    sw = SW()
    try:
        parts = {}
        if "parts" in stages:
            for fn in PART_BUILDERS:
                path = fn(sw)
                parts[path.stem] = path
            sw.app.CloseAllDocuments(True)
        else:
            parts = {f.stem: f for f in OUT.glob("*.SLDPRT")}
        if "drawings" in stages:
            for key in DRAWN:
                make_drawing(sw, parts[key], key, (1, 1) if key.startswith(("clamp", "seal", "strip")) else (1, 2))
            for key in ("strip_v0_1", "clamp_base_v0_1", "clamp_lid_v0_1"):
                err = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
                doc = sw.app.OpenDoc6(str(parts[key]), 1, 1, "", err, err)
                render(sw, doc, key)
                sw.app.CloseDoc(doc.GetTitle)
        if "assembly" in stages:
            a, apath, _ = build_assembly(sw, parts)
            render(sw, a, "dermasense_bench_v0_1", side=True)
            sw.app.CloseAllDocuments(True)
            make_drawing(sw, apath, "dermasense_bench_v0_1", (1, 2))
        sw.app.CloseAllDocuments(True)
    finally:
        sw.restore()
        log(f"done in {time.time() - t0:.0f} s")
        with open(OUT / "build_log.txt", "a", encoding="utf-8") as fh:
            fh.write(f"--- run {time.strftime('%Y-%m-%d %H:%M:%S')} stages={stages}\n" + "\n".join(LOG) + "\n")


if __name__ == "__main__":
    main(tuple(sys.argv[1:]) or ("parts", "drawings", "assembly"))

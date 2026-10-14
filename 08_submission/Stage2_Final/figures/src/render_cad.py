"""
Presentation renders of the verified SolidWorks v0.1 models (06_cad/solidworks). Read-only: no CAD file is changed.

  cad_assembly_iso.png   assembled bench prototype, colour-coded parts, white background
  cad_exploded_iso.png   exploded stack built in a temporary in-memory assembly (never saved) from the same parts,
                         using the verified component positions (06_cad/verify_cad.py PLACEMENTS) + vertical offsets
  cad_clamp_closeup.png  contact clamp: translucent lid over the strip paddle, pogo pins, dowels
  sw_ui_assembly.png     screenshot of the SolidWorks window with the FeatureManager tree (authenticity evidence)
SolidWorks system options touched (background colour/appearance, window state) are saved first and restored.
Run with SolidWorks 2019 installed:  python render_cad.py
"""
import ctypes
import math
import shutil
import sys
import tempfile
import time
from pathlib import Path

import pythoncom
import win32gui
import win32ui
from PIL import Image, ImageChops
from win32com.client import VARIANT

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
ROOT = HERE.parents[3]
NATIVE = ROOT / "06_cad" / "solidworks"
sys.path.insert(0, str(ROOT / "06_cad"))
from verify_cad import PLACEMENTS, SWSession  # noqa: E402

MM = 0.001
COLORS = {  # part -> (r, g, b, transparency)
    "rig_base_v0_1": (0.80, 0.90, 0.95, 0.55), "wound_bed_spacer_v0_1": (0.70, 0.84, 0.90, 0.45),
    "dressing_reference_bordered_foam": (0.97, 0.92, 0.78, 0.0), "seal_v0_1": (0.95, 0.60, 0.15, 0.35),
    "clamp_base_v0_1": (0.16, 0.42, 0.78, 0.0), "clamp_lid_v0_1": (0.45, 0.70, 0.95, 0.55),
    "pogo_pin_P75_simplified": (0.90, 0.72, 0.20, 0.0), "dowel_2x12": (0.62, 0.64, 0.68, 0.0),
}
EXPLODE_DZ = {"rig_base_v0_1": -40, "wound_bed_spacer_v0_1": -24, "clamp_base_v0_1": -24, "pogo_pin_P75_simplified": -12,
              "dowel_2x12": -12, "dressing_reference_bordered_foam": -12, "seal_v0_1": 0, "strip_v0_1": 8, "clamp_lid_v0_1": 22}


def arr(vals):
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(vals))


def appearance(rgb_t):
    r, g, b, t = rgb_t
    return arr([r, g, b, 1.0, 1.0, 0.25, 0.3, t, 0.30])   # some emission: the top lights are dim


def crop_white(path_in, path_out, pad=24):
    im = Image.open(path_in).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if box:
        box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height))
        im = im.crop(box)
    im.save(path_out)
    return im.size


def view_iso(doc):
    doc.ShowNamedView2("*Front", 1)
    v = doc.ActiveView
    v.RotateAboutCenter(math.radians(-58), 0)
    v.RotateAboutCenter(0, math.radians(-32))
    doc.ViewZoomtofit2()


def colored_copies(sw):
    """Copy the native parts + assembly to a temp folder and colour the COPIES at body level.
    (In sw_build.py the part colour is set before the material is assigned, so material parts show the material's grey;
    the frozen CAD is left as verified.)"""
    tmp = Path(tempfile.mkdtemp(prefix="cad_render_"))
    for f in list(NATIVE.glob("*.SLDPRT")) + [NATIVE / "dermasense_bench_v0_1.SLDASM"]:
        shutil.copy2(f, tmp / f.name)
    for base, rgbt in COLORS.items():
        doc, err, _ = sw.open(tmp / f"{base}.SLDPRT", 1)
        if doc is None:
            sw.open  # keep going: an uncoloured part is still a true render
            continue
        pd = sw.typed(doc, "IPartDoc")
        for b in pd.GetBodies2(0, False) or []:
            sw.typed(b, "IBody2").MaterialPropertyValues2 = appearance(rgbt)
        doc.ForceRebuild3(False)
        doc.SaveAs3(str(tmp / f"{base}.SLDPRT"), 0, 1)
        sw.app.CloseDoc(doc.GetTitle)
    return tmp


def tidy(doc):
    doc.Extension.SetUserPreferenceToggle(198, 0, True)       # hide planes, origins, sketches
    doc.GraphicsRedraw2()


def snap(sw, doc, name):
    tmp = FIG / f"_{name}.jpg"
    doc.SaveAs3(str(tmp), 0, 1)
    size = crop_white(tmp, FIG / f"{name}.png")
    tmp.unlink()
    print(f"{name}.png {size}", flush=True)


def window_capture(title_part, out):
    hits = []
    win32gui.EnumWindows(lambda h, _: hits.append(h) if title_part in win32gui.GetWindowText(h) and win32gui.IsWindowVisible(h) else None, None)
    if not hits:
        print("SolidWorks window not found")
        return
    h = hits[0]
    l, t, r, b = win32gui.GetWindowRect(h)
    w, hgt = r - l, b - t
    hdc = win32gui.GetWindowDC(h)
    mdc = win32ui.CreateDCFromHandle(hdc)
    sdc = mdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(mdc, w, hgt)
    sdc.SelectObject(bmp)
    ctypes.windll.user32.PrintWindow(h, sdc.GetSafeHdc(), 2)   # PW_RENDERFULLCONTENT: works even if covered
    info = bmp.GetInfo()
    im = Image.frombuffer("RGB", (info["bmWidth"], info["bmHeight"]), bmp.GetBitmapBits(True), "raw", "BGRX", 0, 1)
    im.save(out)
    win32gui.DeleteObject(bmp.GetHandle())
    sdc.DeleteDC()
    mdc.DeleteDC()
    win32gui.ReleaseDC(h, hdc)
    print(f"{out.name} {im.size}", flush=True)


def exploded(sw, parts_dir):
    a = sw.app.NewDocument(sw.app.GetUserPreferenceStringValue(9), 0, 0, 0)
    asm = sw.typed(a, "IAssemblyDoc")
    title = a.GetTitle
    err = sw.byref()
    math_util = sw.typed(sw.typed(sw.app, "ISldWorks").GetMathUtility(), "IMathUtility")
    for cname, (x, y, z) in PLACEMENTS.items():
        base = cname.rsplit("-", 1)[0]
        path = str(parts_dir / f"{base}.SLDPRT")
        sw.app.OpenDoc6(path, 1, 1 | 2, "", err, err)
        sw.app.ActivateDoc3(title, False, 0, err)
        comp = asm.AddComponent5(path, 0, "", False, "", 0, 0, 0)
        a.ClearSelection2(True)
        comp.Select4(False, None, False)
        a.UnfixComponent()
        z2 = z + EXPLODE_DZ.get(base, 0)
        xf = math_util.CreateTransform(arr([1, 0, 0, 0, 1, 0, 0, 0, 1, x * MM, y * MM, z2 * MM, 1, 0, 0, 0]))
        sw.typed(comp, "IComponent2").Transform2 = xf
    a.ClearSelection2(True)
    a.ForceRebuild3(False)
    return a


def main():
    sw = SWSession()
    app = sw.app
    saved = {k: app.GetUserPreferenceIntegerValue(k) for k in (305, 99)}
    frame = app.FrameState
    try:
        app.SetUserPreferenceIntegerValue(305, 0)              # background appearance: plain
        app.SetUserPreferenceIntegerValue(99, 0xFFFFFF)        # viewport background: white
        app.FrameState = 1                                     # maximised window -> larger image
        time.sleep(1)
        doc, err, _ = sw.open(NATIVE / "dermasense_bench_v0_1.SLDASM", 2)     # native files: UI screenshot
        tidy(doc)
        doc.ShowNamedView2("*Isometric", 7)
        doc.ViewZoomtofit2()
        doc.GraphicsRedraw2()
        time.sleep(1.5)
        window_capture("SOLIDWORKS", FIG / "sw_ui_assembly.png")
        app.CloseAllDocuments(True)
        tmp = colored_copies(sw)
        doc, err, _ = sw.open(tmp / "dermasense_bench_v0_1.SLDASM", 2)
        tidy(doc)
        view_iso(doc)
        snap(sw, doc, "cad_assembly_iso")
        view_iso(doc)
        doc.ViewZoomTo2(-0.020, -0.045, -0.025, 0.075, 0.050, 0.010)
        snap(sw, doc, "cad_clamp_closeup")
        app.CloseAllDocuments(True)
        ex = exploded(sw, tmp)
        tidy(ex)
        view_iso(ex)
        snap(sw, ex, "cad_exploded_iso")
    finally:
        app.CloseAllDocuments(True)                            # nothing is saved
        for k, v in saved.items():
            app.SetUserPreferenceIntegerValue(k, v)
        app.FrameState = frame
        print("SolidWorks options restored", flush=True)


if __name__ == "__main__":
    main()

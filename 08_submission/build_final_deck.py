"""
Build the FINAL Stage 2 deck on the official Vishwakarma template (Template (2), never edited in place).

Template rule followed: sections in the template's order and within its slide limits; every content slide reuses the
template's own example-slide design for that section (background, logos, title position, panels, icons, rationale
bar). The guideline-only instruction slides are dropped, as the template intends; their requirements are mapped
slide by slide in Stage2_Final/PPT_Asset_Index.md.

  1 Application ID (cover)            2 Problem Context                3-4 User Journey (before / after)
  5-6 System Architecture & Specs      7-8 CAD Design & Mechanical      9-10 Electronics Schematics & BOM
  11-12 Maker Journey                  13 Safety & Hazard Mitigation    14 Roadmap
  15 Technical Challenges & Risks      16 Potential Solutions & Risk Mitigation
  17 References & Sources              18 Image Sources

Evidence discipline: every slide carries one status pill (green = completed & verified in software or by source,
amber = designed / physical validation pending, grey = future scope, blue = research or documented decision).
Numbers come from project files or cited sources; targets are called targets.
Run:  python Stage2_Final/figures/src/render_cad.py  (SolidWorks)  ->  make_final_figures.py  ->  this script
"""
import csv
import re
from copy import deepcopy
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATE = HERE / "template" / "Vishwakarma Awards 2026-27 Stage 2 Submission Template (2).pptx"
OUTDIR = HERE / "Stage2_Final"
OUT = OUTDIR / "Vishwakarma_Stage2_Final.pptx"
FIG = OUTDIR / "figures"

NAVY, BODY, MUTED, GREEN, BLUE = "0F172A", "334155", "64748B", "059669", "0369A1"
PILL = {"green": ("047857", "D1FAE5"), "amber": ("B45309", "FEF3C7"), "grey": ("475569", "E2E8F0"), "blue": ("0369A1", "E0F2FE")}
TITLE_FONT, BODY_FONT = "Poppins SemiBold", "DM Sans"
SUP = dict(zip(range(1, 14), "¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ¹⁰ ¹¹ ¹² ¹³".split()))
NOTES = {}


# ================================================================== low-level helpers
def by_id(slide, sid):
    for sh in slide.shapes:
        if sh.shape_id == sid:
            return sh
    raise KeyError(sid)


def delete(slide, *sids):
    for sid in sids:
        el = by_id(slide, sid)._element
        el.getparent().remove(el)


def move(slide, sid, x=None, y=None, w=None, h=None):
    sh = by_id(slide, sid)
    if x is not None:
        sh.left = Inches(x)
    if y is not None:
        sh.top = Inches(y)
    if w is not None:
        sh.width = Inches(w)
    if h is not None:
        sh.height = Inches(h)
    return sh


def runs(p, parts, size, color=BODY, font=BODY_FONT):
    """parts: list of (text, bold[, color]) appended as runs to paragraph p."""
    for part in parts:
        text, bold = part[0], part[1]
        col = part[2] if len(part) > 2 else color
        r = p.add_run()
        r.text = text
        f = r.font
        f.size = Pt(size)
        f.bold = bold
        f.name = font
        f.color.rgb = RGBColor.from_string(col)


def textbox(slide, x, y, w, h, paras, size=10.0, color=BODY, font=BODY_FONT, align=None, space=4, anchor=MSO_ANCHOR.TOP,
            bullets=False, line=1.08):
    """paras: list of paragraphs; a paragraph is a str or a list of (text, bold[, color]) runs."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = anchor
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        parts = [(para, False)] if isinstance(para, str) else list(para)
        if bullets:
            parts = [("▪  ", False, GREEN)] + parts
        runs(p, parts, size, color, font)
        p.space_after = Pt(space)
        p.line_spacing = line
        if align:
            p.alignment = align
    return tb


def set_text(shape, paras, size, color=BODY, font=BODY_FONT, align=None):
    tf = shape.text_frame
    body = tf._txBody
    for p in body.findall(qn("a:p"))[1:]:
        body.remove(p)
    p0 = tf.paragraphs[0]
    for r in list(p0.runs):
        r._r.getparent().remove(r._r)
    for i, para in enumerate(paras):
        p = p0 if i == 0 else tf.add_paragraph()
        parts = [(para, False)] if isinstance(para, str) else list(para)
        runs(p, parts, size, color, font)
        if align:
            p.alignment = align
    return shape


def title(slide, sid, text):
    sh = by_id(slide, sid)
    set_text(sh, [[(text, False)]], 20.25, NAVY, TITLE_FONT)
    sh.width = Inches(9.4)


def pill(slide, text, kind):
    fg, bg = PILL[kind]
    w = 0.30 + 0.068 * len(text)
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.75 - w), Inches(0.50), Inches(w), Inches(0.27))
    shp.adjustments[0] = 0.5
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGBColor.from_string(bg)
    shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    runs(p, [(text, True)], 7.5, fg, BODY_FONT)
    return shp


def picture_in(slide, path, x, y, w, h, frame=None):
    """Add an image scaled to fit (x, y, w, h) inches, centred; optionally resize a template frame around it."""
    from PIL import Image
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    px, py = x + (w - pw) / 2, y + (h - ph) / 2
    pic = slide.shapes.add_picture(str(path), Inches(px), Inches(py), Inches(pw), Inches(ph))
    if frame is not None:
        move(slide, frame, x=x - 0.01, y=y - 0.01, w=w + 0.02, h=h + 0.02)
    return pic


def _border(cell, color="E2E8F0", width=0.75, sides=("B",)):
    tcPr = cell._tc.get_or_add_tcPr()
    for side in ("L", "R", "T", "B"):
        tag = qn(f"a:ln{side}")
        for old in tcPr.findall(tag):
            tcPr.remove(old)
        ln = etree.SubElement(tcPr, tag, w=str(int(width * 12700)))
        if side in sides:
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr"), val=color)
        else:
            etree.SubElement(ln, qn("a:noFill"))


def table(slide, x, y, w, rows, widths, size=8.6, head_size=8.2, row_h=0.26, bold_first_col=True, colors=None):
    """Native table in the template's flat style: bold header, hairline separators, no fills."""
    n, m = len(rows), len(rows[0])
    gf = slide.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(row_h * n))
    t = gf.table
    tblPr = t._tbl.tblPr
    for attr in ("bandRow", "firstRow"):
        tblPr.set(attr, "0")
    style = tblPr.find(qn("a:tableStyleId"))
    if style is not None:
        style.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"       # "No Style, No Grid"
    total = sum(widths)
    for j, cw in enumerate(widths):
        t.columns[j].width = Inches(w * cw / total)
    for i, row in enumerate(rows):
        t.rows[i].height = Inches(row_h)
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.fill.background()
            c.margin_left = c.margin_right = Inches(0.04)
            c.margin_top = Inches(0.025)
            c.margin_bottom = Inches(0.02)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            head = i == 0
            col = NAVY if head or (j == 0 and bold_first_col) else BODY
            if colors and (i, j) in colors:
                col = colors[(i, j)]
            if isinstance(val, str):
                parts = [(val, head or (j == 0 and bold_first_col), col)]
            elif isinstance(val, tuple):                      # one styled cell: (text, bold, colour)
                parts = [val]
            else:
                parts = val
            runs(p, parts, head_size if head else size)
            _border(c, "CBD5E1" if head else "E2E8F0", 1.0 if head else 0.6)
    return gf


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def duplicate(prs, src):
    """Copy a slide (shapes, images, background) to the end of the deck."""
    new = prs.slides.add_slide(src.slide_layout)
    for sh in list(new.shapes):
        sh._element.getparent().remove(sh._element)
    rid_map = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype.endswith(("/slideLayout", "/notesSlide")):
            continue
        rid_map[rid] = (new.part.relate_to(rel.target_ref, rel.reltype, is_external=True) if rel.is_external
                        else new.part.relate_to(rel.target_part, rel.reltype))
    for el in src.shapes._spTree:
        if el.tag not in (qn("p:nvGrpSpPr"), qn("p:grpSpPr")):
            new.shapes._spTree.append(deepcopy(el))
    r_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    for el in new.shapes._spTree.iter():
        for attr, val in list(el.attrib.items()):
            if attr.startswith(r_ns) and val in rid_map:
                el.set(attr, rid_map[val])
    bg = src._element.cSld.find(qn("p:bg"))
    if bg is not None:
        new._element.cSld.insert(0, deepcopy(bg))
    return new


def reorder_and_prune(prs, keep):
    lst = prs.slides._sldIdLst
    by_part = {prs.part.related_part(s.rId): s for s in lst}
    wanted = [by_part[s.part] for s in keep]
    for s in list(lst):
        if s not in wanted:
            prs.part.drop_rel(s.rId)
        lst.remove(s)
    for s in wanted:
        lst.append(s)


def bom_groups():
    rows = {r["id"]: r for r in csv.DictReader(open(ROOT / "09_procurement" / "bom_v0_1.csv", encoding="utf-8"))}

    def rng(ids):
        lo = hi = 0.0
        for i in ids:
            a, b = (rows[i]["est_unit_cost_inr"].split("-") + [None])[:2]
            a = float(a.split()[0])
            b = float(b) if b else a
            q = float(rows[i]["qty"])
            lo, hi = lo + a * q, hi + b * q
        return lo, hi
    groups = [("ESP32-C3 SuperMini", "USB-C, native USB serial", "1", "Local / online", ["R01"]),
              ("ADS1115 module", "16-bit I²C ADC, auto-range", "1", "Local / online", ["R02"]),
              ("Precision resistors", "100 kΩ 0.1 % ×2 · 1 kΩ 1 % ×7", "9", "Online (element14 / Mouser IN)", ["R03", "R04"]),
              ("C0G capacitor, LEDs, perfboard", "10 nF C0G · 3 LEDs · headers", "set", "Local", ["R05", "R06", "R07"]),
              ("Pogo pins P75-B1", "1.02 mm, 2 mm travel (4 + 2 spare)", "6", "Online (Probots)", ["M01"]),
              ("Clamp + bench rig", "PETG print · acrylic · M3/M4 · dowels", "set", "Lab / local", ["M02", "M03", "M04", "M05", "P04"]),
              ("Strip materials", "polyimide film · seal tape · silver paint", "set", "Lab / online", ["P01", "S01", "P02"]),
              ("Test consumables", "1 % resistor set · IPA · gloves · saline", "set", "Local", ["P03", "P05", "P06", "P07"])]
    out, tl, th = [], 0.0, 0.0
    for name, spec, qty, src, ids in groups:
        lo, hi = rng(ids)
        tl, th = tl + lo, th + hi
        out.append((name, spec, qty, src, f"{lo:,.0f}–{hi:,.0f}"))
    return out, (tl, th)


# ================================================================== slide content
def cover(sl):
    by_id(sl, 86).top, by_id(sl, 86).height = Inches(4.30), Inches(0.62)
    set_text(by_id(sl, 86), [[("VK26-IITI-HT-0050", False)]], 24, BLUE, TITLE_FONT, PP_ALIGN.CENTER)
    move(sl, 86, x=2.2, w=8.93)
    textbox(sl, 1.4, 5.0, 10.53, 1.6, [
        [("Dermasense: a laser-written moisture strip that reads a wound dressing's own 'change line'", False)]],
        16, NAVY, TITLE_FONT, PP_ALIGN.CENTER, space=2)
    textbox(sl, 1.4, 5.62, 10.53, 1.0, [
        [("Team: ", True, NAVY), ("Soham Prabhakar Kadu · Bhakti Ajay Kadam", False)],
        [("Track: ", True, NAVY), ("Health Tech: Emergency Response & Remote Monitoring", False)],
        [("Core innovation: ", True, NAVY), ("two laser-carbonised electrode zones, at the pad centre and on the dressing "
                                             "maker's change line, let a clip-on reader say OK, CHANGE or CHECK without "
                                             "lifting the dressing.", False)]], 10.5, BODY, align=PP_ALIGN.CENTER, space=2)
    textbox(sl, 1.4, 6.55, 10.53, 0.3, [[("Evidence key on every slide:  ", True, MUTED), ("● completed & verified", True, GREEN),
                                         ("   ● designed, physical validation pending", True, "B45309"),
                                         ("   ● future scope", True, "475569")]], 8, MUTED, align=PP_ALIGN.CENTER)
    notes(sl, "Cover. Application ID from the Stage 2 invitation. Team names as registered. No institution or mentor "
              "is shown until confirmed (see PPT_QA_Report.md).")


def e4_slide(sl, ttl, pill_txt, pill_kind, metrics, fig, caption, heading, bullets, bar, note):
    title(sl, 133, ttl)
    delete(sl, 134, 152, 153, 154, 155, 148, 149, 150, 151, 145)
    pill(sl, pill_txt, pill_kind)
    for (vid, lid), (val, lab) in zip(((136, 137), (138, 139), (140, 141), (142, 143)), metrics):
        v = set_text(by_id(sl, vid), [[(val, False)]], 15 if len(val) < 12 else 13, BLUE, TITLE_FONT, PP_ALIGN.CENTER)
        v.top, v.height = Inches(1.12), Inches(0.33)          # embedded font; text box tall enough for its line
        lb = set_text(by_id(sl, lid), [[(lab, False)]], 7.6, MUTED, "DM Sans Medium", PP_ALIGN.CENTER)
        lb.top, lb.height = Inches(1.47), Inches(0.24)
    picture_in(sl, FIG / fig, 0.59, 1.91, 5.92, 3.93, frame=132)
    cap = by_id(sl, 144)
    set_text(cap, [[(caption, False)]], 7.6, MUTED)
    cap.top, cap.height = Inches(5.90), Inches(0.22)
    move(sl, 131, y=1.90, h=4.25)
    set_text(by_id(sl, 147), [[(heading, True)]], 11, NAVY)
    by_id(sl, 147).width = Inches(5.3)
    textbox(sl, 7.07, 2.48, 5.5, 3.6, bullets, 10.4, bullets=True, space=8)
    set_text(by_id(sl, 135), bar, 8.6, BODY)
    move(sl, 135, w=11.7, h=0.36)
    notes(sl, note)


def problem(sl):
    e4_slide(sl, "Problem Context", "PUBLISHED EVIDENCE · CITED", "blue",
             [("44.9 %", f"OF 588 CHANGES MADE AT OPTIMAL MOISTURE{SUP[1]}"),
              ("≈ 2 cm", f"MAKER'S 'CHANGE NOW' LINE FROM PAD EDGE{SUP[2]}"),
              ("1 point", f"WHERE TODAY'S MOISTURE SENSOR READS{SUP[1]}"),
              ("Uneven", f"IN-VITRO MOISTURE MAP, 8 POINTS{SUP[3]}")],
             "fig_problem.png",
             f"Figure: the maker's change line (≈ 2 cm inside the pad edge{SUP[2]}) is invisible under a cover. To scale.",
             "Target Beneficiary & Problem Statement",
             [[("Target user: ", True, NAVY), ("nurses and home carers looking after exuding chronic wounds (diabetic foot, "
                                               "venous leg and pressure ulcers) under foam dressings.", False)],
              [("Operational pain point: ", True, NAVY), ("the 'change now' signal is visual. Under bandages, socks or "
                                                          "compression it is hidden, so dressings are changed by the clock, "
                                                          "by lifting the cover, or after a leak.", False)],
              [("Problem statement: ", True, NAVY), ("carers need a reliable, low-cost signal that exudate has reached the "
                                                     "maker's change line, without lifting the dressing.", False)],
              [("Public search disclosure: ", True, NAVY),
               (f"WoundSense reads moisture at one point{SUP[1]}; a lab study mapped 8 points{SUP[3]}; diaper wetness "
                f"strips with clip-on readers exist{SUP[4]}; smart bandages use custom electronics{SUP[5]}. In our search, "
                "none reads a dressing's own change line.", False)],
              [("Why now: ", True, NAVY), (f"some makers already define 'full' as a distance from the pad edge{SUP[2]}, and "
                                           f"conductive carbon can be laser-written onto polyimide in one pass{SUP[7]}: a "
                                           "sensor can follow the maker's own rule at low cost.", False)]],
             [[("Project Overview: ", True, NAVY), ("Dermasense · Team ID VK26-IITI-HT-0050 · Track: Health Tech · "
                                                    "Core innovation: a laser-written two-zone strip that tells carers when a "
                                                    "dressing has reached its own change line.", False)]],
             "Sources: L08 Milne 2016 (full text), L28 dressing IFUs, L26 McColl 2007, P01/P02 patents, L03 Jiang 2022. "
             "Figure: Stage2_Final/figures/fig_problem.png (geometry from strip_v0_1_geometry.json).")


def journey_before(sl):
    e4_slide(sl, "User Journey: Before State", "CURRENT STATE · CITED", "blue",
             [("44.9 %", f"CHANGES WHILE MOISTURE WAS STILL OPTIMAL{SUP[1]}"),
              ("0.1–1.3 g/cm²·day", f"REPORTED EXUDATE RATES, 2 METHODS{SUP[6]}"),
              ("Hidden", "EXUDATE FRONT UNDER BANDAGE OR GARMENT"),
              ("Lift to look", "THE ONLY WAY TO CHECK A COVERED PAD")],
             "fig_journey_before.png",
             "Figure: current pain-point map. Numbers are cited; steps follow dressing instructions.",
             "Current Pain Point Mapping",
             [[("Time loss: ", True, NAVY), ("each check means unwrapping the limb or lifting the border, then re-securing "
                                             "it. Minutes per check will be measured in our nurse interviews (not yet done).",
                                             False)],
              [("Material waste: ", True, NAVY), (f"in the WoundSense study 44.9 % of 588 changes happened while moisture was "
                                                  f"still optimal{SUP[1]}: dressings with capacity left were discarded and the "
                                                  "wound disturbed.", False)],
              [("Safety hazard: ", True, NAVY), ("a late change lets exudate reach the border or leak: wet peri-wound skin "
                                                 "(maceration risk) and soiled clothing.", False)],
              [("Why a schedule fails: ", True, NAVY), (f"reported exudate production ranged from 0.10 to 1.3 g/cm² per day "
                                                        f"across patients and two methods{SUP[6]}; a fixed interval cannot "
                                                        "follow that.", False)],
              [("Root cause: ", True, NAVY), (f"the decision signal, the exudate front against the maker's line{SUP[2]}, is "
                                              "visual, and the dressing is covered.", False)]],
             [[("Quantified Inefficiency: ", True, NAVY), ("only published figures are used; we have not yet measured nurse "
                                                           "time or dressing cost per patient, and we do not estimate them "
                                                           "here.", False)]],
             "Sources: L08 Milne 2016; L38 exudate quantification study (abstract; two methods disagree).")


def journey_after(sl):
    e4_slide(sl, "User Journey: After State (Intended)", "INTENDED WORKFLOW · NOT CLINICALLY VALIDATED", "amber",
             [("2 zones", "CENTRE C + MAKER'S CHANGE LINE A"),
              ("4 states", "OK · CHANGE · CHECK · FAULT"),
              ("±10 %", "TARGET ALERT ACCURACY (BENCH, E4)"),
              ("0", "CONTACT WITH THE WOUND BED (BY DESIGN)")],
             "fig_journey_after.png",
             "Figure: intended workflow, designed and bench-testable, not clinically validated.",
             "Future Solution Mapping & Quantified Efficiency",
             [[("Fits today's routine: ", True, NAVY), ("the strip goes on the pad's outer face when the dressing is "
                                                        "applied; the reader clips onto its paddle. Nothing else changes.",
                                                        False)],
              [("Decision support: ", True, NAVY), ("CHANGE when the front reaches the maker's line; CHECK if A wets before "
                                                    "C (edge leak or misplaced strip); FAULT for a broken strip or reader "
                                                    "error.", False)],
              [("Efficiency targets (to measure in E4): ", True, NAVY), ("alert within ±10 % of the fluid volume at which "
                                                                         "the front visibly reaches the line; zero lifts "
                                                                         "of the dressing just to look.", False)],
              [("Cost target: ", True, NAVY), ("≤ ₹100 per disposable strip: polyimide film + laser time only; the "
                                               "reader is reused (estimate from the BOM film price).", False)],
              [("Who benefits (expected, to verify): ", True, NAVY), ("patients: fewer needless removals; carers: a logged "
                                                                       "reason for each change; clinics: fewer wasted "
                                                                       "dressings.", False)]],
             [[("Design Principle: ", True, NAVY), ("the strip never touches the wound bed; only film and carbon are "
                                                    "thrown away; every electronic part lives in the reusable reader.",
                                                    False)]],
             "Targets, not results. E4 (strips on real dressings with simulated exudate) will measure the alert accuracy.")


def arch(sl):
    title(sl, 186, "System Architecture & Specs")
    delete(sl, 187, 190, 191, *range(194, 212))
    pill(sl, "DESIGNED · PHYSICAL VALIDATION PENDING", "amber")
    picture_in(sl, FIG / "fig_block.png", 0.59, 1.06, 5.92, 4.24, frame=185)
    cap = by_id(sl, 189)
    set_text(cap, [[("Figure: block diagram with the software-verified and hardware-pending status of each block.",
                     False)]], 7.6, MUTED)
    cap.top, cap.height = Inches(5.34), Inches(0.3)
    set_text(by_id(sl, 193), [[("Engineering Target Specifications & Subsystems", True)]], 11, NAVY)
    table(sl, 7.05, 1.60, 5.48, [
        ("Parameter", "Target / design value", "Selected hardware / basis"),
        ("Sensing zones", "2: C (pad centre), A (change line); windows 6 × 3.9 mm", "LIG-like electrodes on 0.125 mm polyimide"),
        ("Electrode line / gap", "1.0 / 1.0 mm (provisional)", "fixed by E2 line-width and isolation data"),
        ("Wet / dry decision", "< 100 kΩ wet, > 300 kΩ dry, 3 scans", "calc: wet 4–15 kΩ, dry ≥ 1 MΩ"),
        ("Excitation", "bipolar, ≤ 33 µA, idle high-Z", "ESP32-C3 GPIO through 1 kΩ"),
        ("Measurement", "16-bit, auto-range, ratiometric", "ADS1115 (I²C 0x48), 100 kΩ 0.1 % ref"),
        ("Self-test", "check resistor ±5 % + COM loop", "100 kΩ 0.1 %; FAULT state"),
        ("Contacts", "4 pads at 5.08 mm, 2 dowels", "P75-B1 pogo pins, PETG clamp"),
        ("Output", "CSV over USB + 3 LEDs (now)", "BLE phone view = future scope"),
    ], [1.15, 1.95, 1.95], size=8.0, head_size=8.0, row_h=0.42)
    set_text(by_id(sl, 188), [[("Architecture Rationale: ", True, NAVY),
                               ("only film and carbon are disposable. Bipolar drive keeps the net DC on wet electrodes near "
                                "zero, and a known resistor checks the reader on every scan.", False)]], 8.6, BODY)
    move(sl, 188, w=11.7)
    notes(sl, "Values: 05_electronics/calc_readout_report.md, 07_firmware/reader_v0_1/config.h, 04_lig_lab/strip_v0_1_geometry.json.")


def e8_slide(sl, ttl, pill_txt, pill_kind, fig, caption, heading, bullets, bar, note, size=9.5):
    title(sl, 238, ttl)
    delete(sl, 239, 242, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254)
    pill(sl, pill_txt, pill_kind)
    picture_in(sl, FIG / fig, 0.59, 1.06, 5.92, 4.24, frame=237)
    cap = by_id(sl, 241)
    set_text(cap, [[(caption, False)]], 7.6, MUTED)
    cap.top, cap.height = Inches(5.36), Inches(0.22)
    move(sl, 236, h=4.85)
    set_text(by_id(sl, 244), [[(heading, True)]], 11, NAVY)
    by_id(sl, 244).width = Inches(5.3)
    textbox(sl, 7.07, 1.60, 5.5, 4.2, bullets, size, bullets=True, space=5)
    set_text(by_id(sl, 240), bar, 8.6, BODY)
    move(sl, 240, w=11.7, h=0.36)
    notes(sl, note)


def firmware(sl):
    e8_slide(sl, "System Architecture & Specs: Firmware & Data Flow", "VERIFIED IN SOFTWARE · HARDWARE PENDING", "green",
             "fig_dataflow.png", "Figure: one reader scan: four bipolar measurements, then hysteresis and the state decision.",
             "Firmware Logic, Signal Measurement & Logging",
             [[("Resistance measurement: ", True, NAVY), ("each path is driven both ways through a 100 kΩ 0.1 % reference. "
                                                          "Equal + and − phases leave no net DC on wet electrodes.", False)],
              [("ADC acquisition: ", True, NAVY), ("ADS1115 single-shot at 128 SPS, auto-ranged. A1 reads the 3V3 rail, so "
                                                   "the maths is ratiometric.", False)],
              [("Processing: ", True, NAVY), ("Rx from both phases, averaged, scaled by the on-board 100 kΩ check (must read "
                                              "within ±5 %, else FAULT), minus the 2 kΩ of protection resistors.", False)],
              [("Interpretation: ", True, NAVY), ("wet below 100 kΩ, dry above 300 kΩ, three scans in a row; LEDs show OK, "
                                                  "CHANGE, CHECK (blinking) or FAULT.", False)],
              [("Logging: ", True, NAVY), ("one CSV line per scan over USB. The PC logger checks the header and every row, "
                                           "adds PC time and keeps bad lines apart.", False)],
              [("Fail-safe behaviour: ", True, NAVY), ("between scans every drive pin is high-impedance, so no current flows "
                                                       "through the strip; during a FAULT the zone states are frozen, not "
                                                       "guessed.", False)]],
             [[("Software vs Hardware: ", True, NAVY), ("19 compile-time logic tests and 10 PC-side tests pass; the "
                                                        "firmware compiles for ESP32-C3 with 0 warnings. It has not run on a "
                                                        "wired board yet (bench test T0–T10 is next).", False)]],
             "Evidence: 07_firmware/reader_v0_1/zone_logic_tests.h, tools/test_*.py, arduino-cli output (327,176 bytes, 24 %).",
             size=9.8)


def cad(sl):
    e8_slide(sl, "CAD Design & Mechanical Specs", "DESIGNED · CAD VERIFIED · NOT YET BUILT", "amber",
             "fig_cad.png", "Figure: our SolidWorks 2019 models (9 parts, 1 assembly, 7 A3 drawings, STEP), v0.1 bench rig.",
             "Material Selection & Mechanical Validation",
             [[("Materials: ", True, NAVY), ("polyimide 0.125 mm (laser-carbonisable, flexible); PETG clamp (printable, "
                                             "tough); cast acrylic rig (laser-cut); stainless 2 mm dowels; P75-B1 pogo pins.",
                                             False)],
              [("Contact force (hand calculation): ", True, NAVY), ("1.48 mm pin compression → 0.72 N per pin, 2.9 N total; "
                                                                    "the 4 mm lid deflects 11 µm, so the springs set the "
                                                                    "force.", False)],
              [("Alignment: ", True, NAVY), ("worst-case tolerance stack 0.49 mm against ±1.35 mm allowed on a 3 mm pad "
                                             "(2.8× margin).", False)],
              [("Strip loads: ", True, NAVY), ("0.62 % bending strain at a 10 mm radius (polyimide yields near 3 %); a 10 N "
                                               "tug gives 20 MPa at the dowels against 231 MPa tensile.", False)],
              [("No FEA: ", True, NAVY), ("loads are below 3 N, so hand calculations suffice; the contact itself is "
                                          "tested physically (T-CON-01).", False)],
              [("Independent check: ", True, NAVY), ("verify_cad.py re-opens every file: units, volumes, 13 positions, "
                                                     "interference, drawings → 99 pass, 0 fail, 5 waiting for E2.", False)]],
             [[("Design Iteration: ", True, NAVY), ("interference detection found the seal tape trapped under the clamp "
                                                    "(9.0 mm³). The seal now starts at x = 23 mm, re-verified with 0 "
                                                    "interference (decision D-013).", False)]],
             "Evidence: 06_cad/calc_mechanical_report.md, 06_cad/verify_cad_report.md, 06_cad/solidworks/*.", size=9.2)


def strip(sl):
    e8_slide(sl, "CAD Design & Mechanical Specs: Sensing Strip & Laser Process", "DESIGNED · PHYSICAL VALIDATION PENDING",
             "amber", "fig_strip.png", "Figure: our laser files drawn from the DXFs: strip v0.1 and the E2 coupon. Not yet lased.",
             "Fabrication Approach & Process Validation (E2)",
             [[("Material: ", True, NAVY), (f"polyimide written by our CO₂ laser in one raster pass{SUP[7]}. We call it a "
                                            "LIG-like laser-carbonised conductive layer until Raman confirms graphene.",
                                            False)],
              [("Machine facts (LaserCAD config): ", True, NAVY), ("1200 × 900 mm bed, 20 kHz PWM, 98 % power cap. Our "
                                                                   "reference '12' is most likely a % PWM command, not "
                                                                   "watts.", False)],
              [("Critical parameters logged: ", True, NAVY), ("min/max power %, speed, 0.1 mm interval, passes, scan "
                                                              "direction, focus and tube current, copied from every layer "
                                                              "dialog.", False)],
              [("E2 plan: ", True, NAVY), ("4 bracket coupons (power 10/12/14, speed ×0.67/1/1.5) on 2 days + 3 "
                                           "resolution coupons; 72 pre-registered samples.", False)],
              [("Pass rules, fixed before testing: ", True, NAVY), ("sheet-resistance CV ≤ 20 %; smallest reliable line and "
                                                                    "gap; gaps > 3 MΩ; laser-cut holes 2.00–2.10 mm.", False)],
              [("Sealed leads: ", True, NAVY), (f"LIG made in air is superhydrophilic{SUP[9]}, so every lead outside the "
                                                "two windows is covered by polyimide tape.", False)]],
             [[("Laser Files Verified: ", True, NAVY), ("4 DXFs pass 35/35 checks (mm units, closed outlines, no overlaps, "
                                                        "minimum line and gap, fits the bed). The import into LaserCAD is "
                                                        "checked at the machine (E2 step S0-6).", False)]],
             "Evidence: 04_lig_lab/laser_files_check.md, 04_lig_lab/e2/E2_procedure.md, e2_sample_matrix.csv, machine_record.md.",
             size=9.2)


def schematic(sl):
    title(sl, 281, "Electronics Schematics & BOM")
    delete(sl, 282, 285, 286, *range(289, 324))
    pill(sl, "ERC VERIFIED · NOT YET WIRED", "green")
    picture_in(sl, FIG / "fig_schematic.png", 0.59, 1.06, 5.92, 3.35, frame=280)
    cap = by_id(sl, 284)
    set_text(cap, [[("Figure: our KiCad 10 schematic of the two-zone reader, exported by kicad-cli.", False)]],
             7.6, MUTED)
    cap.top, cap.height = Inches(4.45), Inches(0.3)
    textbox(sl, 0.62, 4.82, 5.85, 1.35, [
        [("Power distribution: ", True, NAVY), ("USB-C → SuperMini 3V3 regulator → ADS1115 and node network; the 3V3 rail "
                                                "is measured on A1 every scan.", False)],
        [("Connection strategy: ", True, NAVY), ("4 pogo pins press on the strip's 3 × 6 mm pads (no soldering, no ZIF on "
                                                 "porous carbon); 2 dowels through laser-cut holes align it.", False)]],
        8.8, bullets=True, space=4)
    set_text(by_id(sl, 288), [[("Pinout & Connection Map (from the netlist)", True)]], 11, NAVY)
    table(sl, 7.05, 1.60, 5.48, [
        ("Net", "ESP32-C3 / module pin", "Function"),
        ("DRV_C · DRV_A", "GPIO3 · GPIO4", "drive zone C · zone A through 1 kΩ"),
        ("DRV_LOOP", "GPIO5", "COM loop continuity (broken strip)"),
        ("DRV_REF", "GPIO10", "100 kΩ 0.1 % reference to node N"),
        ("DRV_CHK", "GPIO20", "100 kΩ self-check to node N"),
        ("SDA · SCL", "GPIO6 · GPIO7", "I²C to ADS1115 (0x48)"),
        ("N · +3V3", "ADS1115 A0 · A1", "node voltage · rail (ratiometric)"),
        ("LED_G/Y/R", "GPIO0 · GPIO1 · GPIO21", "OK · CHANGE · CHECK/FAULT"),
        ("S_C S_A COM1 COM2", "J4 pins 1–4", "pogo pins on the strip pads"),
        ("not used", "GPIO2 · 8 · 9", "strapping pins kept free"),
    ], [1.35, 1.55, 2.3], size=8.0, head_size=8.0, row_h=0.36)
    set_text(by_id(sl, 283), [[("Verification: ", True, NAVY),
                               ("KiCad ERC 0 violations. A script checks the netlist against the firmware pins and strip pad "
                                "order (0 mismatches) and writes the perfboard wiring table.", False)]], 8.6, BODY)
    move(sl, 283, w=11.7)
    notes(sl, "Evidence: 05_electronics/kicad/out/erc.rpt, 07_firmware/tools/check_consistency.py, 07_firmware/WIRING.md.")


def bom(sl):
    title(sl, 281, "Electronics Schematics & BOM: Bill of Materials")
    delete(sl, 282, 285, 286, *range(289, 324))
    pill(sl, "ESTIMATES · NOT YET ORDERED", "amber")
    picture_in(sl, FIG / "fig_window.png", 0.59, 1.06, 5.92, 4.24, frame=280)
    cap = by_id(sl, 284)
    set_text(cap, [[("Figure: why these values; ranges are calculations, to be replaced by E2/E4 data.", False)]],
             7.6, MUTED)
    cap.top, cap.height = Inches(5.36), Inches(0.3)
    groups, (tl, th) = bom_groups()
    set_text(by_id(sl, 288), [[("Itemized Prototype Bill of Materials (estimates)", True)]], 11, NAVY)
    rows = [("Component", "Specification", "Qty", "Source", "Est. ₹")] + groups + \
           [(("Total (excl. DMM, E4 dressings)", True, NAVY), "", "", "", (f"≈ {tl:,.0f}–{th:,.0f}", True, NAVY))]
    table(sl, 7.05, 1.60, 5.48, rows, [1.35, 1.75, 0.38, 1.12, 0.88], size=7.8, head_size=7.8, row_h=0.42)
    set_text(by_id(sl, 283), [[("Procurement Status: ", True, NAVY),
                               ("nothing ordered yet. Prices are estimates to confirm on supplier pages; all parts are sold "
                                "in India. First order: silver paint, 1 % resistor set, 0.1 % resistors, ADS1115, "
                                "ESP32-C3.", False)]], 8.6, BODY)
    move(sl, 283, w=11.7)
    notes(sl, "Totals computed from 09_procurement/bom_v0_1.csv (ranges = sum of min and max estimates).")


def e12_slide(sl, ttl, pill_txt, pill_kind, fig, caption, heading, bullets, bar, note, size=9.4):
    title(sl, 366, ttl)
    delete(sl, 367, 370, 373, 374, 375, 376, 377, 378, 379, 380)
    pill(sl, pill_txt, pill_kind)
    picture_in(sl, FIG / fig, 0.59, 1.06, 5.92, 4.24, frame=365)
    cap = by_id(sl, 369)
    set_text(cap, [[(caption, False)]], 7.6, MUTED)
    cap.top, cap.height = Inches(5.36), Inches(0.22)
    move(sl, 364, h=4.95)
    set_text(by_id(sl, 372), [[(heading, True)]], 11, NAVY)
    by_id(sl, 372).width = Inches(5.3)
    textbox(sl, 7.07, 1.60, 5.5, 4.3, bullets, size, bullets=True, space=5)
    set_text(by_id(sl, 368), bar, 8.6, BODY)
    move(sl, 368, w=11.7, h=0.36)
    notes(sl, note)


def maker(sl):
    e12_slide(sl, "Maker Journey", "GENUINE ARTIFACTS · NO STAGED EVIDENCE", "green", "fig_maker.png",
              "Figure: SolidWorks window captured on our machine + verbatim tool output (14–15 Oct 2026).",
              "Authenticity Verification: What Each Artifact Proves",
              [[("CAD in active use: ", True, NAVY), ("our native assembly open in SolidWorks with its FeatureManager tree "
                                                      "(13 components + mates); .SLDPRT, .SLDASM, .SLDDRW and .STEP files.",
                                                      False)],
               [("Independent re-check: ", True, NAVY), ("a script re-opens every CAD file and recomputes volumes and "
                                                         "positions from the design data: 99 pass, 0 fail.", False)],
               [("EDA + firmware: ", True, NAVY), ("KiCad schematic with its ERC log (0 violations); firmware built by "
                                                   "arduino-cli; logger and cross-check tests pass.", False)],
               [("Timestamps: ", True, NAVY), ("every step is a git commit since the 14 Oct restart, with raw native files "
                                               "(.SLDPRT, .STEP, .kicad_sch, .ino, .dxf) for audit.", False)],
               [("Lab photographs: ", True, NAVY), ("none yet. The first laser session (E2) will be photographed with ID "
                                                    "badges. We do not stage or generate lab photos.", False)]],
              [[("Raw Repository Linkage: ", True, NAVY), ("[team to insert the GitHub / Drive link before upload]: full "
                                                           "history from commit 330b474. Faculty sign-off follows the E2 "
                                                           "review.", False)]],
              "The repository link is the one item the team must add (see PPT_QA_Report.md). Screenshot: "
              "Stage2_Final/figures/sw_ui_assembly.png (captured by render_cad.py).")


def iterations(sl):
    e12_slide(sl, "Maker Journey: Engineering Iterations", "DOCUMENTED DECISIONS", "blue", "fig_decision.png",
              "Figure: weighted concept scores and the iteration path; each step is a dated git commit.",
              "Stage 1 to Stage 2 Engineering Iterations",
              [[("Iterative pivot: ", True, NAVY), ("Stage 1's closed-loop electrotherapy bandage was too broad to build and "
                                                    "validate in four months; we narrowed it to one measurable job: is the "
                                                    "dressing full?", False)],
               [("Concept selection: ", True, NAVY), ("5 sensing concepts scored on 13 weighted criteria. S2 (4.36) beat the "
                                                      "simpler S1 (4.29) because its order check separates a real front from "
                                                      "a leak.", False)],
               [("Fit the process we have: ", True, NAVY), ("4 zones → 2 zones, and 1 mm lines and gaps until E2 measures "
                                                            "what our laser can resolve.", False)],
               [("Verification-driven fixes: ", True, NAVY), ("seal moved off the clamp; assembly STEP was in cm, now mm; "
                                                              "drawings rebuilt first-angle with every dimension once.", False)],
               [("Risk-driven redesign: ", True, NAVY), ("the FMEA showed a cracked sense lead would read 'dry' forever "
                                                         "(RPN 224), so v0.2 loops each sense lead to a second pad.", False)]],
              [[("Prior Art We Respect: ", True, NAVY), (f"diaper wetness strips with clip-on readers exist{SUP[4]}. Our "
                                                         "contribution is the change-line placement, the order check and a "
                                                         "reproducible laser process.", False)]],
              "Evidence: 03_sensors/decision_matrix.md, 00_control/decisions.md (D-009…D-013), git history.")


def safety(sl):
    title(sl, 421, "Safety & Hazard Mitigation")
    delete(sl, 422, 423, *range(426, 435), 437, 438, 441, 442, 443, 444, 445, 446)
    pill(sl, "RISKS ESTIMATED · TESTS PLANNED", "amber")
    move(sl, 418, h=2.30)
    set_text(by_id(sl, 425), [[("Design FMEA v0.1: 15 failure modes (ratings estimated before tests)", True)]], 11, NAVY)
    by_id(sl, 425).width = Inches(7.0)
    table(sl, 0.82, 1.58, 8.15, [
        ("Failure mode", "Effect", "RPN", "Mitigation / verification"),
        ("F04 cracked sense lead", "zone reads 'dry' forever, no alarm", ("224", True, "DC2626"),
         "v0.2: loop each lead to a 2nd pad · T-MECH-01"),
        ("F07 front path differs", "CHANGE late or never", ("210", True, "DC2626"), "E4 on real foam dressings"),
        ("F08 humid dry baseline", "false wet", ("150", True, "DC2626"), "measure baselines (E4); thresholds in config.h"),
        ("F01 weak conductive layer", "zones always dry", ("140", True, "B45309"), "E2 bracket + per-strip QC record"),
        ("F05 pin contact on porous LIG", "readings drift high", ("120", True, "B45309"), "silver pads, rounded pins · T-CON-01"),
    ], [1.75, 1.95, 0.45, 2.95], size=7.9, head_size=7.8, row_h=0.27)
    picture_in(sl, FIG / "fig_fmea.png", 9.15, 1.25, 3.45, 2.06)
    for pid, iid, hid, x in ((419, 435, 436, 0.58), (420, 439, 440, 6.81)):
        move(sl, pid, y=3.50, h=2.95)
        move(sl, iid, y=3.74)
        move(sl, hid, y=3.71, w=5.3)
    set_text(by_id(sl, 436), [[("Physical & Embedded Fail-safes", True)]], 11, NAVY)
    set_text(by_id(sl, 440), [[("Standards Compliance (considered, not claimed)", True)]], 11, NAVY)
    textbox(sl, 0.84, 4.05, 5.5, 2.35, [
        [("Bench only: ", True, NAVY), ("the USB reader is not for patient use; an on-body version must be battery-only "
                                        "and isolated.", False)],
        [("No net DC: ", True, NAVY), ("bipolar drive, high-Z idle; bench test T8 checks < 5 mV average.", False)],
        [("Self-check every scan: ", True, NAVY), ("known 100 kΩ resistor + COM loop → FAULT instead of a wrong state.",
                                                   False)],
        [("No wound contact: ", True, NAVY), ("strip on the pad's outer face; leads sealed under polyimide tape.", False)],
        [("Laser work: ", True, NAVY), ("signed checklist each session: exhaust, never unattended, CO₂ extinguisher, "
                                        "lowest power first.", False)]], 9.3, bullets=True, space=4)
    textbox(sl, 7.07, 4.05, 5.5, 2.35, [
        [("ISO 14971: ", True, NAVY), ("risk-management approach; the FMEA is updated with test data.", False)],
        [("IEC 60601-1: ", True, NAVY), ("electrical safety for any future on-body reader.", False)],
        [("ISO 10993-1: ", True, NAVY), (f"biological evaluation before any skin or dressing contact; polyimide film is not "
                                         f"sold as medical grade{SUP[11]}.", False)],
        [("EN 13726: ", True, NAVY), (f"simulated exudate ('Solution A') for bench dressing tests{SUP[10]}.", False)],
        [("Laser safety: ", True, NAVY), ("IEC 60825-1 class rules and the lab's SOP during fabrication.", False)]],
        9.3, bullets=True, space=4)
    notes(sl, "Evidence: 00_control/fmea_v0_1.csv, 04_lig_lab/e2/E2_safety_checklist.md. Standards are considered "
              "in the design; no compliance is claimed.")


def roadmap(sl):
    title(sl, 421, "Roadmap")
    delete(sl, 422, 423, *range(426, 435), 437, 438, 441, 442, 443, 444, 445, 446)
    pill(sl, "FUTURE SCOPE · GATED PLAN", "grey")
    move(sl, 418, h=2.62)
    set_text(by_id(sl, 425), [[("4-Month Fabrication & Validation Plan (each gate must pass before the next step)", True)]],
             11, NAVY)
    by_id(sl, 425).width = Inches(9.0)
    picture_in(sl, FIG / "fig_roadmap.png", 0.72, 1.55, 11.9, 2.05)
    for pid, iid, hid in ((419, 435, 436), (420, 439, 440)):
        move(sl, pid, y=3.82, h=2.62)
        move(sl, iid, y=4.06)
        move(sl, hid, y=4.03, w=5.3)
    set_text(by_id(sl, 436), [[("Fabrication & Bench Phase (Months 1 - 2)", True)]], 11, NAVY)
    set_text(by_id(sl, 440), [[("Validation & Stage 3 Demo (Months 3 - 4)", True)]], 11, NAVY)
    textbox(sl, 0.84, 4.37, 5.5, 2.0, [
        [("Nov 2026: ", True, NAVY), ("E2 laser validation (S0, Day 1, Day 2); order parts; wire and bench-test the reader "
                                      "(T0–T10).", False)],
        [("Dec 2026: ", True, NAVY), ("strip v0.2 from E2 data with looped sense leads; print the clamp; contact "
                                      "(T-CON-01) and bend (T-MECH-01) tests.", False)]], 9.2, bullets=True, space=5)
    textbox(sl, 7.07, 4.37, 5.5, 2.0, [
        [("Jan 2027: ", True, NAVY), ("E4: strips on real foam dressings with simulated exudate: dry baselines, thresholds, "
                                      "alert vs the visible front.", False)],
        [("Feb 2027: ", True, NAVY), ("repeatability (≥ 5 strips × 3 runs); integrated bench demo and Stage 3 video with "
                                      "raw data.", False)],
        [("Stage 3 Target: ", True, NAVY), ("a working bench prototype (strip + clamp + reader) showing OK → CHANGE on a "
                                            "real dressing, with logged data. No patient use.", False)]],
        9.2, bullets=True, space=5)
    notes(sl, "Gate criteria from 04_lig_lab/e2/E2_procedure.md and 07_firmware/BENCH_TEST.md. Calendar months assume the "
              "first laser session in the week after submission.")


def e18_cards(sl, ttl, pill_txt, pill_kind, cards, bar, note, card_h=3.05):
    title(sl, 482, ttl)
    delete(sl, 483, 485, 486, 487, 488, 489, 490, 491)
    pill(sl, pill_txt, pill_kind)
    for pid in (479, 480, 481):
        move(sl, pid, h=card_h)
    for (hid, x), (head, paras) in zip(((493, 0.82), (495, 4.95), (497, 9.09)), cards):
        set_text(by_id(sl, hid), [[(head, True)]], 10.5, NAVY)
        by_id(sl, hid).width = Inches(3.35)
        textbox(sl, x, 1.62, 3.45, card_h - 0.62, paras, 9.8, space=6)
    set_text(by_id(sl, 484), bar, 8.6, BODY)
    move(sl, 484, w=11.7, h=0.36)
    notes(sl, note)


def challenges(sl):
    e18_cards(sl, "Technical Challenges & Risks", "FOUND IN OUR OWN VERIFICATION", "blue", [
        ("Geometry: Seal Trapped Under Clamp",
         [[("Observed: ", True, NAVY), ("the 0.09 mm seal tape began at x = 12 mm, but the clamp reaches x = 22 mm: a "
                                        "9.0 mm³ overlap.", False)],
          [("Impact: ", True, NAVY), ("tape under the paddle lifts the strip off the pogo pins: no contact, or an "
                                      "unreliable one.", False)],
          [("How found: ", True, NAVY), ("automated interference detection in our CAD verification script.", False)]]),
        ("Circuit: A Hidden Sense-Lead Failure",
         [[("Observed: ", True, NAVY), ("the reader checks the COM loop, but a cracked SENSE lead simply reads open, "
                                        "which looks like 'dry' (FMEA F04, RPN 224).", False)],
          [("Impact: ", True, NAVY), ("CHANGE would never appear and nothing would alarm.", False)],
          [("How found: ", True, NAVY), ("design FMEA of strip + reader together.", False)]]),
        ("Process: An Unknown Laser Recipe",
         [[("Observed: ", True, NAVY), (f"'12' is a % PWM command on an unidentified tube; CO₂ tubes fire unevenly at "
                                        f"low settings{SUP[8]}. Line width, gap isolation and contact on porous carbon "
                                        "are unmeasured.", False)],
          [("Impact: ", True, NAVY), ("every strip dimension is provisional.", False)],
          [("How found: ", True, NAVY), ("LaserCAD config audit + literature.", False)]]),
    ], [[("Also Caught in Verification: ", True, NAVY), ("assembly STEP exported in cm (now mm); drawings showed 0.13 mm "
                                                          "for a 0.125 mm film and repeated dimensions (fixed); a SolidWorks "
                                                          "API crash on colour arrays (typed arrays).", False)]],
        "Evidence: 06_cad/verify_cad_report.md (interference), 00_control/fmea_v0_1.md, 04_lig_lab/machine_record.md.")
    picture_in(sl, FIG / "fig_challenges.png", 0.62, 4.25, 12.1, 1.80)


def solutions(sl):
    e18_cards(sl, "Potential Solutions & Risk Mitigation", "FIXED · DESIGNED · FUTURE SCOPE", "grey", [
        ("Fixed & Verified",
         [[("Seal: ", True, NAVY), ("now starts at x = 23 mm; re-verified with 0 interference (D-013).", False)],
          [("Units & drawings: ", True, NAVY), ("all STEP in mm; first-angle A3 drawings; CAD checks 99 pass / 0 fail.",
                                                False)],
          [("Design consistency: ", True, NAVY), ("schematic ↔ firmware ↔ strip pads checked by script.", False)]]),
        ("Designed, to Prove on Hardware",
         [[("v0.2 strip: ", True, NAVY), ("each sense lead loops back to a second pad (6 pads), so every lead is checked "
                                          "every scan.", False)],
          [("Contact: ", True, NAVY), ("silver-painted pads and rounded pogo tips; contact resistance over clamp cycles "
                                       "(T-CON-01).", False)],
          [("Self-test: ", True, NAVY), ("check resistor and loop → FAULT, verified in bench test T2–T9.", False)]]),
        ("Fallbacks if E2 Disappoints",
         [[("Wider features: ", True, NAVY), ("set lines and gaps to what E2 resolves, re-run the DRC.", False)],
          [("Process: ", True, NAVY), ("bracket power and speed, slower or defocused passes, log tube current.", False)],
          [("Partner laser: ", True, NAVY), ("same DXF files on another lab's machine.", False)],
          [("Concept: ", True, NAVY), ("S1 single-zone strip (score 4.29) if two zones cannot be resolved.", False)]]),
    ], [[("Rule We Keep: ", True, NAVY), ("no claim of sensing performance, graphene identity or clinical benefit until the "
                                          "measurement exists.", False)]],
        "Future scope and validation plan below the cards; details in E2_measurements_and_unknowns.md.", card_h=2.72)
    box = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.58), Inches(3.92), Inches(12.17), Inches(2.15))
    box.adjustments[0] = 0.06
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor.from_string("F8FAFC")
    box.line.color.rgb = RGBColor.from_string("E2E8F0")
    box.shadow.inherit = False
    textbox(sl, 0.82, 4.02, 11.7, 0.3, [[("Future Scope & Validation Plan: evidence needed before practical or clinical use",
                                          True)]], 10.5, NAVY)
    textbox(sl, 0.82, 4.40, 5.75, 1.6, [
        [("Remaining physical experiments: ", True, NAVY), ("E2 fabrication; reader bench test; E4 wetting tests with "
                                                            "simulated exudate on foam dressings; repeatability.", False)],
        [("Material characterisation: ", True, NAVY), ("Raman (D, G, 2D bands) and SEM through a partner facility before "
                                                       "any 'graphene' claim.", False)],
        [("Reliability: ", True, NAVY), ("bending (T-MECH-01), contact cycling (T-CON-01), storage and humidity "
                                         "drift.", False)]], 8.9, bullets=True, space=3)
    textbox(sl, 6.85, 4.40, 5.75, 1.6, [
        [("Product steps: ", True, NAVY), ("battery-only isolated pod with BLE; multi-strip logging; a strip layout "
                                           "matched to each dressing model's change line.", False)],
        [("Before any patient use: ", True, NAVY), ("ISO 10993 biological evaluation, IEC 60601-1 electrical safety, "
                                                    "clinician feedback and an ethics-approved study.", False)],
        [("Not claimed today: ", True, NAVY), ("that the sensor works, that the material is graphene, or any clinical "
                                               "benefit.", False)]], 8.9, bullets=True, space=3)


REFS = [
    "Milne S.D. et al., A wearable wound moisture sensor as an indicator for wound dressing change, Int. Wound J. 13(6):1309–1314 "
    "(2016). doi:10.1111/iwj.12521 · full text read",
    "Dressing instructions for use: some foam dressings say 'change when exudate approaches ~2 cm from the pad edge'; "
    "Mölnlycke Mepilex Border Flex brochure uses strike-through reaching 3 edges · manufacturer documents, read as excerpts",
    "McColl D., Cartlidge B., Connolly P., Real-time monitoring of moisture levels in wound dressings in vitro, Int. J. Surg. "
    "5(5):316–322 (2007). doi:10.1016/j.ijsu.2007.02.008 · abstract",
    "US 5,469,145 and US 5,838,240 (wet diaper detector: detachable strip + clip-on detector); US 9,291,589; US 10,928,344 · "
    "patent summaries, claims not read",
    "Jiang Y. et al., Wireless, closed-loop, smart bandage with integrated sensors and stimulators, Nat. Biotechnol. (2022). "
    "doi:10.1038/s41587-022-01528-3 · listing + coverage",
    "Dealey C., Cameron J., Arrowsmith M., A study comparing two objective methods of quantifying the production of wound "
    "exudate, J. Wound Care 15(4):149–153 (2006) · abstract (methods disagree)",
    "Lin J. et al., Laser-induced porous graphene films from commercial polymers, Nat. Commun. 5:5714 (2014). "
    "doi:10.1038/ncomms6714 · full text read",
    "CO₂ laser tube current vs PWM setting, engineering measurements, softsolder.com (2022) · not peer-reviewed",
    "Li Y. et al., Laser-induced graphene in controlled atmospheres: from superhydrophilic to superhydrophobic surfaces, "
    "Adv. Mater. 29:1700496 (2017). doi:10.1002/adma.201700496 · abstract",
    "EN 13726-1:2002 / EN 13726:2023, Test methods for wound dressings (absorbency; 'Solution A') · catalogue entry; "
    "online link not reachable from our network",
    "DuPont position statement on the use of DuPont materials in medical applications (Kapton caution) · web page",
    "Texas Instruments ADS1115 datasheet (SBAS444); Espressif ESP32-C3 datasheet · vendor documents",
]


def references(sl):
    delete(sl, 504, 505, 506, 507, 508, 509, 510, 511, 512, 516)
    set_text(by_id(sl, 513), [[("References & Sources", False)]], 20.25, NAVY, TITLE_FONT)
    pill(sl, "SOURCES WITH READING DEPTH", "blue")
    textbox(sl, 0.62, 1.12, 12.1, 0.3, [[("Numbers match the superscripts on each slide. After each source we state how "
                                          "deeply it was read; nothing is labelled verified beyond that.", False)]],
            9, MUTED)
    textbox(sl, 0.62, 1.50, 12.1, 5.2, [[(f"{i}. ", True, NAVY), (r, False)] for i, r in enumerate(REFS, 1)],
            10.2, BODY, space=7)
    notes(sl, "Full list with verification notes: 02_research/literature.csv and research_matrix.csv (36 + 16 entries).")


IMAGES = [
    ("fig_problem.png", "Problem illustration, drawn to scale", "make_final_figures.py · strip_v0_1_geometry.json"),
    ("fig_journey_before.png", "Before-state pain-point map", "make_final_figures.py · cited sources 1–3"),
    ("fig_journey_after.png", "After-state intended workflow", "make_final_figures.py · firmware states"),
    ("fig_block.png", "System block diagram", "make_final_figures.py · verification logs"),
    ("fig_dataflow.png", "Firmware scan and state logic", "make_final_figures.py · reader_v0_1 source"),
    ("fig_cad.png", "SolidWorks renders + drawing", "render_cad.py · 06_cad/solidworks (our models)"),
    ("fig_strip.png", "Strip and E2 coupon layers", "make_final_figures.py · our DXF files"),
    ("fig_schematic.png", "KiCad schematic export", "kicad-cli · reader_v0_1.kicad_sch (ours)"),
    ("fig_window.png", "Measurement window", "make_final_figures.py · calc_readout.py"),
    ("fig_maker.png", "SolidWorks screenshot + logs", "screen capture of our machine · verbatim tool output"),
    ("fig_decision.png", "Decision matrix + iterations", "make_final_figures.py · decision_matrix.md"),
    ("fig_fmea.png", "FMEA risk ranking", "make_final_figures.py · fmea_v0_1.csv"),
    ("fig_roadmap.png", "4-month roadmap", "make_final_figures.py · E2/bench/E4 plans"),
    ("fig_challenges.png", "Seal clash + lead-break diagrams", "make_final_figures.py · geometry + FMEA"),
]


def image_sources(sl):
    delete(sl, *range(523, 550), 550)
    pill(sl, "ALL IMAGES ORIGINAL", "green")
    textbox(sl, 0.58, 1.02, 12.17, 0.45, [[("Every image in this deck was produced by the team from our own project files. "
                                            "No stock photos, no AI-generated images and no external images are used.",
                                            False)]], 9.5, BODY)
    for k, (f, what, src) in enumerate(IMAGES):
        col, row = k % 2, k // 2
        x, y = 0.58 + col * 6.15, 1.55 + row * 0.72
        picture_in(sl, FIG / f, x, y, 0.94, 0.58)
        textbox(sl, x + 1.05, y + 0.02, 4.95, 0.6, [[(what, True, NAVY)], [("Source: ", False, MUTED), (src, False, BLUE)],
                                                    [(f"Stage2_Final/figures/{f}", False, MUTED)]], 7.6, space=0)
    notes(sl, "Generators: Stage2_Final/figures/src/render_cad.py and make_final_figures.py.")


# ================================================================== build
def build():
    prs = Presentation(TEMPLATE)
    t = list(prs.slides)
    e4, e6, e8, e10, e12, e15, e18 = t[3], t[5], t[7], t[9], t[11], t[14], t[17]
    s_before, s_after = duplicate(prs, e4), duplicate(prs, e4)          # duplicates first, from pristine examples
    s_fw, s_strip = duplicate(prs, e8), duplicate(prs, e8)
    s_bom = duplicate(prs, e10)
    s_iter = duplicate(prs, e12)
    s_road = duplicate(prs, e15)
    s_sol = duplicate(prs, e18)
    order = [t[0], e4, s_before, s_after, e6, s_fw, e8, s_strip, e10, s_bom, e12, s_iter, e15, s_road, e18, s_sol,
             t[18], t[19]]
    cover(t[0])
    problem(e4)
    journey_before(s_before)
    journey_after(s_after)
    arch(e6)
    firmware(s_fw)
    cad(e8)
    strip(s_strip)
    schematic(e10)
    bom(s_bom)
    maker(e12)
    iterations(s_iter)
    safety(e15)
    roadmap(s_road)
    challenges(e18)
    solutions(s_sol)
    references(t[18])
    image_sources(t[19])
    reorder_and_prune(prs, order)
    OUTDIR.mkdir(exist_ok=True)
    prs.save(OUT)
    print(f"saved {OUT.relative_to(ROOT)}: {len(prs.slides)} slides")


if __name__ == "__main__":
    build()

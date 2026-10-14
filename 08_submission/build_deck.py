"""
Fill the OFFICIAL Vishwakarma Stage 2 template (unchanged copy in template/) with our content.

What this script changes:
  * text inside existing text boxes and tables (keeping each box's font, size, colour, bold labels)
  * the example photos/stock images -> our own figures (figures/, made by make_figures.py)
  * removes the "GUIDELINE SLIDE" / "PROJECT TERRAWEED EXAMPLE" badges, the "Example:" prefixes
    and the TerraWeed stock thumbnails/links
What it does NOT change: slide order, slide count, layouts, colours, card shapes, headings' wording
(except dropping slide-count hints like "(1-2 Slides)").

Evidence tags used on slides: [A] our earlier records, [B] planned measurement (not done),
[C] published literature.  Run: python build_deck.py
"""
from copy import deepcopy
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template" / "Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx"
OUT = HERE / "VK26-IITI-HT-0050_Stage2_Dermasense.pptx"
FIG = HERE / "figures"

B = True   # bold label run
N = False  # normal run


def shape_by_id(slide, sid):
    for sh in slide.shapes:
        if sh.shape_id == sid:
            return sh
    raise KeyError(f"shape {sid} not found")


def _strip_links(rpr):
    for h in rpr.findall(qn("a:hlinkClick")):
        rpr.remove(h)
    return rpr


def fill(slide, sid, paras):
    """paras: list of paragraphs; a paragraph is a str or a list of (text, bold) runs."""
    sh = shape_by_id(slide, sid)
    body = sh.text_frame._txBody
    ps = body.findall(qn("a:p"))
    all_runs = [r for p in ps for r in p.findall(qn("a:r"))]
    bold_rpr = norm_rpr = None
    for r in all_runs:
        rpr = r.find(qn("a:rPr"))
        if rpr is None:
            continue
        if rpr.get("b") == "1" and bold_rpr is None:
            bold_rpr = rpr
        elif rpr.get("b") != "1" and norm_rpr is None:
            norm_rpr = rpr
    if norm_rpr is None and bold_rpr is not None:
        norm_rpr = deepcopy(bold_rpr); norm_rpr.set("b", "0")
    if bold_rpr is None and norm_rpr is not None:
        bold_rpr = deepcopy(norm_rpr); bold_rpr.set("b", "1")
    first = all_runs[0].find(qn("a:rPr")) if all_runs else None
    ppr = ps[0].find(qn("a:pPr")) if ps else None
    for p in ps:
        body.remove(p)
    for para in paras:
        if isinstance(para, str):
            p = etree.SubElement(body, qn("a:p"))
            if ppr is not None:
                p.append(deepcopy(ppr))
            r = etree.SubElement(p, qn("a:r"))
            if first is not None:
                r.append(_strip_links(deepcopy(first)))
            etree.SubElement(r, qn("a:t")).text = para
            continue
        runs = para
        p = etree.SubElement(body, qn("a:p"))
        if ppr is not None:
            p.append(deepcopy(ppr))
        for text, bold in runs:
            r = etree.SubElement(p, qn("a:r"))
            proto = bold_rpr if bold else norm_rpr
            if proto is not None:
                r.append(_strip_links(deepcopy(proto)))
            etree.SubElement(r, qn("a:t")).text = text
    return sh


def fill_empty(slide, sid, lines, size_pt, color="1E3A8A", font="Poppins SemiBold", bold=True):
    sh = shape_by_id(slide, sid)
    body = sh.text_frame._txBody
    for p in body.findall(qn("a:p")):
        body.remove(p)
    for line, sz in zip(lines, size_pt):
        p = etree.SubElement(body, qn("a:p"))
        etree.SubElement(p, qn("a:pPr"), algn="ctr")
        r = etree.SubElement(p, qn("a:r"))
        rpr = etree.SubElement(r, qn("a:rPr"), lang="en-US", sz=str(int(sz * 100)), b="1" if bold else "0")
        sf = etree.SubElement(rpr, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), val=color)
        etree.SubElement(rpr, qn("a:latin"), typeface=font)
        etree.SubElement(r, qn("a:t")).text = line


def fill_table(slide, sid, rows, start_row=1):
    tbl = shape_by_id(slide, sid).table
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            if text == "":
                continue
            cell = tbl.cell(start_row + i, j)
            proto_cell = tbl.cell(1, j)
            tf = cell.text_frame
            ps = tf._txBody.findall(qn("a:p"))
            src_p = ps[0] if ps and ps[0].findall(qn("a:r")) else proto_cell.text_frame._txBody.findall(qn("a:p"))[0]
            rpr = src_p.find(qn("a:r")).find(qn("a:rPr"))
            ppr = src_p.find(qn("a:pPr"))
            for p in ps:
                tf._txBody.remove(p)
            p = etree.SubElement(tf._txBody, qn("a:p"))
            if ppr is not None:
                p.append(deepcopy(ppr))
            r = etree.SubElement(p, qn("a:r"))
            if rpr is not None:
                r.append(deepcopy(rpr))
            etree.SubElement(r, qn("a:t")).text = text


def replace_picture(slide, sid, image):
    sh = shape_by_id(slide, sid)
    _, rid = slide.part.get_or_add_image_part(str(image))
    blip = sh._element.find(".//" + qn("a:blip"))
    blip.set(qn("r:embed"), rid)
    sh.crop_left = sh.crop_right = sh.crop_top = sh.crop_bottom = 0


def move(slide, sid, dy_in=0.0, dh_in=0.0):
    sh = shape_by_id(slide, sid)
    sh.top = int(sh.top + dy_in * 914400)
    sh.height = int(sh.height + dh_in * 914400)


def delete(slide, *sids):
    for sid in sids:
        el = shape_by_id(slide, sid)._element
        el.getparent().remove(el)


def build():
    prs = Presentation(TEMPLATE)
    s = prs.slides

    # badges that belong to the template, not to our project
    for idx, ids in {2: [102], 3: [120], 5: [177], 7: [229], 9: [272], 11: [334], 13: [399], 14: [412],
                     16: [460], 17: [472], 19: [516], 4: [134], 6: [187], 8: [239], 10: [282], 12: [367],
                     15: [422], 18: [483], 20: [550]}.items():
        delete(s[idx - 1], *ids)

    # ---------- 1  Application ID ----------
    fill_empty(s[0], 86, ["VK26-IITI-HT-0050",
                          "Dermasense · LIG-on-Kapton dressing-moisture strip · Health Tech"], [18, 11])

    # ---------- 2  Problem Context (guideline card) ----------
    sl = s[1]
    fill(sl, 99, ["Problem Context"])
    fill(sl, 95, ["Project Overview & Problem Statement"])
    fill(sl, 96, [[("Project Overview: ", B), ("Dermasense (VK26-IITI-HT-0050, Health Tech): low-cost laser-induced "
                                             "graphene (LIG) strips written on Kapton to show when a dressing is full.", N)]])
    fill(sl, 97, [[("Problem Statement: ", B), ("exudate spread is hidden under bandages; in one study 44.9 % of 588 "
                                              "dressing changes were made while moisture was still optimal [C]. "
                                              "Beneficiaries: wound-care nurses and patients.", N)]])
    move(sl, 97, dy_in=0.25); move(sl, 94, dh_in=0.35)

    # ---------- 3  User Journey (guideline cards) ----------
    sl = s[2]
    fill(sl, 112, ["User Journey"])
    fill(sl, 114, ["Before State (today)"])
    fill(sl, 115, [[("Current Pain Point: ", B), ("exudate spreads unseen → change on a schedule or after leakage "
                                                 "→ early changes disturb the moist wound bed; late changes cause "
                                                 "leakage and skin maceration [C].", N)]])
    fill(sl, 116, [[("Quantified Inefficiency: ", B), ("44.9 % of 588 changes at optimal moisture (Milne 2016) [C]. "
                                                      "Local time and cost per change: to be measured [B].", N)]])
    fill(sl, 108, ["After State (planned, not yet built)"])
    fill(sl, 109, [[("Future Solution: ", B), ("a thin LIG strip on the outer face of the pad (no wound contact) reads "
                                              "wet/dry at the centre and at the maker's 2 cm change line.", N)]])
    fill(sl, 110, [[("Quantified Efficiency (target, unproven): ", B), ("alert within ±10 % of the fluid volume at "
                                                                       "which exudate visibly reaches the 2 cm line in "
                                                                       "bench tests [B]. No clinical benefit claimed.", N)]])
    move(sl, 110, dy_in=0.25); move(sl, 107, dh_in=0.30); move(sl, 113, dh_in=0.10)

    # ---------- 4  Problem Context & User Journey (example layout) ----------
    sl = s[3]
    fill(sl, 133, ["Problem Context & User Journey"])
    for vid, lid, v, lab in ((136, 137, "44.9 %", "CHANGES AT OPTIMAL MOISTURE [C]"),
                             (138, 139, "≈ 2 cm", "MAKER'S CHANGE LINE FROM EDGE [C]"),
                             (140, 141, "< 35 Ω/sq", "LIG BENCHMARK, LIN 2014 [C]"),
                             (142, 143, "'12'", "OUR EARLIER LASER SETTING [A]")):
        fill(sl, vid, [v]); fill(sl, lid, [lab])
    replace_picture(sl, 145, FIG / "f1_before_after.png")
    fill(sl, 144, ["Figure: before-state vs planned after-state (team diagram; after-state not yet built or tested)"])
    fill(sl, 148, [[("Target User: ", B), ("wound-care nurses and patients with exuding chronic wounds (diabetic "
                                          "foot and pressure ulcers) in clinics and home care.", N)]])
    fill(sl, 149, [[("Operational Bottleneck: ", B), ("the change decision depends on seeing the exudate front; under "
                                                     "bandages it is hidden, so changes follow a schedule or leakage "
                                                     "[C; to confirm in nurse interviews].", N)]])
    fill(sl, 150, [[("Before-State Flow: ", B), ("dressing applied → exudate spreads unseen → scheduled change or "
                                                "leakage → wound bed disturbed or skin macerated → repeat.", N)]])
    fill(sl, 151, [[("Public Search Disclosure: ", B), ("WoundSense single-point impedance sensor; McColl 2007 8-point "
                                                       "in-vitro moisture array; moisture-map patents; Stanford "
                                                       "closed-loop bandage 2022 [C]. Novelty of our approach is NOT "
                                                       "yet established.", N)]])
    fill(sl, 135, [[("Submission Note: ", B), ("Team ID: VK26-IITI-HT-0050 | Track: Health Tech | Stage 2 focus: prove "
                                              "a reproducible LIG process on our own 100 W laser before any sensor "
                                              "claim.", N)]])

    # ---------- 5  System Architecture (guideline cards) ----------
    sl = s[4]
    fill(sl, 174, ["System Architecture & Specs"])
    fill(sl, 166, ["Now: film → 100 W CO₂ laser → test coupon → multimeter + microscope → CSV "
                   "→ sheet resistance and repeatability. Planned: LIG strip → ESP32-C3 + 16-bit ADC → "
                   "phone."])
    fill(sl, 168, ["Targets [B]: sheet resistance ≤ 100 Ω/sq; run-to-run CV ≤ 20 %; line growth "
                   "measured; strip dry/wet contrast ≥ 100×; strip cost ≤ ₹100."])
    fill(sl, 170, ["100 W CO₂ laser with LaserCAD V8.28 (1200×900 mm, 20 kHz PWM) [A]; multimeter; "
                   "microscope. Planned: ESP32-C3, ADS1115, TMP117."])

    # ---------- 6  System Architecture & Specs (example layout) ----------
    sl = s[5]
    fill(sl, 186, ["System Architecture & Specs"])
    replace_picture(sl, 191, FIG / "f2_system.png")
    fill(sl, 189, ["Figure: Stage 2 measurement chain (now) and Stage 3 readout chain (planned) — team diagram"])
    fill_table(sl, 190, [
        ("Laser source", "Setting + tube mA logged per cell", "100 W CO₂ tube, LaserCAD V8.28 [A]"),
        ("Sheet resistance", "≤ 100 Ω/sq (target)", "3-length strips + multimeter [B]"),
        ("Repeatability", "CV ≤ 20 % over 2 days", "Reference cell ×2 per coupon [B]"),
        ("Line width", "Measured vs drawn 2.00 mm", "Optical microscope + scale [B]"),
        ("Zone readout", "Dry/wet ≥ 100× (planned)", "ESP32-C3 + ADS1115 16-bit [B]"),
        ("Temperature ref.", "±0.1 °C class sensor", "TMP117, I²C (datasheet) [C]"),
    ])
    fill(sl, 188, [[("Architecture Rationale: ", B), ("material first — no sensor or electronics claim until the LIG "
                                                     "process is shown to be reproducible on our own machine "
                                                     "(Experiment E1).", N)]])

    # ---------- 7  CAD (guideline) ----------
    sl = s[6]
    fill(sl, 226, ["CAD Design & Mechanical Specs"])
    fill(sl, 220, [[("Design Assets (now): ", B), ("parametric laser test coupon (Python → DXF, shown). Strip and "
                                                  "test-rig CAD start after line width is measured.", N)]])
    fill(sl, 221, [[("Material Selection: ", B), ("polyimide (Kapton-type) film, grade and thickness to be measured "
                                                 "[B]; polyimide tape to seal traces; no wound contact.", N)]])
    fill(sl, 222, [[("Mechanical Testing: ", B), ("no FEA claimed; bending durability will be measured (1,000 bends, "
                                                 "10 mm radius), not simulated [B].", N)]])
    replace_picture(sl, 219, FIG / "f3_coupon_tall.png")

    # ---------- 8  CAD (example layout) ----------
    sl = s[7]
    fill(sl, 238, ["CAD Design & Mechanical Specs"])
    replace_picture(sl, 242, FIG / "f3_coupon_wide.png")
    fill(sl, 241, ["Figure: lig_test_coupon.dxf generated by make_test_pattern.py (real design file; not yet fabricated)"])
    fill(sl, 244, ["Design File & Fabrication Constraints"])
    fill(sl, 245, [[("Test Coupon: ", B), ("6 cells × 3 strips, 2.00 mm wide, 8/16/24 mm long, 4 × 4 mm pads; "
                                         "one closed outline each, no overlaps.", N)]])
    fill(sl, 246, [[("Why 3 Lengths: ", B), ("R = Rs·L/W + R0; the slope gives sheet resistance, the intercept "
                                            "gives contact resistance.", N)]])
    fill(sl, 247, [[("Laser Settings: ", B), ("each colour layer has its own power and speed in LaserCAD; the "
                                             "reference cell appears twice per coupon.", N)]])
    fill(sl, 248, [[("Not Final: ", B), ("sensor-strip gaps and pads depend on measured line growth and the minimum "
                                        "isolating gap [B].", N)]])
    fill(sl, 249, [[("Next CAD (SolidWorks): ", B), ("laser alignment plate, bending jig and dressing test rig, "
                                                    "after E1 gives real dimensions.", N)]])
    fill(sl, 240, [[("Design Iteration: ", B), ("Stage 1 closed-loop electrotherapy bandage re-scoped: the LIG process "
                                               "must be proven first; stimulation deferred.", N)]])

    # ---------- 9  Electronics (guideline) ----------
    sl = s[8]
    fill(sl, 269, ["Electronics Schematics & BOM"])
    fill(sl, 263, [[("Circuit Schematics: ", B), ("Stage 2 needs no custom circuit (2-wire multimeter per strip). "
                                                 "Planned zone readout shown; not yet built.", N)]])
    fill(sl, 264, [[("Itemized BOM Table: ", B), ("next slide; characterisation + readout ≈ ₹1.7–3.6k "
                                                 "(estimates), excluding film.", N)]])
    fill(sl, 265, [[("Procurement Sourcing: ", B), ("nothing ordered, no quotations yet; prices are estimates or "
                                                   "public listings seen on 14 Oct 2026.", N)]])
    replace_picture(sl, 262, FIG / "f4_schematic_tall.png")

    # ---------- 10  Electronics (example layout) ----------
    sl = s[9]
    fill(sl, 281, ["Electronics Schematics & BOM"])
    replace_picture(sl, 286, FIG / "f4_schematic_wide.png")
    fill(sl, 284, ["Figure: planned bipolar zone readout (schemdraw); KiCad capture pending — KiCad not installed"])
    fill_table(sl, 285, [
        ("MCU (planned)", "ESP32-C3 dev board", "1", "Local, TBC", "₹250–700*"),
        ("ADC (planned)", "ADS1115 16-bit I²C", "1", "Local, TBC", "₹200–450*"),
        ("Temp. reference", "TMP117 breakout", "1", "Online", "₹446†"),
        ("Ref. resistors", "100 kΩ 0.1 %, 1 kΩ", "4", "Local", "₹40–160*"),
        ("Pad contacts", "Silver paint + Cu tape", "1+1", "Local", "₹750–1,800*"),
        ("Test fluid", "NaCl + CaCl₂ (Solution A)", "Lab", "Lab stock", "₹0"),
        ("Total (estimate, excl. film)", "₹1.7–3.6k", "", "", ""),
    ])
    fill(sl, 283, [[("Procurement Status: ", B), ("nothing ordered yet. * estimate; † public listing seen 14 Oct "
                                                 "2026, not a quotation. Polyimide film stock and grade to confirm.", N)]])

    # ---------- 11  Maker Journey (guideline cards) ----------
    sl = s[10]
    fill(sl, 333, ["Your Maker Journey"])
    fill(sl, 335, ["Earlier work [A] and next steps [B]:"])
    fill(sl, 340, ["Earlier trial on Kapton at setting '12' gave a black, LIG-like layer; no photos or settings "
                   "retained (preliminary)."])
    fill(sl, 341, ["E1 lab photos (team with ID badges at the laser) to be added after the first session."])
    fill(sl, 342, ["Faculty mentor review photo: pending."])
    fill(sl, 336, ["Original assets in our repository:"])
    fill(sl, 345, ["Python DXF generator + coupon file; E1 analysis script; git history from 14 Oct 2026."])
    fill(sl, 346, ["KiCad not installed yet; schematic drawn with schemdraw."])
    fill(sl, 347, ["No FEA claimed; bending will be measured."])
    fill(sl, 337, ["Repository link (to be added after upload):"])
    fill(sl, 350, ["Contains .py, .dxf, .csv and protocols."])
    fill(sl, 351, ["Raw CSVs and original photos committed with timestamps."])
    fill(sl, 352, ["No embedded videos; external links only."])

    # ---------- 12  Maker Journey (example layout) ----------
    sl = s[11]
    fill(sl, 366, ["Maker Journey"])
    replace_picture(sl, 370, FIG / "f5_photo_placeholder.png")
    fill(sl, 369, ["Figure: PLACEHOLDER — original E1 lab photo to be inserted (no photo exists yet)"])
    fill(sl, 373, [[("Iterative Pivot: ", B), ("after an evidence audit, the Stage 1 closed-loop electrotherapy bandage "
                                              "was re-scoped to a measurable first step: reproducible LIG on our own "
                                              "100 W laser.", N)]])
    fill(sl, 374, [[("Machine Facts Recovered: ", B), ("LaserCAD V8.28 config on our laptop: 1200×900 mm bed, "
                                                      "500/400 mm/s axes, 20 kHz PWM, 98 % max power [A].", N)]])
    fill(sl, 375, [[("Preliminary Observation: ", B), ("setting '12' gave a LIG-like black layer [A, unverified]. '12' "
                                                      "is most likely a % PWM command, not watts; tube current must be "
                                                      "measured.", N)]])
    fill(sl, 376, [[("Repository: ", B), ("E1 protocol, pre-filled sample log, test coupon, analysis code and evidence "
                                         "register committed with timestamps (link to be added).", N)]])
    fill(sl, 368, [[("Institutional Sign-Off: ", B), ("faculty mentor review pending — to be added after "
                                                     "Experiment E1.", N)]])

    # ---------- 13  Safety (guideline cards) ----------
    sl = s[12]
    fill(sl, 392, ["Safety & Hazard Mitigation"])
    fill(sl, 389, [[("Physical Fail-safes: ", B), ("laser runs only with exhaust on, lid closed and operator present; "
                                                  "lowest setting first; extinguisher nearby.", N)]])
    fill(sl, 390, [[("FMEA Matrix: ", B), ("see Safety by Design slide. No human or animal testing in Stages 2–3; "
                                          "bench and phantom only.", N)]])
    fill(sl, 395, ["ISO 10993 biocompatibility before any skin or wound contact; IEC 60601-1 limits for any future "
                   "on-body electronics; university laser-safety rules. None claimed as met yet."])

    # ---------- 14  Roadmap (guideline card) ----------
    sl = s[13]
    fill(sl, 409, ["Roadmap"])
    fill(sl, 406, [[("Fabrication Timeline: ", B), ("Oct E1 laser repeatability · Nov line width, strip v0.1, bench "
                                                   "readout · Dec dressing bench tests · Jan integration.", N)]])
    fill(sl, 407, [[("Stage 3 Target: ", B), ("a bench-tested LIG moisture strip with raw data and repeatability "
                                             "statistics; no clinical or diagnostic claims.", N)]])

    # ---------- 15  Safety by Design & Roadmap (example layout) ----------
    sl = s[14]
    fill(sl, 421, ["Safety by Design & Roadmap"])
    fill_table(sl, 423, [
        ("Laser over-power", "Burn-through, flame, polyimide fumes", "Lowest setting first; exhaust on; never unattended; stop on any flame"),
        ("Unstable low-PWM output", "Irreproducible LIG, wrong conclusions", "Log tube mA; reference cell ×2 per coupon; repeat on 2 days; report CV"),
        ("Contact artefacts", "False sheet resistance", "3-length fit separates contacts; silver-paint pads; meter checked on resistors"),
    ])
    fill(sl, 437, [[("Oct 2026: ", B), ("E1 — machine record, film thickness, 4 coupons around setting '12' on 2 "
                                       "days; resistance + microscope.", N)]])
    fill(sl, 438, [[("Nov 2026: ", B), ("E2 — line width and isolation gaps; strip v0.1; bench readout (ESP32-C3 "
                                       "+ ADS1115) assembled.", N)]])
    fill(sl, 440, ["Integration & Bench Demo (Months 3 - 4)"])
    fill(sl, 441, [[("Dec 2026: ", B), ("E3 — strip on real dressings with Solution A: centre zone vs 2 cm-line "
                                       "zone vs visual front.", N)]])
    fill(sl, 442, [[("Jan 2027: ", B), ("repeatability and bending tests; Stage 3 video of the bench system with raw "
                                       "data.", N)]])

    # ---------- 16 / 17  Challenges and mitigation (guideline cards) ----------
    sl = s[15]
    fill(sl, 457, ["Technical Challenges & Risks"])
    fill(sl, 455, ["'12' is a low-PWM setting on a 100 W tube, where output can be unstable [C]; actual power unknown "
                   "[A]; film grade unverified; without Raman/SEM we cannot prove 'graphene'."])
    sl = s[16]
    fill(sl, 469, ["Potential Solutions & Risk Mitigation"])
    fill(sl, 467, ["Log tube current per setting; replicate the reference cell; adjust speed to avoid unstable power; "
                   "request Raman/SEM via IIT Indore SIC; keep claims bench-level."])

    # ---------- 18  Technical Challenges & Risks (example layout) ----------
    sl = s[17]
    fill(sl, 482, ["Technical Challenges & Risks"])
    fill(sl, 493, ["Bottleneck: Laser Stability"])
    fill(sl, 485, [[("Observed Risk: ", B), ("tube current is spiky below ~25 % PWM (engineering measurements, not "
                                            "peer-reviewed) [C]; our '12' is in this range [A].", N)]])
    fill(sl, 486, [[("Mitigation: ", B), ("log tube mA; 2 coupons per day on 2 days; accept only if CV ≤ 20 % "
                                         "(pre-registered).", N)]])
    fill(sl, 495, ["Bottleneck: Proving It Is LIG"])
    fill(sl, 487, [[("Observed Risk: ", B), ("black and conductive does not prove graphene; resistance alone cannot "
                                            "confirm graphitic carbon.", N)]])
    fill(sl, 488, [[("Mitigation: ", B), ("Raman (D, G, 2D) and SEM via a university facility; until then we report a "
                                         "'LIG-like conductive layer'.", N)]])
    fill(sl, 497, ["Claims & Standards"])
    fill(sl, 489, [[("ISO 10993: ", B), ("required before any skin or wound contact; not started.", N)]])
    fill(sl, 490, [[("Wound Contact: ", B), ("none by design; the strip sits on the outer face of the absorbent "
                                            "pad.", N)]])
    fill(sl, 491, [[("Claims: ", B), ("bench data only; no diagnostic or healing claims.", N)]])
    fill(sl, 484, [[("Empirical Verification: ", B), ("none yet — first measurements are Experiment E1 (Oct 2026); "
                                                     "results will replace every target on these slides.", N)]])

    # ---------- 19  References ----------
    sl = s[18]
    title = shape_by_id(sl, 513)
    ps = title.text_frame.paragraphs
    for r in ps[1].runs[1:]:
        r.text = ""
    ps[1].runs[0].text = "(tags: [A] our records · [B] planned measurement · [C] published literature)"
    delete(sl, 507, 510, 511, 512, 505, 506, 509)
    refs = [
        "1. Lin J. et al., Laser-induced porous graphene films from commercial polymers, Nat. Commun. 5, 5714 (2014). doi:10.1038/ncomms6714",
        "2. Milne S.D. et al., A wearable wound moisture sensor as an indicator for wound dressing change, Int. Wound J. 13(6), 1309–1314 (2016). doi:10.1111/iwj.12521",
        "3. McColl D., Cartlidge B., Connolly P., Real-time monitoring of moisture levels in wound dressings in vitro, Int. J. Surg. 5(5), 316–322 (2007). doi:10.1016/j.ijsu.2007.02.008",
        "4. Jiang Y. et al., Wireless, closed-loop, smart bandage with integrated sensors and stimulators, Nat. Biotechnol. (2022). doi:10.1038/s41587-022-01528-3",
        "5. Shirzaei Sani E. et al., A stretchable wireless wearable bioelectronic system for infected chronic wounds, Sci. Adv. 9, eadf7388 (2023). doi:10.1126/sciadv.adf7388",
        "6. Asgharian H. et al., WoundMx: multiplexed wound-infection biomarker detection with laser-induced graphene, Research Square preprint (2025). doi:10.21203/rs.3.rs-7274589/v1",
        "7. Influence of lasing parameters on the morphology and electrical resistance of polyimide-based LIG, Carbon Letters (2023).",
        "8. Design of experiments and optimization of laser-induced graphene, University College Cork (2023).",
        "9. Dressing instructions: Mölnlycke Mepilex Border Flex 'time to change'; 3M Tegaderm silicone foam border guide.",
        "10. EN 13726-1:2002 / EN 13726:2023, Test methods for primary wound dressings (absorbency, 'Solution A').",
        "11. CO₂ laser tube current vs PWM measurements, softsolder.com (2022) — engineering blog, not peer-reviewed.",
        "12. Rezaei I. et al., Wearable Kapton graphene biosensor for toxic gases, J. Hazard. Mater. Adv. 15, 100452 (2024) — simulation only; reviewed, not used as evidence.",
        "13. DuPont statement on use of DuPont materials in medical applications (Kapton medical caution).",
    ]
    box = fill(sl, 508, refs)
    box.left, box.top, box.width = int(0.80 * 914400), int(1.80 * 914400), int(11.8 * 914400)
    card = shape_by_id(sl, 504)
    card.height = int(4.6 * 914400)

    # ---------- 20  Image Sources ----------
    sl = s[19]
    delete(sl, 535, 538, 541, 544, 547, 539, 540, 542, 543, 545, 546, 548, 549,
           524, 525, 526, 529, 530, 531, 532, 533, 534)
    delete(sl, 536, 527, 528)
    move(sl, 523, dh_in=0.25)
    t = fill(sl, 537, ["All figures in this deck were generated by the team from project files: flow diagrams "
                       "(matplotlib), coupon drawing rendered from lig_test_coupon.dxf, schematic (schemdraw). "
                       "Script: 08_submission/make_figures.py.",
                       "No stock photos and no AI-generated images are used. The photo slot on the Maker Journey "
                       "slide is a marked placeholder for an original E1 lab photo."])
    t.left, t.top, t.width = int(0.80 * 914400), int(1.20 * 914400), int(11.8 * 914400)

    prs.save(OUT)
    print(f"saved {OUT.name}")


if __name__ == "__main__":
    build()

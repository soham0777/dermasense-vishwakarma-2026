"""
Build the Stage 2 deck from the OFFICIAL Vishwakarma template (unchanged copy in template/).

Structure (team decision D-011): one strong content slide per template section, in the template's order,
using the template's own content-slide designs. The template's instruction ("guideline") slides are removed;
the Problem-Context design is duplicated so User Journey gets its own slide.

  1 Application ID   2 Problem Context   3 User Journey   4 System Architecture & Specs
  5 CAD Design & Mechanical Specs   6 Electronics Schematics & BOM   7 Maker Journey
  8 Safety by Design & Roadmap   9 Technical Challenges & Risks   10 References   11 Image Sources

Honesty rules: numbers from literature carry a citation number (see References slide); targets are called
targets; concept drawings are labelled as concepts; each slide's bottom strip says what is done vs next.
Run:  python make_figures.py && python build_deck.py
"""
from copy import deepcopy
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template" / "Vishwakarma Awards 2026-27 Stage 2 Submission Template (2).pptx"   # team-named official file (see template/TEMPLATE_PROVENANCE.md)
OUT = HERE / "VK26-IITI-HT-0050_Stage2_Dermasense.pptx"
FIG = HERE / "figures"
EMU = 914400
B, N = True, False
SUP = {1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷",
       8: "⁸", 9: "⁹", 10: "¹⁰", 11: "¹¹"}

# ---------------------------------------------------------------- helpers
def shape_by_id(slide, sid):
    for sh in slide.shapes:
        if sh.shape_id == sid:
            return sh
    raise KeyError(f"shape {sid} not found")


def _clean(rpr):
    for h in rpr.findall(qn("a:hlinkClick")):
        rpr.remove(h)
    return rpr


def fill(slide, sid, paras):
    """Replace a text box's text, keeping its formatting. A paragraph is a str (keeps the box's first-run
    style) or a list of (text, bold) runs (bold label + normal text, like the template)."""
    sh = shape_by_id(slide, sid)
    body = sh.text_frame._txBody
    ps = body.findall(qn("a:p"))
    runs = [r for p in ps for r in p.findall(qn("a:r"))]
    first = runs[0].find(qn("a:rPr")) if runs else None
    bold_rpr = next((r.find(qn("a:rPr")) for r in runs if r.find(qn("a:rPr")) is not None
                     and r.find(qn("a:rPr")).get("b") == "1"), None)
    norm_rpr = next((r.find(qn("a:rPr")) for r in runs if r.find(qn("a:rPr")) is not None
                     and r.find(qn("a:rPr")).get("b") != "1"), None)
    if norm_rpr is None and bold_rpr is not None:
        norm_rpr = deepcopy(bold_rpr); norm_rpr.set("b", "0")
    if bold_rpr is None and norm_rpr is not None:
        bold_rpr = deepcopy(norm_rpr); bold_rpr.set("b", "1")
    ppr = ps[0].find(qn("a:pPr")) if ps else None
    for p in ps:
        body.remove(p)
    for para in paras:
        p = etree.SubElement(body, qn("a:p"))
        if ppr is not None:
            p.append(deepcopy(ppr))
        items = [(para, None)] if isinstance(para, str) else para
        for text, bold in items:
            r = etree.SubElement(p, qn("a:r"))
            proto = first if bold is None else (bold_rpr if bold else norm_rpr)
            if proto is not None:
                r.append(_clean(deepcopy(proto)))
            etree.SubElement(r, qn("a:t")).text = text
    return sh


def lines(slide, sid, specs, color="1E3A8A", font="Poppins SemiBold"):
    """Write centred lines (text, size_pt, bold) into an empty text box."""
    body = shape_by_id(slide, sid).text_frame._txBody
    for p in body.findall(qn("a:p")):
        body.remove(p)
    for text, size, bold in specs:
        p = etree.SubElement(body, qn("a:p"))
        etree.SubElement(p, qn("a:pPr"), algn="ctr")
        r = etree.SubElement(p, qn("a:r"))
        rpr = etree.SubElement(r, qn("a:rPr"), lang="en-US", sz=str(int(size * 100)), b="1" if bold else "0")
        fill_el = etree.SubElement(rpr, qn("a:solidFill"))
        etree.SubElement(fill_el, qn("a:srgbClr"), val=color)
        etree.SubElement(rpr, qn("a:latin"), typeface=font)
        etree.SubElement(r, qn("a:t")).text = text


def table(slide, sid, rows, start=1):
    tbl = shape_by_id(slide, sid).table
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            if text == "":
                continue
            cell = tbl.cell(start + i, j)
            body = cell.text_frame._txBody
            ps = body.findall(qn("a:p"))
            src = ps[0] if ps and ps[0].find(qn("a:r")) is not None else \
                tbl.cell(1, j).text_frame._txBody.findall(qn("a:p"))[0]
            rpr, ppr = src.find(qn("a:r")).find(qn("a:rPr")), src.find(qn("a:pPr"))
            for p in ps:
                body.remove(p)
            p = etree.SubElement(body, qn("a:p"))
            if ppr is not None:
                p.append(deepcopy(ppr))
            r = etree.SubElement(p, qn("a:r"))
            if rpr is not None:
                r.append(deepcopy(rpr))
            etree.SubElement(r, qn("a:t")).text = text


def picture(slide, sid, image):
    sh = shape_by_id(slide, sid)
    _, rid = slide.part.get_or_add_image_part(str(image))
    sh._element.find(".//" + qn("a:blip")).set(qn("r:embed"), rid)
    sh.crop_left = sh.crop_right = sh.crop_top = sh.crop_bottom = 0


def grow(slide, pic, frame, cap, h_in):
    """Make a figure (and its white frame) taller and move the caption under it."""
    p, f, c = shape_by_id(slide, pic), shape_by_id(slide, frame), shape_by_id(slide, cap)
    p.height = int(h_in * EMU)
    f.height = int((h_in + 0.02) * EMU)
    c.top = p.top + p.height + int(0.06 * EMU)


def card(slide, keep, drop, paras, size_pt=11.0, gap_pt=6):
    """Put a whole card's text into one auto-growing box (bigger, readable) and remove the other boxes."""
    sh = fill(slide, keep, paras)
    for p in sh.text_frame.paragraphs:
        p.space_after = int(gap_pt * 12700)
        for r in p.runs:
            r.font.size = int(size_pt * 12700)
    delete(slide, *drop)


def delete(slide, *sids):
    for sid in sids:
        el = shape_by_id(slide, sid)._element
        el.getparent().remove(el)


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
    """keep: slides in the final order; every other slide is removed."""
    lst = prs.slides._sldIdLst
    by_part = {prs.part.related_part(s.rId): s for s in lst}
    wanted = [by_part[s.part] for s in keep]
    for s in list(lst):
        if s not in wanted:
            prs.part.drop_rel(s.rId)
        lst.remove(s)
    for s in wanted:
        lst.append(s)


# ---------------------------------------------------------------- content
def build():
    prs = Presentation(TEMPLATE)
    t = list(prs.slides)                       # template slides, 0-based
    title, problem, arch, cad, elec, maker, safety, risks, refs, imgs = (t[0], t[3], t[5], t[7], t[9], t[11],
                                                                        t[14], t[17], t[18], t[19])
    journey = duplicate(prs, problem)

    for sl, badge in ((problem, 134), (journey, 134), (arch, 187), (cad, 239), (elec, 282), (maker, 367),
                      (safety, 422), (risks, 483), (refs, 516), (imgs, 550)):
        delete(sl, badge)

    # 1 Application ID
    lines(title, 86, [("VK26-IITI-HT-0050", 18, True),
                      ("Dermasense: a laser-written graphene strip that tells nurses when a wound dressing is full",
                       12.5, True),
                      ("Soham Prabhakar Kadu · Bhakti Ajay Kadam  |  Health Tech: Emergency Response & "
                       "Remote Monitoring", 10.5, False)])

    # 2 Problem Context
    sl = problem
    fill(sl, 133, ["Problem Context"])
    for v, l, val, lab in ((136, 137, "44.9 %", f"OF CHANGES MADE AT OPTIMAL MOISTURE{SUP[1]}"),
                           (138, 139, "≈ 2 cm", f"MAKER'S 'CHANGE NOW' LINE FROM PAD EDGE{SUP[2]}"),
                           (140, 141, "1 spot", f"WHAT TODAY'S MOISTURE SENSOR READS{SUP[1]}"),
                           (142, 143, "1 laser pass", f"TO WRITE A GRAPHENE ELECTRODE{SUP[3]}")):
        fill(sl, v, [val]); fill(sl, l, [lab])
    picture(sl, 145, FIG / "problem.png"); grow(sl, 145, 132, 144, 3.85)
    fill(sl, 144, [f"Figure: exudate spreads outward; makers say change when it nears 2 cm from the pad edge{SUP[2]}, "
                   "but under a bandage nobody can see it"])
    fill(sl, 147, ["Target Beneficiary & Before-State User Flow"])
    fill(sl, 148, [[("Target User: ", B), ("wound-care nurses (clinics, home care) and patients with exuding chronic "
                                          "wounds: diabetic foot, pressure and venous leg ulcers.", N)]])
    fill(sl, 149, [[("Operational Bottleneck: ", B), ("the 'change now' signal is visual. Under bandages or opaque "
                                                     "covers it is hidden, so dressings are changed by the clock or "
                                                     "after a leak.", N)]])
    fill(sl, 150, [[("Before-State Flow: ", B), ("dressing on → exudate spreads unseen → changed too early "
                                                "(wasted dressing, disturbed wound) or too late (leak, macerated "
                                                "skin) → repeat.", N)]])
    fill(sl, 151, [[("Public Search Disclosure: ", B), (f"WoundSense reads moisture at one spot under the dressing{SUP[1]}; "
                                                       f"a 2007 lab array mapped moisture{SUP[4]}; Stanford's smart "
                                                       f"bandage uses cleanroom electronics{SUP[5]}; graphene wound sensors are "
                                                       f"still lab-only{SUP[6]}. None reads the maker's change line at "
                                                       "rupee cost.", N)]])
    fill(sl, 135, [[("Core Insight: ", B), ("dressing makers already define 'full' as a distance from the pad edge. "
                                           "Dermasense measures exactly that line, from outside the wound.", N)]])

    # 3 User Journey (duplicated Problem-Context design)
    sl = journey
    fill(sl, 133, ["User Journey"])
    for v, l, val, lab in ((136, 137, "By clock", "HOW DRESSINGS ARE CHANGED TODAY"),
                           (138, 139, "4 zones", "CENTRE → EDGE ON ONE STRIP"),
                           (140, 141, "0", "CONTACT WITH THE WOUND BED"),
                           (142, 143, "≤ ₹100", "TARGET COST PER STRIP")):
        fill(sl, v, [val]); fill(sl, l, [lab])
    picture(sl, 145, FIG / "journey.png"); grow(sl, 145, 132, 144, 3.85)
    fill(sl, 144, ["Figure: today's blind cycle vs the Dermasense cycle (target workflow, to be proven on the bench first)"])
    fill(sl, 147, ["After-State User Flow & Quantified Efficiency"])
    fill(sl, 148, [[("After-State Flow: ", B), ("strip on the pad, reader clipped on → zones read wet/dry → "
                                               "phone shows OK, SOON, CHANGE or LEAK → change when the change "
                                               "line is wet.", N)]])
    fill(sl, 149, [[("Who Benefits: ", B), ("patients get fewer needless removals; nurses get a reason for every "
                                           "change; clinics waste fewer dressings.", N)]])
    fill(sl, 150, [[("Efficiency Target: ", B), ("alert within ±10 % of the fluid volume at which exudate visibly "
                                                f"reaches the change line, in bench tests with simulated exudate{SUP[9]}.", N)]])
    fill(sl, 151, [[("Not Claimed Yet: ", B), ("fewer dressing changes or faster healing. Those need clinical studies "
                                              "after the bench prototype works.", N)]])
    fill(sl, 135, [[("Design Principle: ", B), ("the strip sits on the outer face of the absorbent pad, never on the "
                                               "wound: lower biocompatibility risk and no fouling of the sensor.", N)]])

    # 4 System Architecture & Specs
    sl = arch
    fill(sl, 186, ["System Architecture & Specs"])
    picture(sl, 191, FIG / "concept.png"); grow(sl, 191, 185, 189, 4.15)
    fill(sl, 189, ["Figure: disposable LIG strip on the pad + reusable clip-on reader + phone (concept illustration; not yet built)"])
    table(sl, 190, [
        ("Sensing strip", "4 wet/dry zones", "Laser-induced graphene on Kapton"),
        ("Zone signal", "Dry/wet ≥ 100× (target)", "AC drive between LIG electrodes"),
        ("Reader", "All zones every 5 s", "ESP32-C3 + ADS1115 (16-bit)"),
        ("Temperature ref.", "±0.1 °C class", "TMP117, I²C"),
        ("Display", "OK / SOON / CHANGE / LEAK", "USB log now, BLE app next"),
        ("Strip cost", "≤ ₹100 (target)", "One laser pass, no masks"),
    ])
    fill(sl, 188, [[("Architecture Rationale: ", B), ("only film and graphene are thrown away; every electronic part "
                                                     "lives in the reusable reader.", N)]])

    # 5 CAD Design & Mechanical Specs
    sl = cad
    fill(sl, 238, ["CAD Design & Mechanical Specs"])
    picture(sl, 242, FIG / "coupon_matrix.png"); grow(sl, 242, 237, 241, 3.60)
    fill(sl, 241, ["Figure: our laser test coupon (real DXF from make_test_pattern.py) and the E1 settings around 'setting 12'"])
    fill(sl, 244, ["Design Files & Laser Process Window"])
    fill(sl, 245, [[("Test Coupon: ", B), ("6 cells × 3 graphene strips, 2 mm wide, 8/16/24 mm long; each colour "
                                          "is one laser setting.", N)]])
    fill(sl, 246, [[("Measurement Trick: ", B), ("three lengths separate the graphene's sheet resistance from probe "
                                                "contact resistance, so a multimeter is enough.", N)]])
    fill(sl, 247, [[("Reference: ", B), ("'setting 12', where we saw a graphene-like layer, appears twice per coupon, "
                                        "on 2 days.", N)]])
    fill(sl, 248, [[("Accept Rule: ", B), ("the recipe passes if sheet resistance varies ≤ 20 % between runs, "
                                          "fixed before testing.", N)]])
    fill(sl, 249, [[("Next in SolidWorks: ", B), ("zone strip, clip-on reader and dressing test rig, sized from E1's "
                                                 "measured line width.", N)]])
    fill(sl, 240, [[("Why Process First: ", B), ("every graphene sensor needs a repeatable laser recipe, and '12' sits "
                                                f"in the low-power range where CO₂ tubes can be unstable{SUP[7]}.", N)]])

    # 6 Electronics Schematics & BOM
    sl = elec
    fill(sl, 281, ["Electronics Schematics & BOM"])
    picture(sl, 286, FIG / "schematic.png"); grow(sl, 286, 280, 284, 4.50)
    fill(sl, 284, ["Figure: zone readout; each zone is driven both ways and read by a 16-bit ADC (bench design; KiCad capture next)"])
    table(sl, 285, [
        ("Microcontroller", "ESP32-C3 dev board", "1", "Local", "₹250–700"),
        ("ADC", "ADS1115 16-bit, I²C", "1", "Local", "₹200–450"),
        ("Temp. reference", "TMP117 breakout", "1", "Online", "₹446"),
        ("Resistors", "100 kΩ 0.1 %, 1 kΩ", "4", "Local", "₹40–160"),
        ("Pad contacts", "Silver paint + Cu tape", "1+1", "Local", "₹750–1,800"),
        ("Test fluid", "NaCl + CaCl₂ (Solution A)", "Lab", "Lab stock", "₹0"),
        ("Total (excl. film)", "₹1.7–3.6k", "", "", ""),
    ])
    fill(sl, 283, [[("Procurement Status: ", B), ("every part is available in India. Prices are estimates or listings "
                                                 "seen on 14 Oct 2026; we order after E1 confirms the laser recipe.", N)]])

    # 7 Maker Journey
    sl = maker
    fill(sl, 366, ["Maker Journey"])
    picture(sl, 370, FIG / "work_evidence.png"); grow(sl, 370, 365, 369, 3.30)
    fill(sl, 369, ["Figure: our real work so far: coupon design file, E1 data sheet, machine settings read from our "
                   "LaserCAD install (lab photos follow E1)"])
    fill(sl, 373, [[("Iterative Pivot: ", B), ("Stage 1's closed-loop electrotherapy bandage was too broad to build "
                                              "well; we narrowed it to one measurable job: telling when a dressing is "
                                              "full.", N)]])
    fill(sl, 374, [[("Laser Evidence: ", B), ("our earlier trial on Kapton at setting '12' gave a black, graphene-like "
                                             "layer; E1 repeats it with full records.", N)]])
    fill(sl, 375, [[("Machine Facts: ", B), ("LaserCAD V8.28 on our laptop: 1200 × 900 mm bed, 20 kHz PWM, "
                                            "98 % cap. So '12' is a % command, not watts.", N)]])
    fill(sl, 376, [[("Repository: ", B), ("design scripts, coupon DXF, E1 protocol and data sheets under version "
                                         "control with timestamps (link to be added).", N)]])
    fill(sl, 368, [[("Team: ", B), ("Soham Prabhakar Kadu & Bhakti Ajay Kadam. Faculty mentor sign-off to be added "
                                   "after the E1 review.", N)]])

    # 8 Safety by Design & Roadmap
    sl = safety
    fill(sl, 421, ["Safety by Design & Roadmap"])
    table(sl, 423, [
        ("Laser over-power", "Burn-through, flame, polyimide fumes", "Lowest setting first; exhaust on; never unattended; stop on any flame"),
        ("Unstable low-power output", "Graphene quality varies run to run", "Log tube current; reference cell ×2 per coupon; repeat on 2 days"),
        ("Electrodes near skin (future)", "Irritation, current through tissue", "Strip stays off the wound; AC only, ≤ 10 µA; ISO 10993 tests before skin use"),
    ])
    fill(sl, 437, [[("Oct 2026: ", B), ("E1: reproducible graphene on our laser; measure sheet resistance and line "
                                       "width (4 coupons, 2 days).", N)]])
    fill(sl, 438, [[("Nov 2026: ", B), ("zone strip v0.1 cut from E1 dimensions; bench reader (ESP32-C3 + ADS1115) "
                                       "assembled and calibrated.", N)]])
    fill(sl, 440, ["Integration & Bench Demo (Months 3 - 4)"])
    fill(sl, 441, [[("Dec 2026: ", B), (f"E3: strips on real dressings with simulated exudate{SUP[9]}; zone alerts vs "
                                       "the visible stain front.", N)]])
    fill(sl, 442, [[("Jan 2027: ", B), ("repeatability and bending tests; Stage 3 demo video with raw data.", N)]])

    # 9 Technical Challenges & Risks
    sl = risks
    fill(sl, 482, ["Technical Challenges & Risks"])
    fill(sl, 493, ["Laser Repeatability"])
    card(sl, 485, [486], [
        [("Observed Risk: ", B), (f"'12' is a low-power command on a 100 W tube; such tubes fire unevenly below "
                                  f"~25 %{SUP[7]}, and the polyimide brand changes the result{SUP[8]}.", N)],
        [("Mitigation: ", B), ("log tube current, repeat the reference on 2 days, accept only if variation "
                               "≤ 20 %; fall back to slower or defocused passes.", N)],
        [("Test: ", B), ("E1, 8 reference cells over 2 days, tube current logged.", N)]])
    fill(sl, 495, ["Is It Graphene?"])
    card(sl, 487, [488], [
        [("Observed Risk: ", B), ("black and conductive is not proof of graphene; resistance alone cannot show "
                                  "graphitic carbon.", N)],
        [("Mitigation: ", B), ("Raman (D, G, 2D peaks) and SEM through a university facility; until then we call it "
                               "a graphene-like layer.", N)],
        [("Test: ", B), (f"Raman on our 3 best cells; graphene shows D ≈ 1350, G ≈ 1580 and 2D ≈ "
                         f"2700 cm⁻¹ bands{SUP[3]}.", N)]])
    fill(sl, 497, ["Safety & Standards"])
    card(sl, 489, [490, 491], [
        [("Wound Contact: ", B), ("none by design; the strip sits on the outer face of the pad.", N)],
        [("ISO 10993: ", B), (f"required before any skin contact; Kapton is not sold as medical grade{SUP[10]}.", N)],
        [("IEC 60601-1: ", B), ("applies to the future on-body reader, not to bench tests.", N)],
        [("Claims: ", B), ("bench data only, so no diagnostic or healing claims.", N)]])
    fill(sl, 484, [[("Fallback: ", B), ("if our laser cannot give repeatable graphene, we use a partner lab's laser; "
                                       "the strip design and reader stay the same.", N)]])

    # 10 References
    sl = refs
    ps = shape_by_id(sl, 513).text_frame.paragraphs
    for r in ps[1].runs[1:]:
        r.text = ""
    ps[1].runs[0].text = "(numbers match the superscripts on each slide)"
    delete(sl, 507, 510, 511, 512, 505, 506, 509)
    box = fill(sl, 508, [
        "1. Milne S.D. et al., A wearable wound moisture sensor as an indicator for wound dressing change, Int. Wound J. 13(6):1309–1314 (2016). doi:10.1111/iwj.12521",
        "2. Dressing instructions for use: Mölnlycke Mepilex Border Flex 'time to change'; 3M Tegaderm silicone foam border guide; foam dressings citing the 2 cm rule.",
        "3. Lin J. et al., Laser-induced porous graphene films from commercial polymers, Nat. Commun. 5, 5714 (2014). doi:10.1038/ncomms6714",
        "4. McColl D., Cartlidge B., Connolly P., Real-time monitoring of moisture levels in wound dressings in vitro, Int. J. Surg. 5(5):316–322 (2007). doi:10.1016/j.ijsu.2007.02.008",
        "5. Jiang Y. et al., Wireless, closed-loop, smart bandage with integrated sensors and stimulators, Nat. Biotechnol. (2022). doi:10.1038/s41587-022-01528-3",
        "6. Asgharian H. et al., WoundMx: wound-infection biomarker detection with laser-induced graphene, Research Square preprint (2025). doi:10.21203/rs.3.rs-7274589/v1",
        "7. CO₂ laser tube current vs PWM setting, engineering measurements, softsolder.com (2022), not peer-reviewed.",
        "8. Influence of lasing parameters on the morphology and electrical resistance of polyimide-based LIG, Carbon Letters (2023).",
        "9. EN 13726-1:2002 / EN 13726:2023, Test methods for primary wound dressings (absorbency; 'Solution A' simulated exudate).",
        "10. DuPont statement on the use of DuPont materials in medical applications (Kapton medical caution).",
        "11. Reviewed, not used as evidence: Rezaei I. et al., Wearable Kapton graphene biosensor for toxic gases, J. Hazard. Mater. Adv. 15, 100452 (2024), simulation only.",
    ])
    box.left, box.top, box.width = int(0.80 * EMU), int(1.80 * EMU), int(11.8 * EMU)
    shape_by_id(sl, 504).height = int(4.6 * EMU)

    # 11 Image Sources
    sl = imgs
    delete(sl, 535, 538, 541, 544, 547, 539, 540, 542, 543, 545, 546, 548, 549, 536, 527, 528,
           524, 525, 526, 529, 530, 531, 532, 533, 534)
    shape_by_id(sl, 523).height = int(1.3 * EMU)
    t2 = fill(sl, 537, ["All figures were drawn by the team with Python from project files: problem, journey and "
                        "concept illustrations; the coupon from lig_test_coupon.dxf; the schematic with schemdraw; machine "
                        "settings from LaserCAD SysCfg.ini. Script: 08_submission/make_figures.py.",
                        "No stock photos and no AI-generated images are used; concept drawings are labelled as concepts."])
    t2.left, t2.top, t2.width = int(0.80 * EMU), int(1.20 * EMU), int(11.8 * EMU)

    reorder_and_prune(prs, [title, problem, journey, arch, cad, elec, maker, safety, risks, refs, imgs])
    prs.save(OUT)
    print(f"saved {OUT.name}: {len(prs.slides)} slides")


if __name__ == "__main__":
    build()

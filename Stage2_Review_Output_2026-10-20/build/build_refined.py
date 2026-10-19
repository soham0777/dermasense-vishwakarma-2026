"""
Refined Stage 2 deck, 20 Oct 2026: built on the team's own template copy (template_source/, MD5 4d96244a...).

What this builder changes, following the template page by page (see ../Evidence_Map_PreEdit.md):
  slide 1     cover: Application ID and team names only (template page 1)
  slides 2-3  Problem Context: the problem only. Slide 2 defines it, with the Project Overview in the bottom bar as in
              the template's example page 4. Slide 3 shows what exists today, what each option misses, and our focus.
  slides 4-5  User Journey: WHO is affected (cited Indian data), a native journey map before and after, quantified
              inefficiency and (projected) efficiency
  slide 12    Maker Journey: team and lab photo placeholders live here (template pages 11-12)
All other slides reuse the tested slide functions of 1_presentation/build_deck.py, which is imported and never
modified. Output goes only to this folder; FINAL_SUBMISSION/ and 1_presentation/ are untouched.
Run:  python build_refined.py      then      python qa_refined.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
OUTDIR = HERE.parent
ROOT = OUTDIR.parent
sys.path.insert(0, str(ROOT / "1_presentation"))
import build_deck as B  # noqa: E402  (helpers + tested slide functions; read-only use)

TEMPLATE = HERE / "template_source" / "Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx"
OUT = OUTDIR / "Vishwakarma_Stage2_Refined.pptx"
ASSETS = HERE / "assets"
B.PHOTOS = OUTDIR / "team_photos"            # real team photos: team.*, lab1.* (never generated)
NAVY, BODY, MUTED, GREEN, BLUE = B.NAVY, B.BODY, B.MUTED, B.GREEN, B.BLUE
RED, AMBER = "DC2626", "B45309"
B.SUP.update({16: "¹⁶", 17: "¹⁷", 18: "¹⁸", 19: "¹⁹", 20: "²⁰"})
S = B.SUP

# five sources added on 20 Oct for "who is affected" (details: ../new_sources.csv)
B.REFS = B.REFS + [
    "Gupta N., Gupta S.K., Shukla V.K., Singh S.P., An Indian community-based epidemiological study of wounds, J. Wound "
    "Care 13(8):323–325 (2004). doi:10.12968/jowc.2004.13.8.26657 · abstract",
    "Sharma A. et al., Epidemiological profile of chronic wounds in an Indian population, Cureus 16(9):e68684 (2024). "
    "doi:10.7759/cureus.68684 · full text",
    "Anjana R.M. et al., ICMR-INDIAB national cross-sectional study (ICMR-INDIAB-17), Lancet Diabetes Endocrinol. "
    "11(7):474–489 (2023) · abstract and summaries",
    "Armstrong D.G., Boulton A.J.M., Bus S.A., Diabetic foot ulcers and their recurrence, N. Engl. J. Med. 376:2367–2375 "
    "(2017). doi:10.1056/NEJMra1615439 · summaries; range is an estimate and contested",
    "Price P.E. et al., Dressing-related pain in patients with chronic wounds: an international patient perspective, Int. "
    "Wound J. 5(2):159–171 (2008). doi:10.1111/j.1742-481X.2008.00471.x · abstract",
]
# the before/after journeys are now native PowerPoint shapes, so their old images are no longer used
B.IMAGES = [im for im in B.IMAGES if im[0] not in ("fig_journey_before.png", "fig_journey_after.png")]


# ================================================================== native, editable shapes
def sbox(sl, x, y, w, h, paras, size=9.0, fill="FFFFFF", line="CBD5E1", color=NAVY, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, adj=0.12, lw=1.0, space=0, margin=0.05):
    """Rounded box with editable text. paras: list of paragraphs; a paragraph is a str or a list of runs."""
    shp = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.adjustments[0] = adj
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGBColor.from_string(fill)
    if line:
        shp.line.color.rgb = RGBColor.from_string(line)
        shp.line.width = Pt(lw)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = anchor
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        parts = [(para, False)] if isinstance(para, str) else list(para)
        B.runs(p, parts, size, color)
        p.alignment = align
        p.space_after = Pt(space)
        p.line_spacing = 1.0
    return shp


def arrow_right(sl, x, y, w=0.16, h=0.2, color="94A3B8"):
    a = sl.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    a.fill.solid()
    a.fill.fore_color.rgb = RGBColor.from_string(color)
    a.line.fill.background()
    a.shadow.inherit = False
    return a


def journey_map(sl, x0, y0, w, persona, stages, row_labels, colours):
    """Design-thinking journey map in the template's left frame. stages: (title, does, row2) per column."""
    sbox(sl, x0, y0, w, 0.5, [persona], 8.6, fill="F1F5F9", line=None, color=BODY, align=PP_ALIGN.LEFT, margin=0.1)
    n, gap, lab_w = len(stages), 0.12, 0.62
    cw = (w - lab_w - gap * (n - 1)) / n
    top = y0 + 0.62
    for r, (lab, h) in enumerate(row_labels):
        yy = top + sum(hh for _, hh in row_labels[:r]) + 0.08 * r
        sbox(sl, x0, yy, lab_w - 0.06, h, [[(lab, True, MUTED)]], 7.6, fill="FFFFFF", line=None, align=PP_ALIGN.LEFT,
             margin=0.02)
    for k, (head, does, row2) in enumerate(stages):
        x = x0 + lab_w + k * (cw + gap)
        fill, line, tcol = colours[k]
        h0, h1, h2 = (h for _, h in row_labels)
        sbox(sl, x, top, cw, h0, [[(f"{k + 1}  ", True, line), (head, True, NAVY)]], 9.0, fill=fill, line=line, lw=1.3)
        sbox(sl, x, top + h0 + 0.08, cw, h1, [does], 8.4, fill="FFFFFF", line="E2E8F0", color=BODY)
        sbox(sl, x, top + h0 + h1 + 0.16, cw, h2, [[(row2, True, tcol)]], 8.4, fill=fill, line=None)
        if k < n - 1:
            arrow_right(sl, x + cw - 0.02, top + h0 / 2 - 0.1, w=gap + 0.04, h=0.2)


def placeholder_png(name, label, sub):
    """A plainly marked grey box (never a photo); the team replaces it with Change Picture or team_photos/."""
    ASSETS.mkdir(exist_ok=True)
    path = ASSETS / name
    img = Image.new("RGB", (1200, 800), (241, 245, 249))
    d = ImageDraw.Draw(img)
    for i in range(0, 1200, 36):
        d.line([(i, 18), (i + 18, 18)], fill=(148, 163, 184), width=4)
        d.line([(i, 782), (i + 18, 782)], fill=(148, 163, 184), width=4)
    for j in range(0, 800, 36):
        d.line([(18, j), (18, j + 18)], fill=(148, 163, 184), width=4)
        d.line([(1182, j), (1182, j + 18)], fill=(148, 163, 184), width=4)
    try:
        f1, f2 = ImageFont.truetype("seguisb.ttf", 64), ImageFont.truetype("segoeui.ttf", 40)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    d.text((600, 330), label, fill=(15, 23, 42), font=f1, anchor="mm")
    for i, line in enumerate(sub):
        d.text((600, 430 + i * 56), line, fill=(51, 65, 85), font=f2, anchor="mm")
    img.save(path)
    return path


# ================================================================== slide 1: basic details only
def cover(sl):
    sh = B.by_id(sl, 86)
    sh.top, sh.height = Inches(4.30), Inches(0.62)
    B.set_text(sh, [[("VK26-IITI-HT-0050", False)]], 26, BLUE, B.TITLE_FONT, PP_ALIGN.CENTER)
    B.move(sl, 86, x=2.2, w=8.93)
    B.textbox(sl, 1.4, 5.15, 10.53, 0.45, [[("Team: Soham Prabhakar Kadu · Bhakti Ajay Kadam", False)]], 14, NAVY,
              B.TITLE_FONT, PP_ALIGN.CENTER)
    B.notes(sl, "Template page 1 asks only for the Vishwakarma Application ID; team names added. Project title, track and "
                "core innovation are in the Project Overview bar on slide 2 (as in the template's example page 4).")


# ================================================================== slides 2-3: Problem Context (the problem only)
def problem(sl):
    B.e4_slide(sl, "Problem Context", "PUBLISHED EVIDENCE · CITED", "blue",
               [("44.9 %", f"CHANGES MADE AT STILL-OPTIMAL MOISTURE{S[1]}"),
                ("≈ 2 cm · 75 %", f"MAKERS' VISUAL 'CHANGE NOW' SIGNS{S[2]}{S[14]}"),
                ("1 point", f"WHERE TODAY'S MOISTURE SENSOR READS{S[1]}"),
                ("> 10×", f"SPREAD IN REPORTED EXUDATE RATES{S[6]}")],
               "fig_problem.png", "Figure: the change line is invisible under a cover (to scale, from our strip geometry).",
               "Problem Statement & Target Beneficiary",
               B.pts(("Problem:", "carers cannot see when a covered foam dressing reaches its maker's change line."),
                     ("Result:", "changes come too early (pain, waste) or too late (leaks, wet skin)."),
                     ("Who:", "nurses and family carers of people with exuding chronic wounds: diabetic foot, leg and "
                              "pressure ulcers."),
                     ("We will:", "signal that line from outside, without lifting the dressing.")),
               [[("Project Overview: ", True, NAVY),
                 ("Dermasense · Team ID VK26-IITI-HT-0050 · Health Tech: Emergency Response & Remote Monitoring · "
                  "Core innovation: a strip that reads a dressing's own change line.", False)]],
               "Milne 2016 [1]: 264 of 588 changes at optimal moisture (WoundSense spot readings). Change rules: some foam "
               "dressings ~2 cm from the pad edge [2]; ALLEVYN LIFE 'At 75%, it's time to change' [14]. Exudate 0.10-1.3 "
               "g/cm2/day by two methods [6]. Template page 2: Project Overview + Problem Statement.")


def _bar_size(sl, size):
    for r in B.by_id(sl, 135).text_frame.paragraphs[0].runs:
        r.font.size = Pt(size)


def gap(sl):
    """Problem Context 2/2: what exists today, what each option misses, and our focus (template page 4: public search)."""
    B.title(sl, 133, "Problem Context: What Exists Today and the Gap")
    B.delete(sl, 134, 152, 153, 154, 155, 148, 149, 150, 151, 145, 144, *range(136, 144), 127, 128, 129, 130)
    B.pill(sl, "PUBLIC SEARCH · NOT EXHAUSTIVE", "blue")
    B.move(sl, 132, y=1.05, h=5.02)
    B.move(sl, 131, y=1.05, h=5.02)
    B.textbox(sl, 0.78, 1.18, 5.6, 0.3, [[("What a carer can use today, and what each option misses", True)]], 11.5, NAVY)
    Y, N, P = ("✓", True, GREEN), ("✗", True, RED), ("◐", True, AMBER)
    B.table(sl, 0.72, 1.6, 5.66, [
        ("Today's option", "Without lifting?", "Maker's rule?", "What limits it"),
        ("Fixed schedule (clock)", N, N, f"a guess; exudate varies > 10×{S[6]}"),
        ("Lift and look", N, Y, f"disturbs the wound; removal hurts{S[20]}"),
        (f"Visual change indicator{S[14]}", N, Y, "works only if the dressing is visible"),
        (f"Single-point moisture sensor{S[1]}", P, N, "spot check at one point"),
        (f"Closed-loop smart bandage{S[5]}", Y, N, "lab research (mice); therapy device"),
        (f"Diaper wetness strip{S[4]}", Y, N, "made for diapers, not dressings"),
        ([("Dermasense (our target)", True, NAVY)], ("✓", True, GREEN), ("✓", True, GREEN),
         [("unproven: E2 and E4 test it", True, AMBER)]),
    ], [1.75, 0.95, 0.95, 2.0], size=9.0, head_size=8.6, row_h=0.47)
    B.textbox(sl, 0.78, 5.45, 5.6, 0.45, [[("✓ yes   ✗ no   ◐ partly.   ", True, MUTED),
                                          ("Our own non-exhaustive search of papers, patents and products.", False, MUTED)]],
              8.2, MUTED)
    B.set_text(B.by_id(sl, 147), [[("Public Search Disclosure & Our Focus", True)]], 11.5, NAVY)
    B.move(sl, 147, y=1.26)
    B.move(sl, 146, y=1.28)
    B.by_id(sl, 147).width = Inches(5.3)
    B.textbox(sl, 7.07, 1.75, 5.5, 4.2, B.pts(
        ("Searched:", f"papers, patents and products{S[1]}{S[4]}{S[5]}{S[14]}."),
        ("Found:", "no low-cost sensor that reads a dressing's own change line (in our search)."),
        ("Our focus:", "tell the carer when exudate reaches that line, without lifting the dressing."),
        ("Why now:", f"carbon can be laser-written on polyimide in one pass{S[7]}; makers already define 'full' by "
                     f"position{S[2]}{S[14]}."),
        ("Not our goal:", "diagnosis or therapy; we only report how full the dressing is.")),
        11.5, bullets=True, space=11)
    B.set_text(B.by_id(sl, 135), [[("Design Question: ", True, NAVY),
                                   ("how might a carer know that a covered dressing is full, without lifting it?", False)]],
               B.BAR_SIZE, BODY)
    B.move(sl, 135, w=11.7, h=0.36)
    B.notes(sl, "Ticks are our reading of each source: WoundSense readings in Milne 2016 [1] were spot checks at dressing "
                "change; Jiang 2022 [5] is a mouse-model closed-loop bandage; diaper patents [4] use a strip plus clip-on "
                "detector; ALLEVYN LIFE [14] has a visual change indicator. Source: 2_research/research_gap.md.")


# ================================================================== slides 4-5: User Journey (who is affected, design thinking)
ROWS = [("STAGE", 0.55), ("WHAT HAPPENS", 1.25), ("PAIN POINT", 1.05)]
ROWS_AFTER = [("STAGE", 0.55), ("WHAT HAPPENS", 1.25), ("GAIN", 1.05)]


def journey_before(sl):
    B.e4_slide(sl, "User Journey: Before State", "CURRENT STATE · CITED", "blue",
               [("1.9–4.5 per 1,000", f"HAVE A CHRONIC WOUND (INDIAN SURVEYS){S[16]}{S[17]}"),
                ("101 million", f"INDIANS LIVING WITH DIABETES{S[18]}"),
                ("19–34 %", f"LIFETIME FOOT-ULCER RISK IN DIABETES (EST.){S[19]}"),
                ("40.3 %", f"PATIENTS: CHANGE PAIN IS THE WORST PART{S[20]}")],
               "fig_problem.png", "", "Quantified Inefficiency (published data)",
               B.pts(("Time:", f"≈ 18 min per dressing visit, about 5 visits a week{S[13]} (UK, patient-reported)."),
                     ("Waste:", f"44.9 % of changes came while moisture was still optimal{S[1]}."),
                     ("Cost:", f"₹240–510 for one 10 × 10 cm foam dressing{S[15]}; each early change discards one."),
                     ("Safety:", f"a late change can leak (wet skin); removal hurts{S[20]}."),
                     ("Who carries it:", "the patient, the family carer and the nurse.")),
               [[("Insight: ", True, NAVY), ("the dressing already 'knows' when it is full (its change line); the carer "
                                             "just cannot see it.", False)]],
               "WHO: Gupta 2004 [16] 31 chronic wounds in 6,917 people (4.5/1,000); Sharma 2024 [17] 19 in 10,003 "
               "(1.9/1,000), diabetic foot ulcers 36.8 % of them; ICMR-INDIAB [18] 101 million (11.4 %); Armstrong 2017 [19] "
               "19-34 % lifetime (review estimate; upper bound contested); Price 2008 [20] 790 of 2,018 patients. Persona is "
               "illustrative, built from these data; not a real patient or interview. Quantified: Mölnlycke survey [13], "
               "Milne [1], Truemeds [15].")
    _swap_figure_for_map(sl, "Persona (illustrative, from the cited data; not a real patient): a 60-year-old with a diabetic "
                             "foot ulcer, cared for at home by family; a nurse visits to change the dressing.",
                         [("Dressing on", "foam dressing under a bandage or sock", "the front is hidden"),
                          ("Days pass", "exudate spreads, unseen", "no signal"),
                          ("Decide", "clock, a peek, or wait for a leak", "a guess"),
                          ("Change", "too early, or too late", "pain + waste, or wet skin"),
                          ("Repeat", f"about 5 times a week{S[13]}", f"≈ 18 min each time{S[13]}")],
                         ROWS, [("EFF6FF", "0369A1", "0369A1"), ("FEF2F2", "DC2626", "B91C1C"),
                                ("FEF2F2", "DC2626", "B91C1C"), ("FEF2F2", "DC2626", "B91C1C"),
                                ("FEF2F2", "DC2626", "B91C1C")],
                         "Figure: today's journey (design-thinking map; persona illustrative, numbers cited).")


def journey_after(sl):
    B.e4_slide(sl, "User Journey: After State (Intended)", "INTENDED · NOT CLINICALLY VALIDATED", "amber",
               [("0 lifts", "NEEDED TO CHECK THE DRESSING (BY DESIGN)"),
                ("up to 44.9 %", f"EARLY CHANGES A RELIABLE ALERT COULD AVOID{S[1]}"),
                ("≤ ₹100", "TARGET STRIP COST (ESTIMATE)"),
                ("1 in 2–5", f"AVOIDED CHANGES PAY FOR A STRIP (PROJ.){S[15]}")],
               "fig_problem.png", "", "How Each Person Is Helped (intended)",
               B.pts(("Patient:", f"fewer needless removals, the step patients find most painful{S[20]}."),
                     ("Family carer:", "a clear OK / CHANGE instead of a guess."),
                     ("Nurse:", "checks without unwrapping; every change has a logged reason."),
                     ("Budget:", "fewer wasted dressings; strip ≤ ₹100, reader reused (projection).")),
               [[("Design Principle: ", True, NAVY), ("same routine, nothing touches the wound, only film and carbon are "
                                                      "disposable. Target: alert within ±10 % of the visible front (E4).",
                                                      False)]],
               "Targets and projections, not results. 'Up to 44.9 %' assumes every change waits for CHANGE; some changes "
               "have other clinical reasons. Payback: strip <= Rs 100 (estimate) / dressing Rs 242-514 [15] = 0.19-0.41. "
               "Bluetooth: compiled and tested in software only (bench test T11 pending); no phone app yet.")
    _swap_figure_for_map(sl, "Same persona with Dermasense (intended workflow; bench-testable, not clinically validated).",
                         [("Strip on", "placed on the pad's outer face", "nothing on the wound"),
                          ("Reader on", "clips on: 4 pins, 2 dowels", "same routine"),
                          ("Glance", "green OK, without lifting", "no guess, no pain"),
                          ("Line wet", "amber CHANGE; red CHECK if a leak", "change on time"),
                          ("Remote", "state on a nearby phone (Bluetooth, to be tested)", "nurse sees it; reason logged")],
                         ROWS_AFTER, [("EFF6FF", "0369A1", "047857"), ("EFF6FF", "0369A1", "047857"),
                                      ("ECFDF5", "059669", "047857"), ("FFFBEB", "D97706", "047857"),
                                      ("ECFDF5", "059669", "047857")],
                         "Figure: the intended journey (design-thinking map); tested on the bench first, not on patients.")


def _swap_figure_for_map(sl, persona, stages, rows, colours, caption):
    """Replace the picture that e4_slide placed in the left frame with a native journey map."""
    pics = [sh for sh in sl.shapes if sh.shape_type == 13 and sh.name.startswith("Picture")
            and Inches(1.8) < sh.top < Inches(2.2)]                 # the figure e4_slide just placed
    assert len(pics) == 1, pics
    for p in pics:
        p._element.getparent().remove(p._element)
    B.move(sl, 132, x=0.58, y=1.90, w=5.94, h=3.95)
    journey_map(sl, 0.68, 1.98, 5.74, persona, stages, rows, colours)
    cap = B.by_id(sl, 144)
    B.set_text(cap, [[(caption, False)]], 7.6, MUTED)
    cap.top, cap.height = Inches(5.90), Inches(0.22)


# ================================================================== slide 12: Maker Journey with the team photos
def maker(sl):
    B.e12_slide(sl, "Maker Journey", "REAL FILES · RE-CHECKABLE · NO STAGED PHOTOS", "green", "fig_maker.png",
                "Figure: our own files and tool output (checks re-run 19 Oct 2026).",
                "Our Team at Work", None,
                [[("Raw Repository Linkage: ", True, NAVY), ("[team to insert the Drive link before upload]: all native "
                                                             "files and a dated work history.", False)]],
                "TEAM TO DO: replace the two photo placeholders (right-click > Change Picture, or put team.jpg and lab1.jpg "
                "in Stage2_Review_Output_2026-10-20/team_photos/ and rebuild), and the roles. Template page 11: lab photos "
                "of team members with institutional ID badges; joint photo with a faculty mentor only if one is attached. "
                "Every commit since 14 Oct carries a Co-Authored-By: Claude line.")
    team_ph = placeholder_png("placeholder_team_photo.png", "TEAM PHOTO",
                              ["both members, institutional ID badges visible", "replace: right-click → Change Picture"])
    lab_ph = placeholder_png("placeholder_lab_photo.png", "LAB PHOTO",
                             ["the team at work (CAD, wiring or the laser)", "replace: right-click → Change Picture"])
    for k, (key, ph) in enumerate((("team", team_ph), ("lab1", lab_ph))):
        _photo(sl, key, ph, 7.07 + k * 2.78, 1.62, 2.62, 1.72)
    B.textbox(sl, 7.07, 3.38, 5.5, 0.5, [[("Soham Prabhakar Kadu", True, NAVY), (" · role: ", False, MUTED),
                                         ("[team to add]", True, AMBER)],
                                        [("Bhakti Ajay Kadam", True, NAVY), (" · role: ", False, MUTED),
                                         ("[team to add]", True, AMBER)]], 9.0, space=1)
    B.textbox(sl, 7.07, 3.98, 5.5, 2.2, B.pts(
        ("Real files:", ".SLDPRT .SLDASM .SLDDRW .STEP .kicad_sch .ino .dxf, dated in git since 14 Oct."),
        ("Re-checkable:", "one command re-runs each check shown on the left."),
        ("How we work:", "scripts written with AI assistance (Claude), directed by us, build the CAD, schematic and "
                         "firmware; the physical build and tests are done by us, starting with E2."),
        ("Photos:", "never staged or generated.")), 10.0, bullets=True, space=4)


def _photo(sl, key, placeholder_path, x, y, w, h):
    found = sorted(B.PHOTOS.glob(f"{key}.*")) if B.PHOTOS.exists() else []
    path = found[0] if found else placeholder_path
    iw, ih = Image.open(path).size
    pic = sl.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    box_r, img_r = w / h, iw / ih
    if img_r > box_r:
        pic.crop_left = pic.crop_right = (1 - box_r / img_r) / 2
    else:
        pic.crop_top = pic.crop_bottom = (1 - img_r / box_r) / 2
    pic.name = f"PHOTO {key}" if found else f"PHOTO {key} - PLACEHOLDER (right-click > Change Picture)"
    pic.line.color.rgb = RGBColor.from_string("CBD5E1")
    pic.line.width = Pt(0.75)
    return pic


# ================================================================== slide 18: 20 references
def references(sl):
    B.delete(sl, 504, 505, 506, 507, 508, 509, 510, 511, 512, 516)
    B.set_text(B.by_id(sl, 513), [[("References & Sources", False)]], 20.25, NAVY, B.TITLE_FONT)
    B.pill(sl, "SOURCES WITH READING DEPTH", "blue")
    B.textbox(sl, 0.62, 1.10, 12.1, 0.3, [[("Numbers match the superscripts on each slide. After each source we state how "
                                            "deeply it was read; nothing is labelled verified beyond that.", False)]],
              8.8, MUTED)
    B.textbox(sl, 0.62, 1.42, 12.1, 5.3, [[(f"{i}. ", True, NAVY), (r, False)] for i, r in enumerate(B.REFS, 1)],
              8.6, BODY, space=2.2)
    B.notes(sl, "Full list: 2_research/literature.csv and research_matrix.csv (41 + 16 entries); refs 16-20 added 20 Oct "
                "(Stage2_Review_Output_2026-10-20/new_sources.csv).")


# ================================================================== build
def build():
    prs = Presentation(TEMPLATE)
    t = list(prs.slides)
    e4, e6, e8, e10, e12, e15, e18 = t[3], t[5], t[7], t[9], t[11], t[14], t[17]
    s_gap, s_before, s_after = B.duplicate(prs, e4), B.duplicate(prs, e4), B.duplicate(prs, e4)
    s_fw, s_strip = B.duplicate(prs, e8), B.duplicate(prs, e8)
    s_bom = B.duplicate(prs, e10)
    s_iter = B.duplicate(prs, e12)
    s_road = B.duplicate(prs, e15)
    s_sol = B.duplicate(prs, e18)
    order = [t[0], e4, s_gap, s_before, s_after, e6, s_fw, e8, s_strip, e10, s_bom, e12, s_iter, e15, s_road, e18, s_sol,
             t[18], t[19]]
    cover(t[0])
    problem(e4)
    gap(s_gap)
    journey_before(s_before)
    journey_after(s_after)
    _bar_size(e4, 8.8)
    B.arch(e6)
    B.firmware(s_fw)
    B.cad(e8)
    B.strip(s_strip)
    B.schematic(e10)
    B.bom(s_bom)
    maker(e12)
    B.iterations(s_iter)
    B.safety(e15)
    B.roadmap(s_road)
    B.challenges(e18)
    B.solutions(s_sol)
    references(t[18])
    B.image_sources(t[19])
    for shp in t[19].shapes:                     # photos now live only on slide 12
        if shp.has_text_frame and "Team photos (slides 2 and 12)" in shp.text_frame.text:
            for r in shp.text_frame.paragraphs[0].runs:
                r.text = r.text.replace("Team photos (slides 2 and 12) are taken by the team.",
                                        "Team photos (slide 12) are taken by the team.")
    B.reorder_and_prune(prs, order)
    prs.save(OUT)
    print(f"saved {OUT.name}: {len(prs.slides)} slides")


if __name__ == "__main__":
    build()

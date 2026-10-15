"""
Generate the E2 sample matrix, the pre-filled data files (CSV) and the printable bench sheets (PDF).

Single source for every sample ID, so the sheets you write on, the CSVs you type into and analyze_e2.py agree.
Never overwrites a CSV that already contains measurements (use --force only before any data exists).
Usage: python make_e2_sheets.py [--force]
"""
import argparse
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- pre-registered matrix
A_CELLS = [  # colour, power setting, speed rule, purpose  (same as E1, around the reference "12 @ S_ref")
    ("RED", "10", "S_ref", "power -2"),
    ("YELLOW", "12", "0.67 x S_ref", "speed -33 %"),
    ("GREEN", "12", "S_ref", "REFERENCE replicate 1"),
    ("CYAN", "12", "1.5 x S_ref", "speed +50 %"),
    ("BLUE", "14", "S_ref", "power +2"),
    ("MAGENTA", "12", "S_ref", "REFERENCE replicate 2 (other end)"),
]
A_LADDER = [("RED", "50"), ("YELLOW", "100"), ("GREEN", "150"), ("CYAN", "200"), ("BLUE", "300"), ("MAGENTA", "400")]
A_COUPONS = [("D1", "C1"), ("D1", "C2"), ("D2", "C1"), ("D2", "C2")]
A_LENGTHS = (8, 16, 24)
B_COUPONS = [("D1", "C1"), ("D1", "C2"), ("D2", "C1")]
B_LINES = [("W030", 0.3), ("W050", 0.5), ("W080", 0.8), ("W100", 1.0), ("W150", 1.5)]
B_GAPS = [("G020", 0.2), ("G030", 0.3), ("G050", 0.5), ("G080", 0.8), ("G100", 1.0), ("G150", 1.5)]
B_HOLES = ["H1", "H2", "H3"]
CONTROLS = [("shorted leads", "0"), ("open leads", "OL"), ("resistor 100 ohm 1 %", "100"), ("resistor 10 kohm 1 %", "10000"),
            ("resistor 1 Mohm 1 %", "1000000"), ("un-lased film, probes 10 mm apart", "OL")]


def a_cell(day, cpl, colour):
    return f"E2-A-{day}-{cpl}-{colour}"


def b_feat(day, cpl, feat):
    return f"E2-B-{day}-{cpl}-{feat}"


def tables():
    t = {}
    t["e2_sample_matrix.csv"] = (
        ["sample_id", "part", "day", "coupon", "dxf", "layer_colour", "power_setting", "speed", "interval_mm", "passes",
         "drawn_width_mm", "drawn_lengths_mm", "drawn_gap_mm", "purpose"],
        [[f"E2-A-R-{c}", "A (speed ladder, only if S_ref unknown)", "S0", "R", "lig_test_coupon.dxf", c, "12", f"{s} mm/s",
          "0.1", "1", "2.0", "8/16/24", "", "choose S_ref"] for c, s in A_LADDER]
        + [[a_cell(d, c, col), "A", d, c, "lig_test_coupon.dxf", col, p, sp, "0.1", "1", "2.0", "8/16/24", "", why]
           for d, c in A_COUPONS for col, p, sp, why in A_CELLS]
        + [[b_feat(d, c, f), "B", d, c, "e2_experiment/e2_res_coupon.dxf", "GREEN (ENGRAVE)", "reference", "S_ref", "0.1", "1",
            w, "16", "", "line resolution"] for d, c in B_COUPONS for f, w in B_LINES]
        + [[b_feat(d, c, f), "B", d, c, "e2_experiment/e2_res_coupon.dxf", "GREEN (ENGRAVE)", "reference", "S_ref", "0.1", "1",
            "1.0", "16", g, "gap isolation"] for d, c in B_COUPONS for f, g in B_GAPS]
        + [[b_feat(d, c, h), "B", d, c, "e2_experiment/e2_res_coupon.dxf", "BLUE (CUT)", "cut setting (S0-8)", "cut speed (S0-8)", "",
            "1", "2.0 (hole)", "", "", "laser-cut hole size / dowel fit"] for d, c in B_COUPONS for h in B_HOLES])
    t["e2_session.csv"] = (
        ["session", "date", "operator", "lab_in_charge_permission_YN", "machine_make_model", "controller", "tube_rating_W",
         "film_id_lot", "film_thickness_1_mm", "film_thickness_2_mm", "film_thickness_3_mm", "film_thickness_4_mm",
         "film_thickness_5_mm", "room_C_start", "room_C_end", "RH_pct", "chiller_C_start", "chiller_C_end",
         "S_ref_mm_s", "S_ref_source", "cut_power_setting", "cut_speed_mm_s", "meter_model", "meter_max_range_ohm",
         "microscope_and_scale", "notes"],
        [[s] + [""] * 25 for s in ("S0", "D1", "D2")])
    log_rows = []
    for c, s in A_LADDER:
        log_rows.append(["E2-A-R", "", c, "speed ladder", "Scan", "12", f"{s}", "0.1"] + [""] * 16)
    for i in range(8):
        log_rows.append(["CUTSEARCH", "", "BLUE", f"cut attempt {i + 1}", "Cut", "ref + 3 per step", "20", ""] + [""] * 16)
    for d, cpl in A_COUPONS:
        for col, p, sp, why in A_CELLS:
            log_rows.append([f"E2-A-{d}-{cpl}", "", col, why, "Scan", p, sp, "0.1"] + [""] * 16)
        log_rows.append([f"E2-A-{d}-{cpl}", "", "BLACK (OUTLINE_CUT)", "coupon outline", "Cut or OFF", "cut setting", "cut speed", ""] + [""] * 16)
    for d, cpl in B_COUPONS:
        log_rows.append([f"E2-B-{d}-{cpl}", "", "GREEN (ENGRAVE)", "all lines and gaps", "Scan", "reference", "S_ref", "0.1"] + [""] * 16)
        log_rows.append([f"E2-B-{d}-{cpl}", "", "BLUE (CUT)", "outline + holes (after engraving)", "Cut", "cut setting", "cut speed", ""] + [""] * 16)
    t["e2_machine_log.csv"] = (
        ["coupon_id", "date_time", "layer_colour", "purpose", "mode_planned", "power_planned", "speed_planned_mm_s",
         "interval_planned_mm", "entered_mode", "entered_min_power", "entered_max_power", "power_field_units",
         "entered_speed_mm_s", "entered_interval_mm", "entered_passes", "scan_direction_X_or_Y", "bidirectional_YN",
         "layer_order_no", "focus_method_and_height", "air_assist", "tube_current_mA", "job_file_name", "screenshot_photo",
         "notes"], log_rows)
    t["e2_visual.csv"] = (
        ["sample_id", "grade_0to5", "continuous_YN", "burn_through_YN", "tape_test_pass_fail", "photo_file", "notes"],
        [[a_cell(d, c, col)] + [""] * 6 for d, c in A_COUPONS for col, *_ in A_CELLS]
        + [[b_feat(d, c, f)] + [""] * 3 + ["n/a"] + [""] * 2 for d, c in B_COUPONS for f, _ in B_LINES + B_GAPS])
    t["e2_resistance.csv"] = (
        ["sample_id", "drawn_length_mm", "drawn_width_mm", "reading_no", "R_ohm", "display_if_not_number", "meter_range",
         "contact_method", "room_C", "notes"],
        [[f"{a_cell(d, c, col)}-L{L:02d}", L, 2.0, r, "", "", "", "", "", ""]
         for d, c in A_COUPONS for col, *_ in A_CELLS for L in A_LENGTHS for r in (1, 2, 3)]
        + [[b_feat(d, c, f), 16, w, r, "", "", "", "", "", ""] for d, c in B_COUPONS for f, w in B_LINES for r in (1, 2, 3)])
    t["e2_isolation.csv"] = (
        ["sample_id", "drawn_gap_mm", "reading_no", "R_ohm", "display_if_not_number", "meter_range_ohm", "bridge_seen_YN", "notes"],
        [[b_feat(d, c, f), g, r, "", "", "", "", ""] for d, c in B_COUPONS for f, g in B_GAPS for r in (1, 2)])
    t["e2_linewidth.csv"] = (
        ["sample_id", "feature", "drawn_mm", "position_no", "measured_mm", "instrument", "magnification", "scale_reference",
         "photo_file", "notes"],
        [[f"{a_cell(d, c, col)}-L16", "line", 2.0, p, "", "", "", "", "", ""] for d, c in A_COUPONS for col, *_ in A_CELLS for p in (1, 2, 3)]
        + [[b_feat(d, c, f), "line", w, p, "", "", "", "", "", ""] for d, c in B_COUPONS for f, w in B_LINES for p in (1, 2, 3)]
        + [[b_feat(d, c, f), "gap", g, p, "", "", "", "", "", ""] for d, c in B_COUPONS for f, g in B_GAPS for p in (1, 2, 3)]
        + [[b_feat(d, c, h), "hole", 2.0, p, "", "", "", "", "", "position 1 and 2 = perpendicular diameters"]
           for d, c in B_COUPONS for h in B_HOLES for p in (1, 2)])
    t["e2_holes.csv"] = (["sample_id", "cut_through_YN", "dowel_fit_slides_tight_no", "notes"],
                         [[b_feat(d, c, h), "", "", ""] for d, c in B_COUPONS for h in B_HOLES])
    t["e2_controls.csv"] = (["session", "date", "control", "nominal_ohm", "reading_ohm", "display_if_not_number", "meter_model",
                             "meter_range", "notes"],
                            [[s, "", ctl, nom, "", "", "", "", ""] for s in ("D1", "D2") for ctl, nom in CONTROLS])
    t["e2_thickness.csv"] = (["sample_id", "location_bare_film_or_lig_pad", "reading_no", "thickness_mm", "instrument", "notes"],
                             [[b_feat(d, c, "W150"), loc, r, "", "", "optional (needs 0.001 mm micrometer)"]
                              for d, c in B_COUPONS for loc in ("bare_film", "lig_pad") for r in (1, 2, 3)])
    t["e2_wet_check.csv"] = (["sample_id", "step", "R_ohm", "display_if_not_number", "meter_range", "drop_volume_uL", "notes"],
                             [[b_feat("D2", "C1", f), s, "", "", "", "20" if "wet" in s else "", "optional preview, DC meter"]
                              for f in ("G100", "G150") for s in ("dry", "wet_10s", "wet_60s", "rinsed_dried_30min")])
    return t


def has_data(path, header):
    """True if any measurement column of an existing CSV has been filled in."""
    if not path.exists():
        return False
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    fixed = {"sample_id", "session", "coupon_id", "drawn_length_mm", "drawn_width_mm", "reading_no", "drawn_gap_mm",
             "feature", "drawn_mm", "position_no", "control", "nominal_ohm", "location_bare_film_or_lig_pad", "step",
             "drop_volume_uL", "notes", "layer_colour", "purpose", "mode_planned", "power_planned", "speed_planned_mm_s",
             "interval_planned_mm", "tape_test_pass_fail"}
    return any(v.strip() for r in rows for k, v in r.items() if k not in fixed and v)


def write_csvs(t, force):
    for name, (header, rows) in t.items():
        p = HERE / name
        if name != "e2_sample_matrix.csv" and has_data(p, header) and not force:
            print(f"KEEP {name}: already contains measurements (not overwritten)")
            continue
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)
        print(f"wrote {name}: {len(rows)} rows")


# ---------------------------------------------------------------- printable bench sheets
CSS = ("body{font-family:sans-serif;font-size:8pt} h1{font-size:13pt;margin:0 0 4px 0} h2{font-size:10pt;margin:8px 0 3px 0}"
       " table{border-collapse:collapse;width:100%} td,th{border:0.6px solid #444;padding:2px 3px;height:13px}"
       " th{background:#ddd;font-size:7pt} p{margin:2px 0}")


def page(title, intro, header, rows, widths=None):
    widths = widths or [None] * len(header)
    th = "".join(f'<th style="width:{w}%">{h}</th>' if w else f"<th>{h}</th>" for h, w in zip(header, widths))
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<h1>{title}</h1><p>{intro}</p><table><tr>{th}</tr>{trs}</table>"


def sheets_pdf(t):
    import pymupdf
    blank = ""
    pages = []
    pages.append(page("E2 sheet 1 - session and film (one column per session)",
                      "Fill at the machine. Write only what you see. Leave blank rather than guess. Session S0 = machine "
                      "check day; D1, D2 = lasing days.",
                      ["Item", "S0", "D1", "D2"], [[h.replace("_", " "), blank, blank, blank] for h in t["e2_session.csv"][0][1:]]))
    log_head = ["Coupon", "Layer", "Planned", "Mode", "Min P", "Max P", "Units", "Speed", "Interval", "Passes", "Scan dir",
                "Order", "Focus", "Photo"]
    log_rows = [[r[0], r[2], f"{r[4]} {r[5]} @ {r[6]}", "", "", "", "", "", "", "", "", "", "", ""] for r in t["e2_machine_log.csv"][1]]
    for i in range(0, len(log_rows), 30):
        pages.append(page("E2 sheet 2 - machine-setting log (copy the values exactly as shown in LaserCAD)",
                          "Photograph every layer dialog. 'Min P / Max P' = the two power fields of the layer. Units = what "
                          "LaserCAD shows next to the field. Scan dir = X or Y.", log_head, log_rows[i:i + 30],
                          [9, 9, 14, 6, 6, 6, 6, 6, 6, 5, 6, 5, 8, 8]))
    res = t["e2_resistance.csv"][1]
    by_strip = {}
    for r in res:
        by_strip.setdefault(r[0], (r[1], r[2]))
    rrows = [[sid, L, W, "", "", "", "", ""] for sid, (L, W) in by_strip.items()]
    for i in range(0, len(rrows), 36):
        pages.append(page("E2 sheet 3 - resistance (2-wire DMM)",
                          "Silver paint on pads, dry 10 min. 3 readings per strip; lift and re-place the probes each time. "
                          "Write OL if over range, and the range.", ["Sample", "L mm", "W mm", "R1 ohm", "R2 ohm", "R3 ohm",
                                                                     "Range", "Contact"], rrows[i:i + 36],
                          [22, 5, 5, 15, 15, 15, 11, 12]))
    lw = t["e2_linewidth.csv"][1]
    by_feat = {}
    for r in lw:
        by_feat.setdefault((r[0], r[1], r[2]), 0)
    lrows = [[sid, kind, dr, "", "", "", "", ""] for sid, kind, dr in by_feat]
    for i in range(0, len(lrows), 36):
        pages.append(page("E2 sheet 4 - line width, gap and hole size (microscope)",
                          "Lines and gaps: 3 positions (left, centre, right of the 16 mm length). Holes: 2 perpendicular "
                          "diameters. Note the scale used.", ["Sample", "Feature", "Drawn mm", "Pos 1 mm", "Pos 2 mm",
                                                              "Pos 3 mm", "Magnif.", "Photo"], lrows[i:i + 36],
                          [22, 7, 7, 15, 15, 15, 8, 11]))
    iso = {}
    for r in t["e2_isolation.csv"][1]:
        iso.setdefault(r[0], r[1])
    pages.append(page("E2 sheet 5 - isolation between two lines (highest resistance range)",
                      "Probe pad A (lower left) and pad B (upper right). 2 readings. Then look at the gap under the "
                      "microscope: any black bridge? Pass needs > 3 Mohm (10 x the reader's 300 kohm 'dry' threshold).",
                      ["Sample", "Gap mm", "Reading 1", "Reading 2", "Range ohm", "Bridge seen Y/N", "Notes"],
                      [[s, g, "", "", "", "", ""] for s, g in iso.items()]))
    vis = [[r[0], "", "", "", "" if r[0].startswith("E2-A") else "n/a", ""] for r in t["e2_visual.csv"][1]]
    pages.append(page("E2 sheet 6 - visual grade (0 none, 1 brown, 2 patchy black, 3 continuous black, 4 flaking, 5 burn-through)",
                      "Grade right after lasing, with a macro photo and a ruler in frame. Tape test only on Part A L08 strips, "
                      "LAST (destructive).", ["Sample", "Grade", "Continuous Y/N", "Burn-through Y/N", "Tape pass/fail", "Photo"], vis))
    ctrl = [[r[0], r[2], r[3], "", "", ""] for r in t["e2_controls.csv"][1]]
    holes = [[r[0], "", "", ""] for r in t["e2_holes.csv"][1]]
    html = page("E2 sheet 7 - controls (every measuring session)", "Same meter and leads as the samples.",
                ["Session", "Control", "Nominal ohm", "Reading", "Range", "Notes"], ctrl)
    html += "<h2>Laser-cut holes</h2>" + page("", "Try a 2.00 mm dowel pin (or a 2.00 mm drill shank) in each hole.",
                                               ["Sample", "Cut through Y/N", "Dowel: slides / tight / no", "Notes"], holes)
    pages.append(html)

    out = HERE / "E2_bench_sheets.pdf"
    writer = pymupdf.DocumentWriter(str(out))
    mediabox = pymupdf.paper_rect("a4-l")
    where = mediabox + (28, 28, -28, -28)
    for html in pages:
        story = pymupdf.Story(html=html, user_css=CSS)
        more = True
        while more:
            dev = writer.begin_page(mediabox)
            more, _ = story.place(where)
            story.draw(dev)
            writer.end_page()
    writer.close()
    n = pymupdf.open(out).page_count
    print(f"wrote E2_bench_sheets.pdf: {n} pages (A4 landscape)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="overwrite CSVs even if they contain data (only before E2 starts)")
    a = ap.parse_args()
    t = tables()
    write_csvs(t, a.force)
    sheets_pdf(t)

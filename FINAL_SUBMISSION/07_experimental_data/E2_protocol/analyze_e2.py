"""
Analyse E2 (fabrication validation) from the raw data files. Applies the rules pre-registered in E2_procedure.md.

Reads   e2_resistance.csv, e2_linewidth.csv, e2_isolation.csv, e2_visual.csv, e2_holes.csv, e2_thickness.csv,
        e2_controls.csv (rows with empty measurement fields are ignored; nothing is averaged by hand)
Writes  e2_summary.md, e2_plots.png and, only when real measurements exist, measured_process.json
        (read by 06_cad/verify_cad.py to check the strip design against what the laser actually made).
A data folder containing SYNTHETIC_DATA.txt is test data: the outputs are stamped SYNTHETIC and never MEASURED.
Usage:  python analyze_e2.py [data_dir]          (default: this folder)
"""
import csv
import json
import math
import statistics as st
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ISO_MIN_OHM = 3e6           # [DES] 10 x the reader's 300 kOhm "dry" threshold
RS_WINDOW = 0.30            # [DES] narrow line "reliable" if its Rs is within +/-30 % of the 1.5 mm line
LEAD_MM = 85.0              # strip v0.1 pad -> zone C lead length (verify_cad uses the same)
REF = ("GREEN", "MAGENTA")


def num(v):
    try:
        x = float(str(v).strip())
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def read(d, name):
    p = d / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def cv(xs):
    return 100 * st.stdev(xs) / st.mean(xs) if len(xs) > 1 and st.mean(xs) else None


def fit_line(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - sum((y - a - b * x) ** 2 for x, y in zip(xs, ys)) / ss_tot if ss_tot else 1.0
    return b, a, r2


def analyse(d):
    res, lw, iso = read(d, "e2_resistance.csv"), read(d, "e2_linewidth.csv"), read(d, "e2_isolation.csv")
    vis = {r["sample_id"]: r for r in read(d, "e2_visual.csv")}
    holes, thick = read(d, "e2_holes.csv"), read(d, "e2_thickness.csv")
    out = {"synthetic": (d / "SYNTHETIC_DATA.txt").exists(), "generated": time.strftime("%Y-%m-%d %H:%M")}

    # ---- raw readings: R per sample (median of the readings; OL -> infinite)
    R, opens = {}, set()
    for r in res:
        v = num(r["R_ohm"])
        if v is not None:
            R.setdefault(r["sample_id"], []).append(v)
        elif r.get("display_if_not_number", "").strip().upper().startswith("OL"):
            opens.add(r["sample_id"])
    W = {}
    for r in lw:
        v = num(r["measured_mm"])
        if v is not None:
            W.setdefault((r["sample_id"], r["feature"]), []).append((num(r["drawn_mm"]), v))
    out["counts"] = {"resistance_readings": sum(len(v) for v in R.values()), "width_readings": sum(len(v) for v in W.values()),
                     "isolation_readings": sum(1 for r in iso if num(r["R_ohm"]) is not None or r["display_if_not_number"].strip())}
    if not out["counts"]["resistance_readings"]:
        out["status"] = "NO DATA"
        return out

    def grade(cell):
        return num(vis.get(cell, {}).get("grade_0to5"))

    # ---- Part A: transmission-line fit per cell (R = Rs * L / W + R0)
    cells = {}
    for sid, vals in R.items():
        if sid.startswith("E2-A-") and sid[-4:-2] == "-L":
            cells.setdefault(sid[:-4], {})[int(sid[-2:])] = st.median(vals)
    tlm = {}
    for cell, byL in cells.items():
        if len(byL) < 3:
            continue
        w_meas = [m for _, m in W.get((cell + "-L16", "line"), [])]
        w = st.median(w_meas) if w_meas else 2.0
        Ls = sorted(byL)
        slope, r0, r2 = fit_line(Ls, [byL[L] for L in Ls])
        v = vis.get(cell, {})
        rule = (grade(cell) == 3 and r2 >= 0.95 and byL.get(24, math.inf) < 1e6
                and v.get("tape_test_pass_fail", "").strip().lower() == "pass" and v.get("burn_through_YN", "").strip().upper() != "Y")
        tlm[cell] = {"Rs_ohm_sq": slope * w, "R0_ohm": r0, "R2": r2, "width_used_mm": w,
                     "width_measured": bool(w_meas), "lig_rule_pass": rule}
    out["part_A_cells"] = tlm
    cond = {}
    for cell, t in tlm.items():
        cond.setdefault(cell.split("-")[-1], []).append(t["lig_rule_pass"])
    out["process_window"] = {c: f"{sum(p)}/{len(p)} pass" + (" -> IN WINDOW" if sum(p) >= 3 else "") for c, p in sorted(cond.items())}
    ref = {c: t for c, t in tlm.items() if c.split("-")[-1] in REF}
    if ref:
        rs = [t["Rs_ohm_sq"] for t in ref.values()]
        d1 = [t["Rs_ohm_sq"] for c, t in ref.items() if "-D1-" in c]
        d2 = [t["Rs_ohm_sq"] for c, t in ref.items() if "-D2-" in c]
        c_all = cv(rs)
        out["sheet_resistance_ohm_sq"] = {
            "median": st.median(rs), "n": len(rs), "cv_pct": c_all, "cv_day1_pct": cv(d1), "cv_day2_pct": cv(d2),
            "day_medians": [st.median(x) if x else None for x in (d1, d2)],
            "verdict": None if c_all is None else "reproducible" if c_all <= 20 else "marginal" if c_all <= 40 else "NOT reproducible"}
        out["contact_R0_ohm"] = st.median([t["R0_ohm"] for t in ref.values()])

    # ---- Part B: line growth and smallest reliable line
    growth, by_w = [], {}
    for (sid, feat), pairs in W.items():
        if feat == "line" and sid.startswith("E2-B-"):
            drawn = pairs[0][0]
            g = st.median([m for _, m in pairs]) - drawn
            by_w.setdefault(drawn, []).append(g)
            if drawn >= 0.8:
                growth.append(g)
    if growth:
        out["line_growth_mm"] = st.median(growth)
        out["line_growth_by_width_mm"] = {f"{k:.1f}": st.median(v) for k, v in sorted(by_w.items())}
    gaps_meas = {}
    for (sid, feat), pairs in W.items():
        if feat == "gap":
            gaps_meas.setdefault(pairs[0][0], []).append(st.median([m for _, m in pairs]))
    out["gap_measured_mm"] = {f"{k:.1f}": st.median(v) for k, v in sorted(gaps_meas.items())}
    r0 = out.get("contact_R0_ohm")
    lines = {}
    for sid in {s for s in list(R) + list(opens) if s.startswith("E2-B-") and s.split("-")[-1].startswith("W")}:
        cpl, feat = sid.rsplit("-", 1)
        drawn = int(feat[1:]) / 100
        pairs = W.get((sid, "line"), [])
        w = st.median([m for _, m in pairs]) if pairs else drawn + out.get("line_growth_mm", 0.0)
        rs = None
        if sid in R and r0 is not None and sid not in opens:
            rs = (st.median(R[sid]) - r0) * w / 16.0
        lines.setdefault(drawn, []).append({"coupon": cpl, "Rs": rs, "grade": grade(sid), "open": sid in opens})
    rs_ref = {c["coupon"]: c["Rs"] for c in lines.get(1.5, []) if c["Rs"]}
    reliable = {}
    for drawn, reps in sorted(lines.items()):
        ok = len(reps) >= 2 and all(r["Rs"] is not None and r["grade"] == 3 and not r["open"] and r["coupon"] in rs_ref
                                    and abs(r["Rs"] / rs_ref[r["coupon"]] - 1) <= RS_WINDOW for r in reps)
        reliable[drawn] = ok
    out["line_reliable_by_width"] = {f"{k:.1f}": v for k, v in reliable.items()}
    passing = [w for w in sorted(reliable) if all(reliable[x] for x in reliable if x >= w)]
    if reliable:
        out["min_reliable_line_mm"] = passing[0] if passing else None

    # ---- isolation: smallest gap above which every replicate exceeds ISO_MIN_OHM with no visible bridge
    by_gap = {}
    for r in iso:
        g = num(r["drawn_gap_mm"])
        v, disp, rng = num(r["R_ohm"]), r["display_if_not_number"].strip().upper(), num(r["meter_range_ohm"])
        if v is None and not disp:
            continue
        if v is not None:
            ok = v > ISO_MIN_OHM
        else:
            ok = disp.startswith("OL") and rng is not None and rng >= ISO_MIN_OHM
        ok = ok and r["bridge_seen_YN"].strip().upper() != "Y"
        by_gap.setdefault(g, []).append(ok)
    if by_gap:
        out["isolation_by_gap"] = {f"{g:.1f}": f"{sum(v)}/{len(v)} > {ISO_MIN_OHM / 1e6:.0f} Mohm" for g, v in sorted(by_gap.items())}
        good = [g for g in sorted(by_gap) if all(all(by_gap[x]) and len(by_gap[x]) >= 2 for x in by_gap if x >= g)]
        out["min_isolating_gap_mm"] = good[0] if good else None
        out["isolation_threshold_ohm"] = ISO_MIN_OHM

    # ---- holes and LIG relief
    hd = {}
    for (sid, feat), pairs in W.items():
        if feat == "hole":
            hd[sid] = st.mean([m for _, m in pairs])
    if hd:
        out["cut_hole_d_mm"] = st.median(hd.values())
        out["dowel_fit"] = {h["sample_id"]: h["dowel_fit_slides_tight_no"] for h in holes if h["dowel_fit_slides_tight_no"].strip()}
    tk = {}
    for t in thick:
        v = num(t["thickness_mm"])
        if v is not None:
            tk.setdefault(t["location_bare_film_or_lig_pad"], []).append(v)
    if tk.get("bare_film") and tk.get("lig_pad"):
        out["lig_relief_mm"] = st.median(tk["lig_pad"]) - st.median(tk["bare_film"])

    # ---- strip v0.1 buildability (same rules as 06_cad/verify_cad.py)
    geo = json.loads((HERE.parent / "strip_v0_1_geometry.json").read_text())["parameters"]
    chk = {}
    if out.get("min_reliable_line_mm") is not None:
        chk["trace width F >= smallest reliable line"] = geo["F"] >= out["min_reliable_line_mm"]
    if out.get("min_isolating_gap_mm") is not None and "line_growth_mm" in out:
        chk["as-built min clearance >= smallest isolating gap"] = geo["MIN_CLEAR"] - out["line_growth_mm"] >= out["min_isolating_gap_mm"]
    if "sheet_resistance_ohm_sq" in out:
        r_lead = out["sheet_resistance_ohm_sq"]["median"] * LEAD_MM / (geo["F"] + out.get("line_growth_mm", 0.0))
        out["predicted_lead_R_ohm"] = r_lead
        chk["lead resistance <= 10 kOhm"] = r_lead <= 1e4
    if "cut_hole_d_mm" in out:
        chk["laser-cut hole 2.00-2.10 mm"] = 2.0 <= out["cut_hole_d_mm"] <= 2.10
    out["strip_v0_1_checks"] = chk
    out["status"] = "SYNTHETIC TEST DATA - NOT A MEASUREMENT" if out["synthetic"] else "MEASURED (evidence B)"
    out["material_note"] = "Laser-carbonised conductive layer (LIG-like). Graphene NOT confirmed (no Raman)."
    return out


def plots(out, d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    cells = out.get("part_A_cells", {})
    names = sorted(cells)
    ax[0].bar(range(len(names)), [cells[n]["Rs_ohm_sq"] for n in names],
              color=["tab:green" if cells[n]["lig_rule_pass"] else "tab:red" for n in names])
    ax[0].set_xticks(range(len(names)), [n.replace("E2-A-", "") for n in names], rotation=90, fontsize=6)
    ax[0].set_ylabel("Rs (ohm/sq)")
    ax[0].set_title("Part A sheet resistance per cell\n(green = passes the LIG-like rule)", fontsize=9)
    g = out.get("line_growth_by_width_mm", {})
    ax[1].plot([float(k) for k in g], list(g.values()), "o-")
    ax[1].axhline(0, color="0.6", lw=0.8)
    ax[1].set_xlabel("drawn line width (mm)")
    ax[1].set_ylabel("measured - drawn (mm)")
    ax[1].set_title("Part B line growth", fontsize=9)
    iso = out.get("isolation_by_gap", {})
    frac = [int(v.split("/")[0]) / int(v.split("/")[1].split()[0]) for v in iso.values()]
    ax[2].bar(list(iso), frac, color=["tab:green" if f == 1 else "tab:red" for f in frac])
    ax[2].set_xlabel("drawn gap (mm)")
    ax[2].set_ylabel(f"fraction > {ISO_MIN_OHM / 1e6:.0f} Mohm")
    ax[2].set_title("Part B isolation", fontsize=9)
    if out["synthetic"]:
        fig.suptitle("SYNTHETIC TEST DATA - NOT A MEASUREMENT", color="red", fontsize=12)
    fig.tight_layout()
    fig.savefig(d / "e2_plots.png", dpi=130)
    plt.close(fig)


def fmt(v, nd=3):
    return "-" if v is None else f"{v:.{nd}g}" if isinstance(v, float) else str(v)


def write(out, d):
    lines = [f"# E2 summary ({out['generated']})", "", f"**Status: {out['status']}**", ""]
    if out["status"] == "NO DATA":
        lines += ["No measurements entered yet. Fill the e2_*.csv files (see E2_procedure.md) and run again.",
                  "measured_process.json is NOT written until real data exists."]
        (d / "e2_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        stale = d / "measured_process.json"
        if stale.exists() and not out["synthetic"]:
            stale.unlink()      # never leave numbers that no longer have data behind them
        return
    rs = out.get("sheet_resistance_ohm_sq", {})
    lines += [f"- {out['material_note']}",
              f"- Readings used: {out['counts']}",
              f"- Reference sheet resistance: median {fmt(rs.get('median'))} ohm/sq, n = {rs.get('n')}, CV {fmt(rs.get('cv_pct'))} % "
              f"(day 1 {fmt(rs.get('cv_day1_pct'))} %, day 2 {fmt(rs.get('cv_day2_pct'))} %) -> **{rs.get('verdict')}**",
              f"- Contact + pad resistance R0 (median): {fmt(out.get('contact_R0_ohm'))} ohm",
              f"- Line growth (median, lines >= 0.8 mm): {fmt(out.get('line_growth_mm'))} mm; by width {out.get('line_growth_by_width_mm')}",
              f"- Smallest reliable line: **{fmt(out.get('min_reliable_line_mm'))} mm** ({out.get('line_reliable_by_width')})",
              f"- Smallest isolating gap: **{fmt(out.get('min_isolating_gap_mm'))} mm** ({out.get('isolation_by_gap')})",
              f"- Measured gaps: {out.get('gap_measured_mm')}",
              f"- Laser-cut hole: {fmt(out.get('cut_hole_d_mm'))} mm; dowel fit {out.get('dowel_fit')}",
              f"- LIG relief above the film: {fmt(out.get('lig_relief_mm'))} mm",
              f"- Predicted strip v0.1 lead resistance ({LEAD_MM:.0f} mm): {fmt(out.get('predicted_lead_R_ohm'))} ohm", "",
              "## Process window (Part A, >= 3 of 4 cells pass)", ""] + [f"- {k}: {v}" for k, v in out["process_window"].items()]
    lines += ["", "## Strip v0.1 as drawn", ""] + [f"- {'PASS' if v else 'FAIL'}: {k}" for k, v in out["strip_v0_1_checks"].items()]
    lines += ["", "## Part A cells", "", "| Cell | Rs ohm/sq | R0 ohm | R2 | width used | rule |", "|---|---|---|---|---|---|"]
    lines += [f"| {c} | {t['Rs_ohm_sq']:.3g} | {t['R0_ohm']:.3g} | {t['R2']:.3f} | {t['width_used_mm']:.2f}"
              f"{'' if t['width_measured'] else ' (drawn)'} | {'pass' if t['lig_rule_pass'] else 'fail'} |"
              for c, t in sorted(out.get("part_A_cells", {}).items())]
    (d / "e2_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (d / "measured_process.json").write_text(json.dumps(out, indent=1, default=str))
    plots(out, d)


def main():
    d = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE
    out = analyse(d)
    write(out, d)
    print(f"{out['status']}: summary written to {d / 'e2_summary.md'}")
    return out


if __name__ == "__main__":
    main()

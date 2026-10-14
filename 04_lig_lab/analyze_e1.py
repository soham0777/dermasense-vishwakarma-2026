"""
Experiment E1 analysis: raw CSVs -> per-cell sheet resistance -> per-condition statistics.

Inputs (raw, filled at the bench): e1_samples.csv, e1_resistance.csv, e1_linewidth.csv
Outputs: e1_summary_cells.csv, e1_summary_conditions.csv, e1_plots.png

Method (pre-registered in E1_protocol.md):
  * per strip: median of the repeat readings
  * per cell: least-squares line R = (Rs / W) * L + R0 through the 8/16/24 mm strips
    Rs = slope * W, using the MEASURED strip width (drawn 2.00 mm used only if no
    width was measured - flagged), R0 = pads + contacts
  * cell passes "LIG-like conductive layer" if: visual grade = 3 (continuous black),
    no burn-through, tape test pass, R^2 >= 0.95, R(24 mm) < 1 MOhm
  * reproducibility of the reference condition: CV = SD / mean of Rs
Usage:  python analyze_e1.py [folder]
"""
import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

DRAWN_WIDTH_MM = 2.00
LENGTHS_MM = (8.0, 16.0, 24.0)


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(str(x).strip())
    except (TypeError, ValueError):
        return None


def fit_line(points):
    n = len(points)
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points)
    slope = sum((p[0] - mx) * (p[1] - my) for p in points) / sxx
    icpt = my - slope * mx
    ss_tot = sum((p[1] - my) ** 2 for p in points)
    ss_res = sum((p[1] - (slope * p[0] + icpt)) ** 2 for p in points)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else None
    return slope, icpt, (r2 if n >= 3 else None)


def cv(values):
    return st.stdev(values) / st.mean(values) * 100 if len(values) >= 2 else None


def main(folder="."):
    folder = Path(folder)
    samples = {r["sample_id"]: r for r in rows(folder / "e1_samples.csv")}
    readings = defaultdict(list)                     # (sample, length) -> [R]
    for r in rows(folder / "e1_resistance.csv"):
        R, L = num(r["R_ohm"]), num(r["strip_length_mm"])
        if R is not None and L is not None:
            readings[(r["sample_id"], L)].append(R)
    widths = defaultdict(list)
    for r in rows(folder / "e1_linewidth.csv"):
        w = num(r["measured_mm"])
        if w is not None and abs((num(r["drawn_mm"]) or 0) - DRAWN_WIDTH_MM) < 1e-6:
            widths[r["sample_id"]].append(w)

    cells = []
    for sid, s in samples.items():
        grade = num(s["visual_grade_0to5"])
        if grade is None and not any((sid, L) in readings for L in LENGTHS_MM):
            continue                                  # planned but not yet made
        pts = [(L, st.median(readings[(sid, L)])) for L in LENGTHS_MM if (sid, L) in readings]
        w_meas = st.mean(widths[sid]) if widths[sid] else None
        W = w_meas if w_meas else DRAWN_WIDTH_MM
        rs = r0 = r2 = None
        flags = []
        if w_meas is None:
            flags.append("width not measured (drawn 2.00 mm used)")
        if len(pts) >= 2:
            slope, r0, r2 = fit_line(pts)
            rs = slope * W
            if slope <= 0:
                flags.append("R does not increase with length - recheck contacts")
        else:
            flags.append("fewer than 2 strip lengths measured")
        r24 = dict(pts).get(24.0)
        lig_like = (grade == 3 and s["burn_through_YN"].strip().upper() == "N"
                    and s["tape_test_pass_fail"].strip().lower() == "pass"
                    and r2 is not None and r2 >= 0.95 and r24 is not None and r24 < 1e6
                    and rs is not None and rs > 0)
        cells.append({
            "sample_id": sid, "day": s["day"], "coupon": s["coupon"], "cell_colour": s["cell_colour"],
            "power_setting": s["power_setting"], "speed_mm_s": s["speed_mm_s"], "speed_rule": s["speed_rule"],
            "tube_current_mA": s["tube_current_mA"], "visual_grade": s["visual_grade_0to5"],
            "width_measured_mm": f"{w_meas:.3f}" if w_meas else "",
            "Rs_ohm_sq": f"{rs:.2f}" if rs else "", "R0_ohm": f"{r0:.1f}" if r0 is not None else "",
            "R2": f"{r2:.3f}" if r2 is not None else "", "lig_like": "YES" if lig_like else "no",
            "flags": "; ".join(flags)})

    if not cells:
        print("No measured cells yet. Fill e1_samples.csv / e1_resistance.csv after the lab session.")
        return

    out_cells = folder / "e1_summary_cells.csv"
    with open(out_cells, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cells[0])); w.writeheader(); w.writerows(cells)

    # per condition = (power, speed rule, speed)
    groups = defaultdict(list)
    for c in cells:
        groups[(c["power_setting"], c["speed_rule"], c["speed_mm_s"])].append(c)
    summary = []
    print(f"{'power':>6} {'speed':>12} {'n':>3} {'LIG-like':>9} {'Rs mean':>9} {'SD':>7} {'CV%':>6}")
    for (p, rule, spd), cs in sorted(groups.items()):
        vals = [float(c["Rs_ohm_sq"]) for c in cs if c["lig_like"] == "YES"]
        m = st.mean(vals) if vals else None
        sd = st.stdev(vals) if len(vals) >= 2 else None
        c_v = cv(vals)
        summary.append({"power_setting": p, "speed_rule": rule, "speed_mm_s": spd, "n_cells": len(cs),
                        "n_lig_like": len(vals), "Rs_mean": f"{m:.2f}" if m else "",
                        "Rs_sd": f"{sd:.2f}" if sd else "", "Rs_cv_pct": f"{c_v:.1f}" if c_v else "",
                        "in_window": "YES" if len(vals) >= 3 and len(vals) >= 0.75 * len(cs) else "no"})
        print(f"{p:>6} {(spd or rule):>12} {len(cs):>3} {len(vals):>9} "
              f"{(f'{m:.1f}' if m else '-'):>9} {(f'{sd:.1f}' if sd else '-'):>7} {(f'{c_v:.1f}' if c_v else '-'):>6}")
    with open(folder / "e1_summary_conditions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)

    # reproducibility of the reference (GREEN + MAGENTA cells at setting 12, speed rule S_ref)
    ref = [c for c in cells if c["cell_colour"] in ("GREEN", "MAGENTA") and c["speed_rule"] == "S_ref"
           and c["lig_like"] == "YES"]
    by_day = defaultdict(list)
    for c in ref:
        by_day[c["day"]].append(float(c["Rs_ohm_sq"]))
    print("\nReference condition (setting 12, S_ref):")
    for d, v in sorted(by_day.items()):
        cvd = cv(v)
        print(f"  day {d}: n={len(v)}, mean={st.mean(v):.1f} ohm/sq, CV={'%.1f %%' % cvd if cvd else 'n<2'}")
    all_ref = [float(c["Rs_ohm_sq"]) for c in ref]
    if len(all_ref) >= 2:
        cva = cv(all_ref)
        verdict = "REPRODUCIBLE" if cva <= 20 else "MARGINAL" if cva <= 40 else "NOT REPRODUCIBLE"
        print(f"  all days: n={len(all_ref)}, CV={cva:.1f} %  ->  {verdict} (rule: <=20 / 20-40 / >40 %)")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for c in cells:
        if c["lig_like"] != "YES":
            continue
        x_power = float(c["power_setting"])
        mk = "o" if c["day"] in ("1", "R") else "s"
        if c["speed_rule"] == "S_ref":
            axes[0].plot(x_power, float(c["Rs_ohm_sq"]), mk, color="C0" if c["day"] == "1" else "C1")
        if c["power_setting"] == "12" and c["speed_mm_s"]:
            axes[1].plot(float(c["speed_mm_s"]), float(c["Rs_ohm_sq"]), mk, color="C0" if c["day"] == "1" else "C1")
    axes[0].set_xlabel("Power setting (as entered, units per machine_record)")
    axes[1].set_xlabel("Speed (mm/s) at setting 12")
    for ax in axes:
        ax.set_ylabel("Sheet resistance (ohm/sq)")
        ax.grid(alpha=0.3)
    fig.suptitle("E1 - our measured data (blue: day 1, orange: day 2)")
    fig.tight_layout()
    fig.savefig(folder / "e1_plots.png", dpi=150)
    print(f"\nWrote {out_cells.name}, e1_summary_conditions.csv, e1_plots.png")


if __name__ == "__main__":
    main(*sys.argv[1:])

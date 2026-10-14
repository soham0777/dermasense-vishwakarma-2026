"""
Turn laser_log.csv into sheet resistance numbers and one plot.

For each row we fit a straight line through (strip length, measured resistance):
    R = (Rs / W) * L + R0
    Rs = slope x W   -> sheet resistance, ohm/sq (strip width W = 2 mm)
    R0 = intercept   -> pads + probe contacts, ohm

A good row has a clean straight line (R^2 close to 1) and a small, positive R0.
A bad fit almost always means a poor probe contact: re-measure with silver paint.

Usage:  python analyze_log.py            (reads laser_log.csv, writes lig_window.png)
"""
import csv
import sys
from collections import defaultdict

STRIP_W = 2.0  # mm, must match make_test_pattern.py
LENGTH_COLUMNS = {8.0: "R_8mm_ohm", 16.0: "R_16mm_ohm", 24.0: "R_24mm_ohm"}


def fit(points):
    """Least-squares line through (x, y) points. Returns slope, intercept, r2 (None if 2 points)."""
    n = len(points)
    mx = sum(x for x, _ in points) / n
    my = sum(y for _, y in points) / n
    sxx = sum((x - mx) ** 2 for x, _ in points)
    slope = sum((x - mx) * (y - my) for x, y in points) / sxx
    intercept = my - slope * mx
    if n < 3:
        return slope, intercept, None
    ss_tot = sum((y - my) ** 2 for _, y in points)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in points)
    return slope, intercept, (1 - ss_res / ss_tot) if ss_tot else 1.0


def number(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def main(path="laser_log.csv"):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("laser_log.csv has no rows yet. Fill it in after the first laser run.")
        return

    results = []
    print(f"{'run':<8}{'speed':>6}{'power%':>8}  {'look':<15}{'Rs ohm/sq':>10}{'R0 ohm':>8}{'R^2':>6}  flag")
    for r in rows:
        pts = [(L, number(r.get(col))) for L, col in LENGTH_COLUMNS.items()]
        pts = [(L, R) for L, R in pts if R is not None]
        rs = r0 = r2 = None
        flag = ""
        if len(pts) >= 2:
            slope, r0, r2 = fit(pts)
            rs = slope * STRIP_W
            if rs <= 0:
                flag = "longer strip should read higher, re-measure"
            elif r0 < 0 or (r2 is not None and r2 < 0.95):
                flag = "poor contacts? re-measure"
        else:
            flag = "not conductive / not measured"
        results.append((r, rs, flag))
        print(f"{r['run_id']:<8}{r['speed_mm_s']:>6}{r['power_pct']:>8}  {r['look'][:14]:<15}"
              f"{(f'{rs:.1f}' if rs else '-'):>10}{(f'{r0:.0f}' if r0 is not None else '-'):>8}"
              f"{(f'{r2:.2f}' if r2 is not None else '-'):>6}  {flag}")

    good = [(r, rs) for r, rs, flag in results
            if rs and rs > 0 and not flag and r["tape_test"].strip().lower() == "pass"]
    if good:
        best_row, best_rs = min(good, key=lambda t: t[1])
        print(f"\nBest so far (clean fit, passed tape test): {best_rs:.1f} ohm/sq  ->  run {best_row['run_id']}, "
              f"{best_row['power_pct']}% at {best_row['speed_mm_s']} mm/s, focus: {best_row['focus']}, "
              f"interval {best_row['interval_mm']} mm")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib not installed - skipping plot)")
        return
    groups = defaultdict(list)
    for r, rs, flag in results:
        if rs and rs > 0 and not flag:
            groups[f"{r['speed_mm_s']} mm/s, focus {r['focus']}, {r['film']}"].append((number(r["power_pct"]), rs))
    if not groups:
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, pts in sorted(groups.items()):
        pts.sort()
        ax.plot([p for p, _ in pts], [s for _, s in pts], "o-", label=label)
    ax.set_yscale("log")
    ax.set_xlabel("Laser power setting (%)")
    ax.set_ylabel("Sheet resistance (ohm/sq, log scale)")
    ax.set_title("Our LIG process window")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("lig_window.png", dpi=150)
    print("Saved lig_window.png")


if __name__ == "__main__":
    main(*sys.argv[1:])

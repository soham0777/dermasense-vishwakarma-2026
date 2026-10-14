"""
Battery-life estimate for the pod.

Every input below is an ASSUMPTION until we measure it (test T-EL-03).
Replace the numbers with measured currents and re-run:  python power_budget.py
"""

SCENARIOS = {
    # name: (sleep_mA, measure_s, measure_mA, radio_s, radio_mA)
    "Custom board, lean firmware": (0.020, 1.0, 25.0, 0.5, 40.0),
    "Custom board, pessimistic":   (0.050, 2.0, 30.0, 2.0, 80.0),
    "Dev board (USB chip + LED)":  (1.000, 1.0, 25.0, 0.5, 40.0),
}
INTERVALS_S = (300, 600)        # one reading every 5 or 10 minutes
BATTERIES_MAH = (150, 300)
USABLE = 0.8                    # use 80 % of rated capacity (ageing, cut-off voltage)
TARGET_DAYS = 7                 # ES-10 / PR-7


def average_mA(sleep, t_meas, i_meas, t_radio, i_radio, interval):
    awake = t_meas + t_radio
    charge = sleep * (interval - awake) + i_meas * t_meas + i_radio * t_radio   # mA*s
    return charge / interval


print(f"{'scenario':30s}{'every':>7}{'avg mA':>9}" + "".join(f"{f'{b} mAh':>10}" for b in BATTERIES_MAH))
for name, (sl, tm, im, tr, ir) in SCENARIOS.items():
    for iv in INTERVALS_S:
        avg = average_mA(sl, tm, im, tr, ir, iv)
        days = [b * USABLE / avg / 24 for b in BATTERIES_MAH]
        cells = "".join(f"{d:8.1f} d{'*' if d < TARGET_DAYS else ' '}" for d in days)
        print(f"{name:30s}{iv // 60:>5} m{avg:9.3f}{cells}")
print(f"\n* = misses the {TARGET_DAYS}-day target. All inputs are assumptions until measured (T-EL-03).")

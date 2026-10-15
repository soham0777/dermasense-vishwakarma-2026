"""
Design FMEA v0.1 for the two-zone strip, contact clamp and bench reader. Writes fmea_v0_1.csv and fmea_v0_1.md.
Ratings 1-10 are engineering estimates [EST] made before any test data; every line names the test or design action
that will replace the estimate. S = severity, O = occurrence, D = detection (10 = cannot detect). RPN = S x O x D.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = [  # id, item, failure mode, effect, S, cause, O, current control, D, action, verified by
    ("F01", "Zone electrodes (LIG)", "Layer not conductive / Rs far higher than expected", "Zones always read dry: CHANGE missed", 7,
     "Laser setting or focus drift, film lot", 5, "E2 Rs + CV acceptance; per-strip dry/loop check before use", 4,
     "Run E2; add a per-strip QC record (loop R, both zones dry > 1 Mohm)", "E2"),
    ("F02", "Electrode gap", "Carbon bridges the gap", "Zone reads wet when dry: false CHANGE/CHECK", 6,
     "Line growth larger than the 0.95 mm clearance", 4, "E2 isolation test; start-up rule: both zones must read dry", 3,
     "Set MIN_CLEAR from the E2 smallest isolating gap + growth", "E2"),
    ("F03", "COM loop trace", "Crack or break", "FAULT shown (no wrong state)", 5, "Bending at the dressing edge", 4,
     "Loop continuity measured every scan", 2, "Bend test of 1.0 mm lines at a 10 mm radius", "T-MECH-01"),
    ("F04", "SENSE_C / SENSE_A lead", "Crack or break", "That zone reads open = dry forever: CHANGE missed, no alarm", 7,
     "Bending at the dressing edge", 4, "None (the loop check covers COM only)", 8,
     "v0.2 candidate: loop each SENSE lead to a second pad (6-pad strip) so its continuity is checked every scan",
     "design v0.2 + T-MECH-01"),
    ("F05", "Pogo-pin contact on LIG pad", "High or unstable contact resistance", "Readings drift high (towards dry)", 6,
     "Porous LIG dented by pointed tips, dust, oxidation", 5, "COM pins checked by the loop; silver-painted pads", 4,
     "Rounded-head pins; measure contact R vs clamp cycles", "T-CON-01"),
    ("F06", "Seal registration", "Window shifted onto a lead", "Wet lead read as wet zone: early CHANGE/CHECK", 5,
     "Tape cut or placement error", 4, "DRC: window A is 2.5 mm from the nearest foreign net; alignment holes", 5,
     "Seal jig using the 2 mm dowels; inspect each strip", "E4"),
    ("F07", "Sensing concept", "Exudate front does not reach the windows as assumed", "CHANGE late or never", 7,
     "Dressing wicking differs from the model; strip position", 5, "None yet (concept not validated)", 6,
     "Simulated-exudate test on real bordered foam dressings", "E4"),
    ("F08", "Thresholds", "Dry baseline of a humid dressing below 300 kohm", "False wet", 6, "Humidity, saline residue", 5,
     "Hysteresis + 3-scan persistence", 5, "Measure dry baselines on dressings; adjust config.h with a written reason", "E4"),
    ("F09", "Readout", "Wrong reading from ADC or reference drift", "Wrong state", 7, "Component fault, wiring error", 2,
     "Known 100 k check resistor every scan -> FAULT outside +/-5 %; consistency check of netlist vs firmware", 2,
     "Bench test T2-T10", "BENCH_TEST"),
    ("F10", "Readout", "DC current through wet electrodes", "Electrode corrosion, drift", 4, "Firmware bug leaves a pin driven", 2,
     "Bipolar drive; all pins high-Z between scans", 3, "Bench test T8 (average DC < 5 mV)", "BENCH_TEST"),
    ("F11", "Strip placement", "Strip inserted reversed or off-centre", "Zones swapped: CHECK instead of OK/CHANGE", 5,
     "User error", 3, "CHECK state flags A-before-C; asymmetric paddle", 3, "Orientation mark on the paddle; instructions", "E4"),
    ("F12", "Fabrication", "Operator exposed to polyimide fumes", "Respiratory irritation", 8, "Exhaust off or lid opened early", 3,
     "E2 safety checklist (exhaust check, 30 s wait)", 2, "Checklist signed every session", "E2 safety checklist"),
    ("F13", "Fabrication", "Fire in the laser", "Injury, equipment damage", 9, "Unattended job, too much power", 2,
     "Never unattended; CO2 extinguisher; lowest power first", 2, "Checklist signed every session", "E2 safety checklist"),
    ("F14", "Bench reader", "Mains-connected laptop coupled to a person", "Electric shock path", 9,
     "Using the USB bench reader on a person", 1, "Bench-only rule; 'not for patient use' on schematic and README", 3,
     "Battery-only, isolated design before any human use (out of v0.1 scope)", "design rule"),
    ("F15", "Strip material", "LIG particles shed into the dressing", "Foreign material near the wound", 8,
     "Abrasion, porous carbon", 3, "Strip is outside the wound bed; leads sealed; tape test in E2", 5,
     "Literature and standards review of carbon/polyimide contact; shedding test on wet dressing", "E2 tape test + E4 + review"),
]


def main():
    rows = [r[:4] + (r[4],) + r[5:6] + (r[6],) + r[7:8] + (r[8],) + (r[4] * r[6] * r[8],) + r[9:] for r in ROWS]
    head = ["id", "item", "failure_mode", "effect", "S", "cause", "O", "current_control", "D", "RPN", "action", "verified_by"]
    with open(HERE / "fmea_v0_1.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(head)
        w.writerows(rows)
    top = sorted(rows, key=lambda r: -r[9])
    md = ["# Design FMEA v0.1 (strip + clamp + bench reader)", "",
          "**Status:** first draft (2026-10-14). The S/O/D ratings are engineering **estimates** made before any test data. "
          "Each line names the test that will replace its estimate. Full table: `fmea_v0_1.csv`. Regenerate it with `make_fmea.py`.", "",
          "| Rank | ID | Failure mode | Effect | S | O | D | RPN | Action | Verified by |", "|---|---|---|---|---|---|---|---|---|---|"]
    md += [f"| {i + 1} | {r[0]} | {r[1]}: {r[2]} | {r[3]} | {r[4]} | {r[6]} | {r[8]} | **{r[9]}** | {r[10]} | {r[11]} |"
           for i, r in enumerate(top)]
    md += ["", "**Highest risks:**",
           "- **F07 / F04:** the sensing concept itself, and a broken sense lead that nothing detects.",
           "- **F04 needs a design change** (v0.2: loop each sense lead), not just a test.",
           "- F07 and F08 are retired only by E4 on real dressings."]
    (HERE / "fmea_v0_1.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[6:10]))


if __name__ == "__main__":
    main()

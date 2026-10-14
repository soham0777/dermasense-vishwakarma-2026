"""
Make the LIG test coupon (DXF) for the CO2 laser.

What it draws
-------------
6 test cells in a row along the tape. Each cell sits on its own colour layer,
so in LaserCAD you give each colour a different power.
Each cell has 3 "dog-bone" strips (pad - strip - pad), all 2 mm wide,
with strip lengths of 8, 16 and 24 mm.

Why three lengths? Measured resistance = (sheet resistance x L / W) + contacts.
Plotting R against L gives a straight line: the slope gives the sheet
resistance and the intercept is the probe/contact resistance, so a plain
multimeter is enough. analyze_e1.py / e2/analyze_e2.py do this maths.

Every strip is ONE closed outline. Nothing overlaps, because some laser
software leaves overlapping regions unfilled.

Usage
-----
    python make_test_pattern.py                 # 20 mm wide tape (default)
    python make_test_pattern.py --width 30      # wider film
Output: lig_test_coupon.dxf (in millimetres)
"""
import argparse
import ezdxf

STRIP_W = 2.0                 # strip width, mm
LENGTHS = (8.0, 16.0, 24.0)   # strip lengths, mm
PAD = 4.0                     # square pad size, mm (for probe tip / silver paint)
GAP_Y = 2.0                   # space between strips in a cell, mm
GAP_X = 6.0                   # space between cells, mm
CELLS = 6

# AutoCAD colour numbers 1-6 = red, yellow, green, cyan, blue, magenta.
# These basic colours show up as separate layers in LaserCAD.
CELL_COLOURS = [(1, "RED"), (2, "YELLOW"), (3, "GREEN"),
                (4, "CYAN"), (5, "BLUE"), (6, "MAGENTA")]
OUTLINE_COLOUR = 7            # black/white: cut line around coupon + orientation notch


def dog_bone(x0, yc, length):
    """One closed outline: left pad, strip, right pad. (x0, yc) = left edge, centre line."""
    p, h, w = PAD, PAD / 2, STRIP_W / 2
    x1, x2, x3 = x0 + p, x0 + p + length, x0 + 2 * p + length
    return [(x0, yc - h), (x1, yc - h), (x1, yc - w), (x2, yc - w), (x2, yc - h),
            (x3, yc - h), (x3, yc + h), (x2, yc + h), (x2, yc + w), (x1, yc + w),
            (x1, yc + h), (x0, yc + h)]


def build(width, out):
    stack_h = len(LENGTHS) * PAD + (len(LENGTHS) - 1) * GAP_Y
    if stack_h > width - 2:
        raise SystemExit(f"Film too narrow: need at least {stack_h + 2:.0f} mm, got {width} mm")

    doc = ezdxf.new("R2000", setup=False)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()

    for aci, name in CELL_COLOURS[:CELLS]:
        doc.layers.add(f"CELL_{name}", color=aci)
    doc.layers.add("OUTLINE_CUT", color=OUTLINE_COLOUR)

    cell_len = 2 * PAD + max(LENGTHS)
    y_bottom = (width - stack_h) / 2
    x = 10.0  # leave room for the orientation notch

    for i in range(CELLS):
        layer = f"CELL_{CELL_COLOURS[i][1]}"
        for j, length in enumerate(LENGTHS):
            yc = y_bottom + PAD / 2 + j * (PAD + GAP_Y)
            msp.add_lwpolyline(dog_bone(x, yc, length), close=True,
                               dxfattribs={"layer": layer, "color": 256})
        x += cell_len + GAP_X

    total = x - GAP_X + 5.0
    # Cut outline around the coupon, plus a small triangle notch at the START
    # (cell 1 = red end) so we can always tell which end is which.
    msp.add_lwpolyline([(0, 0), (total, 0), (total, width), (0, width)], close=True,
                       dxfattribs={"layer": "OUTLINE_CUT", "color": 256})
    msp.add_lwpolyline([(2, width / 2 - 2), (6, width / 2), (2, width / 2 + 2)], close=True,
                       dxfattribs={"layer": "OUTLINE_CUT", "color": 256})

    doc.saveas(out)
    print(f"Saved {out}: {total:.0f} mm x {width:.0f} mm, {CELLS} cells x {len(LENGTHS)} strips")
    print("Cell order from the notch end: " + ", ".join(n for _, n in CELL_COLOURS[:CELLS]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--width", type=float, default=20.0, help="film/tape width in mm (default 20)")
    ap.add_argument("--out", default="lig_test_coupon.dxf")
    a = ap.parse_args()
    build(a.width, a.out)

# Step 3: making our first LIG

**Goal:** find the laser settings where Kapton turns into conductive graphene: black, conducts, doesn't flake, no holes. Then make sure we can repeat it.

**You need:**
- the Kapton film or tape
- a flat aluminium plate or glass sheet
- isopropyl alcohol and tissue
- a multimeter
- silver paint (best) or copper tape (OK); bare probe tips work if you have nothing else
- Scotch tape
- a ruler
- a permanent marker
- your phone

## Safety (read before every session)

- Keep the exhaust **on**. Burning polyimide gives off fumes. Don't open the lid until the smoke has cleared, and don't breathe it in.
- **Never leave the laser running unattended**, because film can catch fire.
- Use the lab's laser rules and get the lab in-charge's permission.

## 1. Prepare the film

1. Wipe the film with isopropyl alcohol and let it dry.
2. Stick or tape it **flat** onto the aluminium plate or glass. Push out every bubble, because bubbles change the focus and give uneven results.
3. Write the run ID (R1, R2…) on the film with a marker, next to where the **red** cell will be.

## 2. Set up LaserCAD

1. Make the pattern if you haven't: `python make_test_pattern.py` (or `--width 30` for wider film). This creates `lig_test_coupon.dxf`.
2. Import `lig_test_coupon.dxf`. You should see 6 colour layers, plus a black outline layer.
3. Set the **black outline layer to "Output: No"** for now. Cut the coupon out with scissors later.
4. Set each colour layer to **Scan / Engrave mode** with:
   - **Speed:** the same for all six (the speed of this run)
   - **Min power = Max power** = that colour's power (table below)
   - **Interval (line spacing):** 0.1 mm
   - **Passes:** 1
5. **Focus:** use the machine's normal focus gauge. Write "focus" in the log; defocus is a later experiment.
6. Turn the air assist to **low**, so it doesn't blow the graphene away.

## 3. Run 1 starting settings (a starting guess, not a known recipe)

| Colour | Red | Yellow | Green | Cyan | Blue | Magenta |
|---|---|---|---|---|---|---|
| Power % | 10 | 12 | 14 | 16 | 18 | 20 |

**Speed for Run 1: 300 mm/s.** Then adjust:

| What you see | What to do for the next run |
|---|---|
| Nothing conducts, the film just looks brown | Slow down to **200 mm/s** (same powers) |
| Some cells black and conducting | Good: you've found the window. Repeat at 250 and 350 mm/s to map it |
| Holes, burn-through or curling everywhere | Speed up to **400 mm/s** |
| The tube doesn't fire at 10 % | Note it: that's our tube's minimum. Shift the powers up |

**If the film is thin tape (~25 µm polyimide),** start at **400 mm/s**, because thin film burns through easily.

## 4. Measure each cell

1. **Look** at each cell and write one word: `none`, `brown`, `black`, `black-flaky` or `burned-through`.
2. **Resistance:** measure pad-to-pad on all three strips (8, 16, 24 mm).
   - Best: a small dot of silver paint on each pad, left to dry, then probe the paint.
   - Without silver paint: press the probe tips firmly in the centre of each pad, take 3 readings and write the middle one.
   - The longer strip **must** read higher. If it doesn't, the contact was bad, so measure again.
3. **Tape test** (only after measuring): press Scotch tape onto the **8 mm strip** of that cell and peel it off.
   - `pass`: the tape picks up only a light grey dust and the strip stays solid black.
   - `fail`: black flakes come off.
4. **Photo:**
   - Each coupon next to a ruler, with the run ID visible. Keep the original file.
   - At least once, take one with a team member's college ID card in the frame (the template asks for this).

## 5. Log it and analyse it

- Add **one row per cell** to `laser_log.csv` (open it in Excel, then save as CSV).
- Leave the R columns empty if a cell didn't conduct.
- Then run `python analyze_log.py`. It prints the sheet resistance for every cell, names the best clean setting, and saves `lig_window.png`.

Save photos in `photos/` with names like `2026-10-15_R1_coupon.jpg`, or just keep the phone's original name and write it in the `photo` column.

## Step 3 is done when

- [ ] At least one setting is black, passes the tape test, and has no holes.
- [ ] Its sheet resistance is below 100 Ω/sq. (The original paper got 15–35 Ω/sq, so if we're far above that, we still have room to improve.)
- [ ] The **same setting, run on a different day**, comes within ±20 % of the first result.
- [ ] Everything is logged in the CSV, the photos are saved, and the session is written up in `LAB_NOTEBOOK.md`.

Then send the CSV, the plot and 2–3 photos to Claude for review.

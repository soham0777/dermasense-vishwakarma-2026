# Laser machine record: E2 Session S0 (fill in at the machine, about 20 min)

**Rule:** write only what you **see**: on the machine label, the control panel, or the LaserCAD screen. Leave a field empty rather than guess.

## Already known from the LaserCAD config on our laptop `[A3]`

These come from `C:\LaserCAD\AWCCfg\SysCfg.ini`, the laptop copy. **Confirm that they match the lab machine.**

| Item | Value in config | Matches the lab machine? (Y/N) |
|---|---|---|
| Software | LaserCAD V8.28 (AWC controller family) | |
| Work area | X 1200 mm × Y 900 mm | |
| Max axis speed | X 500 mm/s, Y 400 mm/s | |
| PWM frequency | 20,000 Hz | |
| Max power limit | 98 (%) | |

## To record at the machine

| Item | Write it here | How to find it |
|---|---|---|
| Machine make / model | | Nameplate on the machine body |
| Controller model | | Panel label (e.g. AWC708 / AWC608) |
| Laser tube rating (W) and brand | | Sticker on the tube (open the rear cover only with the lab in-charge) |
| Lens focal length | | Lens holder label or the lab in-charge |
| Is there a current meter (mA) on the panel? | Y / N | Analog needle or digital display |
| Chiller model and water temperature | | Chiller display |
| **Where was "12" set during the earlier trial?** | LaserCAD layer dialog / machine panel / power-supply knob / don't know | Ask whoever ran it |
| **Units shown next to the power field in LaserCAD** | | Open any layer → layer parameters → power fields |
| Earlier trial: speed, interval, passes, focus, film used | | Memory, notes, phone photos of the screen |

## Setting → tube current check (only if a mA meter exists)

1. Put a scrap of the same film on the bed.
2. Run a 30 × 10 mm fill at 100 mm/s for each setting below.
3. Read the meter during each fill and write it in `e2_experiment/e2_machine_log.csv` (column `tube_current_mA`).
4. If the needle flickers, write the min–max range. **That flicker is itself a finding.**

Settings: 8, 10, 12, 14, 16, 20 (%), or whatever the lowest setting is at which the tube fires.

**Why this matters:**
- "12" is most likely a **12 % PWM command**, *not* 12 W `[C5]`.
- Below about 25 % PWM, glass tubes can fire unstably `[C4]`.
- Tube current is the cheapest physical check we have on what the laser actually delivered.

## Film

| Item | Value |
|---|---|
| Product name / brand / supplier (photo of the label) | |
| Form: sheet / roll / tape (adhesive Y/N) | |
| Thickness: 5 micrometer readings (mm) | ___ / ___ / ___ / ___ / ___ |
| If tape: total minus film-only thickness (peel a sample) | |
| Lot or batch number, if printed | |

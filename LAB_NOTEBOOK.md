# Lab notebook

After every work session, add an entry at the **top**: five short lines in your own words. Write what really happened, failures included; this is our proof of work.

```
## YYYY-MM-DD: who
Did:
Saw / measured:
Problem:
Next:
```

---

## 2026-10-14 (evening): Soham (with Claude)

**Did:**
- Searched the PC for the earlier Kapton trial and found LaserCAD V8.28. It was installed 20 Jul 2026; its config gives the machine facts (1200 × 900 mm bed, 20 kHz PWM, 98 % max). There is no record of the Kapton settings.
- Wrote:
  - the evidence register (A/B/C/X)
  - the E1 protocol and machine-record form
  - pre-filled data sheets and the analysis script (tested on synthetic data only, outside the repo)
  - the research-gap analysis
- Filled the official Stage 2 template (build_deck.py) with tagged content and our own figures.

**Saw / measured:** nothing new measured.

**Problem:** we don't know the meaning of "12", the earlier speed, the film grade/thickness, or the mentor status.

**Next:** E1 Session 0 at the machine, then coupons on 2 days.

## 2026-10-14 (later): Soham (with Claude)

**Did:** iteration 1 of the engineering brief.
- Checked the software on this PC.
- Verified 25 literature sources (`02_research/literature.csv`).
- Critiqued the uploaded Rezaei 2024 paper: simulation only, physically implausible.
- Compared 11 sensor concepts and proposed S1 moisture + S2 temperature now, S3 pH later.
- Wrote requirements, traceability, decision log, electronics architecture, preliminary BOM, power budget and CAD plan.
- Set up git.

**Saw / measured:** still no lab data. Every number in the new docs is literature `[LIT]` or estimate `[AI]`.

**Problem:** the portfolio and the C9 pivot need a team decision. KiCad isn't installed.

**Next:** the team approves or changes D-002…D-006, then Step 1 setup, laser booking and interviews.

## 2026-10-14: Soham (with Claude)

**Did:** started the project again from zero. All old files (the AI-heavy v1 deck, scripts and literature) were moved to `Desktop/MBF vishwakarma_ARCHIVE_v1_2026-10-14/`; nothing was deleted. We set up the new folder, the 8-step build plan, the nurse interview guide and the laser test coupon.

**Saw / measured:** nothing yet. We have no LIG made so far.

**Problem:** we don't know the film thickness or when we can use the laser.

**Next:** Step 1 (fill in "Our setup" in the README), then book laser time and start nurse interviews.

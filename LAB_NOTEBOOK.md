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

## 2026-10-19 (night): Claude, for the team: audit and deck refinement

**Did:**
- Read-only audit of every folder: `PROJECT_AUDIT.md`. Re-ran the CAD verification in SolidWorks (99 / 0 / 5) and KiCad ERC (0).
- Read the template twice: `1_presentation/TEMPLATE_EVIDENCE_MAP.md`. It has no team slide; the team photos go on the Project Overview slide (template T2) and the Maker Journey.
- Deck 18 → 19 slides:
  - new Project Overview & Team slide, with photo placeholders
  - new "how it senses" figure
  - annotated SolidWorks exploded view
  - measurement path drawn from the netlist
  - evidence gallery
  - restored the spec basis, CAD checks table, pin map and FMEA top 5 that the 16 Oct declutter had removed
  - corrected wording on Bluetooth, payback and image credits
- Renamed the deck documents: `CLAIM_EVIDENCE_MATRIX.md`, `FINAL_QA_REPORT.md`, `STAGE2_REMAINING_ACTIONS.md`; new `SLIDE_BY_SLIDE_CHANGELOG.md`.

**Saw / measured:** no lab data yet. Everything is checked in software and CAD only.

**Problem:** the deadline is still unconfirmed (25 Oct in the email vs 16 Oct on Internshala).

**Next:** the team adds photos, roles and the link; re-export the PDF; submit by 24 Oct.

## 2026-10-19: Claude, for the team: full review against what the organisers expect

**Did:**
- Read every folder, the official template, the shortlist email, the Stage 1 proposal and the official website. Wrote `STAGE2_CHECKLIST.md`.
- Found and fixed:
  - the roadmap ran past the December video and the IIT Indore finale
  - the sub-theme (Remote Monitoring) had no radio
  - missing D-012 and stale decisions
  - old experiment names
  - three different BOM totals
- Firmware: Bluetooth state broadcast + PC decoder + bench step T11.
- Deck: cited time and cost numbers, quoted prices, prior art (ALLEVYN LIFE), Stage 1 correction, 15 references. QA 0 issues.

**Saw / measured:** still no lab data. Bluetooth is verified only in software (compile + tests).

**Problem:** the Internshala listing says the design proposal was due 16 Oct; our email says 25 Oct. Must be confirmed with the organisers.

**Next:** confirm the deadline; repository link; ID-badge photos; E2 if the laser is free; submit by 24 Oct.

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
- Verified 25 literature sources (`2_research/literature.csv`).
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

## 2026-10-14 (evening): Claude, for the team: CAD freeze, E2 package, reader design, submission folder

**Did:**
- Repaired the SolidWorks drawings: first-angle views, each dimension shown once, mm units everywhere. The assembly STEP had been exported in cm.
- Independent CAD verification found the seal tape trapped under the clamp (D-013); fixed it.
- Prepared E2 with a new resolution/isolation coupon.
- KiCad reader schematic: ERC clean.
- ESP32-C3 firmware compiles, and its tests pass.
- Wrote the BOM, a first FMEA and FINAL_SUBMISSION.

**Saw / measured:** still **no lab data**. Every check today was on files and software, not on the physical prototype.

**Problem:** the FMEA's top risk (F04) is a broken sense lead that the reader can't detect; it needs a design change in v0.2. There is no git remote yet.

**Next:**
1. Buy silver paint, 1 % resistors and the reader parts; borrow a DMM that reads 20 MΩ or more.
2. Book the laser and run E2 Session S0 + Day 1.

## 2026-10-16: Claude, for the team: clean-up and deck declutter

**Did:**
- Reorganised the project into 7 numbered folders plus `FINAL_SUBMISSION/` (only the deck and its PDF) and `_private/`. History kept in git (tag `backup/pre-reorganize-a5e776f`).
- Removed the duplicate copy tree and the iteration-1 documents.
- Gathered the old archive, the backups and all clutter into `Desktop/MBF vishwakarma_TO_DELETE` for the team to delete.
- Deck: 53 % fewer words per slide, larger text, simpler figures; still 0 layout issues and correct template order.

**Saw / measured:** still no lab data. After the move, every generator and check re-ran clean (CAD 99/0, ERC 0, laser files 35/35, tests pass, firmware compiles).

**Next:** add the repository link to slide 11; book the laser for E2.

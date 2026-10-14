# Design review checklist

Run this at each gate. One teammate checks, and the answer to every question is either a file path or "not yet" with a date.

## Gate 1: Concept review (before ordering parts or chemicals)

- [ ] Every requirement in `requirements.md` traces to a user need or a safety need
- [ ] The user needs have been confirmed by real interviews (`01_people/notes/`)
- [ ] Every sensor claim names its row in the "what bare LIG can do" table
- [ ] Every literature claim has an ID in `02_research/literature.csv`, with how it was verified
- [ ] Each decision is in `decisions.md` with "change if…"

## Gate 2: Design review (before ordering a PCB or 3D-printing the pod)

- [ ] The schematic matches a breadboard circuit that actually worked (photo or video)
- [ ] Every BOM line has a source and price, and a second source for hard-to-get parts
- [ ] The PCB STEP fits the SolidWorks pod with ≥ 0.3 mm clearance; the connector is reachable
- [ ] Sensor pads line up with the pod contacts (drawing with tolerances)
- [ ] Safety:
  - [ ] AC-only excitation
  - [ ] DC-blocking capacitors
  - [ ] battery protection
  - [ ] no charging while worn
- [ ] Manufacturing and assembly:
  - [ ] no part needs a tool we don't have
  - [ ] assembly steps written and timed
- [ ] Privacy: no personal data stored on the pod; BLE pairing on
- [ ] Risks list updated

## Gate 3: Prototype review (before the Stage 3 demo or any claim)

- [ ] Every engineering spec has a test result in `test_log.csv` (pass or fail)
- [ ] Repeatability shown with n ≥ 3 sensors
- [ ] Interference tests done, with results reported, including bad ones
- [ ] The words used match `requirements.md` §1, with no diagnostic claims
- [ ] Usability: at least 3 nurses or students tried clipping the pod on (time recorded)
- [ ] Repository: everything committed; photos are originals; the notebook is up to date

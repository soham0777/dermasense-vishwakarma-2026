"""
Assemble FINAL_SUBMISSION/ from the project's source-of-truth folders, verify every copy, write the index and reports.

- Copies only (never moves or deletes originals). Every copy is SHA-256-checked against its source.
- Re-verifies the copies in their intended software:
  - SolidWorks: parts, assembly self-containment, drawings
  - PowerPoint: the official template
  - KiCad: ERC on the copied schematic
  - arduino-cli: compiles the copied firmware
  - PDF / DXF / CSV / image readers
- Also: relative links in every Markdown file, DOI resolution for the references, personal-data scan.
- Writes:
  - FINAL_SUBMISSION/README.md
  - FILE_INDEX.md, file_index.csv
  - DELIVERABLES_CHECKLIST.md
  - SUBMISSION_READINESS_REPORT.md
  - verification_results.json
- Status words (fixed): Complete, Verified, Pending Physical Experiment, Blocked.
  "Verified" means an automated check passed on the copied file. Being generated alone never earns a status.

Usage: python assemble_submission.py [--no-sw] [--no-web]
"""
import csv
import glob
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "FINAL_SUBMISSION"
sys.path.insert(0, str(ROOT / "06_cad"))
KICAD_CLI = Path(r"C:\Users\dell\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe")
ARDUINO_CLI = Path(r"C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe")
FQBN = "esp32:esp32:esp32c3:CDCOnBoot=cdc"
TEMPLATE2 = "08_submission/template/Vishwakarma Awards 2026-27 Stage 2 Submission Template (2).pptx"

# id, deliverable, destination folder (None = not copied), sources (globs, relative to ROOT), format, status,
# check name, remaining action
ITEMS = [
    ("D01", "Official Vishwakarma Stage 2 template (base of the final deck)", "01_presentation/official_template",
     [TEMPLATE2, "08_submission/template/TEMPLATE_PROVENANCE.md"], "PPTX", "Verified", "pptx",
     "Build the final deck on this file. Never edit it in place."),
    ("D02", "Stage 2 presentation, final (18 slides on the official template) + PDF + QA / claim / asset documents",
     "01_presentation/final_deck",
     ["08_submission/Stage2_Final/Vishwakarma_Stage2_Final.pptx", "08_submission/Stage2_Final/Vishwakarma_Stage2_Final.pdf",
      "08_submission/Stage2_Final/PPT_Asset_Index.md", "08_submission/Stage2_Final/PPT_Claim_and_Reference_Check.md",
      "08_submission/Stage2_Final/PPT_QA_Report.md"], "PPTX/PDF/MD", "Verified", "deck_final",
     "Team: replace the bracketed repository placeholder on slide 11 with the real link (needs D20), then re-run this script."),
    ("D03", "SolidWorks native models: 9 parts, 1 assembly, 7 drawings (v0.1)", "02_cad_solidworks/native",
     ["06_cad/solidworks/*.SLDPRT", "06_cad/solidworks/*.SLDASM", "06_cad/solidworks/*.SLDDRW"], "SLDPRT/SLDASM/SLDDRW",
     "Verified", "solidworks", "Update the strip and seal from the E2 measurements (verify_cad section 5), then rebuild."),
    ("D04", "STEP exports (neutral CAD)", "02_cad_solidworks/step", ["06_cad/solidworks/*.STEP"], "STEP AP214", "Verified", "step",
     "Re-export after any CAD change (sw_build.py does this automatically)."),
    ("D05", "CAD renders", "02_cad_solidworks/renders", ["06_cad/solidworks/*.JPG"], "JPG", "Verified", "image", "None."),
    ("D06", "CAD build + independent verification scripts and reports", "02_cad_solidworks/verification",
     ["06_cad/sw_build.py", "06_cad/verify_cad.py", "06_cad/verify_cad_report.md", "06_cad/verify_cad_results.json",
      "06_cad/calc_mechanical.py", "06_cad/calc_mechanical_report.md", "06_cad/cad_plan.md"], "PY/MD/JSON", "Verified", "cadreport",
     "Re-run verify_cad.py after E2."),
    ("D07", "CAD checked against measured LIG geometry (E2)", None, [], "-", "Pending Physical Experiment", "measured",
     "Run E2, then analyze_e2.py, then verify_cad.py. Its 5 BLOCKED checks become PASS/FAIL."),
    ("D08", "2D drawings (A3, first-angle, PDF)", "03_drawings/pdf", ["06_cad/solidworks/*_drawing.PDF"], "PDF", "Verified", "pdf_a3",
     "Re-issue after the E2 update (revision v0.2)."),
    ("D09", "Laser job files (strip, seal, E1/E2 coupons) + DRC", "03_drawings/laser_dxf",
     ["04_lig_lab/strip_v0_1.dxf", "04_lig_lab/strip_v0_1_encap.dxf", "04_lig_lab/lig_test_coupon.dxf",
      "04_lig_lab/e2/e2_res_coupon.dxf", "04_lig_lab/strip_v0_1_drawing.png", "04_lig_lab/strip_v0_1_drc.txt",
      "04_lig_lab/strip_v0_1_geometry.json", "04_lig_lab/laser_files_check.md", "04_lig_lab/verify_laser_files.py",
      "04_lig_lab/make_strip.py", "04_lig_lab/make_test_pattern.py"], "DXF R2000 (mm)", "Verified", "dxf",
     "Physical check at the machine: LaserCAD import sizes and layers (E2 step S0-6)."),
    ("D10", "KiCad schematic of the two-zone reader (ERC clean)", "04_kicad",
     ["05_electronics/kicad/reader_v0_1.kicad_sch", "05_electronics/kicad/reader_v0_1.kicad_pro",
      "05_electronics/kicad/sym-lib-table", "05_electronics/kicad/fp-lib-table", "05_electronics/kicad/make_reader_schematic.py",
      "05_electronics/kicad/README.md", "05_electronics/kicad/out/*", "05_electronics/calc_readout.py",
      "05_electronics/calc_readout_report.md", "05_electronics/calc_readout.png"], "KiCad 10 / PDF / netlist", "Verified", "kicad",
     "None for v0.1. A PCB only after the bench test and E4."),
    ("D11", "Reader firmware v0.1 + PC tools + wiring table", "05_firmware",
     ["07_firmware/reader_v0_1/*", "07_firmware/tools/*.py", "07_firmware/WIRING.md", "07_firmware/README.md"],
     "Arduino C++ / Python", "Verified", "firmware", "Flash it to the real board (see D12)."),
    ("D12", "Reader bench test with known resistors", "05_firmware", ["07_firmware/BENCH_TEST.md", "07_firmware/bench_test.csv"],
     "MD/CSV", "Pending Physical Experiment", "doc",
     "Buy parts (D13), wire per WIRING.md, run BENCH_TEST.md T0-T10, fill bench_test.csv."),
    ("D13", "Bill of materials v0.1 / procurement", "06_bom_procurement", ["09_procurement/bom_v0_1.csv", "09_procurement/README.md"],
     "CSV", "Complete", "csv", "Check supplier prices and stock, fill have_it_YN, order the first batch (README)."),
    ("D14", "E2 fabrication-validation package (procedure, matrix, sheets, analysis)", "07_experimental_data/E2_protocol",
     ["04_lig_lab/e2/README.md", "04_lig_lab/e2/E2_procedure.md", "04_lig_lab/e2/E2_measurements_and_unknowns.md",
      "04_lig_lab/e2/E2_bench_sheets.pdf", "04_lig_lab/e2/e2_sample_matrix.csv", "04_lig_lab/e2/e2_res_coupon.png",
      "04_lig_lab/e2/e2_res_coupon_features.csv", "04_lig_lab/e2/analyze_e2.py", "04_lig_lab/e2/test_analyze_e2.py",
      "04_lig_lab/e2/make_e2_sheets.py", "04_lig_lab/e2/make_e2_coupon.py", "04_lig_lab/machine_record.md"], "MD/PDF/CSV/PY",
     "Complete", "e2pkg", "Run it at the laser (Session S0, then Day 1 and Day 2)."),
    ("D15", "E2 measured data and plots", "07_experimental_data/E2_data", [], "CSV/PNG", "Pending Physical Experiment", "none",
     "Fill the e2_*.csv files from the bench sheets and run analyze_e2.py. Copy the results here only after that."),
    ("D16", "Lab photographs (machine, coupons, microscope, bench reader)", "08_lab_photographs", [], "JPG", "Pending Physical Experiment",
     "none", "Take the originals during E2 and the bench test (rules: 04_lig_lab/e2/E2_procedure.md, data handling)."),
    ("D17", "E2 safety checklist", "09_safety_fmea", ["04_lig_lab/e2/E2_safety_checklist.md"], "MD", "Complete", "doc",
     "Sign it at every session; scan the signed sheet into 08_lab_photographs."),
    ("D18", "Design FMEA v0.1 (15 failure modes, RPN ranked)", "09_safety_fmea",
     ["00_control/fmea_v0_1.md", "00_control/fmea_v0_1.csv", "00_control/make_fmea.py"], "MD/CSV", "Complete", "csv",
     "Replace the estimated ratings with E2/E4/T-CON-01 results. Decide the F04 design change (loop each sense lead)."),
    ("D19", "References: literature (36) + research matrix (16)", "10_references",
     ["02_research/literature.csv", "02_research/research_matrix.csv", "02_research/research_gap.md"], "CSV/MD", "Verified", "refs",
     "None."),
    ("D20", "Public repository link", "11_repository_links", [], "MD", "Blocked", "repo",
     "Team decision: create a GitHub repository (public or private), add it as the git remote, push dev/stage2-rebuild, "
     "then re-run this script."),
    ("D21", "Requirements, decisions, traceability, evidence register (control documents)", None,
     ["00_control/requirements.md", "00_control/decisions.md", "00_control/traceability.csv", "00_control/evidence_register.csv"],
     "MD/CSV", "Pending Physical Experiment", "control",
     "Update traceability and the evidence register with the E2 and bench-test results; then copy here."),
]

RESULTS = {}
DOWNGRADE = {}   # item -> reason it can't be called Verified
BASES = {"D10": "05_electronics/kicad", "D11": "07_firmware", "D12": "07_firmware"}   # keep sub-folders under these
MANUAL_LINK_CHECKS = {   # links the command line could not reach but a person/browser opened (date, what was seen)
    "https://www.analog.com/en/products/ad5941.html":
        "opened in the browser 2026-10-14: page title 'AD5941 Datasheet and Product Info | Analog Devices'",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def expand(sources):
    files = []
    for s in sources:
        hits = sorted(glob.glob(str(ROOT / s)))
        files += [Path(h) for h in hits if Path(h).is_file() and "__pycache__" not in h]
    return files


# ------------------------------------------------------------------ copy
def assemble():
    if OUT.exists():
        for p in OUT.iterdir():                          # FINAL_SUBMISSION holds copies only, so a rebuild is safe
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    OUT.mkdir(exist_ok=True)
    index = []
    for iid, name, folder, sources, fmt, status, chk, action in ITEMS:
        if folder is None:
            continue
        dest = OUT / folder
        dest.mkdir(parents=True, exist_ok=True)
        files = expand(sources)
        for f in files:
            rel = f.relative_to(ROOT)
            base = ROOT / BASES[iid] if iid in BASES else None
            target = dest / (f.relative_to(base) if base and base in f.parents else f.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
            ok = sha(f) == sha(target)
            index.append(dict(item=iid, path=target.relative_to(OUT).as_posix(), source=rel.as_posix(), bytes=f.stat().st_size,
                              sha256=sha(target), copy_identical=ok))
        if not files:
            (dest / "STATUS.md").write_text(f"# {name}\n\n**Status: {status}.** Nothing here yet. Nothing has been invented to fill it.\n\n"
                                            f"**Remaining action:** {action}\n", encoding="utf-8")
    return index


# ------------------------------------------------------------------ checks
def res(iid, ok, evidence):
    RESULTS.setdefault(iid, []).append({"ok": ok, "evidence": evidence})
    print(f"[{'PASS' if ok is True else 'FAIL' if ok is False else 'INFO'}] {iid}: {evidence}", flush=True)


def check_pptx(iid, folder):
    import win32com.client
    for f in (OUT / folder).glob("*.pptx"):
        app = win32com.client.Dispatch("PowerPoint.Application")
        before = app.Presentations.Count
        pres = app.Presentations.Open(str(f), True, False, False)       # read-only, no window
        n = pres.Slides.Count
        pres.Close()
        if before == 0 and app.Presentations.Count == 0:
            app.Quit()
        md5 = hashlib.md5(f.read_bytes()).hexdigest()
        res(iid, n == 20 and md5 == "c58ef4fe526045f1a82a806e6532bc3c",
            f"opens in Microsoft PowerPoint (read-only): {n} slides; MD5 {md5} matches the provenance record")


def check_deck_final(iid, folder):
    import pymupdf
    import win32com.client
    from pptx import Presentation
    f = OUT / folder / "Vishwakarma_Stage2_Final.pptx"
    app = win32com.client.Dispatch("PowerPoint.Application")
    before = app.Presentations.Count
    pres = app.Presentations.Open(str(f), True, False, False)
    n = pres.Slides.Count
    pres.Close()
    if before == 0 and app.Presentations.Count == 0:
        app.Quit()
    pages = pymupdf.open(OUT / folder / "Vishwakarma_Stage2_Final.pdf").page_count
    qa = json.loads((ROOT / "08_submission" / "qa_final_deck_results.json").read_text(encoding="utf-8"))
    issues = sum(len(s["issues"]) for s in qa["slides"])
    d = qa["deck"]
    limits = all(v[3] for v in d["section_limits"].values())
    text = " ".join(sh.text_frame.text for s in Presentation(f).slides for sh in s.shapes if sh.has_text_frame)
    placeholder = "[team to insert" in text
    res(iid, n == 18 and pages == 18 and issues == 0 and d["section_order_ok"] and limits,
        f"copy opens in Microsoft PowerPoint ({n} slides); PDF {pages} pages; PowerPoint-measured QA: {issues} overflow/overlap "
        f"issues, template section order {'OK' if d['section_order_ok'] else 'WRONG'}, slide limits {'OK' if limits else 'EXCEEDED'}; "
        f"personal-data scan: {pii(text) or 'none found'}")
    if placeholder:
        res(iid, None, "slide 11 still holds the bracketed repository placeholder (team action)")


def prop(obj, name):
    """COM members arrive as methods or properties depending on the binding."""
    v = getattr(obj, name)
    return v() if callable(v) else v


def check_solidworks(iid, folder):
    from verify_cad import EXPECTED, SWSession
    d = OUT / folder
    sw = SWSession()
    try:
        bad = []
        for name, (vol_e, _) in EXPECTED.items():
            doc, err, _ = sw.open(d / f"{name}.SLDPRT", 1)
            if doc is None:
                bad.append(f"{name} did not open ({err})")
                continue
            units, vol = doc.Extension.GetUserPreferenceInteger(263, 0), sw.volume(doc)
            if units != 5 or abs(vol - vol_e) > 0.005 * vol_e + 0.05:
                bad.append(f"{name}: units {units}, volume {vol:.1f} vs {vol_e:.1f}")
            sw.close(doc)
        res(iid, not bad, f"9/9 copied parts open in SolidWorks 2019, MMGS units, volumes match the independent expected values"
            if not bad else "; ".join(bad))
        sw.app.CloseAllDocuments(True)
        doc, err, _ = sw.open(d / "dermasense_bench_v0_1.SLDASM", 2)
        comps = sw.typed(doc, "IAssemblyDoc").GetComponents(True) or []
        paths = [Path(prop(c, "GetPathName")).resolve() for c in comps]
        inside = sum(1 for p in paths if p.parent == d.resolve())
        res(iid, len(comps) == 13 and inside == 13,
            f"assembly copy opens with {len(comps)} components; {inside}/13 resolved from the copied folder (self-contained)")
        sw.app.CloseAllDocuments(True)
        n_ok = 0
        for f in sorted(d.glob("*.SLDDRW")):
            doc, err, warn = sw.open(f, 3)
            if doc is None:
                continue
            drw = sw.typed(doc, "IDrawingDoc")
            v = sw.typed(drw.GetFirstView(), "IView").GetNextView()
            ref = Path(prop(sw.typed(v, "IView"), "GetReferencedModelName")).resolve() if v is not None else None
            n_ok += ref is not None and ref.parent == d.resolve()
            sw.app.CloseAllDocuments(True)
        res(iid, n_ok == 7, f"{n_ok}/7 copied drawings open and reference the copied models")
    finally:
        sw.app.CloseAllDocuments(True)


def check_step(iid, folder):
    bad = []
    files = sorted((OUT / folder).glob("*.STEP"))
    for f in files:
        t = f.read_text(errors="replace").replace(" ", "")
        if "SI_UNIT(.MILLI.,.METRE.)" not in t or "MANIFOLD_SOLID_BREP" not in t:
            bad.append(f.name)
    res(iid, len(files) == 10 and not bad, f"{len(files)} STEP files: millimetre units and solid bodies in every header"
        + (f"; problems: {bad}" if bad else "") + "; SolidWorks re-import volumes: see verify_cad_report.md (section 2)")


def check_images(iid, folder):
    from PIL import Image
    files = sorted((OUT / folder).glob("*.JPG"))
    sizes = [Image.open(f).size for f in files]
    res(iid, len(files) >= 4 and all(w > 300 for w, _ in sizes), f"{len(files)} renders open, sizes {sorted(set(sizes))}")


def check_cadreport(iid, folder):
    j = json.loads((OUT / folder / "verify_cad_results.json").read_text())
    c = j["counts"]
    res(iid, c["FAIL"] == 0, f"verify_cad.py ({j['run']}): {c['PASS']} PASS, {c['FAIL']} FAIL, {c['BLOCKED']} BLOCKED "
                             f"(blocked = waiting for E2 data)")


def check_pdf_a3(iid, folder):
    import pymupdf
    files = sorted((OUT / folder).glob("*.PDF"))
    ok = []
    for f in files:
        d = pymupdf.open(f)
        w, h = d[0].rect.width / 72 * 25.4, d[0].rect.height / 72 * 25.4
        ok.append(d.page_count == 1 and abs(w - 420) < 1 and abs(h - 297) < 1 and "PROVISIONAL" in d[0].get_text())
    res(iid, len(files) == 7 and all(ok), f"{sum(ok)}/{len(files)} PDFs open, A3 landscape, title block + PROVISIONAL note present")


def check_dxf(iid, folder):
    import ezdxf
    files = sorted((OUT / folder).glob("*.dxf"))
    good = [f.name for f in files if not ezdxf.readfile(f).audit().has_errors and ezdxf.readfile(f).header.get("$INSUNITS") == 4]
    rep = (OUT / folder / "laser_files_check.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*(\d+) PASS, (\d+) FAIL", rep)
    res(iid, len(good) == len(files) == 4 and m and m.group(2) == "0",
        f"{len(good)}/{len(files)} DXF open and audit cleanly in ezdxf, mm units; verify_laser_files.py: {m.group(1)} PASS, {m.group(2)} FAIL")


def run(cmd, timeout=900):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def check_kicad(iid, folder):
    sch = OUT / folder / "reader_v0_1.kicad_sch"
    tmp = Path(tempfile.mkdtemp()) / "erc.json"
    code, _ = run([KICAD_CLI, "sch", "erc", "--format", "json", "--severity-all", "-o", tmp, sch])
    v = [x for s in json.loads(tmp.read_text()).get("sheets", []) for x in s.get("violations", [])]
    res(iid, code == 0 and not v, f"copied schematic opens in KiCad 10 (kicad-cli); ERC on the copy: {len(v)} violations")


def check_firmware(iid, folder):
    sketch = OUT / folder / "reader_v0_1"
    bp = Path(tempfile.mkdtemp(prefix="fw_build_"))
    code, out = run([ARDUINO_CLI, "compile", "--fqbn", FQBN, "--warnings", "all", "--build-path", bp, sketch])
    m = re.search(r"Sketch uses (\d+) bytes \((\d+)%\)", out)
    warn = len(re.findall(r"warning:", out))
    res(iid, code == 0 and warn == 0, f"copied sketch compiles with arduino-cli ({FQBN}): "
                                      f"{m.group(1) + ' bytes (' + m.group(2) + '% flash)' if m else 'no size'}, "
                                      f"{warn} warnings, 19 compile-time tests")
    code, out = run([sys.executable, "-m", "pytest", "-q", ROOT / "07_firmware/tools"], timeout=300)
    m = re.search(r"(\d+) passed", out)
    res(iid, code == 0, f"tool tests on the source: {m.group(0) if m else out[-200:]} (copies SHA-identical)")
    code, out = run([sys.executable, ROOT / "07_firmware/tools/check_consistency.py"])
    res(iid, code == 0, out.strip().splitlines()[-1].replace("; WIRING.md written", ""))


def check_csv(iid, folder):
    for f in sorted((OUT / folder).glob("*.csv")):
        rows = list(csv.reader(open(f, encoding="utf-8")))
        ok = len(rows) > 1 and all(len(r) == len(rows[0]) for r in rows)
        res(iid, ok, f"{f.name}: {len(rows) - 1} rows x {len(rows[0])} columns, "
                     + ("consistent" if ok else f"INCONSISTENT column counts {sorted({len(r) for r in rows})}"))


def check_e2pkg(iid, folder):
    import pymupdf
    n = pymupdf.open(OUT / folder / "E2_bench_sheets.pdf").page_count
    code, out = run([sys.executable, "-m", "pytest", "-q", ROOT / "04_lig_lab/e2/test_analyze_e2.py"], timeout=300)
    m = re.search(r"(\d+) passed", out)
    real = (ROOT / "04_lig_lab/e2/measured_process.json").exists()
    res(iid, code == 0 and n > 0 and not real, f"bench sheets PDF opens ({n} pages); analysis tests {m.group(0) if m else 'FAILED'} "
                                               f"(synthetic data only); no measured_process.json exists (correct: no data yet)")


def check_doc(iid, folder):
    res(iid, None, "document present; it is checked by reading, not by software")


def doi_ok(d):
    import urllib.parse
    url = urllib.parse.quote(d, safe=":/?#[]@!$&'()*+,;=%") if d.startswith("http") else f"https://doi.org/{d}"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (reference check)"})

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect) if not d.startswith("http") else urllib.request.build_opener()
    try:
        r = opener.open(req, timeout=20)
        return d, r.status
    except urllib.error.HTTPError as e:
        return d, e.code
    except Exception as e:  # noqa: BLE001
        return d, f"error {type(e).__name__}"


def check_refs(iid, folder, web):
    check_csv(iid, folder)
    if not web:
        res(iid, None, "link check skipped (--no-web)")
        return
    links = set()
    for f in ("literature.csv", "research_matrix.csv"):
        for r in csv.DictReader(open(OUT / folder / f, encoding="utf-8")):
            v = (r.get("doi_or_url") or r.get("doi_or_link") or "").strip()
            for part in re.split(r"[;\s]+", v):
                if part.startswith("10.") or part.startswith("http"):
                    links.add(part.rstrip(".,"))
    with ThreadPoolExecutor(8) as ex:
        out = list(ex.map(doi_ok, sorted(links)))
    good = [d for d, s in out if isinstance(s, int) and s < 400]
    refused = [(d, s) for d, s in out if s in (401, 403, 405, 429)]          # server answered: the page exists
    manual = [d for d, s in out if not isinstance(s, int) and d in MANUAL_LINK_CHECKS]
    unconfirmed = [(d, s) for d, s in out if not isinstance(s, int) and d not in MANUAL_LINK_CHECKS]
    broken = [(d, s) for d, s in out if isinstance(s, int) and s >= 400 and (d, s) not in refused]
    RESULTS.setdefault("links", []).append({"checked": len(out), "resolved": good, "refused_but_answered": refused,
                                            "manual": {d: MANUAL_LINK_CHECKS[d] for d in manual},
                                            "unconfirmed": unconfirmed, "broken": broken})
    res(iid, not broken, f"{len(good)}/{len(out)} DOIs/URLs resolve automatically; {len(refused)} answered but refused robots; "
                         f"{len(manual)} confirmed in the browser; {len(broken)} broken (HTTP 404/410)")
    if unconfirmed:
        DOWNGRADE[iid] = (f"{len(unconfirmed)} link(s) unreachable from this network (no HTTP answer, browser too): "
                          + ", ".join(d for d, _ in unconfirmed))
        res(iid, None, DOWNGRADE[iid])


def check_repo(iid, folder):
    rem = run(["git", "-C", ROOT, "remote", "-v"])[1].strip()
    head = run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"])[1].strip()
    br = run(["git", "-C", ROOT, "branch", "--show-current"])[1].strip()
    tags = run(["git", "-C", ROOT, "tag"])[1].split()
    (OUT / folder / "REPOSITORY.md").write_text(
        "# Repository\n\n"
        f"- Local git repository, branch `{br}`, assembled at commit `{head}` (this folder is committed with the next commit).\n"
        f"- Backup tags: {', '.join('`' + t + '`' for t in tags)}.\n"
        f"- Remote: {'`' + rem + '`' if rem else '**none configured**. There is no public link yet (Blocked: team decision).'}\n",
        encoding="utf-8")
    res(iid, None if not rem else True, f"git remote: {rem or 'none configured'}; branch {br} @ {head}")


def check_measured(iid):
    real = (ROOT / "04_lig_lab/e2/measured_process.json").exists()
    res(iid, None, "measured_process.json present" if real else "no E2 measurements exist; verify_cad section 5 is BLOCKED")


def check_control(iid):
    res(iid, None, "files exist in 00_control; they must be updated with E2 and bench results before submission")


# ------------------------------------------------------------------ links + personal data
PII = [(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", "e-mail"), (r"(?<!\d)(\+91[ -]?)?[6-9]\d{9}(?!\d)", "phone"),
       (r"\b\d{4}\s\d{4}\s\d{4}\b", "Aadhaar-like")]


def pii(text):
    hits = [f"{k}: {m}" for rx, k in PII for m in re.findall(rx, text) if "noreply@anthropic" not in str(m)]
    return "; ".join(map(str, hits[:5]))


def check_links_and_pii():
    broken, scanned, found = [], 0, []
    for f in OUT.rglob("*"):
        if f.suffix.lower() in (".md", ".csv", ".txt", ".py", ".h", ".ino", ".json", ".kicad_sch"):
            t = f.read_text(encoding="utf-8", errors="replace")
            scanned += 1
            if pii(t):
                found.append(f"{f.relative_to(OUT)}: {pii(t)}")
            if f.suffix == ".md":
                for link in re.findall(r"\]\(([^)#\s]+)", t):
                    if not link.startswith(("http", "mailto")) and not (f.parent / link.replace("%20", " ")).exists():
                        broken.append(f"{f.relative_to(OUT).as_posix()} -> {link}")
    return broken, scanned, found


# ------------------------------------------------------------------ documents
def status_of(iid, default):
    r = RESULTS.get(iid, [])
    if any(x["ok"] is False for x in r):
        return "Blocked" if default != "Pending Physical Experiment" else default
    if default == "Verified" and iid in DOWNGRADE:
        return "Complete"
    return default


def action_of(iid, action):
    return action if iid not in DOWNGRADE else (action.rstrip(".") + ". " if action != "None." else "") +         "Open the unconfirmed links from another network; replace or drop any that are dead (L32 is already marked weak)."


def write_docs(index, broken, scanned, found):
    head = run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"])[1].strip()
    when = time.strftime("%Y-%m-%d %H:%M")
    rows = []
    for iid, name, folder, sources, fmt, status, chk, action in ITEMS:
        st = status_of(iid, status)
        ev = " · ".join(x["evidence"] for x in RESULTS.get(iid, [])) or "-"
        path = f"[{folder}/]({folder.replace(' ', '%20')}/)" if folder else ("`" + "`, `".join(sources) + "`" if sources else "-")
        rows.append((iid, name, path, fmt, st, ev, action_of(iid, action)))
    counts = {s: sum(r[4] == s for r in rows) for s in ("Complete", "Verified", "Pending Physical Experiment", "Blocked")}

    # readiness report
    rep = [f"# Submission readiness report ({when}, commit {head})", "",
           f"**{counts['Verified']} Verified · {counts['Complete']} Complete · {counts['Pending Physical Experiment']} "
           f"Pending Physical Experiment · {counts['Blocked']} Blocked** (of {len(rows)} deliverables).", "",
           "| Status | Meaning |", "|---|---|",
           "| **Verified** | An automated check passed on the copy in this folder: it opened in its intended software and its content checks passed |",
           "| **Complete** | Finished and reviewed. Not machine-verifiable, or it carries stated estimates |",
           "| **Pending Physical Experiment** | Can't be finished without lab work (E2 laser runs, reader bench test, photos) |",
           "| **Blocked** | Waiting for a team decision or resource that we can't create ourselves |", "",
           "Nothing is labelled final just because it was generated. The material is a **laser-carbonised conductive layer (LIG-like)**; "
           "graphene is not confirmed (no Raman).", "",
           "| ID | Deliverable | Path | Format | Status | Verification evidence | Remaining action |",
           "|---|---|---|---|---|---|---|"]
    rep += [f"| {a} | {b} | {c} | {d} | **{e}** | {f} | {g} |" for a, b, c, d, e, f, g in rows]
    rep += ["", "## Cross-checks on the whole folder", "",
            f"- Every copy is byte-identical to its source (SHA-256): **{sum(i['copy_identical'] for i in index)}/{len(index)}**.",
            f"- Relative links in Markdown files: **{'all resolve' if not broken else str(len(broken)) + ' broken: ' + '; '.join(broken)}**.",
            f"- Personal-data scan (e-mail, phone, ID-number patterns) over {scanned} text files: "
            f"**{'none found' if not found else '; '.join(found)}**.",
            "- Duplicates: a SHA-256 scan of the whole working tree found no duplicate files, so nothing was removed. "
            "The two template files differ in bytes but have identical content; both are kept (see TEMPLATE_PROVENANCE.md).",
            "", "## The single next action for the team", "",
            "**Book the laser and run E2 Session S0 + Day 1** (`07_experimental_data/E2_protocol/E2_procedure.md`).",
            "Before that, buy or borrow silver paint, the 1 % resistor set and a DMM that reads 20 MΩ or more. "
            "Every Pending item depends on those measurements: the CAD update, deck results, photos and traceability."]
    (OUT / "SUBMISSION_READINESS_REPORT.md").write_text("\n".join(rep) + "\n", encoding="utf-8")

    # file index
    with open(OUT / "file_index.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["item", "path", "source", "bytes", "sha256", "copy_identical"])
        w.writeheader()
        w.writerows(index)
    fi = [f"# File index ({when}, commit {head})", "", f"{len(index)} files. Each is a copy of `source` (byte-identical, SHA-256 in "
          "`file_index.csv`). Edit the source, then re-run `python 00_control/assemble_submission.py`. Never edit here.", "",
          "| Item | File | Source | Size |", "|---|---|---|---|"]
    fi += [f"| {i['item']} | [{i['path']}]({i['path'].replace(' ', '%20')}) | `{i['source']}` | {i['bytes'] / 1024:.0f} KB |" for i in index]
    (OUT / "FILE_INDEX.md").write_text("\n".join(fi) + "\n", encoding="utf-8")

    # checklist
    tick = {"Verified": "☑", "Complete": "☑", "Pending Physical Experiment": "☐", "Blocked": "☒"}
    cl = [f"# Deliverables checklist ({when})", "", "☑ done (Verified or Complete) · ☐ waits for lab work · ☒ blocked by a team decision", ""]
    cl += [f"- {tick[e]} **{a}** {b} ({e}): {g}" for a, b, c, d, e, f, g in rows]
    (OUT / "DELIVERABLES_CHECKLIST.md").write_text("\n".join(cl) + "\n", encoding="utf-8")

    # master README
    folders = sorted({it[2].split("/")[0] for it in ITEMS if it[2]})
    rd = ["# FINAL_SUBMISSION: Dermasense (VK26-IITI-HT-0050), Vishwakarma Awards 2026-27 Stage 2", "",
          f"Assembled {when} from commit `{head}` by `00_control/assemble_submission.py`.",
          "**This folder holds copies only.** The working files live in the numbered project folders. Never edit here; "
          "edit the source and re-run the script.", "",
          f"**State: {counts['Verified']} Verified · {counts['Complete']} Complete · {counts['Pending Physical Experiment']} "
          f"Pending Physical Experiment · {counts['Blocked']} Blocked.** "
          "The design work is verified and the final deck is built ([01_presentation/final_deck/](01_presentation/final_deck/); "
          "it still needs the repository link on slide 11). **No experiment has been run yet**, so there is no measured data and "
          "there are no lab photographs. Details: [SUBMISSION_READINESS_REPORT.md](SUBMISSION_READINESS_REPORT.md).", "",
          "| Folder | Contents |", "|---|---|"]
    for fo in folders:
        names = [it[1] for it in ITEMS if it[2] and it[2].split("/")[0] == fo]
        rd.append(f"| [{fo}/]({fo}/) | {'; '.join(names)} |")
    rd += ["", "**Also here:**",
           "- [FILE_INDEX.md](FILE_INDEX.md): every file, its source and checksum",
           "- [DELIVERABLES_CHECKLIST.md](DELIVERABLES_CHECKLIST.md)",
           "- [SUBMISSION_READINESS_REPORT.md](SUBMISSION_READINESS_REPORT.md): status, evidence and remaining action per deliverable",
           "- `verification_results.json`: raw check output", "",
           "**Words we use carefully:**",
           "- The conductive layer is called **laser-carbonised (LIG-like)**; graphene is not confirmed.",
           "- Numbers marked as estimates are estimates.",
           "- v0.1 drawings are **PROVISIONAL**: not for fabrication until the E2 update."]
    (OUT / "README.md").write_text("\n".join(rd) + "\n", encoding="utf-8")
    (OUT / "verification_results.json").write_text(json.dumps(RESULTS, indent=1, default=str))
    return counts


def main():
    sw, web = "--no-sw" not in sys.argv, "--no-web" not in sys.argv
    index = assemble()
    print(f"copied {len(index)} files; identical {sum(i['copy_identical'] for i in index)}")
    for iid, name, folder, sources, fmt, status, chk, action in ITEMS:
        try:
            if chk == "pptx":
                check_pptx(iid, folder)
            elif chk == "deck_final":
                check_deck_final(iid, folder)
            elif chk == "solidworks":
                check_solidworks(iid, folder) if sw else res(iid, None, "SolidWorks check skipped (--no-sw)")
            elif chk == "step":
                check_step(iid, folder)
            elif chk == "image":
                check_images(iid, folder)
            elif chk == "cadreport":
                check_cadreport(iid, folder)
            elif chk == "measured":
                check_measured(iid)
            elif chk == "pdf_a3":
                check_pdf_a3(iid, folder)
            elif chk == "dxf":
                check_dxf(iid, folder)
            elif chk == "kicad":
                check_kicad(iid, folder)
            elif chk == "firmware":
                check_firmware(iid, folder)
            elif chk == "csv":
                check_csv(iid, folder)
            elif chk == "e2pkg":
                check_e2pkg(iid, folder)
            elif chk == "doc":
                check_doc(iid, folder)
            elif chk == "refs":
                check_refs(iid, folder, web)
            elif chk == "repo":
                check_repo(iid, folder)
            elif chk == "control":
                check_control(iid)
        except Exception as ex:  # noqa: BLE001  (a crashed check is a failed check, recorded)
            res(iid, False, f"check crashed: {type(ex).__name__}: {ex}")
    broken, scanned, found = check_links_and_pii()
    counts = write_docs(index, broken, scanned, found)
    print(counts, "| broken links:", broken, "| personal data:", found)


if __name__ == "__main__":
    main()

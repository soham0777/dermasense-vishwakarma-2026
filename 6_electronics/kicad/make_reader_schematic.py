"""
Generate the KiCad 10 schematic of the minimum two-zone reader v0.1, then run ERC and export PDF, netlist and BOM.

Circuit (values from ../calc_readout.py; formulas in its docstring):
  GPIO3 DRV_C  -R1 1k-  S_C  (J4.1, strip SENSE_C pad)        zone C electrode
  GPIO4 DRV_A  -R2 1k-  S_A  (J4.2, strip SENSE_A pad)        zone A electrode
  COM1 (J4.3)  -R3 1k-  N                                     common electrode -> measurement node
  GPIO5 DRV_LOOP -R4 1k- COM2 (J4.4)                          COM loop continuity (broken strip -> FAULT)
  GPIO10 DRV_REF -R5 100k 0.1 %- N                            reference resistor
  GPIO20 DRV_CHK -R6 100k 0.1 %- N                            on-board check resistor (self-test, ADC loading)
  N -C1 10 nF C0G- GND ; N -> ADS1115 A0 ; +3V3 -> ADS1115 A1 (ratiometric Vdd)
  LEDs: GPIO0 green OK, GPIO1 amber CHANGE, GPIO21 red CHECK/FAULT (1k each)
Modules are drawn as their pin headers (Connector_Generic), so the schematic matches what is soldered on perfboard.
Every net is wired by a short stub + label at the pin. Writes reader_v0_1.kicad_sch (+ .kicad_pro).
Usage: python make_reader_schematic.py
"""
import json
import math
import re
import subprocess
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
KICAD = Path(r"C:\Users\dell\AppData\Local\Programs\KiCad\10.0")
SYMDIR = KICAD / "share" / "kicad" / "symbols"
CLI = KICAD / "bin" / "kicad-cli.exe"
NAME = "reader_v0_1"
ROOT = str(uuid.uuid5(uuid.NAMESPACE_URL, "dermasense/reader_v0_1"))
G = 2.54

_n = 0


def uid():
    global _n
    _n += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"dermasense/reader_v0_1/{_n}"))   # stable across runs


def extract(lib, name):
    s = (SYMDIR / f"{lib}.kicad_sym").read_text(encoding="utf-8")
    i = s.index(f'(symbol "{name}"')
    d = 0
    for j in range(i, len(s)):
        d += {"(": 1, ")": -1}.get(s[j], 0)
        if d == 0:
            return s[i:j + 1]


LIBS = {}


def lib_symbol(lib_id):
    """Embedded definition + pin table {number: (x, y, angle)} in symbol coordinates (y up)."""
    if lib_id not in LIBS:
        lib, name = lib_id.split(":")
        txt = extract(lib, name)
        pins = {}
        for m in re.finditer(r'\(pin \w+ \w+\s*\(at ([-\d.]+) ([-\d.]+) (\d+)\).*?\(number "([^"]+)"', txt, re.S):
            pins[m.group(4)] = (float(m.group(1)), float(m.group(2)), int(m.group(3)))
        LIBS[lib_id] = (txt.replace(f'(symbol "{name}"', f'(symbol "{lib_id}"', 1), pins)
    return LIBS[lib_id]


ITEMS = []      # s-expressions
PLACED = []     # (ref, value, footprint) for the report


def prop(key, val, x, y, hide=False, justify=None, angle=0):
    j = f"(justify {justify})" if justify else ""
    h = "(hide yes)" if hide else ""
    return f'(property "{key}" "{val}" (at {x:.2f} {y:.2f} {angle}) {h} (effects (font (size 1.27 1.27)) {j}))'


def place(lib_id, ref, value, x, y, footprint="", desc="", rot=0, label_at=None):
    """Place a symbol; rot = KiCad rotation (counter-clockwise on screen). Returns absolute pin points + angles."""
    _, pins = lib_symbol(lib_id)
    power = lib_id.startswith("power:")
    c, s = round(math.cos(math.radians(rot))), round(math.sin(math.radians(rot)))
    absp = {}
    for n, (px, py, a) in pins.items():
        sx, sy = px, -py                                   # library y-up -> screen y-down
        absp[n] = (x + sx * c + sy * s, y - sx * s + sy * c, (a + rot) % 360)
    rx, ry = label_at or ((x + 2.54, y - 1.27) if not power else (x, y))
    ang = 0 if power else rot % 180                       # keep reference/value text horizontal on rotated parts
    jst = "right" if rot % 360 == 180 else "left"         # KiCad mirrors justification on 180-degree parts
    props = [prop("Reference", ref, rx, ry, hide=power, justify=jst, angle=ang),
             prop("Value", value, rx, ry + 2.54, justify=jst, angle=ang),
             prop("Footprint", footprint, x, y, hide=True), prop("Datasheet", "~", x, y, hide=True),
             prop("Description", desc, x, y, hide=True)]
    pin_s = " ".join(f'(pin "{n}" (uuid "{uid()}"))' for n in pins)
    ITEMS.append(f'(symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} {rot}) (unit 1) (exclude_from_sim no) (in_bom {"no" if power else "yes"}) '
                 f'(on_board yes) (dnp no) (uuid "{uid()}") {" ".join(props)} {pin_s} '
                 f'(instances (project "{NAME}" (path "/{ROOT}" (reference "{ref}") (unit 1)))))')
    if not power:
        PLACED.append((ref, value, footprint))
    return absp


def wire(x1, y1, x2, y2):
    ITEMS.append(f'(wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})) (stroke (width 0) (type default)) (uuid "{uid()}"))')


def stub_end(p, length=G):
    x, y, a = p
    dx, dy = -math.cos(math.radians(a)), math.sin(math.radians(a))     # outward, schematic y down
    return x + dx * length, y + dy * length


PWR_N = [0]


def net(p, name, length=G):
    """Short wire from the pin outward, ending in a local label or a power symbol."""
    x2, y2 = stub_end(p, length)
    wire(p[0], p[1], x2, y2)
    if name in ("GND", "+3V3"):
        PWR_N[0] += 1
        out = "left" if x2 < p[0] - 1e-6 else "right" if x2 > p[0] + 1e-6 else "down" if y2 > p[1] else "up"
        rot = {"GND": {"down": 0, "right": 90, "up": 180, "left": 270},
               "+3V3": {"up": 0, "left": 90, "down": 180, "right": 270}}[name][out]   # symbol points away from the pin
        place(f"power:{name}", f"#PWR0{PWR_N[0]:02d}", name, x2, y2, rot=rot)
    else:
        horiz = abs(x2 - p[0]) > 1e-6
        rot = 180 if (horiz and x2 < p[0]) else 0 if horiz else (90 if y2 < p[1] else 270)
        just = "right bottom" if rot == 180 else "left bottom"
        ITEMS.append(f'(label "{name}" (at {x2:.2f} {y2:.2f} {rot}) (effects (font (size 1.27 1.27)) (justify {just})) (uuid "{uid()}"))')


def nc(p):
    ITEMS.append(f'(no_connect (at {p[0]:.2f} {p[1]:.2f}) (uuid "{uid()}"))')


def text(s, x, y, size=1.27, bold=False):
    s = s.replace('"', "'")
    b = "(bold yes)" if bold else ""
    ITEMS.append(f'(text "{s}" (exclude_from_sim no) (at {x:.2f} {y:.2f} 0) (effects (font (size {size} {size}) {b}) (justify left)) (uuid "{uid()}"))')


FP_R = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
FP_C = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"
FP_LED = "LED_THT:LED_D3.0mm"
FP_H = "Connector_PinHeader_2.54mm:PinHeader_1x{:02d}_P2.54mm_Vertical"


def power_len(name, i):
    """Stagger power-symbol stubs on adjacent header pins so the symbols don't overlap."""
    return (7.62 if i % 2 else 12.7) if name in ("GND", "+3V3") else 5.08


def build():
    text("Dermasense minimum two-zone reader v0.1 (bench, PROVISIONAL)", 20.32, 17.78, 2.5, True)
    text("Bipolar DC drive per zone; values from 6_electronics/calc_readout.py. USB-powered bench tool, not for patient use.", 20.32, 22.86)

    # ---- ESP32-C3 SuperMini as its two 8-pin headers (USB-C at the top)
    text("U1  ESP32-C3 SuperMini (module headers)", 20.32, 33.02, 1.5, True)
    left = ["5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO2", "GPIO1", "GPIO0"]
    right = ["GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10", "GPIO20", "GPIO21"]
    use = {"GND": "GND", "3V3": "+3V3", "GPIO4": "DRV_A", "GPIO3": "DRV_C", "GPIO1": "LED_Y", "GPIO0": "LED_G",
           "GPIO5": "DRV_LOOP", "GPIO6": "SDA", "GPIO7": "SCL", "GPIO10": "DRV_REF", "GPIO20": "DRV_CHK", "GPIO21": "LED_R"}
    for ref, names, x, y in (("J1", left, 45.72, 50.8), ("J2", right, 45.72, 86.36)):
        pins = place("Connector_Generic:Conn_01x08", ref, f"SuperMini {'left' if ref == 'J1' else 'right'} header", x, y, FP_H.format(8),
                     "ESP32-C3 SuperMini module pins", label_at=(x - 5.08, y - 12.7))
        for i, nm in enumerate(names):
            p = pins[str(i + 1)]
            text(nm, x + 3.0, p[1] + 0.4)
            if nm in use:
                net(p, use[nm], power_len(use[nm], i))
            else:
                nc(p)
    text("GPIO2/8/9 = strapping pins (8 = on-board LED, 9 = BOOT): left unused. 5V pin unused (USB powers the module).", 20.32, 104.14)

    # ---- ADS1115 module
    text("U2  ADS1115 ADC module", 86.36, 33.02, 1.5, True)
    ads = ["VDD", "GND", "SCL", "SDA", "ADDR", "ALRT", "A0", "A1", "A2", "A3"]
    ads_use = {"VDD": "+3V3", "GND": "GND", "SCL": "SCL", "SDA": "SDA", "ADDR": "GND", "A0": "N", "A1": "+3V3"}
    pins = place("Connector_Generic:Conn_01x10", "J3", "ADS1115 module header", 111.76, 53.34, FP_H.format(10), "ADS1115 breakout",
                 label_at=(111.76 - 5.08, 53.34 - 15.24))
    for i, nm in enumerate(ads):
        p = pins[str(i + 1)]
        text(nm, 111.76 + 3.0, p[1] + 0.4)
        net(p, ads_use[nm], power_len(ads_use[nm], i)) if nm in ads_use else nc(p)
    text("I2C address 0x48 (ADDR to GND); 10k pull-ups are on the module.", 86.36, 76.2)
    text("A0 = node N (zone/loop/check). A1 = 3V3 rail (ratiometric Vdd).", 86.36, 79.5)

    # ---- drive / sense network
    text("Drive and sense network (one node N, one zone at a time)", 152.4, 33.02, 1.5, True)
    net_r = [("R1", "1k", "DRV_C", "S_C", "zone C protection"), ("R2", "1k", "DRV_A", "S_A", "zone A protection"),
             ("R3", "1k", "COM1", "N", "common electrode protection"), ("R4", "1k", "DRV_LOOP", "COM2", "loop-check protection"),
             ("R5", "100k 0.1%", "DRV_REF", "N", "Rref, 0.1 %, 25 ppm/C"), ("R6", "100k 0.1%", "DRV_CHK", "N", "check resistor, 0.1 %")]
    for i, (ref, val, top, bot, desc) in enumerate(net_r):
        x = 157.48 + i * 12.7
        pins = place("Device:R", ref, val, x, 50.8, FP_R, desc)
        net(pins["1"], top, 5.08)
        net(pins["2"], bot, 5.08)
    pins = place("Device:C", "C1", "10nF C0G", 157.48, 76.2, FP_C, "node filter; settle >= 10 ms (10 tau)")
    net(pins["1"], "N", 5.08)
    net(pins["2"], "GND", 5.08)

    # ---- strip contact (4 pogo pins in the clamp)
    text("J4  strip contact: 4 pogo pins in clamp_base_v0_1", 203.2, 71.12, 1.5, True)
    pins = place("Connector_Generic:Conn_01x04", "J4", "Strip pads (pogo P75-B1)", 231.14, 88.9, FP_H.format(4),
                 "pads at 5.08 mm pitch, strip_v0_1", label_at=(231.14 - 5.08, 88.9 - 10.16))
    for i, (pad, nm) in enumerate((("SENSE_C", "S_C"), ("SENSE_A", "S_A"), ("COM_1", "COM1"), ("COM_2", "COM2"))):
        p = pins[str(i + 1)]
        text(pad, 231.14 + 3.0, p[1] + 0.4)
        net(p, nm, 5.08)

    # ---- status LEDs
    text("Status LEDs (1.3 mA each)", 152.4, 101.6, 1.5, True)
    for i, (ref_r, ref_d, sig, col) in enumerate((("R7", "D1", "LED_G", "green OK"), ("R8", "D2", "LED_Y", "amber CHANGE"),
                                                  ("R9", "D3", "LED_R", "red CHECK/FAULT"))):
        y = 114.3 + i * 10.16
        pr = place("Device:R", ref_r, "1k", 167.64, y, FP_R, "LED series resistor", rot=90, label_at=(165.1, y - 5.08))
        net(pr["1"], sig, 5.08)
        pd = place("Device:LED", ref_d, f"LED {col}", 182.88, y, FP_LED, col, rot=180, label_at=(195.58, y - 1.27))
        wire(pr["2"][0], pr["2"][1], pd["2"][0], pd["2"][1])    # resistor -> anode
        net(pd["1"], "GND", 5.08)                                # cathode

    # ---- power flags (the module's regulator and USB ground are the sources)
    text("Power: USB-C -> SuperMini LDO -> 3V3", 20.32, 111.76, 1.5, True)
    for i, nm in enumerate(("+3V3", "GND")):
        x = 25.4 + i * 15.24
        PWR_N[0] += 1
        place(f"power:{nm}", f"#PWR0{PWR_N[0]:02d}", nm, x, 121.92)
        wire(x, 121.92, x, 127.0)
        place("power:PWR_FLAG", f"#FLG0{i + 1}", "PWR_FLAG", x, 127.0)

    # ---- how it measures
    notes = ["Measurement sequence (firmware 7_firmware/reader_v0_1):",
             "1 Zone C: DRV_C and DRV_REF drive, all other drive pins high-Z. Phase +: DRV_C=1, DRV_REF=0; phase -: DRV_C=0, DRV_REF=1.",
             "   Rx = Rref(Vdd/VN - 1) (phase +), Rx = Rref VN/(Vdd - VN) (phase -); average; subtract R1 + R3 = 2 x 1k.",
             "2 Zone A: same with DRV_A.   3 Loop: DRV_LOOP vs DRV_REF through COM2 -> COM loop -> COM1 (open = FAULT).",
             "4 Check: DRV_CHK vs DRV_REF (known 100k) -> gain/loading correction. Between scans every drive pin is high-Z (no DC on the strip).",
             "Thresholds (calc_readout): wet < 100 kohm, dry > 300 kohm, 3 consecutive scans. States: OK / CHANGE / CHECK (A wet before C) / FAULT."]
    for i, s in enumerate(notes):
        text(s, 20.32, 144.78 + i * 3.3)


def write():
    libs = "\n".join(v[0] for v in LIBS.values())
    sch = (f'(kicad_sch (version 20250610) (generator "eeschema") (generator_version "10.0") (uuid "{ROOT}") (paper "A4")\n'
           f'(title_block (title "Dermasense two-zone reader v0.1") (date "2026-10-14") (rev "0.1 PROVISIONAL") '
           f'(company "Team Dermasense, Vishwakarma Awards 2026-27") (comment 1 "Bench reader: ESP32-C3 SuperMini + ADS1115 module")'
           f' (comment 2 "Generated by 6_electronics/kicad/make_reader_schematic.py - edit the script, not this file"))\n'
           f'(lib_symbols\n{libs}\n)\n' + "\n".join(ITEMS) +
           '\n(sheet_instances (path "/" (page "1")))\n(embedded_fonts no)\n)\n')
    (HERE / f"{NAME}.kicad_sch").write_text(sch, encoding="utf-8")
    # project library tables (KiCad may never have been configured on this PC; paths use KiCad's own variables)
    def lib_table(kind, var, ext, libs):
        rows = "".join(f'  (lib (name "{l}")(type "KiCad")(uri "${{{var}}}/{l}{ext}")(options "")(descr ""))\n' for l in libs)
        return f"({kind} (version 7)\n{rows})\n"
    (HERE / "sym-lib-table").write_text(lib_table("sym_lib_table", "KICAD10_SYMBOL_DIR", ".kicad_sym",
                                                  ("Device", "Connector_Generic", "power")), encoding="utf-8")
    (HERE / "fp-lib-table").write_text(lib_table("fp_lib_table", "KICAD10_FOOTPRINT_DIR", ".pretty",
                                                 ("Resistor_THT", "Capacitor_THT", "LED_THT", "Connector_PinHeader_2.54mm")),
                                       encoding="utf-8")
    pro = HERE / f"{NAME}.kicad_pro"
    if not pro.exists():
        pro.write_text(json.dumps({"meta": {"filename": f"{NAME}.kicad_pro", "version": 3},
                                   "sheets": [[ROOT, "Root"]]}, indent=2), encoding="utf-8")


def run(*args):
    r = subprocess.run([str(CLI), *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def outputs():
    sch = str(HERE / f"{NAME}.kicad_sch")
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    code, msg = run("sch", "erc", "--format", "json", "--severity-all", "-o", str(out / "erc.json"), sch)
    erc = json.loads((out / "erc.json").read_text())
    viol = [v for s in erc.get("sheets", []) for v in s.get("violations", [])]
    run("sch", "erc", "--severity-all", "-o", str(out / "erc.rpt"), sch)
    print(f"ERC: {len(viol)} violations")
    for v in viol:
        print(f"  [{v['severity']}] {v['type']}: {v['description']} "
              + "; ".join(i.get('description', '') for i in v.get('items', [])))
    for args, f in ((("sch", "export", "pdf", "-o"), "reader_v0_1_schematic.pdf"),
                    (("sch", "export", "netlist", "--format", "kicadsexpr", "-o"), "reader_v0_1.net"),
                    (("sch", "export", "bom", "--fields", "Reference,Value,Footprint,${QUANTITY},Description",
                      "--group-by", "Value,Footprint", "-o"), "reader_v0_1_bom.csv")):
        c, m = run(*args, str(out / f), sch)
        print(f"export {f}: {'OK' if c == 0 else 'FAILED ' + m}")
    return viol


if __name__ == "__main__":
    build()
    write()
    print(f"wrote {NAME}.kicad_sch: {len(PLACED)} parts, {len(ITEMS)} items")
    outputs()

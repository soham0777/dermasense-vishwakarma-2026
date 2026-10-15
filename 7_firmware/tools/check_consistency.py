"""
Cross-check the reader design files against each other, then write the perfboard wiring table.

  KiCad netlist (6_electronics/kicad/out/reader_v0_1.net)  <->  firmware pins/values (reader_v0_1/config.h)
  J4 pin order  <->  strip pad order (4_sensor_strip/strip_v0_1_geometry.json)
  ESP32-C3 SuperMini header pinout (module fact, written out below)
Writes 7_firmware/WIRING.md. Exit code 1 on any mismatch.
Usage: python check_consistency.py      (run make_reader_schematic.py first if the schematic changed)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NETLIST = ROOT / "6_electronics" / "kicad" / "out" / "reader_v0_1.net"
CONFIG = ROOT / "7_firmware" / "reader_v0_1" / "config.h"
GEOM = ROOT / "4_sensor_strip" / "strip_v0_1_geometry.json"

# ESP32-C3 SuperMini, USB-C at the top, looking at the component side (module documentation)
SUPERMINI = {"J1": ["5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO2", "GPIO1", "GPIO0"],
             "J2": ["GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10", "GPIO20", "GPIO21"]}
ADS = ["VDD", "GND", "SCL", "SDA", "ADDR", "ALRT", "A0", "A1", "A2", "A3"]
ROLE = {  # config.h constant -> (net name, the resistor/module pin that must be on that net)
    "PIN_DRV_C": ("DRV_C", ("R1", "1")), "PIN_DRV_A": ("DRV_A", ("R2", "1")), "PIN_DRV_LOOP": ("DRV_LOOP", ("R4", "1")),
    "PIN_DRV_REF": ("DRV_REF", ("R5", "1")), "PIN_DRV_CHK": ("DRV_CHK", ("R6", "1")),
    "PIN_SDA": ("SDA", ("J3", "4")), "PIN_SCL": ("SCL", ("J3", "3")),
    "PIN_LED_G": ("LED_G", ("R7", "1")), "PIN_LED_Y": ("LED_Y", ("R8", "1")), "PIN_LED_R": ("LED_R", ("R9", "1"))}
FIXED = {   # nets that do not depend on config.h
    "N": {("R3", "2"), ("R5", "2"), ("R6", "2"), ("C1", "1"), ("J3", "7")},
    "S_C": {("R1", "2"), ("J4", "1")}, "S_A": {("R2", "2"), ("J4", "2")},
    "COM1": {("R3", "1"), ("J4", "3")}, "COM2": {("R4", "2"), ("J4", "4")},
    "+3V3": {("J1", "3"), ("J3", "1"), ("J3", "8")},
    "GND": {("J1", "2"), ("J3", "2"), ("J3", "5"), ("C1", "2"), ("D1", "1"), ("D2", "1"), ("D3", "1")},
}
STRAPPING = {"GPIO2", "GPIO8", "GPIO9"}


def sexpr(text):
    tokens = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', text)
    stack = [[]]
    for t in tokens:
        if t == "(":
            stack.append([])
        elif t == ")":
            last = stack.pop()
            stack[-1].append(last)
        else:
            stack[-1].append(t[1:-1] if t.startswith('"') else t)
    return stack[0][0]


def find(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def field(node, key):
    f = find(node, key)
    return f[0][1] if f else None


def load_netlist(path=NETLIST):
    tree = sexpr(path.read_text(encoding="utf-8"))
    nets = {}
    for n in find(find(tree, "nets")[0], "net"):
        nets[field(n, "name").lstrip("/")] = {(field(x, "ref"), field(x, "pin")) for x in find(n, "node")}
    comps = {field(c, "ref"): field(c, "value") for c in find(find(tree, "components")[0], "comp")}
    return nets, comps


def load_config(path=CONFIG):
    s = path.read_text(encoding="utf-8")
    pins = {k: int(v) for k, v in re.findall(r"constexpr uint8_t (PIN_\w+) = (\d+);", s)}
    nums = {k: float(v) for k, v in re.findall(r"constexpr double (R_\w+) = ([\d.eE+]+);", s)}
    chans = {k: int(v) for k, v in re.findall(r"constexpr uint8_t (ADS_CH_\w+) = (\d+);", s)}
    return pins, nums, chans


def header_pin(gpio):
    for ref, names in SUPERMINI.items():
        if f"GPIO{gpio}" in names:
            return ref, str(names.index(f"GPIO{gpio}") + 1)
    return None


def ohms(value):
    m = re.match(r"([\d.]+)\s*([kM]?)", value)
    return float(m.group(1)) * {"": 1, "k": 1e3, "M": 1e6}[m.group(2)] if m else None


def check(nets, comps, pins, nums, chans):
    errs = []
    for const, (net, must) in ROLE.items():
        if const not in pins:
            errs.append(f"{const} missing in config.h")
            continue
        hp = header_pin(pins[const])
        got = nets.get(net, set())
        if hp is None or f"GPIO{pins[const]}" in STRAPPING:
            errs.append(f"{const} = GPIO{pins[const]} is not a usable SuperMini pin")
        elif hp not in got:
            errs.append(f"{const} = GPIO{pins[const]} ({hp[0]}.{hp[1]}) is not on net {net} in the schematic: {sorted(got)}")
        if must not in got:
            errs.append(f"net {net} lacks {must}")
    for net, nodes in FIXED.items():
        got = {n for n in nets.get(net, set()) if not n[0].startswith("#")}
        if got != nodes:
            errs.append(f"net {net}: schematic {sorted(got)} != expected {sorted(nodes)}")
    a0, a1 = ("J3", str(ADS.index("A0") + 1 + chans.get("ADS_CH_NODE", 0))), ("J3", str(ADS.index("A0") + 1 + chans.get("ADS_CH_VDD", 1)))
    if a0 not in nets.get("N", set()):
        errs.append(f"ADS_CH_NODE points at {a0}, which is not node N")
    if a1 not in nets.get("+3V3", set()):
        errs.append(f"ADS_CH_VDD points at {a1}, which is not the 3V3 rail")
    for ref, const in (("R5", "R_REF"), ("R6", "R_CHECK"), ("R1", "R_PROT"), ("R2", "R_PROT"), ("R3", "R_PROT"), ("R4", "R_PROT")):
        if ohms(comps.get(ref, "")) != nums.get(const):
            errs.append(f"{ref} = {comps.get(ref)} but config {const} = {nums.get(const)}")
    for ref, names in SUPERMINI.items():   # strapping pins must not be wired
        for i, nm in enumerate(names):
            if nm in STRAPPING and any((ref, str(i + 1)) in nodes for net, nodes in nets.items() if not net.startswith("unconnected")):
                errs.append(f"strapping pin {nm} ({ref}.{i + 1}) is wired")
    import json
    pads = json.loads(GEOM.read_text())["pads"]
    order = [n for n, _ in sorted(pads.items(), key=lambda kv: kv[1]["y"])]
    j4 = {"1": "S_C", "2": "S_A", "3": "COM1", "4": "COM2"}
    want = {"SENSE_C": "S_C", "SENSE_A": "S_A", "COM_1": "COM1", "COM_2": "COM2"}
    for i, pad in enumerate(order):
        if want[pad] != j4[str(i + 1)]:
            errs.append(f"pogo pin {i + 1} lands on strip pad {pad} but J4.{i + 1} is {j4[str(i + 1)]}")
    return errs


def describe(ref, pin, comps):
    if ref in SUPERMINI:
        return f"SuperMini {SUPERMINI[ref][int(pin) - 1]}"
    if ref == "J3":
        return f"ADS1115 {ADS[int(pin) - 1]}"
    if ref == "J4":
        return f"pogo pin {pin} (strip {['SENSE_C', 'SENSE_A', 'COM_1', 'COM_2'][int(pin) - 1]})"
    if ref.startswith("D"):
        return f"{ref} LED {'cathode (-)' if pin == '1' else 'anode (+)'}"
    return f"{ref} ({comps.get(ref)}) end {pin}"


def wiring(nets, comps):
    lines = ["# Reader v0.1: point-to-point wiring (perfboard)", "",
             "Generated by `tools/check_consistency.py` from the KiCad netlist. **Do not edit by hand.**",
             "Each row is one electrical node: join everything in the row.",
             "Check every row with the multimeter's continuity beeper before applying power.", "",
             "| Net | Connect together |", "|---|---|"]
    for net in sorted(nets):
        if net.startswith("unconnected"):
            continue
        nodes = sorted((r, p) for r, p in nets[net] if not r.startswith("#"))
        lines.append(f"| `{net}` | " + " · ".join(describe(r, p, comps) for r, p in nodes) + " |")
    unused = sorted(describe(r, p, comps) for net, nodes in nets.items() if net.startswith("unconnected") for r, p in nodes)
    lines += ["", "**Leave unconnected:** " + ", ".join(unused), "",
              "**Parts:** " + ", ".join(f"{r} {v}" for r, v in sorted(comps.items())),
              "", "R5 and R6 must be 0.1 % parts (they set the accuracy). C1 must be C0G/NP0."]
    return "\n".join(lines) + "\n"


def main():
    nets, comps = load_netlist()
    errs = check(nets, comps, *load_config())
    (ROOT / "7_firmware" / "WIRING.md").write_text(wiring(nets, comps), encoding="utf-8")
    for e in errs:
        print("MISMATCH:", e)
    print(f"{'PASS' if not errs else 'FAIL'}: schematic <-> firmware <-> strip pads ({len(errs)} mismatches); WIRING.md written")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()

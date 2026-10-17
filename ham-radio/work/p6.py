from core2 import *
import os
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = lambda n: os.path.join(HERE, f"figT{n}.png")

# --- schematic symbol drawers (centered at cx, cy; ~2 units wide) ---
def sym_res(ax, cx, cy, c="#222"): RES(ax, cx - 1.0, cy, cx + 1.0, c)
def sym_pot(ax, cx, cy, c="#222"):
    RES(ax, cx - 1.0, cy, cx + 1.0, c); ARROW(ax, cx, cy + 0.9, cx, cy + 0.3, c, 2.5, ms=14)
def sym_cap(ax, cx, cy, c="#222"):
    L(ax, [cx - 1.0, cx - 0.15], [cy, cy], c, 2.5); L(ax, [cx + 0.15, cx + 1.0], [cy, cy], c, 2.5)
    L(ax, [cx - 0.15, cx - 0.15], [cy - 0.5, cy + 0.5], c, 3.5); L(ax, [cx + 0.15, cx + 0.15], [cy - 0.5, cy + 0.5], c, 3.5)
def sym_ind(ax, cx, cy, c="#222"):
    for i in range(4): ax.add_patch(Arc((cx - 0.6 + i * 0.4, cy), 0.4, 0.6, theta1=0, theta2=180, color=c, lw=2.5, zorder=5))
    L(ax, [cx - 1.0, cx - 0.8], [cy, cy], c, 2.5); L(ax, [cx + 0.8, cx + 1.0], [cy, cy], c, 2.5)
def sym_diode(ax, cx, cy, c="#222", led=False):
    L(ax, [cx - 1.0, cx + 1.0], [cy, cy], c, 2.5)
    ax.add_patch(Polygon([(cx - 0.35, cy - 0.4), (cx - 0.35, cy + 0.4), (cx + 0.3, cy)], fc=c, ec=c, zorder=5))
    L(ax, [cx + 0.3, cx + 0.3], [cy - 0.4, cy + 0.4], c, 3)
    if led:
        for d in (0, 0.3): ARROW(ax, cx + 0.1 + d, cy + 0.5, cx + 0.5 + d, cy + 0.9, ORANGE, 2, ms=10)
def sym_batt(ax, cx, cy, c="#222"):
    L(ax, [cx - 1.0, cx - 0.25], [cy, cy], c, 2.5); L(ax, [cx + 0.25, cx + 1.0], [cy, cy], c, 2.5)
    L(ax, [cx - 0.25, cx - 0.25], [cy - 0.55, cy + 0.55], c, 3); L(ax, [cx + 0.25, cx + 0.25], [cy - 0.28, cy + 0.28], c, 5)
def sym_switch(ax, cx, cy, c="#222"):
    L(ax, [cx - 1.0, cx - 0.4], [cy, cy], c, 2.5); L(ax, [cx + 0.4, cx + 1.0], [cy, cy], c, 2.5)
    ax.add_patch(Circle((cx - 0.4, cy), 0.08, color=c, zorder=5)); ax.add_patch(Circle((cx + 0.4, cy), 0.08, color=c, zorder=5))
    L(ax, [cx - 0.4, cx + 0.35], [cy, cy + 0.45], c, 2.5)
def sym_lamp(ax, cx, cy, c="#222"):
    ax.add_patch(Circle((cx, cy), 0.45, fc="none", ec=c, lw=2.5, zorder=5))
    L(ax, [cx - 0.32, cx + 0.32], [cy - 0.32, cy + 0.32], c, 2); L(ax, [cx - 0.32, cx + 0.32], [cy + 0.32, cy - 0.32], c, 2)
    L(ax, [cx - 1.0, cx - 0.45], [cy, cy], c, 2.5); L(ax, [cx + 0.45, cx + 1.0], [cy, cy], c, 2.5)
def sym_npn(ax, cx, cy, c="#222"):
    ax.add_patch(Circle((cx, cy), 0.6, fc="none", ec=c, lw=2, zorder=5))
    L(ax, [cx - 0.2, cx - 0.2], [cy - 0.35, cy + 0.35], c, 3.5); L(ax, [cx - 1.0, cx - 0.2], [cy, cy], c, 2.5)
    L(ax, [cx - 0.2, cx + 0.3], [cy + 0.15, cy + 0.6], c, 2.5); L(ax, [cx - 0.2, cx + 0.3], [cy - 0.15, cy - 0.6], c, 2.5)
    ARROW(ax, cx - 0.05, cy - 0.28, cx + 0.3, cy - 0.6, c, 2, ms=10)
def sym_xfmr(ax, cx, cy, c="#222"):
    for side in (-1, 1):
        for i in range(3): ax.add_patch(Arc((cx + side * 0.45, cy - 0.4 + i * 0.4), 0.4, 0.4, theta1=90 if side < 0 else -90, theta2=270 if side < 0 else 90, color=c, lw=2.5, zorder=5))
    L(ax, [cx - 0.08, cx - 0.08], [cy - 0.7, cy + 0.7], c, 2); L(ax, [cx + 0.08, cx + 0.08], [cy - 0.7, cy + 0.7], c, 2)
def sym_ant(ax, cx, cy, c="#222"):
    L(ax, [cx, cx], [cy - 0.7, cy + 0.3], c, 2.5)
    ax.add_patch(Polygon([(cx - 0.5, cy + 0.8), (cx + 0.5, cy + 0.8), (cx, cy + 0.3)], fc="none", ec=c, lw=2.5, zorder=5))

def sym_card(ax, x, y, w, h, fn, name, sub="", color=BLUE):
    RBOX(ax, x, y, w, h, tint(color, 0.84), color, 2, 0.15, 3.5)
    fn(ax, x + w / 2, y + h * 0.62)
    T(ax, x + w / 2, y + h * 0.24 if sub else y + h * 0.2, name, 13, color)
    if sub: T(ax, x + w / 2, y + 0.25, sub, 10.5, "#555", False)

def d_passive(ax):
    r = grid([(1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Resistor & potentiometer", BLUE, 1)
    x, y, w, h = p.scene(2.8)
    sym_card(ax, x + 0.2, y + 0.2, w / 2 - 0.3, h - 0.4, sym_res, "Resistor", "opposes DC current")
    sym_card(ax, x + w / 2 + 0.1, y + 0.2, w / 2 - 0.3, h - 0.4, sym_pot, "Potentiometer", "adjustable resistance")
    p.bul(["Opposes current in DC: RESISTOR", "Volume control: POTENTIOMETER", "Pot controls: RESISTANCE"], size=13)
    p = P(ax, r[1], "Capacitor", GREEN, 2)
    x, y, w, h = p.scene(2.8, top_c="#c8e6c9", bot_c="#e8f5e9")
    sym_card(ax, x + 0.2, y + 0.2, w / 2 - 0.3, h - 0.4, sym_cap, "Capacitor", "symbol", GREEN)
    ax.add_patch(Rectangle((x + w * 0.62, y + 0.5), 0.3, h - 1.0, fc="#90a4ae", zorder=4)); ax.add_patch(Rectangle((x + w * 0.62 + 0.3, y + 0.5), 0.5, h - 1.0, fc="#fff59d", zorder=4)); ax.add_patch(Rectangle((x + w * 0.62 + 0.8, y + 0.5), 0.3, h - 1.0, fc="#90a4ae", zorder=4))
    p.bul(["Stores energy in an ELECTRIC field", "Conductive surfaces separated by an insulator"], size=13)
    p = P(ax, r[2], "Inductor", PURPLE, 3)
    x, y, w, h = p.scene(2.8, top_c="#d1c4e9", bot_c="#ede7f6")
    sym_card(ax, x + 0.2, y + 0.2, w / 2 - 0.3, h - 0.4, sym_ind, "Inductor", "symbol", PURPLE)
    t = np.linspace(0, 1, 300); ax.plot(x + w * 0.58 + 2.2 * t + 0.25 * np.cos(2 * np.pi * 6 * t), y + h / 2 + 0.7 * np.sin(2 * np.pi * 6 * t), color="#b87333", lw=3.5, zorder=5)
    p.bul(["Stores energy in a MAGNETIC field", "Built as a COIL of wire"], size=13)
    p = P(ax, r[3], "Switches", ORANGE, 4)
    x, y, w, h = p.scene(3.0, top_c="#ffcc80", bot_c="#fff3e0")
    sym_card(ax, x + 0.2, y + 0.2, w / 2 - 0.3, h - 0.4, sym_switch, "SPST", "on / off", ORANGE)
    RBOX(ax, x + w / 2 + 0.1, y + 0.2, w / 2 - 0.3, h - 0.4, tint(ORANGE, 0.84), ORANGE, 2, 0.15, 3.5)
    cx, cy = x + w * 0.75, y + h * 0.6
    L(ax, [cx - 1.0, cx - 0.4], [cy, cy], "#222", 2.5); L(ax, [cx - 0.4, cx + 0.4], [cy, cy + 0.4], "#222", 2.5)
    L(ax, [cx + 0.4, cx + 1.0], [cy + 0.45, cy + 0.45], "#222", 2.5); L(ax, [cx + 0.4, cx + 1.0], [cy - 0.45, cy - 0.45], "#222", 2.5)
    T(ax, cx, y + 0.65, "SPDT", 13, ORANGE)
    p.bul(["SPDT: one circuit switched between one of two others", "Component 3 in figure T-2: single-pole single-throw"], size=12)
    p = P(ax, r[4], "Rechargeable batteries", GREEN, 5)
    p.icons([("🔋", "NiMH"), ("🔋", "Lithium-ion"), ("🔋", "Lead-acid")], 2.6)
    p.ok(["Rechargeable: All these choices are correct"], size=13)
    p = P(ax, r[5], "NOT rechargeable", RED, 6)
    p.icons([("🪫", "Carbon-zinc"), ("🚫", "don't charge")], 2.6)
    p.no(["Carbon-zinc: NOT rechargeable"], size=13)
    p.bul(["Cheap disposable cells"], size=13)

def d_semis(ax):
    r = grid([(1, [1, 1.2]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Diode: one-way street", RED, 1)
    x, y, w, h = p.scene(3.4)
    RBOX(ax, x + 0.4, y + 1.0, w - 0.8, 1.2, "#212121", "#000", 2, 0.4, 4)
    ax.add_patch(Rectangle((x + w - 2.2, y + 1.0), 0.5, 1.2, fc="#e0e0e0", zorder=5))
    L(ax, [x + 0.1, x + 0.4], [y + 1.6, y + 1.6], "#9e9e9e", 4); L(ax, [x + w - 0.4, x + w - 0.1], [y + 1.6, y + 1.6], "#9e9e9e", 4)
    T(ax, x + 1.6, y + 2.6, "ANODE (+)", 13, RED); T(ax, x + w - 2.0, y + 2.6, "CATHODE: stripe", 13, BLUE)
    ARROW(ax, x + 1.2, y + 0.5, x + w - 1.2, y + 0.5, GREEN, 3); T(ax, x + w / 2, y + 0.5, " current → one way only ", 12, GREEN, bbox=dict(fc="#fff", ec="none"))
    p.bul(["Electrodes: ANODE and CATHODE", "Cathode marked with a STRIPE", "Forward voltage drop: lower in some diode types than others"], size=13)
    p = P(ax, r[1], "Transistors: switch & amplifier", BLUE, 2)
    x, y, w, h = p.scene(3.4)
    for i, (title, legs, c) in enumerate([("Bipolar (BJT)", "Emitter • Base • Collector", BLUE), ("FET", "Gate • Drain • Source", PURPLE)]):
        bx = x + 0.2 + i * (w - 0.4) / 2
        RBOX(ax, bx + 0.1, y + 0.2, (w - 0.4) / 2 - 0.2, h - 0.4, tint(c, 0.92), c, 2, 0.15, 3.5)
        sym_npn(ax, bx + 1.5, y + h / 2)
        ax.add_patch(Rectangle((bx + 0.3, y + 0.4), 2.4, h - 0.8, fc=tint(c, 0.85), ec="none", zorder=3.6)); sym_npn(ax, bx + 1.5, y + h / 2)
        T(ax, bx + (w - 0.4) / 4 + 0.8, y + h - 0.7, title, 15, c); T(ax, bx + (w - 0.4) / 4 + 0.8, y + h / 2 - 0.2, legs.replace(" • ", "\n"), 12, "#333", False)
    p.bul(["Electronic switch / power gain: TRANSISTOR", "Three regions of semiconductor: TRANSISTOR", "FET: Field Effect Transistor (gate, drain, source)"], size=13)
    p = P(ax, r[2], "LED", ORANGE, 3)
    x, y, w, h = p.scene(2.6, top_c="#ffcc80", bot_c="#fff3e0")
    sym_card(ax, x + 0.2, y + 0.2, w / 2 - 0.3, h - 0.4, lambda a, cx, cy: sym_diode(a, cx, cy, led=True), "LED", "", ORANGE)
    E(ax, "💡", x + w * 0.75, y + h / 2, 1.6)
    p.bul(["Light comes from: FORWARD current"], size=13)
    p = P(ax, r[3], "Gain", GREEN, 4)
    x, y, w, h = p.scene(2.6)
    WAVE(ax, x + 0.3, x + w * 0.35, y + h / 2, 0.3, 2, BLUE, lw=2.5)
    ax.add_patch(Polygon([(x + w * 0.4, y + 0.4), (x + w * 0.4, y + h - 0.4), (x + w * 0.62, y + h / 2)], fc="#c8e6c9", ec=GREEN, lw=2.5, zorder=4))
    WAVE(ax, x + w * 0.65, x + w - 0.3, y + h / 2, 0.95, 2, RED, lw=3)
    p.bul(["Gain: increase in power, voltage or current → All correct"], size=13)
    p = P(ax, r[4], "Remember", GOLD, 5)
    p.table([["Part", "Key fact"], ["Diode", "one direction"], ["Transistor", "switch + gain"], ["BJT", "E, B, C"], ["FET", "G, D, S"]], [1, 1.3], size=14, fill=True)

def d_fig1(ax):
    r = grid([(1, [1.25, 1])])
    p = P(ax, r[0], "Figure T-1 (from the question pool)", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#fff59d", bot_c="#fff8e1")
    fx, fy, fw, fh = FIGFIT(ax, FIG(1), x + 0.3, y + 2.3, w - 0.6, h - 2.5)
    for i, (n, c) in enumerate([("1 Resistor", BLUE), ("2 Transistor", RED), ("3 Lamp", ORANGE), ("4 Battery", GREEN)]):
        LBOX(ax, x + 0.3 + i * (w - 0.6) / 4, y + 0.3, (w - 0.6) / 4 - 0.15, 1.6, n, 16, tint(c, 0.8), c, c)
    p = P(ax, r[1], "What each part is", BLUE, 2)
    x, y, w, h = p.scene(7.0, top_c="#bbdefb", bot_c="#e3f2fd")
    cw, ch = (w - 0.6) / 2, (h - 0.6) / 2
    for i, (fn, n, s_) in enumerate([(sym_res, "1 = Resistor", "zig-zag"), (sym_npn, "2 = Transistor", "controls current flow"), (sym_lamp, "3 = Lamp", "circle with X"), (sym_batt, "4 = Battery", "long + short lines")]):
        sym_card(ax, x + 0.2 + (i % 2) * (cw + 0.2), y + 0.2 + (1 - i // 2) * (ch + 0.2), cw, ch, fn, n, s_)
    p.bul(["Schematic: electrical diagram using standard component symbols",
           "Component 2 job: CONTROL the flow of current", "Schematics accurately show: component CONNECTIONS"], size=14)

def d_fig23(ax):
    r = grid([(1.1, [1.7, 1]), (1, [1.7, 1])])
    p = P(ax, r[0], "Figure T-2", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#fff59d", bot_c="#fff8e1")
    FIGFIT(ax, FIG(2), x + 0.2, y + 0.1, w - 0.4, h - 0.2)
    p = P(ax, r[1], "T-2 parts", BLUE, 2)
    p.table([["#", "Component"], ["3", "Switch (SPST)"], ["4", "Transformer"], ["6", "Capacitor"], ["8", "Light emitting diode"], ["9", "Variable resistor"]], [0.4, 2], size=16, fill=True, hl=set())
    p = P(ax, r[2], "Figure T-3", INDIGO, 3)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#fff59d", bot_c="#fff8e1")
    fx, fy, fw, fh = FIGFIT(ax, FIG(3), x + 0.2, y + 0.1, w * 0.45, h - 0.2)
    rest = x + w * 0.45 + 0.4
    sym_card(ax, rest, y + h / 2 + 0.1, x + w - rest - 0.2, h / 2 - 0.3, sym_ind, "Variable inductor", "coil with an arrow", PURPLE)
    ARROW(ax, rest + 2.6, y + h * 0.62 + 0.9, rest + 3.2, y + h * 0.62 + 0.25, ORANGE, 2.5, ms=14)
    sym_card(ax, rest, y + 0.2, x + w - rest - 0.2, h / 2 - 0.3, sym_ant, "Antenna", "", PURPLE)
    p = P(ax, r[3], "T-3 parts", PURPLE, 4)
    p.table([["#", "Component"], ["3", "Variable inductor"], ["4", "Antenna"]], [0.4, 2], size=16, fill=True)
    p.bul(["Arrow through a symbol = VARIABLE"], size=14)

def d_circuits(ax):
    r = grid([(1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Power supply parts", ORANGE, 1)
    x, y, w, h = p.scene(3.0)
    for i, (e, t) in enumerate([("🔌", "120 V AC"), ("🔁", "TRANSFORMER\nlower AC"), ("➡️", "RECTIFIER\nAC→DC"), ("🎚️", "REGULATOR\nsteady V")]):
        cx = x + w * (i + 0.5) / 4
        E(ax, e, cx, y + h - 0.8, 1.0); T(ax, cx, y + 0.75, t, 10.5)
    p.bul(["AC → varying DC: RECTIFIER", "Controls voltage: REGULATOR", "120 V AC → lower AC: TRANSFORMER"], size=12)
    p = P(ax, r[1], "Relay", BLUE, 2)
    x, y, w, h = p.scene(3.0)
    t = np.linspace(0, 1, 200); ax.plot(x + 0.8 + 1.6 * t, y + 1.2 + 0.4 * np.sin(2 * np.pi * 5 * t), color="#b87333", lw=3, zorder=5)
    L(ax, [x + 3.0, x + w - 0.6], [y + 1.2, y + 1.8], "#222", 3); ax.add_patch(Circle((x + w - 0.6, y + 1.2), 0.1, color="#222", zorder=5))
    T(ax, x + 1.6, y + 0.45, "coil", 12, "#5d4037"); T(ax, x + w - 1.6, y + 2.3, "switch", 12, "#222")
    p.bul(["Relay: an ELECTRICALLY-CONTROLLED switch"], size=13)
    p = P(ax, r[2], "Shielded wire", TEAL, 3)
    x, y, w, h = p.scene(3.0)
    for rr, c in [(1.0, "#212121"), (0.85, "#b0bec5"), (0.6, "#fff"), (0.25, "#b87333")]:
        ax.add_patch(Circle((x + 1.6, y + h / 2), rr, fc=c, ec="#333", lw=1, zorder=5))
    T(ax, x + w - 2.0, y + h / 2, "braid stops\nunwanted\ncoupling", 13, TEAL)
    p.bul(["Why: prevent coupling of unwanted signals to/from the wire"], size=13)
    p = P(ax, r[3], "Resonant (tuned) circuit", PURPLE, 4)
    x, y, w, h = p.scene(3.0)
    sym_ind(ax, x + w * 0.3, y + h / 2); T(ax, x + w / 2, y + h / 2, "+", 24, PURPLE); sym_cap(ax, x + w * 0.7, y + h / 2)
    T(ax, x + w / 2, y + 0.5, "L + C = tuned circuit", 13, PURPLE)
    p.bul(["Inductor + CAPACITOR = resonant circuit", "Resonant: inductor and capacitor in series or parallel"], size=12)
    p = P(ax, r[4], "Indicators & meters", GREEN, 5)
    p.icons([("💡", "LED: visual\nindicator"), ("🔢", "meter: shows\na number")], 3.0)
    p.bul(["Displays a numeric value: METER", "Visual indicator: LED"], size=13)
    p = P(ax, r[5], "Integrated circuit", INDIGO, 6)
    x, y, w, h = p.scene(3.0)
    RBOX(ax, x + w / 2 - 1.6, y + 0.7, 3.2, 1.6, "#212121", "#000", 2, 0.1, 5)
    for i in range(6):
        L(ax, [x + w / 2 - 1.3 + i * 0.52] * 2, [y + 0.3, y + 0.7], "#9e9e9e", 4); L(ax, [x + w / 2 - 1.3 + i * 0.52] * 2, [y + 2.3, y + 2.7], "#9e9e9e", 4)
    T(ax, x + w / 2, y + 1.5, "IC", 18, "white")
    p.bul(["Many semiconductors + parts in one package: INTEGRATED CIRCUIT"], size=13)

SLIDES = [
    dict(title="Resistors, capacitors, inductors, switches & batteries", ids=["T6A01", "T6A02", "T6A03", "T6A04", "T6A05", "T6A06", "T6A07", "T6A08", "T6A09", "T6A10", "T6A11"], draw=d_passive,
         tip="Capacitor = electric field (plates plus insulator). Inductor = magnetic field (coil). Carbon-zinc is not rechargeable."),
    dict(title="Diodes, LEDs & transistors", ids=["T6B02", "T6B09", "T6B06", "T6B01", "T6B07", "T6B03", "T6B04", "T6B10", "T6B05", "T6B08", "T6B12", "T6B11"], draw=d_semis,
         tip="Diode = one-way current (stripe = cathode). Transistor = switch or amplifier. FET = gate, drain, source."),
    dict(title="Schematic figure T-1", ids=["T6C01", "T6C02", "T6C03", "T6C04", "T6C05", "T6D10", "T6C12"], draw=d_fig1,
         tip="Figure T-1: 1 resistor, 2 transistor, 3 lamp, 4 battery."),
    dict(title="Schematic figures T-2 & T-3", ids=["T6C06", "T6C07", "T6C08", "T6C09", "T6C10", "T6C11"], draw=d_fig23,
         tip="T-2: 4 transformer, 6 capacitor, 8 LED, 9 variable resistor. T-3: 3 variable inductor, 4 antenna."),
    dict(title="Rectifiers, regulators, relays & ICs", ids=["T6D01", "T6D05", "T6D06", "T6D02", "T6D03", "T6D08", "T6D11", "T6D04", "T6D07", "T6D09"], draw=d_circuits,
         tip="Transformer lowers AC, rectifier turns AC into DC, regulator holds the voltage steady. L + C = tuned circuit."),
]

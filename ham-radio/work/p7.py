from core2 import *

def chain_box(ax, x, y, w, h, t, c):
    LBOX(ax, x, y, w, h, t, 14, tint(c, 0.8), c, "#111")

def d_rxtx(ax):
    r = grid([(1.05, [1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Inside a transceiver", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#c5cae9", bot_c="#e8eaf6")
    blocks = [("🎤", "Microphone", ""), ("〰️", "MODULATION", "speech + RF carrier"), ("🔀", "MIXER", "changes frequency"), ("🎛️", "VFO / OSCILLATOR", "sets the frequency"), ("📶", "RF POWER AMP", "more output power"), ("📡", "Antenna", "")]
    bw = (w - 0.4) / len(blocks)
    for i, (e, t1, t2) in enumerate(blocks):
        bx = x + 0.2 + i * bw
        RBOX(ax, bx + 0.15, y + 0.3, bw - 0.6, h - 0.6, ["#fff9c4", "#ffe0b2", "#c8e6c9", "#b3e5fc", "#f8bbd0", "#d1c4e9"][i], INDIGO, 2, 0.2, 4)
        E(ax, e, bx + (bw - 0.45) / 2 + 0.07, y + h - 1.3, 1.5)
        T(ax, bx + (bw - 0.45) / 2 + 0.07, y + 1.6, t1, 14, INDIGO)
        if t2: T(ax, bx + (bw - 0.45) / 2 + 0.07, y + 0.85, t2, 11.5, "#333", False)
        if i < len(blocks) - 1: ARROW(ax, bx + bw - 0.45, y + h / 2, bx + bw + 0.15, y + h / 2, RED, 3, ms=16)
    p = P(ax, r[1], "Receiver words", BLUE, 2)
    p.table([["Term", "Meaning"], ["Sensitivity", "can DETECT a weak signal"], ["Selectivity", "can SEPARATE nearby signals"], ["Transceiver", "receiver + transmitter in one"]], [1.15, 1.5], size=14, fill=True)
    p = P(ax, r[2], "Circuits & add-ons", GREEN, 3)
    p.table([["Part", "Job"], ["Oscillator", "makes a signal at one frequency"], ["Mixer", "converts one frequency to another"], ["Transverter", "moves a rig to another band"], ["RF power amp", "increases output power"]], [1, 1.6], size=13, fill=True)
    p = P(ax, r[3], "PTT & amp switch", ORANGE, 4)
    p.icons([("🔘", "PTT grounded\n= transmit"), ("🔀", "SSB / CW-FM\nswitch")], 2.8)
    p.bul(["PTT input: switches from receive to transmit when GROUNDED", "Amp mode switch: sets amp for proper operation in that mode"], size=12)

def d_rfi(ax):
    r = grid([(1.1, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Interference: your signal gets where it shouldn't", RED, 1)
    x, y, w, h = p.scene(p.h - 0.1, "sky")
    E(ax, "🏠", x + 1.6, y + 1.5, 2.2); TOWER(ax, x + 3.2, y + 0.45, 2.8)
    E(ax, "🏡", x + w - 2.0, y + 1.5, 2.2); E(ax, "📺", x + w - 4.2, y + 1.2, 1.3); E(ax, "📻", x + w - 5.6, y + 1.2, 1.2)
    for k in range(4): ax.add_patch(Arc((x + 3.2, y + 3.25), 1.2 + k * 1.4, 1.2 + k * 1.4, theta1=-40, theta2=40, color=RED, lw=3, zorder=5))
    LBOX(ax, x + w * 0.35, y + h - 1.3, w * 0.6, 1.0, "Neighbor's AM/FM radio can't reject strong signals outside its band", 12, "#fff", RED, RED)
    p = P(ax, r[1], "Causes of RFI", ORANGE, 2)
    p.icons([("💥", "overload"), ("🎶", "harmonics"), ("👻", "spurious")], 2.2)
    p.ok(["Fundamental overload", "Harmonics", "Spurious emissions", "→ All these choices are correct"], size=14)
    p.bul(["Low RF output from solid-state rig: HIGH SWR"], size=13)
    p = P(ax, r[2], "Neighbor complains", BLUE, 3)
    p.icons([("🔎", "check YOUR\nstation first"), ("🤝", "be polite")], 2.4)
    p.bul(["First: make sure your station works right & doesn't cause interference to your own TV/radio"], size=12)
    p = P(ax, r[3], "Fixes with filters", GREEN, 4)
    p.table([["Problem", "Fix"], ["Your signal into their TV", "Filter at THEIR antenna input"], ["FM broadcast into 2 m rig", "Band-reject filter"], ["Cable TV RFI (non-fiber)", "Check coax connectors first"]], [1.2, 1.3], size=12, fill=True)
    p = P(ax, r[4], "Their device bothers you", PURPLE, 5)
    p.icons([("🏡", "neighbor's\ngadget"), ("🗣️", "talk\npolitely")], 2.4)
    p.ok(["Work with neighbor to find the cause", "Politely tell them the rules", "Check your own station → All correct"], size=12)

def d_audio(ax):
    r = grid([(1, [1.4, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Distorted audio through a repeater", PURPLE, 1)
    x, y, w, h = p.scene(3.8, "sky")
    HT(ax, x + 1.2, y + 0.45, 0.8); TOWER(ax, x + w - 1.5, y + 0.45, 3.0)
    xs = np.linspace(x + 2.0, x + w - 2.6, 300)
    ax.plot(xs, y + 2.4 + 0.5 * np.sin((xs - x) * 5) + 0.2 * np.sin((xs - x) * 23), color=PURPLE, lw=2.5, zorder=5)
    T(ax, x + w / 2, y + 3.4, "garbled? unintelligible?", 14, PURPLE)
    p.ok(["Wrong frequency", "Low battery", "Bad location → All correct"], size=13)
    p = P(ax, r[1], "Ferrite choke", GREEN, 2)
    x, y, w, h = p.scene(3.4, top_c="#c8e6c9", bot_c="#e8f5e9")
    L(ax, [x + 0.3, x + w - 0.3], [y + h / 2, y + h / 2], "#212121", 6)
    RBOX(ax, x + w / 2 - 1.0, y + h / 2 - 0.6, 2.0, 1.2, "#424242", "#000", 2, 0.4, 5)
    E(ax, "🎤", x + 0.9, y + h / 2 + 0.9, 1.0)
    T(ax, x + w / 2, y + 0.4, "clip-on ferrite on mic cable", 12, GREEN)
    p.bul(["Fixes distorted voice: ferrite CHOKE on the mic cable keeps RF out"], size=13)
    p = P(ax, r[2], "Check the basics", BLUE, 3)
    p.icons([("🔋", "battery"), ("📍", "location"), ("📻", "frequency")], 2.6)
    p.bul(["Most audio trouble reports: something simple"], size=13)
    p = P(ax, r[3], "RF in the shack", ORANGE, 4)
    p.icons([("⚡", "RF"), ("🎤", "mic cable")], 2.6)
    p.bul(["RF getting into audio causes distortion"], size=13)
    p = P(ax, r[4], "Remember", GOLD, 5)
    p.icons([("🗣️", "distorted"), ("🧲", "ferrite")], 2.4)
    p.formula("Distorted voice?\n→ ferrite choke", 18)

def d_swr(ax):
    r = grid([(1.05, [1.3, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "SWR: how well antenna and feed line match", RED, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#ffcdd2", bot_c="#ffebee")
    cx, cy = x + w * 0.3, y + 0.8
    ax.add_patch(Wedge((cx, cy), 3.4, 20, 160, fc="#fff", ec="#333", lw=3, zorder=4))
    ax.add_patch(Wedge((cx, cy), 3.4, 125, 160, fc="#a5d6a7", ec="none", zorder=4.2))
    ax.add_patch(Wedge((cx, cy), 3.4, 20, 60, fc="#ef9a9a", ec="none", zorder=4.2))
    for ang, lab in [(155, "1:1"), (125, "1.5"), (95, "2:1"), (60, "3:1"), (28, "∞")]:
        a = np.radians(ang); T(ax, cx + 2.75 * np.cos(a), cy + 2.75 * np.sin(a), lab, 13)
    L(ax, [cx, cx + 3.0 * np.cos(np.radians(152))], [cy, cy + 3.0 * np.sin(np.radians(152))], RED, 4, 6)
    LBOX(ax, x + w * 0.6, y + h - 1.6, w * 0.38, 1.3, "1:1 = PERFECT match", 16, "#e8f5e9", GREEN, GREEN)
    LBOX(ax, x + w * 0.6, y + h - 3.2, w * 0.38, 1.3, "4:1 = impedance MISMATCH", 15, "#ffebee", RED, RED)
    LBOX(ax, x + w * 0.6, y + 0.4, w * 0.38, 1.3, "High SWR → rig cuts power to protect its transistors", 13, "#fff8e1", GOLD, "#5d4037")
    p = P(ax, r[1], "Test equipment", BLUE, 2)
    p.table([["Tool", "Use"], ["Dummy load", "test WITHOUT transmitting over the air"], ["Antenna analyzer", "is the antenna RESONANT?"], ["Directional wattmeter", "measures SWR"]], [1.1, 1.5], size=13, fill=True)
    p = P(ax, r[2], "Dummy load", GREEN, 3)
    x, y, w, h = p.scene(2.8, top_c="#c8e6c9", bot_c="#e8f5e9")
    for i in range(9): ax.add_patch(Rectangle((x + 1.0 + i * 0.35, y + 0.4), 0.2, h - 0.8, fc="#78909c", zorder=4))
    RBOX(ax, x + 0.8, y + h / 2 - 0.35, 3.3, 0.7, "#ffcc80", "#e65100", 2, 0.1, 5)
    T(ax, x + w - 1.6, y + h / 2, "50 Ω\nresistor\n+ heat sink", 12, GREEN)
    p.bul(["50-ohm NON-INDUCTIVE resistor on a heat sink"], size=13)
    p = P(ax, r[3], "Feed line loss", ORANGE, 4)
    p.icons([("🔥", "lost power\n= HEAT")], 2.4)
    p.bul(["Power lost in a feed line: converted into HEAT"], size=13)
    p = P(ax, r[4], "Coax care", TEAL, 5)
    p.table([["Fact", "Answer"], ["Coax fails from", "MOISTURE"], ["UV-resistant jacket", "UV cracks → water gets in"], ["Foam dielectric", "LESS loss per foot"]], [1, 1.3], size=12, fill=True)

def d_meters(ax):
    r = grid([(1.1, [1, 1]), (1, [1, 1, 1])])
    for k, (title, c, how, what) in enumerate([("VOLTMETER: connect in PARALLEL", BLUE, "parallel", "measures VOLTAGE (electric potential)"),
                                                ("AMMETER: connect in SERIES", RED, "series", "measures CURRENT")]):
        p = P(ax, r[k], title, c, k + 1)
        x, y, w, h = p.scene(p.h - 1.0, top_c=tint(c, 0.75), bot_c=tint(c, 0.9))
        x0, x1, yb, yt = x + 0.8, x + w - 0.8, y + 0.6, y + h - 0.9
        L(ax, [x0, x0, x1, x1, x0], [yb, yt, yt, yb, yb], "#333", 3)
        ax.add_patch(Rectangle((x0 - 0.35, (yb + yt) / 2 - 0.5), 0.7, 1.0, fc=tint(c, 0.8), ec="none", zorder=4.5))
        L(ax, [x0 - 0.3, x0 + 0.3], [(yb + yt) / 2 + 0.2] * 2, "#000", 4, 5); L(ax, [x0 - 0.15, x0 + 0.15], [(yb + yt) / 2 - 0.2] * 2, "#000", 4, 5)
        ax.add_patch(Rectangle((x1 - 0.35, yb + 0.5), 0.7, yt - yb - 1.0, fc=tint(c, 0.8), ec="none", zorder=4.5)); RESV(ax, x1, yb + 0.5, yt - 0.5)
        if how == "parallel":
            mx = x1 - 2.6
            L(ax, [x1, mx, mx], [yt - 0.2, yt - 0.2, (yb + yt) / 2 + 0.6], c, 2.5); L(ax, [x1, mx, mx], [yb + 0.2, yb + 0.2, (yb + yt) / 2 - 0.6], c, 2.5)
            ax.add_patch(Circle((mx, (yb + yt) / 2), 0.6, fc="#fff", ec=c, lw=3, zorder=6)); T(ax, mx, (yb + yt) / 2, "V", 18, c, z=7)
        else:
            mx = (x0 + x1) / 2
            ax.add_patch(Rectangle((mx - 0.7, yt - 0.3), 1.4, 0.6, fc=tint(c, 0.8), ec="none", zorder=4.5))
            ax.add_patch(Circle((mx, yt), 0.6, fc="#fff", ec=c, lw=3, zorder=6)); T(ax, mx, yt, "A", 18, c, z=7)
        T(ax, (x0 + x1) / 2 - (0.6 if how == "parallel" else 0), (yb + yt) / 2 - (0 if how == "parallel" else 0.3), "across the part" if how == "parallel" else "in the path", 14, c)
        p.bul([what.split(" (")[0].capitalize() + (": " + what.split("(")[1].rstrip(")") if "(" in what else "")], size=14)
    p = P(ax, r[2], "Multimeter", GREEN, 3)
    p.icons([("📟", "V • A • Ω")], 1.8)
    p.bul(["Measures: VOLTAGE and RESISTANCE", "Damage: measuring voltage on the RESISTANCE setting"], size=13)
    p = P(ax, r[3], "Ohmmeter tips", PURPLE, 4)
    p.icons([("🔌", "power OFF"), ("Ω", "")] if False else [("🔌", "power OFF"), ("📈", "cap: R rises")], 2.0)
    p.bul(["How it works: applies a small current, measures the voltage", "In-circuit: make sure circuit is NOT powered", "Big discharged capacitor: resistance INCREASES with time"], size=12)
    p = P(ax, r[4], "Soldering", ORANGE, 5)
    p.icons([("🔥", "iron"), ("✘", "acid-core")], 1.8)
    p.no(["Acid-core solder: never for electronics"], size=12)
    p.bul(["Cold joint: ROUGH or LUMPY surface"], size=12)

SLIDES = [
    dict(title="Transceiver building blocks", ids=["T7A02", "T7A01", "T7A04", "T7A05", "T7A03", "T7A11", "T7A08", "T7A06", "T7A10", "T7A09", "T7A07"], draw=d_rxtx,
         tip="Sensitivity = hearing weak signals. Selectivity = separating close signals. Mixer = changes frequency."),
    dict(title="Radio frequency interference (RFI)", ids=["T7B02", "T7B03", "T7B04", "T7B05", "T7B06", "T7B07", "T7B08", "T7B09"], draw=d_rfi,
         tip="Check your own station first. Filters go on the affected equipment. Band-reject filters block FM broadcast."),
    dict(title="Distorted audio & ferrite chokes", ids=["T7B10", "T7B11"], draw=d_audio,
         tip="Distorted voice? Try a clip-on ferrite choke on the mic cable."),
    dict(title="SWR, dummy loads & coax", ids=["T7C04", "T7C06", "T7C05", "T7C01", "T7C03", "T7C02", "T7C08", "T7C07", "T7C09", "T7C10", "T7C11"], draw=d_swr,
         tip="1:1 = perfect match. Dummy load = 50 Ω resistor. Coax fails from moisture; foam has less loss."),
    dict(title="Meters & soldering", ids=["T7D01", "T7D02", "T7D04", "T7D03", "T7D07", "T7D06", "T7D05", "T7D11", "T7D10", "T7D08", "T7D09"], draw=d_meters,
         tip="Voltmeter in parallel, ammeter in series. Never use acid-core solder. Cold joint = lumpy."),
]

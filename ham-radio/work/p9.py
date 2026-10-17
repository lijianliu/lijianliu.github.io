from core2 import *

def d_antennas(ax):
    r = grid([(1.1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Half-wave dipole", BLUE, 1)
    x, y, w, h = p.scene(3.6, "sky")
    TOWER(ax, x + 0.8, y + 0.45, 2.6); TOWER(ax, x + w - 0.8, y + 0.45, 2.6)
    L(ax, [x + 0.9, x + w / 2 - 0.15], [y + 3.0, y + 3.0], "#333", 4); L(ax, [x + w / 2 + 0.15, x + w - 0.9], [y + 3.0, y + 3.0], "#333", 4)
    L(ax, [x + w / 2, x + w / 2], [y + 3.0, y + 0.45], "#212121", 2.5)
    ARROW(ax, x + w / 2, y + 2.8, x + w / 2, y + 1.3, RED, 4); ARROW(ax, x + w / 2 + 1.5, y + 2.5, x + w / 2 + 1.5, y + 1.3, RED, 3)
    T(ax, x + w / 2 - 1.8, y + 1.8, "strongest:\nBROADSIDE", 12, RED)
    p.bul(["Strongest signal: BROADSIDE to the antenna", "Shorten it: resonant frequency goes UP"], size=13)
    p = P(ax, r[1], "Yagi beam", GREEN, 2)
    x, y, w, h = p.scene(3.6, top_c="#c8e6c9", bot_c="#e8f5e9")
    L(ax, [x + 0.6, x + w * 0.6], [y + h / 2, y + h / 2], "#333", 4)
    for i, hh in enumerate([1.4, 1.2, 1.05, 0.95, 0.85]):
        xx = x + 0.8 + i * (w * 0.6 - 0.8) / 4; L(ax, [xx, xx], [y + h / 2 - hh, y + h / 2 + hh], "#333", 3.5)
    ax.add_patch(Ellipse((x + w * 0.8, y + h / 2), w * 0.36, 1.6, fc="#66bb6a88", ec=GREEN, lw=2, zorder=4))
    p.bul(["Beam: CONCENTRATES signals in one direction", "Greatest gain: YAGI"], size=13)
    p = P(ax, r[2], "Gain & loading", ORANGE, 3)
    x, y, w, h = p.scene(3.6, top_c="#ffe0b2", bot_c="#fff3e0")
    L(ax, [x + 1.2, x + 1.2], [y + 0.4, y + h - 0.4], "#333", 4)
    t = np.linspace(0, 1, 200); ax.plot(x + 1.2 + 0.3 * np.sin(2 * np.pi * 6 * t), y + 1.2 + 1.0 * t, color="#b87333", lw=3, zorder=5)
    T(ax, x + w / 2 + 0.8, y + h / 2, "coil = inductor\n→ electrically\nLONGER", 13, ORANGE)
    p.bul(["Gain: more signal in one direction vs a reference antenna", "Loading: inserting INDUCTORS to electrically lengthen"], size=12)
    p = P(ax, r[3], "Vertical lengths on 2 m", PURPLE, 4)
    p.table([["Antenna", "Fact"], ["19-inch vertical", "resonant QUARTER-wave on 2 m"], ["5/8-wave whip", "MORE gain than 1/4-wave"], ["Rubber duck", "LOW efficiency"]], [1, 1.5], size=13, fill=True)
    p = P(ax, r[4], "Polarization", TEAL, 5)
    x, y, w, h = p.scene(2.6)
    L(ax, [x + 1.4, x + 1.4], [y + 0.3, y + h - 0.3], "#333", 6); T(ax, x + 1.4, y + 0.2, "vertical", 11, "#333")
    WAVE(ax, x + 2.2, x + w - 0.4, y + h / 2, 0.8, 3, RED, lw=3); T(ax, x + w / 2 + 1.0, y + h - 0.3, "E field", 12, RED)
    p.bul(["Described by: orientation of the ELECTRIC field"], size=13)
    p = P(ax, r[5], "HT inside a car", RED, 6)
    p.icons([("🚗", "metal body"), ("📻", "HT inside"), ("📉", "weak signal")], 2.6)
    p.bul(["No outside antenna: vehicle SHIELDING reduces signal"], size=13)

def d_feed(ax):
    r = grid([(1.05, [1.4, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Coax cable & connectors", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#c5cae9", bot_c="#e8eaf6")
    cx, cy = x + 2.6, y + h / 2
    for rr, c, lab in [(2.2, "#212121", "jacket"), (1.8, "#b0bec5", "braid shield"), (1.4, "#fafafa", "dielectric"), (0.35, "#b87333", "center")]:
        ax.add_patch(Circle((cx, cy), rr, fc=c, ec="#333", lw=1.5, zorder=5))
    T(ax, cx, y + 0.3, "50 Ω coax (most common)", 13, INDIGO)
    for i, (n, t1, c) in enumerate([("PL-259", "HF & VHF", "#90caf9"), ("Type N", "best above 400 MHz", "#a5d6a7"), ("RG-213", "less loss than RG-58", "#ffcc80"), ("Hardline", "air-insulated: LOWEST loss", "#f48fb1")]):
        LBOX(ax, x + 5.4 + (i % 2) * ((w - 5.7) / 2), y + 0.3 + (1 - i // 2) * ((h - 0.6) / 2), (w - 5.7) / 2 - 0.2, (h - 0.6) / 2 - 0.2, f"{n}\n{t1}", 15, c, "#333")
    p = P(ax, r[1], "Feed line facts", BLUE, 2)
    p.table([["Question", "Answer"], ["Most common impedance", "50 ohms"], ["Why coax?", "easy, few special needs"], ["Higher frequency", "MORE loss"], ["Loss sources", "All these choices are correct"]], [1.2, 1.2], size=13, fill=True)
    p = P(ax, r[2], "Antenna tuner", GREEN, 3)
    x, y, w, h = p.scene(2.8)
    RADIO(ax, x + 0.3, y + 0.6, 2.4, 1.4, "")
    LBOX(ax, x + 3.0, y + 0.6, 2.2, 1.4, "TUNER", 14, "#fff59d", GOLD)
    L(ax, [x + 2.7, x + 3.0], [y + 1.3] * 2, "#333", 3); L(ax, [x + 5.2, x + w - 0.4], [y + 1.3] * 2, "#333", 3); L(ax, [x + w - 0.4] * 2, [y + 1.3, y + 2.5], "#333", 3)
    p.bul(["Matches antenna system impedance to the transceiver's output"], size=13)
    p = P(ax, r[3], "SWR & loose connections", RED, 4)
    p.icons([("🔩", "loose\nconnector"), ("📈", "erratic SWR")], 2.6)
    p.bul(["SWR: how well a load MATCHES a transmission line", "Erratic SWR: LOOSE connection in antenna or feed line"], size=12)
    p = P(ax, r[4], "Weatherproofing", TEAL, 5)
    p.icons([("🌧️", "rain"), ("🩹", "tape it")], 2.6)
    p.ok(["Tape outdoor connectors: All these choices are correct"], size=13)

SLIDES = [
    dict(title="Antenna types, gain & polarization", ids=["T9A10", "T9A05", "T9A01", "T9A06", "T9A11", "T9A02", "T9A08", "T9A09", "T9A04", "T9A03", "T9A07"], draw=d_antennas,
         tip="Dipole radiates broadside. Yagi = most gain. Shorter antenna = higher frequency. 19-inch = quarter-wave on 2 m."),
    dict(title="Feed lines, connectors & SWR", ids=["T9B02", "T9B03", "T9B05", "T9B08", "T9B10", "T9B11", "T9B06", "T9B07", "T9B04", "T9B12", "T9B09", "T9B01"], draw=d_feed,
         tip="50 Ω coax. Higher frequency = more loss. Type N above 400 MHz. Hardline has the lowest loss."),
]

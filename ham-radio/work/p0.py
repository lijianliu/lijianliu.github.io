from core2 import *

def d_elec(ax):
    r = grid([(1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Battery dangers", RED, 1)
    x, y, w, h = p.scene(2.8, top_c="#ffcdd2", bot_c="#ffebee")
    RBOX(ax, x + 0.5, y + 0.4, 3.0, 1.8, "#424242", "#000", 2, 0.15, 4)
    ax.add_patch(Rectangle((x + 0.9, y + 2.2), 0.5, 0.3, fc=RED, zorder=4)); ax.add_patch(Rectangle((x + 2.6, y + 2.2), 0.5, 0.3, fc="#000", zorder=4))
    T(ax, x + 2.0, y + 1.3, "12 V", 16, "white"); E(ax, "🔥", x + w - 1.4, y + h / 2, 1.6)
    p.bul(["Short the terminals: BURNS, FIRE or EXPLOSION", "Fast charge/discharge: OVERHEATING or out-gassing"], size=12)
    p = P(ax, r[1], "Current through the body", ORANGE, 2)
    p.icons([("🔥", "heat\ntissue"), ("⚡", "nerves"), ("❤️", "heart")], 2.6)
    p.ok(["Health hazards: All these choices are correct"], size=13)
    p = P(ax, r[2], "AC wiring colors (US)", GOLD, 3)
    x, y, w, h = p.scene(2.6)
    for i, (c, t) in enumerate([("#000", "BLACK = HOT"), ("#fafafa", "WHITE = neutral"), ("#2e7d32", "GREEN = ground")]):
        L(ax, [x + 0.4, x + 2.6], [y + h - 0.5 - i * 0.8] * 2, c, 9, 5); L(ax, [x + 0.4, x + 2.6], [y + h - 0.5 - i * 0.8] * 2, "#333", 10.5, 4.9)
        T(ax, x + 2.9, y + h - 0.5 - i * 0.8, t, 13, "#222", ha="left")
    p.bul(["Fuse/breaker: in SERIES with the HOT conductor only"], size=12)
    p = P(ax, r[3], "Fuses", BLUE, 4)
    x, y, w, h = p.scene(2.6)
    for i, (a, ok) in enumerate([("5 A", True), ("20 A", False)]):
        bx = x + 0.4 + i * (w / 2)
        RBOX(ax, bx, y + 0.8, w / 2 - 0.8, 1.0, "#e3f2fd", "#555", 2, 0.4, 4); L(ax, [bx + 0.3, bx + w / 2 - 1.1], [y + 1.3] * 2, "#9e9e9e", 2, 5)
        T(ax, bx + (w / 2 - 0.8) / 2, y + 2.2, a + (" ✔" if ok else " ✘"), 14, GREEN if ok else RED, family="DejaVu Sans")
    p.bul(["Fuse: removes power on OVERLOAD", "Never 5 A → 20 A: excess current could cause a FIRE"], size=12)
    p = P(ax, r[4], "Stay safe from shock", GREEN, 5)
    p.icons([("⏚", "safety\nground"), ("🔌", "GFCI"), ("🧤", "cover\nwires")], 2.4)
    p.ok(["Common safety ground", "Ground-fault interrupter (GFCI)", "Cover exposed wires → All correct"], size=13)
    p = P(ax, r[5], "After power OFF", PURPLE, 6)
    p.icons([("🔌", "unplugged"), ("⚡", "capacitors\nstill charged")], 2.6)
    p.bul(["Hazard: charge stored in FILTER CAPACITORS", "High-voltage meter: leads RATED for that voltage"], size=12)

def d_tower(ax):
    r = grid([(1.1, [1.4, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Antenna & tower safety", ORANGE, 1)
    x, y, w, h = p.scene(p.h - 0.1, "sky")
    TOWER(ax, x + 2.6, y + 0.45, h - 1.0, 1.2)
    E(ax, "🧗", x + 2.6, y + h * 0.55, 1.2); E(ax, "🧑‍🔧", x + 4.6, y + 1.3, 1.3); T(ax, x + 4.6, y + 0.15 + 0.45, "helper", 11, "#111")
    L(ax, [x + w - 1.0, x + w - 1.0], [y + 0.45, y + h - 0.5], "#5d4037", 6)
    L(ax, [x + w - 4.5, x + w - 1.0], [y + h - 1.0, y + h - 0.8], "#000", 2); L(ax, [x + w - 4.5, x + w - 1.0], [y + h - 1.4, y + h - 1.2], "#000", 2)
    E(ax, "⚡", x + w - 2.8, y + h - 2.0, 1.0)
    ax.add_patch(Arc((x + 6.6, y + 0.45), 6.0, 6.0, theta1=0, theta2=90, color=RED, lw=2.5, ls="--", zorder=5))
    LBOX(ax, x + 5.2, y + 3.6, w - 8.4, 1.1, "If it falls, no part comes within 10 FEET of power lines", 12, "#fff", RED, RED)
    p = P(ax, r[1], "Climbing rules", RED, 2)
    p.table([["Rule", "Answer"], ["Climb alone?", "NEVER"], ["Required gear", "harness, hard hat, glasses → All"], ["Crank-up tower", "don't climb unless retracted or blocked"], ["Turnbuckle safety wire", "stops loosening from vibration"]], [1, 1.5], size=12, fill=True)
    p = P(ax, r[2], "Stay off utility poles", PURPLE, 3)
    p.icons([("🚫", ""), ("⚡", "high-voltage\nlines")], 2.6)
    p.bul(["Antenna could contact HIGH-VOLTAGE lines", "Putting up a tower: look for & stay clear of overhead wires"], size=12)
    p = P(ax, r[3], "Grounding the tower", GREEN, 4)
    x, y, w, h = p.scene(2.8, top_c="#d7ccc8", bot_c="#efebe9")
    ax.add_patch(Polygon([(x + w / 2 - 1.2, y + 1.2), (x + w / 2, y + h - 0.2), (x + w / 2 + 1.2, y + 1.2)], fc="none", ec="#607d8b", lw=3, zorder=4))
    for dx in (-1.2, 0, 1.2): L(ax, [x + w / 2 + dx] * 2, [y + 1.2, y + 0.2], "#b87333", 4, 5)
    L(ax, [x + w / 2 - 1.2, x + w / 2 + 1.2], [y + 0.7] * 2, "#b87333", 3, 5)
    p.bul(["Separate 8-FOOT ground rods per leg, bonded together", "Short & direct, NO sharp bends"], size=12)
    p = P(ax, r[4], "Lightning & codes", BLUE, 5)
    p.table([["Item", "Answer"], ["Lightning arrester", "grounded panel where feed lines enter"], ["All ground rods", "BOND together"], ["Grounding rules from", "LOCAL electrical codes"]], [1, 1.4], size=12, fill=True)

def d_rf(ax):
    r = grid([(1.05, [1.4, 1]), (1, [1, 1, 1, 1])])
    p = P(ax, r[0], "RF is NON-ionizing radiation", TEAL, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#b2dfdb", bot_c="#e0f2f1")
    names = [("Radio", "#81c784"), ("Microwave", "#aed581"), ("Infrared", "#ffb74d"), ("Light", "#fff176"), ("UV", "#ce93d8"), ("X-ray", "#e57373")]
    bw = (w - 0.4) / 6
    for i, (n, c) in enumerate(names):
        LBOX(ax, x + 0.2 + i * bw, y + h - 2.0, bw - 0.08, 1.6, n, 15, c, "#333")
    L(ax, [x + 0.2 + 4 * bw - 0.04] * 2, [y + 0.3, y + h - 0.2], RED, 4, 6, "--")
    LBOX(ax, x + 0.3, y + 0.4, 4 * bw - 0.6, 1.8, "NON-ionizing: not enough energy to cause chemical changes in cells or damage DNA", 13, "#e8f5e9", GREEN, GREEN)
    LBOX(ax, x + 4 * bw + 0.2, y + 0.4, 2 * bw - 0.4, 1.8, "IONIZING (radioactivity)", 13, "#ffebee", RED, RED)
    p = P(ax, r[1], "Duty cycle", ORANGE, 2)
    x, y, w, h = p.scene(2.4, top_c="#ffe0b2", bot_c="#fff3e0")
    for i in range(6):
        ax.add_patch(Rectangle((x + 0.4 + i * (w - 0.8) / 6, y + 0.4), (w - 0.8) / 12, h - 0.8, fc="#ef6c00", zorder=4))
    p.bul(["Duty cycle: % of time the transmitter is transmitting", "Matters because it affects AVERAGE exposure", "100% → 50%: allowed power density ×2"], size=12)
    p = P(ax, r[2], "Exposure rules", RED, 3)
    p.table([["Question", "Answer"], ["Lowest max exposure band", "50 MHz"], ["Why limits vary with f", "body absorbs more at some f"], ["Who is responsible", "STATION LICENSEE"]], [1.2, 1.2], size=12, fill=True)
    p = P(ax, r[3], "What affects exposure", BLUE, 4)
    p.icons([("📶", "power &\nfrequency"), ("📏", "distance"), ("📡", "pattern")], 2.2)
    p.ok(["Frequency & power level", "Distance from antenna", "Radiation pattern → All correct"], size=12)
    p.ok(["Check compliance: calculation, computer modeling, measurement → All correct"], size=12)
    p = P(ax, r[4], "Touching an antenna", PINK, 5)
    p.icons([("✋", "touch"), ("📡", "transmitting"), ("🔥", "RF burn")], 2.4)
    p.bul(["Hazard: RF BURN to skin"], size=13)
    p = P(ax, r[5], "Reduce & re-check", GREEN, 6)
    p.icons([("↔️", "relocate\nantennas"), ("🔁", "re-evaluate\non changes")], 2.4)
    p.bul(["Reduce exposure: RELOCATE antennas", "Stay compliant: re-evaluate when transmitter or antenna changes"], size=12)

SLIDES = [
    dict(title="Electrical safety: batteries, fuses & wiring", ids=["T0A01", "T0A10", "T0A02", "T0A03", "T0A08", "T0A04", "T0A05", "T0A06", "T0A11", "T0A12"], draw=d_elec,
         tip="Black wire = hot. Never replace a fuse with a bigger one. Capacitors stay charged after power-off."),
    dict(title="Tower, antenna & lightning safety", ids=["T0B03", "T0B02", "T0B07", "T0B05", "T0B04", "T0B06", "T0B09", "T0B01", "T0B08", "T0B10", "T0A07", "T0A09", "T0B11"], draw=d_tower,
         tip="Never climb alone. Stay 10 feet from power lines even if the antenna falls. Short, direct ground wires with no sharp bends."),
    dict(title="RF exposure safety", ids=["T0C01", "T0C12", "T0C11", "T0C10", "T0C03", "T0C02", "T0C05", "T0C13", "T0C04", "T0C06", "T0C07", "T0C08", "T0C09"], draw=d_rf,
         tip="RF is non-ionizing. Duty cycle affects average exposure. The station licensee is responsible."),
]

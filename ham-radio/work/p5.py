from core2 import *

def ohm_triangle(ax, x, y, w, h, top="E", bl="I", br="R", ct=GREEN, cl=RED, cr=PURPLE, fc="#e3f2fd", ec=BLUE):
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w / 2, y + h)], fc=fc, ec=ec, lw=4, zorder=4))
    L(ax, [x + w * 0.25, x + w * 0.75], [y + h / 2, y + h / 2], ec, 4, 5); L(ax, [x + w / 2, x + w / 2], [y, y + h / 2], ec, 4, 5)
    T(ax, x + w / 2, y + h * 0.66, top, 34, ct); T(ax, x + w * 0.33, y + h * 0.22, bl, 30, cl); T(ax, x + w * 0.67, y + h * 0.22, br, 30, cr)

def d_basics(ax):
    r = grid([(1.1, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Electricity is like water in a pipe", BLUE, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#bbdefb", bot_c="#e3f2fd")
    ax.add_patch(Rectangle((x + 0.5, y + 1.2), 2.4, h - 1.6, fc="#bbdefb", ec=BLUE, lw=3, zorder=4))
    ax.add_patch(Rectangle((x + 0.5, y + 1.2), 2.4, (h - 1.6) * 0.8, fc="#42a5f5", zorder=4))
    ax.add_patch(Rectangle((x + 2.9, y + 1.4), w * 0.5, 0.8, fc="#42a5f5", ec=BLUE, lw=3, zorder=4))
    for i in range(5): ARROW(ax, x + 3.3 + i * 1.3, y + 1.8, x + 4.1 + i * 1.3, y + 1.8, "white", 3, ms=16, z=6)
    ax.add_patch(Rectangle((x + 2.9 + w * 0.5, y + 1.6), 2.0, 0.4, fc="#42a5f5", ec=RED, lw=3, zorder=4))
    LBOX(ax, x + 0.3, y + 0.15, 3.0, 0.9, "VOLTAGE = push", 13, "#fff", BLUE, BLUE)
    LBOX(ax, x + 4.0, y + 2.6, 5.0, 0.9, "CURRENT = flow of electrons", 13, "#fff", BLUE, BLUE)
    LBOX(ax, x + w - 4.8, y + 2.6, 4.5, 0.9, "RESISTANCE = narrow pipe", 13, "#fff", RED, RED)
    LBOX(ax, x + w - 4.8, y + h - 1.2, 4.5, 0.9, "POWER = rate energy used", 13, "#fff", ORANGE, ORANGE)
    LBOX(ax, x + 4.0, y + h - 1.2, 5.0, 0.9, "Voltage DIFFERENCE causes flow", 13, "#fff8e1", GOLD, "#5d4037")
    p = P(ax, r[1], "Quantity → unit", RED, 2)
    p.table([["Quantity", "Unit"], ["Current", "Ampere (A)"], ["Voltage", "Volt (V)"], ["Power", "Watt (W)"], ["Resistance / impedance", "Ohm (Ω)"], ["Frequency", "Hertz (Hz)"], ["Capacitance", "Farad (F)"], ["Inductance", "Henry (H)"]], [1.4, 1], size=13, fill=True)
    p = P(ax, r[2], "AC vs DC", ORANGE, 3)
    x, y, w, h = p.scene(3.0, top_c="#fff3e0", bot_c="#fafafa")
    L(ax, [x + 0.3, x + w - 0.3], [y + h - 0.6, y + h - 0.6], RED, 4, 5); T(ax, x + w / 2, y + h - 0.25, "DC: one direction", 12, RED)
    WAVE(ax, x + 0.3, x + w - 0.3, y + 1.0, 0.6, 3, BLUE, lw=3); T(ax, x + w / 2, y + 0.2, "AC: alternates + / −", 12, BLUE)
    p.bul(["Frequency: complete AC cycles per second (hertz)", "Resistance opposes: ALL types of current"], size=12)
    p = P(ax, r[3], "Conductors vs insulators", GREEN, 4)
    p.icons([("🔩", "metal:\nconductor"), ("🥛", "glass:\ninsulator")], 2.8)
    p.bul(["Metals conduct: many FREE ELECTRONS", "Good insulator: GLASS"], size=13)
    p = P(ax, r[4], "Power = rate of energy use", PURPLE, 5)
    p.icons([("💡", "100 W bulb"), ("⚡", "energy/sec")], 2.6)
    p.bul(["Rate electrical energy is used: POWER (watts)"], size=13)

def d_prefix(ax):
    r = grid([(1, [1]), (1.15, [1, 1])])
    p = P(ax, r[0], "Metric prefixes: each step is ×1000", RED, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#ffebee", bot_c="#fafafa")
    pre = [("p", "pico", "÷10¹²", "pF"), ("µ", "micro", "÷1,000,000", "µV, µF"), ("m", "milli", "÷1000", "mA, mW"), ("—", "base unit", "×1", "A, V, W, Hz"), ("k", "kilo", "×1000", "kHz, kV"), ("M", "mega", "×1,000,000", "MHz"), ("G", "giga", "×10⁹", "GHz")]
    bw = (w - 0.4) / 7
    for i, (s_, n, v, ex) in enumerate(pre):
        bx = x + 0.2 + i * bw
        RBOX(ax, bx + 0.08, y + 0.9, bw - 0.16, h - 1.2, "#c8e6c9" if s_ == "—" else "#ffcdd2", RED, 2, 0.2, 4)
        T(ax, bx + bw / 2, y + h - 1.0, s_, 34, RED); T(ax, bx + bw / 2, y + h / 2 + 0.3, n, 17); T(ax, bx + bw / 2, y + h / 2 - 0.6, v, 13, "#333")
        LBOX(ax, bx + 0.3, y + 1.1, bw - 0.6, 0.8, ex, 12, "#fff", "#e57373", "#333")
    ARROW(ax, x + 0.5, y + 0.45, x + w - 0.5, y + 0.45, GREEN, 3, both=True)
    T(ax, x + w / 2, y + 0.45, "  each step = 1000×  ", 13, GREEN, bbox=dict(fc="white", ec="none"))
    p = P(ax, r[1], "Bank conversions", BLUE, 2)
    p.table([["Given", "Equals"], ["1.5 A", "1500 mA"], ["3000 mA", "3 A"], ["500 mW", "0.5 W"], ["1 kilovolt", "1000 volts"], ["1 microvolt", "one-millionth of a volt"]], [1, 1.3], size=15, fill=True)
    p = P(ax, r[2], "Frequency & capacitance", GREEN, 3)
    p.table([["Given", "Equals"], ["1,500,000 Hz", "1500 kHz"], ["3.525 MHz", "3525 kHz"], ["28400 kHz", "28.400 MHz"], ["2425 MHz", "2.425 GHz"], ["1,000,000 pF", "1 µF"]], [1, 1], size=15, fill=True)

def d_db(ax):
    r = grid([(1.1, [1.6, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Decibels: 3 dB = ×2, 10 dB = ×10", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#c5cae9", bot_c="#e8eaf6")
    bw = (w - 0.4) / 3
    for i, (a, b, d, m, ha, hb, c) in enumerate([(5, 10, "+3 dB", "×2", 1.5, 3.0, "#66bb6a"), (12, 3, "−6 dB", "÷4", 3.6, 0.9, "#ef5350"), (20, 200, "+10 dB", "×10", 0.4, 4.0, "#42a5f5")]):
        bx = x + 0.2 + i * bw
        RBOX(ax, bx + 0.1, y + 0.2, bw - 0.2, h - 0.4, "#f5f5f5", "#9fa8da", 1.5, 0.2, 3)
        for gy in np.arange(y + 1.2, y + h - 0.3, 0.5): L(ax, [bx + 0.3, bx + bw - 0.3], [gy, gy], "#e0e0e0", 1, 3.2)
        ax.add_patch(Rectangle((bx + 0.6, y + 1.2), 1.4, ha, fc="#b0bec5", ec="#333", lw=2, zorder=4))
        ax.add_patch(Rectangle((bx + 2.4, y + 1.2), 1.4, hb, fc=c, ec="#333", lw=2, zorder=4))
        T(ax, bx + 1.3, y + 0.75, f"{a} W", 15); T(ax, bx + 3.1, y + 0.75, f"{b} W", 15)
        ARROW(ax, bx + 2.0, y + 1.2 + ha + 0.3, bx + 2.4, y + 1.2 + hb + 0.3, "#333", 2, ms=14)
        T(ax, bx + bw - 1.55, y + h - 1.4, d, 26, RED); T(ax, bx + bw - 1.55, y + h - 2.5, m, 22, "#37474f")
    p = P(ax, r[1], "dB cheat table", RED, 2)
    p.table([["Power change", "dB"], ["×2 (double)", "+3 dB"], ["×4", "+6 dB"], ["×10", "+10 dB"], ["×100", "+20 dB"], ["÷2 (half)", "−3 dB"], ["÷4", "−6 dB"], ["÷10", "−10 dB"]], [1.2, 1], size=15, fill=True)
    for i, (title, f, ans, c, tipx) in enumerate([("5 W → 10 W", "10 ÷ 5 = 2", "→ +3 dB", GREEN, "Double the power = +3 dB"),
                                                  ("12 W → 3 W", "12 ÷ 3 = 4 (less)", "→ −6 dB", RED, "Power DOWN → minus sign"),
                                                  ("20 W → 200 W", "200 ÷ 20 = 10", "→ +10 dB", BLUE, "Ten times the power = +10 dB")]):
        p = P(ax, r[2 + i], title, c, 3 + i)
        p.icons([("📻", "before"), ("➡️", ""), ("📡", "after")], 2.0)
        p.formula(f"{f}\n{ans}", 22, fc=tint(c, 0.85), ec=c, color=c)
        p.bul(["Step 1: divide big ÷ small", "Step 2: look up ×2, ×4 or ×10", tipx], size=14)

def d_lc(ax):
    r = grid([(1.1, [1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Capacitance: energy in an ELECTRIC field", BLUE, 1)
    x, y, w, h = p.scene(4.0, top_c="#bbdefb", bot_c="#e3f2fd")
    cx = x + w * 0.3
    L(ax, [cx - 0.6, cx - 0.6], [y + 0.6, y + h - 0.6], "#333", 10); L(ax, [cx + 0.6, cx + 0.6], [y + 0.6, y + h - 0.6], "#333", 10)
    for yy in np.linspace(y + 0.9, y + h - 0.9, 6): ARROW(ax, cx - 0.45, yy, cx + 0.45, yy, RED, 2, ms=12)
    LBOX(ax, x + w * 0.52, y + h - 1.6, w * 0.45, 1.3, "unit: FARAD", 18, "#fff", BLUE, BLUE)
    LBOX(ax, x + w * 0.52, y + 0.4, w * 0.45, 1.3, "plates + insulator", 14, "#fff", BLUE, "#333")
    p.bul(["Ability to store energy in an electric field: CAPACITANCE"], size=13)
    p = P(ax, r[1], "Inductance: energy in a MAGNETIC field", PURPLE, 2)
    x, y, w, h = p.scene(4.0, top_c="#d1c4e9", bot_c="#ede7f6")
    t = np.linspace(0, 1, 500); cx = x + w * 0.1
    ax.plot(cx + 3.4 * t + 0.4 * np.cos(2 * np.pi * 7 * t), y + h / 2 + 1.0 * np.sin(2 * np.pi * 7 * t), color="#b87333", lw=4, zorder=5)
    for k in [2.6, 3.4]: ax.add_patch(Ellipse((cx + 1.7, y + h / 2), 4.4 + k - 2.6, k, fc="none", ec=BLUE, lw=1.5, ls="--", zorder=4))
    LBOX(ax, x + w * 0.58, y + h - 1.6, w * 0.4, 1.3, "unit: HENRY", 18, "#fff", PURPLE, PURPLE)
    LBOX(ax, x + w * 0.58, y + 0.4, w * 0.4, 1.3, "coil of wire", 14, "#fff", PURPLE, "#333")
    p.bul(["Ability to store energy in a magnetic field: INDUCTANCE"], size=13)
    p = P(ax, r[2], "Impedance", ORANGE, 3)
    p.icons([("〰️", "AC"), ("🚧", "opposition")], 2.4)
    p.bul(["Impedance: opposition to AC current flow", "Unit: OHM"], size=13)
    p = P(ax, r[3], "Abbreviations", GREEN, 4)
    p.table([["Write", "Means"], ["kHz", "kilohertz"], ["MHz", "megahertz"], ["GHz", "gigahertz"]], [1, 1.4], size=15, fill=True)
    p.note("Lower-case k, capital M & G", 13, fc="#e8f5e9", ec=GREEN, color=GREEN)
    p = P(ax, r[4], "Units summary", RED, 5)
    p.table([["Thing", "Unit"], ["Capacitance", "Farad"], ["Inductance", "Henry"], ["Impedance", "Ohm"]], [1.2, 1], size=15, fill=True)

def d_power_calc(ax):
    r = grid([(1, [1, 1.3]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Power triangle", ORANGE, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#ffecb3", bot_c="#fff8e1")
    ohm_triangle(ax, x + w / 2 - 3.0, y + 0.4, 6.0, h - 0.8, "P", "I", "E", RED, BLUE, GREEN, "#fff9c4", ORANGE)
    p = P(ax, r[1], "P = I × E", RED, 2)
    p.formula("P (watts) = I (amps) × E (volts)", 20)
    p.table([["Find", "Formula"], ["Power P", "P = I × E"], ["Current I", "I = P ÷ E"], ["Voltage E", "E = P ÷ I"]], [1, 1.3], size=15, fill=True)
    for i, (title, f, ans, c) in enumerate([("13.8 V × 10 A", "13.8 × 10", "= 138 W", GREEN), ("12 V × 2.5 A", "12 × 2.5", "= 30 W", BLUE), ("120 W at 12 V", "120 ÷ 12", "= 10 A", PURPLE)]):
        p = P(ax, r[2 + i], title, c, 3 + i)
        p.icons([("⚡", "power")] if i < 2 else [("🔌", "current")], 1.8)
        p.formula(f"{f}\n{ans}", 24, fc=tint(c, 0.85), ec=c, color=c)

def d_ohm(ax):
    r = grid([(1, [1, 1.3]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Ohm's Law triangle", BLUE, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#bbdefb", bot_c="#e3f2fd")
    ohm_triangle(ax, x + w / 2 - 3.0, y + 0.4, 6.0, h - 0.8)
    p = P(ax, r[1], "Cover what you want to find", GREEN, 2)
    p.table([["Find", "Formula", "Example"], ["Current I", "I = E / R", "12 V ÷ 4 Ω = 3 A"], ["Voltage E", "E = I × R", "2 A × 5 Ω = 10 V"], ["Resistance R", "R = E / I", "12 V ÷ 3 A = 4 Ω"]], [1, 1, 1.4], size=15, fill=True)
    p.bul(["E: volts • I: amps • R: ohms"], size=15)
    for i, (title, c, rows) in enumerate([("Find R = E ÷ I", PURPLE, [["90 V ÷ 3 A", "30 Ω"], ["12 V ÷ 1.5 A", "8 Ω"], ["12 V ÷ 4 A", "3 Ω"]]),
                                          ("Find I = E ÷ R", RED, [["120 V ÷ 80 Ω", "1.5 A"], ["200 V ÷ 100 Ω", "2 A"], ["240 V ÷ 24 Ω", "10 A"]]),
                                          ("Find E = I × R", GREEN, [["0.5 A × 2 Ω", "1 V"], ["1 A × 10 Ω", "10 V"], ["2 A × 10 Ω", "20 V"]])]):
        p = P(ax, r[2 + i], title, c, 3 + i)
        p.table([["Problem", "Answer"]] + rows, [1.5, 1], size=16, fill=True)

def d_series(ax):
    r = grid([(1.4, [1, 1]), (1, [1])])
    for k, (title, c, txt_) in enumerate([("SERIES: one path → same CURRENT", RED, "Current is the SAME through all components"),
                                           ("PARALLEL: side by side → same VOLTAGE", GREEN, "Voltage is the SAME across all components")]):
        p = P(ax, r[k], title, c, k + 1)
        x, y, w, h = p.scene(p.h - 1.6, top_c=tint(c, 0.75), bot_c=tint(c, 0.9))
        x0, x1, yb, yt = x + 0.8, x + w - 0.8, y + 0.6, y + h - 0.6
        if k == 0:
            L(ax, [x0, x0, x1, x1, x0], [yb, yt, yt, yb, yb], BLUE, 3)
            seg = (x1 - x0) / 3
            for i in range(3):
                a, b = x0 + seg * i + 0.4, x0 + seg * (i + 1) - 0.4
                ax.add_patch(Rectangle((a, yt - 0.3), b - a, 0.6, fc=tint(c, 0.9), ec="none", zorder=4.5)); RES(ax, a, yt, b)
            for i in range(4): ARROW(ax, x0 + 0.5 + i * (x1 - x0) / 4, yb, x0 + 1.3 + i * (x1 - x0) / 4, yb, RED, 3, ms=16)
            T(ax, (x0 + x1) / 2, yb + 0.6, "same current I everywhere", 14, RED)
        else:
            L(ax, [x0, x0, x1, x1, x0], [yb, yt, yt, yb, yb], BLUE, 3)
            for i in range(3):
                xx = x0 + (x1 - x0) * (i + 1) / 4
                L(ax, [xx, xx], [yb, yt], BLUE, 3)
                ax.add_patch(Rectangle((xx - 0.35, yb + 0.6), 0.7, yt - yb - 1.2, fc=tint(c, 0.9), ec="none", zorder=4.5)); RESV(ax, xx, yb + 0.6, yt - 0.6)
                T(ax, xx + 0.75, (yb + yt) / 2, "V", 14, GREEN)
        ax.add_patch(Rectangle((x0 - 0.35, (yb + yt) / 2 - 0.5), 0.7, 1.0, fc="#fff", ec="none", zorder=4.5))
        L(ax, [x0 - 0.3, x0 + 0.3], [(yb + yt) / 2 + 0.2, (yb + yt) / 2 + 0.2], "#000", 4, 5); L(ax, [x0 - 0.15, x0 + 0.15], [(yb + yt) / 2 - 0.2, (yb + yt) / 2 - 0.2], "#000", 4, 5)
        p.note(txt_, 15, fc=tint(c, 0.85), ec=c, color=c)
    r2 = grid([(1, [1, 1, 1])], top=r[2][1] + r[2][3], bottom=r[2][1])
    p = P(ax, r2[0], "Series = train", RED, 3)
    p.icons([("🚃", ""), ("🚃", ""), ("🚃", "")], 1.6)
    p.bul(["One path, cars in a line", "SAME CURRENT through all"], size=14)
    p = P(ax, r2[1], "Parallel = highway lanes", GREEN, 4)
    p.icons([("🚗", ""), ("🚙", ""), ("🚕", "")], 1.6)
    p.bul(["Side-by-side paths", "SAME VOLTAGE across all"], size=14)
    p = P(ax, r2[2], "Exam answers", GOLD, 5)
    p.table([["Circuit", "Same…"], ["Series", "Current ✔"], ["Parallel", "Voltage ✔"]], [1, 1], size=15, fill=True)

SLIDES = [
    dict(title="Voltage, current, power & units", ids=["T5A03", "T5A05", "T5A10", "T5A01", "T5A02", "T5A06", "T5A04", "T5A09", "T5A11", "T5A07", "T5A08"], draw=d_basics,
         tip="Voltage pushes, current flows, resistance resists. Amps, volts, watts, hertz. Metals conduct, glass insulates."),
    dict(title="Metric prefix conversions", ids=["T5B01", "T5B06", "T5B05", "T5B03", "T5B04", "T5B02", "T5B07", "T5B12", "T5B13", "T5B08"], draw=d_prefix,
         tip="kilo = 1000, mega = 1,000,000, milli = 1/1000, micro = 1/1,000,000. Each step is ×1000."),
    dict(title="Decibels", ids=["T5B09", "T5B10", "T5B11"], draw=d_db,
         tip="Double = +3 dB. Four times = +6 dB. Ten times = +10 dB. Power going down? Add a minus sign."),
    dict(title="Capacitance, inductance & impedance", ids=["T5C01", "T5C02", "T5C03", "T5C04", "T5C05", "T5C12", "T5C06", "T5C07"], draw=d_lc,
         tip="Capacitor = electric field, farads. Inductor = magnetic field, henrys. Impedance = ohms."),
    dict(title="Calculating power: P = I × E", ids=["T5C08", "T5C09", "T5C10", "T5C11"], draw=d_power_calc,
         tip="Power (watts) = current (amps) × voltage (volts). Cover the letter you want in the triangle."),
    dict(title="Ohm's Law: E = I × R", ids=["T5D01", "T5D02", "T5D03", "T5D04", "T5D05", "T5D06", "T5D07", "T5D08", "T5D09", "T5D10", "T5D11", "T5D12"], draw=d_ohm,
         tip="R = E ÷ I, I = E ÷ R, E = I × R. Cover the letter you want in the triangle."),
    dict(title="Series & parallel circuits", ids=["T5D13", "T5D14"], draw=d_series,
         tip="Series = same Current. Parallel = same Voltage."),
]

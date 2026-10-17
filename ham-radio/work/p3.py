from core2 import *

def d_wave(ax):
    r = grid([(1.1, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "A radio wave = electric + magnetic field", PURPLE, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#d1c4e9", bot_c="#ede7f6")
    xs = np.linspace(x + 0.5, x + w - 1.2, 500); cy = y + h / 2
    Ev = 1.6 * np.sin(2 * np.pi * (xs - xs[0]) / ((w - 1.7) / 2.5))
    for xi in np.linspace(xs[0], xs[-1], 30):
        e = 1.6 * np.sin(2 * np.pi * (xi - xs[0]) / ((w - 1.7) / 2.5))
        L(ax, [xi, xi], [cy, cy + e], "#ef9a9a", 1.5, 4); L(ax, [xi, xi + 0.4 * e], [cy, cy - 0.4 * e], "#90caf9", 1.5, 4)
    ax.plot(xs, cy + Ev, color=RED, lw=4, zorder=5); ax.plot(xs, cy - 0.4 * Ev, color=BLUE, lw=4, zorder=5, ls="--")
    ARROW(ax, x + 0.5, cy, x + w - 0.4, cy, "#333", 2.5)
    LBOX(ax, x + 0.3, y + h - 1.1, 5.0, 0.85, "Electric field (E)", 14, "#ffebee", RED, RED)
    LBOX(ax, x + 0.3, y + 0.25, 5.4, 0.85, "Magnetic field (at right angles)", 14, "#e3f2fd", BLUE, BLUE)
    LBOX(ax, x + w - 5.6, y + h - 1.1, 5.3, 0.85, "E and M at 90° (right angles)", 14, "#fff8e1", GOLD, PURPLE)
    LBOX(ax, x + w - 5.6, y + 0.25, 5.3, 0.85, "speed of light: 300,000,000 m/s", 13, "#e8f5e9", GREEN, GREEN)
    T(ax, x + w - 0.8, cy + 0.5, "travel", 12)
    p = P(ax, r[1], "Key facts", RED, 2)
    p.table([["Question", "Answer"], ["Two components", "Electric + magnetic fields"], ["How are they related?", "At right angles"],
             ["Polarization is set by", "Orientation of ELECTRIC field"], ["Speed in free space", "Speed of light"], ["Approx. speed", "300,000,000 m/s"]], [1.2, 1.3], size=13, hl={3})
    p = P(ax, r[2], "Same speed for all!", GREEN, 3)
    p.icons([("🐢", "HF"), ("🐇", "VHF"), ("🚀", "UHF")], 2.2)
    p.formula("All radio frequencies travel\nat the same velocity", 14, fc="#e8f5e9", ec=GREEN, color=GREEN)
    p = P(ax, r[3], "λ = 300 ÷ f (MHz)", ORANGE, 4)
    p.formula("λ (meters) = 300 ÷ f (MHz)", 19)
    p.table([["Freq", "Wavelength", "Band"], ["50 MHz", "6 m", "6 m"], ["146 MHz", "≈2 m", "2 m"], ["440 MHz", "≈0.7 m", "70 cm"], ["28 MHz", "≈10.7 m", "10 m"]], [1, 1, 1], size=13, fill=True)
    p = P(ax, r[4], "Higher f → shorter λ", BLUE, 5)
    x, y, w, h = p.scene(3.4, top_c="#e3f2fd", bot_c="#fafafa")
    WAVE(ax, x + 0.3, x + w - 0.3, y + h * 0.72, 0.5, 2, BLUE, lw=3.5); T(ax, x + w / 2, y + h - 0.25, "low f: LONG waves", 12, BLUE)
    WAVE(ax, x + 0.3, x + w - 0.3, y + h * 0.28, 0.5, 9, RED, lw=3); T(ax, x + w / 2, y + 0.2, "high f: short waves", 12, RED)
    p.bul(["Bands are also named by approximate wavelength in meters"], size=13)

def d_bands(ax):
    r = grid([(1, [1]), (1, [1, 1])])
    p = P(ax, r[0], "The radio spectrum: each range is 10× the last", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#eceff1", bot_c="#fafafa")
    for i, (n, rg, c, ex) in enumerate([("HF", "3 – 30 MHz", "#ffcc80", "10 m band (28 MHz)"), ("VHF", "30 – 300 MHz", "#a5d6a7", "6 m (50) • 2 m (146)"), ("UHF", "300 – 3000 MHz", "#90caf9", "70 cm (440 MHz)")]):
        bx = x + 0.2 + i * (w - 0.4) / 3
        RBOX(ax, bx + 0.1, y + 0.2, (w - 0.4) / 3 - 0.2, h - 0.4, c, "#333", 2.5, 0.25, 3)
        cx = bx + (w - 0.4) / 6
        T(ax, cx, y + h - 1.2, n, 40); T(ax, cx, y + h / 2 - 0.1, rg, 22); T(ax, cx, y + 0.9, ex, 15, "#333", False)
    p = P(ax, r[1], "Memory trick", RED, 2)
    p.formula("3 → 30 → 300 → 3000 MHz", 24)
    p.bul(["H: High frequency (3–30 MHz)", "V: VERY high frequency (30–300 MHz)", "U: ULTRA high frequency (300–3000 MHz)"], size=15)
    p.icons([("📻", "HF: 10 m"), ("🚗", "VHF: 2 m"), ("📶", "UHF: 70 cm")], 2.0)
    p = P(ax, r[1 + 1], "Watch out for kHz traps!", ORANGE, 3)
    p.table([["Answer choice", "Correct?"], ["30 MHz to 300 MHz (VHF)", "✔"], ["30 kHz to 300 kHz", "✘ wrong unit"], ["300 to 3000 MHz (UHF)", "✔"], ["300 to 3000 kHz", "✘ wrong unit"]], [2, 1], size=15, fill=True)
    p.bul(["Read the unit: MHz, not kHz!"], size=14)

def d_multipath(ax):
    r = grid([(1.1, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Multipath: signals arrive by several paths", BLUE, 1)
    x, y, w, h = p.scene(p.h - 0.1, "sky")
    TOWER(ax, x + 1.2, y + 0.45, 3.2)
    for bx, bh in [(x + w * 0.42, 3.4), (x + w * 0.6, 2.4)]:
        ax.add_patch(Rectangle((bx, y + 0.45), 1.5, bh, fc="#90a4ae", ec="#455a64", lw=2, zorder=4))
        for wy in np.arange(y + 0.8, y + 0.45 + bh - 0.3, 0.55):
            ax.add_patch(Rectangle((bx + 0.25, wy), 0.35, 0.3, fc="#fff59d", zorder=4.5)); ax.add_patch(Rectangle((bx + 0.9, wy), 0.35, 0.3, fc="#fff59d", zorder=4.5))
    E(ax, "🚗", x + w - 1.3, y + 1.0, 1.1)
    tx, ty = x + 1.3, y + 3.6; rx, ry = x + w - 1.6, y + 1.3
    ARROW(ax, tx, ty, rx, ry, BLUE, 3)
    ARROW(ax, tx, ty, x + w * 0.42, y + 3.4, ORANGE, 3, head=False); ARROW(ax, x + w * 0.42, y + 3.4, rx, ry + 0.2, ORANGE, 3)
    ARROW(ax, tx, ty, x + w * 0.6, y + 2.8, PURPLE, 3, head=False); ARROW(ax, x + w * 0.6, y + 2.8, rx, ry - 0.1, PURPLE, 3)
    LBOX(ax, x + w * 0.25, y + h - 1.2, w * 0.5, 0.9, "paths ADD or CANCEL at the receiver", 13, "#fff8e1", GOLD, RED)
    p = P(ax, r[1], "Effects of multipath", RED, 2)
    p.table([["Situation", "Result"], ["Move VHF antenna a few feet", "Big signal change"], ["Mobile station moving", "\"Picket fencing\" flutter"],
             ["Ionosphere paths", "Irregular fading"], ["Data transmissions", "Error rates INCREASE"]], [1.3, 1.1], size=13)
    p = P(ax, r[2], "Picket fencing", ORANGE, 3)
    x, y, w, h = p.scene(2.6)
    for i in range(14):
        ax.add_patch(Rectangle((x + 0.3 + i * (w - 0.6) / 14, y + 0.3), (w - 0.6) / 28, h - 0.6, fc="#a1887f", zorder=4))
    E(ax, "🚙", x + w / 2, y + h / 2, 1.2)
    p.bul(["Rapid flutter on MOBILE signals due to multipath"], size=13)
    p = P(ax, r[3], "Blocked? Bounce it!", TEAL, 4)
    x, y, w, h = p.scene(2.6, "sky")
    ax.add_patch(Rectangle((x + w / 2 - 0.5, y + 0.45), 1.0, 1.7, fc="#78909c", zorder=4))
    ax.add_patch(Rectangle((x + w / 2 - 1.5, y + h - 0.6), 3.0, 0.4, fc="#90a4ae", zorder=4))
    HT(ax, x + 0.8, y + 0.45, 0.5); TOWER(ax, x + w - 0.8, y + 0.45, 1.5)
    ARROW(ax, x + 1.1, y + 1.6, x + w / 2, y + h - 0.65, TEAL, 2.5, head=False); ARROW(ax, x + w / 2, y + h - 0.65, x + w - 0.9, y + 1.8, TEAL, 2.5)
    p.bul(["With a directional antenna: find a path that REFLECTS signals to the repeater"], size=13)
    p = P(ax, r[4], "Polarization match", PURPLE, 5)
    x, y, w, h = p.scene(2.6, top_c="#e1bee7", bot_c="#f3e5f5")
    L(ax, [x + 0.4, x + 2.0], [y + 1.8, y + 1.8], "#333", 7); L(ax, [x + 3.0, x + 4.6], [y + 1.8, y + 1.8], "#333", 7); T(ax, x + 2.5, y + 1.25, "✔ strong", 12, GREEN, family="DejaVu Sans")
    L(ax, [x + w - 3.6, x + w - 2.4], [y + 1.0, y + 1.0], "#333", 7); L(ax, [x + w - 0.8, x + w - 0.8], [y + 0.4, y + 1.8], "#333", 7); T(ax, x + w - 1.6, y + 2.2, "✘ weak", 12, RED, family="DejaVu Sans")
    p.bul(["Long-distance VHF/UHF CW/SSB: HORIZONTAL", "Cross-polarized: signal strength reduced", "Ionosphere (elliptical): either polarization works"], size=13)

def d_weather(ax):
    r = grid([(1, [1.4, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "What absorbs or blocks signals?", GREEN, 1)
    x, y, w, h = p.scene(p.h - 0.1, "sky", top_c="#90a4ae", bot_c="#eceff1")
    TOWER(ax, x + 1.0, y + 0.45, 3.0)
    E(ax, "🌧️", x + w * 0.35, y + h - 1.0, 1.6)
    E(ax, "🌲", x + w * 0.62, y + 1.6, 2.4); E(ax, "🌳", x + w * 0.75, y + 1.5, 2.2)
    WAVE(ax, x + 1.5, x + w * 0.55, y + 2.8, 0.35, 10, RED, lw=3)
    WAVE(ax, x + w * 0.55, x + w - 0.4, y + 2.8, 0.12, 6, RED, lw=2, ls="--")
    LBOX(ax, x + w * 0.5, y + h - 1.3, w * 0.48, 1.0, "microwave/UHF gets weaker", 13, "#ffebee", RED, RED)
    p = P(ax, r[1], "Weather & vegetation", BLUE, 2)
    p.table([["Thing", "Effect"], ["Leaves on UHF/microwave", "ABSORB → poor weak-signal reception"], ["Rain at microwave", "PRECIPITATION can cut range"], ["Fog/rain on 10 m & 6 m", "LITTLE effect"]], [1.1, 1.5], size=13, fill=True)
    p = P(ax, r[2], "Radio horizon", ORANGE, 3)
    x, y, w, h = p.scene(3.0, "sky")
    ax.add_patch(Circle((x + w / 2, y - 14.5), 15.0, fc="#81c784", ec="#2e7d32", lw=2, zorder=3))
    TOWER(ax, x + 0.9, y + 0.4, 1.8)
    L(ax, [x + 1.0, x + w - 0.3], [y + 2.3, y + 0.9], "#555", 1.5, 5, "--")
    xs = np.linspace(x + 1.0, x + w - 0.3, 100); ax.plot(xs, y + 2.3 - (xs - x - 1) * 0.25 + 0.03 * (xs - x - 1) ** 2, color=RED, lw=3, zorder=5)
    p.bul(["Radio horizon farther than visual: atmosphere REFRACTS (bends) radio waves slightly"], size=12)
    p = P(ax, r[3], "Knife-edge diffraction", PURPLE, 4)
    x, y, w, h = p.scene(3.0, "sky")
    ax.add_patch(Polygon([(x + w / 2 - 1.2, y + 0.45), (x + w / 2, y + 2.4), (x + w / 2 + 1.2, y + 0.45)], fc="#8d6e63", ec="#5d4037", lw=2, zorder=4))
    ARROW(ax, x + 0.4, y + 2.0, x + w / 2, y + 2.45, PURPLE, 3, head=False); ARROW(ax, x + w / 2, y + 2.45, x + w - 0.4, y + 0.8, PURPLE, 3)
    p.bul(["Signals bend over a sharp edge to reach beyond obstructions"], size=13)
    p = P(ax, r[4], "UHF & the ionosphere", INDIGO, 5)
    p.icons([("📶", "UHF simplex"), ("🚫", "no sky bounce")], 2.6)
    p.bul(["UHF rarely heard past horizon: NOT propagated by the ionosphere"], size=13)

def d_iono(ax):
    r = grid([(1.15, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "The ionosphere bounces HF back to Earth", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, "night", top_c="#0d1b3e", bot_c="#3f51b5")
    ax.add_patch(Rectangle((x, y + h - 1.5), w, 0.8, fc="#ffeb3b55", zorder=3)); T(ax, x + 1.6, y + h - 1.1, "F region", 13, "#fff59d")
    ax.add_patch(Rectangle((x, y + h - 2.6), w, 0.45, fc="#ff980055", zorder=3)); T(ax, x + 1.4, y + h - 2.38, "E region", 12, "#ffcc80")
    GROUND(ax, x, y, w, 0.5, z=3)
    E(ax, "☀️", x + w - 1.0, y + h - 0.7, 1.0)
    TOWER(ax, x + 1.0, y + 0.5, 1.6); TOWER(ax, x + w - 1.0, y + 0.5, 1.6)
    L(ax, [x + 1.1, x + w / 2, x + w - 1.1], [y + 2.1, y + h - 1.15, y + 2.1], "#ff5252", 4, 5)
    ARROW(ax, x + 1.1, y + 2.2, x + w * 0.38, y + h - 0.1, "#80d8ff", 2.5, ls="--")
    T(ax, x + w * 0.27, y + h - 0.5, "UHF passes through", 12, "#80d8ff")
    T(ax, x + w / 2, y + 1.3, "HF skip = long distance", 14, "white")
    p = P(ax, r[1], "HF vs VHF/UHF", RED, 2)
    p.bul(["Ionosphere: region of the atmosphere that can REFLECT HF waves",
           "HF: long-distance ionospheric propagation far more common than on VHF+"], size=13)
    p.note("Sunspot peak → 6 m & 10 m open via F region", 13, fc="#fff8e1", ec=GOLD, color="#5d4037")
    p = P(ax, r[2], "Best time for 10 m", ORANGE, 3)
    x, y, w, h = p.scene(2.4, top_c="#ffe082", bot_c="#fff8e1")
    E(ax, "🌅", x + 1.0, y + h / 2, 1.4); ARROW(ax, x + 1.9, y + h / 2, x + w - 1.9, y + h / 2, ORANGE, 3); E(ax, "🌇", x + w - 1.0, y + h / 2, 1.4)
    p.bul(["From DAWN to shortly after SUNSET during HIGH sunspot activity"], size=13)
    p = P(ax, r[3], "Sunspots help", GOLD, 4)
    p.icons([("☀️", "more sunspots"), ("📈", "stronger F"), ("🌎", "6 & 10 m DX")], 2.6)
    p.bul(["Sunspot peak: 6 and 10 meters via the F region"], size=13)
    p = P(ax, r[4], "Irregular fading", PURPLE, 5)
    x, y, w, h = p.scene(2.6)
    xs = np.linspace(x + 0.3, x + w - 0.3, 400)
    ax.plot(xs, y + h / 2 + 0.8 * np.sin((xs - x) * 8) * (0.5 + 0.5 * np.sin((xs - x) * 1.3)), color=PURPLE, lw=2.5, zorder=5)
    p.bul(["Ionosphere fading: random combining of signals via different paths"], size=13)

def d_vhfdx(ax):
    r = grid([(1.1, [1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "VHF/UHF beyond the horizon", PURPLE, 1)
    x, y, w, h = p.scene(p.h - 0.1, "night", top_c="#0d1b3e", bot_c="#5c6bc0")
    GROUND(ax, x, y, w, 0.5, z=3)
    items = [(0.12, "☄️", "Meteor scatter", "best on 6 m"), (0.37, "🌌", "Aurora", "raspy, distorted"), (0.62, "⚡", "Sporadic E", "strong 10/6/2 m"), (0.87, "🌡️", "Tropo ducting", "≈300 miles")]
    for fx, e, t1, t2 in items:
        cx = x + w * fx
        E(ax, e, cx, y + h - 1.2, 1.3)
        LBOX(ax, cx - 2.6, y + 0.8, 5.2, 1.5, f"{t1}\n{t2}", 15, "#ffffffdd", "#fff", INDIGO)
    ax.add_patch(Rectangle((x + w * 0.75, y + 2.7), w * 0.24, 0.6, fc="#ffffff44", ec="#fff", ls="--", lw=1.5, zorder=3))
    p = P(ax, r[1], "Meteor & aurora", BLUE, 2)
    p.table([["Mode", "Key fact"], ["Meteor scatter", "Best band: 6 METERS"], ["Auroral backscatter", "Distorted, RASPY sound"]], [1, 1.3], size=14, fill=True)
    p.icons([("☄️", "meteor"), ("🌌", "aurora")], 2.0)
    p = P(ax, r[2], "Sporadic E", ORANGE, 3)
    p.icons([("⚡", "E layer patch"), ("📻", "10/6/2 m")], 2.4)
    p.bul(["Occasional STRONG signals on 10, 6 and 2 m from beyond the radio horizon"], size=13)
    p = P(ax, r[3], "Tropospheric ducting", TEAL, 4)
    x, y, w, h = p.scene(2.6, "sky")
    ax.add_patch(Rectangle((x, y + 1.3), w, 0.8, fc="#ffffff88", ec=TEAL, ls="--", lw=2, zorder=3))
    WAVE(ax, x + 0.3, x + w - 0.3, y + 1.7, 0.3, 6, RED, lw=2.5)
    p.bul(["Cause: TEMPERATURE INVERSIONS", "Range: ≈300 miles, regularly"], size=13)

SLIDES = [
    dict(title="Radio waves, speed & wavelength", ids=["T3B03", "T3B01", "T3B02", "T3B04", "T3B11", "T3B12", "T3B05", "T3B06", "T3B07"], draw=d_wave,
         tip="Electric + magnetic fields at right angles. Speed of light. Wavelength (m) = 300 ÷ MHz."),
    dict(title="HF, VHF & UHF frequency ranges", ids=["T3B10", "T3B08", "T3B09"], draw=d_bands,
         tip="HF 3–30 MHz, VHF 30–300 MHz, UHF 300–3000 MHz. Watch out for kHz trap answers!"),
    dict(title="Multipath, picket fencing & polarization", ids=["T3A01", "T3A06", "T3A08", "T3A10", "T3A05", "T3A03", "T3A04", "T3A09"], draw=d_multipath,
         tip="Bounced signals add up or cancel. Match polarization; long-distance VHF/UHF SSB uses horizontal."),
    dict(title="Weather, trees, horizon & diffraction", ids=["T3A02", "T3A07", "T3A12", "T3C11", "T3C05", "T3C01"], draw=d_weather,
         tip="Leaves and rain soak up microwaves. Air bends radio waves past the visible horizon."),
    dict(title="The ionosphere & HF propagation", ids=["T3A11", "T3C02", "T3C09", "T3C10"], draw=d_iono,
         tip="The ionosphere reflects HF. More sunspots = better 10 m and 6 m, from dawn until just after sunset."),
    dict(title="VHF DX: meteors, aurora, sporadic E, ducting", ids=["T3C07", "T3C03", "T3C04", "T3C06", "T3C08"], draw=d_vhfdx,
         tip="Meteor = 6 m. Aurora = raspy. Sporadic E = strong 10/6/2 m. Ducting = temperature inversion, ~300 mi."),
]

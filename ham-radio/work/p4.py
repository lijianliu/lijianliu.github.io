from core2 import *

def d_power(ax):
    r = grid([(1.1, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Powering a 50-watt mobile radio", ORANGE, 1)
    x, y, w, h = p.scene(p.h - 0.1)
    RBOX(ax, x + 0.4, y + 1.0, 4.4, 3.2, "#455a64", "#000", 2, 0.2, 4)
    T(ax, x + 2.6, y + 3.7, "POWER SUPPLY", 13, "white"); T(ax, x + 2.6, y + 2.4, "13.8 V\n12 A", 24, "#b2ff59")
    L(ax, [x + 4.8, x + 8.6], [y + 2.9, y + 2.9], RED, 11, 5); L(ax, [x + 4.8, x + 8.6], [y + 2.2, y + 2.2], "#111", 11, 5)
    LBOX(ax, x + 4.9, y + 3.5, 3.6, 1.0, "short, HEAVY wires", 13, "#fff", RED, RED)
    LBOX(ax, x + 4.9, y + 0.6, 3.6, 1.2, "less voltage drop when transmitting", 12, "#fff", ORANGE, "#333")
    RADIO(ax, x + 8.8, y + 1.6, 4.0, 2.0, "50 W")
    LBOX(ax, x + 9.0, y + h - 1.2, 3.6, 0.9, "50 W FM rig", 13, "#fff", ORANGE, ORANGE)
    p = P(ax, r[1], "In a vehicle", BLUE, 2)
    p.icons([("🚗", "car"), ("🔋", "12 V battery"), ("⏚", "chassis ground")], 2.6)
    p.bul(["Negative return: connect at the 12-volt battery CHASSIS GROUND", "Not to the antenna mount or fuse block"], size=13)
    p = P(ax, r[2], "Battery run time", GREEN, 3)
    p.formula("hours = Ah ÷ amps", 20)
    p.table([["Battery", "Draw", "Run time"], ["10 Ah", "2 A", "5 h"], ["7 Ah", "1 A", "7 h"]], [1, 1, 1], size=14, fill=True)
    p.bul(["Divide ampere-hour rating by average current draw"], size=13)
    p = P(ax, r[3], "SWR / power meter", RED, 4)
    x, y, w, h = p.scene(2.8)
    RADIO(ax, x + 0.2, y + 0.6, 2.4, 1.3, "TX")
    L(ax, [x + 2.6, x + 3.6], [y + 1.25, y + 1.25], "#111", 5)
    RBOX(ax, x + 3.6, y + 0.4, 2.4, 1.8, "#fff3e0", ORANGE, 2, 0.15, 4)
    ax.add_patch(Wedge((x + 4.8, y + 0.8), 1.0, 30, 150, fc="#fff", ec="#333", lw=1.5, zorder=5)); L(ax, [x + 4.8, x + 5.2], [y + 0.8, y + 1.6], RED, 2.5, 6)
    L(ax, [x + 6.0, x + w - 0.6], [y + 1.25, y + 1.25], "#111", 5); L(ax, [x + w - 0.6, x + w - 0.6], [y + 1.25, y + 2.5], "#424242", 4)
    p.bul(["Install: IN THE FEED LINE between transmitter and antenna", "Choosing one: check frequency & power level"], size=12)
    p = P(ax, r[4], "Bonding at RF", TEAL, 5)
    x, y, w, h = p.scene(2.6)
    ax.add_patch(Rectangle((x + 0.5, y + 1.1), w - 1.0, 0.4, fc="#d88c4a", ec="#8d4e1f", lw=2, zorder=5))
    T(ax, x + w / 2, y + 2.0, "FLAT copper strap ✔", 14, GREEN, family="DejaVu Sans")
    L(ax, [x + 0.5, x + w - 0.5], [y + 0.55, y + 0.55], "#b87333", 3, 5); T(ax, x + w / 2, y + 0.25, "round wire ✘", 11, RED, family="DejaVu Sans")
    p.bul(["Preferred for RF bonding: flat copper strap"], size=13)

def d_digital(ax):
    r = grid([(1.1, [1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Computer + radio for digital modes (FT8)", PURPLE, 1)
    x, y, w, h = p.scene(p.h - 0.1)
    E(ax, "💻", x + 2.4, y + h / 2 + 0.3, 3.0); T(ax, x + 2.4, y + 0.5, "Computer running FT8", 13)
    RADIO(ax, x + w - 5.2, y + 1.3, 4.6, 2.3, "FT8 14.074")
    for i, (yy, c, lab, rev) in enumerate([(y + h - 1.0, GREEN, "RECEIVE audio: radio speaker → computer 'line in'", True),
                                           (y + h / 2, BLUE, "TRANSMIT audio: computer audio out → radio audio in", False),
                                           (y + 1.0, RED, "TRANSMITTER KEYING (PTT)", False)]):
        if rev: ARROW(ax, x + w - 5.4, yy, x + 4.4, yy, c, 4)
        else: ARROW(ax, x + 4.4, yy, x + w - 5.4, yy, c, 4)
        LBOX(ax, x + 5.0, yy + 0.15, w - 11.0, 0.8, lab, 13, "#fff", c, c)
    p = P(ax, r[1], "The 3 signals", BLUE, 2)
    p.table([["Signal", "Direction"], ["Receive audio", "radio → PC"], ["Transmit audio", "PC → radio"], ["Keying (PTT)", "PC → radio"]], [1, 1], size=14, fill=True)
    p.bul(["FT8 rig audio in/out: to the computer's audio out/in"], size=13)
    p = P(ax, r[2], "Digital hotspot", TEAL, 3)
    p.icons([("📻", "your HT"), ("📶", "hotspot"), ("🌐", "network")], 2.6)
    p.bul(["Hotspot: links nearby radios to a digital voice or data network"], size=13)
    p = P(ax, r[3], "Electronic keyer", ORANGE, 4)
    p.icons([("🎛️", "paddle"), ("📟", "· − · −")], 2.6)
    p.bul(["Keyer: device that ASSISTS manual sending of Morse code"], size=13)

def d_tuning(ax):
    r = grid([(1.1, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Transceiver front panel", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1)
    RBOX(ax, x + 0.3, y + 0.3, w - 0.6, h - 0.6, "#37474f", "#000", 2.5, 0.3, 4)
    RBOX(ax, x + 0.8, y + h - 2.4, 7.0, 1.7, "#b2ff59", "#000", 2, 0.1, 5)
    T(ax, x + 4.3, y + h - 1.55, "146.520", 34, "#1b5e20", family="monospace")
    ax.add_patch(Circle((x + w - 3.0, y + h / 2), 1.7, fc="#cfd8dc", ec="#000", lw=3, zorder=5)); ax.add_patch(Circle((x + w - 3.0, y + h / 2), 0.3, fc="#607d8b", zorder=6))
    T(ax, x + w - 3.0, y + 0.75, "VFO knob", 13, "white")
    for i in range(3):
        for j in range(4):
            RBOX(ax, x + 0.9 + j * 1.5, y + 0.6 + i * 0.75, 1.2, 0.55, "#90a4ae", "#000", 1, 0.08, 5)
    for i, lab in enumerate(["SCAN", "RIT", "SQL"]):
        LBOX(ax, x + 7.4 + i * 1.6, y + 0.6, 1.4, 0.7, lab, 12, "#ffcc80", "#000", "#000", z=6)
    T(ax, x + 3.9, y + h - 2.85, "Keypad or VFO → set frequency", 13, "white")
    p = P(ax, r[1], "What each control does", BLUE, 2)
    p.table([["Control", "Job"], ["Keypad / VFO", "Enter operating frequency"], ["SCAN", "Tunes a range checking for activity"], ["RIT / Clarifier", "Fix SSB voice too high/low"], ["Squelch", "Mute when no signal"]], [1, 1.6], size=13, fill=True)
    p = P(ax, r[2], "FM off frequency", RED, 3)
    x, y, w, h = p.scene(2.6)
    xs = np.linspace(x + 0.3, x + w - 0.3, 300)
    ax.plot(xs, y + h / 2 + 0.7 * np.sin((xs - x) * 6) + 0.25 * np.sin((xs - x) * 23), color=RED, lw=2.5, zorder=5)
    p.bul(["FM received slightly off frequency: audio becomes DISTORTED"], size=13)
    p = P(ax, r[3], "RIT / Clarifier", ORANGE, 4)
    p.icons([("🐭", "too high"), ("🎛️", "turn RIT"), ("🐻", "too low")], 2.6)
    p.bul(["SSB voice pitch too high or low: adjust the RIT (Clarifier)"], size=13)
    p = P(ax, r[4], "Scanning", GREEN, 5)
    x, y, w, h = p.scene(2.6)
    for i, f in enumerate(["146.52", "146.94", "147.12", "147.33"]):
        LBOX(ax, x + 0.2 + i * (w - 0.4) / 4, y + 0.8, (w - 0.4) / 4 - 0.1, 1.0, f, 12, "#b2ff59" if i == 2 else "#fff", GREEN, "#1b5e20")
    ARROW(ax, x + 0.4, y + 0.45, x + w - 0.4, y + 0.45, GREEN, 2.5)
    p.bul(["Scan: tunes through frequencies to check for activity"], size=13)

def d_rx(ax):
    r = grid([(1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Squelch for weak FM", BLUE, 1)
    x, y, w, h = p.scene(2.8)
    ax.add_patch(Wedge((x + w / 2, y + 0.4), 2.0, 0, 180, fc="#eceff1", ec="#333", lw=2, zorder=4))
    L(ax, [x + w / 2, x + w / 2 - 1.5], [y + 0.4, y + 1.3], RED, 4, 5); T(ax, x + w / 2 - 2.6, y + 0.6, "OPEN", 12, RED)
    p.bul(["Weak FM signal: set squelch so audio is ON ALL THE TIME (open)"], size=13)
    p = P(ax, r[1], "Filter bandwidth", GREEN, 2)
    x, y, w, h = p.scene(3.2, top_c="#c8e6c9", bot_c="#e8f5e9")
    xs = np.linspace(x + 0.3, x + w - 0.3, 300); cx = x + w / 2
    rng = np.random.default_rng(1); ax.plot(xs, y + 0.3 + 0.3 * rng.random(300), color="#9e9e9e", lw=1, zorder=4.2)
    ax.plot(xs, y + 0.3 + 2.0 * np.exp(-((xs - cx) / 0.9) ** 2), color=BLUE, lw=3, zorder=5)
    T(ax, cx, y + h - 0.3, "filter passes only the signal", 12, GREEN); T(ax, x + 1.2, y + 1.0, "noise", 11, "#616161"); T(ax, x + w - 1.2, y + 1.0, "noise", 11, "#616161")
    ax.add_patch(Rectangle((cx - 1.1, y + 0.3), 2.2, 2.2, fc="#a5d6a766", ec=GREEN, lw=2.5, zorder=4))
    T(ax, cx, y + 2.75, "filter passes only this", 12, GREEN)
    p.bul(["Choice of filters: cut noise/interference by matching bandwidth to the mode"], size=13)
    p = P(ax, r[2], "Best SSB filter", TEAL, 3)
    p.table([["Filter", "Use"], ["500 Hz", "CW"], ["2400 Hz", "SSB ✔"], ["15 kHz", "FM"]], [1, 1], size=15, hl={2}, fill=True)
    p = P(ax, r[3], "Mic gain on SSB", RED, 4)
    x, y, w, h = p.scene(2.8)
    E(ax, "🎤", x + 1.2, y + h / 2, 1.6)
    xs = np.linspace(x + 2.4, x + w - 0.3, 300)
    ax.plot(xs, np.clip(y + h / 2 + 1.5 * np.sin((xs - x) * 6), y + h / 2 - 0.8, y + h / 2 + 0.8), color=RED, lw=2.5, zorder=5)
    p.bul(["Excessive mic gain on SSB: DISTORTED transmitted audio"], size=13)
    p = P(ax, r[4], "D-STAR setup", PURPLE, 5)
    x, y, w, h = p.scene(2.8)
    RADIO(ax, x + 0.4, y + 0.5, 3.6, 1.8, "KF1XXX")
    E(ax, "🪪", x + w - 1.2, y + h / 2, 1.5)
    p.bul(["Must program before transmitting: YOUR CALL SIGN"], size=13)
    p = P(ax, r[5], "Over-deviation (FM)", ORANGE, 6)
    p.icons([("🗣️", "too close"), ("↔️", "move back"), ("🎤", "mic")], 2.6)
    p.bul(["Told you're over-deviating: talk FARTHER from the microphone"], size=13)

SLIDES = [
    dict(title="Station power, meters & bonding", ids=["T4A01", "T4A03", "T4A11", "T4A09", "T4A05", "T4A02", "T4A08"], draw=d_power,
         tip="A 50 W radio needs about 13.8 V at 12 A. The meter goes in the feed line. Bond with flat copper strap."),
    dict(title="Digital modes: computers, hotspots & keyers", ids=["T4A04", "T4A06", "T4A07", "T4A10", "T4A12"], draw=d_digital,
         tip="Three connections: receive audio, transmit audio and PTT keying."),
    dict(title="Front-panel controls: VFO, scan & RIT", ids=["T4B02", "T4B05", "T4B06", "T4B04"], draw=d_tuning,
         tip="Keypad or VFO sets the frequency. RIT fixes SSB voices that sound too high or too low."),
    dict(title="Squelch, filters, mic gain & D-STAR", ids=["T4B03", "T4B08", "T4B10", "T4B01", "T4B11", "T7B01"], draw=d_rx,
         tip="2400 Hz filter for SSB. Too much mic gain = distortion. Over-deviating? Back away from the mic."),
]

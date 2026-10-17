from core2 import *

def d_modes(ax):
    r = grid([(1.1, [1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Modulation types & bandwidth (narrow → wide)", ORANGE, 1)
    x, y, w, h = p.scene(p.h - 0.1, top_c="#ffe0b2", bot_c="#fff3e0")
    modes = [("CW", "≈150 Hz", "Morse: on / off", lambda t: (np.sin(2 * np.pi * 3 * t) > 0).astype(float), "#90caf9", 0.10),
             ("SSB", "≈3 kHz", "a form of AM; weak-signal VHF/UHF", lambda t: 0.4 + 0.6 * np.abs(np.sin(5 * np.pi * t)), "#ce93d8", 0.25),
             ("FM / PM", "10–15 kHz", "repeaters & packet", None, "#a5d6a7", 0.45),
             ("AM fast-scan TV", "≈6 MHz", "NTSC analog TV", lambda t: 0.5 + 0.5 * np.sin(2 * np.pi * 2 * t), "#ffcc80", 0.95)]
    cw_ = (w - 0.4) / 4
    for i, (n, bw, use, env, c, wid) in enumerate(modes):
        bx = x + 0.2 + i * cw_
        RBOX(ax, bx + 0.1, y + 0.2, cw_ - 0.2, h - 0.4, tint(c, 0.6), c, 2.5, 0.2, 3.5)
        RBOX(ax, bx + 0.3, y + h / 2 - 1.2, cw_ - 0.6, 2.0, "#fff", "#bbb", 1, 0.1, 3.6)
        cx = bx + cw_ / 2
        T(ax, cx, y + h - 0.7, n, 22, "#222"); T(ax, cx, y + h - 1.55, bw, 18, RED)
        if env is None:
            xs = np.linspace(bx + 0.4, bx + cw_ - 0.4, 400); tt = (xs - xs[0]) / (xs[-1] - xs[0])
            ax.plot(xs, y + h / 2 - 0.2 + 0.6 * np.sin(2 * np.pi * (6 * tt + 2 * np.sin(2 * np.pi * 1.5 * tt))), color=GREEN, lw=2, zorder=5)
        else:
            WAVE(ax, bx + 0.4, bx + cw_ - 0.4, y + h / 2 - 0.2, 0.7, 14, "#37474f", lw=1.8, env=env)
        ax.add_patch(Rectangle((cx - (cw_ - 0.8) * wid / 2, y + 1.15), (cw_ - 0.8) * wid, 0.35, fc=c, ec="#333", lw=1.5, zorder=5))
        T(ax, cx, y + 0.65, use, 12, "#333", False)
    p = P(ax, r[1], "Which mode where?", BLUE, 2)
    p.table([["Use", "Mode"], ["VHF/UHF repeaters", "FM or PM"], ["VHF packet radio", "FM or PM"], ["Weak-signal VHF/UHF", "SSB"], ["10 m, VHF, UHF SSB", "UPPER sideband"]], [1.4, 1], size=14, fill=True)
    p = P(ax, r[2], "SSB vs FM", PURPLE, 3)
    x, y, w, h = p.scene(2.4, top_c="#e1bee7", bot_c="#f3e5f5")
    ax.add_patch(Rectangle((x + w * 0.15, y + 0.4), w * 0.15, h - 1.0, fc="#ce93d8", ec="#333", lw=2, zorder=4)); T(ax, x + w * 0.225, y + h - 0.35, "SSB", 13, PURPLE)
    ax.add_patch(Rectangle((x + w * 0.45, y + 0.4), w * 0.45, h - 1.0, fc="#a5d6a7", ec="#333", lw=2, zorder=4)); T(ax, x + w * 0.675, y + h - 0.35, "FM", 13, GREEN)
    p.ok(["SSB is a form of AMPLITUDE modulation", "SSB: NARROWER bandwidth than FM"], size=13)
    p.no(["FM drawback: only ONE signal received at a time"], size=13)
    p = P(ax, r[3], "Bandwidth cheat table", GREEN, 4)
    p.table([["Signal", "Bandwidth"], ["CW (narrowest)", "150 Hz"], ["SSB voice", "3 kHz"], ["FM voice repeater", "10–15 kHz"], ["AM fast-scan TV", "about 6 MHz"]], [1.3, 1], size=14, fill=True, hl={1})

def d_sat(ax):
    r = grid([(1.15, [1.4, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Working an amateur satellite", INDIGO, 1)
    x, y, w, h = p.scene(p.h - 0.1, "night")
    ax.add_patch(Circle((x + w / 2, y - 9.0), 10.2, fc="#1e88e5", ec="#90caf9", lw=3, zorder=3))
    ax.add_patch(Arc((x + w / 2, y - 9.0), 24.0, 24.0, theta1=55, theta2=125, color="#ffeb3b", lw=2, ls="--", zorder=3.5))
    E(ax, "🛰️", x + w * 0.62, y + h - 1.0, 1.4)
    T(ax, x + w * 0.62 + 1.8, y + h - 0.6, "LEO ≈100 min orbit", 12, "#ffeb3b", ha="left")
    E(ax, "🧑", x + 2.0, y + 1.7, 1.2); HT(ax, x + 3.0, y + 1.1, 0.6)
    ARROW(ax, x + 3.3, y + 2.6, x + w * 0.6, y + h - 1.6, "#ef5350", 3); T(ax, x + w * 0.32, y + h - 1.9, "UPLINK 70 cm (U)", 13, "#ef9a9a")
    ARROW(ax, x + w * 0.66, y + h - 1.6, x + w - 2.0, y + 2.0, "#66bb6a", 3); T(ax, x + w * 0.82, y + h - 2.6, "DOWNLINK 2 m (V)", 13, "#a5d6a7")
    LBOX(ax, x + w - 6.0, y + 0.3, 5.7, 0.9, "U/V mode: up 70 cm, down 2 m", 13, "#ffffffdd", "#fff", INDIGO)
    p = P(ax, r[1], "Satellite words", BLUE, 2)
    p.table([["Term", "Meaning"], ["Beacon", "status info: health & status of satellite"], ["Doppler shift", "freq change from relative motion"], ["Spin fading", "rotation of satellite & antennas"], ["Keplerian elements", "input to tracking programs"], ["Telemetry", "ANYONE may receive it"]], [1, 1.6], size=12, fill=True)
    p = P(ax, r[2], "Don't hog the bird", RED, 3)
    p.icons([("📢", "too much ERP"), ("🚫", "blocks others")], 2.4)
    p.bul(["Excessive uplink power: blocks other users", "Right power: your downlink ≈ beacon strength"], size=12)
    p = P(ax, r[3], "Tracking programs", GREEN, 4)
    p.icons([("🗺️", "maps"), ("⏰", "pass times"), ("〰️", "Doppler")], 2.4)
    p.ok(["Provide: maps, pass times, Doppler-shifted freqs → All correct"], size=12)
    p = P(ax, r[4], "Satellite modes", ORANGE, 5)
    p.icons([("🗣️", "SSB"), ("📻", "FM"), ("📟", "CW/data")], 2.4)
    p.ok(["Common modes: All these choices are correct"], size=13)

def d_activities(ax):
    r = grid([(1, [1.2, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Fox hunt: radio direction finding", GREEN, 1)
    x, y, w, h = p.scene(p.h - 0.1, "sky", top_c="#a5d6a7", bot_c="#e8f5e9")
    E(ax, "🦊", x + w - 1.6, y + 1.6, 1.8); E(ax, "🌲", x + w * 0.5, y + 1.6, 1.8); E(ax, "🌳", x + w * 0.7, y + 1.4, 1.5)
    E(ax, "🧑", x + 1.4, y + 1.6, 1.5)
    L(ax, [x + 2.2, x + 3.6], [y + 2.2, y + 2.2], "#333", 3, 5)
    for k in range(4): L(ax, [x + 2.5 + k * 0.35] * 2, [y + 1.8, y + 2.6], "#333", 2.5, 5)
    ARROW(ax, x + 3.8, y + 2.2, x + w - 2.6, y + 1.8, RED, 3, ls="--")
    LBOX(ax, x + 0.3, y + h - 1.2, w - 0.6, 0.9, "DIRECTIONAL antenna points to the hidden transmitter", 13, "#fff", GREEN, GREEN)
    p.bul(["Locate noise or jamming: RADIO DIRECTION FINDING", "Hidden transmitter hunt: a DIRECTIONAL antenna"], size=13)
    p = P(ax, r[1], "Contesting", RED, 2)
    p.icons([("🏁", "many contacts"), ("⏱️", "set time")], 2.4)
    p.bul(["Contesting: contact as many stations as possible in a set time", "Good practice: send only the MINIMUM info needed"], size=13)
    p = P(ax, r[2], "Grid locator", BLUE, 3)
    x, y, w, h = p.scene(2.8, top_c="#bbdefb", bot_c="#e3f2fd")
    for i in range(6): L(ax, [x + 0.2 + i * (w - 0.4) / 5] * 2, [y + 0.2, y + h - 0.2], "#90a4ae", 1.5, 4)
    for j in range(4): L(ax, [x + 0.2, x + w - 0.2], [y + 0.2 + j * (h - 0.4) / 3] * 2, "#90a4ae", 1.5, 4)
    LBOX(ax, x + 0.2 + 2 * (w - 0.4) / 5, y + 0.2 + (h - 0.4) / 3, (w - 0.4) / 5, (h - 0.4) / 3, "CM87", 12, "#fff59d", RED, RED)
    p.bul(["Grid locator: letter-number code for a geographic location"], size=13)
    p = P(ax, r[3], "Internet linking", TEAL, 4)
    p.table([["Term", "Meaning"], ["VoIP", "voice over the internet, digital"], ["IRLP", "links repeaters via internet; access by DTMF"], ["EchoLink", "transmit via repeater WITHOUT a radio; register call + proof of license"], ["Gateway", "station connecting others to internet"]], [0.8, 1.8], size=11.5, fill=True)
    p = P(ax, r[4], "Remember", GOLD, 5)
    x, y, w, h = p.scene(2.6, top_c="#ffecb3", bot_c="#fff8e1")
    for i in range(12):
        LBOX(ax, x + 0.3 + (i % 4) * (w - 0.6) / 4, y + 0.2 + (2 - i // 4) * (h - 0.4) / 3, (w - 0.6) / 4 - 0.12, (h - 0.4) / 3 - 0.1, "123A456B789C"[i], 12, "#fff", GOLD, "#333")
    p.bul(["IRLP access: DTMF signals", "EchoLink: register first"], size=13)

def d_digital(ax):
    r = grid([(1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Digital modes", PURPLE, 1)
    p.table([["Term", "Meaning"], ["FT8", "works at LOW signal-to-noise"], ["PSK", "Phase Shift Keying"], ["CW", "Morse code"], ["NTSC", "analog fast-scan color TV"]], [0.7, 1.6], size=13, fill=True)
    p.ok(["Digital modes: All these choices are correct"], size=12)
    p = P(ax, r[1], "APRS", BLUE, 2)
    x, y, w, h = p.scene(2.8, top_c="#c8e6c9", bot_c="#e8f5e9")
    for i in range(5): L(ax, [x + 0.3, x + w - 0.3], [y + 0.4 + i * 0.5] * 2, "#a5d6a7", 1.5, 4)
    E(ax, "🚗", x + w * 0.3, y + h / 2, 1.0); E(ax, "📍", x + w * 0.65, y + h / 2 + 0.3, 1.0); E(ax, "🌦️", x + w * 0.85, y + h / 2, 0.9)
    p.ok(["Sends: GPS position, text, weather → All correct", "Use: real-time tactical comms with a map"], size=12)
    p = P(ax, r[2], "Packet radio", TEAL, 3)
    x, y, w, h = p.scene(2.2)
    for i, (t, c) in enumerate([("header", "#90caf9"), ("data", "#a5d6a7"), ("check", "#ffcc80")]):
        LBOX(ax, x + 0.2 + i * (w - 0.4) / 3, y + 0.4, (w - 0.4) / 3 - 0.1, h - 0.8, t, 13, c, "#333")
    p.ok(["Includes: header, check sum, automatic repeat request → All correct"], size=12)
    p.bul(["ARQ: receiver detects errors & asks for retransmission"], size=12)
    p = P(ax, r[3], "DMR", RED, 4)
    x, y, w, h = p.scene(2.2)
    for i in range(6):
        LBOX(ax, x + 0.2 + i * (w - 0.4) / 6, y + 0.4, (w - 0.4) / 6 - 0.05, h - 0.8, "1" if i % 2 == 0 else "2", 14, "#ef9a9a" if i % 2 == 0 else "#90caf9", "#333")
    p.bul(["DMR: time-multiplexes TWO digital voice signals on one 12.5 kHz channel"], size=13)
    p = P(ax, r[4], "WSJT-X software", GREEN, 5)
    p.icons([("🌙", "moonbounce"), ("☄️", "meteor"), ("📉", "weak signal")], 2.4)
    p.ok(["Supports: EME, meteor scatter, weak signal → All correct"], size=12)
    p = P(ax, r[5], "Mesh network", ORANGE, 6)
    x, y, w, h = p.scene(2.6)
    pts = [(0.15, 0.3), (0.4, 0.75), (0.6, 0.3), (0.85, 0.7), (0.3, 0.2)]
    for a in pts:
        for b in pts:
            if a < b: L(ax, [x + w * a[0], x + w * b[0]], [y + h * a[1], y + h * b[1]], "#ffb74d", 1.5, 4)
    for a in pts: E(ax, "📶", x + w * a[0], y + h * a[1], 0.7)
    p.bul(["Mesh: ham data network using MODIFIED commercial Wi-Fi gear"], size=12)

SLIDES = [
    dict(title="Modulation & bandwidth", ids=["T8A01", "T8A02", "T8A04", "T8A03", "T8A06", "T8A07", "T8A12", "T8A05", "T8A11", "T8A08", "T8A09", "T8A10"], draw=d_modes,
         tip="Narrow to wide: CW about 150 Hz, SSB about 3 kHz, FM 10–15 kHz, TV about 6 MHz. Repeaters use FM. SSB = a form of AM."),
    dict(title="Amateur satellites", ids=["T8B08", "T8B10", "T8B01", "T8B05", "T8B11", "T8B07", "T8B09", "T8B06", "T8B03", "T8B02", "T8B12", "T8B04"], draw=d_sat,
         tip="U/V = up on 70 cm, down on 2 m. Doppler shift comes from motion. Don't use more uplink power than you need."),
    dict(title="Fox hunts, contests, grids & internet linking", ids=["T8C01", "T8C02", "T8C03", "T8C04", "T8C05", "T8C07", "T8C08", "T8C06", "T8C09", "T8C10", "T8C11"], draw=d_activities,
         tip="Directional antenna for fox hunts. IRLP uses DTMF. EchoLink needs registration."),
    dict(title="Digital modes: FT8, APRS, packet, DMR & mesh", ids=["T8D01", "T8D02", "T8D06", "T8D09", "T8D04", "T8D03", "T8D05", "T8D08", "T8D11", "T8D07", "T8D10", "T8D12"], draw=d_digital,
         tip="FT8 works with weak signals. APRS sends GPS position. ARQ asks for a resend when there are errors."),
]

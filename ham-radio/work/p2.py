from core2 import *

def d_offsets(ax):
    r = grid([(1.15, [1.5, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "How a repeater works: offset", TEAL, 1)
    x, y, w, h = p.scene(p.h - 0.1, "sky")
    TOWER(ax, x + w / 2, y + 0.45, 3.4); L(ax, [x + w / 2, x + w / 2], [y + 3.85, y + 4.5], "#424242", 3, 5)
    LBOX(ax, x + w / 2 - 1.6, y + 0.6, 3.2, 0.9, "REPEATER", 13, "#37474f", "#000", "white")
    HT(ax, x + 1.6, y + 0.45, 0.8); HT(ax, x + w - 1.6, y + 0.45, 0.8)
    ARROW(ax, x + 2.2, y + 2.8, x + w / 2 - 0.4, y + 4.0, BLUE, 4)
    ARROW(ax, x + w / 2 + 0.4, y + 4.0, x + w - 2.2, y + 2.8, GREEN, 4)
    LBOX(ax, x + 0.3, y + h - 1.6, 4.6, 1.3, "You transmit on repeater INPUT 146.34", 13, "#e3f2fd", BLUE, BLUE)
    LBOX(ax, x + w - 4.9, y + h - 1.6, 4.6, 1.3, "Repeater transmits on OUTPUT 146.94", 13, "#e8f5e9", GREEN, GREEN)
    LBOX(ax, x + w / 2 - 3.0, y + h - 0.95, 6.0, 0.75, "difference = 600 kHz OFFSET", 13, "#fff8e1", GOLD, RED)
    p = P(ax, r[1], "Offsets & calling frequencies", BLUE, 2)
    p.table([["Item", "Value"], ["2 m repeater offset", "± 600 kHz"], ["70 cm repeater offset", "± 5 MHz"], ["2 m FM simplex calling", "146.520 MHz"]], [1.5, 1], size=14, hl={3}, fill=True)
    p.bul(["Repeater offset: difference between a repeater's transmit and receive frequencies",
           "Simplex: transmitting and receiving on the SAME frequency"], size=13)
    p = P(ax, r[2], "Simplex: talk direct", GREEN, 3)
    x, y, w, h = p.scene(2.8, "sky")
    HT(ax, x + 1.3, y + 0.45, 0.7); HT(ax, x + w - 1.3, y + 0.45, 0.7)
    ARROW(ax, x + 1.9, y + 1.6, x + w - 1.9, y + 1.6, GREEN, 3, both=True)
    T(ax, x + w / 2, y + 2.1, "146.52 both ways", 13, GREEN)
    p.bul(["Why simplex channels: nearby stations talk without tying up a repeater"], size=13)
    p = P(ax, r[3], "REVERSE button", ORANGE, 4)
    x, y, w, h = p.scene(2.8)
    RADIO(ax, x + 0.4, y + 0.6, 3.4, 1.7, "REV")
    T(ax, x + w - 2.0, y + h / 2, "TX ⇄ RX\nswapped", 15, ORANGE)
    p.bul(["Purpose: listen on a repeater's INPUT frequency", "Hear the other station directly? → go simplex"], size=13)
    p = P(ax, r[4], "Sharing a frequency", PURPLE, 5)
    p.icons([("📻", "station A"), ("🤝", "negotiate"), ("📻", "station B")], 2.8)
    p.bul(["Two stations interfere on the same freq: they should NEGOTIATE continued use", "Nobody 'owns' a frequency"], size=13)

def d_calling(ax):
    r = grid([(1, [1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Calling a friend on a repeater", BLUE, 1)
    x, y, w, h = p.scene(4.0, "sky")
    HT(ax, x + 1.0, y + 0.45, 0.8); E(ax, "🧑", x + 2.3, y + 1.4, 1.4)
    LBOX(ax, x + 3.3, y + h - 1.6, w - 6.6, 1.3, "\"W1ABC, this is K7XYZ\"", 20, "#fff", BLUE, BLUE)
    TOWER(ax, x + w / 2, y + 0.45, 1.8)
    E(ax, "👩", x + w - 2.3, y + 1.4, 1.4); HT(ax, x + w - 1.0, y + 0.45, 0.8)
    ARROW(ax, x + 1.4, y + 2.4, x + w / 2 - 0.3, y + 2.3, BLUE, 2.5); ARROW(ax, x + w / 2 + 0.3, y + 2.3, x + w - 1.4, y + 2.4, GREEN, 2.5)
    T(ax, x + 3.6, y + 0.3, "K7XYZ (you)", 12, "#111"); T(ax, x + w - 3.6, y + 0.3, "W1ABC (friend)", 12, "#111")
    p.bul(["Order: THEIR call sign first, then YOUR call sign", "Don't say 'breaker break' or just your call"], size=13)
    p = P(ax, r[1], "Answering a CQ", GREEN, 2)
    x, y, w, h = p.scene(3.0)
    LBOX(ax, x + 0.3, y + h / 2 + 0.1, w * 0.45, h / 2 - 0.4, "\"CQ CQ, this is W1ABC\"", 14, "#fff", GREEN, "#222")
    LBOX(ax, x + w * 0.52, y + 0.3, w * 0.45, h / 2 - 0.4, "\"W1ABC, this is K7XYZ\"", 14, "#fff", GREEN, GREEN)
    ARROW(ax, x + w * 0.45, y + h / 2 + 0.1, x + w * 0.55, y + h / 2 - 0.1, GREEN, 3)
    p.bul(["Respond: transmit the other station's call sign, then yours"], size=13)
    p = P(ax, r[2], "CQ = calling any station", RED, 3)
    p.icons([("📢", "CQ CQ CQ"), ("👂", "pause &\nlisten")], 2.6)
    p.bul(["Not on a repeater: say 'CQ' a few times, 'this is', your call, then pause and listen; repeat"], size=13)
    p = P(ax, r[3], "On a repeater", TEAL, 4)
    x, y, w, h = p.scene(2.6)
    E(ax, "👂", x + 0.9, y + h / 2, 1.4)
    LBOX(ax, x + 1.8, y + 0.4, w - 2.1, h - 0.8, "\"K7XYZ listening\"", 18, "#fff", TEAL, TEAL)
    p.bul(["Looking for a contact on a repeater: your call sign + the word 'listening'"], size=13)
    p = P(ax, r[4], "Order to remember", GOLD, 5)
    p.formula("THEIR call\n→ then YOURS", 20)
    p.icons([("1️⃣", "them"), ("2️⃣", "you")], 1.8)

def d_tones(ax):
    r = grid([(1, [1.4, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Can hear the repeater but can't get in?", RED, 1)
    x, y, w, h = p.scene(3.8, "sky")
    TOWER(ax, x + w - 1.8, y + 0.45, 3.0); LBOX(ax, x + w - 3.2, y + 0.55, 2.8, 0.8, "REPEATER", 12, "#37474f", "#000", "white")
    HT(ax, x + 1.2, y + 0.45, 0.8)
    WAVE(ax, x + 2.0, x + w - 3.4, y + 2.6, 0.35, 9, BLUE)
    WAVE(ax, x + 2.0, x + w - 3.4, y + 2.6, 0.12, 2, ORANGE, lw=4)
    T(ax, x + (w - 1.4) / 2, y + 3.4, "voice + hidden low tone (CTCSS)", 13, ORANGE)
    T(ax, x + w - 1.8, y + 3.85, "❌ no tone = ignored", 12, RED)
    p.bul(["Possible causes: wrong offset • wrong CTCSS tone • wrong DCS code → All correct"], size=13)
    p = P(ax, r[1], "Tones & codes", ORANGE, 2)
    p.table([["Name", "What it is"], ["CTCSS", "sub-audible tone with voice that opens a receiver's squelch"], ["DTMF", "TWO tones at once (keypad)"], ["DCS", "digital squelch code"]], [0.7, 2], size=13, hl={1}, fill=True)
    p.icons([("🔢", "DTMF keypad")], 1.6)
    p = P(ax, r[2], "Linked repeaters", TEAL, 3)
    x, y, w, h = p.scene(3.0, "sky")
    for i in range(3):
        TOWER(ax, x + w * (0.2 + i * 0.3), y + 0.45, 1.8)
    for i in range(2):
        ARROW(ax, x + w * (0.25 + i * 0.3), y + 2.0, x + w * (0.45 + i * 0.3), y + 2.0, TEAL, 2.5, both=True)
    p.bul(["Linked network: signal received by one repeater is transmitted by ALL"], size=13)
    p = P(ax, r[3], "Squelch", BLUE, 4)
    x, y, w, h = p.scene(2.8)
    ax.add_patch(Wedge((x + 1.8, y + 0.5), 1.6, 0, 180, fc="#eceff1", ec="#333", lw=2, zorder=4))
    L(ax, [x + 1.8, x + 1.0], [y + 0.5, y + 1.8], RED, 4, 5)
    T(ax, x + w - 2.2, y + h / 2, "no signal\n= silence 🔇", 13, BLUE)
    p.bul(["Purpose: mute receiver audio when no signal is present"], size=13)
    p = P(ax, r[4], "Too loud!", PINK, 5)
    x, y, w, h = p.scene(2.8)
    xs = np.linspace(x + 0.3, x + w - 0.3, 400)
    ys = y + h / 2 + 1.4 * np.sin((xs - x) * 7) * np.exp(-((xs - x - w / 2) / 1.6) ** 2)
    ax.plot(xs, np.clip(ys, y + h / 2 - 0.8, y + h / 2 + 0.8), color=RED, lw=2.5, zorder=5)
    L(ax, [x + 0.3, x + w - 0.3], [y + h / 2 + 0.8, y + h / 2 + 0.8], "#777", 1.5, 5, "--")
    p.bul(["FM audio drops out on voice peaks: you're talking too LOUDLY"], size=13)

def d_dmr(ax):
    r = grid([(1, [1, 1.3]), (1, [1, 1, 1])])
    p = P(ax, r[0], "DMR radio setup", INDIGO, 1)
    x, y, w, h = p.scene(3.4)
    RADIO(ax, x + 0.4, y + 0.6, 4.0, 2.2, "TG 3100")
    LBOX(ax, x + 4.8, y + 0.5, w - 5.1, h - 1.0, "code plug = settings file loaded into radio", 13, "#fff", INDIGO, INDIGO)
    p.bul(["Code plug: configuration data loaded onto your radio to access repeaters and talkgroups"], size=13)
    p = P(ax, r[1], "Talkgroups = separate conversations", BLUE, 2)
    x, y, w, h = p.scene(3.4)
    for i, (n, c) in enumerate([("TG 91\nWorldwide", "#90caf9"), ("TG 3100\nUSA", "#a5d6a7"), ("TG 3106\nCalifornia", "#ffcc80"), ("TG 9\nLocal", "#ce93d8")]):
        LBOX(ax, x + 0.2 + i * (w - 0.4) / 4, y + 0.4, (w - 0.4) / 4 - 0.2, h - 0.8, n, 14, c, "#333")
    p.bul(["Talkgroup: identifier DMR uses to organize traffic — you only hear your group",
           "Join / select a group: program or enter the group's ID code"], size=13)
    p = P(ax, r[2], "Color code", RED, 3)
    p.icons([("🔑", "access code"), ("🗼", "specific\nrepeater")], 2.6)
    p.bul(["Color code: access code programmed into a DMR transmitter to access a specific repeater"], size=13)
    p = P(ax, r[3], "Q signals", PURPLE, 4)
    p.table([["Code", "Meaning"], ["QRM", "interference from other stations"], ["QSY", "changing frequency"], ["CQ", "calling any station"],
             ["QRN", "static / natural noise"], ["QTH", "my location"], ["QSL", "I confirm receipt"]], [0.7, 2], size=14, hl={1, 2})
    p = P(ax, r[4], "Band plan", GOLD, 5)
    x, y, w, h = p.scene(2.4)
    segs = [(0.0, 0.1, "CW", "#90caf9"), (0.1, 0.25, "SSB", "#ce93d8"), (0.25, 0.5, "digital", "#ffe082"), (0.5, 1.0, "FM / repeaters", "#a5d6a7")]
    for a, b, tt, c in segs:
        LBOX(ax, x + 0.2 + a * (w - 0.4), y + 0.4, (b - a) * (w - 0.4), h - 0.8, tt, 12, c, "#333")
    p.bul(["Band plan: VOLUNTARY guideline for modes/activities beyond FCC rules"], size=13)

def d_nets(ax):
    r = grid([(1.1, [1.3, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "A net in action", TEAL, 1)
    x, y, w, h = p.scene(4.4)
    cx, cy = x + w / 2, y + h / 2
    E(ax, "🧑‍✈️", cx, cy + 0.2, 1.6); T(ax, cx, cy - 1.0, "Net Control", 13, TEAL)
    for dx, dy in [(-0.36, 0.25), (0.36, 0.25), (-0.36, -0.25), (0.36, -0.25)]:
        hx, hy = cx + dx * w, cy + dy * h
        E(ax, "🙂", hx, hy, 1.0)
        ARROW(ax, hx + (0.6 if dx < 0 else -0.6), hy, cx + (-1.0 if dx < 0 else 1.0), cy + 0.2, TEAL, 2, both=True, ms=14)
    p.bul(["Net control duties: call the net to order, direct stations checking in",
           "Standard practice: transmit ONLY when directed by net control (unless emergency)"], size=13)
    p = P(ax, r[1], "Emergency groups", RED, 2)
    p.table([["", "RACES", "ARES"], ["What", "FCC Part 97 service for civil defense", "Volunteers registered for public service"],
             ["Needs", "Civil defense certification", "Registration of skills & gear"]], [0.6, 1.2, 1.2], size=12)
    p.note("Certification by civil defense agency → RACES", 13)
    p = P(ax, r[2], "Radiogram parts", ORANGE, 3)
    x, y, w, h = p.scene(3.4, top_c="#fff8e1", bot_c="#fffde7")
    LBOX(ax, x + 0.2, y + h - 1.3, w - 0.4, 1.1, "PREAMBLE: NR 12 R K7XYZ CHECK 8", 12, "#ffe0b2", ORANGE, "#5d4037")
    T(ax, x + w / 2, y + 1.3, "ARRIVED SAFELY X WEATHER\nGOOD X LOVE TO ALL", 12, "#333", family="monospace")
    p.bul(["Preamble: info needed to TRACK the message", "Check: number of words in the TEXT"], size=13)
    p = P(ax, r[3], "Traffic", GREEN, 4)
    p.icons([("📨", "formal\nmessages"), ("🔁", "passed along")], 2.8)
    p.bul(["Traffic: formal messages exchanged by net stations"], size=13)
    p = P(ax, r[4], "Winlink & RACES control op", BLUE, 5)
    p.icons([("📧", "email"), ("📻", "over radio")], 2.4)
    p.bul(["Winlink: relays messages using email addresses based on ham call signs",
           "RACES control op: needs certification of enrollment by a civil defense organization"], size=12)

SLIDES = [
    dict(title="Repeater offsets, simplex & reverse", ids=["T2A07", "T2A01", "T2A03", "T2A02", "T2A11", "T2B09", "T2B01", "T2B08"], draw=d_offsets,
         tip="Repeaters listen on one frequency and talk on another. 2 m offset = 600 kHz, 70 cm = 5 MHz. Simplex = same frequency."),
    dict(title="How to call: CQ and call-sign order", ids=["T2A04", "T2A05", "T2A06", "T2A08", "T2A09"], draw=d_calling,
         tip="Their call sign first, then yours. CQ = calling any station."),
    dict(title="Repeater access: tones, squelch & audio", ids=["T2B04", "T2B02", "T2B06", "T2B03", "T2B13", "T2B05"], draw=d_tones,
         tip="CTCSS = one hidden low tone. DTMF = two tones at once. Squelch hides the hiss."),
    dict(title="DMR, Q signals & band plans", ids=["T4B07", "T2B14", "T2B07", "T4B09", "T2B12", "T2B10", "T2B11", "T2A10"], draw=d_dmr,
         tip="Color code = which repeater. Talkgroup = which conversation. QRM = interference, QSY = change frequency."),
    dict(title="Nets, traffic & emergency groups", ids=["T2C02", "T2C07", "T2C04", "T2C06", "T2C12", "T1A10", "T2C10", "T2C11", "T2C05", "T2C08"], draw=d_nets,
         tip="Net control directs the net. RACES = civil defense with certification. ARES = registered volunteers."),
]

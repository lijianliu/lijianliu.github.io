from core2 import *

# ---------------------------------------------------------------- 1. FCC + license grant
def d_fcc(ax):
    r = grid([(1, [1, 1, 1]), (1, [1.3, 1, 0.9])])
    p = P(ax, r[0], "Who runs ham radio?", BLUE, 1)
    p.icons([("🏛️", "FCC"), ("📜", "Part 97 rules"), ("👮", "enforces")], 2.4)
    p.bul(["FCC: Federal Communications Commission REGULATES and ENFORCES amateur rules in the U.S.",
           "Not: ARRL (a club), Homeland Security, ITU"], size=13)
    p.note("FCC rules ALWAYS apply to an amateur station", 13)
    p = P(ax, r[1], "Basis & purpose of ham radio", GREEN, 2)
    p.icons([("🔧", "technical"), ("🎙️", "communication"), ("🆘", "emergency"), ("🌍", "goodwill")], 2.4)
    p.ok(["Advancing skills in the TECHNICAL and COMMUNICATION phases of the radio art"], size=13)
    p.no(["Business / making money", "Broadcasting to the public"], size=13)
    p = P(ax, r[2], "Keep your email current!", RED, 3)
    p.icons([("📧", "FCC email"), ("❌", "bounces"), ("⚠️", "trouble!")], 2.4)
    p.bul(["Can't reach you by email: REVOCATION of station license or SUSPENSION of operator license",
           "FCC contacts you by EMAIL, not paper mail"], size=13)
    p = P(ax, r[3], "From exam to on-the-air", INDIGO, 4)
    x, y, w, h = p.scene(4.0)
    steps = [("📝", "1. Pass\nexam"), ("💾", "2. Grant in\nFCC ULS\ndatabase"), ("📧", "3. Email link\nto download\nlicense"), ("🎙️", "4. Transmit!")]
    for i, (e, t) in enumerate(steps):
        cx = x + w * (0.125 + i * 0.25)
        RBOX(ax, cx - w * 0.105, y + 0.15, w * 0.21, h - 0.3, "#fff", INDIGO, 2, 0.2, 3)
        E(ax, e, cx, y + h - 0.95, 1.2)
        T(ax, cx, y + 1.15, t, 12, "#222")
        if i < 3: ARROW(ax, cx + w * 0.108, y + h / 2, cx + w * 0.142, y + h / 2, INDIGO, 3, ms=16)
    p.bul(["Proof of license: it APPEARS in the FCC ULS database", "Transmit: as soon as your grant appears in the database"], size=13)
    p = P(ax, r[4], "What is ULS?", TEAL, 5)
    x, y, w, h = p.scene(3.4, top_c="#b2dfdb", bot_c="#e0f2f1")
    RBOX(ax, x + 0.3, y + 0.3, w - 0.6, h - 0.6, "#fff", "#555", 2, 0.1, 3)
    ax.add_patch(Rectangle((x + 0.3, y + h - 0.95), w - 0.6, 0.65, fc="#37474f", zorder=3.5))
    ax.add_patch(Rectangle((x + 0.3, y + h - 0.95), w - 0.6, 0.65, fc="#37474f", zorder=3.5)); T(ax, x + w / 2, y + h - 0.62, "FCC ULS License Search", 12, "white")
    p.table([["Call", "Class", "Status"], ["KF1XXX", "Technician", "ACTIVE"]], [1, 1.2, 1], r0=0.07, r1=0.93, top=y + h - 1.15, size=12)
    p.bul(["ULS: Universal Licensing System – online FCC database", "Holds: your name, mailing address & call sign"], size=13)
    p = P(ax, r[5], "Memory hooks", GOLD, 6)
    p.icons([("🧠", "remember")], 1.6)
    p.formula("FCC = the boss", 17, fc="#e3f2fd", ec=BLUE, color=BLUE)
    p.formula("ULS = proof", 17, fc="#e8f5e9", ec=GREEN, color=GREEN)
    p.formula("Email = keep\nit current", 16, fc="#ffebee", ec=RED, color=RED)

# ---------------------------------------------------------------- 2. classes, term, call signs
def d_classes(ax):
    r = grid([(1, [1, 1.6]), (1.05, [1.15, 1, 1])])
    p = P(ax, r[0], "License classes issued today", BLUE, 1)
    x, y, w, h = p.scene(3.4)
    for i, (n, c) in enumerate([("Technician", GREEN), ("General", BLUE), ("Amateur Extra", PURPLE)]):
        LBOX(ax, x + 0.3 + i * 0.7, y + 0.2 + i * 1.05, w * 0.6, 0.9, n, 15, c, "#111", "white")
    T(ax, x + w * 0.86, y + h / 2, "⬆\nmore\nprivileges", 12, PURPLE)
    p.ok(["Technician, General, Amateur Extra"], size=13)
    p.no(["Novice, Technician Plus, Advanced: no new licenses"], size=13)
    p = P(ax, r[1], "License timeline: 10 years • 90 days • 2 years", RED, 2)
    x, y, w, h = p.scene(4.2)
    yy = y + 1.9
    L(ax, [x + 0.3, x + w - 0.3], [yy, yy], "#333", 5)
    X = lambda t: x + 0.6 + t / 12.4 * (w - 1.2)
    for i in range(11):
        L(ax, [X(i), X(i)], [yy - 0.12, yy + 0.12], "#333", 2); T(ax, X(i), yy - 0.4, f"{i}y", 10, "#555", False)
    ax.add_patch(Rectangle((X(9.75), yy - 0.22), X(10) - X(9.75), 0.44, fc=GREEN, zorder=5))
    ax.add_patch(Rectangle((X(10), yy - 0.22), X(12) - X(10), 0.44, fc=ORANGE, zorder=5))
    for t in [0, 9.75, 10, 12]:
        ax.add_patch(Circle((X(t), yy), 0.2, fc=RED, zorder=6))
    E(ax, "📜", X(0) + 0.3, yy + 1.0, 1.0); T(ax, X(0) + 1.6, yy + 1.0, "granted", 12)
    T(ax, X(5), yy + 0.9, "Normal term = TEN years", 16, GREEN)
    T(ax, X(9.75) - 0.6, yy - 1.2, "90 days early:\nmay renew", 12, GREEN)
    T(ax, X(10), yy + 1.25, "EXPIRES", 13, RED)
    T(ax, X(11.2), yy - 1.2, "2-year grace:\nrenew, but\nNO transmitting", 11, ORANGE)
    p.note("Expired but in grace period? Wait until renewed before transmitting.", 13)
    p = P(ax, r[2], "Reading a call sign", INDIGO, 3)
    x, y, w, h = p.scene(2.7)
    cw = (w - 0.5) / 6
    for i, (ch, c) in enumerate(zip("KF1XXX", [BLUE, BLUE, RED, GREEN, GREEN, GREEN])):
        LBOX(ax, x + 0.25 + i * cw + 0.04, y + 0.75, cw - 0.08, 1.75, ch, 30, "#fff", c, c)
    for a, b, lab, c in [(0, 2, "prefix", BLUE), (2, 3, "digit", RED), (3, 6, "suffix", GREEN)]:
        T(ax, x + 0.25 + (a + b) / 2 * cw, y + 0.38, lab, 12, c)
    p.bul(["Group D: 2 letters + digit + 3 letters (KF1XXX)", "Shorter calls: Groups A–C (higher classes)"], size=13)
    p = P(ax, r[3], "Vanity call signs", PURPLE, 4)
    p.icons([("✨", "pick your own"), ("🪪", "any license")], 2.6)
    p.ok(["ANY licensed amateur may choose one"], size=13)
    p.no(["Only Extra class", "Only club stations"], size=13)
    p = P(ax, r[4], "Add-ons after your call (phone)", TEAL, 5)
    x, y, w, h = p.scene(3.4)
    for i, s in enumerate(["KF1XXX / KT", "KF1XXX / W3", "KF1XXX / 4"]):
        LBOX(ax, x + 0.25, y + h - 1.0 - i * 1.05, w * 0.62, 0.85, s, 15, "#fff", TEAL, "#222")
        T(ax, x + w * 0.83, y + h - 0.58 - i * 1.05, "✔ OK", 15, GREEN, family="DejaVu Sans")
    p.bul(["Self-assigned indicators: All these choices are correct"], size=13)

# ---------------------------------------------------------------- 3. phonetics & identification
def d_id(ax):
    r = grid([(1, [1.2, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "ID: at least every 10 minutes AND at the end", BLUE, 1)
    x, y, w, h = p.scene(3.9)
    yy = y + 1.1
    L(ax, [x + 0.3, x + w - 0.3], [yy, yy], "#333", 4)
    X = lambda m: x + 0.6 + m / 30 * (w - 1.2)
    for m in range(0, 31, 5):
        L(ax, [X(m), X(m)], [yy - 0.15, yy + 0.15], "#333", 2); T(ax, X(m), yy - 0.5, f"{m} min", 11, "#333", False)
    for m, lab in [(0, "start"), (10, "ID"), (20, "ID"), (27, "END: ID")]:
        E(ax, "🗣️", X(m), yy + 1.1, 1.0); T(ax, X(m), yy + 2.15, lab, 13, RED)
    ax.add_patch(Rectangle((X(0), yy - 0.08), X(27) - X(0), 0.16, fc=BLUE, zorder=5))
    p.bul(["Tactical calls: \"Race Headquarters\" is fine, but STILL give your FCC call every 10 min",
           "Test transmissions: must identify too"], size=13)
    p = P(ax, r[1], "How to identify", GREEN, 2)
    p.table([["Rule", "Answer"], ["Language on phone", "ENGLISH"], ["Phone station IDs with", "CW or phone"],
             ["Phonetic alphabet", "ENCOURAGED on phone"], ["No ID needed when", "controlling model craft"]], [1.3, 1], size=13)
    p.note("Phonetics: encouraged, not required!", 13, fc="#e8f5e9", ec=GREEN, color=GREEN)
    for k, (title, words) in enumerate([("Phonetic alphabet A–M", ["Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliett", "Kilo", "Lima", "Mike"]),
                                         ("Phonetic alphabet N–Z", ["November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"])]):
        p = P(ax, r[2 + k], title, INDIGO, 3 + k)
        rows = [[w_[0], w_] for w_ in words]
        p.table([rows[i] + (rows[i + 7] if i + 7 < len(rows) else ["", ""]) for i in range(7)], [0.4, 1.3, 0.4, 1.3], head=False, size=14, align=["center", "left", "center", "left"])
    p = P(ax, r[4], "Spelling unusual words", ORANGE, 5)
    p.icons([("🔤", "odd name?"), ("🗣️", "spell it")], 2.2)
    p.formula("X-ray India Oscar", 15)
    p.bul(["Technique: spell words with a standard phonetic alphabet"], size=13)

# ---------------------------------------------------------------- 4. HF privileges & power
def d_hf(ax):
    r = grid([(1.15, [1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "10-meter band for Technicians (28.0 – 29.7 MHz)", BLUE, 1)
    x, y, w, h = p.scene(p.h - 0.1)
    f0, f1 = 28.0, 29.7
    X = lambda f: x + 0.4 + (f - f0) / (f1 - f0) * (w - 0.8)
    top = y + h - 1.0
    LBOX(ax, X(28.0), top - 2.4, X(28.3) - X(28.0), 2.2, "CW + data\n(FT8)\n28.0–28.3", 15, "#90caf9", BLUE)
    LBOX(ax, X(28.3), top - 2.4, X(28.5) - X(28.3), 2.2, "PHONE\n+ CW\n28.300–\n28.500", 15, "#a5d6a7", GREEN)
    LBOX(ax, X(28.5), top - 2.4, X(29.7) - X(28.5), 2.2, "General / Extra only — Technicians have NO privileges 28.5–29.7", 16, "#eeeeee", "#999", "#666")
    for f in [28.0, 28.3, 28.5, 29.0, 29.5, 29.7]:
        T(ax, X(f), top + 0.35, f"{f:.1f}", 13, "#111")
    LBOX(ax, X(28.2) - 0.2, y + 0.3, 3.2, 1.0, "Beacons 28.2–28.3", 12, "#ffe082", ORANGE)
    ARROW(ax, X(28.25), y + 1.35, X(28.25), top - 2.45, ORANGE, 2, ms=14)
    E(ax, "🎙️", X(28.4), y + 0.85, 1.1)
    LBOX(ax, X(28.6), y + 0.3, X(29.65) - X(28.6), 1.0, "Automatic propagation beacons: 28.200–28.300 MHz", 13, "#fff8e1", GOLD)
    p = P(ax, r[1], "Technician phone on HF", GREEN, 2)
    p.icons([("🎙️", "voice"), ("🔟", "meters")], 2.4)
    p.formula("10-meter band ONLY", 17, fc="#e8f5e9", ec=GREEN, color=GREEN)
    p.bul(["Voice: 28.300 – 28.500 MHz"], size=13)
    p = P(ax, r[2], "Maximum power (PEP)", RED, 3)
    p.table([["Where", "Max PEP"], ["Tech HF segments", "200 W"], ["Above 30 MHz", "1500 W"]], [1.4, 1], size=15, hl={1})
    p.icons([("⚡", "PEP = peak envelope power")], 1.6)
    p.bul(["1500 W: except some specific restrictions"], size=13)
    p = P(ax, r[3], "Digital (FT8) privileges", PURPLE, 4)
    x, y, w, h = p.scene(2.0)
    for i, b in enumerate(["10 m", "6 m", "2 m"]):
        LBOX(ax, x + 0.2 + i * (w - 0.4) / 3, y + 0.3, (w - 0.4) / 3 - 0.15, h - 0.6, b, 18, "#fff", PURPLE, PURPLE)
    p.icons([("💻", "FT8 software"), ("📻", "radio")], 1.8)
    p.ok(["Bands for Tech FT8: All these choices are correct"], size=13)

# ---------------------------------------------------------------- 5. VHF/UHF & edges
def d_vhf(ax):
    r = grid([(1, [1]), (1.1, [1, 1, 1.15])])
    p = P(ax, r[0], "VHF / UHF bands – Technicians get full privileges above 50 MHz", BLUE, 1)
    x, y, w, h = p.scene(p.h - 0.1)
    for i, (n, rg, ex, c) in enumerate([("6 m", "50 – 54 MHz", "52.525 MHz ✔", "#ffcc80"), ("2 m", "144 – 148 MHz", "146.52 MHz ✔", "#a5d6a7"),
                                        ("1.25 m", "222 – 225 MHz", "", "#ce93d8"), ("70 cm", "420 – 450 MHz", "", "#90caf9"), ("23 cm", "1240 – 1300 MHz", "", "#f48fb1")]):
        bx = x + 0.2 + i * (w - 0.4) / 5
        RBOX(ax, bx + 0.08, y + 0.2, (w - 0.4) / 5 - 0.16, h - 0.4, c, "#333", 2, 0.2, 3)
        cx = bx + (w - 0.4) / 10
        T(ax, cx, y + h - 0.9, n, 26); T(ax, cx, y + h - 2.0, rg, 15, "#222", False)
        if ex: T(ax, cx, y + 0.9, ex, 15, GREEN, family="DejaVu Sans")
        else: HT(ax, cx, y + 0.45, 0.6)
    p = P(ax, r[1], "CW-only segments", INDIGO, 2)
    x, y, w, h = p.scene(2.2)
    for i, (a, b) in enumerate([("50.0", "50.1"), ("144.0", "144.1")]):
        LBOX(ax, x + 0.15 + i * (w - 0.3) / 2, y + 0.2, (w - 0.3) / 2 - 0.15, h - 0.4, f"{a} – {b} MHz", 15, "#fff", INDIGO, INDIGO)
    p.icons([("📟", "Morse  ·−  only")], 1.8)
    p.bul(["Bottom 100 kHz of 6 m and 2 m"], size=13)
    p = P(ax, r[2], "SSB above 50 MHz", TEAL, 3)
    x, y, w, h = p.scene(2.4)
    WAVE(ax, x + 0.3, x + w - 0.3, y + h / 2, 0.75, 14, TEAL, lw=2.5, env=lambda t: 0.3 + 0.7 * np.abs(np.sin(3 * np.pi * t)))
    p.bul(["SSB phone: allowed in at least SOME segment of ALL these bands"], size=13)
    p.bul(["Weak-signal SSB lives at the bottom of each band"], size=13)
    p = P(ax, r[3], "Don't sit on the band edge!", RED, 4)
    x, y, w, h = p.scene(2.8, top_c="#fff", bot_c="#fff")
    ax.add_patch(Rectangle((x + 0.1, y + 0.1), w * 0.6, h - 0.5, fc="#c8e6c9", ec=GREEN, lw=2, zorder=3))
    ax.add_patch(Rectangle((x + 0.1 + w * 0.6, y + 0.1), w * 0.4 - 0.2, h - 0.5, fc="#ffcdd2", ec=RED, lw=2, zorder=3))
    xs = np.linspace(x + w * 0.38, x + w * 0.85, 200)
    ax.plot(xs, y + 0.1 + 1.9 * np.exp(-((xs - x - 0.1 - w * 0.6) / 0.8) ** 2), color=PURPLE, lw=3, zorder=5)
    T(ax, x + w * 0.2, y + 0.55, "in band", 12, GREEN); T(ax, x + w * 0.86, y + 0.55, "outside!", 12, RED)
    p.bul(["Why: signal width • dial error • drift → All correct", "Secondary segments: avoid interfering with non-ham users"], size=12)

# ---------------------------------------------------------------- 6. space + repeaters
def d_space(ax):
    r = grid([(1, [1.2, 1]), (1, [1.3, 1])])
    p = P(ax, r[0], "Space stations & the ISS", INDIGO, 1)
    x, y, w, h = p.scene(4.0, "night")
    ax.add_patch(Rectangle((x, y), w, 0.7, fc="#1e88e5", zorder=4))
    L(ax, [x, x + w], [y + 1.5, y + 1.5], "#ffeb3b", 2, 5, "--")
    T(ax, x + 1.4, y + 1.85, "50 km", 12, "#ffeb3b")
    E(ax, "🛰️", x + w * 0.72, y + h - 1.0, 1.4)
    HT(ax, x + 1.2, y + 0.7, 0.55)
    ARROW(ax, x + 1.6, y + 2.3, x + w * 0.66, y + h - 1.1, "#ffeb3b", 2.5)
    T(ax, x + w * 0.38, y + h - 0.6, "uplink", 12, "#ffeb3b")
    p.bul(["Space station: amateur station MORE than 50 km above Earth", "Talk to ISS on VHF: ANY Technician or higher",
           "Satellite control op: anyone allowed on the UPLINK frequency"], size=12)
    p = P(ax, r[1], "Repeater = retransmits at the same time", TEAL, 2)
    x, y, w, h = p.scene(3.4, "sky")
    TOWER(ax, x + w / 2, y + 0.45, 2.3); L(ax, [x + w / 2, x + w / 2], [y + 2.75, y + 3.2], "#424242", 3, 5)
    HT(ax, x + 1.0, y + 0.45, 0.6); HT(ax, x + w - 1.0, y + 0.45, 0.6)
    ARROW(ax, x + 1.4, y + 2.1, x + w / 2 - 0.3, y + 2.8, BLUE, 2.5); ARROW(ax, x + w / 2 + 0.3, y + 2.8, x + w - 1.4, y + 2.1, GREEN, 2.5)
    T(ax, x + w / 2 - 2.0, y + 3.0, "in: ch A", 11, BLUE); T(ax, x + w / 2 + 2.0, y + 3.0, "out: ch B", 11, GREEN)
    p.bul(["Repeater station: simultaneously retransmits another station on a different channel", "Bad message relayed by mistake: control op of the ORIGINATING station is accountable"], size=12)
    p = P(ax, r[2], "Frequency coordinators", ORANGE, 3)
    x, y, w, h = p.scene(2.6)
    for i, (e, t) in enumerate([("👥", "local hams who\ncould run repeaters"), ("🧑‍💼", "pick Volunteer\nFrequency Coordinator"), ("📋", "recommends repeater\n& auxiliary channels")]):
        cx = x + w * (i + 0.5) / 3
        E(ax, e, cx, y + h - 0.75, 1.1); T(ax, cx, y + 0.65, t, 11)
        if i < 2: ARROW(ax, cx + 0.8, y + h - 0.75, cx + w / 3 - 0.8, y + h - 0.75, ORANGE, 2.5, ms=16)
    p.bul(["Recommends channels: Volunteer Frequency Coordinator recognized by local amateurs",
           "Selects coordinator: local/regional hams whose stations could be repeater or auxiliary stations"], size=12)
    p = P(ax, r[3], "Auxiliary station", PURPLE, 4)
    x, y, w, h = p.scene(3.2, "sky")
    TOWER(ax, x + 1.2, y + 0.45, 1.8); TOWER(ax, x + w - 1.2, y + 0.45, 2.4)
    T(ax, x + 1.2, y + 2.8, "remote\nreceiver", 11, "#111"); T(ax, x + w - 1.2, y + 3.0, "main repeater", 11, "#111")
    ARROW(ax, x + 1.8, y + 2.0, x + w - 1.8, y + 2.4, PURPLE, 3)
    T(ax, x + w / 2, y + 1.6, "one-way link", 13, PURPLE)
    p.bul(["Example: one-way link from a remote repeater receiver to the main repeater transmitter"], size=12)

# ---------------------------------------------------------------- 7. control operator
def d_control(ax):
    r = grid([(1, [1.2, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Control operator vs station licensee", BLUE, 1)
    x, y, w, h = p.scene(3.6)
    E(ax, "🏠", x + 1.4, y + 2.2, 1.7); T(ax, x + 1.4, y + 0.65, "Station licensee\n(owner)", 12)
    E(ax, "🧑‍✈️", x + w - 1.6, y + 2.2, 1.7); T(ax, x + w - 1.6, y + 0.65, "Control operator", 12)
    RADIO(ax, x + w / 2 - 1.5, y + 0.5, 3.0, 1.5, "TX")
    ARROW(ax, x + 2.5, y + 3.0, x + w - 2.6, y + 3.0, PURPLE, 3, rad=-0.15)
    T(ax, x + w / 2, y + 2.65, "DESIGNATES", 12, PURPLE)
    p.bul(["Control operator: designated by the licensee; responsible for transmissions & FCC rule compliance",
           "Who designates: the station licensee", "Control point: where the control operator function is performed"], size=12)
    p = P(ax, r[1], "Responsibility & rules", RED, 2)
    p.table([["Question", "Answer"], ["Transmit with NO control op?", "NEVER"], ["Control op ≠ licensee: who's responsible?", "BOTH"],
             ["Whose class sets privileges?", "Control operator's"], ["Tech control op in Extra segment?", "At no time"]], [1.7, 1], size=13, hl={1})
    p.note("Outside privileges: only for immediate safety of life/property", 12)
    p = P(ax, r[2], "LOCAL control", GREEN, 3)
    x, y, w, h = p.scene(3.0)
    E(ax, "🧑‍💻", x + w * 0.3, y + h / 2, 2.0); RADIO(ax, x + w * 0.55, y + 0.7, 2.6, 1.4, "")
    p.bul(["Operator is AT the radio", "Uses the controls directly"], size=13)
    p = P(ax, r[3], "REMOTE control", TEAL, 4)
    p.icons([("💻", "you"), ("🌐", "internet"), ("📻", "station")], 3.0)
    p.bul(["Example: operating over the INTERNET", "May be remotely controlled: ANY station"], size=13)
    p = P(ax, r[4], "AUTOMATIC control", ORANGE, 5)
    x, y, w, h = p.scene(3.0, "sky")
    E(ax, "🤖", x + w * 0.3, y + h / 2 + 0.2, 1.8); TOWER(ax, x + w * 0.7, y + 0.45, 2.2)
    p.bul(["Example: REPEATER operation", "No operator at a control point"], size=13)

# ---------------------------------------------------------------- 8. prohibited
def d_prohibit(ax):
    r = grid([(1, [1, 1, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "No broadcasting", RED, 1)
    p.icons([("📡", "to the public"), ("🚫", "not allowed")], 2.6)
    p.bul(["Broadcasting: transmissions intended for the GENERAL PUBLIC", "One-way transmission prohibited: broadcasting"], size=13)
    p = P(ax, r[1], "Music", PINK, 2)
    p.icons([("🎵", "music ✘"), ("🚀", "manned\nspacecraft"), ("🎧", "retransmit")], 2.6)
    p.bul(["Music only when INCIDENTAL to retransmitting MANNED spacecraft communications"], size=13)
    p = P(ax, r[2], "Helping news / broadcasters", ORANGE, 3)
    p.icons([("📰", "news"), ("🚑", "life safety")], 2.6)
    p.bul(["Only when directly related to IMMEDIATE safety of human life or protection of property"], size=13)
    p = P(ax, r[3], "Secret codes", INDIGO, 4)
    p.icons([("🔒", "codes ✘"), ("🛰️", "space\nstation"), ("✈️", "model\ncraft")], 2.6)
    p.bul(["Encoded messages only for CONTROL COMMANDS to space stations or model craft", "Model craft control: no on-air ID needed"], size=13)
    p = P(ax, r[4], "Bad language & jamming", RED, 5)
    p.icons([("🤬", "obscene"), ("📢", "jamming")], 2.6)
    p.bul(["Indecent or obscene: ANY such language prohibited", "Willful or malicious interference: prohibited"], size=13)
    p = P(ax, r[5], "Money & selling", GREEN, 6)
    p.icons([("🏫", "classroom"), ("📦", "sell gear")], 2.6)
    p.bul(["Paid: only classroom instruction at a school", "Sell YOUR gear: OK, not regularly"], size=13)

# ---------------------------------------------------------------- 9. international, third party, clubs
def d_intl(ax):
    r = grid([(1.1, [1.3, 1]), (1, [1, 1, 1])])
    p = P(ax, r[0], "Third-party communications", BLUE, 1)
    x, y, w, h = p.scene(3.8)
    E(ax, "👧", x + 1.0, y + 2.4, 1.6); T(ax, x + 1.0, y + 0.8, "unlicensed\nfriend", 12)
    E(ax, "🧑‍✈️", x + 3.6, y + 2.4, 1.6); T(ax, x + 3.6, y + 0.8, "you\n(control op)", 12)
    RADIO(ax, x + 5.0, y + 1.7, 2.4, 1.2, "")
    ARROW(ax, x + 7.6, y + 2.3, x + w - 2.2, y + 2.3, BLUE, 3)
    E(ax, "🧔", x + w - 1.2, y + 2.4, 1.6); T(ax, x + w - 1.2, y + 0.8, "foreign\nham", 12)
    T(ax, x + (7.6 + w - 2.2) / 2, y + 2.85, "on behalf of friend", 12, BLUE)
    T(ax, x + 6.2, y + 0.8, "message", 12, "#333")
    p.bul(["Definition: message from a control op to another station's control op on behalf of ANOTHER PERSON",
           "Foreign station: must be in a country with a THIRD-PARTY AGREEMENT with the U.S."], size=13)
    p = P(ax, r[1], "Talking to other countries", TEAL, 2)
    p.icons([("🌍", "worldwide"), ("📻", "ham topics"), ("💬", "personal\nremarks")], 2.6)
    p.bul(["Allowed: talk incidental to ham radio + remarks of a personal character",
           "Banned: any country that told the ITU it objects"], size=13)
    p = P(ax, r[2], "At sea", INDIGO, 3)
    p.icons([("🚢", "US-documented\nvessel"), ("👨‍✈️", "master's\npermission")], 3.0)
    p.bul(["International waters: OK from a US-documented vessel WITH the master's permission"], size=13)
    p = P(ax, r[3], "Club station license", GREEN, 4)
    p.icons(["🙂", "🙂", "🙂", "🙂"], 2.0)
    p.formula("At least 4 members", 18, fc="#e8f5e9", ec=GREEN, color=GREEN)
    p.bul(["Club license: needs a club with 4+ members"], size=13)
    p = P(ax, r[4], "FCC inspection", RED, 5)
    p.icons([("🕵️", "FCC rep"), ("📋", "records")], 3.0)
    p.bul(["Station & records: available at ANY TIME upon request by an FCC representative"], size=13)

SLIDES = [
    dict(title="The FCC & getting your license", ids=["T1A01", "T1A02", "T2C01", "T1A04", "T1A05", "T1C10", "T1C04"], draw=d_fcc,
         tip="The FCC makes and enforces the rules. Your license is official once it shows in the FCC ULS database."),
    dict(title="License classes, term, renewal & call signs", ids=["T1C01", "T1C08", "T1C07", "T1C09", "T1C11", "T1C05", "T1C02", "T1F06"], draw=d_classes,
         tip="10-year term • renew up to 90 days early • 2-year grace period, but no transmitting while expired."),
    dict(title="Station ID & the phonetic alphabet", ids=["T1F03", "T1F02", "T1F04", "T1F05", "T1D12", "T1D11", "T1A03", "T2C03"], draw=d_id,
         tip="Give your call sign at least every 10 minutes and at the end, in English. Phonetics are encouraged."),
    dict(title="Technician HF privileges & power limits", ids=["T1B01", "T1B06", "T1B11", "T1A06", "T1B12", "T1B05"], draw=d_hf,
         tip="Tech voice on HF = 28.300–28.500 MHz only, 200 W PEP. Above 30 MHz: up to 1500 W."),
    dict(title="VHF/UHF bands & band edges", ids=["T1B03", "T1B04", "T1B07", "T1B10", "T1B09", "T1B08"], draw=d_vhf,
         tip="6 m = 50–54 MHz, 2 m = 144–148 MHz. The bottom 100 kHz of each is CW only."),
    dict(title="Space stations, repeaters & coordinators", ids=["T1A07", "T1B02", "T1E02", "T1F09", "T1F10", "T1A08", "T1A09", "T1D07"], draw=d_space,
         tip="Space = above 50 km. Repeaters re-send signals on another channel. Coordinators are chosen by local hams.",
         explain=["""<h3>&#128225; What is an auxiliary station?</h3>
<p>An <b>auxiliary station</b> is a <b>helper station</b>. It doesn't talk to people. It sends signals
<b>from one point to another inside a group of ham stations that work together</b>, usually to help run a repeater.</p>
<p><b>Example: a repeater with a remote receiver.</b> A repeater sits on a hill. To hear weak handheld radios in a valley
far away, the club puts an extra <b>receiver</b> in that valley. That receiver needs a way to send what it hears
back to the repeater, so a small transmitter beams it <b>one way</b> to the main repeater on a separate channel.
That one-way link is an auxiliary station (the "one-way link" panel in the picture above).</p>
<ul>
<li><span class="yes">&#10004; Auxiliary station:</span> one-way transmissions between a remote repeater receiver and the main repeater transmitter.</li>
<li><span class="no">&#10008; Not one:</span> a backup radio kept for emergencies. That's just a spare radio.</li>
<li><span class="no">&#10008; Not one:</span> a station in the Military Auxiliary Radio System (MARS). The word "auxiliary" is a trap!</li>
<li><span class="no">&#10008; Not one:</span> a second station at a multi-operator contest site.</li>
</ul>
<p><b>Who picks their channels?</b> Repeater and auxiliary stations need channels that won't bump into each other.
A <b>Volunteer Frequency Coordinator recognized by local amateurs</b> recommends them. The coordinator is chosen by
<b>local or regional hams whose stations could be repeater or auxiliary stations</b>, not by the FCC.</p>"""]),
    dict(title="Control operators & types of control", ids=["T1E11", "T1E03", "T1E05", "T1E01", "T1E07", "T1E04", "T1E06", "T2C09", "T1E08", "T1E09", "T1E10"], draw=d_control,
         tip="Every transmitting station needs a control operator. Repeater = automatic, internet = remote."),
    dict(title="What's prohibited (and the exceptions)", ids=["T1D10", "T1D02", "T1D04", "T1D09", "T1D03", "T1D06", "T1A11", "T1D08", "T1D05"], draw=d_prohibit,
         tip="No broadcasting, music, codes or bad words, but learn the exceptions: ISS audio, model craft, safety of life."),
    dict(title="Third-party, international, clubs & inspections", ids=["T1F08", "T1F07", "T1C03", "T1D01", "T1C06", "T1F11", "T1F01"], draw=d_intl,
         tip="Passing a message for someone else = third-party. Foreign country must have an agreement with the U.S."),
]

"""Slide rendering engine: illustration (matplotlib) + exact bank questions (PIL)."""
import json, os, io, textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, FancyArrowPatch, Ellipse, Arc, Wedge
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "qs.json")))}

plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]

W = 2000            # slide width
ILL_H = 760         # illustration height
SUP = "/System/Library/Fonts/Supplemental/"
F_REG = SUP + "Arial.ttf"
F_BOLD = SUP + "Arial Bold.ttf"
F_BLACK = SUP + "Arial Black.ttf"
F_UNI = SUP + "Arial Unicode.ttf"
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------------------------------------------------------------- emoji
_emoji_cache = {}
def emoji_img(ch):
    if ch not in _emoji_cache:
        f = ImageFont.truetype(EMOJI_FONT, 160)
        im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, 20), ch, font=f, embedded_color=True)
        bb = im.getbbox()
        if not bb:
            QA.append(f'EMOJI-BLANK: {ch!r}')
        im = im.crop(bb) if bb else im
        _emoji_cache[ch] = np.asarray(im)
    return _emoji_cache[ch]

# ---------------------------------------------------------------- drawing helpers (axes units: x 0..20, y 0..7.6)
def emo(ax, ch, x, y, s=1.0, z=5):
    """Place emoji centred at (x,y) with height s."""
    a = emoji_img(ch)
    h, w = a.shape[:2]
    sw = s * w / h
    ax.imshow(a, extent=(x - sw / 2, x + sw / 2, y - s / 2, y + s / 2), zorder=z, interpolation="bilinear")

def txt(ax, x, y, s, size=20, color="#222", weight="bold", ha="center", va="center", z=6, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z, **kw)

def box(ax, x, y, w, h, text="", fc="#e3f2fd", ec="#1565c0", size=18, color="#0d2a4a", lw=3, r=0.25, weight="bold", z=3, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z, ls=ls)
    ax.add_patch(p)
    if text:
        t = txt(ax, x + w / 2, y + h / 2, text, size=size, color=color, weight=weight, z=z + 1)
        BOXED.append((p, t))
    return p

def arrow(ax, x1, y1, x2, y2, color="#d32f2f", lw=4, text=None, size=16, both=False, style="-|>", ms=28, z=4, rad=0.0, tcolor=None, toff=(0, 0.3), ls="-"):
    st = "<|-|>" if both else style
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=st, mutation_scale=ms, color=color, lw=lw, zorder=z,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls)
    ax.add_patch(a)
    if text:
        txt(ax, (x1 + x2) / 2 + toff[0], (y1 + y2) / 2 + toff[1], text, size=size, color=tcolor or color, z=z + 1)

def wave(ax, x0, x1, y, amp=0.4, cycles=4, color="#1976d2", lw=3, phase=0, z=3, ls="-"):
    x = np.linspace(x0, x1, 600)
    ax.plot(x, y + amp * np.sin(2 * np.pi * cycles * (x - x0) / (x1 - x0) + phase), color=color, lw=lw, zorder=z, ls=ls)

def line(ax, xs, ys, color="#333", lw=3, z=2, ls="-"):
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, ls=ls, solid_capstyle="round")

def radio(ax, x, y, w=2.4, h=1.2, label="", color="#37474f", screen="146.520"):
    """Simple transceiver at bottom-left (x,y)."""
    box(ax, x, y, w, h, fc=color, ec="#111", lw=2, r=0.15, z=3)
    box(ax, x + 0.15, y + h * 0.45, w * 0.55, h * 0.4, fc="#b2ff59", ec="#111", lw=1.5, r=0.05, z=4)
    if screen:
        txt(ax, x + 0.15 + w * 0.275, y + h * 0.65, screen, size=max(9, int(13 * w / 2.4)), color="#1b5e20", z=5, family="monospace")
    ax.add_patch(Circle((x + w * 0.83, y + h * 0.6), h * 0.2, fc="#cfd8dc", ec="#111", lw=1.5, zorder=4))
    for i in range(4):
        ax.add_patch(Rectangle((x + 0.2 + i * w * 0.13, y + 0.12), w * 0.09, h * 0.18, fc="#90a4ae", ec="#111", lw=1, zorder=4))
    if label:
        txt(ax, x + w / 2, y - 0.3, label, size=16)

def handheld(ax, x, y, s=1.0, color="#263238"):
    box(ax, x - 0.35 * s, y, 0.7 * s, 1.6 * s, fc=color, ec="#000", lw=2, r=0.12, z=4)
    line(ax, [x + 0.2 * s, x + 0.2 * s], [y + 1.6 * s, y + 2.5 * s], color="#000", lw=5 * s, z=4)
    box(ax, x - 0.25 * s, y + 0.9 * s, 0.5 * s, 0.45 * s, fc="#b2ff59", ec="#000", lw=1, r=0.05, z=5)

def antenna(ax, x, y, h=2.5, color="#424242", lw=4):
    line(ax, [x, x], [y, y + h], color=color, lw=lw, z=3)
    ax.add_patch(Circle((x, y + h), 0.08, fc=color, ec=color, zorder=3))

def yagi(ax, x, y, length=3, color="#424242", n=5, mast=2.0):
    line(ax, [x, x], [y, y + mast], color=color, lw=4)
    line(ax, [x - length / 2, x + length / 2], [y + mast, y + mast], color=color, lw=4)
    for i in range(n):
        xx = x - length / 2 + i * length / (n - 1)
        hh = 0.9 - 0.08 * i
        line(ax, [xx, xx], [y + mast - hh / 2, y + mast + hh / 2], color=color, lw=3)

def tower(ax, x, y, h=4, w=0.8, color="#78909c"):
    line(ax, [x - w / 2, x - 0.1], [y, y + h], color=color, lw=3)
    line(ax, [x + w / 2, x + 0.1], [y, y + h], color=color, lw=3)
    n = 8
    for i in range(n):
        y1 = y + i * h / n; y2 = y + (i + 1) * h / n
        f1 = 1 - i / n * (1 - 0.2 / w); f2 = 1 - (i + 1) / n * (1 - 0.2 / w)
        line(ax, [x - w / 2 * f1, x + w / 2 * f2], [y1, y2], color=color, lw=1.5)
        line(ax, [x + w / 2 * f1, x - w / 2 * f2], [y1, y2], color=color, lw=1.5)

def ground(ax, x, y, color="#333"):
    for i, w in enumerate([0.5, 0.33, 0.16]):
        line(ax, [x - w / 2, x + w / 2], [y - i * 0.12, y - i * 0.12], color=color, lw=3)

def earth(ax, y=0.6, color="#8d6e63", grass="#66bb6a"):
    ax.add_patch(Rectangle((0, 0), 20, y, fc=color, ec="none", zorder=1))
    ax.add_patch(Rectangle((0, y - 0.12), 20, 0.12, fc=grass, ec="none", zorder=1))

def sky(ax, top="#bbdefb", bottom="#e3f2fd"):
    g = np.linspace(0, 1, 256).reshape(-1, 1)
    import matplotlib.colors as mc
    cm = mc.LinearSegmentedColormap.from_list("s", [bottom, top])
    ax.imshow(g, extent=(0, 20, 0, 7.6), origin="lower", cmap=cm, aspect="auto", zorder=0)

def check(ax, x, y, ok=True, size=26):
    txt(ax, x, y, "✔" if ok else "✘", size=size, color="#2e7d32" if ok else "#c62828", family="DejaVu Sans")

# ---------------------------------------------------------------- slide composition
QA = []
BOXED = []
def _qa_texts(fig, ax):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bbs = []
    for t in ax.texts:
        if not t.get_text().strip():
            continue
        bb = t.get_window_extent(r)
        if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > W + 2 or bb.y1 > ILL_H + 2:
            QA.append(f"OFFCANVAS: {t.get_text()!r} {bb}")
        bbs.append((t.get_text(), bb))
    for p, t in BOXED:
        pb = p.get_window_extent(r); tb = t.get_window_extent(r)
        if tb.x0 < pb.x0 - 1 or tb.x1 > pb.x1 + 1 or tb.y0 < pb.y0 - 1 or tb.y1 > pb.y1 + 1:
            QA.append(f"BOXOVERFLOW: {t.get_text()!r}")
    BOXED.clear()
    for im in ax.images:
        if im.get_zorder() == 0:
            continue
        ib = im.get_window_extent(r)
        for s_, tb in bbs:
            ox = min(ib.x1, tb.x1) - max(ib.x0, tb.x0); oy = min(ib.y1, tb.y1) - max(ib.y0, tb.y0)
            if ox > 6 and oy > 6:
                QA.append(f"EMOJI-ON-TEXT: {s_!r}")
    pbs = [p.get_window_extent(r) for p in ax.patches if isinstance(p, FancyBboxPatch)]
    for s_, tb in bbs:
        for pb in pbs:
            ox = min(pb.x1, tb.x1) - max(pb.x0, tb.x0); oy = min(pb.y1, tb.y1) - max(pb.y0, tb.y0)
            inside = tb.x0 >= pb.x0 - 1 and tb.x1 <= pb.x1 + 1 and tb.y0 >= pb.y0 - 1 and tb.y1 <= pb.y1 + 1
            if ox > 4 and oy > 4 and not inside:
                QA.append(f"CROSSES-BOX: {s_!r}")
    for i in range(len(bbs)):
        for j in range(i + 1, len(bbs)):
            a, b = bbs[i][1], bbs[j][1]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0); oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > 4 and oy > 4:
                QA.append(f"OVERLAP: {bbs[i][0]!r} <> {bbs[j][0]!r}")

def render_illustration(fn):
    fig = plt.figure(figsize=(W / 100, ILL_H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 20); ax.set_ylim(0, 7.6); ax.axis("off")
    ax.set_facecolor("white")
    fn(ax)
    ax.set_xlim(0, 20); ax.set_ylim(0, 7.6)
    _qa_texts(fig, ax)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")

def wrap_px(draw, text, fnt, maxw):
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

SUBCOLORS = {"T1": "#1565c0", "T2": "#00838f", "T3": "#6a1b9a", "T4": "#ef6c00", "T5": "#c62828",
             "T6": "#2e7d32", "T7": "#4527a0", "T8": "#ad1457", "T9": "#00695c", "T0": "#d84315"}
SUBNAMES = {"T1": "Commission's Rules", "T2": "Operating Procedures", "T3": "Radio Wave Propagation",
            "T4": "Amateur Radio Practices", "T5": "Electrical Principles", "T6": "Electronic Components",
            "T7": "Practical Circuits", "T8": "Signals and Emissions", "T9": "Antennas and Feed Lines", "T0": "Safety"}

def question_block(draw_dummy, q, colw, fonts):
    """Return list of drawing ops & height for one question."""
    fq, fo, fid, fs = fonts
    ops = []
    y = 0
    # id badge line
    ops.append(("badge", y, q["id"]))
    qlines = wrap_px(draw_dummy, q["q"], fq, colw - 20)
    y += 46
    for l in qlines:
        ops.append(("q", y, l)); y += 36
    y += 8
    for i, o in enumerate(q["opts"]):
        letter = "ABCD"[i]
        ok = letter == q["ans"]
        olines = wrap_px(draw_dummy, o, fo, colw - 110)
        h = 12 + 31 * len(olines) + 6
        ops.append(("opt", y, letter, olines, ok, h))
        y += h + 7
    y += 18
    return ops, y

def render_slide(num, total, slide, out_path):
    ids = slide["ids"]
    sub = ids[0][:2]
    col = SUBCOLORS[sub]
    ill = render_illustration(slide["draw"])
    fq = font(F_BOLD, 28); fo = font(F_REG, 26); fid = font(F_BLACK, 24); fs = font(F_UNI, 30)
    dummy = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    ncol = 2
    gap = 40; margin = 40
    colw = (W - 2 * margin - gap) // ncol
    blocks = [question_block(dummy, QS[i], colw, (fq, fo, fid, fs)) for i in ids]
    # distribute blocks into columns balancing height (keep order: fill col1 then col2)
    total_h = sum(b[1] for b in blocks)
    cols = [[], []]; hs = [0, 0]
    best = None
    for split in range(len(blocks) + 1):
        h1 = sum(b[1] for b in blocks[:split]); h2 = total_h - h1
        m = max(h1, h2)
        if best is None or m < best[0]:
            best = (m, split)
    split = best[1]
    cols = [blocks[:split], blocks[split:]]
    qh = best[0]
    HEAD = 120
    TIP = 0
    tip = slide.get("tip", "")
    ftip = font(F_BOLD, 30)
    tiplines = wrap_px(dummy, "💡  " + tip, ftip, W - 2 * margin - 40) if tip else []
    TIP = 30 + 40 * len(tiplines) if tip else 0
    H = HEAD + ILL_H + TIP + 30 + qh + 60
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, HEAD], fill=col)
    d.text((margin, 18), slide["title"], font=font(F_BLACK, 46), fill="white")
    subs = []
    for i in ids:
        if i[:2] not in subs:
            subs.append(i[:2])
    d.text((margin, 80), " + ".join(f"{s_} {SUBNAMES[s_]}" for s_ in subs) + f"   •   {len(ids)} questions", font=font(F_BOLD, 26), fill="white")
    pg = f"{num}/{total}"
    fpg = font(F_BLACK, 40)
    d.text((W - margin - d.textlength(pg, font=fpg), 30), pg, font=fpg, fill="white")
    img.paste(ill, (0, HEAD))
    y0 = HEAD + ILL_H
    d.line([0, y0, W, y0], fill=col, width=4)
    if tip:
        d.rectangle([margin, y0 + 12, W - margin, y0 + TIP - 6], fill="#fff8e1", outline="#ffb300", width=3)
        yy = y0 + 24
        for l in tiplines:
            # draw emoji bulb separately
            if l.startswith("💡"):
                e = Image.fromarray(emoji_img("💡")).resize((34, 34))
                img.paste(e, (margin + 18, yy), e)
                l = l[1:].lstrip()
                d.text((margin + 62, yy), l, font=ftip, fill="#5d4037")
            else:
                d.text((margin + 62, yy), l, font=ftip, fill="#5d4037")
            yy += 40
    ystart = y0 + TIP + 24
    for ci, colblocks in enumerate(cols):
        x0 = margin + ci * (colw + gap)
        y = ystart
        for ops, h in colblocks:
            for op in ops:
                if op[0] == "badge":
                    bw = d.textlength(op[2], font=fid) + 28
                    d.rounded_rectangle([x0, y + op[1], x0 + bw, y + op[1] + 38], radius=10, fill=col)
                    d.text((x0 + 14, y + op[1] + 4), op[2], font=fid, fill="white")
                elif op[0] == "q":
                    d.text((x0, y + op[1]), op[2], font=fq, fill="#111")
                elif op[0] == "opt":
                    _, oy, letter, olines, ok, oh = op
                    fill = "#e8f5e9" if ok else "#fafafa"
                    outl = "#2e7d32" if ok else "#e0e0e0"
                    d.rounded_rectangle([x0, y + oy, x0 + colw, y + oy + oh], radius=10, fill=fill, outline=outl, width=4 if ok else 2)
                    sym = "✔" if ok else "✘"
                    d.text((x0 + 12, y + oy + 6), sym, font=fs, fill="#2e7d32" if ok else "#c62828")
                    d.text((x0 + 52, y + oy + 8), letter + ".", font=font(F_BOLD, 26), fill="#2e7d32" if ok else "#777")
                    ly = y + oy + 8
                    for l in olines:
                        d.text((x0 + 92, ly), l, font=font(F_BOLD, 26) if ok else fo, fill="#1b5e20" if ok else "#555")
                        ly += 31
            y += h
    # footer
    d.text((margin, H - 42), "Questions & answers copied word-for-word from the 2026-2030 Technician Class (Element 2) Question Pool.  ✔ = correct answer,  ✘ = wrong answer",
           font=font(F_UNI, 20), fill="#888")
    img.save(out_path, optimize=True)
    return img


def render_image(slide, out_path):
    """Illustration-only PNG for the HTML page."""
    ill = render_illustration(slide["draw"])
    ill.save(out_path, optimize=True)
    return ill

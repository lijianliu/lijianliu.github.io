"""Cheat-sheet style panel engine. Canvas 1536x1024 px, axes units 30 x 20 (51.2 px per unit)."""
import io, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, FancyArrowPatch, Ellipse, Arc, Wedge
from PIL import Image, ImageFont
from core import emoji_img, QS, SUBCOLORS, SUBNAMES

plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
HERE = os.path.dirname(os.path.abspath(__file__))
PXW, PXH = 1536, 1024
UW, UH = 30.0, 20.0
PPU = PXW / UW                      # pixels per unit
SUP = "/System/Library/Fonts/Supplemental/"
_FONTS = {}
def _pil(size, bold):
    k = (round(size * 100 / 72), bold)
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(SUP + ("Arial Bold.ttf" if bold else "Arial.ttf"), k[0])
    return _FONTS[k]

def text_w(s, size, bold=False):
    """Width of string in axes units."""
    return _pil(size, bold).getlength(s) / PPU

def line_h(size):
    return size * 100 / 72 * 1.22 / PPU

def wrap(s, size, maxw, bold=False):
    out = []
    for para in s.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if text_w(t, size, bold) <= maxw or not cur:
                cur = t
            else:
                out.append(cur); cur = w
        out.append(cur)
    return out

def tint(c, f=0.88):
    r, g, b = mcolors.to_rgb(c)
    return (r + (1 - r) * f, g + (1 - g) * f, b + (1 - b) * f)

QA = []
BLUE, RED, GREEN, ORANGE, PURPLE, TEAL, GOLD, PINK, INDIGO, BROWN = (
    "#1565c0", "#c62828", "#2e7d32", "#e65100", "#6a1b9a", "#00838f", "#f9a825", "#ad1457", "#283593", "#5d4037")

# ------------------------------------------------------------------ primitives (absolute units)
def T(ax, x, y, s, size=14, color="#222", bold=True, ha="center", va="center", z=8, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight="bold" if bold else "normal",
                   ha=ha, va=va, zorder=z, linespacing=1.15, **kw)

def E(ax, ch, x, y, s=1.5, z=6):
    a = emoji_img(ch); h, w = a.shape[:2]; sw = s * w / h
    ax.imshow(a, extent=(x - sw / 2, x + sw / 2, y - s / 2, y + s / 2), zorder=z, interpolation="bilinear")

def IMG(ax, path, x, y, w=None, h=None, z=6):
    a = np.asarray(Image.open(path).convert("RGB")); ih, iw = a.shape[:2]
    if w is None: w = h * iw / ih
    if h is None: h = w * ih / iw
    ax.imshow(a, extent=(x, x + w, y, y + h), zorder=z)
    return w, h

def FIGFIT(ax, path, x, y, w, h, tint_rgb=(255, 244, 200), z=6, pad=0.15):
    """Fit a scanned figure inside (x,y,w,h) keeping aspect; paper-white becomes a soft tint."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    lum = a.mean(2, keepdims=True) / 255.0
    t = np.array(tint_rgb, float).reshape(1, 1, 3)
    out = (a * (1 - lum) + t * lum).clip(0, 255).astype(np.uint8)
    ih, iw = out.shape[:2]
    sc = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    fw, fh = iw * sc, ih * sc
    fx, fy = x + (w - fw) / 2, y + (h - fh) / 2
    ax.imshow(out, extent=(fx, fx + fw, fy, fy + fh), zorder=z, interpolation="lanczos")
    ax.add_patch(Rectangle((fx, fy), fw, fh, fc="none", ec="#bdbdbd", lw=1.5, zorder=z + 0.1))
    return fx, fy, fw, fh

def RBOX(ax, x, y, w, h, fc="#fff", ec="#333", lw=2, r=0.25, z=3, ls="-", alpha=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z, ls=ls, alpha=alpha)
    ax.add_patch(p); return p

def LBOX(ax, x, y, w, h, s, size=14, fc="#fff8e1", ec=GOLD, color="#222", lw=2, z=4, bold=True, r=0.2):
    """Box with centred, auto-wrapped label; shrinks font until it fits."""
    RBOX(ax, x, y, w, h, fc, ec, lw, r, z)
    while size > 8:
        ls = wrap(s, size, w - 0.35, bold)
        if len(ls) * line_h(size) <= h - 0.15 and all(text_w(l, size, bold) <= w - 0.3 for l in ls):
            break
        size -= 0.5
    if size <= 8: QA.append(f"LBOX-TOO-SMALL: {s[:40]!r}")
    T(ax, x + w / 2, y + h / 2, "\n".join(ls), size, color, bold, z=z + 1)

def ARROW(ax, x1, y1, x2, y2, color=RED, lw=3, both=False, ms=22, z=5, rad=0.0, ls="-", head=True):
    st = "<|-|>" if both else ("-|>" if head else "-")
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=st, mutation_scale=ms, color=color, lw=lw, zorder=z,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls))

def L(ax, xs, ys, color="#333", lw=3, z=4, ls="-"):
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, ls=ls, solid_capstyle="round")

def WAVE(ax, x0, x1, y, amp=0.4, cycles=4, color=BLUE, lw=3, phase=0, z=5, ls="-", env=None):
    x = np.linspace(x0, x1, 800)
    yy = amp * np.sin(2 * np.pi * cycles * (x - x0) / (x1 - x0) + phase)
    if env is not None:
        yy = yy * env((x - x0) / (x1 - x0))
    ax.plot(x, y + yy, color=color, lw=lw, zorder=z, ls=ls)

def TOWER(ax, x, y, h=4, w=0.9, color="#78909c", z=4):
    L(ax, [x - w / 2, x - 0.1], [y, y + h], color, 3, z); L(ax, [x + w / 2, x + 0.1], [y, y + h], color, 3, z)
    n = max(4, int(h * 2))
    for i in range(n):
        y1 = y + i * h / n; y2 = y + (i + 1) * h / n
        f1 = 1 - i / n * (1 - 0.2 / w); f2 = 1 - (i + 1) / n * (1 - 0.2 / w)
        L(ax, [x - w / 2 * f1, x + w / 2 * f2], [y1, y2], color, 1.3, z); L(ax, [x + w / 2 * f1, x - w / 2 * f2], [y1, y2], color, 1.3, z)

def RADIO(ax, x, y, w=3.2, h=1.6, screen="146.520", color="#37474f", z=5):
    RBOX(ax, x, y, w, h, color, "#111", 2, 0.15, z)
    RBOX(ax, x + 0.15, y + h * 0.45, w * 0.58, h * 0.42, "#b2ff59", "#111", 1.2, 0.05, z + 1)
    if screen:
        sz = 11
        while text_w(screen, sz, True) > w * 0.55 and sz > 6: sz -= 0.5
        T(ax, x + 0.15 + w * 0.29, y + h * 0.66, screen, sz, "#1b5e20", z=z + 2, family="monospace")
    ax.add_patch(Circle((x + w * 0.84, y + h * 0.62), h * 0.21, fc="#cfd8dc", ec="#111", lw=1.5, zorder=z + 1))
    for i in range(4):
        ax.add_patch(Rectangle((x + 0.18 + i * w * 0.14, y + 0.13), w * 0.1, h * 0.17, fc="#90a4ae", ec="#111", lw=1, zorder=z + 1))

def HT(ax, x, y, s=1.0, color="#263238", z=5):
    """Handheld radio, bottom-centre at (x,y), height ~2.5*s."""
    RBOX(ax, x - 0.38 * s, y, 0.76 * s, 1.7 * s, color, "#000", 1.8, 0.12 * s, z)
    L(ax, [x + 0.2 * s, x + 0.2 * s], [y + 1.7 * s, y + 2.6 * s], "#000", 4.5 * s, z)
    RBOX(ax, x - 0.27 * s, y + 0.95 * s, 0.54 * s, 0.48 * s, "#b2ff59", "#000", 1, 0.05, z + 1)
    for i in range(3):
        ax.add_patch(Rectangle((x - 0.25 * s + i * 0.19 * s, y + 0.2 * s), 0.13 * s, 0.13 * s, fc="#90a4ae", zorder=z + 1))

def GND(ax, x, y, color="#333", s=1.0):
    for i, w in enumerate([0.6, 0.4, 0.2]):
        L(ax, [x - w * s / 2, x + w * s / 2], [y - i * 0.14 * s, y - i * 0.14 * s], color, 2.5)

def RES(ax, x0, y, x1, color="#333", lw=2.5, z=5):
    """Zig-zag resistor horizontal from x0 to x1."""
    n = 6; xs = np.linspace(x0 + (x1 - x0) * 0.15, x1 - (x1 - x0) * 0.15, n * 2 + 1)
    ys = [y + (0.22 if i % 2 else -0.22) if 0 < i < n * 2 else y for i in range(n * 2 + 1)]
    L(ax, [x0] + list(xs) + [x1], [y] + ys + [y], color, lw, z)

def RESV(ax, x, y0, y1, color="#333", lw=2.5, z=5):
    n = 6; ys = np.linspace(y0 + (y1 - y0) * 0.15, y1 - (y1 - y0) * 0.15, n * 2 + 1)
    xs = [x + (0.22 if i % 2 else -0.22) if 0 < i < n * 2 else x for i in range(n * 2 + 1)]
    L(ax, [x] + xs + [x], [y0] + list(ys) + [y1], color, lw, z)

def SKY(ax, x, y, w, h, top="#90caf9", bottom="#e3f2fd", z=1):
    g = np.linspace(0, 1, 128).reshape(-1, 1)
    cm = mcolors.LinearSegmentedColormap.from_list("s", [bottom, top])
    ax.imshow(g, extent=(x, x + w, y, y + h), origin="lower", cmap=cm, aspect="auto", zorder=z)

def GROUND(ax, x, y, w, h=0.5, z=2):
    ax.add_patch(Rectangle((x, y), w, h, fc="#8d6e63", ec="none", zorder=z))
    ax.add_patch(Rectangle((x, y + h - 0.12), w, 0.12, fc="#66bb6a", ec="none", zorder=z))

# ------------------------------------------------------------------ panels
PANELS = []
SCALES = {}
FILL_ON = [False]
FREE = {}
FILL_ROWS = {}
SHIFT = {}
MAXS = 1.75
class P:
    HEAD = 1.15
    def __init__(self, ax, rect, title, color=BLUE, num=None):
        x, y, w, h = rect
        self.ax, self.color = ax, color
        RBOX(ax, x, y, w, h, tint(color, 0.93), color, 2.5, 0.3, 2)
        RBOX(ax, x, y + h - self.HEAD, w, self.HEAD, color, color, 2.5, 0.3, 2.1)
        ax.add_patch(Rectangle((x + 0.02, y + h - self.HEAD), w - 0.04, 0.35, fc=color, ec="none", zorder=2.2))
        tx = x + 0.35
        if num is not None:
            ax.add_patch(Circle((x + 0.75, y + h - self.HEAD / 2), 0.42, fc="white", ec="none", zorder=3))
            T(ax, x + 0.75, y + h - self.HEAD / 2, str(num), 15, color, z=4)
            tx = x + 1.35
        sz = 17
        while text_w(title, sz, True) > x + w - tx - 0.2 and sz > 10: sz -= 0.5
        T(ax, tx, y + h - self.HEAD / 2, title, sz, "white", ha="left", z=4)
        self.x, self.y, self.w, self.h = x + 0.3, y + 0.25, w - 0.6, h - self.HEAD - 0.5
        self.title = title
        self.cursor = self.y + self.h          # top of free space (absolute)
        self.idx = len(PANELS)
        self.fill_rows = 0
        self.s = SCALES.get(self.idx, 1.0)
        self.cursor -= SHIFT.get(self.idx, 0)
        PANELS.append(self)

    def X(self, r): return self.x + r * self.w
    def E(self, ch, xr, dy, size):
        E(self.ax, ch, self.X(xr), self.cursor - dy * self.s, size * min(self.s, 1.5))
    def T(self, xr, dy, s, size=14, color="#222", bold=True, **kw):
        return T(self.ax, self.X(xr), self.cursor - dy * self.s, s, size * self.s, color, bold, **kw)
    def Y(self, r): return self.y + r * self.h

    def _chk(self, bottom, what):
        if bottom < self.y - 0.15:
            QA.append(f"PANEL-OVERFLOW [{self.title}] {what[:40]!r} by {self.y - bottom:.2f}u")

    def bul(self, items, r0=0.0, r1=1.0, top=None, size=14, color="#222", gap=0.12, dot="•", dotc=None, bold_lead=True):
        size = size * self.s
        """Bullets. Item 'Lead: rest' renders lead in panel colour. Returns new top (absolute y)."""
        x0, x1 = self.X(r0), self.X(r1)
        y = self.cursor if top is None else top
        dotc = dotc or self.color
        for it in items:
            lead, rest = "", it
            if bold_lead and ": " in it and it.index(": ") < 28:
                lead, rest = it.split(": ", 1); lead += ": "
            ind = (text_w(dot, size, True) + 0.25) if dot else 0.1
            lines = wrap(lead + rest, size, x1 - x0 - ind - 0.05, True)
            if dot:
                T(self.ax, x0 + 0.05, y - line_h(size) / 2, dot, size, dotc, ha="left", va="center", family="DejaVu Sans" if dot in "✔✘" else None)
            # draw first line with lead coloured
            for i, ln in enumerate(lines):
                yy = y - line_h(size) * (i + 0.5)
                if i == 0 and lead and ln.startswith(lead.strip()):
                    lt = lead.strip()
                    T(self.ax, x0 + ind, yy, lt, size, self.color, True, ha="left")
                    rest_ln = ln[len(lt):].lstrip()
                    if rest_ln:
                        T(self.ax, x0 + ind + text_w(lt, size, True) + text_w(" ", size) + 0.05, yy, rest_ln, size, color, False, ha="left")
                else:
                    T(self.ax, x0 + ind, yy, ln, size, color, False, ha="left")
            y -= line_h(size) * len(lines) + gap
        self._chk(y + gap, items[-1] if items else "")
        if top is None: self.cursor = y
        return y

    def para(self, s, r0=0.0, r1=1.0, top=None, size=14, color="#222", bold=False, ha="left"):
        size = size * self.s
        x0, x1 = self.X(r0), self.X(r1)
        y = self.cursor if top is None else top
        lines = wrap(s, size, x1 - x0 - 0.1, bold)
        xx = x0 if ha == "left" else (x0 + x1) / 2
        T(self.ax, xx, y, "\n".join(lines), size, color, bold, ha=ha, va="top")
        y -= line_h(size) * len(lines) + 0.12
        self._chk(y, s)
        if top is None: self.cursor = y
        return y

    def table(self, rows, cols, r0=0.0, r1=1.0, top=None, size=13, head=True, hl=None, hcolor=None, align=None, fill=False):
        size = size * self.s
        """rows: list of lists; cols: relative widths. hl: set of row indexes to highlight."""
        x0, x1 = self.X(r0), self.X(r1)
        y = self.cursor if top is None else top
        tw = x1 - x0; cw = [c / sum(cols) * tw for c in cols]
        hcolor = hcolor or self.color
        hl = hl or set()
        allw = [[wrap(str(c), size, cw[ci] - 0.25, (head and ri == 0) or ci == 0) for ci, c in enumerate(row)] for ri, row in enumerate(rows)]
        nat = [max(len(w) for w in wl) * line_h(size) + 0.18 for wl in allw]
        if fill and top is None: self.fill_rows += len(rows)
        extra = 0
        if fill and top is None and FILL_ON[0]:
            nrows_fill = FILL_ROWS.get(self.idx, len(rows))
            extra = max(0, FREE.get(self.idx, 0) - 0.15) / nrows_fill
            extra = min(extra, line_h(size) * 1.6)
        for ri, row in enumerate(rows):
            isH = head and ri == 0
            wrapped = allw[ri]
            rh = nat[ri] + extra
            fc = hcolor if isH else ("#fff59d" if ri in hl else ("#ffffff" if ri % 2 else tint(self.color, 0.85)))
            self.ax.add_patch(Rectangle((x0, y - rh), tw, rh, fc=fc, ec=tint(self.color, 0.4), lw=1, zorder=3))
            xx = x0
            for ci, wl in enumerate(wrapped):
                a = (align[ci] if align else ("left" if ci == 0 else "center"))
                tx = xx + 0.12 if a == "left" else xx + cw[ci] / 2
                T(self.ax, tx, y - rh / 2, "\n".join(wl), size, "white" if isH else "#222",
                  isH or (ci == 0), ha=a)
                xx += cw[ci]
            y -= rh
        self._chk(y, "table")
        y -= 0.15
        if top is None: self.cursor = y
        return y

    def formula(self, s, size=24, r0=0.0, r1=1.0, top=None, h=None, fc="#fff9c4", ec=GOLD, color=RED):
        size = size * self.s
        y = self.cursor if top is None else top
        h = h or line_h(size) * (s.count("\n") + 1) + 0.35
        LBOX(self.ax, self.X(r0), y - h, self.X(r1) - self.X(r0), h, s, size, fc, ec, color, 2.5)
        y -= h + 0.18
        self._chk(y, s)
        if top is None: self.cursor = y
        return y

    def note(self, s, size=13, r0=0.0, r1=1.0, top=None, h=None, fc="#ffebee", ec=RED, color="#b71c1c"):
        size = size * self.s
        y = self.cursor if top is None else top
        lines = wrap(s, size, self.X(r1) - self.X(r0) - 0.4, True)
        h = h or len(lines) * line_h(size) + 0.3
        LBOX(self.ax, self.X(r0), y - h, self.X(r1) - self.X(r0), h, s, size, fc, ec, color, 2)
        y -= h + 0.18
        self._chk(y, s)
        if top is None: self.cursor = y
        return y

    def rest(self, pad=0.1):
        """Remaining area below cursor -> (x, y, w, h); marks panel full."""
        h = self.cursor - self.y - pad
        top = self.cursor
        self.cursor = self.y
        return self.x, top - h - pad / 2, self.w, max(h, 0)

    def ok(self, items, **kw):
        return self.bul(items, dot="✔", dotc=GREEN, **kw)

    def no(self, items, **kw):
        return self.bul(items, dot="✘", dotc=RED, **kw)

    def scene(self, h, kind="card", top_c=None, bot_c=None):
        """Reserve a drawing area with a filled background. kind: card|sky|night|space."""
        x, y, w, hh = self.area(h)
        ax = self.ax
        if kind == "sky":
            SKY(ax, x, y, w, hh, top_c or "#64b5f6", bot_c or "#e3f2fd", z=2.5); GROUND(ax, x, y, w, 0.45, z=2.6)
        elif kind == "night":
            SKY(ax, x, y, w, hh, top_c or "#0d1b3e", bot_c or "#3949ab", z=2.5)
            rng = np.random.default_rng(int(x * 10 + y))
            ax.scatter(x + rng.uniform(0, w, int(w * 4)), y + rng.uniform(hh * 0.3, hh, int(w * 4)), s=3, c="white", zorder=2.7)
        else:
            SKY(ax, x, y, w, hh, top_c or tint(self.color, 0.55), bot_c or tint(self.color, 0.82), z=2.5)
        ax.add_patch(FancyBboxPatch((x, y), w, hh, boxstyle="round,pad=0,rounding_size=0.2", fc="none", ec=self.color, lw=2, zorder=2.8))
        return x, y, w, hh

    def icons(self, items, h=2.2, kind="card", label_size=12, color=None):
        """Row of (emoji, label) on a scene card."""
        x, y, w, hh = self.scene(h, kind)
        n = len(items)
        for i, it in enumerate(items):
            e, lab = (it, "") if isinstance(it, str) else it
            cx = x + w * (i + 0.5) / n
            es = min(hh * (0.62 if lab else 0.8), w / n * 0.8)
            E(self.ax, e, cx, y + hh - es / 2 - 0.12 if lab else y + hh / 2, es)
            if lab:
                ls = label_size * self.s
                while text_w(max(lab.split("\n"), key=len), ls, True) > w / n - 0.1 and ls > 8: ls -= 0.5
                T(self.ax, cx, y + 0.12 + line_h(ls) * (lab.count("\n") + 1) / 2, lab, ls, color or "#111", True, z=8)
        return x, y, w, hh

    def space(self, d):
        self.cursor -= d * self.s
        return self.cursor

    def area(self, h):
        """Reserve h units at cursor for a drawing; returns (x, y_bottom, w, h)."""
        h = h * max(0.5, min(self.s, 1.5))
        top = self.cursor
        self.cursor -= h + 0.15
        self._chk(self.cursor + 0.15, "drawing area")
        return self.x, top - h, self.w, h

def grid(rows, top=18.55, bottom=0.2, left=0.2, right=29.8, gap=0.28):
    """rows: list of (height_weight, [width_weights]) -> list of rects."""
    H = top - bottom - gap * (len(rows) - 1)
    tot = sum(r[0] for r in rows)
    out, y = [], top
    for hw, ws in rows:
        h = H * hw / tot; y -= h
        Wd = right - left - gap * (len(ws) - 1); x = left
        for wf in ws:
            w = Wd * wf / sum(ws); out.append((x, y, w, h)); x += w + gap
        y -= gap
    return out

# ------------------------------------------------------------------ QA + render
def _qa(fig, ax):
    fig.canvas.draw(); r = fig.canvas.get_renderer()
    bbs = []
    for t in ax.texts:
        s = t.get_text()
        if not s.strip(): continue
        bb = t.get_window_extent(r)
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1 > PXW + 1 or bb.y1 > PXH + 1:
            QA.append(f"OFFCANVAS: {s[:40]!r}")
        bbs.append((s, bb))
    for i in range(len(bbs)):
        a = bbs[i][1]
        for j in range(i + 1, len(bbs)):
            b = bbs[j][1]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0); oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > 3 and oy > 3:
                QA.append(f"OVERLAP: {bbs[i][0][:30]!r} <> {bbs[j][0][:30]!r}")
    for im in ax.images:
        if im.get_zorder() <= 3: continue      # backgrounds (sky/gradient) are fine under text
        ib = im.get_window_extent(r)
        # shrink emoji box to its opaque core (emoji images have transparent margins)
        dx = (ib.x1 - ib.x0) * 0.12; dy = (ib.y1 - ib.y0) * 0.12
        from matplotlib.transforms import Bbox
        ib = Bbox.from_extents(ib.x0 + dx, ib.y0 + dy, ib.x1 - dx, ib.y1 - dy)
        for s, tb in bbs:
            ox = min(ib.x1, tb.x1) - max(ib.x0, tb.x0); oy = min(ib.y1, tb.y1) - max(ib.y0, tb.y0)
            if ox > 5 and oy > 5:
                QA.append(f"IMAGE-ON-TEXT: {s[:30]!r}")

def render(slide, out_path):
    QA.clear()
    fig = plt.figure(figsize=(PXW / 100, PXH / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, UW); ax.set_ylim(0, UH); ax.axis("off")
    sub = slide["ids"][0][:2]; col = SUBCOLORS[sub]
    ax.add_patch(Rectangle((0, 0), UW, UH, fc="#fafafa", ec="none", zorder=0))
    ax.add_patch(Rectangle((0, 18.8), UW, 1.2, fc=col, ec="none", zorder=1))
    ax.add_patch(Rectangle((0, 18.72), UW, 0.1, fc=GOLD, ec="none", zorder=1))
    t = slide["title"]; sz = 24
    while text_w(t, sz, True) > 21 and sz > 14: sz -= 0.5
    T(ax, 0.4, 19.4, t, sz, "white", ha="left")
    subs = list(dict.fromkeys(i[:2] for i in slide["ids"]))
    st = " + ".join(f"{s} {SUBNAMES[s]}" for s in subs)
    s2 = 13
    while text_w(st, s2, True) > 29.2 - 0.4 - text_w(t, sz, True) - 0.6 and s2 > 9: s2 -= 0.5
    T(ax, 29.6, 19.4, st, s2, "#ffffffdd", ha="right")
    SCALES.clear(); SHIFT.clear(); FILL_ON[0] = False
    for it in range(14):
        PANELS.clear(); QA.clear()
        for a_ in list(ax.patches) + list(ax.texts) + list(ax.images) + list(ax.lines) + list(ax.collections):
            a_.remove()
        ax.add_patch(Rectangle((0, 0), UW, UH, fc="#fafafa", ec="none", zorder=0))
        ax.add_patch(Rectangle((0, 18.8), UW, 1.2, fc=col, ec="none", zorder=1))
        ax.add_patch(Rectangle((0, 18.72), UW, 0.1, fc=GOLD, ec="none", zorder=1))
        T(ax, 0.4, 19.4, t, sz, "white", ha="left")
        T(ax, 29.6, 19.4, st, s2, "#ffffffdd", ha="right")
        slide["draw"](ax)
        done = True
        for p in PANELS:
            used = p.y + p.h - p.cursor
            ratio = p.h / max(used, 0.1)
            if 1.0 <= ratio <= 1.07 or (ratio > 1 and p.s >= MAXS):
                continue
            done = False
            SCALES[p.idx] = max(0.6, min(MAXS, p.s * (ratio ** 0.75 if ratio > 1 else ratio ** 1.4)))
        if done:
            break
    def redraw():
        PANELS.clear(); QA.clear()
        for a_ in list(ax.patches) + list(ax.texts) + list(ax.images) + list(ax.lines) + list(ax.collections):
            a_.remove()
        ax.add_patch(Rectangle((0, 0), UW, UH, fc="#fafafa", ec="none", zorder=0))
        ax.add_patch(Rectangle((0, 18.8), UW, 1.2, fc=col, ec="none", zorder=1))
        ax.add_patch(Rectangle((0, 18.72), UW, 0.1, fc=GOLD, ec="none", zorder=1))
        T(ax, 0.4, 19.4, t, sz, "white", ha="left")
        T(ax, 29.6, 19.4, st, s2, "#ffffffdd", ha="right")
        slide["draw"](ax)
    redraw()   # draw with the final scales chosen above
    # shrink-only pass: guarantee nothing overflows
    for it in range(14):
        bad = [p for p in PANELS if p.cursor < p.y - 0.02]
        if not bad:
            break
        for p in bad:
            SCALES[p.idx] = max(0.55, p.s * 0.95)
        redraw()
    # final: let tables stretch into leftover space, then centre what's left
    FREE.clear(); FILL_ROWS.clear()
    for p in PANELS:
        FREE[p.idx] = max(0, p.cursor - p.y)
        FILL_ROWS[p.idx] = max(1, p.fill_rows)
    FILL_ON[0] = True
    redraw()
    again = False
    for p in PANELS:
        free = p.cursor - p.y
        if free > 0.4:
            SHIFT[p.idx] = free / 2; again = True
    if again:
        PANELS.clear(); QA.clear()
        for a_ in list(ax.patches) + list(ax.texts) + list(ax.images) + list(ax.lines) + list(ax.collections):
            a_.remove()
        ax.add_patch(Rectangle((0, 0), UW, UH, fc="#fafafa", ec="none", zorder=0))
        ax.add_patch(Rectangle((0, 18.8), UW, 1.2, fc=col, ec="none", zorder=1))
        ax.add_patch(Rectangle((0, 18.72), UW, 0.1, fc=GOLD, ec="none", zorder=1))
        T(ax, 0.4, 19.4, t, sz, "white", ha="left")
        T(ax, 29.6, 19.4, st, s2, "#ffffffdd", ha="right")
        slide["draw"](ax)
    for p in PANELS:
        free = (p.cursor - p.y + SHIFT.get(p.idx, 0)) / (p.h + P.HEAD)
        if free > 0.22:
            QA.append(f"PANEL-EMPTY {free:.0%} s={p.s:.2f} [{p.title}]")
    ax.set_xlim(0, UW); ax.set_ylim(0, UH)
    mins = min((t_.get_fontsize() for t_ in ax.texts if t_.get_text().strip()), default=99)
    if mins < 10.5:
        small = sorted(set(t_.get_text()[:25] for t_ in ax.texts if t_.get_text().strip() and t_.get_fontsize() < 10.5))[:4]
        QA.append(f"SMALL-FONT {mins:.1f}pt: {small}")
    _qa(fig, ax)
    fig.savefig(out_path, dpi=100, facecolor="white")
    plt.close(fig)
    a = np.asarray(Image.open(out_path).convert("RGB")).astype(int)
    # per-panel emptiness report
    g = a.mean(2); lo = a.min(2)
    for p in PANELS:
        x0 = int(p.x * PPU); x1 = int((p.x + p.w) * PPU); y1 = int(PXH - p.y * PPU); y0 = int(PXH - (p.y + p.h) * PPU)
        n = e = 0
        for yy in range(y0, y1 - 31, 32):
            for xx in range(x0, x1 - 31, 32):
                blk = g[yy:yy + 32, xx:xx + 32]; n += 1
                if blk.std() < 1.5 and lo[yy:yy + 32, xx:xx + 32].mean() > 228: e += 1
        if n and e / n > 0.25:
            QA.append(f"PANEL-SPARSE {e / n:.0%} [{p.title}]")
    return emptiness(a)

def emptiness(a):
    """Fraction of 32x32 tiles with no content (flat colour) and edge density."""
    g = a.mean(2)
    H, Wd = g.shape
    t = 32
    gg = g[:H // t * t, :Wd // t * t].reshape(H // t, t, Wd // t, t)
    lo = a.min(2)[:H // t * t, :Wd // t * t].reshape(H // t, t, Wd // t, t).mean(axis=(1, 3))
    empty = ((gg.std(axis=(1, 3)) < 1.5) & (lo > 228)).mean()   # flat AND near-white = wasted space
    edge = (np.abs(np.diff(g, axis=1)) > 40).mean()
    return empty, edge

# Generates the math study site (math/site) in the same format as ham-radio/site.
# Content = CPM Chapter 7 homework (7-102 .. 7-115): two-way tables, scatterplots,
# line of best fit, slope/rates, solving equations, systems.  ~10 questions per page.
import random, html, math, json, os
from fractions import Fraction as F

OUT = os.path.join(os.path.dirname(__file__), '..', 'site')
E = html.escape
MINUS = '\u2212'

def fr(x):
    x = F(x)
    s = str(abs(x.numerator)) if x.denominator == 1 else f"{abs(x.numerator)}/{x.denominator}"
    return (MINUS if x < 0 else '') + s

def dec(x, nd=2):
    x = round(float(x), nd)
    s = f"{x:.{nd}f}".rstrip('0').rstrip('.')
    if s in ('-0', ''): s = '0'
    return s.replace('-', MINUS)

def money(x):
    x = round(float(x), 2)
    return ('$' + (f"{x:,.0f}" if x == int(x) else f"{x:,.2f}"))

def lin(m, b, x='x', y='y'):
    """pretty y = mx + b"""
    m, b = F(m), F(b)
    if m == 0: t = fr(b)
    else:
        ms = '' if m == 1 else (MINUS if m == -1 else (fr(m) if m.denominator == 1 else f"({fr(m)})"))
        t = f"{ms}{x}"
        if b > 0: t += f" + {fr(b)}"
        elif b < 0: t += f" {MINUS} {fr(-b)}"
    return f"{y} = {t}"

def lind(m, b, x='x', y='y'):
    """y = mx + b with decimals"""
    t = f"{dec(m)}{x}" if m not in (1, -1) else ('' if m == 1 else MINUS) + x
    if b > 0: t += f" + {dec(b)}"
    elif b < 0: t += f" {MINUS} {dec(-b)}"
    return f"{y} = {t}"

def term(a, v='x', first=True):
    a = F(a)
    if a == 0: return ''
    core = (v if abs(a) == 1 else (fr(abs(a)) if a.denominator == 1 else dec(float(abs(a)))) + v) if v else (fr(abs(a)) if a.denominator == 1 else dec(float(abs(a))))
    if first: return (MINUS if a < 0 else '') + core
    return (f" {MINUS} " if a < 0 else ' + ') + core

def expr(*pairs):
    """expr((3,'x'),(4,'')) -> 3x + 4"""
    out = ''
    for a, v in pairs:
        if a == 0: continue
        out += term(a, v, first=(out == ''))
    return out or '0'

def mc(correct, wrongs, rnd, filler=None):
    opts = [correct]
    for w in wrongs:
        if w not in opts and len(opts) < 4: opts.append(w)
    tries = 0
    while len(opts) < 4 and filler and tries < 200:
        c = filler(); tries += 1
        if c not in opts: opts.append(c)
    assert len(opts) == 4, (correct, opts)
    return opts

def numfill(val, rnd, fmt=lambda v: fr(v), spread=None):
    spread = spread or max(2, abs(int(val)) // 4 + 2)
    return lambda: fmt(val + rnd.choice([i for i in range(-spread, spread + 1) if i != 0]))

# ---------------------------------------------------------------- SVG graphs
def svg_plot(points=(), xr=(0, 10), yr=(0, 20), xs=1, ys=2, xl='x', yl='y', lines=(), labels=(), w=360, h=270, gridlbl=None):
    L, R, T, B = 46, 14, 12, 40
    pw, ph = w - L - R, h - T - B
    X = lambda x: L + (x - xr[0]) / (xr[1] - xr[0]) * pw
    Y = lambda y: T + ph - (y - yr[0]) / (yr[1] - yr[0]) * ph
    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;background:#fff">']
    lx = gridlbl[0] if gridlbl else xs
    ly = gridlbl[1] if gridlbl else ys
    k = 0
    v = xr[0]
    while v <= xr[1] + 1e-9:
        s.append(f'<line x1="{X(v):.1f}" y1="{T}" x2="{X(v):.1f}" y2="{T+ph}" stroke="#e3e8ec"/>')
        if abs((v - xr[0]) / lx - round((v - xr[0]) / lx)) < 1e-9:
            s.append(f'<text x="{X(v):.1f}" y="{T+ph+15}" font-size="11" text-anchor="middle" fill="#455a64">{dec(v)}</text>')
        v += xs
    v = yr[0]
    while v <= yr[1] + 1e-9:
        s.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{L+pw}" y2="{Y(v):.1f}" stroke="#e3e8ec"/>')
        if abs((v - yr[0]) / ly - round((v - yr[0]) / ly)) < 1e-9:
            s.append(f'<text x="{L-5}" y="{Y(v)+4:.1f}" font-size="11" text-anchor="end" fill="#455a64">{dec(v)}</text>')
        v += ys
    s.append(f'<line x1="{L}" y1="{T+ph}" x2="{L+pw}" y2="{T+ph}" stroke="#263238" stroke-width="1.6"/>')
    s.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T+ph}" stroke="#263238" stroke-width="1.6"/>')
    s.append(f'<text x="{L+pw/2}" y="{h-6}" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#263238">{E(xl)}</text>')
    s.append(f'<text x="12" y="{T+ph/2}" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#263238" transform="rotate(-90 12 {T+ph/2})">{E(yl)}</text>')
    for (x1, y1, x2, y2, col, lab) in lines:
        s.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" stroke="{col}" stroke-width="3"/>')
        if lab:
            s.append(f'<text x="{X(x2)-4:.1f}" y="{Y(y2)-7:.1f}" font-size="13" font-weight="bold" text-anchor="end" fill="{col}">{E(lab)}</text>')
    for (x, y) in points:
        s.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4.2" fill="#1565c0" stroke="#fff" stroke-width="1"/>')
    s.append('</svg>')
    return ''.join(s)

def table_html(head, rows):
    t = '<table class="tw"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>'
    for r in rows:
        t += '<tr>' + ''.join((f'<th>{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(r)) + '</tr>'
    return t + '</table>'

def Q(qt, opts, why='', fig=None, ref=''):
    return dict(qt=qt, opts=opts, why=why, fig=fig, ref=ref)

def uniq(gen, n=10, rnd=None):
    out, seen, tries = [], set(), 0
    while len(out) < n and tries < 500:
        q = gen(len(out)); tries += 1
        key = q['qt'] + (q['fig'] or '')
        if key in seen: continue
        seen.add(key); out.append(q)
    return out

# ================================================================ PAGES
PAGES = []
def page(sec, title, tip, kw, ex=''):
    def deco(fn):
        PAGES.append(dict(sec=sec, title=title, tip=tip, kw=kw, ex=ex, fn=fn)); return fn
    return deco

SECTIONS = {
    'A': ('A \u2013 Two-way tables & association', '#1565c0'),
    'B': ('B \u2013 Scatterplots & graphs', '#00838f'),
    'C': ('C \u2013 Line of best fit', '#6a1b9a'),
    'D': ('D \u2013 Rates, proportions & slope', '#ef6c00'),
    'E': ('E \u2013 Solving equations (Checkpoint 7)', '#2e7d32'),
    'F': ('F \u2013 Systems of equations', '#c62828'),
}

# ---------- A1
TW_CTX = [
    ('Owns a pet', 'Grade 7', 'Grade 8'), ('Plays a sport', 'Boys', 'Girls'), ('Likes pizza best', '6th grade', '7th grade'),
    ('Walks to school', 'Lives in town', 'Lives outside town'), ('Has a phone', 'Age 11', 'Age 12'),
    ('Reads every night', 'Morning class', 'Afternoon class'), ('Takes the bus', 'North School', 'South School'),
    ('Plays an instrument', 'Band class', 'Art class'),
]
@page('A', 'Completing two-way tables (row & column totals)',
      'Row total = add across. Column total = add down. Missing cell = total \u2212 the other cell.',
      [('Two-way table', 'A table that sorts data by two categories at once (one along the rows, one along the columns).'),
       ('Row total', 'Add every cell across a row.'), ('Column total', 'Add every cell down a column.'),
       ('Grand total', 'Bottom-right corner: the total of everything. Row totals and column totals both add up to it.'),
       ('Missing cell', 'Subtract: total \u2212 the known cell.')],
      'HW 7-110: Highly fuel-efficient trucks 392 + ordinary cars 36,929 = <b>37,321</b> vehicles bought in that column.')
def A1(rnd):
    def g(i):
        cat, c1, c2 = rnd.choice(TW_CTX)
        a, b, c, d = [rnd.randint(8, 95) for _ in range(4)]
        r1, r2, k1, k2, T = a + b, c + d, a + c, b + d, a + b + c + d
        kind = i % 5
        head = ['', c1, c2, 'Total']
        rows = [[f'{cat}: Yes', a, b, r1], [f'{cat}: No', c, d, r2], ['Total', k1, k2, T]]
        if kind == 0:
            rows[0][1] = '?'; ans, wr = a, [r1 + b, b, k1 + c]
            why = f'Row total \u2212 other cell = {r1} \u2212 {b} = {a}.'
        elif kind == 1:
            rows[1][3] = '?'; rows[2][3] = '?'; ans, wr = r2, [c * d // max(1, c) + c + 1 if c + d + 1 != r2 else r2 + 2, abs(c - d), r1]
            why = f'Add across the row: {c} + {d} = {r2}.'
        elif kind == 2:
            rows[2][2] = '?'; rows[2][3] = '?'; ans, wr = k2, [a + b, abs(b - d), k2 + 10]
            why = f'Add down the column: {b} + {d} = {k2}.'
        elif kind == 3:
            rows[2][3] = '?'; ans, wr = T, [r1 + k1, T - 10, r1 + r2 + k1]
            why = f'Grand total = {r1} + {r2} = {T} (or {k1} + {k2}).'
        else:
            rows[1][2] = '?'; rows[1][3] = '?'; ans, wr = d, [k2 + b, c, k2 - a]
            why = f'Column total \u2212 other cell = {k2} \u2212 {b} = {d}.'
        wr = [x for x in wr if x != ans and x > 0]
        return Q('What number belongs in the cell marked <b>?</b>',
                 mc(str(ans), [str(x) for x in wr], rnd, numfill(ans, rnd, str, 9)), why, table_html(head, rows))
    qs = uniq(g, 10)
    for q in qs:  # fix wording for tables with two '?'
        if q['fig'].count('>?<') == 2:
            q['qt'] = 'What number belongs in the <b>first</b> cell marked <b>?</b> (reading left to right, top to bottom)?'
    return qs

# ---------- A2
VARS = [
    ('fuel prices', 'number of fuel-efficient trucks bought', 'the color of the trucks', 'the name of the car dealer',
     'Do gasoline prices change how many fuel-efficient trucks people buy?'),
    ('hours of sleep', 'number of items remembered', 'the students\u2019 grade level', 'the day of the week',
     'Does the amount of sleep change how many items a student remembers?'),
    ('age (years)', 'height (inches)', 'favorite food', 'family last name',
     'At a family reunion, each person recorded age and height.'),
    ('age of the car', 'miles per gallon', 'color of the car', 'number of doors',
     'Marissa wants to show that newer cars get better gas mileage.'),
    ('hours spent studying', 'test score', 'the teacher\u2019s name', 'the room number',
     'Does studying longer lead to higher test scores?'),
    ('temperature outside', 'number of ice cream cones sold', 'the flavor list', 'the shop\u2019s address',
     'An ice cream shop records the daily temperature and the cones it sells.'),
    ('number of months saving', 'total amount saved', 'name of the bank', 'the saver\u2019s age',
     'Liz puts the same amount in the bank each month.'),
    ('amount of fertilizer', 'height of the plant', 'shape of the pot', 'name of the plant',
     'A science class tests how fertilizer affects plant growth.'),
    ('ticket price', 'number of tickets sold', 'the movie\u2019s title', 'the seat color',
     'A theater changes its ticket price and counts how many tickets it sells.'),
    ('number of hops', 'distance traveled (feet)', 'size of shoes', 'hallway color',
     'Malcolm counts his hops and measures how far he goes.'),
    ('time spent playing video games', 'time spent studying', 'type of game console', 'number of siblings',
     'Ruthie surveyed classmates about video games and studying.'),
    ('number of people at a party', 'number of pizzas needed', 'party theme', 'day of the party',
     'A host plans how much pizza to order.'),
]
@page('A', 'Independent & dependent variables',
      'Independent = the cause (x-axis, the one you change). Dependent = the result (y-axis, it "depends" on x).',
      [('Independent variable', 'The input or cause. Goes on the x-axis (horizontal).'),
       ('Dependent variable', 'The output or result. Its value depends on the independent variable. Goes on the y-axis.'),
       ('Association', 'A relationship: when one variable changes, the other tends to change too.'),
       ('Trick question?', 'Ask yourself: "Does A change B, or does B change A?" The one doing the changing is independent.')],
      'HW 7-110a: "What is the independent variable?" \u2192 <b>fuel prices</b>. They affect how many fuel-efficient trucks are bought.')
def A2(rnd):
    out = []
    pool = VARS[:]; rnd.shuffle(pool)
    for i, (ind, dep, d1, d2, sc) in enumerate(pool[:10]):
        ask_ind = i % 2 == 0
        corr = ind if ask_ind else dep
        other = dep if ask_ind else ind
        opts = mc(corr, [other, d1, d2], rnd)
        out.append(Q(f'{E(sc)} Which is the <b>{"independent" if ask_ind else "dependent"}</b> variable?', [E(o) for o in opts],
                     f'The {ind} affects the {dep}, so <b>{ind}</b> is independent (x) and <b>{dep}</b> is dependent (y).'))
    return out

# ---------- A3
RF_CTX = [
    ('students who slept less than 7 hours', 'remembered all 10 items'),
    ('students in the band', 'also play a sport'),
    ('customers who bought a truck', 'chose a hybrid'),
    ('7th graders surveyed', 'have a pet dog'),
    ('people at the game', 'bought a snack'),
    ('students who ride the bus', 'arrive before 8:00'),
    ('cars in the parking lot', 'are electric'),
    ('kids at summer camp', 'can swim'),
]
@page('A', 'Relative frequency (percent of a row)',
      'Relative frequency = part \u00f7 row total \u00d7 100. Divide by the total of THAT row, not the grand total!',
      [('Relative frequency', 'A count turned into a percent (or fraction) of a total.'),
       ('Row relative frequency', 'Divide each cell by its row total. Each row then adds up to 100%.'),
       ('Percent', 'part \u00f7 whole \u00d7 100'), ('Rounding', '3.8709...% to the nearest hundredth is 3.87%.')],
      'HW 7-111: 6 of the 155 students who slept less than 7 hours remembered all 10 items: 6 \u00f7 155 = 0.0387 \u2192 <b>3.87%</b>.')
def A3(rnd):
    def g(i):
        grp, trait = rnd.choice(RF_CTX)
        tot = rnd.choice([20, 25, 40, 50, 80, 120, 155, 160, 200, 250, 300])
        part = rnd.randint(2, tot - 2)
        if i < 5:
            p = part / tot * 100
            ans = dec(p, 1) + '%'
            wr = [dec(100 - p, 1) + '%', dec(part / (tot + rnd.randint(30, 90)) * 100, 1) + '%', dec(part, 1) + '%']
            return Q(f'Out of {tot} {E(grp)}, {part} {E(trait)}. What percent {E(trait)}? (Round to the nearest tenth.)',
                     mc(ans, wr, rnd, lambda: dec(p + rnd.choice([-5, -3, 3, 5]) + rnd.random(), 1) + '%'),
                     f'{part} \u00f7 {tot} \u00d7 100 \u2248 {ans}.')
        else:
            pct = rnd.choice([10, 20, 25, 30, 40, 60, 75, 80, 5, 15])
            tot = rnd.choice([t for t in [20, 40, 60, 80, 100, 120, 200, 240, 300, 400] if t * pct % 100 == 0])
            part = tot * pct // 100
            return Q(f'In a relative frequency table, {pct}% of the {tot} {E(grp)} {E(trait)}. How many is that?',
                     mc(str(part), [str(tot - part), str(pct), str(tot // pct if pct else 1)], rnd, numfill(part, rnd, str, 6)),
                     f'{pct}% of {tot} = {pct/100} \u00d7 {tot} = {part}.')
    return uniq(g, 10)

# ---------- A4
ASSOC_CTX = [
    ('students who play a sport', 'students who do not play a sport', 'eat breakfast every day'),
    ('high fuel prices', 'low fuel prices', 'bought a highly fuel-efficient truck'),
    ('people who exercise', 'people who do not exercise', 'sleep 8+ hours'),
    ('students with a phone', 'students without a phone', 'finish homework on time'),
    ('kids who read daily', 'kids who rarely read', 'scored above 80 on the test'),
    ('customers on weekdays', 'customers on weekends', 'ordered dessert'),
    ('dog owners', 'cat owners', 'walk 30+ minutes a day'),
]
YES_A = 'Yes. The percents are very different, so there is an association.'
NO_A = 'No. The percents are about the same, so there is no association.'
WRONG_A = ['Yes, because the two groups have different totals.', 'No, because you can never tell from percents.',
           'Yes, because any difference at all means an association.', 'No, because the bigger group always wins.']
@page('A', 'Is there an association? (compare the percents)',
      'Compare the ROW PERCENTS, not the raw counts. Big difference \u2192 association. About the same \u2192 no association.',
      [('Association (categorical)', 'The percent with a trait is clearly different between the groups.'),
       ('No association', 'The percents are close (for example 1.05% vs 1.04%).'),
       ('Why percents?', 'Groups have different sizes, so raw counts can fool you.')],
      'HW 7-110b: 1.05% vs 1.04% of buyers chose highly fuel-efficient trucks \u2192 almost the same \u2192 <b>no association</b> between fuel prices and buying them.')
def A4(rnd):
    def g(i):
        g1, g2, tr = rnd.choice(ASSOC_CTX)
        p1 = rnd.randint(10, 85)
        if i % 2 == 0:
            p2 = p1 + rnd.choice([-1, 1]) * rnd.randint(25, 40)
            if not 2 <= p2 <= 98: p2 = p1 + 30 if p1 < 60 else p1 - 30
            corr = YES_A
        else:
            p2 = p1 + rnd.choice([-2, -1, 0, 1, 2]) + rnd.choice([0.0, 0.3, 0.6])
            corr = NO_A
        other = NO_A if corr == YES_A else YES_A
        opts = mc(corr, [other] + rnd.sample(WRONG_A, 2), rnd)
        return Q(f'{dec(p1,1)}% of {E(g1)} {E(tr)}, but {dec(p2,1)}% of {E(g2)} {E(tr)}. Is there an association?', opts,
                 f'The difference is {dec(abs(p1-p2),1)} percentage points: ' + ('large \u2192 association.' if corr == YES_A else 'tiny \u2192 no association.'))
    return uniq(g, 10)

# ---------- A5  (homework data)
SLEEP = table_html(['Hours of sleep', 'Remembered all 10: No', 'Yes', 'Total'],
                   [['Less than 7', 149, 6, 155], ['7\u20139', 109, 11, 120], ['At least 10', 20, 5, 25], ['Total', 278, 22, 300]])
FUEL = table_html(['', 'High fuel prices', 'Low fuel prices', 'Total'],
                  [['Highly fuel-efficient trucks', 392, 442, '?'], ['Ordinary cars & regular trucks', '36,929', '42,255', '?'], ['Total', '?', '?', '?']])
@page('A', 'Homework practice: sleep study & fuel prices (7-110, 7-111)',
      'Same steps every time: complete totals \u2192 divide by row/column total \u2192 compare the percents.',
      [('Step 1', 'Fill in all row and column totals.'), ('Step 2', 'Make a relative frequency table: cell \u00f7 its total.'),
       ('Step 3', 'Compare percents between groups to decide on association.'),
       ('Conclusion sentence', '"Students who sleep more are more likely to remember all 10 items."')],
      'HW 7-111: Yes% goes 3.87% \u2192 9.17% \u2192 20% as sleep increases. The percents are very different, so there <b>is</b> an association.')
def A5(rnd):
    S, Fu = SLEEP, FUEL
    L = [
        Q('Sleep study: what percent of students who slept <b>less than 7 hours</b> remembered all 10 items?', ['3.87%', '96.13%', '2.00%', '27.27%'], '6 \u00f7 155 \u2248 0.0387 = 3.87%.', S),
        Q('Sleep study: what percent of students who slept <b>7\u20139 hours</b> remembered all 10 items?', ['9.17%', '90.83%', '3.67%', '50.00%'], '11 \u00f7 120 \u2248 9.17%.', S),
        Q('Sleep study: what percent of students who slept <b>at least 10 hours</b> remembered all 10 items?', ['20%', '80%', '5%', '22.73%'], '5 \u00f7 25 = 20%.', S),
        Q('Sleep study: what is the <b>independent</b> variable?', ['Hours of sleep', 'Whether all 10 items were remembered', 'The 300 students', 'The 10 objects'], 'Sleep is the possible cause, so it is independent.', S),
        Q('Sleep study: is there an association between hours of sleep and memory?', ['Yes. The more sleep, the higher the percent who remembered all 10.', 'No. Most students in every group said No.', 'No. The groups have different totals.', 'Yes. More students slept less than 7 hours.'], '3.87% \u2192 9.17% \u2192 20%: a big change \u2192 association.', S),
        Q('Sleep study: what percent of <b>all 300</b> students remembered all 10 items?', ['7.33%', '22%', '92.67%', '3.87%'], '22 \u00f7 300 \u2248 7.33%.', S),
        Q('Fuel study: what is the column total for <b>high fuel prices</b>?', ['37,321', '36,537', '834', '42,697'], '392 + 36,929 = 37,321.', Fu),
        Q('Fuel study: what is the <b>grand total</b> of all vehicles purchased?', ['80,018', '79,184', '37,321', '834'], '37,321 + 42,697 = 80,018.', Fu),
        Q('Fuel study: during high fuel prices, what percent of purchases were highly fuel-efficient trucks?', ['1.05%', '0.49%', '98.95%', '47.0%'], '392 \u00f7 37,321 \u2248 1.05%.', Fu),
        Q('Fuel study: 1.05% (high prices) vs 1.04% (low prices) bought highly fuel-efficient trucks. Is there an association?', ['No. The percents are almost the same.', 'Yes. 442 is more than 392.', 'Yes. Prices always change what people buy.', 'No. The table is too big to tell.'], 'Comparing percents, not counts: 1.05% \u2248 1.04% \u2192 no association.', Fu),
    ]
    return L

# ---------- B1  scatter direction
def scatter(rnd, kind, n=12, noise=1.2, xr=(0, 10), yr=(0, 20)):
    pts = []
    xs = sorted(rnd.sample(range(xr[0], xr[1] + 1), min(n, xr[1] - xr[0] + 1)) + [rnd.randint(xr[0], xr[1]) for _ in range(max(0, n - (xr[1] - xr[0] + 1)))])
    for x in xs:
        t = (x - xr[0]) / (xr[1] - xr[0])
        if kind == 'pos': y = 2 + 15 * t
        elif kind == 'neg': y = 18 - 15 * t
        elif kind == 'curve_neg': y = 2 + 16 * (1 - t) ** 2.6
        elif kind == 'curve_pos': y = 2 + 16 * t ** 2.6
        elif kind == 'hump': y = 3 + 15 * (1 - (2 * t - 1) ** 2)
        else: y = rnd.uniform(2, 18)
        y += rnd.gauss(0, noise) if kind != 'none' else 0
        pts.append((x + rnd.choice([0, 0.25, -0.25]), max(0.5, min(19.5, y))))
    return pts
SC_CTX = [('Hours studied', 'Test score'), ('Age (years)', 'Height'), ('Car age (years)', 'Miles per gallon'),
          ('Video game time', 'Study time'), ('Temperature', 'Cones sold'), ('Shoe size', 'Math grade'),
          ('Practice hours', 'Free throws made'), ('Days absent', 'Grade')]
DIR = {'pos': 'Positive association', 'neg': 'Negative association', 'none': 'No association'}
@page('B', 'Scatterplots: positive, negative or none?',
      'Read left to right. Points go UP \u2192 positive. Points go DOWN \u2192 negative. A random cloud \u2192 no association.',
      [('Scatterplot', 'A graph of (x, y) points showing how two numeric variables relate.'),
       ('Positive association', 'As x increases, y tends to increase.'),
       ('Negative association', 'As x increases, y tends to decrease.'),
       ('No association', 'No up or down pattern: the points look scattered randomly.')],
      'HW 7-112: As time playing video games increases, time spent studying <b>decreases</b> \u2192 negative association.')
def B1(rnd):
    def g(i):
        k = ['pos', 'neg', 'none'][i % 3]
        xl, yl = rnd.choice(SC_CTX)
        pts = scatter(rnd, k, n=rnd.randint(10, 14), noise=rnd.choice([0.8, 1.5, 2.2]))
        return Q('What kind of association does this scatterplot show?',
                 mc(DIR[k], [v for kk, v in DIR.items() if kk != k] + ['Both positive and negative at the same time'], rnd),
                 {'pos': 'The points rise from left to right.', 'neg': 'The points fall from left to right.', 'none': 'No clear up/down trend.'}[k],
                 svg_plot(pts, xl=xl, yl=yl, xs=1, ys=2, gridlbl=(2, 4)))
    return uniq(g, 10)

# ---------- B2 form & strength
FORMS = {'spl': ('Strong, positive, linear', 'pos', 0.6), 'wpl': ('Weak, positive, linear', 'pos', 3.0),
         'snl': ('Strong, negative, linear', 'neg', 0.6), 'wnl': ('Weak, negative, linear', 'neg', 3.0),
         'nln': ('Negative, nonlinear (curved)', 'curve_neg', 0.5), 'nlp': ('Positive, nonlinear (curved)', 'curve_pos', 0.5)}
@page('B', 'Describe it fully: form, direction, strength, outliers',
      'Say all 4 things: FORM (linear or curved), DIRECTION (+ or \u2212), STRENGTH (tight or spread out), OUTLIERS.',
      [('Form', 'Linear (along a straight line) or nonlinear (curved).'),
       ('Direction', 'Positive or negative.'),
       ('Strength', 'Strong = points close to the trend. Weak = points spread far from it.'),
       ('Outlier', 'A point far away from the pattern of the others.')],
      'HW 7-112a: "As time spent playing video games increases, time spent studying decreases": <b>nonlinear, negative</b>.')
def B2(rnd):
    keys = list(FORMS)
    def g(i):
        k = keys[i % len(keys)]
        name, kind, noise = FORMS[k]
        xl, yl = rnd.choice(SC_CTX)
        pts = scatter(rnd, kind, n=14, noise=noise)
        wr = [FORMS[x][0] for x in rnd.sample([x for x in keys if x != k], 3)]
        return Q('Which description fits this scatterplot best?', mc(name, wr, rnd),
                 f'{name}: ' + ('the points hug a straight line.' if noise < 1 and 'linear' in name and 'non' not in name else 'they spread out from the line.' if 'Weak' in name else 'the pattern bends instead of following a straight line.'),
                 svg_plot(pts, xl=xl, yl=yl, xs=1, ys=2, gridlbl=(2, 4)))
    return uniq(g, 10)

# ---------- B3 outliers
@page('B', 'Finding outliers on a scatterplot',
      'An outlier sits far away from the trend of the other points. Name it with an ordered pair (x, y): x first!',
      [('Outlier', 'A data point far from the overall pattern.'),
       ('Ordered pair', '(x, y): go across to x, then up to y.'),
       ('Effect', 'Outliers can pull a line of best fit away from the rest of the data.')],
      'HW 7-112b: Ruthie\u2019s scatterplot had an outlier at about <b>(100, 140)</b>: lots of gaming AND lots of studying.')
def B3(rnd):
    def g(i):
        m = rnd.choice([1, 2, -1, -2, 1.5, -1.5])
        b = 2 if m > 0 else 19
        xs = sorted(rnd.sample(range(0, 11), 9))
        pts = []
        for x in xs:
            y = round(b + m * x + rnd.choice([-1, 0, 0, 1]))
            if 0 <= y <= 20: pts.append((x, y))
        while True:
            ox = rnd.randint(1, 9); oy = rnd.randint(1, 19)
            if abs(oy - (b + m * ox)) >= 9 and all(p[0] != ox for p in pts): break
        allp = pts + [(ox, oy)]
        corr = f'({ox}, {oy})'
        wr = [f'({x}, {y})' for (x, y) in rnd.sample(pts, 2)] + [f'({oy}, {ox})']
        return Q('Which point is an <b>outlier</b>?', mc(corr, wr, rnd),
                 f'All the other points follow the trend; ({ox}, {oy}) is far from it. (Remember: x first, then y.)',
                 svg_plot(allp, xr=(0, 10), yr=(0, 20), xl='x', yl='y', xs=1, ys=1, gridlbl=(1, 2)))
    return uniq(g, 10)

# ---------- B4 association in words
@page('B', 'Association in words (real situations)',
      'Turn "as ___ increases, ___ increases/decreases" into positive/negative.',
      [('"Both go up"', 'Positive association.'), ('"One goes up, the other goes down"', 'Negative association.'),
       ('"No pattern"', 'No association.'), ('Association \u2260 causation', 'Two things can be related without one causing the other.')],
      'HW 7-102: Family reunion \u2192 "positive, linear: as age increases, height increases" (for kids; adults level off).')
def B4(rnd):
    items = [
        ('As a car gets older, its miles per gallon tends to go down.', 'neg'),
        ('As children get older, they tend to get taller.', 'pos'),
        ('The more hours students sleep, the more items they remember.', 'pos'),
        ('The more time spent playing video games, the less time spent studying.', 'neg'),
        ('A person\u2019s shoe size and their favorite number.', 'none'),
        ('As the temperature rises, more ice cream cones are sold.', 'pos'),
        ('The more absences a student has, the lower their grade tends to be.', 'neg'),
        ('The month you were born and how fast you can run.', 'none'),
        ('As ticket prices go up, fewer tickets are sold.', 'neg'),
        ('The more months Liz saves, the more money she has.', 'pos'),
        ('Height of a student and the number of letters in their name.', 'none'),
        ('As the number of workers increases, the time to finish the job decreases.', 'neg'),
    ]
    rnd.shuffle(items)
    out = []
    for s, k in items[:10]:
        out.append(Q(f'\u201c{E(s)}\u201d What association is this?', mc(DIR[k], [v for kk, v in DIR.items() if kk != k] + ['It depends on the outliers only'], rnd),
                     {'pos': 'Both increase together \u2192 positive.', 'neg': 'One increases while the other decreases \u2192 negative.', 'none': 'No reason for a pattern \u2192 no association.'}[k]))
    return out

# ---------- B5 choose display
@page('B', 'Choosing the right graph',
      'ONE numeric variable \u2192 histogram / box plot / dot plot. TWO numeric variables \u2192 scatterplot. TWO categories \u2192 two-way table.',
      [('Histogram', 'Bars showing how many data values fall in each interval.'),
       ('Box plot', 'Shows median, quartiles, and range; great for "typical" value and spread.'),
       ('Dot plot', 'A dot for each value above a number line.'),
       ('Scatterplot', 'Shows the relationship between two numeric variables.'),
       ('Two-way table', 'Compares two categorical variables.')],
      'HW 7-103: Typical age of cars \u2192 <b>box plot or histogram</b>. Newer cars more fuel-efficient? \u2192 <b>scatterplot</b> (age vs mpg).')
def B5(rnd):
    D = ['Box plot', 'Histogram', 'Scatterplot', 'Two-way table', 'Dot plot', 'Circle graph']
    items = [
        ('Marissa wants to know the <b>typical age</b> of her friends\u2019 cars (and the spread).', 'Box plot', ['Scatterplot', 'Two-way table', 'Circle graph']),
        ('Marissa wants to show her dad that <b>newer cars get more miles per gallon</b>.', 'Scatterplot', ['Box plot', 'Histogram', 'Dot plot']),
        ('Is there an association between <b>grade level (6th/7th/8th)</b> and <b>favorite sport</b>?', 'Two-way table', ['Scatterplot', 'Box plot', 'Dot plot']),
        ('Show how many students scored 60\u201369, 70\u201379, 80\u201389, 90\u201399.', 'Histogram', ['Scatterplot', 'Two-way table', 'Circle graph']),
        ('Show each of 15 quiz scores as its own mark above a number line.', 'Dot plot', ['Scatterplot', 'Two-way table', 'Circle graph']),
        ('See if <b>hours of practice</b> is related to <b>free throws made</b>.', 'Scatterplot', ['Histogram', 'Circle graph', 'Box plot']),
        ('Quickly find the <b>median and quartiles</b> of 40 heights.', 'Box plot', ['Scatterplot', 'Two-way table', 'Circle graph']),
        ('Compare whether <b>boys and girls</b> differ in <b>owning a pet (yes/no)</b>.', 'Two-way table', ['Scatterplot', 'Histogram', 'Dot plot']),
        ('Decide whether a <b>line of best fit</b> makes sense for age vs. height data.', 'Scatterplot', ['Box plot', 'Histogram', 'Circle graph']),
        ('Show what <b>fraction of the class</b> picked each lunch choice (parts of a whole).', 'Circle graph', ['Scatterplot', 'Box plot', 'Histogram']),
    ]
    return [Q(f'{s} Which display is best?', mc(c, w, rnd),
              {'Box plot': 'One numeric variable, focus on center & spread \u2192 box plot.', 'Histogram': 'Counts in intervals \u2192 histogram.',
               'Scatterplot': 'Two numeric variables together \u2192 scatterplot.', 'Two-way table': 'Two categorical variables \u2192 two-way table.',
               'Dot plot': 'Each value as a dot on a number line \u2192 dot plot.', 'Circle graph': 'Parts of a whole \u2192 circle graph.'}[c]) for s, c, w in items]

# ---------- C1 line through two points
@page('C', 'Equation of a line from two points',
      'slope m = (y\u2082 \u2212 y\u2081) \u00f7 (x\u2082 \u2212 x\u2081). Then b = y \u2212 m\u00b7x. Write y = mx + b.',
      [('Slope (m)', 'Rise over run: change in y \u00f7 change in x.'), ('y-intercept (b)', 'Where the line crosses the y-axis (x = 0).'),
       ('Slope-intercept form', 'y = mx + b'), ('Line of best fit', 'A line drawn through the middle of scatterplot data to show its trend.')],
      'Through (2, 9) and (6, 17): m = (17\u22129)/(6\u22122) = 8/4 = <b>2</b>; b = 9 \u2212 2\u00b72 = <b>5</b> \u2192 y = 2x + 5.')
def C1(rnd):
    def g(i):
        m = F(rnd.choice([1, 2, 3, 4, -1, -2, -3, 5])) if i < 7 else F(rnd.choice([1, -1, 3, -3]), 2)
        b = F(rnd.randint(-8, 12))
        x1 = rnd.randint(-3, 3) * (m.denominator); x2 = x1 + rnd.choice([2, 4]) * m.denominator
        y1, y2 = m * x1 + b, m * x2 + b
        corr = lin(m, b)
        wr = [lin(-m, b), lin(1 / m if m else 1, b), lin(m, y1 if y1 != b else b + 1)]
        return Q(f'Which equation is the line through ({fr(x1)}, {fr(y1)}) and ({fr(x2)}, {fr(y2)})?', mc(corr, wr, rnd, lambda: lin(m, b + rnd.choice([-3, -2, 2, 3]))),
                 f'm = ({fr(y2)} \u2212 {fr(y1)}) \u00f7 ({fr(x2)} \u2212 {fr(x1)}) = {fr(m)}; b = {fr(y1)} \u2212 {fr(m)}\u00b7{fr(x1)} = {fr(b)}.')
    return uniq(g, 10)

# ---------- C2 predictions
PRED = [('hours studied', 'test score', 'points', 6.5, 52, (2, 6)), ('age in years (kids)', 'height in inches', 'inches', 2.5, 30, (4, 12)),
        ('car age in years', 'miles per gallon', 'mpg', -0.7, 35.9, (3, 15)), ('temperature (\u00b0F)', 'cones sold', 'cones', 3, -120, (60, 95)),
        ('months saved', 'dollars in the bank', 'dollars', 30, 40, (3, 12)), ('practice hours', 'free throws made (out of 50)', 'free throws', 1.5, 18, (4, 16)),
        ('days absent', 'grade (%)', '%', -2.5, 94, (2, 10))]
@page('C', 'Making predictions with a line of best fit',
      'Plug the x-value into the equation. Multiply first, then add b.',
      [('Prediction', 'Use y = mx + b: substitute x, then compute y.'), ('Interpolation', 'Predicting inside the data range: usually reliable.'),
       ('Extrapolation', 'Predicting far outside the data: risky!'), ('Order of operations', 'Multiply m\u00b7x before adding b.')],
      'HW 7-103f: y = \u22120.7x + 35.9 for a 7-year-old car: \u22120.7(7) + 35.9 = \u22124.9 + 35.9 = <b>31 mpg</b>.')
def C2(rnd):
    def g(i):
        xl, yl, u, m, b, (lo, hi) = rnd.choice(PRED)
        x = rnd.randint(lo, hi)
        y = m * x + b
        wr = [dec(m * x), dec(m + x + b), dec(b - m * x) if m > 0 else dec(m * x - b), dec((x + b) * m)]
        return Q(f'A line of best fit for <i>{E(xl)}</i> (x) vs. <i>{E(yl)}</i> (y) is <b>{lind(m, b)}</b>. Predict y when x = {x}.',
                 mc(dec(y), wr, rnd, lambda: dec(y + rnd.choice([-4, -2, 2, 4, 1.5]))),
                 f'y = {dec(m)}({x}) + {dec(b)} = {dec(m*x)} + {dec(b)} = {dec(y)} {E(u)}.'.replace('+ -', f'{MINUS} ').replace('-', MINUS))
    return uniq(g, 10)

# ---------- C3 slope meaning
SL = [('the number of months', 'dollars saved', 30, 50, 'Liz saves $30 each month', 'month', 'dollars'),
      ('the age of the car (years)', 'miles per gallon', -0.7, 35.9, None, 'year', 'miles per gallon'),
      ('hours studied', 'test score', 6, 55, None, 'hour', 'points'),
      ('age (years)', 'height (inches)', 2.5, 30, None, 'year', 'inches'),
      ('number of hops', 'feet traveled', 1.2, 0, None, 'hop', 'feet'),
      ('minutes of video games', 'minutes studying', -0.5, 140, None, 'minute', 'minutes'),
      ('number of tickets sold', 'money raised ($)', 8, -150, None, 'ticket', 'dollars'),
      ('hours worked', 'pay earned ($)', 15, 0, None, 'hour', 'dollars'),
      ('weeks', 'plant height (cm)', 1.8, 4, None, 'week', 'cm'),
      ('days', 'water in tank (gallons)', -12, 400, None, 'day', 'gallons')]
@page('C', 'What does the slope mean?',
      'Slope sentence: "For each additional 1 [x-unit], the [y] goes up/down by [m] [y-units]."',
      [('Slope = rate of change', 'How much y changes when x goes up by 1.'), ('Positive slope', 'y increases as x increases.'),
       ('Negative slope', 'y decreases as x increases.'), ('Units', 'Slope units are "y-units per x-unit" (e.g. mpg per year).')],
      'HW 7-103g: slope \u22120.7 \u2192 "For each year older, a car gets about <b>0.7 fewer miles per gallon</b>."')
def C3(rnd):
    out = []
    for xl, yl, m, b, _, xu, yu in SL:
        d = 'increases' if m > 0 else 'decreases'
        corr = f'For each 1 {xu} increase, {yl} {d} by {dec(abs(m))} {yu}.'
        wr = [f'When {xl} is 0, {yl} is {dec(b)}.', f'For each 1 {xu} increase, {yl} {"decreases" if m > 0 else "increases"} by {dec(abs(m))} {yu}.',
              f'For each 1 {yu} increase, {xl} increases by {dec(abs(m))}.']
        out.append(Q(f'x = {E(xl)}, y = {E(yl)}. Line: <b>{lind(m, b)}</b>. What does the <b>slope</b> mean?', [E(o) for o in mc(corr, wr, rnd)],
                     f'The slope is {dec(m)}: the change in y for each +1 in x.'))
    return out

# ---------- C4 y-intercept meaning / sense
YI = [('age (years)', 'height (inches)', 2.5, 20, True, 'A newborn is about 20 inches long, so yes, it makes sense.'),
      ('age of car (years)', 'miles per gallon', -0.7, 35.9, True, 'A brand-new car (age 0) gets about 35.9 mpg: makes sense.'),
      ('months', 'dollars saved', 30, 50, True, 'She started with $50 before saving: makes sense.'),
      ('temperature (\u00b0F)', 'cones sold', 3, -120, False, 'You can\u2019t sell \u2212120 cones, so it does NOT make sense.'),
      ('hours studied', 'test score', 6, 55, True, 'Studying 0 hours could still give a score of 55: makes sense.'),
      ('height (inches)', 'shoe size', 0.4, -18, False, 'Nobody is 0 inches tall and shoe size can\u2019t be \u221218: does NOT make sense.'),
      ('number of hops', 'feet traveled', 1.2, 0, True, '0 hops \u2192 0 feet: makes sense.'),
      ('days', 'water in tank (gallons)', -12, 400, True, 'The tank started with 400 gallons: makes sense.'),
      ('years of experience', 'hourly pay ($)', 1.5, 12, True, 'Starting pay with no experience is $12: makes sense.'),
      ('weight of dog (lb)', 'food per day (cups)', 0.05, -0.5, False, 'A 0 lb dog eating \u22120.5 cups does NOT make sense.')]
@page('C', 'What does the y-intercept mean? Does it make sense?',
      'The y-intercept is the y-value when x = 0. Ask: "Does x = 0 even make sense here?"',
      [('y-intercept', 'The starting value: y when x = 0.'), ('Makes sense?', 'Check if x = 0 is possible AND the y-value is realistic.'),
       ('Negative intercept', 'Often impossible in real life (negative cones, negative height).'),
       ('Extrapolation', 'x = 0 may be far outside the data, so the model may break down.')],
      'HW 7-102: age vs height: the y-intercept is the height at age 0 (a baby\u2019s length). It makes sense if it is around 20 inches.')
def C4(rnd):
    out = []
    for i, (xl, yl, m, b, ok, why) in enumerate(YI):
        if i % 2 == 0:
            corr = f'When {xl.split(" (")[0]} is 0, {yl} is {dec(b)}.'
            wr = [f'For each 1 unit of {xl.split(" (")[0]}, {yl} changes by {dec(b)}.', f'When {yl.split(" (")[0]} is 0, {xl} is {dec(b)}.',
                  f'{yl.capitalize()} changes by {dec(m)} each unit.']
            out.append(Q(f'x = {E(xl)}, y = {E(yl)}. Line: <b>{lind(m, b)}</b>. What does the y-intercept mean?', [E(o) for o in mc(corr, wr, rnd)], E(why)))
        else:
            corr = ('Yes. ' if ok else 'No. ') + why.split(':')[0].split(', so')[0]
            Y = 'Yes, it is a reasonable starting value.'; N = 'No, it is not a realistic value at x = 0.'
            corr = Y if ok else N
            out.append(Q(f'x = {E(xl)}, y = {E(yl)}. Line: <b>{lind(m, b)}</b>. Does the y-intercept make sense in this situation?',
                         mc(corr, [N if ok else Y, 'Only if the slope is positive.', 'A y-intercept never makes sense.'], rnd), E(why)))
    return out

# ---------- C5 Marissa car data
@page('C', 'Homework practice: Marissa\u2019s car data (7-103)',
      'Line of best fit: y = \u22120.7x + 35.9 (x = car age in years, y = miles per gallon).',
      [('Predict', 'Substitute the car age for x.'), ('Solve backwards', 'Given mpg, set \u22120.7x + 35.9 = mpg and solve for x.'),
       ('Slope \u22120.7', 'Each year older \u2192 0.7 fewer mpg.'), ('Intercept 35.9', 'A brand-new car gets about 35.9 mpg.')],
      'Predict a 7-year-old car: y = \u22120.7(7) + 35.9 = <b>31 mpg</b>.')
def C5(rnd):
    m, b = F(-7, 10), F(359, 10)
    out = []
    for x in [2, 5, 10, 12, 4]:
        y = m * x + b
        out.append(Q(f'Using y = \u22120.7x + 35.9, predict the mpg of a <b>{x}-year-old</b> car.',
                     mc(dec(y), [dec(b + m * -x), dec(b - F(x)), dec(m * x)], rnd, lambda: dec(y + rnd.choice([-2, -1, 1, 2]))),
                     f'\u22120.7({x}) + 35.9 = {dec(m*x)} + 35.9 = {dec(y)}.'.replace('-', MINUS)))
    for x in [3, 8, 13]:
        y = m * x + b
        out.append(Q(f'Using y = \u22120.7x + 35.9, how old is a car that gets <b>{dec(y)} mpg</b>?',
                     mc(f'{x} years', [f'{x+2} years', f'{x-1} years', f'{dec(y)} years'], rnd),
                     f'\u22120.7x + 35.9 = {dec(y)} \u2192 \u22120.7x = {dec(y-b)} \u2192 x = {x}.'.replace('-', MINUS)))
    out.append(Q('In y = \u22120.7x + 35.9, what does \u22120.7 tell you?',
                 ['Each year older, a car gets 0.7 fewer miles per gallon.', 'A new car gets 0.7 mpg.', 'Each year older, a car gets 0.7 more mpg.', 'Cars last 0.7 years.'],
                 'Slope = change in mpg per year of age.'))
    out.append(Q('Marissa\u2019s data shows newer cars get more mpg. Which association is it?',
                 ['Negative: as age increases, mpg decreases', 'Positive: as age increases, mpg increases', 'No association', 'Nonlinear positive'],
                 'Slope is negative \u2192 negative association.'))
    return out

# ---------- D1 proportions
PROP = [('Malcolm hops {a} times and travels {b} feet.', 'How many hops to travel {D} feet?', 'hops'),
        ('Ana reads {b} pages in {a} minutes.', 'How many minutes to read {D} pages?', 'minutes'),
        ('A printer prints {b} pages in {a} minutes.', 'How many minutes to print {D} pages?', 'minutes'),
        ('{a} gallons of gas take a car {b} miles.', 'How many gallons for {D} miles?', 'gallons'),
        ('A recipe uses {a} cups of flour for {b} cookies.', 'How many cups for {D} cookies?', 'cups'),
        ('Sam walks {b} blocks in {a} minutes.', 'How many minutes to walk {D} blocks?', 'minutes')]
@page('D', 'Proportions (scaling up and down)',
      'Set up two equal ratios with the SAME units on top: a/b = x/D. Then cross-multiply.',
      [('Ratio', 'A comparison of two quantities, like 10 hops : 12 feet.'), ('Proportion', 'Two equal ratios: 10/12 = x/90.'),
       ('Cross-multiply', '12x = 10 \u00b7 90 \u2192 x = 75.'), ('Unit rate', 'Amount for 1 unit: 12 \u00f7 10 = 1.2 feet per hop.')],
      'HW 7-104: 10 hops = 12 feet. 10/12 = x/90 \u2192 12x = 900 \u2192 <b>x = 75 hops</b>.')
def D1(rnd):
    def g(i):
        s, q, u = rnd.choice(PROP)
        a = rnd.choice([2, 3, 4, 5, 6, 8, 10]); b = rnd.choice([3, 5, 6, 9, 12, 15, 20, 24])
        if a == b: b += 1
        k = rnd.randint(2, 9)
        D = b * k  # answer a*k
        ans = a * k
        wr = [D * b // a if D * b % a == 0 else D * b / a, D // a if D % a == 0 else D - a, ans + a, b * k // 2 if b * k // 2 != ans else ans - 1]
        wr = [str(int(w)) if float(w) == int(w) else dec(w) for w in wr]
        return Q(E(s.format(a=a, b=b)) + ' ' + E(q.format(D=D)), mc(str(ans), wr, rnd, numfill(ans, rnd, str, 5)),
                 f'{a}/{b} = x/{D} \u2192 {b}x = {a*D} \u2192 x = {ans} {u}.')
    return uniq(g, 10)

# ---------- D2 unit rates
@page('D', 'Unit rates & better buys',
      'Unit rate = divide to get the amount for ONE. Lower price per item = better buy.',
      [('Unit rate', 'A rate with 1 in the denominator: $2.50 per notebook.'), ('Unit price', 'Cost \u00f7 number of items.'),
       ('Better buy', 'The option with the lower unit price.'), ('Speed', 'distance \u00f7 time: a unit rate.')],
      '12 feet in 10 hops \u2192 12 \u00f7 10 = <b>1.2 feet per hop</b>.')
def D2(rnd):
    def g(i):
        if i < 6:
            n = rnd.choice([3, 4, 5, 6, 8, 10, 12]); unit = rnd.choice([0.5, 0.75, 1.25, 1.5, 2.25, 2.5, 3.2, 4])
            item = rnd.choice(['notebooks', 'pens', 'apples', 'juice boxes', 'stickers', 'muffins'])
            tot = round(n * unit, 2)
            return Q(f'{n} {item} cost {money(tot)}. What is the cost of <b>one</b>?',
                     mc(money(unit), [money(n / tot) if tot else '$1', money(tot + n), money(unit * 2)], rnd, lambda: money(unit + rnd.choice([-0.25, 0.25, 0.5, 1]))),
                     f'{money(tot)} \u00f7 {n} = {money(unit)} each.')
        else:
            n1, n2 = rnd.choice([(4, 6), (3, 5), (6, 10), (8, 12), (5, 8)])
            u1 = rnd.choice([1.5, 2, 2.5, 3]); u2 = u1 + (0.5 if i % 2 else -0.5) * rnd.choice([1, 0.5])
            p1, p2 = round(n1 * u1, 2), round(n2 * u2, 2)
            best = 'Store A' if u1 < u2 else 'Store B'
            return Q(f'Store A: {n1} granola bars for {money(p1)}. Store B: {n2} granola bars for {money(p2)}. Which is the better buy?',
                     mc(best, ['Store B' if best == 'Store A' else 'Store A', 'They are the same', 'The one with more bars, always'], rnd),
                     f'A: {money(p1)} \u00f7 {n1} = {money(u1)} each. B: {money(p2)} \u00f7 {n2} = {money(u2)} each. Lower unit price wins.')
    return uniq(g, 10)

# ---------- D3 slope from graph
@page('D', 'Slope from a graph (rate of change)',
      'Pick two points ON the grid. slope = rise \u00f7 run = (change in y) \u00f7 (change in x).',
      [('Rise', 'Vertical change (up +, down \u2212).'), ('Run', 'Horizontal change (to the right).'),
       ('Rate of change', 'Slope with units, like $30 per month.'), ('Starting amount', 'Where the line starts on the y-axis (x = 0).')],
      'HW 7-105: Liz\u2019s line rises $30 every month \u2192 slope = <b>30 dollars per month</b>.')
def D3(rnd):
    def g(i):
        m = rnd.choice([10, 15, 20, 25, 30, 40, 5]); b = rnd.choice([0, 0, 10, 20, 40])
        top = b + m * 6
        ymax = int(math.ceil(top / 20.0) * 20)
        name = rnd.choice(['Liz', 'Jeffrey', 'Maya', 'Omar', 'Priya'])
        fig = svg_plot(xr=(0, 6), yr=(0, ymax), xs=1, ys=10 if ymax <= 200 else 20, gridlbl=(1, 20 if ymax <= 200 else 40),
                       xl='Time (months)', yl='Amount saved ($)', lines=[(0, b, 6, b + m * 6, '#c62828', name)])
        if i % 2 == 0:
            return Q(f'The graph shows {name}\u2019s savings. What is the slope (rate of saving)?',
                     mc(f'${m} per month', [f'${b + m} per month' if b else f'${m*2} per month', f'${m*6} per month', f'{fr(F(1, m))} dollar per month'], rnd,
                        lambda: f'${m + rnd.choice([-5, 5, 10])} per month'),
                     f'Each month the line goes up ${m}. (e.g. from ({0}, {b}) to (1, {b+m})).', fig)
        else:
            return Q(f'The graph shows {name}\u2019s savings. How much had {name} saved at the start (month 0)?',
                     mc(f'${b}', [f'${m}', f'${b+m}', f'${m*6+b}'], rnd, lambda: f'${b + rnd.choice([5, 10, 15])}'),
                     f'Read where the line crosses the y-axis: ${b}.', fig)
    return uniq(g, 10)

# ---------- D4 comparing two rates
@page('D', 'Comparing two lines: who is faster?',
      'Steeper line = faster rate. Compare the slopes, not where the lines start.',
      [('Steeper', 'Bigger slope \u2192 grows faster.'), ('Intersection', 'Where two lines cross, both have the same y at the same x.'),
       ('Difference in rates', 'Subtract the slopes: 30 \u2212 20 = $10 more per month.')],
      'HW 7-105a: Liz saves $30/month, Jeffrey $20/month \u2192 <b>Liz</b> is saving fastest even if Jeffrey started with more.')
def D4(rnd):
    def g(i):
        m1, m2 = rnd.sample([10, 15, 20, 25, 30, 40], 2)
        b1, b2 = rnd.choice([0, 20, 40, 60]), rnd.choice([0, 20, 40, 60])
        top = max(b1 + 6 * m1, b2 + 6 * m2); ymax = int(math.ceil(top / 40.0) * 40)
        fig = svg_plot(xr=(0, 6), yr=(0, ymax), xs=1, ys=20, gridlbl=(1, 40), xl='Time (months)', yl='Amount saved ($)',
                       lines=[(0, b1, 6, b1 + 6 * m1, '#c62828', 'Liz'), (0, b2, 6, b2 + 6 * m2, '#1565c0', 'Jeffrey')])
        fast = 'Liz' if m1 > m2 else 'Jeffrey'
        if i % 2 == 0:
            return Q('Who is saving money <b>faster</b>?', mc(fast, ['Jeffrey' if fast == 'Liz' else 'Liz', 'They save at the same rate', 'Whoever started with more'], rnd),
                     f'Liz: ${m1}/month, Jeffrey: ${m2}/month. Steeper line \u2192 {fast}.', fig)
        d = abs(m1 - m2)
        return Q(f'How much <b>more per month</b> does {fast} save than the other person?', mc(f'${d}', [f'${m1+m2}', f'${abs(b1-b2) or d+10}', f'${d*6}'], rnd, lambda: f'${d + rnd.choice([5, 10])}'),
                 f'{max(m1,m2)} \u2212 {min(m1,m2)} = ${d} per month.', fig)
    return uniq(g, 10)

# ---------- D5 slope from points / table
@page('D', 'Slope from two points or a table',
      'slope = (y\u2082 \u2212 y\u2081) \u00f7 (x\u2082 \u2212 x\u2081). Keep the same order on top and bottom!',
      [('Slope formula', 'm = (y\u2082 \u2212 y\u2081)/(x\u2082 \u2212 x\u2081)'), ('Table', 'Look at how y changes when x changes.'),
       ('Common mistake', 'Putting x on top: that gives run/rise, the wrong answer.'), ('Negative slope', 'y goes down as x goes up.')],
      '(1, 4) and (5, 12): (12 \u2212 4)/(5 \u2212 1) = 8/4 = <b>2</b>.')
def D5(rnd):
    def g(i):
        m = F(rnd.choice([1, 2, 3, -2, -3, 4, -1]), rnd.choice([1, 1, 2, 3]))
        x1 = rnd.randint(-4, 4); dx = m.denominator * rnd.choice([1, 2]); x2 = x1 + dx
        y1 = rnd.randint(-6, 8); y2 = y1 + m * dx
        if i < 6:
            q = f'What is the slope of the line through ({x1}, {fr(y1)}) and ({x2}, {fr(y2)})?'.replace('-', MINUS)
            fig = None
        else:
            xs = [x1 + k * dx for k in range(4)]; ys = [y1 + m * k * dx for k in range(4)]
            fig = table_html(['x'] + [fr(v) for v in xs], [['y'] + [fr(v) for v in ys]])
            q = 'What is the slope (rate of change) shown in this table?'
        wr = [fr(1 / m), fr(-m), fr(m * dx) if dx != 1 else fr(m + 1)]
        return Q(q, mc(fr(m), wr, rnd, lambda: fr(m + rnd.choice([-1, 1, 2]))),
                 f'({fr(y2)} \u2212 {fr(y1)}) \u00f7 ({x2} \u2212 {x1}) = {fr(y2-y1)} \u00f7 {dx} = {fr(m)}.'.replace('-', MINUS), fig)
    return uniq(g, 10)

# ---------- E1 two-step decimals
@page('E', 'Two-step equations with decimals',
      'Undo in reverse order: first add/subtract, then divide. Tip: multiply by 10 or 100 to get rid of decimals.',
      [('Inverse operations', 'Addition \u2194 subtraction, multiplication \u2194 division.'), ('Isolate x', 'Get x alone on one side.'),
       ('Clear decimals', 'Multiply every term by 10 (one decimal place) or 100 (two places).'), ('Check', 'Plug your answer back in.')],
      '2.5x + 1.5 = 14 \u2192 2.5x = 12.5 \u2192 x = <b>5</b>.')
def E1(rnd):
    def g(i):
        a = rnd.choice([0.5, 1.5, 2.5, 0.2, 1.2, 3.5, 0.25, 4.5]); b = rnd.choice([1.5, 2.25, -3.5, 4.5, 0.75, -1.25, 6])
        x = rnd.choice([-6, -4, -2, 2, 3, 4, 5, 6, 8, 10, 12])
        c = round(a * x + b, 2)
        eq = f'{dec(a)}x {"+" if b > 0 else MINUS} {dec(abs(b))} = {dec(c)}'
        wr = [dec((c + b) / a), dec(c / a - b), dec(-x)]
        return Q(f'Solve: <b>{eq}</b>', mc(f'x = {dec(x)}', [f'x = {w}' for w in wr], rnd, lambda: f'x = {dec(x + rnd.choice([-2, -1, 1, 2]))}'),
                 f'Subtract {dec(b)}: {dec(a)}x = {dec(c-b)}. Divide by {dec(a)}: x = {dec(x)}.'.replace('-', MINUS))
    return uniq(g, 10)

# ---------- E2 variables both sides
@page('E', 'Variables on both sides',
      'Move x-terms to one side and numbers to the other (do the same thing to both sides), then divide.',
      [('Balance', 'Whatever you do to one side, do to the other.'), ('Collect like terms', 'Gather x-terms together and numbers together.'),
       ('Tip', 'Move the SMALLER x-term to avoid negatives.'), ('Check', 'Both sides should give the same number.')],
      'HW 7-106b: 3x + 4.5 = 4.5x \u2212 18 \u2192 22.5 = 1.5x \u2192 <b>x = 15</b>.')
def E2(rnd):
    def g(i):
        x = rnd.choice([-8, -5, -3, -2, 2, 3, 4, 5, 6, 7, 9, 12, 15])
        if i < 7:
            a, c = rnd.sample([2, 3, 4, 5, 6, 7, 8, 9, -2, -3], 2)
            b = rnd.randint(-15, 15); d = a * x + b - c * x
            eq = f'{expr((a,"x"),(b,""))} = {expr((c,"x"),(d,""))}'
        else:
            a, c = rnd.sample([1.5, 3, 4.5, 2.5, 0.5, 6], 2)
            b = rnd.choice([4.5, -2.5, 7.5, 1.5]); d = round(a * x + b - c * x, 2)
            eq = f'{dec(a)}x {"+" if b > 0 else MINUS} {dec(abs(b))} = {dec(c)}x {"+" if d >= 0 else MINUS} {dec(abs(d))}'
        wrong = F(str(d)) + F(str(b))
        wrong = wrong / (F(str(a)) - F(str(c)))
        wr = [-x, x + rnd.choice([1, 2]), wrong if wrong != x else x * 2]
        return Q(f'Solve: <b>{eq}</b>', mc(f'x = {fr(x)}', [f'x = {fr(F(w).limit_denominator(100))}' for w in wr], rnd, lambda: f'x = {fr(x + rnd.choice([-3, 3, 4]))}'),
                 f'Get x-terms together: ({dec(a)} \u2212 {dec(c)})x = {dec(d)} \u2212 {dec(b)} \u2192 {dec(a-c)}x = {dec(d-b)} \u2192 x = {fr(x)}.'.replace('-', MINUS))
    return uniq(g, 10)

# ---------- E3 distributive
@page('E', 'Distributive property & combining like terms',
      'First distribute (multiply into the parentheses), then combine like terms, then solve.',
      [('Distribute', 'a(b + c) = ab + ac. Multiply EVERY term inside.'), ('Like terms', 'Terms with the same variable: 6.25x and \u22122.5x.'),
       ('Watch the sign', '\u22123(x \u2212 2) = \u22123x + 6.'), ('Simplify first', 'Clean up each side before solving.')],
      'HW 7-106d: 6.25x + 7.5 \u2212 2.5x = 3.75x \u2212 8.75 \u2192 3.75x + 7.5 = 3.75x \u2212 8.75 \u2192 7.5 = \u22128.75 \u2192 <b>no solution</b>.')
def E3(rnd):
    def g(i):
        x = rnd.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 8])
        p = rnd.choice([2, 3, 4, 5, 6, 7, -2, -3]); q = rnd.randint(-6, 6) or 2
        r = rnd.choice([1, 2, 3, 4, -1]); 
        if r == p: r += 1
        s = p * (x + q) - r * x
        eq = f'{fr(p)}(x {"+" if q > 0 else MINUS} {abs(q)}) = {expr((r,"x"),(s,""))}'
        wrong_dist = F(s - q, p - r) if p != r else x + 1   # forgot to distribute to q
        wr = [wrong_dist, -x, x + 2]
        return Q(f'Solve: <b>{eq}</b>', mc(f'x = {fr(x)}', [f'x = {fr(w)}' for w in wr if w != x], rnd, lambda: f'x = {fr(x + rnd.choice([-3, -1, 1, 3]))}'),
                 f'Distribute: {expr((p,"x"),(p*q,""))} = {expr((r,"x"),(s,""))} \u2192 {fr(p-r)}x = {fr(s-p*q)} \u2192 x = {fr(x)}.')
    return uniq(g, 10)

# ---------- E4 fraction busters
@page('E', 'Fraction Busters (clearing fractions)',
      'Multiply EVERY term on both sides by the least common multiple (LCM) of the denominators. The fractions disappear!',
      [('Fraction Busters', 'Multiply both sides by a number that cancels every denominator.'), ('LCM', 'Smallest number all denominators divide into.'),
       ('Every term', 'Don\u2019t forget whole numbers: they get multiplied too!'), ('Check', 'Substitute the answer into the original equation.')],
      'HW 7-115a: x/3 + x/5 = 8 \u2192 multiply by 15: 5x + 3x = 120 \u2192 8x = 120 \u2192 <b>x = 15</b>.')
def E4(rnd):
    def g(i):
        a, b = rnd.sample([2, 3, 4, 5, 6, 8, 10], 2)
        L = a * b // math.gcd(a, b)
        if i % 3 == 2:
            return Q(f'To use Fraction Busters on <b>x/{a} + x/{b} = 7</b>, what is the best number to multiply both sides by?',
                     mc(str(L), [str(a + b), str(a * b) if a * b != L else str(L * 2), str(max(a, b))], rnd, numfill(L, rnd, str)),
                     f'The LCM of {a} and {b} is {L}.')
        k = rnd.randint(1, 4)
        x = L * k
        if i % 3 == 0:
            c = F(x, a) + F(x, b)
            eq = f'x/{a} + x/{b} = {fr(c)}'
            why = f'Multiply by {L}: {L//a}x + {L//b}x = {fr(c*L)} \u2192 {L//a + L//b}x = {fr(c*L)} \u2192 x = {x}.'
        else:
            c = F(x, a) - F(x, b)
            if c == 0: c = F(x, a) + 1; eq = f'x/{a} = x/{b} + 1' if False else None
            eq = f'x/{a} {MINUS} x/{b} = {fr(c)}'
            why = f'Multiply by {L}: {L//a}x \u2212 {L//b}x = {fr(c*L)} \u2192 x = {x}.'
        wr = [c * (a + b), c * a, x + L]
        return Q(f'Solve: <b>{eq}</b>', mc(f'x = {fr(x)}', [f'x = {fr(w)}' for w in wr], rnd, lambda: f'x = {fr(x + rnd.choice([-2, 2, L]))}'), why)
    return uniq(g, 10)

# ---------- E5 percent equations
@page('E', 'Percent equations (x + 0.15x)',
      'x + 0.15x = 1.15x. Price + 15% tax/tip = 1.15 \u00d7 price. Price \u2212 20% off = 0.80 \u00d7 price.',
      [('Increase by p%', 'Multiply by (1 + p/100): +15% \u2192 1.15x.'), ('Decrease by p%', 'Multiply by (1 \u2212 p/100): \u221220% \u2192 0.80x.'),
       ('Original price', 'Divide the final amount by the multiplier.'), ('Combine', 'x + 0.15x: x is 1x, so 1x + 0.15x = 1.15x.')],
      'HW 7-115b: x + 0.15x = $230 \u2192 1.15x = 230 \u2192 <b>x = $200</b>.')
def E5(rnd):
    def g(i):
        p = rnd.choice([5, 10, 15, 20, 25, 30, 40, 8])
        x = rnd.choice([20, 40, 60, 80, 100, 120, 150, 200, 240, 300, 500])
        up = i % 2 == 0
        tot = x * (100 + p) / 100 if up else x * (100 - p) / 100
        what = rnd.choice(['tip', 'sales tax', 'markup']) if up else rnd.choice(['discount', 'off sale'])
        sgn = '+' if up else MINUS
        q = f'A price plus a {p}% {what} is {money(tot)}: x {sgn} {dec(p/100)}x = {money(tot)}. What is the original price x?' if up else \
            f'An item is {p}% off and now costs {money(tot)}: x {sgn} {dec(p/100)}x = {money(tot)}. What is the original price x?'
        wr = [tot - tot * p / 100 if up else tot + tot * p / 100, tot / (p / 100 + 0) if False else tot - p if up else tot + p, tot * (1 + p / 100) if up else tot / (1 + p / 100)]
        return Q(q, mc(money(x), [money(w) for w in wr], rnd, lambda: money(x + rnd.choice([-10, 10, 5]))),
                 f'{dec(1 + p/100) if up else dec(1 - p/100)}x = {money(tot)} \u2192 x = {money(tot)} \u00f7 {dec(1 + p/100) if up else dec(1 - p/100)} = {money(x)}.')
    return uniq(g, 10)

# ---------- E6 number of solutions
@page('E', 'One solution, no solution, or infinitely many?',
      'Solve it. If x disappears: a FALSE statement (7.5 = \u22128.75) \u2192 no solution. A TRUE statement (6 = 6) \u2192 infinitely many.',
      [('One solution', 'You end with x = a number.'), ('No solution', 'x cancels and you get something false, like 4 = \u22122.'),
       ('Infinitely many', 'x cancels and you get something always true, like 6 = 6. Both sides are the same expression.'),
       ('Same slope', 'Same x-coefficient on both sides is the warning sign that x will cancel.')],
      'HW 7-106d: 3.75x + 7.5 = 3.75x \u2212 8.75 \u2192 7.5 = \u22128.75 (false) \u2192 <b>no solution</b>.')
def E6(rnd):
    def g(i):
        k = i % 3
        a = rnd.choice([2, 3, 4, 5, 6]); b = rnd.randint(1, 9)
        if k == 0:  # no solution
            c = b + rnd.choice([-5, -3, 2, 4, 7])
            eq = f'{a}(x + {b}) = {expr((a,"x"),(a*c,""))}'
            corr = 'No solution'; why = f'{a}x + {a*b} = {expr((a,"x"),(a*c,""))} \u2192 {a*b} = {fr(a*c)}: false \u2192 no solution.'
        elif k == 1:
            eq = f'{a}(x + {b}) {MINUS} x = {expr((a-1,"x"),(a*b,""))}'
            corr = 'Infinitely many solutions'; why = f'Left side simplifies to {expr((a-1,"x"),(a*b,""))}, the same as the right \u2192 always true.'
        else:
            x = rnd.randint(-5, 6) or 1; c = a + rnd.choice([1, 2, -1])
            d = a * x + b - c * x
            eq = f'{expr((a,"x"),(b,""))} = {expr((c,"x"),(d,""))}'
            corr = f'One solution: x = {fr(x)}'; why = f'({a} \u2212 {c})x = {fr(d)} \u2212 {b} \u2192 x = {fr(x)}.'
        opts = mc(corr, ['No solution', 'Infinitely many solutions', 'One solution: x = 0', f'One solution: x = {fr(b)}'], rnd)
        return Q(f'How many solutions does <b>{eq}</b> have?', opts, why)
    return uniq(g, 10)

# ---------- E7 checking solutions
@page('E', 'Checking a solution (substitute and see)',
      'Substitute the value for x on BOTH sides. If both sides are equal, it is a solution.',
      [('Substitute', 'Replace x with the number (use parentheses for negatives!).'), ('Solution', 'A value that makes the equation true.'),
       ('Ordered-pair check', 'For a system, the point must work in BOTH equations.')],
      'Is x = 6 a solution of 2x \u2212 2 = \u2212x + 16? Left: 2(6) \u2212 2 = 10. Right: \u22126 + 16 = 10. Equal \u2192 <b>yes</b>.')
def E7(rnd):
    def g(i):
        x = rnd.randint(-5, 9) or 2
        a, c = rnd.sample([2, 3, 4, 5, -1, -2, 1], 2); b = rnd.randint(-9, 9); d = a * x + b - c * x
        eq = f'{expr((a,"x"),(b,""))} = {expr((c,"x"),(d,""))}'
        if i < 6:
            others = [v for v in [x + 1, x - 2, -x, x + 3] if v != x]
            return Q(f'Which value of x makes <b>{eq}</b> true?', mc(f'x = {fr(x)}', [f'x = {fr(v)}' for v in others], rnd),
                     f'Left: {a}({fr(x)}) + {b} = {fr(a*x+b)}. Right: {c}({fr(x)}) + {fr(d)} = {fr(c*x+d)}. Equal \u2713'.replace('+ -', f'{MINUS} '))
        m1, m2 = rnd.sample([1, 2, 3, -1, -2], 2); b1 = rnd.randint(-4, 6); X = rnd.randint(-3, 4); Y = m1 * X + b1; b2 = Y - m2 * X
        pt = (X, Y) if i % 2 == 0 else (X, Y + 2)
        ok = pt == (X, Y)
        return Q(f'Is <b>({fr(pt[0])}, {fr(pt[1])})</b> a solution of the system {lin(m1, b1)} and {lin(m2, b2)}?',
                 mc('Yes, it works in both equations' if ok else 'No, it does not work in both equations',
                    ['No, it does not work in both equations' if ok else 'Yes, it works in both equations', 'Yes, it only needs to work in one equation', 'You can\u2019t check a point'], rnd),
                 f'Plug x = {fr(pt[0])} into each: y = {fr(m1*pt[0]+b1)} and y = {fr(m2*pt[0]+b2)}. ' + ('Both match y.' if ok else 'They don\u2019t both match.'))
    return uniq(g, 10)

# ---------- F1 equal values
@page('F', 'Systems: Equal Values Method',
      'Both equations say "y = ...". Set the right sides equal, solve for x, then plug x back in to get y.',
      [('System of equations', 'Two equations that must both be true at once.'), ('Equal Values Method', 'If y = A and y = B, then A = B.'),
       ('Solution', 'An ordered pair (x, y): the point where the lines cross.'), ('Don\u2019t stop at x!', 'Find y too, and write (x, y).')],
      'HW 7-115d: y = \u00bdx + 8 and y = \u2153x + 10 \u2192 \u00bdx + 8 = \u2153x + 10 \u2192 x = 12, y = 14 \u2192 <b>(12, 14)</b>.')
def F1(rnd):
    def g(i):
        x = rnd.randint(-5, 8); m1, m2 = rnd.sample([1, 2, 3, 4, -1, -2, -3], 2)
        b1 = rnd.randint(-8, 10); y = m1 * x + b1; b2 = y - m2 * x
        corr = f'({fr(x)}, {fr(y)})'
        wr = [f'({fr(y)}, {fr(x)})', f'({fr(x)}, {fr(y + m1)})', f'({fr(-x)}, {fr(y)})' if x else f'(1, {fr(y)})']
        return Q(f'Solve the system: <b>{lin(m1, b1)}</b> and <b>{lin(m2, b2)}</b>', mc(corr, wr, rnd, lambda: f'({fr(x + rnd.choice([-1, 1, 2]))}, {fr(y)})'),
                 f'{lin(m1, b1, y="").replace("= ", "")} = {lin(m2, b2, y="").replace("= ", "")} \u2192 x = {fr(x)}; y = {fr(y)}.')
    return uniq(g, 10)

# ---------- F2 substitution
@page('F', 'Systems: Substitution',
      'Replace y in the second equation with what y equals in the first. Solve for x, then find y.',
      [('Substitution', 'Swap a variable for an equal expression.'), ('Parentheses', '2x + 3(x \u2212 1): keep the parentheses when you substitute!'),
       ('Back-substitute', 'Plug the x you found into the easier equation to find y.')],
      'y = x \u2212 1 and 2x + 3y = 12 \u2192 2x + 3(x \u2212 1) = 12 \u2192 5x = 15 \u2192 x = 3, y = 2 \u2192 <b>(3, 2)</b>.')
def F2(rnd):
    def g(i):
        x = rnd.randint(-3, 6); y = rnd.randint(-4, 8)
        m = rnd.choice([1, 2, 3, -1, -2]); b = y - m * x
        a, c = rnd.choice([1, 2, 3, 4]), rnd.choice([1, 2, 3, -1, -2])
        if a + c * m == 0: c += 1
        d = a * x + c * y
        corr = f'({fr(x)}, {fr(y)})'
        wr = [f'({fr(y)}, {fr(x)})', f'({fr(x)}, {fr(m*x)})' if b else f'({fr(x)}, {fr(y+1)})', f'({fr(x+1)}, {fr(m*(x+1)+b)})']
        return Q(f'Solve the system: <b>{lin(m, b)}</b> and <b>{expr((a,"x"),(c,"y"))} = {fr(d)}</b>', mc(corr, wr, rnd, lambda: f'({fr(x)}, {fr(y + rnd.choice([-2, 2]))})'),
                 f'Substitute: {expr((a,"x"))} + {fr(c)}({lin(m, b, y="").replace("= ", "")}) = {fr(d)} \u2192 x = {fr(x)}; then y = {fr(y)}.')
    return uniq(g, 10)

# ---------- F3 word problems
@page('F', 'Systems word problems: when are they equal?',
      'Write y = start + rate\u00b7x for each person/plan. Set them equal and solve: that\u2019s when they match.',
      [('Start (b)', 'The amount at time 0.'), ('Rate (m)', 'The change per month/day/hour.'),
       ('Equal Values', 'start\u2081 + rate\u2081\u00b7x = start\u2082 + rate\u2082\u00b7x'),
       ('Meaning of the solution', 'x = when they are equal, y = the amount they both have then.')],
      'Jeffrey has $100 and saves $20/month; Liz has $40 and saves $30/month: 100 + 20x = 40 + 30x \u2192 <b>x = 6 months</b>, both have $220.')
def F3(rnd):
    def g(i):
        r1, r2 = rnd.sample([5, 10, 15, 20, 25, 30, 40], 2)
        if r1 > r2: r1, r2 = r2, r1
        x = rnd.randint(2, 10); s2 = rnd.choice([0, 10, 20, 40, 50]); s1 = s2 + (r2 - r1) * x
        kind = i % 3
        if kind == 0:
            q = f'Jeffrey has ${s1} and saves ${r1} per month. Liz has ${s2} and saves ${r2} per month. After how many months will they have the same amount?'
            corr, wr = f'{x} months', [f'{x+2} months', f'{(s1 + s2)//(r1 + r2) or 1} month' + ('s' if (s1 + s2)//(r1 + r2) > 1 else '') if (s1 + s2)//(r1 + r2) != x else f'{x+1} months', f'{s1 // r2 or x+3} months' if s1 // r2 != x else f'{x-1} months']
        elif kind == 1:
            q = f'Gym A costs ${s1} to join plus ${r1} per month. Gym B costs ${s2} to join plus ${r2} per month. When do they cost the same, and how much?'
            y = s1 + r1 * x
            corr, wr = f'After {x} months, ${y}', [f'After {x} months, ${y + r1}', f'After {y} months, ${x}', f'After {x+1} months, ${s1 + r1*(x+1)}']
        else:
            a1 = rnd.choice([2, 3, 4]); a2 = a1 + rnd.choice([1, 2, 3]); h = x; c1 = rnd.choice([30, 40, 50, 60]); c2 = c1 - (a2 - a1) * h
            if c2 <= 0: c2 = c1; c1 = c2 + (a2 - a1) * h
            q = f'Plant A is {c1} cm tall and grows {a1} cm per week. Plant B is {c2} cm tall and grows {a2} cm per week. In how many weeks will they be the same height?'
            corr, wr = f'{h} weeks', [f'{h+1} weeks', f'{c1 - c2} weeks', f'{h*2} weeks']
        unit = corr.split()[-1] if kind != 1 else 'months'
        return Q(E(q), mc(corr, wr, rnd, lambda: f'{x + rnd.choice([3, 4, 5])} {unit}'),
                 'Set start + rate\u00b7x equal for both and solve for x' + (f': {s1} + {r1}x = {s2} + {r2}x \u2192 x = {x}.' if kind < 2 else '.'))
    return uniq(g, 10)

# ================================================================ BUILD
HEAD = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.png" type="image/png" sizes="64x64"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="stylesheet" href="style.css"></head>
'''
FOOT = '<footer>{note}</footer>\n<script>window.PREV={prev};window.NEXT={next};</script><script src="groups.js"></script><script src="app.js"></script></body></html>'
NOTE = 'Math 7 / CPM Chapter 7 review: practice questions modeled on homework 7-102 to 7-115. Answer order is shuffled every time. Tip: use &larr; &rarr; keys.'

def qhtml(q, gi, color, link=None):
    o = ''.join(f'<div class="o{" ok" if k == 0 else ""}"><span class="m">{"&#10004;" if k == 0 else "&#10008;"}</span><b class="l">{"ABCD"[k]}.</b><span>{t}</span></div>'
                for k, t in enumerate(q['opts']))
    fig = f'<div class="qfig">{q["fig"]}</div>' if q['fig'] else ''
    why = f'<div class="why">&#128161; {q["why"]}</div>' if q['why'] else ''
    frm = f'<a class="from" href="{link[0]}">&#128214; Study this topic: {E(link[1])}</a>' if link else ''
    return (f'<div class="q" data-id="{q["id"]}" data-g="{gi}"><span class="qid" style="background:{color}">{q["id"]}</span>'
            f'<span class="qact"><button class="chk" type="button" disabled>Check</button><span class="cmsg"></span></span>'
            f'<button class="hardbtn" type="button">&#9734; Mark hard</button><span class="hist"></span><span class="cnt"></span>'
            f'<div class="qt">{q["qt"]}</div>{fig}{o}{frm}{why}<div class="verdict"></div></div>')

def build():
    os.makedirs(OUT, exist_ok=True)
    groups, allq, toc = [], [], []
    seccount = {}
    N = len(PAGES)
    for gi, p in enumerate(PAGES):
        rnd = random.Random(1000 + gi)
        qs = p['fn'](rnd)
        assert len(qs) >= 10, (p['title'], len(qs))
        seccount[p['sec']] = seccount.get(p['sec'], 0) + 1
        for k, q in enumerate(qs):
            q['id'] = f"{p['sec']}{seccount[p['sec']]}-{k+1:02d}"
            assert len(set(q['opts'])) == 4, (q['id'], q['opts'])
            # randomise where the correct answer sits in the HTML (JS also shuffles)
        p['qs'] = qs; p['n'] = gi + 1; p['file'] = f'page_{gi+1:03d}.html'
        groups.append([q['id'] for q in qs])
    for gi, p in enumerate(PAGES):
        secname, color = SECTIONS[p['sec']]
        prev = f'"page_{gi:03d}.html"' if gi else 'null'
        nxt = f'"page_{gi+2:03d}.html"' if gi + 1 < N else 'null'
        nav = (f'<div class="nav"><a href="index.html">Topics</a>' + (f'<a href="page_{gi:03d}.html">&larr; Prev</a>' if gi else '<span>&larr; Prev</span>') +
               f'<span class="pg">{gi+1} / {N}</span>' + (f'<a href="page_{gi+2:03d}.html">Next &rarr;</a>' if gi + 1 < N else '<span>Next &rarr;</span>') + '</div>')
        kw = ''.join(f'<div class="it"><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in p['kw'])
        ex = f'<div class="explain"><h3>&#9999;&#65039; From the homework</h3>{p["ex"]}</div>' if p['ex'] else ''
        body = (HEAD.format(title=f'{gi+1}. {E(p["title"])} \u2013 Math 7 Study') +
                f'<body class="quiz"><header style="background:{color}"><div class="t"><h1>{gi+1}. {E(p["title"])}</h1>\n'
                f'<div class="sub">{E(secname)} &bull; {len(p["qs"])} questions</div></div><div class="stats" id="stats"></div>{nav}</header>\n'
                f'<main><div class="tip">&#128161; {E(p["tip"])}</div><div class="kw"><h3>&#128218; Key words</h3><dl>{kw}</dl></div>{ex}\n'
                '<div class="tools"><button id="mode">Study mode: show all answers</button><span class="hint">Press <b>Check</b> on any question to see if you\'re right (it won\'t show the answer), or <b>Grade</b> at the bottom to grade the whole page. Use scratch paper!</span></div>\n'
                + ''.join(qhtml(q, gi, color) for q in p['qs']) +
                '\n<div class="gradebar"><button class="grade">Grade my answers</button><span class="score" id="score"></span><button class="reset">&#8635; Try again</button></div>\n'
                f'<div style="text-align:center;margin:20px">{nav}</div>\n</main>' + FOOT.format(note=NOTE, prev=prev, next=nxt))
        open(os.path.join(OUT, p['file']), 'w').write(body)
    # groups.js
    open(os.path.join(OUT, 'groups.js'), 'w').write('window.GROUPS=' + json.dumps(groups) + ';\n')
    total = sum(len(g) for g in groups)
    # index
    toc = ''; last = None
    for gi, p in enumerate(PAGES):
        if p['sec'] != last:
            secname, color = SECTIONS[p['sec']]; toc += f'<h2 style="color:{color}">{E(secname)}</h2>'; last = p['sec']
        toc += f'<a href="{p["file"]}" data-g="{gi}"><span class="n">{gi+1}.</span>{E(p["title"])}<span class="c">{len(p["qs"])} q</span><span class="gs"></span></a>'
    idx = (HEAD.format(title='Math 7 Chapter 7 \u2013 Study by Topic') +
           '<body><header style="background:#263238"><div class="t"><h1>&#128208; Math 7 Chapter 7 \u2013 Study by Topic</h1>\n'
           f'<div class="sub">{N} topic pages &bull; {total} practice questions &bull; data, scatterplots, lines, equations, systems</div></div>\n'
           '<div class="stats" id="stats"></div><div class="nav"><a href="page_001.html">Start &rarr;</a><a href="mock.html">&#128221; Mock exam</a><button class="resetall" id="exportbtn">Export</button><button class="resetall" id="importbtn">Import</button><button class="resetall" id="resetall">Reset progress</button></div></header>\n'
           '<main class="toc"><div class="xfer" id="xfer" hidden><h3 id="xtitle"></h3><p id="xhelp"></p>\n<textarea id="xtext" spellcheck="false"></textarea>\n'
           '<div class="xrow"><label>Format: <select id="xfmt"><option value="json">JSON (readable)</option><option value="b64">Short code for texting (compressed)</option></select></label><span id="xsize" class="hint"></span></div>\n'
           '<div class="xrow"><button id="xgo"></button><button class="sec" id="xdl">Download .txt</button><label>or load a file: <input type="file" id="xfile" accept=".txt,.json,text/plain"></label>\n'
           '<span class="xmsg" id="xmsg"></span><button class="sec" id="xclose" style="margin-left:auto">Close</button></div></div>\n'
           + toc + '</main><footer>' + NOTE + '</footer>\n<script>window.PREV=null;window.NEXT="page_001.html";</script><script src="groups.js"></script><script src="app.js"></script></body></html>')
    open(os.path.join(OUT, 'index.html'), 'w').write(idx)
    # review (all questions with link back) & mock (all questions, JS picks one per page)
    allcards = ''.join(qhtml(q, gi, SECTIONS[p['sec']][1], (p['file'], f'{gi+1}. {p["title"]}')) for gi, p in enumerate(PAGES) for q in p['qs'])
    allplain = ''.join(qhtml(q, gi, SECTIONS[p['sec']][1]) for gi, p in enumerate(PAGES) for q in p['qs'])
    rv = (HEAD.format(title='Review \u2013 Math 7 Study') +
          '<body class="quiz"><header style="background:#b71c1c"><div class="t"><h1 id="rtitle">Review</h1>\n<div class="sub">Practice the questions you missed or marked hard &bull; answers re-shuffled each time</div></div>\n'
          '<div class="stats" id="stats"></div><div class="nav"><a href="index.html">Topics</a></div></header>\n'
          '<main id="review"><div class="rtabs"><a id="tab-failed" href="review.html?f=failed">Failed</a><a id="tab-freq" href="review.html?f=freq">Frequently failed</a><a id="tab-hard" href="review.html?f=hard">Hard</a></div>\n'
          '<div class="tools"><button id="mode">Study mode: show all answers</button><span class="hint">Pick an answer for each question, then press <b>Grade</b> at the bottom. Fixed ones leave the Failed list next time.</span></div>\n'
          + allcards + '\n<div class="gradebar"><button class="grade">Grade my answers</button><span class="score" id="score"></span><button class="reset">&#8635; Try again</button></div>\n</main>'
          + FOOT.format(note=NOTE, prev='null', next='null'))
    open(os.path.join(OUT, 'review.html'), 'w').write(rv)
    mk = (HEAD.format(title='Mock exam \u2013 Math 7 Study') +
          '<body class="quiz mockpage"><header style="background:#37474f"><div class="t"><h1 id="mtitle">Mock exam</h1>\n'
          f'<div class="sub">One random question from each of the {N} topics &bull; answers shuffled</div></div>\n'
          '<div class="stats" id="stats"></div><div class="nav"><a href="index.html">Topics</a></div></header>\n'
          f'<main id="mock"><div class="tools"><span class="hint">Answer all {N}, then press <b>Finish &amp; grade exam</b> at the bottom. You need <b>{math.ceil(N*0.8)} correct (80%)</b> to pass. Blank answers count as wrong.</span></div>\n'
          '<div class="mockhist" id="mockhist"></div><div class="mocksaved" id="mocksaved"></div>\n'
          + allplain + '\n<div class="gradebar"><button class="grade">Finish &amp; grade exam</button><span class="score" id="score"></span><button class="reset">&#8635; New mock exam</button></div>\n'
          '<div class="mockres" id="mockres" hidden></div>\n</main>' + FOOT.format(note=NOTE, prev='null', next='null'))
    open(os.path.join(OUT, 'mock.html'), 'w').write(mk)
    print(f'{N} pages, {total} questions')

if __name__ == '__main__':
    build()

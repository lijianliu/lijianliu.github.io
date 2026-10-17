"""Build one HTML page per topic group: PNG illustration on top, exact bank questions below, prev/next nav."""
import sys, os, importlib, collections, html, json
from core import QS, SUBCOLORS, SUBNAMES
import core2

MODS = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p0"]
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "site"))
IMG = os.path.join(OUT, "img")

slides = []
for m in MODS:
    if os.path.exists(os.path.join(os.path.dirname(__file__), f"{m}.py")):
        slides += importlib.import_module(m).SLIDES

seen = collections.Counter(i for s in slides for i in s["ids"])
dups = [k for k, v in seen.items() if v > 1]
bad = [k for k in seen if k not in QS]
missing = [k for k in QS if k not in seen]
print(f"pages {len(slides)}  covered {len(seen)}/{len(QS)}  dups {dups}  bad {bad}  missing {len(missing)}")

CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f4f6f9;color:#222}
header{position:sticky;top:0;z-index:5;color:#fff;padding:10px 16px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;box-shadow:0 2px 6px #0003}
header .t{flex:1;min-width:200px}
header h1{margin:0;font-size:22px}
header .sub{font-size:14px;opacity:.9}
.nav a,.nav span{display:inline-block;padding:8px 14px;border-radius:8px;background:#fff;color:#222;text-decoration:none;font-weight:bold;margin-left:6px}
.nav span{opacity:.35}
.nav .pg{background:transparent;color:#fff;opacity:1}
main{max-width:1100px;margin:0 auto;padding:16px}
.ill{width:100%;border-radius:12px;box-shadow:0 2px 8px #0002;background:#fff;display:block}
.tip{background:#fff8e1;border:2px solid #ffb300;border-radius:10px;padding:12px 16px;margin:16px 0;font-size:19px;font-weight:bold;color:#5d4037}
.q{background:#fff;border-radius:12px;padding:16px;margin:14px 0;box-shadow:0 1px 4px #0001}
.qid{display:inline-block;color:#fff;font-weight:bold;border-radius:6px;padding:3px 10px;font-size:15px}
.ref{color:#888;font-size:13px;margin-left:8px}
.qt{font-size:20px;font-weight:bold;margin:10px 0}
.o{border:2px solid #e3e3e3;border-radius:8px;padding:9px 12px;margin:6px 0;font-size:18px;color:#555;background:#fafafa;display:flex;gap:10px}
.o b.l{min-width:22px}
.o .m{min-width:22px;color:#c62828;font-weight:bold}
.o.ok{border-color:#2e7d32;background:#e8f5e9;color:#1b5e20;font-weight:bold}
.o.ok .m{color:#2e7d32}
/* quiz mode (default): answers hidden until the student picks one */
.quiz .o{cursor:pointer;color:#222}
.quiz .o:hover{border-color:#90caf9;background:#e3f2fd}
.quiz .o .m{visibility:hidden}
.quiz .o.ok{border-color:#e3e3e3;background:#fafafa;color:#222;font-weight:normal}
.quiz .q.done .o{cursor:default}
.quiz .q.done .o .m{visibility:visible}
.quiz .q.done .o.ok{border-color:#2e7d32;background:#e8f5e9;color:#1b5e20;font-weight:bold}
.quiz .q.done .o.pick:not(.ok){border-color:#c62828;background:#ffebee;color:#b71c1c;font-weight:bold}
.quiz .q.done .o:not(.ok):not(.pick){opacity:.55}
.verdict{display:none;margin-top:8px;font-weight:bold;font-size:18px}
.quiz .q.done .verdict{display:block}
.q.right .verdict{color:#2e7d32}.q.wrong .verdict{color:#c62828}
.q.right{box-shadow:0 0 0 3px #a5d6a7}.q.wrong{box-shadow:0 0 0 3px #ef9a9a}
.tools{margin:10px 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap;position:sticky;top:64px;z-index:4;background:#f4f6f9;padding:8px 0}
.tools button{font-size:16px;padding:8px 14px;border-radius:8px;border:1px solid #999;background:#fff;cursor:pointer}
.score{font-size:18px;font-weight:bold;background:#263238;color:#fff;border-radius:8px;padding:8px 14px}
.hint{color:#666}
footer{text-align:center;color:#888;font-size:13px;padding:20px}
.toc a{display:block;padding:10px 14px;margin:6px 0;background:#fff;border-radius:8px;text-decoration:none;color:#222;box-shadow:0 1px 3px #0001}
.toc h2{margin-top:26px}
.toc .n{display:inline-block;width:40px;color:#888}
.toc .c{color:#888;font-size:14px;float:right}
"""

JS = r"""
(function(){
const body=document.body, qs=[...document.querySelectorAll('.q')];
const sc=document.getElementById('score'), mb=document.getElementById('mode'), rb=document.getElementById('reset');
function upd(){ if(!sc) return;
  const d=qs.filter(q=>q.classList.contains('done')).length, r=qs.filter(q=>q.classList.contains('right')).length;
  sc.textContent=`Score: ${r} / ${d} answered (of ${qs.length})`+(d===qs.length&&qs.length?(r===qs.length?'  \u{1F389} Perfect!':''):''); }
qs.forEach(q=>{
  q.querySelectorAll('.o').forEach(o=>o.addEventListener('click',()=>{
    if(!body.classList.contains('quiz')||q.classList.contains('done')) return;
    o.classList.add('pick'); q.classList.add('done');
    const ok=o.classList.contains('ok'); q.classList.add(ok?'right':'wrong');
    const v=q.querySelector('.verdict');
    if(v) v.textContent= ok? '\u2714 Correct!' : '\u2718 Not quite. The correct answer is '+q.querySelector('.o.ok b.l').textContent.replace('.','');
    upd();
  }));
});
function reset(){ qs.forEach(q=>{q.classList.remove('done','right','wrong');q.querySelectorAll('.o').forEach(o=>o.classList.remove('pick'));}); upd(); }
if(mb) mb.onclick=()=>{ body.classList.toggle('quiz'); reset();
  mb.textContent=body.classList.contains('quiz')?'Study mode: show all answers':'Back to quiz mode';
  if(sc) sc.style.display=body.classList.contains('quiz')?'':'none'; };
if(rb) rb.onclick=reset;
upd();
document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'&&window.PREV)location=PREV;if(e.key==='ArrowRight'&&window.NEXT)location=NEXT;});
})();
"""

def fname(n):
    return f"page_{n:03d}.html"

def nav(n, total):
    p = f'<a href="{fname(n-1)}">&larr; Prev</a>' if n > 1 else '<span>&larr; Prev</span>'
    x = f'<a href="{fname(n+1)}">Next &rarr;</a>' if n < total else '<span>Next &rarr;</span>'
    return f'<div class="nav"><a href="index.html">Topics</a>{p}<span class="pg">{n} / {total}</span>{x}</div>'

import random, re
def order(q, qid):
    """Shuffle answer positions (allowed), but keep 'All/None of these' style options last
    and leave questions whose options refer to each other by letter in their original order."""
    idx = list(range(4))
    txt = " ".join(q["opts"])
    if re.search(r"\b(?:[ABCD] and [ABCD]|[ABCD], [ABCD])\b|choices? [ABCD]\b", txt):
        return idx
    fixed = [i for i in idx if re.match(r"(All these (choices|answers) are correct|None of (these|the above))", q["opts"][i])]
    move = [i for i in idx if i not in fixed]
    random.Random(qid).shuffle(move)
    return move + fixed

def q_html(qid, col):
    q = QS[qid]
    e = html.escape
    opts = []
    for pos, i in enumerate(order(q, qid)):
        L = "ABCD"[pos]
        ok = "ABCD"[i] == q["ans"]
        opts.append(f'<div class="o{" ok" if ok else ""}"><span class="m">{"&#10004;" if ok else "&#10008;"}</span><b class="l">{L}.</b><span>{e(q["opts"][i])}</span></div>')
    ref = f'<span class="ref">{e(q["ref"])}</span>' if q["ref"] else ""
    return (f'<div class="q"><span class="qid" style="background:{col}">{qid}</span>{ref}'
            f'<div class="qt">{e(q["q"])}</div>{"".join(opts)}<div class="verdict"></div></div>')

def page(n, total, s):
    col = SUBCOLORS[s["ids"][0][:2]]
    subs = list(dict.fromkeys(i[:2] for i in s["ids"]))
    subtxt = " + ".join(f"{x} {SUBNAMES[x]}" for x in subs)
    e = html.escape
    tip = f'<div class="tip">&#128161; {e(s["tip"])}</div>' if s.get("tip") else ""
    prev = f'"{fname(n-1)}"' if n > 1 else "null"
    nxt = f'"{fname(n+1)}"' if n < total else "null"
    extra = "".join(f'<img class="ill" style="margin-top:12px" src="{x}" alt="{e(x)}">' for x in s.get("extra_imgs", []))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{n}. {e(s['title'])} – Ham Technician Study</title><link rel="stylesheet" href="style.css"></head>
<body class="quiz"><header style="background:{col}"><div class="t"><h1>{n}. {e(s['title'])}</h1>
<div class="sub">{e(subtxt)} &bull; {len(s['ids'])} question{'s' if len(s['ids'])!=1 else ''}</div></div>{nav(n,total)}</header>
<main><img class="ill" src="img/group_{n:03d}.png" alt="Illustration: {e(s['title'])}">{extra}
{tip}
<div class="tools"><span class="score" id="score"></span><button id="reset">&#8635; Try again</button><button id="mode">Study mode: show all answers</button><span class="hint">Tap an answer to check it.</span></div>
{''.join(q_html(i, col) for i in s['ids'])}
<div style="text-align:center;margin:20px">{nav(n,total)}</div>
</main><footer>Questions &amp; answers copied word-for-word from the 2026-2030 Technician Class (Element 2) Question Pool. Only the A/B/C/D order is shuffled. Tip: use &larr; &rarr; keys.</footer>
<script>window.PREV={prev};window.NEXT={nxt};</script><script src="app.js"></script></body></html>"""

def index(slides):
    out, cur = [], None
    for n, s in enumerate(slides, 1):
        sub = s["ids"][0][:2]
        if sub != cur:
            cur = sub
            out.append(f'<h2 style="color:{SUBCOLORS[sub]}">{sub} – {SUBNAMES[sub]}</h2>')
        out.append(f'<a href="{fname(n)}"><span class="n">{n}.</span>{html.escape(s["title"])}<span class="c">{len(s["ids"])} q</span></a>')
    total = sum(len(s["ids"]) for s in slides)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ham Radio Technician – Study by Topic</title><link rel="stylesheet" href="style.css"></head><body>
<header style="background:#263238"><div class="t"><h1>&#128251; Ham Radio Technician 2026–2030 – Study by Topic</h1>
<div class="sub">{len(slides)} topic pages &bull; {total} of {len(QS)} pool questions</div></div>
<div class="nav"><a href="{fname(1)}">Start &rarr;</a></div></header>
<main class="toc">{''.join(out)}</main><script src="app.js"></script></body></html>"""

if __name__ == "__main__":
    only = sys.argv[1:]
    os.makedirs(IMG, exist_ok=True)
    open(os.path.join(OUT, "style.css"), "w").write(CSS)
    open(os.path.join(OUT, "app.js"), "w").write(JS)
    total = len(slides)
    for n, s in enumerate(slides, 1):
        if not only or str(n) in only:
            emp, edge = core2.render(s, os.path.join(IMG, f"group_{n:03d}.png"))
            flag = "  <-- SPARSE" if emp > 0.12 or edge < 0.035 else ""
            print(f"{n:3d} empty {emp:5.1%} edge {edge:.3f}  {s['title']}{flag}")
            for q in core2.QA:
                print(f"      QA: {q}")
        open(os.path.join(OUT, fname(n)), "w").write(page(n, total, s))
    open(os.path.join(OUT, "index.html"), "w").write(index(slides))
    print("wrote", OUT)

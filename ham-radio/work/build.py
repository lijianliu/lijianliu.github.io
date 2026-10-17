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
.explain{background:#fff;border-left:6px solid #7b1fa2;border-radius:10px;padding:12px 20px;margin:16px 0;font-size:18px;line-height:1.5;box-shadow:0 1px 4px #0001}
.explain h3{margin:4px 0 8px;color:#6a1b9a;font-size:21px}
.explain ul{margin:6px 0;padding-left:24px}.explain li{margin:4px 0}
.explain .yes{color:#2e7d32;font-weight:bold}.explain .no{color:#c62828;font-weight:bold}
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
/* quiz mode (default): pick answers, nothing is graded until "Grade" */
.quiz .o{cursor:pointer;color:#222}
.quiz .o:hover{border-color:#90caf9;background:#e3f2fd}
.quiz .o .m{visibility:hidden}
.quiz .o.ok{border-color:#e3e3e3;background:#fafafa;color:#222;font-weight:normal}
.quiz .o.sel{border-color:#1565c0;background:#bbdefb;color:#0d47a1;font-weight:bold}
.quiz .q.done .o{cursor:default}
.quiz .q.done .o .m{visibility:visible}
.quiz .q.done .o.ok{border-color:#2e7d32;background:#e8f5e9;color:#1b5e20;font-weight:bold}
.quiz .q.done .o.sel:not(.ok){border-color:#c62828;background:#ffebee;color:#b71c1c;font-weight:bold}
.quiz .q.done .o:not(.ok):not(.sel){opacity:.55}
.qact{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:8px}
button.chk{font-size:16px;font-weight:bold;padding:7px 16px;border-radius:8px;border:2px solid #1565c0;background:#fff;color:#1565c0;cursor:pointer}
button.chk:disabled{border-color:#bdbdbd;color:#9e9e9e;cursor:default}
.cmsg{font-weight:bold;font-size:17px}
.q.c-right .cmsg{color:#2e7d32}.q.c-wrong .cmsg{color:#c62828}
.quiz .q.c-right .o.sel{border-color:#2e7d32;background:#c8e6c9;color:#1b5e20}
.quiz .q.c-wrong .o.sel{border-color:#c62828;background:#ffcdd2;color:#b71c1c}
.q.c-right{box-shadow:0 0 0 3px #a5d6a7}.q.c-wrong{box-shadow:0 0 0 3px #ef9a9a}
.quiz .q.done .qact{display:none}
body:not(.quiz) .qact{display:none}
.verdict{display:none;margin-top:8px;font-weight:bold;font-size:18px}
.quiz .q.done .verdict,.quiz .q.skip .verdict{display:block}
.q.right .verdict{color:#2e7d32}.q.wrong .verdict{color:#c62828}.q.skip .verdict{color:#e65100}
.q.right{box-shadow:0 0 0 3px #a5d6a7}.q.wrong{box-shadow:0 0 0 3px #ef9a9a}.q.skip{box-shadow:0 0 0 3px #ffcc80}
.hist{float:right;font-size:13px;font-weight:bold;border-radius:6px;padding:3px 8px}
.hist.h-right{background:#e8f5e9;color:#2e7d32}.hist.h-wrong{background:#ffebee;color:#c62828}.hist.h-new{background:#eceff1;color:#607d8b}
.tools{margin:10px 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.tools button,.gradebar button{font-size:16px;padding:8px 14px;border-radius:8px;border:1px solid #999;background:#fff;cursor:pointer}
button.grade{background:#2e7d32;color:#fff;border-color:#1b5e20;font-weight:bold;font-size:18px;padding:10px 22px}
button.grade:disabled{background:#9e9e9e;border-color:#9e9e9e;cursor:default}
.gradebar{display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;background:#fff;border-radius:12px;padding:14px;margin:18px 0;box-shadow:0 1px 4px #0001}
.score{font-size:18px;font-weight:bold;background:#263238;color:#fff;border-radius:8px;padding:8px 14px}
.score:empty{display:none}
.hint{color:#666}
.stats{display:flex;gap:6px;align-items:center;flex-wrap:wrap;font-size:14px;font-weight:bold}
.stats .pill{background:#ffffffe6;color:#222;border-radius:20px;padding:5px 11px;white-space:nowrap}
.stats .pill b{font-size:16px}
.stats .p-bad b{color:#c62828}.stats .p-ok b{color:#2e7d32}
a.pill{text-decoration:none}
a.pill:hover{outline:2px solid #fff;filter:brightness(1.05)}
.stats .p-hard b{color:#ef6c00}
.hardbtn{float:right;margin-left:8px;font-size:13px;font-weight:bold;border-radius:6px;padding:3px 9px;border:1.5px solid #ffb74d;background:#fff;color:#ef6c00;cursor:pointer}
.hardbtn.on{background:#ff9800;border-color:#ef6c00;color:#fff}
.from{display:block;margin-top:8px;font-size:14px;color:#1565c0}
.rtabs{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 14px}
.rtabs a{padding:10px 18px;border-radius:10px;background:#fff;color:#222;text-decoration:none;font-weight:bold;font-size:17px;box-shadow:0 1px 3px #0002}
.rtabs a.cur{background:#263238;color:#fff}
.empty{background:#fff;border-radius:12px;padding:30px;text-align:center;font-size:20px;color:#555}
.gs .h{background:#fff3e0;color:#ef6c00}
.toc .gs{float:right;font-size:14px;margin-left:10px}
.toc .gs span{display:inline-block;border-radius:6px;padding:2px 8px;margin-left:4px;font-weight:bold}
.gs .f{background:#ffebee;color:#c62828}.gs .nt{background:#eceff1;color:#546e7a}.gs .done{background:#e8f5e9;color:#2e7d32}
.resetall{font-size:14px;padding:8px 12px;border-radius:8px;border:1px solid #fff;background:transparent;color:#fff;cursor:pointer;margin-left:6px}
footer{text-align:center;color:#888;font-size:13px;padding:20px}
.toc a{display:block;padding:10px 14px;margin:6px 0;background:#fff;border-radius:8px;text-decoration:none;color:#222;box-shadow:0 1px 3px #0001}
.toc h2{margin-top:26px}
.toc .n{display:inline-block;width:40px;color:#888}
.toc .c{color:#888;font-size:14px;float:right;margin-left:10px}
"""

JS = r"""
(function(){
// ---- progress store (browser localStorage) ----
// hamtech.v1 = { "T1A01": {r:"right"|"wrong", n:attempts, w:times_wrong, t:timestamp}, ... }
const KEY='hamtech.v1';
function load(){ try{ return JSON.parse(localStorage.getItem(KEY))||{}; }catch(e){ return {}; } }
function save(s){ try{ localStorage.setItem(KEY, JSON.stringify(s)); }catch(e){} }
const ALL=(window.GROUPS||[]).flat();
const HKEY='hamtech.hard';   // { "T1A01": true, ... } questions the student marked as hard
function loadHard(){ try{ return JSON.parse(localStorage.getItem(HKEY))||{}; }catch(e){ return {}; } }
function saveHard(h){ try{ localStorage.setItem(HKEY, JSON.stringify(h)); }catch(e){} }

// ---- review page: keep only failed / hard questions ----
const RV=document.getElementById('review');
if(RV){
  const f=(new URLSearchParams(location.search).get('f')==='hard')?'hard':'failed';
  const s=load(), h=loadHard();
  const keep=id=> f==='hard' ? !!h[id] : (s[id] && s[id].r==='wrong');
  let n=0;
  RV.querySelectorAll('.q').forEach(q=>{ if(keep(q.dataset.id)) n++; else q.remove(); });
  const nf=ALL.filter(id=>s[id]&&s[id].r==='wrong').length, nh=ALL.filter(id=>h[id]).length;
  document.getElementById('tab-failed').innerHTML=`&#10008; Failed questions (${nf})`;
  document.getElementById('tab-hard').innerHTML=`&#9733; Hard questions (${nh})`;
  document.getElementById('tab-'+f).classList.add('cur');
  document.getElementById('rtitle').textContent= f==='hard' ? 'Review: questions you marked hard' : 'Review: questions you got wrong';
  if(!n){
    RV.querySelectorAll('.gradebar,.tools').forEach(x=>x.remove());
    RV.insertAdjacentHTML('beforeend', f==='hard'
      ? '<div class="empty">No hard questions yet.<br>Tap <b>&#9734; Mark hard</b> on any question to add it here.</div>'
      : '<div class="empty">&#127881; No failed questions! Keep testing on the topic pages.</div>');
  }
}
function overall(){
  const s=load(); let tested=0, failed=0;
  ALL.forEach(id=>{ if(s[id]){ tested++; if(s[id].r==='wrong') failed++; } });
  return {tested, failed, total:ALL.length};
}
function paintStats(){
  const el=document.getElementById('stats'); if(!el) return;
  const o=overall();
  const nh=ALL.filter(id=>loadHard()[id]).length;
  el.innerHTML=`<span class="pill">Tested <b>${o.tested}</b> / ${o.total}</span>`+
               `<a class="pill p-bad" href="review.html?f=failed" title="Show all failed questions">Failed <b>${o.failed}</b></a>`+
               `<span class="pill p-ok">Passed <b>${o.tested-o.failed}</b></span>`+
               `<a class="pill p-hard" href="review.html?f=hard" title="Show questions you marked hard">&#9733; Hard <b>${nh}</b></a>`;
}

// ---- index page: per-group status ----
document.querySelectorAll('.toc a[data-g]').forEach(a=>{
  const ids=(window.GROUPS||[])[+a.dataset.g]||[], s=load(), hd=loadHard();
  const f=ids.filter(id=>s[id]&&s[id].r==='wrong').length, nt=ids.filter(id=>!s[id]).length, nh=ids.filter(id=>hd[id]).length;
  const gs=a.querySelector('.gs');
  if(gs) gs.innerHTML=(f?`<span class="f">[${f}] failed</span>`:'')+(nt?`<span class="nt">[${nt}] not tested</span>`:'')+(!f&&!nt?'<span class="done">✔ all passed</span>':'')+(nh?`<span class="h">&#9733; ${nh} hard</span>`:'');
});
const ra=document.getElementById('resetall');
if(ra) ra.onclick=()=>{ if(confirm('Erase ALL saved progress (results and hard marks) on this computer?')){ localStorage.removeItem(KEY); localStorage.removeItem(HKEY); location.reload(); } };

// ---- topic page: pick answers, then grade all at once ----
const body=document.body, qs=[...document.querySelectorAll('.q')];
const sc=document.getElementById('score'), mb=document.getElementById('mode');
const gbs=[...document.querySelectorAll('button.grade')], rbs=[...document.querySelectorAll('button.reset')];
let graded=false;
// ---- shuffle answer order on every page load (and on "Try again") ----
// "All these choices are correct" / "None of these" stay last; letters are re-assigned A-D.
const FIXED=/^(All these (choices|answers) are correct|None of (these|the above))/;
function shuffleAnswers(){
  qs.forEach(q=>{
    const opts=[...q.querySelectorAll('.o')], v=q.querySelector('.qact')||q.querySelector('.from')||q.querySelector('.verdict');
    const txt=o=>o.querySelector('span:last-child').textContent.trim();
    const move=opts.filter(o=>!FIXED.test(txt(o))), fixed=opts.filter(o=>FIXED.test(txt(o)));
    for(let i=move.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [move[i],move[j]]=[move[j],move[i]]; }
    move.concat(fixed).forEach((o,i)=>{ q.insertBefore(o,v); o.querySelector('b.l').textContent='ABCD'[i]+'.'; });
  });
}
shuffleAnswers();
function paintHist(){
  const s=load();
  qs.forEach(q=>{ const h=q.querySelector('.hist'); if(!h) return; const r=s[q.dataset.id];
    h.className='hist '+(r?(r.r==='right'?'h-right':'h-wrong'):'h-new');
    h.textContent=r?(r.r==='right'?'✔ passed':'✘ failed'):'not tested yet'; });
}
function picked(){ return qs.filter(q=>q.querySelector('.o.sel')).length; }
function paintButtons(){
  const p=picked();
  gbs.forEach(b=>{ b.disabled=graded||p===0; b.textContent=graded?'Graded ✔':`Grade my answers (${p} / ${qs.length})`; });
}
qs.forEach(q=>{
  q.querySelectorAll('.o').forEach(o=>o.addEventListener('click',()=>{
    if(!body.classList.contains('quiz')||graded) return;
    q.querySelectorAll('.o').forEach(x=>x.classList.remove('sel'));
    o.classList.add('sel'); q.classList.remove('skip'); clearCheck(q); paintButtons();
  }));
  const cb=q.querySelector('button.chk');
  if(cb) cb.addEventListener('click',()=>checkOne(q));
});
// ---- per-question Check: says right / wrong, never reveals which option is correct ----
// Every Check / Grade saves the latest result: a pass removes it from Failed, a miss adds it.
function clearCheck(q){
  q.classList.remove('c-right','c-wrong');
  const m=q.querySelector('.cmsg'); if(m) m.textContent='';
  const cb=q.querySelector('button.chk'); if(cb) cb.disabled=!q.querySelector('.o.sel');
}
function record(q, ok){
  const s=load(), id=q.dataset.id, r=s[id]||{n:0,w:0};
  r.n++; if(!ok) r.w++;
  r.r=ok?'right':'wrong'; r.t=Date.now(); s[id]=r; save(s);
}
function checkOne(q){
  const sel=q.querySelector('.o.sel'); if(!sel||graded) return;
  const ok=sel.classList.contains('ok');
  q.classList.remove('c-right','c-wrong'); q.classList.add(ok?'c-right':'c-wrong');
  q.querySelector('.cmsg').textContent= ok ? '✔ Correct!' : '✘ Not correct. Pick another answer and check again.';
  q.querySelector('button.chk').disabled=true;
  record(q, ok); paintStats(); paintHist();
}
function grade(){
  if(graded) return;
  let right=0, done=0, first=null;
  qs.forEach(q=>{
    const sel=q.querySelector('.o.sel'), v=q.querySelector('.verdict');
    if(!sel){ q.classList.add('skip'); v.textContent='– Not answered (not counted)'; return; }
    const ok=sel.classList.contains('ok'); done++; if(ok) right++;
    q.classList.add('done', ok?'right':'wrong');
    v.textContent= ok ? '✔ Correct!' : '✘ Not quite. The correct answer is '+q.querySelector('.o.ok b.l').textContent.replace('.','');
    q.classList.remove('c-right','c-wrong');
    record(q, ok);
    if(!ok && !first) first=q;
  });
  graded=true;
  if(sc) sc.textContent=`This page: ${right} / ${done} correct`+(done===qs.length&&right===done?'  🎉 Perfect!':'');
  paintButtons(); paintStats(); paintHist();
  (first||sc||document.body).scrollIntoView({behavior:'smooth', block:'center'});
}
function reset(){
  graded=false; if(sc) sc.textContent='';
  qs.forEach(q=>{ q.classList.remove('done','right','wrong','skip'); q.querySelectorAll('.o').forEach(o=>o.classList.remove('sel')); clearCheck(q); });
  shuffleAnswers(); paintHist(); paintButtons();
}
gbs.forEach(b=>b.onclick=grade);
rbs.forEach(b=>b.onclick=()=>{ reset(); window.scrollTo({top:0,behavior:'smooth'}); });
if(mb) mb.onclick=()=>{ body.classList.toggle('quiz'); reset();
  const q=body.classList.contains('quiz');
  mb.textContent=q?'Study mode: show all answers':'Back to quiz mode';
  document.querySelectorAll('.gradebar').forEach(g=>g.style.display=q?'':'none'); };

// ---- "Mark hard" toggle on every question ----
function paintHard(){
  const h=loadHard();
  qs.forEach(q=>{ const b=q.querySelector('.hardbtn'); if(!b) return; const on=!!h[q.dataset.id];
    b.classList.toggle('on',on); b.innerHTML=on?'&#9733; Hard':'&#9734; Mark hard'; b.title=on?'Click to un-mark':'Save this question to your Hard list'; });
}
qs.forEach(q=>{ const b=q.querySelector('.hardbtn'); if(b) b.addEventListener('click',e=>{
  e.stopPropagation(); const h=loadHard(), id=q.dataset.id;
  if(h[id]) delete h[id]; else h[id]=true;
  saveHard(h); paintHard(); paintStats(); }); });

paintStats(); paintHist(); paintButtons(); paintHard();
// refresh counts if another tab changed progress
window.addEventListener('storage',e=>{ if(e.key===KEY||e.key===HKEY){ paintStats(); paintHist(); paintHard(); } });
document.addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return; if(e.key==='ArrowLeft'&&window.PREV)location=PREV;if(e.key==='ArrowRight'&&window.NEXT)location=NEXT;});
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

def q_html(qid, col, src=None):
    q = QS[qid]
    e = html.escape
    opts = []
    for pos, i in enumerate(order(q, qid)):
        L = "ABCD"[pos]
        ok = "ABCD"[i] == q["ans"]
        opts.append(f'<div class="o{" ok" if ok else ""}"><span class="m">{"&#10004;" if ok else "&#10008;"}</span><b class="l">{L}.</b><span>{e(q["opts"][i])}</span></div>')
    ref = f'<span class="ref">{e(q["ref"])}</span>' if q["ref"] else ""
    frm = f'<a class="from" href="{fname(src[0])}">&#128214; Study this topic: {src[0]}. {e(src[1])}</a>' if src else ""
    return (f'<div class="q" data-id="{qid}"><span class="qid" style="background:{col}">{qid}</span>{ref}'
            f'<button class="hardbtn" type="button">&#9734; Mark hard</button><span class="hist"></span>'
            f'<div class="qt">{e(q["q"])}</div>{"".join(opts)}'
            f'<div class="qact"><button class="chk" type="button" disabled>Check</button><span class="cmsg"></span></div>'
            f'{frm}<div class="verdict"></div></div>')

def page(n, total, s):
    col = SUBCOLORS[s["ids"][0][:2]]
    subs = list(dict.fromkeys(i[:2] for i in s["ids"]))
    subtxt = " + ".join(f"{x} {SUBNAMES[x]}" for x in subs)
    e = html.escape
    tip = f'<div class="tip">&#128161; {e(s["tip"])}</div>' if s.get("tip") else ""
    tip += "".join(f'<div class="explain">{x}</div>' for x in s.get("explain", []))  # trusted HTML written in p*.py
    prev = f'"{fname(n-1)}"' if n > 1 else "null"
    nxt = f'"{fname(n+1)}"' if n < total else "null"
    extra = "".join(f'<img class="ill" style="margin-top:12px" src="{x}" alt="{e(x)}">' for x in s.get("extra_imgs", []))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{n}. {e(s['title'])} – Ham Technician Study</title><link rel="stylesheet" href="style.css"></head>
<body class="quiz"><header style="background:{col}"><div class="t"><h1>{n}. {e(s['title'])}</h1>
<div class="sub">{e(subtxt)} &bull; {len(s['ids'])} question{'s' if len(s['ids'])!=1 else ''}</div></div><div class="stats" id="stats"></div>{nav(n,total)}</header>
<main><img class="ill" src="img/group_{n:03d}.png" alt="Illustration: {e(s['title'])}">{extra}
{tip}
<div class="tools"><button id="mode">Study mode: show all answers</button><span class="hint">Press <b>Check</b> on any question to see if you're right (it won't show the answer), or <b>Grade</b> at the bottom to grade the whole page.</span></div>
{''.join(q_html(i, col) for i in s['ids'])}
<div class="gradebar"><button class="grade">Grade my answers</button><span class="score" id="score"></span><button class="reset">&#8635; Try again</button></div>
<div style="text-align:center;margin:20px">{nav(n,total)}</div>
</main><footer>Questions &amp; answers copied word-for-word from the 2026-2030 Technician Class (Element 2) Question Pool. Only the A/B/C/D order is shuffled. Tip: use &larr; &rarr; keys.</footer>
<script>window.PREV={prev};window.NEXT={nxt};</script><script src="groups.js"></script><script src="app.js"></script></body></html>"""

def index(slides):
    out, cur = [], None
    for n, s in enumerate(slides, 1):
        sub = s["ids"][0][:2]
        if sub != cur:
            cur = sub
            out.append(f'<h2 style="color:{SUBCOLORS[sub]}">{sub} – {SUBNAMES[sub]}</h2>')
        out.append(f'<a href="{fname(n)}" data-g="{n-1}"><span class="n">{n}.</span>{html.escape(s["title"])}<span class="c">{len(s["ids"])} q</span><span class="gs"></span></a>')
    total = sum(len(s["ids"]) for s in slides)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ham Radio Technician – Study by Topic</title><link rel="stylesheet" href="style.css"></head><body>
<header style="background:#263238"><div class="t"><h1>&#128251; Ham Radio Technician 2026–2030 – Study by Topic</h1>
<div class="sub">{len(slides)} topic pages &bull; {total} of {len(QS)} pool questions</div></div>
<div class="stats" id="stats"></div><div class="nav"><a href="{fname(1)}">Start &rarr;</a><button class="resetall" id="resetall">Reset progress</button></div></header>
<main class="toc">{''.join(out)}</main><script src="groups.js"></script><script src="app.js"></script></body></html>"""

def review(slides):
    qs_html = []
    for n, s in enumerate(slides, 1):
        for i in s["ids"]:
            qs_html.append(q_html(i, SUBCOLORS[i[:2]], (n, s["title"])))
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Review – Ham Technician Study</title><link rel="stylesheet" href="style.css"></head>
<body class="quiz"><header style="background:#b71c1c"><div class="t"><h1 id="rtitle">Review</h1>
<div class="sub">Questions copied word-for-word from the pool &bull; answers re-shuffled each time</div></div>
<div class="stats" id="stats"></div><div class="nav"><a href="index.html">Topics</a></div></header>
<main id="review"><div class="rtabs"><a id="tab-failed" href="review.html?f=failed">Failed</a><a id="tab-hard" href="review.html?f=hard">Hard</a></div>
<div class="tools"><button id="mode">Study mode: show all answers</button><span class="hint">Pick an answer for each question, then press <b>Grade</b> at the bottom. Fixed ones leave the Failed list next time.</span></div>
{''.join(qs_html)}
<div class="gradebar"><button class="grade">Grade my answers</button><span class="score" id="score"></span><button class="reset">&#8635; Try again</button></div>
</main><footer>Questions &amp; answers copied word-for-word from the 2026-2030 Technician Class (Element 2) Question Pool.</footer>
<script>window.PREV=null;window.NEXT=null;</script><script src="groups.js"></script><script src="app.js"></script></body></html>"""

if __name__ == "__main__":
    only = sys.argv[1:]
    os.makedirs(IMG, exist_ok=True)
    open(os.path.join(OUT, "style.css"), "w").write(CSS)
    open(os.path.join(OUT, "app.js"), "w").write(JS)
    open(os.path.join(OUT, "groups.js"), "w").write("window.GROUPS=" + json.dumps([s["ids"] for s in slides]) + ";\n")
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
    open(os.path.join(OUT, "review.html"), "w").write(review(slides))
    print("wrote", OUT)


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

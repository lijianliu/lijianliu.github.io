
(function(){
// ---- progress store (browser localStorage) ----
// hamtech.v1 = { "T1A01": {r:"right"|"wrong", n:attempts, w:times_wrong, t:timestamp}, ... }
// ---- profiles: each has its own results + hard marks ----
const PROFILES=['student1','student2','exam1'];
const PKEY='hamtech.profile';
// one-time migration: progress saved before profiles existed becomes student1's
try{
  if(localStorage.getItem('hamtech.v1')!==null && localStorage.getItem('hamtech.student1.v1')===null){
    localStorage.setItem('hamtech.student1.v1', localStorage.getItem('hamtech.v1'));
    if(localStorage.getItem('hamtech.hard')!==null) localStorage.setItem('hamtech.student1.hard', localStorage.getItem('hamtech.hard'));
    localStorage.removeItem('hamtech.v1'); localStorage.removeItem('hamtech.hard');
  }
}catch(e){}
let PROFILE='student1';
try{ const p=localStorage.getItem(PKEY); if(PROFILES.includes(p)) PROFILE=p; }catch(e){}
const KEY='hamtech.'+PROFILE+'.v1';
function load(){ try{ return JSON.parse(localStorage.getItem(KEY))||{}; }catch(e){ return {}; } }
function save(s){ try{ localStorage.setItem(KEY, JSON.stringify(s)); }catch(e){} }
const ALL=(window.GROUPS||[]).flat();
const HKEY='hamtech.'+PROFILE+'.hard';   // { "T1A01": true, ... } questions the student marked as hard
function loadHard(){ try{ return JSON.parse(localStorage.getItem(HKEY))||{}; }catch(e){ return {}; } }
function saveHard(h){ try{ localStorage.setItem(HKEY, JSON.stringify(h)); }catch(e){} }

// ---- frequently failed: missed 2+ times, most misses first (then worst miss rate), top 20 ----
const FREQ_MIN=2, FREQ_TOP=20;
function freqList(){
  const s=load();
  return ALL.filter(id=>s[id] && s[id].w>=FREQ_MIN)
    .sort((a,b)=> s[b].w-s[a].w || (s[b].w/s[b].n)-(s[a].w/s[a].n) || a.localeCompare(b))
    .slice(0,FREQ_TOP);
}
// ---- review page: keep only failed / hard / frequently failed questions ----
const RV=document.getElementById('review');
if(RV){
  const fp=new URLSearchParams(location.search).get('f');
  const f=['hard','freq'].includes(fp)?fp:'failed';
  const s=load(), h=loadHard(), fl=freqList();
  const keep=id=> f==='hard' ? !!h[id] : f==='freq' ? fl.includes(id) : (s[id] && s[id].r==='wrong');
  let n=0;
  RV.querySelectorAll('.q').forEach(q=>{ if(keep(q.dataset.id)) n++; else q.remove(); });
  if(f==='freq'){   // worst first, with a rank badge
    const cards=[...RV.querySelectorAll('.q')], anchor=RV.querySelector('.gradebar');
    fl.forEach((id,i)=>{ const c=cards.find(x=>x.dataset.id===id); if(!c) return;
      c.querySelector('.qid').insertAdjacentHTML('afterend',`<span class="rank">#${i+1} most missed</span>`);
      RV.insertBefore(c,anchor); });
  }
  const nf=ALL.filter(id=>s[id]&&s[id].r==='wrong').length, nh=ALL.filter(id=>h[id]).length;
  document.getElementById('tab-failed').innerHTML=`&#10008; Failed questions (${nf})`;
  document.getElementById('tab-freq').innerHTML=`&#128293; Frequently failed (${fl.length})`;
  document.getElementById('tab-hard').innerHTML=`&#9733; Hard questions (${nh})`;
  document.getElementById('tab-'+f).classList.add('cur');
  document.getElementById('rtitle').textContent= f==='hard' ? 'Review: questions you marked hard'
    : f==='freq' ? `Review: your most-missed questions (missed ${FREQ_MIN}+ times, top ${FREQ_TOP})` : 'Review: questions you got wrong';
  if(!n){
    RV.querySelectorAll('.gradebar,.tools').forEach(x=>x.remove());
    RV.insertAdjacentHTML('beforeend', f==='hard'
      ? '<div class="empty">No hard questions yet.<br>Tap <b>&#9734; Mark hard</b> on any question to add it here.</div>'
      : f==='freq' ? `<div class="empty">No frequently failed questions yet.<br>A question shows up here once you've missed it ${FREQ_MIN} or more times.</div>`
      : '<div class="empty">&#127881; No failed questions! Keep testing on the topic pages.</div>');
  }
}
function overall(){
  const s=load(); let tested=0, failed=0;
  ALL.forEach(id=>{ if(s[id]){ tested++; if(s[id].r==='wrong') failed++; } });
  return {tested, failed, total:ALL.length};
}
function paintProfile(){
  const st=document.getElementById('stats'); if(!st || document.getElementById('profile')) return;
  st.insertAdjacentHTML('beforebegin',
    `<label class="prof" title="Each profile keeps its own progress">&#128100; <select id="profile">${PROFILES.map(p=>`<option value="${p}"${p===PROFILE?' selected':''}>${p}</option>`).join('')}</select></label>`);
  document.getElementById('profile').onchange=e=>{ try{ localStorage.setItem(PKEY,e.target.value); }catch(_){} location.reload(); };
}
paintProfile();
function paintStats(){
  const el=document.getElementById('stats'); if(!el) return;
  const o=overall();
  const nh=ALL.filter(id=>loadHard()[id]).length;
  el.innerHTML=`<span class="pill">Tested <b>${o.tested}</b> / ${o.total}</span>`+
               `<a class="pill p-bad" href="review.html?f=failed" title="Show all failed questions">Failed <b>${o.failed}</b></a>`+
               `<span class="pill p-ok">Passed <b>${o.tested-o.failed}</b></span>`+
               `<a class="pill p-freq" href="review.html?f=freq" title="Questions you missed ${FREQ_MIN}+ times">&#128293; Frequently failed <b>${freqList().length}</b></a>`+
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
if(ra) ra.onclick=()=>{ if(confirm(`Erase ALL saved progress (results and hard marks) for profile "${PROFILE}"?`)){ localStorage.removeItem(KEY); localStorage.removeItem(HKEY); location.reload(); } };

// ---- export / import the current profile as text ----
const exb=document.getElementById('exportbtn'), imb=document.getElementById('importbtn'), xbox=document.getElementById('xfer');
function xfer(mode){
  xbox.hidden=false;
  const ta=document.getElementById('xtext'), msg=document.getElementById('xmsg');
  const go=document.getElementById('xgo'), dl=document.getElementById('xdl'), fi=document.getElementById('xfile');
  msg.textContent=''; msg.className='xmsg';
  if(mode==='export'){
    const data={app:'hamtech', version:1, profile:PROFILE, exported:new Date().toISOString(), results:load(), hard:loadHard()};
    ta.value=JSON.stringify(data,null,1); ta.readOnly=true;
    document.getElementById('xtitle').textContent=`Export profile "${PROFILE}"`;
    document.getElementById('xhelp').textContent='Copy this text (or download it) and keep it somewhere safe. Use Import to load it back on any computer or into another profile.';
    go.textContent='Copy to clipboard'; dl.hidden=false; fi.parentElement.hidden=true;
    go.onclick=()=>{ ta.select(); let ok=false; try{ ok=document.execCommand('copy'); }catch(e){}
      if(navigator.clipboard) navigator.clipboard.writeText(ta.value).then(()=>{msg.textContent='Copied!';},()=>{});
      msg.textContent= ok?'Copied!':'Text selected: press Ctrl+C (Cmd+C on Mac) to copy.'; };
    dl.onclick=()=>{ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([ta.value],{type:'text/plain'}));
      a.download=`hamtech-${PROFILE}-${new Date().toISOString().slice(0,10)}.txt`; document.body.appendChild(a); a.click(); a.remove(); };
    ta.focus(); ta.select();
  }else{
    ta.value=''; ta.readOnly=false;
    document.getElementById('xtitle').textContent=`Import into profile "${PROFILE}"`;
    document.getElementById('xhelp').textContent=`Paste exported text below (or choose a file), then press Import. This REPLACES the current progress of "${PROFILE}".`;
    go.textContent='Import'; dl.hidden=true; fi.parentElement.hidden=false;
    fi.value=''; fi.onchange=()=>{ const f=fi.files[0]; if(!f) return; const r=new FileReader(); r.onload=()=>{ ta.value=r.result; }; r.readAsText(f); };
    go.onclick=()=>{
      let d; try{ d=JSON.parse(ta.value); }catch(e){ msg.textContent='That text is not valid export data.'; msg.className='xmsg bad'; return; }
      if(!d || d.app!=='hamtech' || typeof d.results!=='object' || d.results===null){ msg.textContent='That text is not a Ham Technician export.'; msg.className='xmsg bad'; return; }
      const valid=new Set(ALL), res={}, hard={};
      for(const [id,r] of Object.entries(d.results)){
        if(!valid.has(id)||!r||typeof r!=='object') continue;
        const n=Math.max(0,parseInt(r.n)||0), w=Math.min(n,Math.max(0,parseInt(r.w)||0));
        if(!n || (r.r!=='right'&&r.r!=='wrong')) continue;
        res[id]={n, w, r:r.r, t:+r.t||Date.now()};
      }
      for(const [id,v] of Object.entries(d.hard||{})) if(valid.has(id)&&v) hard[id]=true;
      const nr=Object.keys(res).length, nh=Object.keys(hard).length;
      if(!confirm(`Replace progress of "${PROFILE}" with ${nr} question result(s) and ${nh} hard mark(s)`+(d.profile&&d.profile!==PROFILE?` from profile "${d.profile}"`:'')+'?')) return;
      save(res); saveHard(hard);
      msg.textContent=`Imported ${nr} result(s) and ${nh} hard mark(s).`; msg.className='xmsg ok';
      setTimeout(()=>location.reload(),900);
    };
    ta.focus();
  }
}
if(exb) exb.onclick=()=>xfer('export');
if(imb) imb.onclick=()=>xfer('import');
const xc=document.getElementById('xclose'); if(xc) xc.onclick=()=>{ xbox.hidden=true; };

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
    h.textContent=r?(r.r==='right'?'✔ passed':'✘ failed'):'not tested yet';
    const c=q.querySelector('.cnt');
    if(c){ c.textContent=r?`tried ${r.n}× · missed ${r.w}×`:''; c.title='How many times you checked or graded this question, and how many of those were wrong'; } });
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

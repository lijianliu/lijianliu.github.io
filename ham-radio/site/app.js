
(function(){
// ---- progress store (browser localStorage) ----
// hamtech.<profile>.v1 = { "T1A01": {r:"right"|"wrong", n:attempts, w:times_wrong}, ... }
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
// ---- mock test: one random question from each of the 35 groups (T0A ... T9B), pass = 26 ----
const MKEY='hamtech.'+PROFILE+'.mock', PASS_MARK=26;
function loadMock(){ try{ return JSON.parse(localStorage.getItem(MKEY))||[]; }catch(e){ return []; } }
function saveMock(m){ try{ localStorage.setItem(MKEY, JSON.stringify(m)); }catch(e){} }
const MOCK=document.getElementById('mock');
// in-progress exam is saved after every click, so leaving the page by accident loses nothing.
// { ids:[35 question IDs], order:{id:[original option indexes in shown order]}, sel:{id:original index}, graded:bool }
const NKEY='hamtech.'+PROFILE+'.mocknow';
function loadSess(){ try{ return JSON.parse(localStorage.getItem(NKEY)); }catch(e){ return null; } }
function saveSess(s){ try{ localStorage.setItem(NKEY, JSON.stringify(s)); }catch(e){} }
let SESS=null;
if(MOCK){
  const byGroup={};
  MOCK.querySelectorAll('.q').forEach(q=>{
    q.querySelectorAll('.o').forEach((o,k)=>o.dataset.k=k);        // stable option identity (HTML order)
    (byGroup[q.dataset.id.slice(0,3)]=byGroup[q.dataset.id.slice(0,3)]||[]).push(q); });
  const anchor=MOCK.querySelector('.gradebar');
  SESS=loadSess();
  const saved=SESS&&Array.isArray(SESS.ids)?new Set(SESS.ids):null;
  // a saved exam is only reused if it still has exactly one valid question per group
  if(saved && !Object.keys(byGroup).every(g=>byGroup[g].filter(q=>saved.has(q.dataset.id)).length===1)) SESS=null;
  Object.keys(byGroup).sort().forEach((g,i)=>{
    const list=byGroup[g], pick=SESS?list.find(q=>saved.has(q.dataset.id)):list[Math.floor(Math.random()*list.length)];
    list.forEach(q=>{ if(q!==pick) q.remove(); });
    pick.querySelector('.qid').insertAdjacentHTML('beforebegin',`<span class="qnum">Q${i+1}</span>`);
    MOCK.insertBefore(pick,anchor);
  });
  const tot=MOCK.querySelectorAll('.q').length;
  document.getElementById('mtitle').textContent=`Mock exam: ${tot} questions, pass with ${PASS_MARK} correct`;
  paintMockHist();
}
function paintMockHist(){
  const el=document.getElementById('mockhist'); if(!el) return;
  const m=loadMock();
  if(!m.length){ el.innerHTML='<b>Past mock exams:</b> none yet. Good luck on your first one!'; return; }
  const passes=m.filter(x=>x.score>=PASS_MARK).length, best=Math.max(...m.map(x=>x.score));
  el.innerHTML=`<b>Past mock exams (${PROFILE}):</b> ${m.length} taken &bull; ${passes} passed &bull; best ${best}/35<div class="mh">`+
    m.slice(-10).reverse().map(x=>`<span class="${x.score>=PASS_MARK?'mp':'mf'}" title="${x.t?new Date(x.t).toLocaleString():''}">${x.score}/${x.total}</span>`).join('')+'</div>';
}
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
    `<label class="prof" title="Each profile keeps its own progress">&#128100; <select id="profile">${PROFILES.map(p=>`<option value="${p}"${p===PROFILE?' selected':''}>${p}</option>`).join('')}</select>`+
    `<button type="button" class="topreset" title="Erase all saved progress for this profile">&#8634; Reset</button></label>`);
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
               `<a class="pill p-hard" href="review.html?f=hard" title="Show questions you marked hard">&#9733; Hard <b>${nh}</b></a>`+
               `<a class="pill p-mock" href="mock.html" title="35 random questions, like the real exam">&#128221; Mock exam</a>`;
}

// ---- index page: per-group status ----
document.querySelectorAll('.toc a[data-g]').forEach(a=>{
  const ids=(window.GROUPS||[])[+a.dataset.g]||[], s=load(), hd=loadHard();
  const f=ids.filter(id=>s[id]&&s[id].r==='wrong').length, nt=ids.filter(id=>!s[id]).length, nh=ids.filter(id=>hd[id]).length;
  const gs=a.querySelector('.gs');
  if(gs) gs.innerHTML=(f?`<span class="f">[${f}] failed</span>`:'')+(nt?`<span class="nt">[${nt}] not tested</span>`:'')+(!f&&!nt?'<span class="done">✔ all passed</span>':'')+(nh?`<span class="h">&#9733; ${nh} hard</span>`:'');
});
function resetProfile(){
  if(!confirm(`Are you sure you want to reset profile "${PROFILE}"?\n\nThis erases ALL its saved results, hard marks and mock exam history. It cannot be undone.\n(Tip: use Export on the Topics page first to keep a copy.)`)) return;
  localStorage.removeItem(KEY); localStorage.removeItem(HKEY); localStorage.removeItem(MKEY); localStorage.removeItem('hamtech.'+PROFILE+'.mocknow'); location.reload();
}
document.querySelectorAll('#resetall, .topreset').forEach(b=>b.addEventListener('click',e=>{ e.preventDefault(); resetProfile(); }));

// ---- export / import the current profile as text ----
const exb=document.getElementById('exportbtn'), imb=document.getElementById('importbtn'), xbox=document.getElementById('xfer');
// export format: compact JSON, or "HAM1:" + base64url(deflate-raw(JSON)) for texting
function exportData(){
  const res={};
  for(const [id,r] of Object.entries(load())) res[id]={r:r.r, n:r.n, w:r.w};       // no timestamp: never used
  return {app:'hamtech', version:2, profile:PROFILE, results:res, hard:Object.keys(loadHard()),
          mock:loadMock().map(x=>({t:x.t, score:x.score, total:x.total}))};        // t = date shown in mock history
}
async function gzipB64(str){
  const cs=new Blob([str]).stream().pipeThrough(new CompressionStream('deflate-raw'));
  const buf=new Uint8Array(await new Response(cs).arrayBuffer());
  let bin=''; for(let i=0;i<buf.length;i+=0x8000) bin+=String.fromCharCode.apply(null,buf.subarray(i,i+0x8000));
  return 'HAM1:'+btoa(bin).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
}
async function gunzipB64(txt){
  let s=txt.replace(/^HAM1:/,'').replace(/\s+/g,'').replace(/-/g,'+').replace(/_/g,'/');
  while(s.length%4) s+='=';
  const bin=atob(s), buf=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) buf[i]=bin.charCodeAt(i);
  const ds=new Blob([buf]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
  return await new Response(ds).text();
}
async function parseImport(txt){
  txt=txt.trim();
  if(/^HAM1:/.test(txt)) return JSON.parse(await gunzipB64(txt));
  return JSON.parse(txt);
}
function xfer(mode){
  xbox.hidden=false;
  const ta=document.getElementById('xtext'), msg=document.getElementById('xmsg');
  const go=document.getElementById('xgo'), dl=document.getElementById('xdl'), fi=document.getElementById('xfile');
  const fmt=document.getElementById('xfmt');
  msg.textContent=''; msg.className='xmsg';
  if(mode==='export'){
    const json=JSON.stringify(exportData());
    const show=async()=>{
      if(fmt.value==='b64'){
        try{ ta.value=await gzipB64(json); }
        catch(e){ ta.value=json; fmt.value='json'; msg.textContent='Compression not supported in this browser: showing JSON.'; msg.className='xmsg bad'; }
      }else ta.value=json;
      document.getElementById('xsize').textContent=`${ta.value.length.toLocaleString()} characters`;
      ta.focus(); ta.select();
    };
    ta.readOnly=true; fmt.parentElement.hidden=false; fmt.onchange=show;
    document.getElementById('xtitle').textContent=`Export profile "${PROFILE}"`;
    document.getElementById('xhelp').textContent='Copy this text (or download it). "Short code" is compressed so it fits in a text message. Use Import on the other computer or profile to load it.';
    go.textContent='Copy to clipboard'; dl.hidden=false; fi.parentElement.hidden=true;
    go.onclick=()=>{ ta.select(); let ok=false; try{ ok=document.execCommand('copy'); }catch(e){}
      if(navigator.clipboard) navigator.clipboard.writeText(ta.value).then(()=>{msg.textContent='Copied!';},()=>{});
      msg.textContent= ok?'Copied!':'Text selected: press Ctrl+C (Cmd+C on Mac) to copy.'; msg.className='xmsg ok'; };
    dl.onclick=()=>{ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([ta.value],{type:'text/plain'}));
      a.download=`hamtech-${PROFILE}-${new Date().toISOString().slice(0,10)}.txt`; document.body.appendChild(a); a.click(); a.remove(); };
    show();
  }else{
    ta.value=''; ta.readOnly=false; fmt.parentElement.hidden=true; document.getElementById('xsize').textContent='';
    document.getElementById('xtitle').textContent=`Import into profile "${PROFILE}"`;
    document.getElementById('xhelp').textContent=`Paste the exported text or short code (HAM1:...) below, or choose a file, then press Import. This REPLACES the current progress of "${PROFILE}".`;
    go.textContent='Import'; dl.hidden=true; fi.parentElement.hidden=false;
    fi.value=''; fi.onchange=()=>{ const f=fi.files[0]; if(!f) return; const r=new FileReader(); r.onload=()=>{ ta.value=r.result; }; r.readAsText(f); };
    go.onclick=async()=>{
      let d; try{ d=await parseImport(ta.value); }catch(e){ msg.textContent='That text is not valid export data (was it copied completely?).'; msg.className='xmsg bad'; return; }
      if(!d || d.app!=='hamtech' || typeof d.results!=='object' || d.results===null){ msg.textContent='That text is not a Ham Technician export.'; msg.className='xmsg bad'; return; }
      const valid=new Set(ALL), res={}, hard={};
      for(const [id,r] of Object.entries(d.results)){
        if(!valid.has(id)||!r||typeof r!=='object') continue;
        const n=Math.max(0,parseInt(r.n)||0), w=Math.min(n,Math.max(0,parseInt(r.w)||0));
        if(!n || (r.r!=='right'&&r.r!=='wrong')) continue;
        res[id]={r:r.r, n, w};
      }
      // hard: v2 = list of IDs, v1 = {id:true}
      const hl=Array.isArray(d.hard)?d.hard:Object.keys(d.hard||{}).filter(k=>d.hard[k]);
      for(const id of hl) if(valid.has(id)) hard[id]=true;
      const mk=Array.isArray(d.mock)?d.mock.filter(x=>x&&Number.isFinite(+x.score)).map(x=>({t:+x.t||0, score:Math.max(0,Math.min(35,+x.score)), total:+x.total||35})):[];
      const nr=Object.keys(res).length, nh=Object.keys(hard).length;
      if(!confirm(`Replace progress of "${PROFILE}" with ${nr} question result(s), ${nh} hard mark(s) and ${mk.length} mock exam(s)`+(d.profile&&d.profile!==PROFILE?` from profile "${d.profile}"`:'')+'?')) return;
      save(res); saveHard(hard); saveMock(mk);
      msg.textContent=`Imported ${nr} result(s), ${nh} hard mark(s), ${mk.length} mock exam(s).`; msg.className='xmsg ok';
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
    const opts=[...q.querySelectorAll('.o')], v=q.querySelector('.from')||q.querySelector('.verdict');
    const txt=o=>o.querySelector('span:last-child').textContent.trim();
    const move=opts.filter(o=>!FIXED.test(txt(o))), fixed=opts.filter(o=>FIXED.test(txt(o)));
    for(let i=move.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [move[i],move[j]]=[move[j],move[i]]; }
    move.concat(fixed).forEach((o,i)=>{ q.insertBefore(o,v); o.querySelector('b.l').textContent='ABCD'[i]+'.'; });
  });
}
shuffleAnswers();
function sessOrder(q){ return [...q.querySelectorAll('.o')].map(o=>+o.dataset.k); }
function relabel(q){ q.querySelectorAll('.o').forEach((o,i)=>o.querySelector('b.l').textContent='ABCD'[i]+'.'); }
if(MOCK){
  if(SESS){
    qs.forEach(q=>{
      const ord=SESS.order&&SESS.order[q.dataset.id], v=q.querySelector('.from')||q.querySelector('.verdict');
      const opts=[...q.querySelectorAll('.o')];
      if(Array.isArray(ord)&&ord.length===opts.length){ ord.forEach(k=>{ const o=opts.find(x=>+x.dataset.k===k); if(o) q.insertBefore(o,v); }); relabel(q); }
      const k=SESS.sel&&SESS.sel[q.dataset.id];
      if(k!==undefined&&k!==null){ const o=opts.find(x=>+x.dataset.k===+k); if(o) o.classList.add('sel'); }
    });
  }else{
    SESS={ids:qs.map(q=>q.dataset.id), order:{}, sel:{}, graded:false, started:Date.now()};
    qs.forEach(q=>SESS.order[q.dataset.id]=sessOrder(q));
    saveSess(SESS);
  }
}
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
  gbs.forEach(b=>{ b.disabled=graded||p===0; b.textContent=graded?'Graded ✔':(MOCK?`Finish & grade exam (${p} / ${qs.length} answered)`:`Grade my answers (${p} / ${qs.length})`); });
}
qs.forEach(q=>{
  q.querySelectorAll('.o').forEach(o=>o.addEventListener('click',()=>{
    if(!body.classList.contains('quiz')||graded) return;
    q.querySelectorAll('.o').forEach(x=>x.classList.remove('sel'));
    o.classList.add('sel'); q.classList.remove('skip'); clearCheck(q); paintButtons();
    if(MOCK&&SESS){ SESS.sel[q.dataset.id]=+o.dataset.k; saveSess(SESS); paintSaved(); }
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
  r.r=ok?'right':'wrong'; delete r.t; s[id]=r; save(s);
}
function checkOne(q){
  const sel=q.querySelector('.o.sel'); if(!sel||graded) return;
  const ok=sel.classList.contains('ok');
  q.classList.remove('c-right','c-wrong'); q.classList.add(ok?'c-right':'c-wrong');
  const cm=q.querySelector('.cmsg'); cm.textContent= ok ? '✔ Correct!' : '✘ Not correct, try again'; cm.title= ok ? '' : 'Pick another answer and press Check again';
  q.querySelector('button.chk').disabled=true;
  record(q, ok); paintStats(); paintHist();
}
function grade(restoring){
  restoring = restoring===true;
  if(graded) return;
  let right=0, done=0, first=null;
  qs.forEach(q=>{
    const sel=q.querySelector('.o.sel'), v=q.querySelector('.verdict');
    if(!sel){ q.classList.add('skip'); v.textContent='– Not answered (not counted)'; return; }
    const ok=sel.classList.contains('ok'); done++; if(ok) right++;
    q.classList.add('done', ok?'right':'wrong');
    v.textContent= ok ? '✔ Correct!' : '✘ Not quite. The correct answer is '+q.querySelector('.o.ok b.l').textContent.replace('.','');
    q.classList.remove('c-right','c-wrong');
    if(!restoring) record(q, ok);
    if(!ok && !first) first=q;
  });
  graded=true;
  if(MOCK){
    // real exam rules: every question counts; a blank is a wrong answer
    const total=qs.length, pass=right>=PASS_MARK;
    qs.forEach(q=>{ if(q.classList.contains('skip')) q.querySelector('.verdict').textContent='– Not answered (counts as wrong). The correct answer is '+q.querySelector('.o.ok b.l').textContent.replace('.',''); });
    if(!restoring){ const m=loadMock(); m.push({t:Date.now(), score:right, total}); saveMock(m); SESS.graded=true; saveSess(SESS); }
    const res=document.getElementById('mockres');
    res.hidden=false; res.className='mockres '+(pass?'pass':'fail');
    res.innerHTML=(pass?'🎉 PASS!':'✘ Not yet. Keep studying!')+`<div class="big">${right} / ${total}</div>`+
      `<div>You need ${PASS_MARK} to pass. ${pass?`You had ${right-PASS_MARK} to spare.`:`You needed ${PASS_MARK-right} more.`} Wrong: ${done-right} &bull; Blank: ${total-done}</div>`;
    if(sc) sc.textContent=`${right} / ${total} correct, ${pass?'PASS':'not passed'}`;
    paintButtons(); paintStats(); paintHist(); paintMockHist(); paintSaved();
    if(!restoring) res.scrollIntoView({behavior:'smooth', block:'center'});
    return;
  }
  if(sc) sc.textContent=`This page: ${right} / ${done} correct`+(done===qs.length&&right===done?'  🎉 Perfect!':'');
  paintButtons(); paintStats(); paintHist();
  (first||sc||document.body).scrollIntoView({behavior:'smooth', block:'center'});
}
function reset(){
  graded=false; if(sc) sc.textContent='';
  qs.forEach(q=>{ q.classList.remove('done','right','wrong','skip'); q.querySelectorAll('.o').forEach(o=>o.classList.remove('sel')); clearCheck(q); });
  shuffleAnswers(); paintHist(); paintButtons();
}
gbs.forEach(b=>b.onclick=()=>grade());
// "New mock exam" is the ONLY thing that throws away the saved exam
rbs.forEach(b=>b.onclick=()=>{
  if(MOCK){
    const s=loadSess(), n=s&&s.sel?Object.keys(s.sel).length:0;
    if(s&&!s.graded&&n>0&&!confirm(`Start a new mock exam? Your ${n} answer(s) on the current exam will be thrown away.`)) return;
    try{ localStorage.removeItem(NKEY); }catch(e){}
    location.reload(); return;
  }
  reset(); window.scrollTo({top:0,behavior:'smooth'}); });
function paintSaved(){
  const el=document.getElementById('mocksaved'); if(!el||!SESS) return;
  const n=Object.keys(SESS.sel||{}).length;
  el.textContent = SESS.graded ? 'This exam is graded. Press "New mock exam" for another one.'
    : n ? `💾 ${n} / ${qs.length} answers saved automatically. You can leave and come back anytime.`
        : '💾 Your answers are saved automatically as you pick them.';
}
if(MOCK){ paintButtons(); paintSaved(); if(SESS&&SESS.graded) grade(true); }
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
window.addEventListener('storage',e=>{ if(e.key===KEY||e.key===HKEY||e.key===MKEY){ paintStats(); paintHist(); paintHard(); } });
document.addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return; if(e.key==='ArrowLeft'&&window.PREV)location=PREV;if(e.key==='ArrowRight'&&window.NEXT)location=NEXT;});
})();

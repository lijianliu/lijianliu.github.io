
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

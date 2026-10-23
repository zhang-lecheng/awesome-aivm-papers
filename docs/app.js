const $ = s => document.querySelector(s);
const state = {category:'all', scope:'all', query:'', sort:'reading', stage:null, data:null};
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url = v => {try {const u=new URL(v); return u.protocol==='https:'?esc(u.href):'#';}catch{return '#';}};
const levels = {abstract:'摘要已核对',metadata:'出版元数据已核对',fulltext:'正文已核对',reproduced:'已实际复现'};
const scores = {question:'问题变化',decision:'实验或决策',information:'信息条件',evaluation:'评价方法',evidence:'证据强度',nontriviality:'超出常规组合'};
function visible(){
  if(!state.data) return [];
  const latest = state.data.issues[0];
  const fresh = new Set(latest?.paper_ids || []);
  const q=state.query.trim().toLowerCase();
  return state.data.papers.filter(p => (state.category==='all'||p.category===state.category) && (!state.stage||p.reading_stage===state.stage) && (state.scope==='all'||(state.scope==='essential'?p.essential:fresh.has(p.id))) && (!q||[p.title,p.method,p.authors,p.venue,p.doi,p.arxiv_id,p.pmcid,p.summary_zh,p.why_read,p.limitation].join(' ').toLowerCase().includes(q))).sort((a,b)=>state.sort==='year'?(b.year-a.year||a.title.localeCompare(b.title)):state.sort==='added'?String(b.added_on).localeCompare(String(a.added_on))||b.year-a.year:(a.reading_stage||6)-(b.reading_stage||6)||Number(b.essential)-Number(a.essential)||b.year-a.year);
}
function renderLibrary(){
  const list=visible();
  $('#result-count').textContent=`${list.length} 篇文献`;
  $('#empty').hidden=!!list.length;
  $('#active-stage').hidden=!state.stage;
  $('#active-stage').innerHTML=state.stage?`当前路线：第 ${state.stage} 步 <button id="clear-stage">取消路线筛选</button>`:'';
  $('#clear-stage')?.addEventListener('click',()=>{state.stage=null;renderLibrary();});
  $('#paper-list').innerHTML=list.map(p=>`<article class="paper"><div class="paper-heading"><h3><a href="${url(p.url)}" target="_blank" rel="noreferrer">${esc(p.title)}</a></h3><span class="paper-year">${esc(p.year)}</span></div><div class="paper-meta"><span class="badge">${esc(p.method||state.data.categories[p.category])}</span>${p.essential?'<span class="badge essential">入门必读</span>':''}<span>${esc(p.venue)}</span><span>·</span><span>${esc(levels[p.evidence_level]||'待核对')}</span></div><p class="paper-summary">${esc(p.summary_zh)}</p><details><summary>为什么读，以及如何判断证据</summary><dl><dt>为什么读</dt><dd>${esc(p.why_read)}</dd><dt>阅读时注意</dt><dd>${esc(p.limitation)}</dd>${p.new_question?`<dt>提出的新问题</dt><dd>${esc(p.new_question)}</dd>`:''}<dt>作者</dt><dd>${esc(p.authors||'见论文原文')}</dd>${p.scores?`<dt>本期阅读优先分</dt><dd>${Number(p.innovation_score)}/100；${Object.entries(p.scores).map(([k,v])=>`${scores[k]} ${Number(v)}`).join('，')}</dd>`:''}<dt>证据入口</dt><dd>${(p.evidence_urls||[p.url]).map((u,i)=>`<a href="${url(u)}" target="_blank" rel="noreferrer">来源 ${i+1} ↗</a>`).join('　')}</dd></dl></details><div class="paper-footer"><span>${p.doi?'DOI '+esc(p.doi):'arXiv '+esc(p.arxiv_id)} · 核查 ${esc(p.verified_on)}</span><a href="${url(p.url)}" target="_blank" rel="noreferrer">原文 ↗</a></div></article>`).join('');
  document.querySelectorAll('#categories button').forEach(b=>b.classList.toggle('active',b.dataset.category===state.category));
  document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('active',b.dataset.scope===state.scope));
  document.querySelectorAll('.step').forEach(b=>b.classList.toggle('chosen',Number(b.dataset.stage)===state.stage));
}
function renderWeek(index){
  const issue=state.data.issues[Number(index)];
  if(!issue){$('#weekly-content').innerHTML='<div class="weekly-editorial"><p>首期正在准备。已有基础文献可以从下方阅读路线开始。</p></div>';return;}
  const report=`https://github.com/zhang-lecheng/awesome-aivm-papers/blob/master/weekly/${issue.date}.md`;
  $('#weekly-content').innerHTML=`<div class="weekly-editorial"><p>${esc(issue.editorial_zh)}</p><a href="${report}" target="_blank" rel="noreferrer">完整周报 ↗</a></div><div class="week-grid">${issue.snapshots.map(p=>`<article class="week-paper"><div class="week-score">${Number(p.innovation_score)}</div><div><h3><a href="${url(p.url)}" target="_blank" rel="noreferrer">${esc(p.title)}</a></h3><p>${esc(p.new_question)}</p><small>${p.status==='featured'?'本周重点':'观察区'} · ${esc(levels[p.evidence_level])} · ${esc(p.date)}</small></div></article>`).join('')}</div><details class="source-notes"><summary>检索 ${esc(issue.since)}—${esc(issue.until)} · ${issue.candidate_count} 篇候选 · 查看来源与覆盖范围</summary><ul>${issue.sources.map(s=>`<li>${esc(s.source)}：${s.ok?`返回 ${s.returned} 条，命中 ${s.total_hits} 条${s.truncated?'（受返回上限影响）':''}`:'失败，'+esc(s.error)}</li>`).join('')}</ul></details>`;
}
function setup(data){
  state.data=data;
  $('#stat-total').textContent=data.papers.length;
  $('#stat-essential').textContent=data.papers.filter(p=>p.essential).length;
  $('#stat-categories').textContent=Object.keys(data.categories).length;
  $('#last-update').textContent=`最近核查 ${data.updated}`;
  const cats={all:'全部主题',...data.categories};
  $('#categories').innerHTML=Object.entries(cats).map(([key,name])=>`<button data-category="${key}" class="${key==='all'?'active':''}"><span>${esc(name)}</span><small>${key==='all'?data.papers.length:data.papers.filter(p=>p.category===key).length}</small></button>`).join('');
  $('#categories').addEventListener('click',e=>{const b=e.target.closest('button');if(b){state.category=b.dataset.category;state.stage=null;renderLibrary();}});
  $('#path-steps').innerHTML=data.pathways.map(p=>`<button class="step" data-stage="${p.step}"><span class="step-number">0${p.step} —</span><strong>${esc(p.title)}</strong><p>${esc(p.description)}</p><span class="step-methods">${esc(p.methods.slice(0,3).join(' · '))}</span></button>`).join('');
  $('#path-steps').addEventListener('click',e=>{const b=e.target.closest('button');if(b){state.stage=Number(b.dataset.stage);state.scope='all';state.category='all';state.query='';$('#search').value='';renderLibrary();$('#library').scrollIntoView({behavior:'smooth'});}});
  $('#week-select').innerHTML=data.issues.map((i,n)=>`<option value="${n}">${esc(i.date)}</option>`).join('')||'<option>尚无周报</option>';
  renderWeek(0);renderLibrary();
}
document.querySelectorAll('.tabs button').forEach(b=>b.addEventListener('click',()=>{state.scope=b.dataset.scope;state.stage=null;renderLibrary();}));
$('#search').addEventListener('input',e=>{state.query=e.target.value;renderLibrary();});
$('#sort').addEventListener('change',e=>{state.sort=e.target.value;renderLibrary();});
$('#week-select').addEventListener('change',e=>renderWeek(e.target.value));
$('#reset').addEventListener('click',()=>{Object.assign(state,{category:'all',scope:'all',query:'',stage:null});$('#search').value='';renderLibrary();});
$('#export').addEventListener('click',()=>{
  const safe=v=>String(v||'').replace(/[{}\\]/g,'');
  const bib=visible().map(p=>`@article{${(p.method||'aivm').replace(/[^a-zA-Z0-9]/g,'')}${p.year}${p.id.slice(-4).replace(/[^a-zA-Z0-9]/g,'')},\n  title = {${safe(p.title)}},\n  journal = {${safe(p.venue)}},\n  year = {${p.year}},\n  ${p.doi?'doi = {'+safe(p.doi)+'}':'url = {'+safe(p.url)+'}'}\n}`).join('\n\n');
  const blob=new Blob([bib+'\n'],{type:'application/x-bibtex;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='awesome-aivm-papers.bib';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
});
fetch('./data.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json();}).then(setup).catch(()=>{$('#paper-list').innerHTML='<p class="loading">暂时无法加载文献库，请刷新页面，或到 GitHub 查看 README。</p>';$('#weekly-content').innerHTML='';$('#last-update').textContent='数据加载失败';});

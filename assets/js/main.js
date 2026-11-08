(() => {
  "use strict";
  const search = document.querySelector('#search-input');
  const results = document.querySelector('#article-results');
  const status = document.querySelector('#results-status');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const original = results ? results.innerHTML : '';
  let all = null;
  let active = 'all';
  const cn = { stocks:'股票', etf:'ETF', funds:'基金', bonds:'債券', banking:'銀行與存款', insurance:'保險', planning:'風險與理財' };
  const esc = str => String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const base = document.querySelector('link[rel="stylesheet"]')?.getAttribute('href')?.replace(/assets\/css\/style\.css.*$/, '') || '/';
  const searchUrl = base + 'search.json';
  function setActive(category){ active = category; filters.forEach(b=>{ const selected=b.dataset.filter===category; b.classList.toggle('is-active',selected); b.setAttribute('aria-pressed',String(selected)); }); }
  function card(a){ return `<a class="article-card" href="${esc(a.url)}" data-category="${esc(a.category)}"><div class="article-card-top"><span class="pill pill-${esc(a.category)}">${esc(cn[a.category]||a.category)}</span><span class="article-arrow" aria-hidden="true">↗</span></div><h3>${esc(a.title)}</h3><p>${esc(a.description)}</p><div class="card-bottom"><span>入門教學</span><span>${esc(a.reading_time)} 分鐘閱讀</span></div></a>`; }
  function render(){ if(!results||!search||!all)return; const query=search.value.toLocaleLowerCase('zh-TW').trim(); const tokens=query.split(/\s+/).filter(Boolean); const matches=all.filter(a => (active==='all'||a.category===active) && tokens.every(t => [a.title,a.description,cn[a.category],...(a.tags||[])].join(' ').toLocaleLowerCase('zh-TW').includes(t))); results.innerHTML=matches.length ? `<div class="noscript-grid">${matches.map(card).join('')}</div>` : '<div class="empty-state"><strong>目前沒有符合的文章</strong><p>試試其他關鍵字，或切換分類看看。</p></div>'; status.textContent=`找到 ${matches.length} 篇文章`; }
  if(results&&search){
    const embedded = document.querySelector('#finance-data');
    if (embedded) {
      try { all = JSON.parse(embedded.textContent); if (!Array.isArray(all)) throw Error('Index format'); render(); }
      catch(e) { results.innerHTML=original; document.querySelector('#search-error')?.removeAttribute('hidden'); }
    } else {
      fetch(searchUrl).then(res=>{ if(!res.ok)throw Error('HTTP '+res.status);return res.json() }).then(data=>{ if(!Array.isArray(data))throw Error('Invalid index');all=data;render(); }).catch(()=>{results.innerHTML=original;document.querySelector('#search-error')?.removeAttribute('hidden');});
    }
    search.addEventListener('input',render);
    document.querySelector('#hero-search')?.addEventListener('submit',e=>{e.preventDefault();document.querySelector('#library')?.scrollIntoView({behavior:'smooth'});render();});
    filters.forEach(button=>button.addEventListener('click',()=>{setActive(button.dataset.filter);render();}));
    document.querySelectorAll('[data-select-category]').forEach(link=>link.addEventListener('click',()=>{setActive(link.dataset.selectCategory);render();}));
    document.querySelectorAll('[data-query]').forEach(button=>button.addEventListener('click',()=>{search.value=button.dataset.query;setActive('all');render();document.querySelector('#library')?.scrollIntoView({behavior:'smooth'});search.focus({preventScroll:true});}));
  }
  const body=document.querySelector('#article-body'); const toc=document.querySelector('#article-toc');
  if(body)body.querySelectorAll('table').forEach(table=>{const wrap=document.createElement('div');wrap.className='table-wrapper';wrap.tabIndex=0;wrap.setAttribute('role','region');wrap.setAttribute('aria-label','可水平捲動的比較表');table.parentNode.insertBefore(wrap,table);wrap.append(table);});
  if(body&&toc){const headings=[...body.querySelectorAll('h2')]; if(headings.length){const list=document.createElement('ol'); headings.forEach((h,i)=>{if(!h.id)h.id='section-'+(i+1);const li=document.createElement('li');const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;li.append(a);list.append(li);});toc.replaceChildren(list);}else{toc.textContent='本文沒有獨立章節';}}
})();

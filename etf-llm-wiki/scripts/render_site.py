#!/usr/bin/env python3
"""Build static, offline-viewable HTML from the locally ingested ETF Wiki."""
import json,html,re
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parent.parent
sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
evidence={e['id']:e for e in json.loads((ROOT/'cards/evidence.json').read_text(encoding='utf-8'))}
topics=json.loads((ROOT/'data/topics.json').read_text(encoding='utf-8'))
slides=json.loads((ROOT/'data/slides.json').read_text(encoding='utf-8'))
sources_by_id={s['id']:s for s in sources}
def h(s):return html.escape(str(s),quote=True)
def refs(eids):
 ss=[]
 for eid in eids:
  for sid in evidence[eid]['sources']:
   if sid not in ss:ss.append(sid)
 return ''.join(f'<a class="source-link" href="{h(sources_by_id[sid]["url"])}" target="_blank" rel="noopener noreferrer" title="{h(sources_by_id[sid]["title"])}">[{sid}]</a>' for sid in ss)
def shell(title, css, body,script='',relative=''):
 return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="ETF 投資入門：可追溯來源的 LLM Wiki 與互動 HTML 教學簡報"><title>{h(title)}</title><link rel="stylesheet" href="{relative}{css}"></head><body>{body}<script src="{relative}{script}" defer></script></body></html>''' if script else f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{h(title)}</title><link rel="stylesheet" href="{relative}{css}"></head><body>{body}</body></html>'''
landing='''<div class="grid-noise"></div><div class="wrapper"><header class="global-head"><a class="brand" href="index.html"><span class="brand-icon">E<span>·</span></span><span>ETF LAB <small>金融知識設計</small></span></a><nav aria-label="主要導覽"><a href="wiki/index.html">知識庫</a><a href="slides/index.html">教學簡報</a><a href="sources.md">來源索引</a></nav></header><main class="landing"><div class="landing-left"><span class="kicker">OPEN LEARNING / VOL. 01</span><h1>金融知識，<br><em>從這一頁開始。</em></h1><p class="lead">以 7 份官方與公開教育資料為基礎，整理 20 張可查核的證據卡，帶你用 10 頁互動簡報認識 ETF。</p><div class="action-row"><a class="btn-primary" href="slides/index.html">進入教學簡報 <span aria-hidden="true">↗</span></a><a class="btn-secondary" href="wiki/index.html">瀏覽 LLM Wiki</a></div><div class="mini-facts"><div><b>07</b><span>資料來源</span></div><div><b>20</b><span>證據卡</span></div><div><b>10</b><span>教學頁面</span></div></div></div><div class="landing-right"><div class="orbit orbit-a"></div><div class="orbit orbit-b"></div><div class="orbit orbit-c"></div><div class="orbit-title">ETF</div><div class="float-card card-1"><span>01 · FUND</span><strong>一籃子資產</strong></div><div class="float-card card-2"><span>02 · RISK</span><strong>分散 ≠ 保本</strong></div><div class="float-card card-3"><span>03 · PROOF</span><strong>來源可追溯</strong></div><div class="hero-foot">Understand the product. Own the decision.</div></div></main><section class="landing-bottom"><div><span class="section-overline">THE APPROACH</span><h2>不只給答案，也留下證據鏈。</h2></div><p>從可信來源 → Wiki 文章 → 證據卡 → HTML 簡報 → 自動化檢查。每個重要教學主張都能找到對應資料，並保留真實檢查報告。</p></section><footer class="site-foot">教育性內容，不構成個別投資建議。<span>Updated 2026.11.16 · ETF LAB</span></footer></div>'''
(ROOT/'index.html').write_text(shell('ETF LAB｜從零開始學 ETF','assets/site.css',landing),encoding='utf-8')

# wiki: topic index, fully inlined sources, search/filter and anchor navigation
nav=''.join(f'<a class="topic-nav" href="#topic-{t["id"]}"><span>{str(i+1).zfill(2)}</span>{h(t["title"].split("｜",1)[1])}</a>' for i,t in enumerate(topics))
body_topics=[]
for i,t in enumerate(topics):
 parts=[]
 for head,body,eid in t['blocks']:
  ev=evidence[eid]
  parts.append(f'<div class="wiki-paragraph"><h3>{h(head)}</h3><p>{h(body)}</p><div class="wiki-proof"><span>證據卡 {eid}</span> <span class="proof-arrow">→</span> {refs([eid])}</div></div>')
 body_topics.append(f'<article class="wiki-article" id="topic-{t["id"]}" data-search="{h(t["title"]+t["subtitle"]+" ".join(b[1] for b in t["blocks"]))}"><div class="article-head"><span class="article-tag">{h(" / ".join(t["tags"]))}</span><span>{h(t["read"])}閱讀</span></div><h2>{h(t["title"])}</h2><p class="article-desc">{h(t["subtitle"])}</p>{"".join(parts)}</article>')
source_cards=''.join(f'<li class="source-card" id="source-{s["id"]}"><span>{s["id"]}</span><div><strong>{h(s["title"])}</strong><p>{h(s["publisher"])} · {h(s["published"])} · 查核 2026-11-16</p><p>{h(s["summary"])}</p><a href="{h(s["url"])}" target="_blank" rel="noopener noreferrer">查看原始來源 ↗</a></div></li>' for s in sources)
wiki=f'''<div class="wiki-layout"><aside class="wiki-sidebar"><a class="brand" href="../index.html"><span class="brand-icon">E<span>·</span></span><span>ETF LAB <small>LLM WIKI</small></span></a><div class="nav-head">01 — KNOWLEDGE BASE</div><nav aria-label="Wiki 主題">{nav}</nav><div class="nav-head">02 — EVIDENCE</div><a class="topic-nav" href="#sources"><span>↗</span>來源索引 · 7 篇</a><a class="topic-nav" href="../slides/index.html"><span>▶</span>開啟教學簡報</a><p class="side-note">資料以公開官方網站人工核對後整理成摘要，不含原站全文重製。</p></aside><main class="wiki-main"><header class="wiki-top"><a href="../index.html">← 返回首頁</a><a href="../slides/index.html">開始 10 頁教學 <span aria-hidden="true">↗</span></a></header><section class="wiki-hero"><span class="kicker">ETF KNOWLEDGE SYSTEM · VERSION 1.0</span><h1>把複雜的金融知識，<br><em>拆成看得懂的七個主題。</em></h1><p>為一般大眾設計的 ETF 入門 Wiki。每個重要知識點都標記 Evidence ID，與下方來源連結相互對應。</p><div class="search-row"><label class="sr-only" for="topicSearch">搜尋 Wiki 主題</label><input type="search" id="topicSearch" placeholder="搜尋：配息、折溢價、風險…" autocomplete="off"><span id="searchCount" aria-live="polite">顯示 7 / 7 個主題</span></div></section><div id="wikiArticles">{"".join(body_topics)}</div><div id="noResults" class="no-results" hidden>沒有符合的文章。請試試其他關鍵字。</div><section class="sources-section" id="sources"><span class="kicker">SOURCE REGISTER</span><h2>來源索引 <small>07 SOURCES</small></h2><p>每份內容均有發布單位、原始連結與閱讀後的獨立摘要。官方網站可能更新；下單、稅費及商品規定請以最新公告為準。</p><ol class="source-list">{source_cards}</ol></section><footer class="site-foot">教育性內容，不構成個別投資建議。<span>查核日期：2026.11.16</span></footer></main></div><script src="../assets/wiki.js" defer></script>'''
(ROOT/'wiki'/'index.html').write_text(shell('ETF LAB｜可追溯的 ETF Wiki','../assets/site.css',wiki),encoding='utf-8')

# Slides: progressive, source-cited HTML, with no network or external dependencies.
def inner(kind):
 if kind=='cover':
  return '''<div class="cover-art"><div class="disk disk-a"></div><div class="disk disk-b"></div><div class="disk disk-c"></div><div class="cover-letter">E<span>T</span>F</div><div class="cover-label label-one">FUND / 基金</div><div class="cover-label label-two">TRADE / 交易</div><div class="cover-label label-three">LEARN / 學習</div></div><div class="cover-baseline"><span>NO. 01 / FINANCIAL LITERACY</span><span>往右開始探索 →</span></div>'''
 if kind=='roadmap':
  cards=[('01','基本概念','一檔 ETF 究竟是什麼？','book-open'),('02','種類與價格','主動、被動、淨值、溢價','layers'),('03','配息與成本','有領息，為何不一定賺錢？','calculator'),('04','風險與選擇','建立自己的交易前清單','shield')]
  return '<div class="roadmap-grid">'+''.join(f'<div class="roadmap-item"><span class="road-index">{n}</span><div class="road-symbol">{icon}</div><h3>{title}</h3><p>{desc}</p></div>' for n,title,desc,icon in cards)+'</div>'
 if kind=='basket':
  return '''<div class="split"><div class="diagram-basket"><div class="basket-top">一籃子標的 <span>概念示意</span></div><div class="basket-content"><div class="token t1">科技</div><div class="token t2">金融</div><div class="token t3">民生</div><div class="token t4">其他</div></div><div class="basket-label">ETF 基金份額</div></div><div class="text-col"><span class="small-label">THINK OF IT LIKE THIS</span><h3>不是只押一家公司。</h3><p>ETF 可以持有一組股票或其他資產，讓你用一個基金商品參與多個標的。</p><div class="caution">但別忘了：<strong>持股可能仍偏向某個產業。</strong></div></div></div>'''
 if kind=='types':
  return '''<div class="type-grid"><div class="type-panel"><div class="type-number">01 / 被動式</div><h3>追蹤指數</h3><p>依指數規則組合投資，目標是盡量貼近指數表現。</p><div class="tag-pills"><span>指數規則</span><span>追蹤差距</span></div></div><div class="type-panel accent"><div class="type-number">02 / 主動式</div><h3>依策略選擇</h3><p>由投信依既定方針分析、選擇及調整投資組合。</p><div class="tag-pills"><span>經理人決策</span><span>策略風險</span></div></div></div><div class="type-strip"><b>還要看投資標的</b><span>股票</span><span>債券</span><span>多資產</span><span>期貨</span><span>槓桿／反向*</span><small>* 槓桿及反向商品以單日倍數或反向報酬為目標，風險不同。</small></div>'''
 if kind=='mechanism':
  return '''<div class="price-compare"><div class="price-tile"><div class="overline">基金淨值 / NAV</div><strong>20<span>.00</span></strong><p>基金持有資產的每單位淨值</p></div><div class="compare-center">≠<small>兩個價格<br>可能有差</small></div><div class="price-tile focus"><div class="overline">市場價格 / MARKET</div><strong>20<span>.50</span></strong><p>投資人實際買賣的市場成交價</p></div></div><div class="calculation"><span>溢價率（教學假設）</span><b>(20.50 − 20.00) ÷ 20.00 = <em>2.5%</em></b><small>非真實 ETF 報價；市場供需、套利及交易時差都可能造成差異。</small></div>'''
 if kind=='compare':
  return '''<div class="comparison"><div class="comparison-heading"><span>比較面向</span><b>單一公司股票</b><b>持有多標的的 ETF</b></div><div><span>資產內容</span><p>單一公司權益</p><p>一組資產的基金份額</p></div><div><span>主要曝險</span><p>個別公司風險較集中</p><p>可分散部分個股風險*</p></div><div><span>交易方式</span><p>透過證券商下單</p><p>透過證券商下單</p></div><div><span>額外觀察</span><p>公司財報與價格</p><p>持股、費用、NAV 折溢價</p></div></div><div class="bottom-warning">* 不是所有 ETF 都高度分散，仍可能集中投資單一產業；兩者都可能虧損。</div>'''
 if kind=='dividend':
  return '''<div class="dividend-workshop"><div class="dividend-figures"><div class="number-card"><span>除息前價格（假設）</span><b>50<small>元</small></b></div><div class="number-op">→</div><div class="number-card minus"><span>除息參考價</span><b>45<small>元</small></b></div><div class="number-op">＋</div><div class="number-card plus"><span>領到現金分配</span><b>5<small>元</small></b></div></div><div class="dividend-answer"><div><span class="small-label">CALCULATE IT</span><p>45 + 5 = <strong>50 元</strong></p><small>忽略市場變動與交易／稅費的教學示意，不是任何實際ETF的報價。</small></div><button type="button" class="reveal-btn" id="dividendReveal" aria-expanded="false" aria-controls="dividendExplanation">點我看：為什麼不是多賺 5 元？ ↓</button></div><div class="explanation" id="dividendExplanation" hidden>配息是把基金資產的一部分以現金形式交給持有人。判斷投資成果應同時考慮基金價格變化、領取的現金及成本，不能只看配息率。</div></div>'''
 if kind=='costs':
  return '''<div class="cost-grid"><div class="cost-card"><div class="icon-ring">↗</div><h3>買進／賣出</h3><ul><li>券商手續費</li><li>買賣價差（Spread）</li><li>可能的賣出證交稅</li></ul><p>臺灣一般ETF賣出證交稅在規則頁列示 0.1%；特定商品有例外。</p></div><div class="cost-card dark"><div class="icon-ring">◷</div><h3>持有期間</h3><ul><li>基金經理與保管等運作成本</li><li>被動式商品可能有追蹤差距</li><li>費用會反映在淨值表現</li></ul><p>看公開說明書與最新費用揭露，不只看配息率。</p></div></div>'''
 if kind=='risks':
  x=[('01','市場','市場跌，基金也可能跌'),('02','流動性','成交不易、價差可能擴大'),('03','海外','匯率與交易時間差影響'),('04','追蹤與策略','追蹤誤差；槓桿單日倍數')]
  return '<div class="risk-grid">'+''.join(f'<div class="risk-card"><b>{n}</b><h3>{title}</h3><p>{desc}</p></div>' for n,title,desc in x)+'</div><div class="risk-sub">分散投資可降低部分個別標的風險，不能消除市場風險或保證獲利。</div>'
 if kind=='quiz':
  q=[('01','ETF 一定都只是被動追蹤指數嗎？',[('A','是'),('B','不是，還有主動式 ETF')],'B'),('02','領到配息就一定代表總報酬為正嗎？',[('A','不是，要連價格變化一起看'),('B','是，只要領到現金就算賺錢')],'A'),('03','ETF 市價高於 NAV，稱為什麼？',[('A','折價'),('B','溢價')],'B')]
  blocks=''.join(f'<fieldset class="quiz-question" data-answer="{ans}"><legend><span>{num}</span>{h(qq)}</legend><div class="choices">'+''.join(f'<label><input type="radio" name="quiz{num}" value="{val}"><span>{h(label)}</span></label>' for val,label in opts)+'</div></fieldset>' for num,qq,opts,ans in q)
  return f'<div class="final-grid"><div class="quiz-panel"><div class="quiz-title">理解檢查 <span>3 題</span></div>{blocks}<button type="button" class="check-btn" id="quizCheck">檢查答案</button><p class="quiz-result" id="quizResult" role="status" aria-live="polite"></p></div><div class="checklist-panel"><span class="small-label">BEFORE YOU BUY</span><h3>投資前六問</h3><ul><li>我的目的和期限？</li><li>可以承受多少下跌？</li><li>買的是哪種資產／策略？</li><li>持股是否過度集中？</li><li>成本、流動性、折溢價？</li><li>配息以外，總報酬如何？</li></ul><a href="../wiki/index.html" class="wiki-btn">查閱完整 Wiki →</a></div></div>'
 return ''
all_slides=[]
for s in slides:
 n=s['num'];title=h(s['title']).replace('\n','<br>');
 cite_str=refs(s['cite'])
 all_slides.append(f'''<section class="slide {'cover' if n==1 else 'regular'}" id="slide-{n}" data-slide="{n}" aria-label="第 {n} 頁：{h(s['tag'])}" {'hidden' if n!=1 else ''}><div class="slide-main"><div class="slide-head"><span>{h(s['eyebrow'])}</span><span>{h(s['tag'])} <span class="head-sep">/</span> {n:02}—10</span></div><div class="slide-intro"><h1>{title}</h1><p>{h(s['subtitle'])}</p></div>{inner(s['kind'])}<div class="slide-bottom"><p><span class="accent-glyph">✳</span>{h(s['takeaway'])}</p><div class="slide-sources"><span>依據</span>{cite_str}</div></div></div></section>''')
deck=f'''<div class="slide-app"><header class="deck-header"><a class="deck-logo" href="../index.html" aria-label="回到專案首頁">ETF <span>LAB.</span></a><div class="deck-label">AN OPEN LEARNING DECK <span>·</span> NOV 2026</div><a href="../wiki/index.html" class="deck-wiki">開啟 Wiki <span aria-hidden="true">↗</span></a></header><main id="deck" tabindex="-1">{''.join(all_slides)}</main><nav class="deck-controls" aria-label="簡報控制"><button type="button" id="prevBtn" aria-label="上一頁" disabled>← <span>上一頁</span></button><div class="progress"><div class="progress-track"><div id="progressFill"></div></div><span class="progress-label" id="progressText">01 <i>/</i> 10</span></div><button type="button" id="nextBtn" aria-label="下一頁"><span>下一頁</span> →</button></nav><div class="keyboard-hint">← → 切換頁面 · <a href="../wiki/index.html">閱讀來源</a></div></div>'''
(ROOT/'slides'/'index.html').write_text(shell('ETF 入門｜10 頁互動 HTML 教學簡報','style.css',deck,'script.js'),encoding='utf-8')
print('Rendered: landing page, Wiki site, 10 offline slide sections')

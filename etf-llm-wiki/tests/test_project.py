"""Offline verifiable content and provenance tests for ETF LLM Wiki."""
from pathlib import Path
import json, re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
SRC=load('data/sources.json'); EVD=load('cards/evidence.json'); TOP=load('data/topics.json'); SLIDES=load('data/slides.json')
def test_ingest_count_and_raw_source_records():
 assert len(SRC)>=5
 assert len({s['url'] for s in SRC})==len(SRC)
 assert len(list((ROOT/'raw').glob('S*.md')))==len(SRC)
 assert len(EVD)>=10
 for src in SRC:
  assert src['url'].startswith('https://')
  assert 'twse.com.tw' in src['url']
  assert src['id'] in (ROOT/'sources.md').read_text(encoding='utf-8')
def test_evidence_card_sources_traceable():
 ids={s['id'] for s in SRC};eid={x['id'] for x in EVD}
 assert len(eid)==len(EVD)
 for e in EVD:
  assert e['sources'] and set(e['sources']).issubset(ids)
 for topic in TOP:
  assert (ROOT/'wiki/topics'/f'{topic["id"]}.md').exists()
  for block in topic['blocks']:
   assert block[2] in eid
 for slide in SLIDES:
  assert slide['cite'] and set(slide['cite']).issubset(eid)
def test_html_has_full_deck_and_readable_wiki():
 bs=BeautifulSoup((ROOT/'slides/index.html').read_text(encoding='utf-8'),'html.parser')
 slides=bs.select('.slide')
 assert len(slides)==10
 assert [int(x.get('data-slide')) for x in slides]==list(range(1,11))
 assert all(x.select('.source-link') for x in slides)
 assert len(bs.select('#quizCheck'))==1
 assert len(bs.select('#dividendReveal'))==1
 wb=BeautifulSoup((ROOT/'wiki/index.html').read_text(encoding='utf-8'),'html.parser')
 assert len(wb.select('.wiki-article'))==len(TOP)
 assert len(wb.select('.source-card'))==len(SRC)
 assert len(wb.select('.wiki-proof'))==sum(len(t['blocks']) for t in TOP)
def test_local_links_and_source_links():
 for f in [ROOT/'index.html',ROOT/'wiki/index.html',ROOT/'slides/index.html']:
  page=BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser')
  for tag in page.select('a[href],link[href],script[src]'):
   dest=tag.get('href',tag.get('src',''))
   if dest.startswith(('http:','https:','#','mailto:','javascript:')):continue
   target=(f.parent/dest.split('#')[0]).resolve()
   assert target.exists(),f'{f.name} missing {dest}'
def test_finance_corrections_present():
 deck=(ROOT/'slides/index.html').read_text(encoding='utf-8')
 for phrase in ('主動式','被動式','配息','溢價','費用','風險','不保證'):
  assert phrase in deck
 assert '沒有風險' not in deck

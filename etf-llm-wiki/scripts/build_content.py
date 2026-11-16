#!/usr/bin/env python3
"""Deterministic offline ingest: verified external source notes -> evidence cards -> Wiki.
This does not download/republish copyrighted external webpages. Source URLs and
original summaries are retained, with citations to corresponding sections.
"""
from pathlib import Path
import json, datetime, re
ROOT=Path(__file__).resolve().parent.parent
DATE='2026-11-16'
SOURCES=[
 dict(id='S01',title='ETF 總覽：定義、種類、風險',publisher='臺灣證券交易所 TWSE',published='網站動態更新',url='https://www.twse.com.tw/zh/products/securities/etf/overview/introduction.html',section='ETF定義、種類；ETF風險', summary='ETF 為在交易所上市的基金；可於盤中買賣。現今有被動式與主動式ETF；按投資標的區分股票、債券、多資產、期貨與槓桿反向商品，風險結構不同。',tags=['定義','類型','風險']),
 dict(id='S02',title='ETF 交易規則',publisher='臺灣證券交易所 TWSE',published='網站動態更新',url='https://www.twse.com.tw/zh/products/securities/etf/overview/rules.html',section='交易方式；交易單位；交易成本',summary='臺灣上市新台幣ETF一般可透過證券戶交易；一般一張為1000受益權單位，ETF賣方證交稅原則上0.1%，但商品及期間可能有免稅例外，使用前應查最新規定。',tags=['交易','費用']),
 dict(id='S03',title='證交所投資人知識網：ETF 問答',publisher='臺灣證券交易所 投資人知識網',published='網站動態更新，部分問答可能較舊',url='https://investoredu.twse.com.tw/pages/TWSE_InvestmentQA.aspx?ID=11',section='ETF 問答：配息、買賣成本、零股交易、ETF與股票差異',summary='ETF配息依發行商公開說明書及公告，配息不保證；可在證交所查詢收益分配。證交所問答說明交易手續費、證交稅及零股交易，適用費率需核對現行規定。',tags=['配息','費用','比較']),
 dict(id='S04',title='ETF投資風險',publisher='臺灣證券交易所 投資人知識網',published='網站動態更新',url='https://investoredu.twse.com.tw/Pages/TWSE_InvestmentEntry2_6.aspx?ID=2',section='ETF一般投資風險；追蹤誤差',summary='被動式ETF面臨指數波動、市場、流動性、折溢價和追蹤誤差風險；投資海外資產需另外考慮匯率與交易時間差。',tags=['風險']),
 dict(id='S05',title='槓桿型及反向型 ETF',publisher='臺灣證券交易所 TWSE',published='網站動態更新',url='https://www.twse.com.tw/zh/products/securities/etf/products/li.html',section='商品特性及風險',summary='槓桿及反向ETF追求的是標的指數「單日」的正向倍數或反向報酬，因每日調整和複利效果，長期持有不會等於指數長期報酬的簡單倍數。',tags=['類型','風險']),
 dict(id='S06',title='金管會提醒投資 ETF 應考量自身投資需求及瞭解商品特性',publisher='金融監督管理委員會（臺灣證券交易所轉載）',published='2023-11-08',url='https://www.twse.com.tw/zh/ETFortune/newsDetail/ff8080818b7e232e018bacd925a600f9',section='商品特性、折溢價及選擇因素',summary='選擇ETF時應考量投資目標與風險承受度，查投資標的、追蹤差距、買賣價差、流動性與折溢價。不同投資策略及配息頻率不能直接比較優劣。',tags=['選擇方法','費用','風險']),
 dict(id='S07',title='ETF折溢價：市場熱潮下容易忽略的投資成本',publisher='臺灣證券交易所 ETF e添富',published='2026-06-03',url='https://www.twse.com.tw/zh/ETFortune/invest/8a8216d69e6379f4019e87050e710106',section='折溢價定義、套利機制、價差擴大成因',summary='ETF市價與基金淨值可能不同，市價高於淨值為溢價、低於淨值為折價。投資情緒、跨市場時間差與流動性可能放大偏離，應留意買入價格。',tags=['定價','風險']),
]
EVIDENCE=[
 ('E01','ETF 是可在證券交易所掛牌買賣的基金；有基金屬性、也能像股票透過券商交易。',['S01'],'ETF定義'),
 ('E02','不是所有ETF都被動追蹤指數：現有被動式與主動式ETF，主動式由經理人依策略選擇資產。',['S01'],'ETF種類：管理方式'),
 ('E03','ETF可依投資資產或策略分為股票、債券、多資產、期貨、槓桿與反向等；不同類型風險不同。',['S01','S05'],'ETF種類'),
 ('E04','買一檔股票是承擔該公司風險；一檔持有多個標的的ETF可分散個別公司風險，但仍可能集中於某產業或少數公司。',['S01'],'ETF風險：集中度'),
 ('E05','上市ETF一般可透過證券帳戶於交易時間買賣，實際成交價受市場供需影響。',['S01','S02'],'ETF定義；交易方式'),
 ('E06','ETF有市價與資產淨值（NAV）；溢價是市價高於淨值，折價是市價低於淨值。',['S07','S06'],'折溢價定義'),
 ('E07','ETF可使用申購／買回、造市與套利機制使市價向淨值靠攏，但不保證無折溢價。',['S01','S07'],'市場機制'),
 ('E08','ETF配息不是額外憑空增加的報酬；評估績效應連同價格變動一起看總報酬。',['S03','S06'],'配息；投資需求'),
 ('E09','各檔ETF的配息規定、頻率與組成不同，應查投信公開說明書及收益分配公告；配息不保證。',['S03'],'ETF配息資訊'),
 ('E10','一般ETF買賣可能涉及券商手續費與賣出時證交稅；費率及例外應以商品與最新規定為準。',['S02','S03'],'交易成本'),
 ('E11','基金運作費用和買賣價差都會影響投資人的實際報酬，不能只看表面的配息數字。',['S01','S06'],'追蹤誤差原因；買賣價差'),
 ('E12','ETF仍有市場風險，標的資產大跌時基金可能下跌；分散投資不能保證不虧。',['S04','S01'],'一般投資風險'),
 ('E13','流動性不足可能造成不易成交、買賣價差較大；成交量和報價也值得檢查。',['S04','S06'],'流動性風險'),
 ('E14','海外資產ETF還可能受到匯率波動與境內外交易時間差影響。',['S01','S04'],'海外ETF其他風險'),
 ('E15','被動式ETF可能有追蹤誤差；基金費用、持股差異等可造成基金報酬與指數不完全相同。',['S04','S01'],'追蹤誤差風險'),
 ('E16','槓桿／反向ETF主要追求標的的單日倍數或反向報酬，並不等於長期累積報酬的倍數。',['S05'],'槓桿反向產品特性'),
 ('E17','選擇ETF應先想投資目標、可承受風險、資產類型、標的／策略，再比較總成本、流動性、折溢價。',['S06'],'投資需求與產品／市場資訊'),
 ('E18','ETF不能只因「高配息」或「熱門」就認定適合；需要查配息來源、風險與總報酬。',['S03','S06'],'配息及商品選擇'),
 ('E19','ETF賣出時證交稅在證交所規則頁對一般ETF記載0.1%，部分如特定債券ETF的免稅規定具有期間／品項限制，不能一概套用。',['S02'],'交易成本及免稅附註'),
 ('E20','ETF的完整市場報酬比較宜同時考慮市價變化與分配現金，若計入費用與稅負，淨報酬會不同。',['S03','S06'],'配息與交易成本'),
]
TOPICS=[
 dict(id='basics',title='01｜ETF 到底是什麼？',subtitle='從一籃子資產理解交易所交易基金',read='3 分鐘',tags=['定義','概念'],blocks=[
  ('什麼是 ETF？','ETF 是 Exchange-Traded Fund（交易所交易基金）。它是「基金」，但掛牌後可以像股票一樣，在交易時間透過券商買賣。','E01'),
  ('生活比喻','買一家公司股票像只選一道菜；投資持有多檔標的的 ETF，比較像選一份組合餐。但組合餐仍可能偏重一類食材——ETF 也可能集中在同一產業。','E04'),
  ('別混淆兩種管理方式','被動式 ETF 設法追蹤指數；主動式 ETF 則由投信依策略主動選擇資產。不能把所有 ETF 都說成「只能追蹤指數」。','E02'),
 ]),
 dict(id='types',title='02｜ETF 的種類與策略',subtitle='股票、債券、多資產與策略型產品',read='4 分鐘',tags=['類型','策略'],blocks=[
  ('依投資標的分類','常見有股票 ETF、債券 ETF、多資產 ETF，也有連結期貨等商品。ETF 是交易方式與基金結構的統稱，不是單一風險程度。','E03'),
  ('依管理方式分類','被動式 ETF 以追蹤指數為目標；主動式 ETF 依投資方針選擇持有標的，兩者都會受到市場風險影響。','E02'),
  ('槓桿與反向商品特別注意','槓桿及反向 ETF 追求每日的倍數或反向報酬，長期結果會受到每日調整及複利路徑影響，初學者不宜把它當成一般長期指數投資。','E16'),
 ]),
 dict(id='compare',title='03｜ETF 和個股、傳統基金差在哪？',subtitle='比較曝險方式、交易方式和可能風險',read='3 分鐘',tags=['比較','入門'],blocks=[
  ('持有內容','個股對應單一公司；持有多檔證券的 ETF 可分散公司特定風險，但如果ETF集中於單一產業，依然有集中風險。','E04'),
  ('買賣方式','上市 ETF 可以透過證券戶在市場交易時間買賣，成交價由買賣雙方決定。','E05'),
  ('價格與淨值','ETF 同時有「市場成交價」及代表基金資產價值的「淨值」。兩者可能有差，形成折價或溢價。','E06'),
 ]),
 dict(id='mechanism',title='04｜ETF 如何運作、如何定價？',subtitle='市場價格、淨值與折溢價',read='4 分鐘',tags=['運作','折溢價'],blocks=[
  ('兩個價格','NAV（Net Asset Value）是基金的資產淨值；市價是市場實際成交價。市價高於 NAV 為溢價；低於 NAV 為折價。','E06'),
  ('為什麼不是永遠相等？','供需、交易時差與資產流動性都會使兩個價格暫時偏離。市場有申購買回與套利等機制，可能縮小差距，但不保證完全消除。','E07'),
  ('示意計算','假設淨值每單位 20 元，市場價 20.5 元，溢價率 = (20.5 - 20) ÷ 20 = 2.5%。這只是教學假設，不代表任何真實ETF報價。','E06'),
 ]),
 dict(id='dividends',title='05｜ETF 配息不等於賺錢',subtitle='分配現金、除息與總報酬',read='4 分鐘',tags=['配息','總報酬'],blocks=[
  ('配息是什麼？','部分 ETF 會把基金可分配的收益以現金方式發給投資人；是否配息、何時配息，需看基金規定及公告，不保證固定發放。','E09'),
  ('教學算例：現金不會憑空增加','假設除息前每單位 50 元，除息參考價調整為 45 元，領到 5 元現金，忽略其他市場變動與稅費時，45 + 5 = 50 元；不能只看領到 5 元就說賺了 10%。這是簡化示意。','E08'),
  ('看總報酬而不是只看殖利率','簡化概念：總報酬率 = （期末市值 − 期初投入 ＋ 期間已領現金分配）÷ 期初投入。若計入稅費、再投資時點等，實際淨報酬另有差異。','E20'),
 ]),
 dict(id='costs',title='06｜ETF 有哪些成本？',subtitle='交易成本與基金持有成本都要看',read='3 分鐘',tags=['費用','交易'],blocks=[
  ('交易時','買賣可能支付券商手續費、買賣價差；依商品類型，賣出也可能有證交稅。費率、特例和適用期間應查最新官方公告。','E10'),
  ('持有期間','基金內部運作費用（例如經理／保管等費用）會影響淨值和實際表現，不會因為帳戶沒有直接扣款就不存在。','E11'),
  ('不要直接套舊費率','證交所規則頁對一般ETF列有賣方證交稅 0.1% 等資訊；個別品種與免稅期間有例外，實際交易須再次確認。','E19'),
 ]),
 dict(id='risks',title='07｜風險、選擇與常見迷思',subtitle='初學者做決定前的安全檢查',read='5 分鐘',tags=['風險','選擇'],blocks=[
  ('市場風險和集中度','ETF 不是保本商品；如果市場下跌，ETF 也可能下跌。分散多家公司，不代表整體市場或產業風險消失。','E12'),
  ('流動性、匯率、追蹤誤差','買賣價差可能較大；海外 ETF 可能受匯率與時差影響；被動式 ETF 的報酬也可能和指數有差距。','E13'),
  ('選擇前六問','目的與期限？承受下跌的程度？投資什麼資產？基金策略及持股集中嗎？總成本和折溢價合理嗎？配息與總報酬看清楚了嗎？','E17'),
  ('迷思提醒','高配息未必高總報酬；熱門未必適合；槓桿 ETF 的每日倍數不等於長期倍數；買前先理解來源和風險。','E18'),
 ]),
]
SLIDES=[
 dict(num=1,kind='cover',eyebrow='FINANCE BASICS · 01',title='把投資變得\n比較好理解。',subtitle='ETF 投資入門 · 從零開始的 10 頁微課程',takeaway='你不用先懂金融，也能建立選擇 ETF 的基本判斷力。',cite=['E01'],tag='入門導覽'),
 dict(num=2,kind='roadmap',eyebrow='LEARNING PATH',title='10 分鐘，先學會這 4 件事',subtitle='先懂商品，再學會識別風險與費用',takeaway='不是教你買哪一檔，而是教你怎麼判斷。',cite=['E17'],tag='學習目標'),
 dict(num=3,kind='basket',eyebrow='01 / THE IDEA',title='ETF = 可以在市場交易的基金',subtitle='一個商品，可以裝進多種資產',takeaway='「一籃子」不代表「一定安全」；有些 ETF 持股仍很集中。',cite=['E01','E04'],tag='基本概念'),
 dict(num=4,kind='types',eyebrow='02 / THE TYPES',title='同樣叫 ETF，內容可能差很多',subtitle='先分清「投資什麼」與「如何管理」',takeaway='目前已有主動式 ETF；並非所有 ETF 都只追蹤指數。',cite=['E02','E03','E16'],tag='商品種類'),
 dict(num=5,kind='mechanism',eyebrow='03 / THE MECHANISM',title='為什麼 ETF 會有兩種價格？',subtitle='市價與淨值，是交易前的兩個檢查點',takeaway='溢價代表買得比淨值貴；不代表一定馬上回跌，但需要留意。',cite=['E05','E06','E07'],tag='運作機制'),
 dict(num=6,kind='compare',eyebrow='04 / THE COMPARE',title='ETF 跟單一股票差在哪？',subtitle='一個是公司，一個是基金組合',takeaway='ETF 能分散部分個股風險，但無法消除市場下跌的可能。',cite=['E04','E12'],tag='商品比較'),
 dict(num=7,kind='dividend',eyebrow='05 / THE DIVIDEND',title='領到配息，不等於多賺一筆',subtitle='看懂「現金流」與「總報酬」',takeaway='ETF 配息不保證；真正要比較的是價格變化＋領到的現金分配，再扣除相關成本。',cite=['E08','E09','E20'],tag='配息與績效'),
 dict(num=8,kind='costs',eyebrow='06 / THE COST',title='ETF 的成本，不只交易手續費',subtitle='下單前與持有期間，費用都可能發生',takeaway='費率與免稅例外可能改變；請查最新規定和公開說明書。',cite=['E10','E11','E19'],tag='交易費用'),
 dict(num=9,kind='risks',eyebrow='07 / THE RISKS',title='分散投資 ≠ 不會虧損',subtitle='看風險，才知道自己買的是什麼',takeaway='海外、集中度、流動性與特殊策略都會改變風險。',cite=['E12','E13','E14','E15','E16'],tag='風險辨識'),
 dict(num=10,kind='quiz',eyebrow='FINAL / YOUR TURN',title='現在，換你做判斷。',subtitle='3 題快速自我檢查＋投資前 6 問',takeaway='投資前，先把「目的、標的、風險、費用、價格、配息」都查清楚。',cite=['E17','E18'],tag='知識測驗'),
]
def safe(s):return s.replace('|','\\|')

def render_note(src):
 return f"""# Ingested source note {src['id']} | {src['title']}\n\n> 來源記錄不是全文轉載。以下為本專案閱讀原網頁後的**獨立摘要與證據抽取**；請點開原始頁面核對。\n\n- 編號：{src['id']}\n- 發布單位：{src['publisher']}\n- 網頁名稱：{src['title']}\n- 網址：{src['url']}\n- 網頁日期：{src['published']}\n- 本次讀取：{DATE}\n- 對應段落：{src['section']}\n- 運用主題：{', '.join(src['tags'])}\n\n## 自行整理的重點（非原文複製）\n\n{src['summary']}\n\n## Ingest 說明\n\n1. 確認原始公開網頁和發布單位。\n2. 摘取相關事實作為可追溯證據（見 `cards/evidence.json`）。\n3. 將證據組織到 `wiki/topics/`，並指定對應簡報頁面。\n4. 若原始頁面有更新，以最新官方內容重新核對。\n"""
def md_topic(t,evidence):
 lines=[f"# {t['title']}","",f"> {t['subtitle']} · 預估閱讀 {t['read']}","", "*讀者：完全沒有金融基礎的一般民眾。非個別投資建議。*",""]
 for head,body,eid in t['blocks']:
  e=evidence[eid];links=', '.join(f"[{sid}](../../sources.md#{sid.lower()})" for sid in e['sources'])
  lines.extend([f"## {head}","",body,"",f"**資料依據：** {links} · 證據卡 `{eid}`（{e['anchor']}）"," "])
 lines.extend(["## 延伸閱讀","",'請參照 [完整來源索引](../../sources.md)，核對原始網站的最新資料。',""])
 return '\n'.join(lines)

def run():
 evid={eid:{'id':eid,'claim':claim,'sources':src,'anchor':anchor} for eid,claim,src,anchor in EVIDENCE}
 source_ids={s['id'] for s in SOURCES}
 assert len(SOURCES)>=5 and all(set(e['sources'])<=source_ids for e in evid.values())
 for s in SOURCES:(ROOT/'raw'/f"{s['id']}-{re.sub('[^a-zA-Z0-9]','-',s['title'])[:28].strip('-')}.md").write_text(render_note(s),encoding='utf-8')
 (ROOT/'data'/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'cards'/'evidence.json').write_text(json.dumps(list(evid.values()),ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'data'/'topics.json').write_text(json.dumps(TOPICS,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'data'/'slides.json').write_text(json.dumps(SLIDES,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'wiki'/'index.md').write_text('# ETF 投資入門 LLM Wiki\n\n以臺灣證券交易所及金管會公開教育資料為主要依據，閱讀原始資料後整理出的可追溯知識庫。\n\n'+ '\n'.join(f"- [{t['title']}](topics/{t['id']}.md) — {t['subtitle']}" for t in TOPICS) +'\n\n## 使用方式\n\n先讀 `sources.md`，再用 `cards/evidence.json` 對應重要敘述；教學簡報以其內的 E 編號標示每一頁資料來源。\n',encoding='utf-8')
 for t in TOPICS:(ROOT/'wiki'/'topics'/f"{t['id']}.md").write_text(md_topic(t,evid),encoding='utf-8')
 sourcesmd='# 來源索引（至少 5 篇）\n\n本專案於 '+DATE+' 檢視公開網頁共 '+str(len(SOURCES))+' 篇，手動驗證、轉寫為獨立摘要與 evidence cards；不是全文爬蟲或原文全文下載。\n\n'
 for s in SOURCES:
  sourcesmd+=f"<a id=\"{s['id'].lower()}\"></a>\n## {s['id']}｜{s['title']}\n\n- 發布單位：{s['publisher']}\n- 網頁日期：{s['published']}｜查核：{DATE}\n- 原始頁面：{s['url']}\n- 依據段落：{s['section']}\n- 自行摘要：{s['summary']}\n\n"
 (ROOT/'sources.md').write_text(sourcesmd,encoding='utf-8')
 (ROOT/'reports'/'ingest-log.json').write_text(json.dumps({'ingested_at':DATE,'method':'read and verify public official pages; curated structured summary, not raw copyrighted full-text','count':len(SOURCES),'sources':[{k:s[k] for k in ('id','url','title','section')} for s in SOURCES],'evidence_count':len(evid),'topic_count':len(TOPICS)},ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'Ingest complete: {len(SOURCES)} sources -> {len(evid)} evidence cards -> {len(TOPICS)} Wiki topics')
if __name__=='__main__':run()

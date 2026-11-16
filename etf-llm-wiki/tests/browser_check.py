"""Real Chromium smoke test; saves timestamped artifacts and truthful outcomes."""
from pathlib import Path
from datetime import datetime, timezone
import json,sys,threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports'/'screenshots';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,cond,detail=''):
 checks.append(dict(name=name,passed=bool(cond),detail=detail))
 if not cond:errors.append(name)

def main():
 class QuietHandler(SimpleHTTPRequestHandler):
  def log_message(self, *args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 base=f'http://127.0.0.1:{server.server_address[1]}'
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  desktop=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1)
  page=desktop.new_page();js=[]
  page.on('pageerror',lambda exc:js.append(str(exc)))
  page.goto(base+'/slides/index.html');page.wait_for_timeout(250)
  check('desktop: initial cover visible',page.locator('#slide-1').is_visible())
  check('desktop: exactly 1 visible page',page.locator('.slide:visible').count()==1)
  page.screenshot(path=str(OUT/'01-cover-desktop.png'))
  page.locator('#nextBtn').click()
  check('desktop: next page clickable',page.locator('#slide-2').is_visible())
  page.keyboard.press('ArrowRight')
  check('desktop: keyboard arrow navigation',page.locator('#slide-3').is_visible())
  page.keyboard.press('End')
  check('desktop: End moves to last slide',page.locator('#slide-10').is_visible())
  check('desktop: Next disabled at final slide',page.locator('#nextBtn').is_disabled())
  page.screenshot(path=str(OUT/'10-quiz-desktop.png'))
  page.locator('#quizCheck').click()
  check('quiz: incomplete answers trigger prompt','請先完成' in page.locator('#quizResult').inner_text())
  for i,answer in [(1,'B'),(2,'A'),(3,'B')]:page.locator(f'input[name=quiz0{i}][value={answer}]').check()
  page.locator('#quizCheck').click()
  check('quiz: all 3 correct scored','3 / 3' in page.locator('#quizResult').inner_text())
  page.keyboard.press('Home')
  check('desktop: Home moves to first',page.locator('#slide-1').is_visible())
  page.goto(base+'/slides/index.html'+'#slide-7')
  check('deep-link opens slide 7',page.locator('#slide-7').is_visible())
  page.locator('#dividendReveal').click()
  check('dividend: interactive explanation opens',page.locator('#dividendExplanation').is_visible())
  page.screenshot(path=str(OUT/'07-dividend-desktop.png'))
  page.goto(base+'/wiki/index.html');page.wait_for_timeout(150)
  check('wiki: 7 topic articles',page.locator('.wiki-article').count()==7)
  check('wiki: 7 source cards',page.locator('.source-card').count()==7)
  page.locator('#topicSearch').fill('配息')
  check('wiki: searching filters topic articles',page.locator('.wiki-article:visible').count()<7 and page.locator('.wiki-article:visible').count()>0)
  page.screenshot(path=str(OUT/'wiki-desktop.png'),full_page=True)
  mobile=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
  mp=mobile.new_page();mp.on('pageerror',lambda exc:js.append(str(exc)))
  for n in [1,3,4,5,7,8,9,10]:
   mp.goto(base+'/slides/index.html'+f'#slide-{n}')
   mp.wait_for_timeout(50)
   metrics=mp.locator(f'#slide-{n} .slide-main').evaluate('el => ({sh:el.scrollHeight,ch:el.clientHeight,sw:el.scrollWidth,cw:el.clientWidth})')
   check(f'mobile: slide {n} no horizontal overflow',metrics['sw']<=metrics['cw']+3,str(metrics))
   check(f'mobile: slide {n} no vertical clipping',metrics['sh']<=metrics['ch']+5,str(metrics))
  mp.screenshot(path=str(OUT/'10-quiz-mobile.png'))
  mp.goto(base+'/wiki/index.html');mp.wait_for_timeout(100)
  mm=mp.evaluate('({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth})')
  check('mobile: wiki no horizontal overflow',mm['sw']<=mm['cw']+3,str(mm))
  mp.screenshot(path=str(OUT/'wiki-mobile.png'))
  check('browser: no page JavaScript exceptions',not js,'; '.join(js[:10]))
  browser.close()
 server.shutdown()
 summary={'executed_at':datetime.now(timezone.utc).isoformat(),'browser':'Chromium headless','modes':['desktop 1440x900','mobile 390x844'],'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'failures':errors,'js_errors':js}
 (ROOT/'reports'/'browser-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 for c in checks:print(('PASS' if c['passed'] else 'FAIL'),c['name'],c['detail'] if not c['passed'] else '')
 print(f'BROWSER: {summary["passed"]}/{summary["total"]} passed')
 return 0 if not errors else 1
if __name__=='__main__':
 try:sys.exit(main())
 except Exception as exc:
  reason=str(exc)
  blocked='ERR_BLOCKED_BY_ADMINISTRATOR' in reason
  record={'status':'blocked_by_environment_policy' if blocked else 'failed_before_completion',
          'reason':reason[:1500], 'passed':0, 'completed':False,
          'browser':'Chromium', 'note':'No visual or browser-interaction claim is made.'}
  (ROOT/'reports'/'browser-results.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
  print('BROWSER NOT COMPLETED:',record['status'])
  sys.exit(2)

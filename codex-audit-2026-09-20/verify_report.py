from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json,hashlib,re

out=Path(__file__).resolve().parent
report=out/'AUDIT_REPORT.html'
data=json.loads((out/'findings.json').read_text(encoding='utf8'))
raw=report.read_text(encoding='utf8')
soup=BeautifulSoup(raw,'html.parser')
ids=[t['id'] for t in soup.find_all(id=True)]
assert len(ids)==len(set(ids)), 'Duplicate report anchor'
bad=[]
for a in soup.find_all('a',href=True):
 href=a['href']
 if re.match(r'^[a-z]+:',href):continue
 dest,_,anchor=href.partition('#')
 target=out/dest if dest else report
 if not target.exists():bad.append(href)
 elif anchor and target.suffix=='.html':
  ts=soup if not dest else BeautifulSoup(target.read_text(encoding='utf8'),'html.parser')
  if not ts.find(id=anchor):bad.append(href)
assert not bad,bad
for f in data['content']:
 assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',f['replacement']),f['id']
assert len(soup.select('.finding'))==40
assert len(soup.select('.prose-edit'))==48

result={'report_findings':40,'prose_edits':48,'duplicate_ids':0,'broken_report_links':bad}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1060},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 page.goto(report.as_uri(),wait_until='networkidle',timeout=60000)
 page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise',timeout=30000)
 page.evaluate('async()=>{await MathJax.startup.promise}')
 result['mathjax_error_count']=page.locator('[data-mml-node="merror"],mjx-merror').count()
 result['mathjax_container_count']=page.locator('mjx-container').count()
 assert result['mathjax_error_count']==0
 assert result['mathjax_container_count']>100
 assert page.locator('.finding:visible').count()==40
 page.select_option('#module-filter','12')
 expected=sum(x['module']==12 for x in data['content'])
 assert page.locator('.finding:visible').count()==expected
 page.select_option('#severity-filter','Blocking')
 assert page.locator('.finding:visible').count()==2
 page.click('#reset')
 assert page.locator('.finding:visible').count()==40
 result['filter_checks']='passed'
 page.evaluate('window.scrollTo(0,0)')
 page.screenshot(path=str(out/'report-desktop.png'))
 page.locator('#C03').scroll_into_view_if_needed()
 page.screenshot(path=str(out/'report-finding.png'))
 page.set_viewport_size({'width':390,'height':844})
 page.evaluate('window.scrollTo(0,0)')
 page.screenshot(path=str(out/'report-mobile.png'))
 result['mobile_horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth > innerWidth')
 assert not result['mobile_horizontal_overflow']
 result['javascript_errors']=errors
 assert not errors
 browser.close()
result['report_sha256']=hashlib.sha256(report.read_bytes()).hexdigest()
(out/'report-validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, json, hashlib
import fitz

out = Path(__file__).parent / 'sources'
out.mkdir(exist_ok=True)
sources = {
 'marrone2007': 'https://arxiv.org/pdf/astro-ph/0611791',
 'zhuravleva2019': 'https://arxiv.org/pdf/1906.06346',
 'kandori2005': 'https://arxiv.org/pdf/astro-ph/0506205',
 'troland2008': 'https://arxiv.org/pdf/0802.2253',
 'king2007': 'https://arxiv.org/pdf/astro-ph/0701803',
 'venzheimer2018': 'https://arxiv.org/pdf/1711.07534',
}
def fetch(item):
 key, url = item
 try:
  req = urllib.request.Request(url, headers={'User-Agent': 'Codex textbook editorial audit'})
  data = urllib.request.urlopen(req, timeout=45).read()
  if not data.startswith(b'%PDF'): raise ValueError('Not a PDF')
  (out / (key+'.pdf')).write_bytes(data)
  doc=fitz.open(stream=data,filetype='pdf')
  txt='\n'.join(f'\n=== PDF PAGE {i+1} ===\n'+p.get_text() for i,p in enumerate(doc))
  (out/(key+'.txt')).write_text(txt,encoding='utf-8')
  return {'id':key,'url':url,'pages':len(doc),'sha256':hashlib.sha256(data).hexdigest(),'status':'downloaded and extracted; passages require reading'}
 except Exception as e: return {'id':key,'url':url,'error':str(e)}
results=list(ThreadPoolExecutor(max_workers=4).map(fetch,sources.items()))
(out/'source-manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))

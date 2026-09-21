from bs4 import BeautifulSoup
from pathlib import Path
out=Path('codex-audit-2026-09-20')
for p in sorted(Path('afd').glob('module*.html')):
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for x in s(['script','style','svg','nav','details','pre']):x.decompose()
 for x in s.select('.proof'):x.decompose()
 lines=[]
 for x in s.find_all(['h1','h2','h3','p','figcaption','tr']):
  if x.find_parent(['p','tr','figcaption']):continue
  t=x.get_text(' ',strip=True)
  if t:lines.append(str(x.sourceline)+': '+t)
 (out/(p.stem+'-narrative.txt')).write_text('\n'.join(lines),encoding='utf-8')
 print(p.stem,len(' '.join(lines).split()))

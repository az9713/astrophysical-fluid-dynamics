from pathlib import Path
import hashlib,json,re,subprocess
from bs4 import BeautifulSoup
root=Path.cwd(); out=root/'codex-audit-2026-09-20'
files={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts and out.name not in p.relative_to(root).parts}
(out/'original-file-hashes.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
(out/'initial-git-status.txt').write_text(subprocess.check_output(['git','status','--short'],text=True),encoding='utf-8')
stats=[]
for p in sorted((root/'afd').glob('module*.html')):
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for tag in s(['script','style','svg','nav']): tag.decompose()
 blocks=[]
 for tag in s.find_all(['h1','h2','h3','h4','p','li','tr','summary','figcaption','div']):
  if tag.name=='div' and (tag.find(['p','div','h2','h3','table','ul','ol']) or not tag.get('class')): continue
  if tag.find_parent(['p','li','tr','summary','figcaption']): continue
  txt=tag.get_text(' ',strip=True)
  if txt: blocks.append(f'{tag.sourceline}: '+txt)
 (out/(p.stem+'-reading.txt')).write_text('\n'.join(blocks),encoding='utf-8')
 stats.append({'file':p.name,'lines':len(p.read_text(encoding='utf-8').splitlines()),'words':len(s.get_text(' ',strip=True).split()),'blocks':len(blocks),'headings':[(x.sourceline,x.get_text(' ',strip=True)) for x in s.find_all(['h1','h2'])]})
(out/'coverage-inventory.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print(json.dumps(stats,indent=2))
print('Snapshot files:',len(files))

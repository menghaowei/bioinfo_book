#!/usr/bin/env python3
"""Validate book structure, local HTML dependencies, anchors, and migrated headings.

Uses only Python's standard library. External scientific links are preserved but
not crawled. Checks rendered content and assets, not analysis-code correctness.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs'
manifest=json.loads((ROOT/'scripts/validation-manifest.json').read_text())
errors=[];warnings=[]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.duplicates=[];self.h2=0;self.imgs=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):
   if a['id'] in self.ids:self.duplicates.append(a['id'])
   self.ids.add(a['id'])
  if tag=='h2':self.h2+=1
  if tag=='img':self.imgs+=1
  for key in ('href','src','poster'):
   if a.get(key):self.links.append((tag,key,a[key]))
pages={}
for p in OUT.rglob('*.html'):
 parser=Page();parser.feed(p.read_text());pages[p.resolve()]=parser
 for d in parser.duplicates:errors.append(f'Duplicate anchor: {p.relative_to(OUT)}#{d}')
 if re.search(r'(?<![\w])\?\?(?:\s*</|\s*fig|\s*sec|\s*eq)',p.read_text()):errors.append(f'Unresolved Quarto reference: {p.relative_to(OUT)}')
for p,parser in pages.items():
 for tag,key,link in parser.links:
  u=urlsplit(link)
  if u.scheme or u.netloc or link.startswith(('data:','javascript:')):continue
  if not u.path:target=p
  elif u.path.startswith('/bioinfo_book/'):target=(OUT/u.path.removeprefix('/bioinfo_book/')).resolve()
  elif u.path.startswith('/'):target=(OUT/u.path.lstrip('/')).resolve()
  else:target=(p.parent/unquote(u.path)).resolve()
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'Missing local file: {p.relative_to(OUT)} → {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
   # Bootstrap's # target is empty and does not reach this branch.
   errors.append(f'Missing anchor: {p.relative_to(OUT)} → {link}')

planned=0
chapters=sorted((ROOT/'manuscript').glob('*.md'))
if len(chapters)!=10:errors.append(f'Expected 10 chapters, got {len(chapters)}')
for chapter in manifest['chapters']:
 p=ROOT/chapter['file'];n=chapter['planned_sections']
 if not p.is_file():
  errors.append(f'Missing chapter source: {chapter["file"]}');continue
 count=len(re.findall(r'^## .+\{#sec-\d+-\d+\}',p.read_text(),re.M));planned+=count
 if count!=n:errors.append(f'{p.name}: expected {n} planned sections, got {count}')
 if not (OUT/'manuscript'/p.with_suffix('.html').name).exists():errors.append(f'Missing chapter HTML: {p.stem}')

for target,anchors in manifest['required_anchors'].items():
 p=(OUT/Path(target).with_suffix('.html')).resolve()
 for anchor in anchors:
  if p not in pages or anchor not in pages[p].ids:
   errors.append(f'Required anchor missing from HTML: {target}#{anchor}')
for url in manifest['known_missing_images']:
 warnings.append('Original external image unavailable, explicit placeholder retained: '+url)
for name in ['README.md','HANDOFF.md','build.json','archive','editorial','handoff-evidence']:
 if (OUT/name).exists():errors.append(f'Local project record must not be published: {name}')
license_page=OUT/'license.html'
if not license_page.is_file() or 'MENG Haowei' not in license_page.read_text():
 errors.append('Missing copyright page for MENG Haowei')
report={'chapters':len(chapters),'planned_sections':planned,'rendered_html_pages':len(pages),'required_anchors':sum(map(len,manifest['required_anchors'].values())),'rendered_images':sum(x.imgs for x in pages.values()),'errors':sorted(set(errors)),'warnings':warnings,'scope':'Structure, assets and internal links; scientific examples not executed.'}
logs=ROOT/'build-logs';logs.mkdir(exist_ok=True)
(logs/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))

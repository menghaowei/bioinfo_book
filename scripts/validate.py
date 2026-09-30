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
  elif u.path.startswith('/'):continue
  else:target=(p.parent/unquote(u.path)).resolve()
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'Missing local file: {p.relative_to(OUT)} → {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
   # Bootstrap's # target is empty and does not reach this branch.
   errors.append(f'Missing anchor: {p.relative_to(OUT)} → {link}')

planned=0
chapters=sorted((ROOT/'manuscript').glob('*.md'))
if len(chapters)!=10:errors.append(f'Expected 10 chapters, got {len(chapters)}')
expected=[5,6,7,8,7,8,8,8,7,7]
for p,n in zip(chapters,expected):
 count=len(re.findall(r'^## .+\{#sec-\d+-\d+\}',p.read_text(),re.M));planned+=count
 if count!=n:errors.append(f'{p.name}: expected {n} planned sections, got {count}')
 if not (OUT/'manuscript'/p.with_suffix('.html').name).exists():errors.append(f'Missing chapter HTML: {p.stem}')

mapping=json.loads((ROOT/'editorial/section-mapping.json').read_text())
for row in mapping:
 p=(OUT/Path(row['target_file']).with_suffix('.html')).resolve()
 if p not in pages or row['target_anchor'] not in pages[p].ids:
  errors.append(f'Migrated heading missing from HTML: {row["source_file"]}:{row["source_start_line"]}')
missing=json.loads((ROOT/'editorial/missing-assets.json').read_text())
for x in missing:warnings.append('Original external image unavailable, explicit placeholder retained: '+x['image'])
report={'chapters':len(chapters),'planned_sections':planned,'rendered_html_pages':len(pages),'migrated_heading_anchors':len(mapping),'rendered_images':sum(x.imgs for x in pages.values()),'errors':sorted(set(errors)),'warnings':warnings,'scope':'Structure, assets and internal links; scientific examples not executed.'}
(ROOT/'editorial/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))

#!/usr/bin/env python3
"""One-time, auditable Rmd/Markdown migration. Not run by build or CI.

Usage: python3 scripts/migrate_sources.py SOURCE_BOOK SOURCE_QUESTIONS
Requires the original, decoded ZIP directories. Normal writing edits manuscript/*.md.
All imported headings are recorded with original line spans and SHA256 hashes.
"""
from pathlib import Path
import sys, re, json, hashlib, shutil, csv, html, urllib.parse
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
BOOK, QUESTIONS = map(Path, sys.argv[1:3])
OUTLINE = json.loads((ROOT/'editorial/outline.json').read_text())
SLUGS = ['01-learning-and-study-design','02-computing-and-programming','03-sequencing-and-data-formats','04-quality-control-and-alignment','05-statistics-and-exploration','06-rna-seq','07-chip-seq-and-atac-seq','08-wgs-and-wes','09-snakemake-and-reproducibility','10-ai-and-independent-analysis']
# Inclusive starting lines. Each boundary is an actual original heading.
ROUTES = {
 '0010-introduction.Rmd': [(8,'1.1')],
 '0020-introduction_of_NGS.Rmd': [(1,'3.2'),(78,'3.3'),(84,'3.2')],
 '0040-mapping_and_BAM_operation.Rmd': [(8,'4.4'),(98,'4.5'),(276,'4.6'),(433,'4.7'),(467,'4.8')],
 '0050-RNA_seq.Rmd': [(1,'6.1'),(85,'3.3'),(91,'6.1'),(101,'6.2'),(128,'4.2'),(132,'3.4'),(154,'4.2'),(204,'4.3'),(210,'3.5'),(247,'6.3'),(286,'6.4'),(300,'6.5'),(349,'6.4'),(360,'6.6'),(376,'6.7'),(392,'6.2'),(423,'6.3'),(625,'6.4'),(768,'6.6'),(930,'6.7'),(1122,'6.8')],
 '0060-ChIP_seq.Rmd': [(20,'7.1'),(52,'7.2'),(82,'7.3'),(229,'7.2'),(311,'7.3'),(630,'7.4'),(732,'7.6'),(797,'7.7'),(820,'7.8')],
 '0070-WGS.Rmd': [(1,'8.1'),(9,'4.1'),(46,'4.7'),(287,'8.3'),(363,'8.4'),(639,'8.1'),(679,'8.2'),(701,'8.5'),(796,'8.7')],
 '0080-statistics.Rmd': [(1,'5.1'),(3,'5.3'),(5,'5.5'),(7,'5.6'),(13,'5.7')],
 '0090-build_up_bioinfo_platform.Rmd': [(1,'2.1'),(13,'2.2'),(25,'2.1'),(270,'2.5'),(300,'2.4'),(346,'2.5'),(431,'2.6')],
 '_0030-QC_of_FASTQ.Rmd': [(7,'4.2'),(17,'4.3')],
}

def digest(s): return hashlib.sha256(s if isinstance(s,bytes) else s.encode()).hexdigest()

def headings(text, loose=False):
    lines=text.splitlines(); found=[]; fence=None
    for i,line in enumerate(lines):
        fm=re.match(r'^\s*(`{3,}|~{3,})',line)
        if fm:
            c=fm[1][0]
            if fence is None: fence=c
            elif fence==c: fence=None
            continue
        if fence: continue
        pat=r'^(#{1,6})\s*(\S.*)$' if loose else r'^(#{1,6})\s+(\S.*)$'
        m=re.match(pat,line)
        if m: found.append((i+1,len(m[1]),m[2]))
    return lines,found

sections=defaultdict(list); mapping=[]; assets=[]; missing=[]; asset_cache={}; counter=defaultdict(int)
all_images=[p for root in (BOOK,QUESTIONS) for p in root.rglob('*') if p.is_file() and p.suffix.lower() in ('.png','.jpg','.jpeg','.gif','.svg','.webp')]

def asset(src, origin, slug, caption):
    src=html.unescape(urllib.parse.unquote(src.strip().strip('<>')))
    key=(str(origin.parent),src,slug)
    if key in asset_cache: return asset_cache[key]
    external=src.startswith(('http://','https://'))
    p=origin.parent/src
    resolution='relative path'
    if external:
        # Downloaded external resources are provided by fetch_external_assets.py.
        p=ROOT/'editorial/external-cache'/digest(src)[:16]
        resolution='external download'
    if not p.is_file() and not external:
        candidates=[f for f in all_images if f.name==Path(src).name]
        if candidates:
            p=sorted(candidates,key=lambda f:(len(f.parts),str(f)))[0]
            resolution='resolved by original basename'
    if not p.is_file():
        missing.append({'source':str(origin.relative_to(BOOK) if origin.is_relative_to(BOOK) else origin.relative_to(QUESTIONS)),'image':src,'target':slug})
        return None
    counter[slug]+=1
    stem=re.sub(r'[^a-zA-Z0-9]+','-',Path(src).stem).strip('-').lower()[:55] or 'illustration'
    if len(stem)<3: stem='illustration'
    ext=Path(urllib.parse.urlparse(src).path).suffix.lower() if external else p.suffix.lower()
    if ext not in ('.png','.jpg','.jpeg','.gif','.svg','.webp'): ext='.png'
    name=f'{counter[slug]:03d}-{stem}{ext}'
    target=ROOT/'assets'/slug/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    result=(f'../assets/{slug}/{name}',f'fig-{slug}-{counter[slug]:03d}')
    asset_cache[key]=result
    assets.append({'original_file':str(origin.relative_to(BOOK) if origin.is_relative_to(BOOK) else origin.relative_to(QUESTIONS)), 'original_image':src,'new_image':str(target.relative_to(ROOT)),'sha256':digest(p.read_bytes()),'resolution':resolution})
    return result

def normalize(text,origin,slug):
    # Executable Rmd chunks become ordinary displayed code. Build never runs analyses.
    text=re.sub(r'```\{(r|python|bash|sh)[^}]*\}',lambda m:'```'+m[1],text)
    text=text.replace('随便写一点内容！','待完善').replace('需要增加解释','待完善：需补充解释')
    text=re.sub(r'10<sup>(\d+)</sup>',lambda m:'$10^{'+m[1]+'}$',text)
    if origin.name=='0050-RNA_seq.Rmd':
        used=set()
        def foot(m):
            nums=m[1].split(',');used.update(nums)
            return ''.join('[^rna-ref-'+n+']' for n in nums)
        text=re.sub(r'<sup>(\d+(?:,\d+)*)</sup>',foot,text)
        # Definitions collected per output file below, avoiding repeated definitions.
    def img(md):
        caption,src=md
        result=asset(src,origin,slug,caption)
        if not result:
            return '\n\n::: {.callout-note title="原图待完善"}\n原稿图片缺失或外部地址不可用：`'+src+'`。原有图位保留。\n:::\n\n'
        path,ident=result
        caption=caption.strip()
        if not caption or caption in ('image','img','ascll') or caption.startswith('image-'):
            caption=Path(src).stem.replace('_',' ').replace('-',' ')
            if re.fullmatch(r'[\da-f -]{8,}',caption) or caption.isdigit():caption='原稿配图'
        return '\n\n!['+caption+']('+path+'){#'+ident+'}\n\n'
    def raw_img(m):
        tag=m[0]; sm=re.search(r'src\s*=\s*(?:"([^"]+)"|\x27([^\x27]+)\x27|([^\s>]+))',tag)
        if not sm:return m[0]
        src=next(x for x in sm.groups() if x is not None).rstrip('/')
        am=re.search(r'alt\s*=\s*["\x27](.*?)["\x27]',tag)
        return img((am[1] if am else '',src))
    # Convert raw HTML images first; protect generated output from double handling.
    placeholders=[]
    def stash(v):placeholders.append(v);return f'@@IMAGE{len(placeholders)-1}@@'
    text=re.sub(r'<img\b[^>]*>',lambda m:stash(raw_img(m)),text,flags=re.I)
    text=re.sub(r'!\[([^\]]*)\]\(([^\n]*?)\)',lambda m:stash(img((m[1],m[2]))),text)
    for i,v in enumerate(placeholders):text=text.replace(f'@@IMAGE{i}@@',v)
    text=re.sub(r"<p align=['\"]center['\"]>\s*(.*?)\s*</p>",r'\1',text,flags=re.S)
    text=re.sub(r'\n{4,}','\n\n\n',text)
    return text

for filename,routes in ROUTES.items():
    origin=BOOK/filename; original=origin.read_text(); lines,hs=headings(original)
    for i,(line,level,title) in enumerate(hs):
        if line<routes[0][0]:continue
        end=hs[i+1][0]-1 if i+1<len(hs) else len(lines)
        sec=next(s for start,s in reversed(routes) if start<=line)
        ch=int(sec.split('.')[0]);slug=SLUGS[ch-1]
        clean_title=re.sub(r'\{[^}]*\}','',title).strip()
        clean_title=clean_title.replace('（待补充）','').replace('（需要增加解释）','')
        ident=f'src-{filename.replace(".Rmd","").replace("_","-").strip("-")}-{line}'
        body='\n'.join(lines[line:end]).strip()
        newlevel=min(6,max(3,level+1))
        # Empty leaf headings remain visible and explicitly marked.
        nextlevel=hs[i+1][1] if i+1<len(hs) else 0
        if not body and nextlevel<=level:body='待完善'
        block='#'*newlevel+' '+clean_title+' {#'+ident+'}\n\n'+body+'\n'
        block=normalize(block,origin,slug)
        sections[sec].append(block)
        mapping.append({'source_file':filename,'source_start_line':line,'source_end_line':end,'source_heading':title,'source_sha256':digest('\n'.join(lines[line-1:end])),'target_file':f'manuscript/{slug}.md','target_section':sec,'target_anchor':ident,'treatment':'正文迁移；标题层级、图片路径及展示语法规范化'})

for n,ch in enumerate(OUTLINE['chapters'],1):
    slug=SLUGS[n-1]
    out=['# '+ch['title']+' {#sec-ch'+str(n).zfill(2)+'}\n',ch.get('purpose','')+'\n']
    if n in (2,4,6,7,8):
        out.append('::: {.callout-note title="阅读提示" collapse="true"}\n本章保留原稿中的原理、命令和历史软件示例。命令不会在网页构建时执行；实战环境、软件版本与预期结果仍需按各节“待完善”项补齐。\n:::\n')
    for j,s in enumerate(ch['sections'],1):
        sec=f'{n}.{j}';blocks=sections[sec]
        out.append('## '+s['title']+' {#sec-'+str(n).zfill(2)+'-'+str(j).zfill(2)+'}\n')
        out.append(s.get('purpose','')+'\n')
        if blocks:out+=blocks
        else:out.append('待完善\n')
        if blocks and s.get('status')!='A':
            out.append('::: {.callout-note title="待完善" collapse="true"}\n'+s.get('action',s.get('content',''))+'\n:::\n')
    text='\n'.join(out)
    refs=sorted(set(re.findall(r'\[\^rna-ref-(\d+)\]',text)),key=int)
    for ref in refs:text+=f'\n[^rna-ref-{ref}]: 原稿文献编号 {ref}；完整书目信息待完善。\n'
    (ROOT/'manuscript'/f'{slug}.md').write_text(text)

# Appendix: preserve all 25 questions and their published draft answers.
qfiles=[next(QUESTIONS.glob('Anwser-01*/*.md')),next(QUESTIONS.glob('Anwser-02*/*MHW.md')),next(QUESTIONS.glob('Anwser-03*/*MHW.md')),next(QUESTIONS.glob('100_BBQ_16-20/*.md')),next(QUESTIONS.glob('Anwser-05*/*.md'))]
for i,f in enumerate(qfiles):
    lo=i*5+1;hi=lo+4;slug=f'a-questions-{lo:02d}-{hi:02d}'
    lines,hs=headings(f.read_text(),loose=True)
    text=f'# 基础问题 {lo}—{hi} {{#sec-{slug}}}\n\n本组保留原题和原稿参考答案。题库目前收录 1—25 题；历史仪器参数和软件用法仍需逐项更新。\n\n'
    if i==0:text+='对应 [测序与数据格式](../manuscript/03-sequencing-and-data-formats.md)。\n\n'
    elif i<=2:text+='对应 [质控与比对](../manuscript/04-quality-control-and-alignment.md)。\n\n'
    else:text+='对应 [文件与比对](../manuscript/04-quality-control-and-alignment.md) 和 [RNA-seq](../manuscript/06-rna-seq.md)。\n\n'
    for k,(line,level,title) in enumerate(hs):
        end=hs[k+1][0]-1 if k+1<len(hs) else len(lines)
        if k==0 and (i>0):continue # original bundle title is replaced by the appendix title
        title=title.strip('* ')
        if re.search(r'BBQ100-\d+|Questions_\d+',title):newlevel=2
        else:newlevel=min(6,max(3,level if i==0 else level+1))
        anchor=f'question-{lo:02d}-{line}'
        block='#'*newlevel+' '+title+' {#'+anchor+'}\n\n'+'\n'.join(lines[line:end])+'\n'
        text+=normalize(block,f,slug)+'\n'
        mapping.append({'source_file':str(f.relative_to(QUESTIONS)),'source_start_line':line,'source_end_line':end,'source_heading':title,'source_sha256':digest('\n'.join(lines[line-1:end])),'target_file':f'appendices/{slug}.md','target_section':f'A.{i+1}','target_anchor':anchor,'treatment':'题库主稿迁移；同题其他版本完整归档'})
    (ROOT/'appendices'/f'{slug}.md').write_text(text)
for f in QUESTIONS.rglob('*.md'):
    target=ROOT/'archive/question-drafts'/f.relative_to(QUESTIONS);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
shutil.copy2(QUESTIONS/'100-questions.txt',ROOT/'archive/question-drafts/100-questions.txt')
for name,rows in [('section-mapping',mapping),('asset-mapping',assets),('missing-assets',missing)]:
    (ROOT/'editorial'/f'{name}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    if rows:
        with (ROOT/'editorial'/f'{name}.tsv').open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
print(json.dumps({'imported_headings':len(mapping),'assets':len(assets),'missing_assets':len(missing),'chapters':10,'sections':71},ensure_ascii=False))

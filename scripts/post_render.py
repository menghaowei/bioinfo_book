#!/usr/bin/env python3
"""Complete the portable HTML output after Quarto rendering."""
from pathlib import Path
import json,os,shutil,subprocess,datetime,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs'
if not (ROOT/'vendor/mathjax/tex-chtml.js').is_file():
 raise SystemExit('Missing vendored MathJax: restore vendor/mathjax from the repository.')
shutil.copytree(ROOT/'vendor/mathjax',OUT/'vendor/mathjax',dirs_exist_ok=True)
for p in OUT.rglob('*.html'):
 s=p.read_text()
 rel=os.path.relpath(OUT/'vendor/mathjax/tex-chtml.js',p.parent).replace(os.sep,'/')
 s=re.sub(r'src="[^"]*(?:vendor/mathjax/tex-chtml\.js|mathjax@[^"/]+/es5/tex-mml-chtml\.js)"',f'src="{rel}"',s)
 p.write_text(s)
(OUT/'.nojekyll').touch()
# Compatibility with the repository's pre-existing master/root Pages source.
# The Actions deployment serves docs/ itself at the original site URL.
(ROOT/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=docs/index.html"><title>生物信息学入门</title><p><a href="docs/index.html">打开新版教材</a></p></html>')
try:sha=os.environ.get('GITHUB_SHA') or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
except Exception:sha='local'
run_url=(f"{os.environ.get('GITHUB_SERVER_URL','https://github.com')}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}" if os.environ.get('GITHUB_RUN_ID') and os.environ.get('GITHUB_REPOSITORY') else None)
(OUT/'build.json').write_text(json.dumps({'source_commit':sha,'workflow_run_url':run_url,'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'quarto':'1.8.27','chapters':10,'planned_sections':71},ensure_ascii=False,indent=2)+'\n')
aliases={'intro.html':'manuscript/01-learning-and-study-design.html','author.html':'index.html','NGS-tech.html':'manuscript/03-sequencing-and-data-formats.html','build-up-platform.html':'manuscript/02-computing-and-programming.html','RNA-seq.html':'manuscript/06-rna-seq.html','ChIP-seq.html':'manuscript/07-chip-seq-and-atac-seq.html','WGS.html':'manuscript/08-wgs-and-wes.html','statistics.html':'manuscript/05-statistics-and-exploration.html','references.html':'appendices/e-references-and-maintenance.html','sound.html':'index.html','microarray.html':'manuscript/10-ai-and-independent-analysis.html','-.html':'index.html'}
for name,target in aliases.items():
 (OUT/name).write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='+target+'"><title>章节已迁移</title><p>本章节已迁移至<a href="'+target+'">新版目录</a>。</p></html>')

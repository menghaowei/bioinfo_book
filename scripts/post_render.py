#!/usr/bin/env python3
"""Complete the portable HTML output after Quarto rendering."""
from pathlib import Path
from html import escape
import json,os,shutil,subprocess,datetime,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs'
manifest=json.loads((ROOT/'scripts/validation-manifest.json').read_text())
if not (ROOT/'vendor/mathjax/tex-chtml.js').is_file():
 raise SystemExit('Missing vendored MathJax: restore vendor/mathjax from the repository.')
shutil.copytree(ROOT/'vendor/mathjax',OUT/'vendor/mathjax',dirs_exist_ok=True)
for p in OUT.rglob('*.html'):
 s=p.read_text()
 rel=os.path.relpath(OUT/'vendor/mathjax/tex-chtml.js',p.parent).replace(os.sep,'/')
 s=re.sub(r'src="[^"]*(?:vendor/mathjax/tex-chtml\.js|mathjax@[^"/]+/es5/tex-mml-chtml\.js)"',f'src="{rel}"',s)
 p.write_text(s)
(OUT/'.nojekyll').touch()
# Operational metadata stays out of the public website and Git history.
logs=ROOT/'build-logs';logs.mkdir(exist_ok=True)
try:sha=os.environ.get('GITHUB_SHA') or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
except Exception:sha='local'
run_url=(f"{os.environ.get('GITHUB_SERVER_URL','https://github.com')}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}" if os.environ.get('GITHUB_RUN_ID') and os.environ.get('GITHUB_REPOSITORY') else None)
(logs/'build.json').write_text(json.dumps({'source_commit':sha,'workflow_run_url':run_url,'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'quarto':'1.8.27','chapters':len(manifest['chapters']),'planned_sections':sum(c['planned_sections'] for c in manifest['chapters']),'chapter_summaries':sum(bool(c.get('summary')) for c in manifest['chapters'])},ensure_ascii=False,indent=2)+'\n')
shutil.copytree(ROOT/'vendor/licenses',OUT/'vendor/licenses',dirs_exist_ok=True)
shutil.copy2(ROOT/'vendor/NOTICE.txt',OUT/'vendor/NOTICE.txt')
license_text=escape((ROOT/'LICENSE').read_text())
(OUT/'license.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>版权与使用条款 · BioinfoBook</title><link rel="stylesheet" href="styles/book.css"></head><body class="license-page"><main><p><a href="index.html">← 返回教材</a></p><h1>版权与使用条款</h1><div class="license-text">'+license_text+'</div><p>第三方组件声明：<a href="vendor/NOTICE.txt">NOTICE</a> · <a href="vendor/mathjax/LICENSE">MathJax</a> · <a href="vendor/licenses/bookdown-template-MIT.txt">历史模板版权声明</a></p></main></body></html>')
aliases=json.loads((ROOT/'scripts/legacy-redirects.json').read_text())
for name,route in aliases.items():
 page=OUT/name;page.parent.mkdir(parents=True,exist_ok=True)
 def relative(target):
  path,sep,anchor=target.partition('#')
  return os.path.relpath(OUT/path,page.parent).replace(os.sep,'/')+(sep+anchor if sep else '')
 target=relative(route['target'])
 destinations={anchor:relative(dest) for anchor,dest in route['anchors'].items()}
 encoded=json.dumps(destinations,ensure_ascii=False).replace('<','\\u003c')
 fallback=json.dumps(target,ensure_ascii=False).replace('<','\\u003c')
 script='const destinations='+encoded+';let anchor=location.hash.slice(1);try{anchor=decodeURIComponent(anchor)}catch(e){}const destination=destinations[anchor]||('+fallback+'+location.hash);const url=new URL(destination,location.href);url.search=location.search;location.replace(url.href);'
 page.write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>章节已迁移</title><script>'+script+'</script><noscript><meta http-equiv="refresh" content="0;url='+escape(target,quote=True)+'"></noscript></head><body><p>本章节已迁移至<a href="'+escape(target,quote=True)+'">新版目录</a>。</p></body></html>')

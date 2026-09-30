#!/usr/bin/env python3
"""One-command HTML build; never executes the book's bioinformatics examples."""
from pathlib import Path
import shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
quarto=shutil.which('quarto')
if not quarto:raise SystemExit('请先安装 Quarto 1.8.27，并确认 quarto 已加入 PATH：https://quarto.org/docs/get-started/')
subprocess.run([quarto,'render','--to','html'],cwd=root,check=True)
subprocess.run([sys.executable,'scripts/validate.py'],cwd=root,check=True)
print('构建完成：docs/index.html。预览：python3 -m http.server 8000 --directory docs')

#!/usr/bin/env python3
"""Preview with Quarto's live reload. Stop with Ctrl+C."""
from pathlib import Path
import shutil,subprocess
root=Path(__file__).resolve().parents[1]
quarto=shutil.which('quarto')
if not quarto:raise SystemExit('请先安装 Quarto 1.8.27 并加入 PATH。')
raise SystemExit(subprocess.call([quarto,'preview','--port','4200','--no-browser'],cwd=root))

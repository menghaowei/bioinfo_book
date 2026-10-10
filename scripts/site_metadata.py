"""Reader-facing modification date, derived from source history rather than builds."""
from datetime import datetime, timedelta, timezone
from html import escape
import subprocess


def last_modified_markup(root):
    # Generated HTML commits must not advance the source modification date.
    committed_at = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cI', '--', '.', ':(exclude)docs'],
        cwd=root, text=True,
    ).strip()
    if not committed_at:
        raise RuntimeError('Cannot determine the last source modification time from Git')
    modified = datetime.fromisoformat(committed_at).astimezone(timezone(timedelta(hours=8)))
    return (f'<time class="book-last-modified" datetime="{escape(modified.isoformat(), quote=True)}"'
            ' title="最后修改时间（北京时间，UTC+08:00）">'
            f'最后修改 {modified:%Y-%m-%d %H:%M}</time>')

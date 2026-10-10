"""Reader-facing modification date, derived from source history rather than builds."""
from datetime import datetime, timedelta, timezone
from html import escape
import re
import subprocess


def source_modified_at(root, source=None):
    # Follow a chapter's own history; generated HTML never advances its date.
    paths = ['--follow', '--', source] if source else ['--', '.', ':(exclude)docs']
    committed_at = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cI', *paths],
        cwd=root, text=True,
    ).strip()
    if not committed_at:
        raise RuntimeError(f'Cannot determine the last source modification time from Git: {source or root}')
    return datetime.fromisoformat(committed_at).astimezone(timezone(timedelta(hours=8)))


def last_modified_markup(root):
    modified = source_modified_at(root)
    return (f'<time class="book-last-modified" datetime="{escape(modified.isoformat(), quote=True)}"'
            ' title="最后修改时间（北京时间，UTC+08:00）">'
            f'最后修改 {modified:%Y-%m-%d %H:%M}</time>')


def chapter_modified_markup(root, source):
    modified = source_modified_at(root, source)
    return ('<p class="chapter-last-modified">'
            f'<time datetime="{escape(modified.isoformat(), quote=True)}"'
            ' title="本章书稿最后修改时间（北京时间，UTC+08:00）">'
            f'最后修改：{modified:%Y-%m-%d %H:%M}（北京时间）</time></p>')


def add_chapter_modified(html, root, source):
    # Repeated post-render passes replace the note instead of duplicating it.
    html = re.sub(r'\n?<p class="chapter-last-modified">.*?</p>', '', html, flags=re.S)
    markup = chapter_modified_markup(root, source)
    html, count = re.subn(
        r'(<header id="title-block-header"[^>]*>.*?</h1>)',
        lambda match: match[1] + '\n' + markup, html, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError(f'Cannot locate chapter title for modification date: {source}')
    return html

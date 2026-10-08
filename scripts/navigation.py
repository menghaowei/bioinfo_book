"""Build a portable, static chapter/section directory from rendered headings."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import os


class BookPage(HTMLParser):
    """Read headings and replacement ranges without rewriting book content."""
    void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__()
        self.source = source
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.stack = []
        self.ranges = {}
        self.title = ''
        self.headings = []
        self.heading = None
        self.feed(source)
        self.close()

    def position(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        key = None
        if attrs.get('id') == 'quarto-margin-sidebar':
            key = 'margin'
        if 'sidebar-menu-container' in attrs.get('class', '').split():
            key = 'menu'
        in_main = any(t == 'main' for t, _, _, _ in self.stack)
        if in_main and tag == 'h1' and not self.title:
            self.heading = {'level': 1, 'id': '', 'text': []}
        elif in_main and tag in ('h2', 'h3') and attrs.get('data-anchor-id'):
            excluded = any(set(a.get('class', '').split()) & {'unlisted', 'footnotes'}
                           for _, a, _, _ in self.stack)
            if not excluded and 'unlisted' not in attrs.get('class', '').split():
                self.heading = {'level': int(tag[1]), 'id': attrs['data-anchor-id'], 'text': []}
        if tag not in self.void_tags:
            self.stack.append((tag, attrs, self.position(), key))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.heading is not None:
            self.heading['text'].append(data)

    def handle_endtag(self, tag):
        if self.heading is not None and tag == 'h' + str(self.heading['level']):
            heading = self.heading
            heading['text'] = ' '.join(''.join(heading['text']).split())
            if heading['level'] == 1:
                self.title = heading['text']
            else:
                self.headings.append(heading)
            self.heading = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, _, start, key = self.stack[i]
                if key:
                    self.ranges[key] = (start, self.source.index('>', self.position()) + 1)
                del self.stack[i:]
                break


def book_files(manifest):
    return [Path('index.html'),
            *(Path(c['file']).with_suffix('.html') for c in manifest['chapters']),
            *(Path(f).with_suffix('.html') for f in manifest['appendices'])]


def render_navigation(current, catalog):
    parts = ['<div class="sidebar-menu-container" tabindex="0" aria-label="目录，可横向滚动">',
             '<ul class="book-tree" aria-label="全书章节与小节">']
    for number, (file, page) in enumerate(catalog):
        selected = file == current
        route = os.path.relpath(file, current.parent).replace(os.sep, '/')
        title = '阅读指南' if file == Path('index.html') else page.title
        chapter_link = (f'<a class="book-nav-link book-chapter-link no-external" href="{escape(route, quote=True)}"'
                        + (' aria-current="page"' if selected else '')
                        + f'>{escape(title)}</a>')
        parts.append('<li>')
        if page.headings:
            parts.append(f'<details class="book-chapter" data-book-page="{escape(str(file), quote=True)}"'
                         + (' open data-current-chapter="true"' if selected else '') + '>')
            parts.append(f'<summary>{chapter_link}</summary><ul class="book-sections">')
            groups = []
            for heading in page.headings:
                if heading['level'] == 2 or not groups:
                    groups.append((heading, []))
                else:
                    groups[-1][1].append(heading)

            def link(heading):
                anchor = heading['id']
                href = ('#' if selected else route + '#') + anchor
                return (f'<a class="book-nav-link book-section-link no-external" href="{escape(href, quote=True)}"'
                        f' data-book-level="{heading["level"]}"'
                        + (f' data-book-target="{escape(anchor, quote=True)}"' if selected else '')
                        + f' id="book-nav-{number}-{escape(anchor, quote=True)}">{escape(heading["text"])}</a>')

            for heading, children in groups:
                parts.append('<li>')
                if children:
                    parts.append(f'<details class="book-section"><summary>{link(heading)}</summary><ul>')
                    parts.extend(f'<li class="book-nav-leaf">{link(child)}</li>' for child in children)
                    parts.append('</ul></details>')
                else:
                    parts.append(f'<div class="book-nav-leaf">{link(heading)}</div>')
                parts.append('</li>')
            parts.append('</ul></details>')
        else:
            parts.append(f'<div class="book-nav-leaf book-chapter-empty">{chapter_link}</div>')
        parts.append('</li>')
    parts.append('</ul></div>')
    return '\n'.join(parts)


def build_navigation(output, manifest):
    catalog = [(file, BookPage((output / file).read_text())) for file in book_files(manifest)]
    for file, page in catalog:
        if not page.title or 'menu' not in page.ranges:
            raise ValueError(f'Missing book title or navigation container: {file}')
        replacements = [(page.ranges['menu'], render_navigation(file, catalog))]
        if 'margin' in page.ranges:
            start, end = page.ranges['margin']
            line_start = page.source.rfind('\n', 0, start) + 1
            if not page.source[line_start:start].strip():
                start = line_start
            replacements.append(((start, end), ''))
        source = page.source
        for (start, end), markup in sorted(replacements, reverse=True):
            source = source[:start] + markup + source[end:]
        (output / file).write_text(source)

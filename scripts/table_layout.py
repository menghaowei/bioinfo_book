"""Wrap reading tables without rewriting their contents or column alignment."""
from html.parser import HTMLParser


def wrap_tables(source):
    """Add one scroll region per outermost table in main; preserve source bytes."""
    class Tables(HTMLParser):
        void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                     'link', 'meta', 'param', 'source', 'track', 'wbr'}

        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.line_offsets = [0]
            for line in source.splitlines(keepends=True):
                self.line_offsets.append(self.line_offsets[-1] + len(line))
            self.stack = []
            self.insertions = {}
            self.param_table = False      # 当前表是否为“参数｜含义”两列表
            self.first_row_cells = None   # None=未在首行；list=收集中的首行单元格文本
            self.cell_text = None

        def source_position(self):
            line, column = self.getpos()
            return self.line_offsets[line - 1] + column

        def insert(self, position, markup):
            self.insertions.setdefault(position, []).append(markup)

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            ancestors = [item[0] for item in self.stack]
            already_wrapped = any('book-table-scroll' in item[1].get('class', '').split()
                                  for item in self.stack)
            wrap = tag == 'table' and 'main' in ancestors and 'table' not in ancestors and not already_wrapped
            if wrap:
                self.insert(self.source_position(), '<div class="book-table-scroll" role="region" '
                            'aria-label="表格，可横向滚动" tabindex="0">')
                self.param_table = False
                self.first_row_cells = []
                # colgroup 注入点：紧跟 <table ...> 起始标签之后
                self.colgroup_pos = source.index('>', self.source_position()) + 1
            if self.first_row_cells is not None and tag in ('th', 'td') and 'table' in ancestors:
                self.cell_text = []
            if tag not in self.void_tags:
                self.stack.append((tag, attrs, wrap))

        def handle_startendtag(self, tag, attrs):
            # Self-closing elements cannot contain a reading table.
            pass

        def handle_data(self, data):
            if self.cell_text is not None:
                self.cell_text.append(data)

        def handle_endtag(self, tag):
            if tag in ('th', 'td') and self.cell_text is not None:
                self.first_row_cells.append(''.join(self.cell_text).strip())
                self.cell_text = None
            if tag == 'tr' and self.first_row_cells:
                if len(self.first_row_cells) == 2 and self.first_row_cells[0] == '参数':
                    self.param_table = True
                    self.insert(self.colgroup_pos,
                                '<colgroup><col style="width:22%;min-width:110px"><col style="width:78%"></colgroup>')
                self.first_row_cells = None   # 只看首行
            if tag == 'table' and self.first_row_cells is not None:
                self.first_row_cells = None
            for index in range(len(self.stack) - 1, -1, -1):
                if self.stack[index][0] == tag:
                    if self.stack[index][2]:
                        self.insert(source.index('>', self.source_position()) + 1, '</div>')
                    del self.stack[index:]
                    break

    parser = Tables()
    parser.feed(source)
    parser.close()
    result = source
    for position in sorted(parser.insertions, reverse=True):
        result = result[:position] + ''.join(parser.insertions[position]) + result[position:]
    return result

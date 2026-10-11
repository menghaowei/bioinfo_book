#!/usr/bin/env python3
"""第12章概念示意图生成：大模型时间线、三阶段用法演进。

遵循 AUTHORING_GUIDE 第 14 节：统一色表、字体栈内嵌声明、
SVG 同时保留 width/height 与 viewBox，并提供 <title>/<desc>。
生成：assets/12-ai-learning-and-practice/001-llm-timeline.svg
      assets/12-ai-learning-and-practice/003-three-stages.svg
"""
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "..", "..", "assets", "12-ai-learning-and-practice")

SANS = "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"

COLOR_TEXT = "#333333"
COLOR_MUTED = "#6b7280"
COLOR_PRIMARY = "#186254"
COLOR_FILL = "#e8f4f1"
COLOR_WARN = "#b45309"
COLOR_LINE = "#9ca3af"


def text_el(x, y, s, size=13, fill=COLOR_TEXT, anchor="start", weight="normal",
            font=SANS):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, font, size, fill, anchor, weight, escape(s)))


def svg_doc(width, height, title, desc, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d">\n<title>%s</title>\n<desc>%s</desc>\n%s\n</svg>\n'
            % (width, height, width, height, escape(title), escape(desc), body))


# ---------------------------------------------------------------- 图 1：时间线
def gen_timeline():
    W, H = 1000, 330
    axis_y = 168
    x0, x1 = 120, 880
    nodes = [
        ("2013–2016", "深度学习普及", ["词向量、序列到序列翻译", "2016 AlphaGo 出圈"]),
        ("2017", "Transformer", ["注意力取代循环结构", "可并行、可随规模扩展"]),
        ("2020", "GPT-3", ["1750 亿参数", "少样本上下文学习"]),
        ("2022", "思维链 CoT", ["在提示中给推理示例", "让模型“先想再答”"]),
        ("2023", "GPT-4", ["多模态输入", "综合推理能力跃升"]),
        ("2024", "o1", ["开创推理模型形态", "（闭源产品）"]),
        ("2025.1", "DeepSeek-R1", ["MIT 许可完整开源", "同年 9 月登 Nature 封面"]),
    ]
    parts = []
    parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>'
                 % (60, axis_y, x1 + 36, axis_y, COLOR_LINE))
    parts.append('<path d="M %.1f %d l -12 -6 l 0 12 z" fill="%s"/>'
                 % (x1 + 48, axis_y, COLOR_LINE))
    step = (x1 - x0) / (len(nodes) - 1)
    for i, (year, title, notes) in enumerate(nodes):
        cx = x0 + i * step
        last = i == len(nodes) - 1
        color = COLOR_WARN if last else COLOR_PRIMARY
        parts.append('<circle cx="%.1f" cy="%d" r="10" fill="none" stroke="%s" stroke-width="1.5" opacity="0.45"/>'
                     % (cx, axis_y, color))
        parts.append('<circle cx="%.1f" cy="%d" r="6" fill="%s"/>'
                     % (cx, axis_y, color))
        if i % 2 == 0:  # 标签块在上方：注释在最上，标题居中，年份贴近轴
            parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="142" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>'
                         % (cx, axis_y - 12, cx, COLOR_LINE))
            parts.append(text_el(cx, 94, notes[0], 12, COLOR_MUTED, anchor="middle"))
            parts.append(text_el(cx, 111, notes[1], 12, COLOR_MUTED, anchor="middle"))
            parts.append(text_el(cx, 130, title, 14, COLOR_TEXT, anchor="middle", weight="bold"))
            parts.append(text_el(cx, 150, year, 13, color, anchor="middle", weight="bold"))
        else:  # 标签块在下方：年份贴近轴
            parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="204" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>'
                         % (cx, axis_y + 12, cx, COLOR_LINE))
            parts.append(text_el(cx, 218, year, 13, color, anchor="middle", weight="bold"))
            parts.append(text_el(cx, 240, title, 14, COLOR_TEXT, anchor="middle", weight="bold"))
            parts.append(text_el(cx, 262, notes[0], 12, COLOR_MUTED, anchor="middle"))
            parts.append(text_el(cx, 279, notes[1], 12, COLOR_MUTED, anchor="middle"))
    body = "\n".join(parts)
    return svg_doc(W, H,
                   "从自然语言处理到大语言模型的关键节点时间线",
                   "2013 至 2025 年的七个关键节点：深度学习普及、2017 年 Transformer、"
                   "2020 年 GPT-3、2022 年思维链、2023 年 GPT-4、2024 年 o1、"
                   "2025 年 1 月 DeepSeek-R1 开源（琥珀色标出）。每一节点的能力建立在此前积累之上。",
                   body)


# ------------------------------------------------------------- 图 2：三阶段
def gen_three_stages():
    W, H = 900, 540
    parts = []
    # 三层嵌套；名称两行（英文在上、中文在下），每层文字区完整落在下一内层框顶边之上
    rings = [
        dict(rect=(30, 26, 840, 488), name_en="Harness Engineering", name_zh="Harness 工程",
             subtitle="给模型装上手脚：工具、规则与循环",
             items="工具调用 · AGENTS.md 项目规则 · 审批与沙箱",
             example=None),
        dict(rect=(110, 140, 680, 336), name_en="Context Engineering", name_zh="上下文工程",
             subtitle="把材料喂进去：模型只知道窗口里的信息",
             items="报错原文 · 版本与环境 · 文件与数据说明 · 按需选材",
             example="示例：贴上完整报错、命令与版本，而不是“好像有格式错误”"),
        dict(rect=(190, 290, 500, 150), name_en="Prompt Engineering", name_zh="提示词工程",
             subtitle="把任务讲清楚",
             items="角色与目标 · 示例 · 分步骤 · 输出格式与约束",
             example="示例：请逐列解释这份 DESeq2 结果表"),
    ]
    for idx, ring in enumerate(rings):
        x, y, w, h = ring["rect"]
        inner = idx == len(rings) - 1
        fill = COLOR_FILL if inner else "none"
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="14" '
                     'fill="%s" stroke="%s" stroke-width="2.4"/>'
                     % (x, y, w, h, fill, COLOR_PRIMARY))
        parts.append(text_el(x + 22, y + 32, ring["name_en"], 16, COLOR_PRIMARY, weight="bold"))
        parts.append(text_el(x + 22, y + 54, ring["name_zh"], 14, COLOR_TEXT, weight="bold"))
        parts.append(text_el(x + 22, y + 76, ring["subtitle"], 13, COLOR_TEXT))
        parts.append(text_el(x + 22, y + 98, ring["items"], 12, COLOR_MUTED))
        if ring["example"]:
            parts.append(text_el(x + 22, y + 126, ring["example"], 12.5, COLOR_TEXT, font=MONO))
    # agent 循环：属于最外层（Harness），放在内层框下方、外层框内部
    parts.append(text_el(450, 494, "循环：计划 → 行动 → 观察结果 → 修正，直到任务完成", 13,
                         COLOR_TEXT, anchor="middle", font=MONO))
    body = "\n".join(parts)
    return svg_doc(W, H,
                   "用好大语言模型的三个阶段",
                   "三层嵌套：提示词工程（最内，把任务讲清楚）包含于上下文工程"
                   "（把对的材料喂进上下文窗口），再包含于 Harness 工程（为模型配置工具、"
                   "规则与循环）。每层名称英文在上、中文在下；外层阶段包含内层阶段。",
                   body)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    docs = {
        "001-llm-timeline.svg": gen_timeline(),
        "003-three-stages.svg": gen_three_stages(),
    }
    for name, svg in docs.items():
        path = os.path.join(OUT_DIR, name)
        with open(path, "w") as fh:
            fh.write(svg)
        print("written:", os.path.normpath(path))


if __name__ == "__main__":
    main()

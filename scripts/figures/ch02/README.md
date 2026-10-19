# 第 2 章插图生成

## 本地电脑与远端服务器

```bash
python3 scripts/figures/ch02/gen_local_remote_platform.py
```

使用 Python 标准库生成 `assets/02-computing-and-programming/svg/local-remote-platform.svg`，无需联网或额外依赖。画布为 640 × 610，文字保留为可编辑的 SVG 文本；颜色沿用本书深绿、浅绿和暖白体系，中文使用无衬线字体栈。

图示对应 2.1 平台构建和 2.2 SSH 连接：本地系统按需选择，服务器通常使用 Linux，两端系统不必相同。箭头分别表示远端命令和返回输出，不表示文件上传下载。两侧任务是本书采用的常见分工；“使用 AI agent”不限定模型推理发生的位置。图中不包含品牌推荐、安装步骤或硬件兼容性说明。

生成后核对标签与箭头关系、文字边界及重叠，在实际网页的桌面和手机宽度下检查可读性、图题居中和缩放比例。显示图号由 Quarto 生成。

## 排错流程

```bash
python3 scripts/figures/ch02/gen_troubleshooting_flow.py
```

沿用已有脚本与 `ch04/common.py`，输出 `troubleshooting-flow.svg`。

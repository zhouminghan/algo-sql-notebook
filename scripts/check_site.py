#!/usr/bin/env python3
"""站点结构自检（提交前跑一遍）。

检查内容
    1. assets/js/problems.js 是唯一数据源：id 唯一、file 存在、字段完整
    2. 每个题库页面：meta[name=asn-file] 与实际路径一致
    3. 页面引用的本地资源（CSS/JS）都存在
    4. 页面内的站内链接（上下题、侧栏、首页）都能解析到真实文件
    5. 页面未再引用已下线的第三方 CSS（pico.css）
    6. 内容源 <-> 生成页 <-> problems.js 三者一一对应，没有孤儿
    7. head 规范：favicon、og:title、highlight.js 必须 defer
    8. 标题层级：分节用 h2，且不出现 h1 → h4 这类跳级
    9. 题目分类必须落在 common.js 声明的词表内（防止拼错造出新分类）
   10. 运行时约定：无障碍播报区、打印前展开折叠块的逻辑必须在 common.js 里
   11. 404.html 存在且能正确处理子路径（含 <base> 注入）
   12. 仓库卫生：本地垃圾文件必须被 .gitignore 覆盖，且尽量别留在工作区

运行
    python3 scripts/check_site.py        # 0 = 通过，1 = 有问题
"""
from __future__ import annotations

import fnmatch
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBLEMS_JS = ROOT / "assets" / "js" / "problems.js"
DIRS = ("algo", "sql")
SPEC_DIRS = {"algo": ROOT / "scripts" / "specs" / "algo", "sql": ROOT / "scripts" / "specs" / "sql"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_problems() -> dict:
    text = PROBLEMS_JS.read_text(encoding="utf-8")
    return json.loads(text[text.index("{"): text.rindex("}") + 1])


def check_data(data: dict) -> None:
    seen_ids: dict[tuple[str, int], str] = {}
    seen_files: dict[str, str] = {}
    for dirname, items in data.items():
        if dirname not in DIRS:
            warn(f"problems.js 出现未知题库分区：{dirname}")
            continue
        for p in items:
            for key in ("id", "title", "diff", "file"):
                if not p.get(key):
                    err(f"problems.js {dirname} 条目缺字段 {key}: {p}")
            if p["diff"] not in ("easy", "medium", "hard"):
                err(f"problems.js {dirname}#{p.get('id')} 难度取值非法：{p['diff']}")
            key = (dirname, p["id"])
            if key in seen_ids:
                err(f"problems.js {dirname} 题号重复：{p['id']}")
            seen_ids[key] = p["title"]
            f = p["file"]
            if f in seen_files:
                err(f"problems.js 文件重复登记：{f}")
            seen_files[f] = p["title"]
            if not f.startswith(dirname + "/"):
                err(f"problems.js {f} 与所在分区 {dirname} 不一致")
            if not (ROOT / f).exists():
                err(f"problems.js 登记的页面不存在：{f}")

            spec = SPEC_DIRS[dirname] / pathlib.Path(f).name
            if dirname == "sql" and not spec.exists():
                err(f"SQL 内容源缺失：{spec.relative_to(ROOT)}")
    print(f"· problems.js：{sum(len(v) for v in data.values() if isinstance(v, list))} 条题目登记")


def check_pages(data: dict) -> None:
    registered = {p["file"] for items in data.values() if isinstance(items, list) for p in items}
    pages = [PH for d in DIRS for PH in sorted((ROOT / d).glob("*.html"))]

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")
        label = rel

        if rel not in registered:
            err(f"{label} 未在 problems.js 登记（孤儿页面）")
        if 'lang="zh-CN"' not in text:
            err(f"{label} 缺少 lang=zh-CN")
        if "pico.min.css" in text:
            err(f"{label} 仍引用已下线的 pico.min.css")

        m = re.search(r'<meta name="asn-file" content="([^"]+)"', text)
        if not m:
            err(f"{label} 缺少 <meta name=asn-file>（侧栏高亮/上一题下一题会失效）")
        elif m.group(1) != rel:
            err(f"{label} asn-file 写成 {m.group(1)}，与实际路径不一致")

        if text.count("<h1") != 0:
            warn(f"{label} 正文里出现 <h1>，标题应由题头组件生成")

        # 本地资源引用
        for href in re.findall(r'(?:src|href)="([^"#]+)"', text):
            if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            target = (page.parent / href).resolve()
            if not target.exists():
                err(f"{label} 引用的资源不存在：{href}")

        # 站内链接
        for href in re.findall(r'href="((?:\.\./)?(?:algo|sql)/[^"#]+|[^"/:#]+\.html)"', text):
            target = (page.parent / href).resolve()
            if not target.exists():
                err(f"{label} 站内链接失效：{href}")

    print(f"· 页面：{len(pages)} 个（algo {len(list((ROOT / 'algo').glob('*.html')))} / "
          f"sql {len(list((ROOT / 'sql').glob('*.html')))}）")

    # 孤儿内容源
    for dirname, spec_dir in SPEC_DIRS.items():
        if not spec_dir.exists():
            continue
        suffix = ".py" if dirname == "algo" else ".html"
        # 内容源与页面同名、仅扩展名不同（algo: .py / sql: .html）
        names = {f.stem for f in spec_dir.glob("*" + suffix) if f.name != "__init__.py"}
        pages_here = {f.stem for f in (ROOT / dirname).glob("*.html")}
        for name in sorted(names - pages_here):
            err(f"{dirname} 内容源没有对应页面：{spec_dir.relative_to(ROOT)}/{name}")
        for name in sorted(pages_here - names):
            err(f"{dirname} 页面没有对应内容源：{name}")

    # 首页
    index = ROOT / "index.html"
    if not index.exists():
        err("缺少 index.html")
    else:
        text = index.read_text(encoding="utf-8")
        if 'id="catalog"' not in text:
            err("index.html 缺少 #catalog 容器")
        if "pico.min.css" in text:
            err("index.html 仍引用 pico.min.css")


def main() -> int:
    data = load_problems()
    check_data(data)
    check_pages(data)
    check_design_tokens()
    check_head_contract()
    check_heading_levels()
    check_category_vocabulary(data)
    check_runtime_contract()
    check_404()
    check_hygiene()


def check_design_tokens() -> None:
    """CSS 变量是设计系统的唯一入口：任何被引用但没定义的变量都会静默失效。"""
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    defined = set(re.findall(r"^\s*(--[a-z0-9-]+)\s*:", css, re.M))

    sources = list((ROOT / "assets").rglob("*.js")) + list(ROOT.glob("*.html"))
    sources += list((ROOT / "algo").glob("*.html")) + list((ROOT / "sql").glob("*.html"))
    for path in sources:
        used = set(re.findall(r"var\((--[a-z0-9-]+)", path.read_text(encoding="utf-8")))
        for name in sorted(used - defined):
            err(f"{path.relative_to(ROOT)} 引用了未定义的 CSS 变量 {name}")
    print(f"· 设计令牌：style.css 定义了 {len(defined)} 个变量，引用全部可解析")


def check_head_contract() -> None:
    """favicon / 分享元信息 / highlight.js 的 defer —— 缺一个都会掉到线上才发现。"""
    pages = [p for d in DIRS for p in sorted((ROOT / d).glob("*.html"))]
    pages += [ROOT / "index.html", ROOT / "404.html"]
    n = 0
    for page in pages:
        if not page.exists():
            continue
        n += 1
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")

        m = re.search(r'<link rel="icon" href="([^"]+)"', text)
        if not m:
            err(f"{rel} 缺少 favicon <link rel=icon>")
        elif not (page.parent / m.group(1)).exists():
            err(f"{rel} 的 favicon 指向不存在的文件：{m.group(1)}")
        if 'property="og:title"' not in text:
            err(f"{rel} 缺少 og:title（分享出去没有标题）")
        if "highlight.min.js" in text and not re.search(r"<script defer src=\"[^\"]*highlight\.min\.js\"", text):
            err(f"{rel} 的 highlight.min.js 没有 defer（121KB 会阻塞首屏）")
    print(f"· head 规范：{n} 个页面（favicon / og:title / defer）")


def check_heading_levels() -> None:
    """h1 = 题目标题，分节 = h2。跳级会影响屏幕阅读器按标题导航。"""
    pages = [p for d in DIRS for p in sorted((ROOT / d).glob("*.html"))]
    bad = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        levels = [int(m) for m in re.findall(r"<h([1-4])[ >]", text)]
        h2 = levels.count(2)
        if h2 < 3:
            err(f"{page.relative_to(ROOT)} 分节标题不足（h2={h2}），应至少 3 个")
            bad += 1
        try:
            first_h2 = levels.index(2)
        except ValueError:
            err(f"{page.relative_to(ROOT)} 完全没有 h2 分节标题")
            bad += 1
            continue
        deeper = [i for i, lv in enumerate(levels) if lv >= 3]
        if deeper and min(deeper) < first_h2:
            err(f"{page.relative_to(ROOT)} 标题层级跳级（h3/h4 出现在第一个 h2 之前）")
            bad += 1
    print(f"· 标题层级：{len(pages)} 个页面，{len(pages) - bad} 个通过")


def check_category_vocabulary(data: dict) -> None:
    """分类名由 common.js 的 CAT_ORDER 声明；problems.js 写了词表外的名字就报错。"""
    js = (ROOT / "assets" / "js" / "common.js").read_text(encoding="utf-8")
    block = js[js.index("var CAT_ORDER"): js.index("var DIFF_MAP")]
    declared = {
        "algo": set(re.findall(r"'([^']+)'", block.split("algo:")[1].split("]")[0])),
        "sql": set(re.findall(r"'([^']+)'", block.split("sql:")[1].split("]")[0])),
    }
    for dirname, items in data.items():
        if dirname not in DIRS:
            continue
        for p in items:
            cat = p.get("cat")
            if cat and cat not in declared[dirname]:
                err(f"problems.js {dirname}#{p['id']} 的分类「{cat}」不在 common.js 的 CAT_ORDER 词表里")
    print(f"· 分类词表：algo {len(declared['algo'])} 类 / sql {len(declared['sql'])} 类")


def check_runtime_contract() -> None:
    """外壳里的关键能力：用字符串断言防止以后被误删。"""
    js = (ROOT / "assets" / "js" / "common.js").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    required = [
        (js, "aria-live", "无障碍播报区（搜索结果/进度变化）"),
        (js, "beforeprint", "打印前展开折叠块"),
        (js, "tb-progress-trigger", "进度弹层入口"),
        (js, "scrollTop", "侧栏滚动定位（不能用 scrollIntoView 拖走整页）"),
        (css, "@media print", "打印样式"),
        (css, ".popover", "进度弹层样式"),
    ]
    for text, needle, label in required:
        if needle not in text:
            err(f"缺少运行时约定：{label}（找不到「{needle}」）")
    print("· 运行时约定：播报区 / 打印展开 / 进度弹层 / 侧栏滚动 / 打印样式")


def check_404() -> None:
    page = ROOT / "404.html"
    if not page.exists():
        err("缺少 404.html（GitHub Pages 会走默认 404 页）")
        return
    text = page.read_text(encoding="utf-8")
    if "<base" not in text:
        err("404.html 缺少 <base> 注入：Pages 在深层 URL 下会解析错资源路径")
    print("· 404 页：存在且带子路径兜底")


# 本地会产生、但绝不该入库的东西：(说明, 用于匹配 .gitignore 的样本名, 用于扫描工作区的通配符)
JUNK_KINDS = [
    ("__pycache__ 目录", "__pycache__/", "__pycache__"),
    ("Python 字节码", "x.pyc", "*.py[co]"),
    ("macOS 元数据", ".DS_Store", ".DS_Store"),
    ("日志", "x.log", "*.log"),
    ("临时文件", "x.tmp", "*.tmp"),
    ("编辑器备份", "x.swp", "*.swp"),
    ("编辑器临时文件", "x~", "*~"),
]
SKIP_DIRS = {".git"}


def _ignored(name: str, rules: list[str]) -> bool:
    """按 .gitignore 的常见写法做一次匹配（够用即可，不追求完整实现 git 语义）。"""
    for rule in rules:
        rule = rule.strip()
        if not rule or rule.startswith("#") or rule.startswith("!"):
            continue
        if rule.endswith("/"):
            if name.startswith(rule) or name == rule.rstrip("/"):
                return True
        elif fnmatch.fnmatch(name, rule) or name == rule:
            return True
    return False


def check_hygiene() -> None:
    """仓库卫生：垃圾文件是否都被 .gitignore 覆盖；顺便报出工作区里现存的垃圾。"""
    rules = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    for label, sample, _ in JUNK_KINDS:
        if not _ignored(sample, rules):
            err(f".gitignore 没有覆盖「{label}」（样本 {sample}）")

    found: dict[str, int] = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in dirnames + filenames:
            for label, _, pattern in JUNK_KINDS:
                if fnmatch.fnmatch(name, pattern):
                    found[label] = found.get(label, 0) + 1
                    break

    if found:
        detail = "、".join(f"{k} {v} 个" for k, v in sorted(found.items()))
        warn(f"工作区里还有本地垃圾（已被 git 忽略，建议顺手删掉）：{detail}")
    print(f"· 仓库卫生：{len(JUNK_KINDS)} 类本地文件均已被 .gitignore 覆盖"
          + (f"，现存 {sum(found.values())} 个" if found else "，工作区干净"))

    if warnings:
        print("\n警告：")
        for w in warnings:
            print("  ~ " + w)
    if errors:
        print("\n错误：")
        for e in errors:
            print("  x " + e)
        print(f"\n自检未通过：{len(errors)} 个错误 / {len(warnings)} 个警告")
        return 1
    print(f"\n自检通过：0 个错误 / {len(warnings)} 个警告")
    return 0


if __name__ == "__main__":
    sys.exit(main())

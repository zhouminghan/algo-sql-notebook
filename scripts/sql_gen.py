#!/usr/bin/env python3
"""SQL 题页面生成器。

内容源：scripts/specs/sql/<文件名>.html —— 只写正文 + 图解脚本，不写外壳。
元数据：assets/js/problems.js 里的 sql 条目（id/title/diff/tags/cat/file/file 决定输出名）。
输出：  sql/<文件名>.html —— 外壳（题头、左侧导航、右侧目录、上一下一）
        由 assets/js/common.js 在运行时注入。

为什么正文用 HTML 而不是 Markdown
    SQL 题解由「N 帧图解 + 每帧一段 CTE + SVG 表格」构成，帧之间是严格顺序的
    结构而不是自由文本，HTML 片段能 1:1 保留既有内容，避免解析歧义。

运行：
    python3 scripts/sql_gen.py             # 生成全部 SQL 题
    python3 scripts/sql_gen.py --id 2      # 只生成 002
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"
SPECS_DIR = ROOT / "scripts" / "specs" / "sql"
PROBLEMS_JS = ROOT / "assets" / "js" / "problems.js"

HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="asn-file" content="@@FILE@@">
<meta name="description" content="@@NUM@@. @@TITLE@@ — SQL 机试题图解：源数据 + CTE 分帧 + 完整答案 + 易错点 + 自我检验。">
<title>@@NUM@@. @@TITLE@@ — algo-sql-notebook</title>
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:title" content="@@NUM@@. @@TITLE@@">
<meta property="og:description" content="SQL 机试题图解：源数据 + CTE 分帧 + 完整答案 + 易错点 + 自我检验。">
<script>
(function () {
  // localStorage 在隐私模式/受限环境可能抛异常，兜底回退到系统偏好
  try {
    var s = localStorage.getItem('asn-theme');
    var d = s || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', d);
  } catch (e) {}
})();
</script>
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="stylesheet" href="../assets/vendor/github.min.css">
<script src="../assets/js/problems.js"></script>
<script src="../assets/js/common.js"></script>
<script src="../assets/js/draw-utils.js"></script>
<script defer src="../assets/vendor/highlight.min.js"></script>
</head>
<body>

"""

TAIL = """
</body>
</html>
"""


def load_meta() -> dict:
    """从 problems.js 读取 sql 条目（单一数据源）。"""
    text = PROBLEMS_JS.read_text(encoding="utf-8")
    data = json.loads(text[text.index("{"): text.rindex("}") + 1])
    return data


def render(meta: dict, fragment: str) -> str:
    name = meta["file"].split("/")[-1]
    head = (HEAD
            .replace("@@FILE@@", meta["file"])
            .replace("@@NUM@@", f"{meta['id']:03d}")
            .replace("@@TITLE@@", meta["title"]))
    return head + fragment.strip() + "\n" + TAIL


def generate(only_id=None) -> int:
    data = load_meta()
    items = [p for p in data.get("sql", []) if p.get("file")]
    if only_id is not None:
        items = [p for p in items if p["id"] == only_id]
    if not items:
        print("没有可生成的 SQL 题", f"(id={only_id})" if only_id else "")
        return 1

    missing = []
    for meta in items:
        name = meta["file"].split("/")[-1]
        spec = SPECS_DIR / name
        if not spec.exists():
            missing.append(str(spec.relative_to(ROOT)))
            continue
        out = SQL_DIR / name
        out.write_text(render(meta, spec.read_text(encoding="utf-8")), encoding="utf-8")
        print("written", meta["file"])

    if missing:
        print("\n缺少内容源：")
        for m in missing:
            print("  -", m)
        return 1
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    oid = int(args[args.index("--id") + 1]) if "--id" in args else None
    sys.exit(generate(oid))

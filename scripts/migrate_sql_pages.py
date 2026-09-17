#!/usr/bin/env python3
"""一次性迁移脚本：把历史上手写的 sql/*.html 拆成「内容源」。

背景
    早期 SQL 题页面是手写整页 HTML（页面外壳、正文、图解脚本混在一个文件里），
    改一次外壳要动 6 个文件。迁移后内容源只保留「正文 + 图解脚本」，
    外壳统一由 scripts/sql_gen.py 套用，与算法题（specs/algo -> algo/）对齐。

产物
    scripts/specs/sql/<与 sql/ 下同名的>.html
    内容 = 原 <body> 内的正文 + 末尾的图解脚本；内联样式换成语义 class。

安全性
    默认不覆盖已存在的内容源，需要显式 --force 才重写。

运行
    python3 scripts/migrate_sql_pages.py
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"
SPECS_DIR = ROOT / "scripts" / "specs" / "sql"


def normalize(body: str) -> tuple[str, list[str]]:
    """内联样式 -> 语义 class；折叠块 -> 原生 <details>。返回 (正文, 残留样式列表)。"""
    # 1. 图解卡片：间距交给 CSS
    body = re.sub(r'(class="frame-card")\s+style="margin-bottom:[^"]*"', r"\1", body)

    # 2. 代码语言标题
    body = re.sub(r'<h4 style="margin-bottom:[^"]*">', "<h4>", body)

    # 3. 自我检验区块
    body = body.replace('<div style="margin-top:0.5rem;">', '<div class="selfcheck-body">')
    body = body.replace(
        '<p style="color:var(--color-done);margin-left:1rem;">',
        '<p class="selfcheck-answer">',
    )
    body = body.replace("<summary><strong>自我检验</strong></summary>", "<summary>自我检验</summary>")

    # 4. 帧说明 / 脚注
    body = re.sub(r'<div class="frame-caption" style="[^"]*">', '<div class="frame-caption">', body)
    body = body.replace(
        '<p style="margin-top:1rem;color:var(--color-neutral);font-size:0.85rem;">',
        '<p class="frame-note">',
    )

    # 5. 本地复现折叠块：改用原生 details，去掉手写的 class 切换脚本
    body = body.replace('<details id="ddlToggle">', '<details class="collapsible">')
    body = re.sub(r'<summary class="collapsible-toggle" onclick="[^"]*">', "<summary>", body)
    body = body.replace('<div id="ddlBody" class="collapsible-body">', '<div class="collapsible-body">')
    body = re.sub(
        r'<button id="ddlAllCopy" class="copy-btn" style="display:block"',
        '<button type="button" id="ddlAllCopy" class="copy-btn copy-btn--block"',
        body,
    )

    # 6. 复制按钮统一补 type
    body = body.replace(
        '<button class="copy-btn" onclick=', '<button type="button" class="copy-btn" onclick='
    )

    # 7. 兜底：记录并清掉残留内联样式
    left = [m.group(1) for m in re.finditer(r'style="([^"]*)"', body)]
    body = re.sub(r'\s+style="[^"]*"', "", body)
    return body.strip() + "\n", left


def split_page(text: str) -> tuple[str, str]:
    """拆出 <body> 内的正文与末尾的图解脚本。"""
    body = text[text.index("<body>") + len("<body>"): text.rindex("</body>")]
    at = body.rindex("<script>")
    return body[:at].strip() + "\n", body[at:].strip()


def migrate(force: bool) -> int:
    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    pages = sorted(SQL_DIR.glob("*.html"))
    if not pages:
        print("sql/ 下没有页面可迁移")
        return 1

    written = 0
    for page in pages:
        target = SPECS_DIR / page.name
        if target.exists() and not force:
            print("skip (已存在)", target.relative_to(ROOT))
            continue
        content, script = split_page(page.read_text(encoding="utf-8"))
        content, left = normalize(content)
        if left:
            print(f"  ! {page.name} 移除的残留内联样式：{sorted(set(left))}")
        target.write_text(content + "\n" + script + "\n", encoding="utf-8")
        written += 1
        print("written", target.relative_to(ROOT))

    print(f"\n迁移完成：{written} 个内容源 -> scripts/specs/sql/")
    print("下一步：python3 scripts/sql_gen.py")
    return 0


if __name__ == "__main__":
    sys.exit(migrate(force="--force" in sys.argv[1:]))

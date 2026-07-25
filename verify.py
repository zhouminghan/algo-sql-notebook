#!/usr/bin/env python3
"""
verify.py — 自动化验证脚本

运行: python verify.py

检查每道渲染好的题目页面，确保：
1. 关键 HTML 元素存在
2. 没有明显的渲染错误（未转义 markdown、重复标签等）
3. Walkthrough 数据可解析（如果有的话）
"""

import json
import re
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
ERRORS = []


def check(condition: bool, msg: str):
    if not condition:
        ERRORS.append(msg)
        print(f"  ❌ {msg}")
        return False
    return True


def verify_algo(html_path: Path):
    html = html_path.read_text(encoding="utf-8")
    pid = html_path.stem
    ok = True

    # 1. 基础结构
    ok &= check("</html>" in html, f"{pid}: 缺少闭合 </html>")
    ok &= check("CodeMirror" in html or "codemirror" in html.lower(),
               f"{pid}: 缺少 CodeMirror 引用")
    ok &= check("playback-trigger" in html,
               f"{pid}: 缺少 playback-trigger 按钮")

    # 2. 不要有双重 <pre> 标签（历史 bug）
    ok &= check("<pre><pre>" not in html and "</pre></pre>" not in html,
               f"{pid}: 双重 pre 标签（历史bug复现）")

    # 3. Walkthrough 数据
    m = re.search(r'WALKTHROUGH_DATA\s*=\s*null;', html)
    if not m:
        m = re.search(r'_rawData\s*=\s*(.*?);\s*if', html, re.DOTALL)
        if m:
            raw = m.group(1).strip()
            try:
                data = json.loads(raw) if raw != '""' and raw != 'null' else None
                if data and "steps" in data:
                    print(f"  ✅ {pid}: {len(data['steps'])} 步 walkthrough, "
                          f"code_python {len(data['code_python'].split(chr(10)))} 行")
                else:
                    print(f"  ℹ️  {pid}: 无 walkthrough 数据")
            except json.JSONDecodeError:
                ok &= check(False, f"{pid}: walkthrough JSON 解析失败")

    # 4. 检查未转义的 markdown（常见 bug）—— 只在可见内容中检查
    visible = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    visible = re.sub(r'<style[^>]*>.*?</style>', '', visible, flags=re.DOTALL)
    bad_patterns = [
        (r'<p>[^<]*\*\*[^*]+\*\*', "段落中未转义粗体"),
    ]
    for pattern, desc in bad_patterns:
        matches = list(re.finditer(pattern, visible))
        if matches:
            ok &= check(False, f"{pid}: {desc} ({len(matches)}处)")
    # BUT: <b> 包裹的粗体是正常的
    if re.search(r'<b>[^<]+</b>', visible):
        ok &= check(True, "")  # no-op, just acknowledge

    return ok


def verify_sql(html_path: Path):
    html = html_path.read_text(encoding="utf-8")
    pid = html_path.stem
    ok = True

    ok &= check("</html>" in html, f"{pid}: 缺少闭合 </html>")
    ok &= check("CodeMirror" in html or "codemirror" in html.lower(),
               f"{pid}: 缺少 CodeMirror 引用")
    ok &= check("scenario" in html, f"{pid}: 缺少 scenario 区域")
    ok &= check("table-info" in html, f"{pid}: 缺少 table-info 表格")
    ok &= check("collapsible" in html or "折叠" in html or "toggle" in html,
               f"{pid}: 缺折叠区")

    # SQL 描述中不应有原始 markdown
    bad = ["**" in html, "```sql" in html]
    # Actually, check more carefully: do they appear inside scenario div?
    m = re.search(r'class="scenario">(.*?)(?=<div class="table-info")', html, re.DOTALL)
    if m:
        content = m.group(1)
        if "**" in content:
            ok &= check(False, f"{pid}: scenario 中有未转义的 ** 粗体")
        if "```" in content:
            ok &= check(False, f"{pid}: scenario 中有未转义的代码块")

    return ok


def main():
    print("🔍 验证输出文件...")
    print()

    all_ok = True

    algo_dir = OUTPUT_DIR / "algo"
    if algo_dir.exists():
        for f in sorted(algo_dir.glob("*.html")):
            all_ok &= verify_algo(f)

    sql_dir = OUTPUT_DIR / "sql"
    if sql_dir.exists():
        for f in sorted(sql_dir.glob("*.html")):
            all_ok &= verify_sql(f)

    print()
    if ERRORS:
        print(f"❌ {len(ERRORS)} 个错误:")
        for e in ERRORS:
            print(f"   {e}")
        sys.exit(1)
    else:
        print("✅ 全部验证通过")
        sys.exit(0)


if __name__ == "__main__":
    main()

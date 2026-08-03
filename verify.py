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

    # 1.5 检查 localStorage 进度（v2.3 静态化要求）
    ok &= check("shared/progress.js" in html or "progressData" in html or "STORAGE_KEY" in html,
               f"{pid}: 缺少 localStorage 进度（shared/progress.js 或 progressData）")
    ok &= check("shared/splitter.js" in html or "setVSplit" in html,
               f"{pid}: 缺少 shared/splitter.js 引用")

    # 1.6 JS 语法检查
    ok &= verify_js_syntax(html_path)

    # 2.5 检查 walkthrough 函数完整性
    required_funcs = ["escHtml", "openPlayback", "renderCodePanel", "renderPlayerStep"]
    for fn in required_funcs:
        if "WALKTHROUGH_DATA" in html and html.count("WALKTHROUGH_DATA") > 0:
            ok &= check(f"function {fn}" in html or f"{fn} = function" in html or f"function {fn}(" in html,
                       f"{pid}: 缺少函数 {fn}()")

    # 2. 不要有双重 <pre> 标签（历史 bug）
    ok &= check("<pre><pre>" not in html and "</pre></pre>" not in html,
               f"{pid}: 双重 pre 标签（历史bug复现）")

    # 2.2 检查不包含 API 调用（v2.3 静态化要求）
    ok &= check("/api/" not in html, f"{pid}: 包含 /api/ 请求（v2.3 应纯静态）")

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
                    # 检查步骤数据完整性
                    for i, step in enumerate(data["steps"]):
                        ok &= check("hint" in step or "desc" in step,
                                   f"{pid}: 步骤 {i} 缺少 hint/desc")
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

    # v2.3: 纯静态检查 — SQL 页面不应该包含 API 调用
    ok &= check("/api/sql/execute" not in html,
               f"{pid}: 包含 /api/sql/execute (v2.3 应移除)")
    ok &= check("/api/" not in html,
               f"{pid}: 包含 /api/ 请求 (v2.3 应纯静态)")

    # v2.3: DDL 复制功能检查
    ok &= check("copyDDL" in html,
               f"{pid}: 缺少 copyDDL 函数 (v2.3 需要)")
    ok &= check("{{SQL_INIT_SQL}}" not in html,
               f"{pid}: 包含未替换的 {{SQL_INIT_SQL}} 占位符")

    # v2.3: localStorage 进度
    ok &= check("shared/progress.js" in html or "progressData" in html,
               f"{pid}: 缺少 localStorage 进度 (shared/progress.js)")

    # v2.3: JS 语法检查
    ok &= verify_js_syntax(html_path)

    # SQL 描述中不应有原始 markdown
    m = re.search(r'class="scenario">(.*?)(?=<div class="table-info")', html, re.DOTALL)
    if m:
        content = m.group(1)
        if "**" in content:
            ok &= check(False, f"{pid}: scenario 中有未转义的 ** 粗体")
        if "```" in content:
            ok &= check(False, f"{pid}: scenario 中有未转义的代码块")

    return ok


def verify_js_syntax(html_path: Path):
    """检查内联 JS 的致命语法问题（模板占位符残留、未闭合模板字面量）"""
    html = html_path.read_text(encoding="utf-8")
    pid = html_path.stem
    ok = True

    # 提取所有内联 <script> 块内容
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)

    for i, block in enumerate(script_blocks):
        label = f"{pid}:script-{i}"

        # 0. 括号平衡（致命错误）
        braces_diff = block.count("{") - block.count("}")
        if braces_diff != 0:
            ok &= check(False, f"{label}: 大括号不平衡 (多{'左' if braces_diff > 0 else '右'}{abs(braces_diff)}个)")

        # 1. 未替换的模板占位符（致命错误）
        for m in re.finditer(r'\{\{(.+?)\}\}', block):
            ok &= check(False, f"{label}: 未替换的占位符 {{{{ {m.group(1)} }}}}")
        if "}}" in block and "{{" not in block:
            ok &= check(False, f"{label}: 残留的 }}}}")

        # 2. DDL_SQL 模板字面量闭合检查
        if "DDL_SQL" in block:
            ddl_m = re.search(r'DDL_SQL\s*=\s*`', block)
            if ddl_m:
                pos = ddl_m.end()
                while pos < len(block) and block[pos] != "`":
                    if block[pos:pos+2] == "\\" and pos+1 < len(block):
                        pos += 1  # 跳过转义
                    pos += 1
                if pos >= len(block):
                    ok &= check(False, f"{label}: DDL_SQL 模板字面量未闭合")

        # 3. 字符串字面量含裸换行（不通过 + 拼接的跨行字符串 = 语法错误）
        for m in re.finditer(r'=\s*"([^"]*\n[^"]*)"', block):
            # 排除末尾有 + 的情况（正常拼接）
            end_pos = m.end()
            rest = block[end_pos:end_pos+5].strip()
            if not rest.startswith("+"):
                ok &= check(False, f"{label}: 字符串含裸换行 '{m.group(1)[:40]}...'")

    return ok


def verify_walkthrough_json(json_path: Path):
    """验证 walkthrough JSON 文件的结构完整性"""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        check(False, f"{json_path.name}: JSON 解析失败 ({e})")
        return

    pid = json_path.stem.replace("-walkthrough", "")

    # 检查 db_init_sql（SQL 题型）
    if "db_init_sql" in data and data["db_init_sql"]:
        print(f"  ✅ {pid}: db_init_sql {len(data['db_init_sql'])} 字符")

    # 检查 steps
    steps = data.get("steps", [])
    if not steps:
        check(False, f"{json_path.name}: steps 为空")
        return

    print(f"  ✅ {pid}: {len(steps)} 步 walkthrough (JSON)")

    for i, step in enumerate(steps):
        if "sql" in step:
            # SQL 步骤：必须有 columns 和 rows
            check("columns" in step, f"{json_path.name}: 步骤 {i} ({step.get('label','?')}) 缺少 columns")
            check("rows" in step, f"{json_path.name}: 步骤 {i} ({step.get('label','?')}) 缺少 rows")
        else:
            # 算法步骤：必须有 hint/desc
            check("hint" in step or "desc" in step, f"{json_path.name}: 步骤 {i} 缺少 hint/desc")


def smoke_test():
    """启动本地服务 → 请求关键页面 → 验证 HTTP 200 + 关键内容"""
    import subprocess
    import urllib.request
    import urllib.parse
    import time

    PORT = 9876  # 测试用非标准端口
    BASE = f"http://localhost:{PORT}"
    ok = True

    # 启动 server.py
    print("🌐 冒烟测试：启动 server.py ...")
    base_dir = Path(__file__).parent
    server_script = base_dir / "server.py"
    proc = subprocess.Popen(
        [sys.executable, str(server_script), str(PORT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        cwd=str(base_dir)
    )
    time.sleep(0.5)

    def fetch(path, desc):
        nonlocal ok
        try:
            # URL 编码中文路径
            url = f"{BASE}{urllib.parse.quote(path, safe='/')}"
            resp = urllib.request.urlopen(url, timeout=3)
            content = resp.read().decode("utf-8", errors="replace")
            if resp.status == 200:
                print(f"  ✅ {desc} → 200 ({len(content)} 字节)")
            else:
                ok &= check(False, f"{desc} → HTTP {resp.status}")
            return content
        except Exception as e:
            ok &= check(False, f"{desc} → 连接失败: {e}")
            return ""

    # 首页
    html = fetch("/", "首页")
    # 算法页
    for f in sorted((OUTPUT_DIR / "algo").glob("*.html")):
        pid = f.stem
        fetch(f"/algo/{pid}", f"算法 {pid}")
    # SQL 页
    for f in sorted((OUTPUT_DIR / "sql").glob("*.html")):
        pid = f.stem
        fetch(f"/sql/{pid}", f"SQL {pid}")
    # 资源文件
    fetch("/index.json", "index.json")
    fetch("/lib/codemirror.min.js", "CodeMirror")

    # 停服务
    proc.terminate()
    proc.wait(timeout=3)
    return ok


def main():
    print("🔍 验证输出文件...")
    print()

    all_ok = True

    # 1. 检查 walkthrough JSON 文件
    for jf in sorted(OUTPUT_DIR.glob("*-walkthrough.json")):
        verify_walkthrough_json(jf)

    # 2. 检查 HTML 文件
    algo_dir = OUTPUT_DIR / "algo"
    if algo_dir.exists():
        for f in sorted(algo_dir.glob("*.html")):
            all_ok &= verify_algo(f)

    sql_dir = OUTPUT_DIR / "sql"
    if sql_dir.exists():
        for f in sorted(sql_dir.glob("*.html")):
            all_ok &= verify_sql(f)

    # 3. 服务端冒烟测试
    if ERRORS:
        print(f"\n⚠️  静态检查有误，跳过冒烟测试")
    else:
        print()
        all_ok &= smoke_test()

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

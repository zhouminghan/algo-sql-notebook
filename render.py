#!/usr/bin/env python3
"""
render.py — Markdown → HTML 渲染器

将 problems/ 下的题目 markdown 配合模板生成 output/ 下的 HTML 文件。

用法:
  python render.py              # 渲染全部题目
  python render.py 001-两数之和 # 渲染单题（算法）
  python render.py SQL01-连续登录天数  # 渲染单题（SQL）
"""

import csv
import io
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROBLEMS_DIR = BASE_DIR / "problems"
FRONTEND_DIR = BASE_DIR / "frontend"
OUTPUT_DIR = BASE_DIR / "output"


def load_template(name: str) -> str:
    path = FRONTEND_DIR / name / "template.html"
    if not path.exists():
        print(f"模板不存在: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ═══════════════════════════════════════════════════════════
#  算法题解析
# ═══════════════════════════════════════════════════════════

def extract_code_template(full_code: str, lang: str) -> str:
    """从完整代码中提取函数签名作为做题模板，保证缩进和花括号配对"""
    lines = full_code.strip().split("\n")
    template_lines = []
    in_class = False
    method_done = False

    for line in lines:
        stripped = line.strip()
        # imports
        if stripped.startswith(("import ", "from ")):
            template_lines.append(line)
            continue
        # class line
        if lang == "python" and stripped.startswith("class "):
            template_lines.append(line)
            in_class = True
            continue
        if lang == "java" and stripped.startswith(("class ", "public class")):
            template_lines.append(line)
            in_class = True
            continue
        # method signature
        if in_class and not method_done:
            is_method = False
            if lang == "python" and stripped.startswith("def "):
                is_method = True
                template_lines.append(line)
                indent = " " * 4
                template_lines.append(f"{indent}# 在此编写你的代码")
                template_lines.append(f"{indent}pass")
            if lang == "java" and ("public " in stripped or "private " in stripped or "protected " in stripped) and "(" in stripped:
                is_method = True
                template_lines.append(line)
                indent = " " * 8
                template_lines.append(f"{indent}// 在此编写你的代码")
                template_lines.append(f"{indent}return -1;")
                template_lines.append(f"    }}")
            if is_method:
                method_done = True

    # ensure class closing brace for Java
    if lang == "java" and in_class:
        template_lines.append("}")

    if not template_lines:
        # fallback: return first 6 lines
        for line in lines[:6]:
            template_lines.append(line)

    return "\n".join(template_lines)


def parse_examples(text: str) -> str:
    """从题目描述中解析示例，生成 HTML 卡片"""
    # 匹配 **示例 N：** 后面的代码块
    pattern = r'\*\*示例\s*(\d+)\s*[：:]\s*\*\*\s*\n```\n(.*?)```'
    matches = list(re.finditer(pattern, text, re.DOTALL))
    if not matches:
        return ""

    html_parts = ['<div class="examples-section"><h3>示例</h3>']
    for m in matches:
        num = m.group(1)
        content = m.group(2).strip()
        ex = {"input": "", "output": "", "explanation": ""}
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("输入："):
                ex["input"] = escape_html(line[3:])
            elif line.startswith("输入:"):
                ex["input"] = escape_html(line[3:])
            elif line.startswith("输出："):
                ex["output"] = escape_html(line[3:])
            elif line.startswith("输出:"):
                ex["output"] = escape_html(line[3:])
            elif line.startswith("解释："):
                ex["explanation"] = escape_html(line[3:])
            elif line.startswith("解释:"):
                ex["explanation"] = escape_html(line[3:])

        html_parts.append(f'<div class="example-card">')
        html_parts.append(f'  <div class="example-num">示例 {num}</div>')
        if ex["input"]:
            html_parts.append(f'  <div class="example-row"><span class="ex-label">输入</span><code>{ex["input"]}</code></div>')
        if ex["output"]:
            html_parts.append(f'  <div class="example-row"><span class="ex-label">输出</span><code>{ex["output"]}</code></div>')
        if ex["explanation"]:
            html_parts.append(f'  <div class="example-row"><span class="ex-label">解释</span><span class="ex-text">{ex["explanation"]}</span></div>')
        html_parts.append(f'</div>')

    html_parts.append('</div>')
    return "\n".join(html_parts)


def parse_algo_md(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")

    # Title
    title_match = re.search(r"^# .+? (.+)", text, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem.split("-", 1)[-1]

    # Difficulty
    diff_map = {"简单": ("easy", "简单"), "中等": ("medium", "中等"), "困难": ("hard", "困难")}
    diff_match = re.search(r"难度.*?([简单中等困难]+)", text)
    diff_class, diff_label = diff_map.get(diff_match.group(1) if diff_match else "", ("medium", "中等"))

    # Description (plain text without examples code blocks)
    desc_match = re.search(r"## 📖 题目描述\n\n(.*?)(?:\n---|\n##)", text, re.DOTALL)
    raw_desc = desc_match.group(1).strip() if desc_match else ""
    # Strip example code blocks from description text
    desc_clean = re.sub(r'\*\*示例.*?\*\*\s*\n```.*?```', '', raw_desc, flags=re.DOTALL).strip()
    description = escape_html(desc_clean)

    # Examples as HTML
    examples_html = parse_examples(raw_desc)

    # Python
    py_match = re.search(r"## 🐍 Python 解法.*?```python\n(.*?)```", text, re.DOTALL)
    python_full = py_match.group(1).strip() if py_match else ""
    python_template = extract_code_template(python_full, "python") if python_full else ""

    # Java
    java_match = re.search(r"## ☕ Java 解法.*?```java\n(.*?)```", text, re.DOTALL)
    java_full = java_match.group(1).strip() if java_match else ""
    java_template = extract_code_template(java_full, "java") if java_full else ""

    # Keypoints
    kp_match = re.search(r"## 🧠 关键点\n(.*?)(?:\n---|\n##|$)", text, re.DOTALL)
    keypoints = kp_match.group(1).strip() if kp_match else ""
    keypoints_html = ""
    for line in keypoints.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "1. ", "2. ", "3. ", "4. ")):
            keypoints_html += f"<li>{stripped.lstrip('- 1234567890. ')}</li>"

    # Gotchas
    gotcha_match = re.search(r"## 🔄 易错点\n(.*?)(?:\n---|\n##|$)", text, re.DOTALL)
    gotchas = gotcha_match.group(1).strip() if gotcha_match else ""
    gotchas_html = ""
    for line in gotchas.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "1. ", "2. ", "3. ", "4. ")):
            gotchas_html += f"<li>{stripped.lstrip('- 1234567890. ')}</li>"

    return {
        "title": title,
        "difficulty_class": diff_class,
        "difficulty": diff_label,
        "description": description,
        "examples": examples_html,
        "python_full": escape_html(python_full),
        "java_full": escape_html(java_full),
        "python_template": escape_html(python_template),
        "java_template": escape_html(java_template),
        "keypoints": keypoints_html,
        "gotchas": gotchas_html,
    }


# ═══════════════════════════════════════════════════════════
#  SQL 题解析
# ═══════════════════════════════════════════════════════════

def parse_init_sql_schema_and_data(sql_path: Path):
    """从 init SQL 提取所有表结构 + 示例数据，使用真实列名作为表头

    Returns: (schema_html, sample_html, first_table_name)
    其中 schema_html 包含所有表结构，sample_html 包含所有示例数据
    """
    content = sql_path.read_text(encoding="utf-8")

    # ── 提取 CREATE TABLE → {table_name: [col_names]}
    tables = re.findall(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)
    if not tables:
        return "", "", ""

    table_columns = {}  # table_name → [(col_name, col_type), ...]
    for table_name, cols_text in tables:
        columns = []
        for line in cols_text.split("\n"):
            line = line.strip().rstrip(",")
            if not line or line.startswith("--"):
                continue
            parts = line.split(None, 1)
            if parts:
                col_name = parts[0].strip('"`')
                col_type = parts[1].strip() if len(parts) > 1 else ""
                columns.append((col_name, col_type))
        table_columns[table_name] = columns

    # ── 生成结构 HTML
    schema_parts = []
    for table_name, columns in table_columns.items():
        html = '<div class="table-info">'
        html += f'<h4>表：{table_name}</h4>'
        html += '<table><thead><tr><th>列名</th><th>类型</th></tr></thead><tbody>'
        for name, dtype in columns:
            html += f'<tr><td><code>{name}</code></td><td>{dtype}</td></tr>'
        html += '</tbody></table></div>'
        schema_parts.append(html)
    schema_html = "\n".join(schema_parts)

    # ── 提取 INSERT → {table_name: [(val1, val2, ...)]}
    pattern = r'INSERT INTO\s+(\w+)\s+VALUES\s*(.*?);'
    inserts = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

    sample_parts = []
    for table_name, values_text in inserts:
        columns = table_columns.get(table_name, [])
        col_names = [c[0] for c in columns]  # 提取列名列表

        clean_text = "\n".join(
            line for line in values_text.split("\n")
            if not line.strip().startswith("--")
        )
        rows = []
        vals = re.findall(r"\(([^)]+)\)", clean_text)
        for v in vals:
            row = [c.strip().strip("'\"") for c in v.split(",")]
            rows.append(row)

        if not rows:
            continue

        html = f'<div class="table-info sample"><h4>示例数据：{table_name}</h4>'
        html += '<table><thead><tr>'
        # 使用真实列名作为表头
        ncols = len(rows[0])
        for i in range(ncols):
            header = col_names[i] if i < len(col_names) else f'列 {i+1}'
            html += f'<th>{header}</th>'
        html += '</tr></thead><tbody>'
        for row in rows:
            html += '<tr>'
            for cell in row:
                html += f'<td>{cell}</td>'
            html += '</tr>'
        html += '</tbody></table></div>'
        sample_parts.append(html)
    sample_html = "\n".join(sample_parts)

    first_name = tables[0][0] if tables else ""
    return schema_html, sample_html, first_name


def _md_table_to_html(md_table_text: str) -> str:
    """将 markdown 表格转 HTML 表格（跳过 `|---|---|` 分隔行）"""
    lines = [l.strip() for l in md_table_text.strip().split("\n") if l.strip()]
    if len(lines) < 2:
        return escape_html(md_table_text)

    # 过滤掉分隔行（如 |---|----|）
    data_lines = []
    for line in lines:
        # 分隔行特征：只包含 |、-、:、空格
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue
        data_lines.append(line)

    if len(data_lines) < 2:
        return escape_html(md_table_text)

    html = '<table><thead><tr>'
    headers = [c.strip() for c in data_lines[0].strip("|").split("|")]
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for row_line in data_lines[1:]:
        html += '<tr>'
        cells = [c.strip() for c in row_line.strip("|").split("|")]
        for c in cells:
            html += f'<td>{c}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def _inline_md(text: str) -> str:
    """内联 markdown 转 HTML：**粗体**，`代码`，保留普通文本"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def _parse_md_description(raw_desc: str) -> str:
    """将题目描述 markdown 转为 HTML，支持：列表、表格、引用、粗体、代码"""
    lines = raw_desc.split("\n")
    html_parts = []
    in_list = False
    in_quote = False
    in_table = False
    table_lines = []

    def flush_list():
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    def flush_table():
        nonlocal in_table, table_lines
        if in_table and len(table_lines) >= 2:
            html_parts.append(_md_table_to_html("\n".join(table_lines)))
        table_lines = []
        in_table = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_list()
            flush_table()
            in_quote = False
            continue

        # 表格
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                flush_list()
                in_quote = False
                in_table = True
            table_lines.append(line)
            continue
        else:
            flush_table()

        # 引用
        if stripped.startswith(">"):
            flush_list()
            in_quote = True
            content = stripped.lstrip("> ").strip()
            html_parts.append(f'<p class="note">{_inline_md(escape_html(content))}</p>')
            continue
        elif in_quote and not stripped.startswith(">"):
            in_quote = False

        # 列表项
        if stripped.startswith(("- ", "* ")):
            if not in_list:
                flush_table()
                in_list = True
                html_parts.append('<ul>')
            content = stripped[2:].strip()
            html_parts.append(f'<li>{_inline_md(escape_html(content))}</li>')
            continue
        else:
            flush_list()

        # 普通段落（处理内联粗体/代码）
        html_parts.append(f'<p>{_inline_md(escape_html(stripped))}</p>')

    flush_list()
    flush_table()
    return "\n".join(html_parts)


def _wrap_code_blocks(text: str) -> str:
    """检测 markdown 代码块并包裹为 SQL 高亮区"""
    def repl(m):
        code = m.group(1).strip()
        return f'<pre class="sql-hl" data-sql="{escape_html(code)}"></pre>'
    text = re.sub(r'```(?:sql)?\n(.*?)```', repl, text, flags=re.DOTALL)
    return text


def _parse_domain_knowledge(text: str) -> str:
    """解析「领域知识」节 → 完整 HTML 折叠块（含外壳）"""
    dk_match = re.search(r"## 领域知识\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if not dk_match:
        return ""
    raw = dk_match.group(1).strip()
    # 提取引用说明行
    note_match = re.search(r"^> (.*)$", raw, re.MULTILINE)
    note = note_match.group(1) if note_match else ""
    # 提取 markdown 表格
    table_match = re.search(r"\|.*\|[\s\S]*", raw)
    if not table_match:
        return ""
    table_html = _md_table_to_html(table_match.group(0))
    html = '<div class="collapsible" id="domainKnowledgeBlock">\n'
    html += '  <button class="collapsible-toggle" onclick="toggleSection(this)">\n'
    html += '    <span>📖 领域知识</span><span class="arrow">▶</span>\n'
    html += '  </button>\n'
    html += '  <div class="collapsible-body domain-k-body">\n'
    if note:
        html += f'    <p class="dk-note">{escape_html(note)}</p>\n'
    html += table_html
    html += '  </div>\n'
    html += '</div>'
    return html


def parse_sql_md(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    title = md_path.stem

    # 题目描述（从「题目描述」节提取）
    desc_match = re.search(r"## 二、题目描述\n(.*?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    raw_desc = desc_match.group(1).strip() if desc_match else ""
    description_html = _parse_md_description(raw_desc)

    # 从 init SQL 提取表结构和数据
    num_match = re.match(r"SQL(\d+)", title)
    schema_html = ""
    sample_html = ""
    table_name = ""
    if num_match:
        num = int(num_match.group(1))
        init_dir = BASE_DIR / "db" / "init"
        for f in sorted(init_dir.glob("*.sql")):
            if f.stem.startswith(f"{num:02d}"):
                schema_html, sample_html, table_name = parse_init_sql_schema_and_data(f)
                break

    # Answer SQL — 优先读 answer 文件，否则用 MD 第四节
    answer_path = md_path.parent / f"{md_path.stem}-answer.sql"
    if answer_path.exists():
        answer_sql = answer_path.read_text(encoding="utf-8")
    else:
        ans_match = re.search(r"## 四、最终 SQL\s*\n```(?:sql)?\n(.*?)```", text, re.DOTALL)
        answer_sql = ans_match.group(1).strip() if ans_match else ""

    # 解题思路 hints — 解析并处理代码块
    hints_match = re.search(r"## 三、解题思路\n(.*?)(?=\n## [四五]|\Z)", text, re.DOTALL)
    hints_text = hints_match.group(1).strip() if hints_match else ""
    # 先处理代码块
    hints_text = _wrap_code_blocks(hints_text)
    hints_html = ""
    in_code = False
    for line in hints_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("<pre class="):
            hints_html += stripped + "\n"
            continue
        if stripped.startswith("**") and "**" in stripped[2:]:
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', stripped)
            hints_html += f'<div class="hint-step">{content}</div>'
        elif stripped.startswith(("1.", "2.", "3.", "4.")):
            hints_html += f'<p class="hint-item">{escape_html(stripped)}</p>'
        elif stripped and not stripped.startswith("```"):
            hints_html += f'<p style="font-size:0.82rem;margin:4px 0;color:#777;">{escape_html(stripped)}</p>'

    # 期望结果 — 第五节
    expected_match = re.search(r"## 五、执行结果示例\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    expected_html = ""
    if expected_match:
        expected_text = expected_match.group(1).strip()
        # 提取表格
        table_match = re.search(r'\|.*\|[\s\S]*?(?=\n\n|\Z)', expected_text)
        if table_match:
            expected_html += _md_table_to_html(table_match.group(0))
        # 提取总结文字
        after_table = re.sub(r'\|.*\|[\s\S]*?(?=\n\n|\Z)', '', expected_text, count=1).strip()
        if after_table:
            expected_html += '<div class="expected-note">'
            for line in after_table.split("\n"):
                s = line.strip()
                if s and not s.startswith("---"):
                    expected_html += f'<p>{escape_html(s)}</p>'
            expected_html += '</div>'

    # 易错点
    gotcha_match = re.search(r"## 六、常见坑点.+\n(.*?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    gotchas_text = gotcha_match.group(1).strip() if gotcha_match else ""
    gotchas_html = ""
    for line in gotchas_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("-"):
            gotchas_html += f"<li>{escape_html(stripped.lstrip('- '))}</li>"

    # 领域知识
    domain_knowledge_html = _parse_domain_knowledge(text)

    return {
        "title": title,
        "description": description_html,
        "domain_knowledge": domain_knowledge_html,
        "schema": schema_html,
        "sample_data": sample_html,
        "table_name": table_name,
        "hints": hints_html,
        "answer_sql": escape_html(answer_sql),
        "expected": expected_html,
        "gotchas": gotchas_html,
    }


# ═══════════════════════════════════════════════════════════
#  渲染
# ═══════════════════════════════════════════════════════════

def render_algo(problem_id: str, data: dict) -> None:
    template = load_template("algo")

    html = template.replace("{{TITLE}}", data["title"])
    html = html.replace("{{DESCRIPTION}}", data["description"])
    html = html.replace("{{EXAMPLES}}", data["examples"])
    html = html.replace("{{DIFFICULTY}}", data["difficulty"])
    html = html.replace("{{DIFFICULTY_CLASS}}", data["difficulty_class"])
    html = html.replace("{{ANSWER_PYTHON}}", data["python_full"])
    html = html.replace("{{ANSWER_JAVA}}", data["java_full"])
    html = html.replace("{{CODE_PYTHON}}", data["python_template"])
    html = html.replace("{{CODE_JAVA}}", data["java_template"])
    html = html.replace("{{KEYPOINTS}}", data["keypoints"])
    html = html.replace("{{GOTCHAS}}", data["gotchas"])
    html = html.replace("{{PROBLEM_ID}}", problem_id)

    out_path = OUTPUT_DIR / "algo" / f"{problem_id}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ algo/{problem_id}.html")


def render_sql(problem_id: str, data: dict) -> None:
    template = load_template("sql")

    html = template.replace("{{TITLE}}", data["title"])
    html = html.replace("{{DESCRIPTION}}", data["description"])
    html = html.replace("{{DOMAIN_KNOWLEDGE}}", data.get("domain_knowledge", ""))
    html = html.replace("{{TABLE_SCHEMA}}", data["schema"])
    html = html.replace("{{SAMPLE_DATA}}", data["sample_data"])
    html = html.replace("{{TABLE_NAME}}", data["table_name"])
    html = html.replace("{{HINTS}}", data["hints"])
    html = html.replace("{{ANSWER_SQL}}", data["answer_sql"])
    html = html.replace("{{EXPECTED}}", data.get("expected", ""))
    html = html.replace("{{GOTCHAS}}", data["gotchas"])
    html = html.replace("{{PROBLEM_ID}}", problem_id)

    out_path = OUTPUT_DIR / "sql" / f"{problem_id}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ sql/{problem_id}.html")


# ═══════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════

def main():
    args = sys.argv[1:]

    if args:
        pid = args[0]
        if pid.startswith("SQL"):
            md_path = PROBLEMS_DIR / "sql" / f"{pid}.md"
            if not md_path.exists():
                print(f"❌ 题目不存在: {pid}")
                sys.exit(1)
            data = parse_sql_md(md_path)
            render_sql(pid, data)
        else:
            md_path = PROBLEMS_DIR / "algo" / f"{pid}.md"
            if not md_path.exists():
                print(f"❌ 题目不存在: {pid}")
                sys.exit(1)
            data = parse_algo_md(md_path)
            render_algo(pid, data)
    else:
        print("🔨 渲染全部题目...\n")
        algo_dir = PROBLEMS_DIR / "algo"
        if algo_dir.exists():
            for md_file in sorted(algo_dir.glob("*.md")):
                pid = md_file.stem
                if pid == "index":
                    continue
                data = parse_algo_md(md_file)
                render_algo(pid, data)

        sql_dir = PROBLEMS_DIR / "sql"
        if sql_dir.exists():
            for md_file in sorted(sql_dir.glob("*.md")):
                pid = md_file.stem
                if pid == "index":
                    continue
                data = parse_sql_md(md_file)
                render_sql(pid, data)

        print("\n✨ 渲染完成")


if __name__ == "__main__":
    main()

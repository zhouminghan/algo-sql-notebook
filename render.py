#!/usr/bin/env python3
"""
render.py — JSON → HTML 渲染器

将 problems/ 下的题目 markdown 配合模板生成 output/ 下的 HTML 文件。

用法:
  python render.py              # 渲染全部题目
  python render.py 001-两数之和 # 渲染单题（算法）
  python render.py SQL01-连续登录天数  # 渲染单题（SQL）
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROBLEMS_DIR = BASE_DIR / "problems"
FRONTEND_DIR = BASE_DIR / "frontend"
OUTPUT_DIR = BASE_DIR / "output"

# ── Templates ──
def load_template(name: str) -> str:
    path = FRONTEND_DIR / name / "template.html"
    if not path.exists():
        print(f"⚠️  模板不存在: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")

# ── SQL: extra table schemas from init SQL ──
def extract_table_schemas(sql_file: Path) -> str:
    """从 init SQL 中提取 CREATE TABLE 语句用于展示"""
    content = sql_file.read_text(encoding="utf-8")
    creates = re.findall(r"CREATE TABLE.*?;", content, re.DOTALL | re.IGNORECASE)
    if not creates:
        return ""
    html = ""
    for c in creates:
        html += f'<pre style="white-space:pre-wrap;margin:8px 0;padding:10px;background:#1e1e2e;border-radius:6px;font-size:0.8rem;">{c.strip()}</pre>'
    return html

def extract_sample_data(sql_file: Path) -> str:
    """从 init SQL 中提取 INSERT 语句"""
    content = sql_file.read_text(encoding="utf-8")
    inserts = re.findall(r"INSERT INTO.*?;", content, re.DOTALL | re.IGNORECASE)
    if not inserts:
        return ""
    html = '<div class="sample-data"><h4>示例数据</h4>'
    for ins in inserts:
        html += f'<pre>{ins.strip()[:2000]}</pre>'  # Limit size
    html += '</div>'
    return html


# ── Parser: .md → dict ──
def parse_algo_md(md_path: Path) -> dict:
    """解析算法题 markdown -> {title, difficulty, description, python, java, keypoints, gotchas}"""
    text = md_path.read_text(encoding="utf-8")

    # Title from first heading
    title_match = re.search(r"^# .+? (.+)", text, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem.split("-", 1)[-1]

    # Difficulty
    diff_map = {"简单": ("easy", "🟢 简单"), "中等": ("medium", "🟡 中等"), "困难": ("hard", "🔴 困难")}
    diff_match = re.search(r"难度.*?([简单中等困难]+)", text)
    diff_class, diff_label = diff_map.get(diff_match.group(1), ("medium", "🟡 中等")) if diff_match else ("medium", "🟡 中等")

    # Description
    desc_match = re.search(r"## 📖 题目描述\n\n(.*?)(?:\n---|\n##)", text, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Python solution
    py_match = re.search(r"## 🐍 Python 解法.*?```python\n(.*?)```", text, re.DOTALL)
    python = py_match.group(1).strip() if py_match else ""

    # Java solution
    java_match = re.search(r"## ☕ Java 解法.*?```java\n(.*?)```", text, re.DOTALL)
    java = java_match.group(1).strip() if java_match else ""

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
        "python": escape_html(python),
        "java": escape_html(java),
        "keypoints": keypoints_html,
        "gotchas": gotchas_html,
    }

def parse_sql_md(md_path: Path) -> dict:
    """解析 SQL 题 markdown -> {title, description, schemas, sample_data, hints, answer, keypoints, gotchas}"""
    text = md_path.read_text(encoding="utf-8")

    # Title: from filename "SQL01-连续登录天数" -> "SQL01-连续登录天数"
    title = md_path.stem

    # Description (everything before "解题思路" or "最终SQL")
    desc_match = re.search(r"## 📖 (?:题目描述|场景描述)\n(.*?)(?:\n##|\n---)", text, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else text[:500]

    # Answer SQL
    answer_path = md_path.parent / f"{md_path.stem}-answer.sql"
    answer_sql = ""
    if answer_path.exists():
        answer_sql = answer_path.read_text(encoding="utf-8")

    # Hints: from "解题思路"
    hints_match = re.search(r"## 💡 解题思路\n(.*?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    hints_text = hints_match.group(1).strip() if hints_match else ""
    hints_html = ""
    step = 1
    for line in hints_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("### ", "#### ")):
            hints_html += f'<div class="hint-step"><span class="step-num">{step}</span>{stripped.lstrip("# ")}</div>'
            step += 1
        elif stripped and not stripped.startswith("```"):
            hints_html += f'<p style="font-size:0.85rem;margin:4px 0;color:#777;">{stripped}</p>'

    # Table schemas: try to find corresponding init file
    # e.g. SQL01 -> db/init/01-login.sql
    num_match = re.match(r"SQL(\d+)", title)
    schemas_html = ""
    sample_data_html = ""
    if num_match:
        num = int(num_match.group(1))
        init_dir = BASE_DIR / "db" / "init"
        for f in sorted(init_dir.glob("*.sql")):
            if f.stem.startswith(f"{num:02d}"):
                schemas_html = '<div class="table-info"><h4>表结构</h4>' + extract_table_schemas(f) + '</div>'
                sample_data_html = extract_sample_data(f)
                break

    # Keypoints
    kp_match = re.search(r"## 🧠 关键(?:点|要点)\n(.*?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    keypoints_text = kp_match.group(1).strip() if kp_match else ""
    keypoints_html = ""
    for line in keypoints_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "1. ", "2. ", "3. ")):
            keypoints_html += f"<li>{stripped.lstrip('- 1234567890. ')}</li>"

    # Gotchas
    gotcha_match = re.search(r"## (?:⚠️ )?易错点\n(.*?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    gotchas_text = gotcha_match.group(1).strip() if gotcha_match else ""
    gotchas_html = ""
    for line in gotchas_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "1. ", "2. ", "3. ")):
            gotchas_html += f"<li>{stripped.lstrip('- 1234567890. ')}</li>"

    return {
        "title": title,
        "description": description,
        "schemas": schemas_html,
        "sample_data": sample_data_html,
        "hints": hints_html,
        "answer_sql": escape_html(answer_sql),
        "keypoints": keypoints_html,
        "gotchas": gotchas_html,
    }


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── Render ──
def render_algo(problem_id: str, data: dict) -> None:
    """渲染单道算法题 -> output/algo/{problem_id}.html"""
    template = load_template("algo")

    # VIZ_STEPS: extract from description lines starting with "输入"/"输出"
    viz_steps = ""
    desc_lines = data["description"].split("\n")
    in_output = False
    for line in desc_lines:
        stripped = line.strip()
        if stripped.startswith("输入"):
            in_output = False
            viz_steps += f'<div class="viz-step"><div class="step-label">输入</div><pre>{escape_html(stripped)}</pre></div>\n'
        elif stripped.startswith("输出"):
            in_output = True
            viz_steps += f'<div class="viz-step"><div class="step-label">期望输出</div><pre>{escape_html(stripped)}</pre></div>\n'
        elif in_output and stripped.startswith("解释"):
            viz_steps += f'<div class="viz-step"><div class="step-label">解释</div><pre>{escape_html(stripped)}</pre></div>\n'
            in_output = False

    html = template.replace("{{TITLE}}", data["title"])
    html = html.replace("{{DESCRIPTION}}", escape_html(data["description"]))
    html = html.replace("{{VIZ_STEPS}}", viz_steps)
    html = html.replace("{{DIFFICULTY}}", data["difficulty"])
    html = html.replace("{{DIFFICULTY_CLASS}}", data["difficulty_class"])
    html = html.replace("{{ANSWER_PYTHON}}", f"<pre>{data['python']}</pre>")
    html = html.replace("{{ANSWER_JAVA}}", f"<pre>{data['java']}</pre>")
    html = html.replace("{{KEYPOINTS}}", data["keypoints"])
    html = html.replace("{{GOTCHAS}}", data["gotchas"])
    html = html.replace("{{PROBLEM_ID}}", problem_id)

    out_path = OUTPUT_DIR / "algo" / f"{problem_id}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ algo/{problem_id}.html")

def render_sql(problem_id: str, data: dict) -> None:
    """渲染单道 SQL 题 -> output/sql/{problem_id}.html"""
    template = load_template("sql")

    html = template.replace("{{TITLE}}", data["title"])
    html = html.replace("{{DESCRIPTION}}", escape_html(data["description"]))
    html = html.replace("{{TABLE_SCHEMAS}}", data["schemas"])
    html = html.replace("{{SAMPLE_DATA}}", data["sample_data"])
    html = html.replace("{{HINTS}}", data["hints"])
    html = html.replace("{{ANSWER_SQL}}", data["answer_sql"])
    html = html.replace("{{KEYPOINTS}}", data["keypoints"])
    html = html.replace("{{GOTCHAS}}", data["gotchas"])
    html = html.replace("{{PROBLEM_ID}}", problem_id)

    out_path = OUTPUT_DIR / "sql" / f"{problem_id}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ sql/{problem_id}.html")


# ── Main ──
def main():
    args = sys.argv[1:]

    if args:
        # Render single problem
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
        # Render all
        print("🔨 渲染全部题目...\n")

        algo_dir = PROBLEMS_DIR / "algo"
        if algo_dir.exists():
            for md_file in sorted(algo_dir.glob("*.md")):
                pid = md_file.stem
                if pid == "index":
                    continue  # skip category index
                data = parse_algo_md(md_file)
                render_algo(pid, data)

        sql_dir = PROBLEMS_DIR / "sql"
        if sql_dir.exists():
            for md_file in sorted(sql_dir.glob("*.md")):
                pid = md_file.stem
                if pid == "index":
                    continue  # skip category index
                data = parse_sql_md(md_file)
                render_sql(pid, data)

        print("\n✨ 渲染完成")

if __name__ == "__main__":
    main()

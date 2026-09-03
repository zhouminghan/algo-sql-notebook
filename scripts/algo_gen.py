#!/usr/bin/env python3
"""算法题页面生成器。

从 scripts/specs/*.py 读取题目规格，输出到 algo/NNN-标题.html。
规格字段见 algo_spec 示例。运行：python3 scripts/algo_gen.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALGO_DIR = ROOT / "algo"
PROBLEMS_JS = ROOT / "assets" / "js" / "problems.js"


def esc_text(s: str) -> str:
    """转义普通文本（用于 pre/code 内容）。"""
    return html.escape(s, quote=False)


def frame(label: str, fn: str, **args):
    """一个图解帧：label 为帧标签，fn 为 draw-utils 函数名。"""
    return {"label": label, "fn": fn, "args": args}


HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="asn-file" content="@@FILE@@">
<title>@@NUM@@. @@TITLE@@ — algo-sql-notebook</title>
<script>
(function () {
  var s = localStorage.getItem('asn-theme');
  var d = s || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', d);
})();
</script>
<link rel="stylesheet" href="../assets/vendor/pico.min.css">
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="stylesheet" href="../assets/vendor/github.min.css">
<script src="../assets/js/problems.js"></script>
<script src="../assets/js/common.js"></script>
<script src="../assets/js/draw-utils.js"></script>
<script src="../assets/vendor/highlight.min.js"></script>
</head>
<body>

"""


def _frame_html(idx: int, f: dict) -> str:
    return (
        f'<div class="frame-card" style="margin-bottom:1.25rem;">\n'
        f'  <div class="frame-label">{esc_text(f["label"])}</div>\n'
        f'  <div id="frame{idx}-svg"></div>\n'
        f'</div>\n'
    )


def _frame_js(idx: int, f: dict) -> str:
    args = dict(f["args"])
    marker = f"__WIDTH_{idx}__"
    args["width"] = marker
    s = json.dumps(args, ensure_ascii=False)
    s = s.replace(f'"{marker}"', f"U.frameCardWidth('frame{idx}-svg')")
    return f"document.getElementById('frame{idx}-svg').innerHTML = U.{f['fn']}({s});"


def render(prob: dict) -> str:
    """prob 字段：id,title,diff,tags,leetcode,origin,why,desc,frames,conclusion,
    py,java,time,space,pitfalls,selfcheck"""
    file = prob["file"]
    num = f"{prob['id']:03d}"
    head = HEAD.replace("@@FILE@@", file).replace("@@NUM@@", num).replace("@@TITLE@@", prob["title"])
    parts = [head]

    parts.append(
        f'<a class="origin-link" href="{prob["origin"]}" target="_blank">→ LeetCode 原题</a>\n\n'
    )

    parts.append('<div class="why-box">\n')
    parts.append(f'  <strong>🤔 为什么用这个思路？</strong><br>\n  {prob["why"]}\n')
    parts.append('</div>\n\n')

    parts.append('<h3>📄 题目描述</h3>\n')
    parts.append(prob["desc"].strip() + '\n\n')

    parts.append('<h3>📐 图解即思路</h3>\n')
    if prob.get("concept"):
        parts.append('<div class="why-box">\n  ' + prob["concept"].strip() + '\n</div>\n')
    for i, f in enumerate(prob["frames"], start=1):
        parts.append(_frame_html(i, f))
    if prob.get("conclusion"):
        parts.append('<div class="why-box">\n  <strong>✅ 结论</strong><br>\n  ' + prob["conclusion"].strip() + '\n</div>\n')
    parts.append('\n')

    parts.append('<h3>📝 最优解代码</h3>\n\n')
    parts.append('<h4 style="margin-bottom:0.25rem;">Python</h4>\n')
    parts.append('<div class="code-block-wrapper">\n')
    parts.append('  <button class="copy-btn" onclick="copyCode(this, \'py-code\')">📋 复制</button>\n')
    parts.append(f'  <pre><code class="language-python" id="py-code">{esc_text(prob["py"].strip())}</code></pre>\n')
    parts.append('</div>\n\n')
    parts.append('<h4 style="margin-bottom:0.25rem;">Java</h4>\n')
    parts.append('<div class="code-block-wrapper">\n')
    parts.append('  <button class="copy-btn" onclick="copyCode(this, \'java-code\')">📋 复制</button>\n')
    parts.append(f'  <pre><code class="language-java" id="java-code">{esc_text(prob["java"].strip())}</code></pre>\n')
    parts.append('</div>\n\n')

    parts.append('<h3>⏱ 复杂度分析</h3>\n<ul>\n')
    parts.append(f'  <li><strong>时间</strong>：{prob["time"]}</li>\n')
    parts.append(f'  <li><strong>空间</strong>：{prob["space"]}</li>\n')
    parts.append('</ul>\n\n')

    parts.append('<h3>⚠️ 易错点</h3>\n<ul>\n')
    for bold, text in prob["pitfalls"]:
        parts.append(f'  <li><strong>{bold}</strong>：{text}</li>\n')
    parts.append('</ul>\n\n')

    parts.append('<details class="selfcheck-box" open>\n')
    parts.append('  <summary><strong>🧪 自我检验</strong></summary>\n')
    parts.append('  <div style="margin-top:0.5rem;">\n')
    for q, a in prob["selfcheck"]:
        parts.append(f'    <p><strong>Q:</strong> {q}</p>\n')
        parts.append(f'    <p style="color:var(--color-done);margin-left:1rem;">✅ <strong>答：</strong> {a}</p>\n')
    parts.append('  </div>\n</details>\n\n')

    parts.append('<script>\nconst U = window.DrawUtils;\n\nfunction renderFrames() {\n')
    for i, f in enumerate(prob["frames"], start=1):
        parts.append(_frame_js(i, f) + '\n')
    parts.append('}\n\nrenderFrames();\nU.autoFitResize(renderFrames);\nhljs.highlightAll();\n</script>\n')

    parts.append('</body>\n</html>\n')
    return ''.join(parts)


def generate(problems):
    for p in problems:
        p["file"] = f"algo/{p['id']:03d}-{p['title']}.html"
        out = ALGO_DIR / p["file"].split("/")[-1]
        out.write_text(render(p), encoding="utf-8")
        print("written", p["file"])


def sync_problems(problems):
    """把新生成的 file / leetcode 回写到 problems.js（保留 sql 部分）。"""
    text = PROBLEMS_JS.read_text(encoding="utf-8")
    data = json.loads(text[text.index("{"): text.rindex("}") + 1])
    by_id = {p["id"]: p for p in problems}
    for it in data["algo"]:
        spec = by_id.get(it["id"])
        if spec:
            it["file"] = f"algo/{spec['id']:03d}-{spec['title']}.html"
            if spec.get("leetcode"):
                it["leetcode"] = spec["leetcode"]
    PROBLEMS_JS.write_text(
        "// 题目唯一数据源（index 列表、README、页面导航均从此读取）\n"
        "// 修改题目：只改这里；新增页面文件后在此登记 file 即可自动上架\n"
        "window.PROBLEMS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    print("synced problems.js")


if __name__ == "__main__":
    from scripts.specs import ALL  # noqa
    generate(ALL)
    sync_problems(ALL)

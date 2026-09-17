#!/usr/bin/env python3
"""算法题页面生成器。

从 scripts/specs/algo/*.py 读取题目规格，输出到 algo/NNN-标题.html，
并把 file / leetcode 字段回写到 assets/js/problems.js。

页面本身只写「正文」：题头、左侧导航、右侧目录、上一题/下一题
都由 assets/js/common.js 在运行时注入（见 AGENTS.md「页面外壳」一节）。

运行：
    python3 scripts/algo_gen.py            # 全量生成 100 题
    python3 scripts/algo_gen.py --id 1     # 只重新生成 001
"""
import html
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALGO_DIR = ROOT / "algo"
PROBLEMS_JS = ROOT / "assets" / "js" / "problems.js"
SPECS_DIR = ROOT / "scripts" / "specs" / "algo"

# highlight.min.js 用 defer 加载（121KB，不该阻塞首屏），
# 所以页面里要等它执行完再调用高亮。
HL_BOOT = (
    "function highlightCode() { if (window.hljs) window.hljs.highlightAll(); }\n"
    "if (document.readyState === 'complete') highlightCode();\n"
    "else window.addEventListener('load', highlightCode);"
)


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
<meta name="description" content="@@NUM@@. @@TITLE@@ — 图解思路 + Python/Java 最优解 + 复杂度分析 + 易错点 + 自我检验。">
<title>@@NUM@@. @@TITLE@@ — algo-sql-notebook</title>
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:title" content="@@NUM@@. @@TITLE@@">
<meta property="og:description" content="图解思路 + Python/Java 最优解 + 复杂度分析 + 易错点 + 自我检验。">
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


def _frame_html(idx: int, f: dict) -> str:
    return (
        f'<div class="frame-card">\n'
        f'  <div class="frame-label">{esc_text(f["label"])}</div>\n'
        f'  <div class="frame-canvas" id="frame{idx}-svg"></div>\n'
        f'</div>\n'
    )


# 只让「表格类」图解撑满卡片宽度；栈/链表/双指针等窄图保持自然宽度
FILL_FNS = {
    "drawTable", "drawDPTable", "drawWindowFunc", "diffTable",
    "drawGroupBy", "drawJoin", "drawSubquery", "drawCTE", "drawSetOp",
    "drawPivot", "drawStringFunc", "drawDateFunc", "drawConditionFunc",
}
# 这类函数会按内容自动贴合宽度，传 0 让它们自适应（去掉右侧大片空白）
AUTO_FIT_FNS = {"drawTwoPointers", "drawBinarySearch"}


def _frame_js(idx: int, f: dict) -> str:
    args = dict(f["args"])
    if f["fn"] in FILL_FNS:
        marker = f"__WIDTH_{idx}__"
        args["width"] = marker
        s = json.dumps(args, ensure_ascii=False)
        s = s.replace(f'"{marker}"', f"U.frameCardWidth('frame{idx}-svg')")
    elif f["fn"] in AUTO_FIT_FNS:
        args["width"] = 0
        s = json.dumps(args, ensure_ascii=False)
    else:
        s = json.dumps(args, ensure_ascii=False)
    return f"document.getElementById('frame{idx}-svg').innerHTML = U.{f['fn']}({s});"


def render(prob: dict) -> str:
    """prob 字段：id,title,diff,tags,leetcode,origin,why,desc,frames,conclusion,
    py,java,time,space,pitfalls,selfcheck"""
    file = prob["file"]
    num = f"{prob['id']:03d}"
    head = HEAD.replace("@@FILE@@", file).replace("@@NUM@@", num).replace("@@TITLE@@", prob["title"])
    parts = [head]

    parts.append('<div class="why-box">\n')
    parts.append(f'  <strong>为什么用这个思路？</strong><br>\n  {prob["why"]}\n')
    parts.append('</div>\n\n')

    parts.append('<h2>题目描述</h2>\n')
    parts.append(prob["desc"].strip() + '\n\n')

    parts.append('<h2>图解即思路</h2>\n')
    if prob.get("concept"):
        parts.append('<div class="why-box">\n  ' + prob["concept"].strip() + '\n</div>\n')
    for i, f in enumerate(prob["frames"], start=1):
        parts.append(_frame_html(i, f))
    if prob.get("conclusion"):
        parts.append('<div class="why-box">\n  <strong>结论</strong><br>\n  ' + prob["conclusion"].strip() + '\n</div>\n')
    parts.append('\n')

    parts.append('<h2>最优解代码</h2>\n\n')
    parts.append('<h4>Python</h4>\n')
    parts.append('<div class="code-block-wrapper">\n')
    parts.append('  <button type="button" class="copy-btn" onclick="copyCode(this, \'py-code\')">复制</button>\n')
    parts.append(f'  <pre><code class="language-python" id="py-code">{esc_text(prob["py"].strip())}</code></pre>\n')
    parts.append('</div>\n\n')
    parts.append('<h4>Java</h4>\n')
    parts.append('<div class="code-block-wrapper">\n')
    parts.append('  <button type="button" class="copy-btn" onclick="copyCode(this, \'java-code\')">复制</button>\n')
    parts.append(f'  <pre><code class="language-java" id="java-code">{esc_text(prob["java"].strip())}</code></pre>\n')
    parts.append('</div>\n\n')

    parts.append('<h2>复杂度分析</h2>\n<ul>\n')
    parts.append(f'  <li><strong>时间</strong>：{prob["time"]}</li>\n')
    parts.append(f'  <li><strong>空间</strong>：{prob["space"]}</li>\n')
    parts.append('</ul>\n\n')

    parts.append('<h2>易错点</h2>\n<ul>\n')
    for bold, text in prob["pitfalls"]:
        parts.append(f'  <li><strong>{bold}</strong>：{text}</li>\n')
    parts.append('</ul>\n\n')

    parts.append('<details class="selfcheck-box" open>\n')
    parts.append('  <summary>自我检验</summary>\n')
    parts.append('  <div class="selfcheck-body">\n')
    for q, a in prob["selfcheck"]:
        parts.append(f'    <p><strong>Q:</strong> {q}</p>\n')
        parts.append(f'    <p class="selfcheck-answer"><strong>答：</strong> {a}</p>\n')
    parts.append('  </div>\n</details>\n\n')

    parts.append('<script>\nconst U = window.DrawUtils;\n\nfunction renderFrames() {\n')
    for i, f in enumerate(prob["frames"], start=1):
        parts.append(_frame_js(i, f) + '\n')
    parts.append('}\n\nrenderFrames();\nU.autoFitResize(renderFrames);\n' + HL_BOOT + '\n</script>\n')

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


def load_spec(path: pathlib.Path) -> dict:
    """加载单个 spec 文件（每文件一个 PROBLEM）。"""
    name = "spec_" + path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod.PROBLEM


def load_problems(only_id: int = None):
    """扫描 specs/algo/*.py，返回题目列表（可按 id 只取一个）。"""
    problems = []
    for f in sorted(SPECS_DIR.glob("*.py")):
        if f.name == "__init__.py":
            continue
        p = load_spec(f)
        if only_id is not None and p["id"] != only_id:
            continue
        problems.append(p)
    return problems


if __name__ == "__main__":
    only_id = None
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--id" and i + 1 < len(args):
            only_id = int(args[i + 1])
    problems = load_problems(only_id)
    if not problems:
        print("未找到题目", f"(id={only_id})" if only_id else "")
        sys.exit(1)
    generate(problems)
    sync_problems(problems)

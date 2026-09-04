from scripts.algo_gen import frame

PROBLEM = {
    "id": 13,
    "title": "括号生成",
    "diff": "medium",
    "tags": ["回溯"],
    "leetcode": 22,
    "origin": "https://leetcode.cn/problems/generate-parentheses/",
    "why": "生成所有合法括号组合，本质是一棵决策树：每一步要么放 '(' 要么放 ')'。两条剪枝规则保证结果合法——左括号数量不超过 n，右括号数量不超过当前左括号数（否则会「先右后左」不匹配）。",
    "desc": """<p>数字 <code>n</code> 代表生成括号的对数，设计一个函数，返回所有可能的并且<strong>有效的</strong>括号组合。</p>
<p><strong>示例：</strong><br><code>n = 3</code> → <code>["((()))","(()())","(())()","()(())","()()()"]</code></p>""",
    "frames": [
    frame("① 决策树：每步放 '(' 或 ')'，剪掉非法分支", "drawBacktrack", nodes=[{"val": "", "x": 300, "y": 20, "color": "normal"}, {"val": "(", "x": 160, "y": 80, "color": "path"}, {"val": "((", "x": 60, "y": 150, "color": "path"}, {"val": "(((", "x": 30, "y": 220, "color": "path"}, {"val": "((()", "x": 140, "y": 290, "color": "path"}, {"val": "()", "x": 480, "y": 150, "color": "path"}, {"val": "())", "x": 540, "y": 220, "color": "pruned"}], edges=[{"x1": 300, "y1": 20, "x2": 160, "y2": 80, "color": "path"}, {"x1": 300, "y1": 20, "x2": 480, "y2": 150, "color": "path"}, {"x1": 160, "y1": 80, "x2": 60, "y2": 150, "color": "path"}, {"x1": 60, "y1": 150, "x2": 30, "y2": 220, "color": "path"}, {"x1": 30, "y1": 220, "x2": 140, "y2": 290, "color": "path"}, {"x1": 480, "y1": 150, "x2": 540, "y2": 220, "color": "pruned"}], width=620, height=320),
    frame("② n=1：先 '(' 再 ')'，得 ()", "drawBacktrack", nodes=[{"val": "", "x": 300, "y": 20, "color": "normal"}, {"val": "(", "x": 220, "y": 90, "color": "path"}, {"val": "()", "x": 220, "y": 170, "color": "path"}], edges=[{"x1": 300, "y1": 20, "x2": 220, "y2": 90, "color": "path"}, {"x1": 220, "y1": 90, "x2": 220, "y2": 170, "color": "path"}], width=620, height=220),
    ],
    "conclusion": "「左括号数 ≤ n」与「右括号数 ≤ 左括号数」两条约束贯穿整棵树，走到 2n 长度就收集一个答案。",
    "py": """def generateParenthesis(n):
    ans = []
    def dfs(s, left, right):
        if len(s) == 2 * n:
            ans.append(s); return
        if left < n:                       # 还能放左括号
            dfs(s + '(', left + 1, right)
        if right < left:                   # 右括号不能超过左括号
            dfs(s + ')', left, right + 1)
    dfs('', 0, 0)
    return ans""",
    "java": """public List<String> generateParenthesis(int n) {
    List<String> ans = new ArrayList<>();
    dfs(new StringBuilder(), 0, 0, n, ans);
    return ans;
}
void dfs(StringBuilder sb, int left, int right, int n, List<String> ans) {
    if (sb.length() == 2 * n) { ans.add(sb.toString()); return; }
    if (left < n) { sb.append('('); dfs(sb, left + 1, right, n, ans); sb.deleteCharAt(sb.length() - 1); }
    if (right < left) { sb.append(')'); dfs(sb, left, right + 1, n, ans); sb.deleteCharAt(sb.length() - 1); }
}""",
    "time": "O(C(2n,n)/(n+1) · n) — 卡特兰数个答案，每个答案长 2n",
    "space": "O(n) — 递归栈深度 2n",
    "pitfalls": [["剪枝条件写反", "右括号条件是 right < left 而非 right < n，否则会生成 \")(\" 这种非法开头"], ["回溯要恢复现场", "用可变字符串（StringBuilder）时，递归返回后要 deleteCharAt 撤销本次选择"]],
    "selfcheck": [["为什么第二个条件不是 right < n 而是 right < left？", "right < n 只限制总量，无法阻止右括号出现在左括号之前（如 ')(('）；right < left 保证任意前缀里右括号都不多于左括号，这正是合法的充要条件。"], ["n=1 会生成什么？", "先放 '('，此时 right(0) < left(1) 可放 ')'，得 '()'；没有其他分支，结果唯一。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 93,
    "title": "删除无效的括号",
    "diff": "hard",
    "tags": ["BFS"],
    "leetcode": 301,
    "origin": "https://leetcode.cn/problems/remove-invalid-parentheses/",
    "why": "要删「最少」的括号，按层 BFS：每次尝试删一个括号得到下一层，一旦某层出现合法串，该层就是最小删除层，收集该层所有合法串即可。",
    "desc": """<p>给定只含 <code>(</code> 和 <code>)</code> 以及小写字母的字符串，删除<strong>最少数量的</strong>无效括号，使剩余字符串合法。返回所有可能的结果。</p>
<p><strong>示例：</strong><br><code>"()())()"</code> → <code>["(())()","()()()"]</code>；<code>"(a)())()"</code> → <code>["(a())()","(a)()()"]</code></p>""",
    "frames": [
    frame("① 按层 BFS：每删一个括号一层", "drawBacktrack", nodes=[{"val": "()())()", "x": 300, "y": 15, "color": "normal"}, {"val": "删1个(4个候选)", "x": 160, "y": 95, "color": "path"}, {"val": "(())() ✓", "x": 90, "y": 175, "color": "path"}, {"val": "()()() ✓", "x": 230, "y": 175, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 160, "y2": 95, "color": "path"}, {"x1": 160, "y1": 95, "x2": 90, "y2": 175, "color": "path"}, {"x1": 160, "y1": 95, "x2": 230, "y2": 175, "color": "path"}], width=560, height=220),
    frame("② 用计数判断合法：左加右减，中途不为负、最后为 0", "drawTable", headers=["串", "计数", "合法?"], rows=[["(())()", "0", "✓"], ["()()()", "0", "✓"], ["())(()", "中途负", "✗"]], width=460, height=160),
    ],
    "conclusion": "BFS 保证先找到的就是删除最少的，用 visited 去重避免重复状态。",
    "py": """def removeInvalidParentheses(s):
    def valid(t):
        cnt = 0
        for ch in t:
            if ch == '(': cnt += 1
            elif ch == ')':
                cnt -= 1
                if cnt < 0: return False
        return cnt == 0
    level = {s}
    while True:
        ans = [t for t in level if valid(t)]
        if ans:
            return ans
        nxt = set()
        for t in level:
            for i in range(len(t)):
                if t[i] not in '()': continue
                nxt.add(t[:i] + t[i + 1:])
        level = nxt""",
    "java": """public List<String> removeInvalidParentheses(String s) {
    List<String> ans = new ArrayList<>();
    Set<String> level = new HashSet<>();
    level.add(s);
    while (true) {
        for (String t : level) if (valid(t)) ans.add(t);
        if (!ans.isEmpty()) return ans;
        Set<String> nxt = new HashSet<>();
        for (String t : level)
            for (int i = 0; i < t.length(); i++)
                if (t.charAt(i) == '(' || t.charAt(i) == ')')
                    nxt.add(t.substring(0, i) + t.substring(i + 1));
        level = nxt;
    }
}
boolean valid(String t) {
    int cnt = 0;
    for (char c : t.toCharArray()) {
        if (c == '(') cnt++;
        else if (c == ')' && --cnt < 0) return false;
    }
    return cnt == 0;
}""",
    "time": "最坏 O(n · 2^n)，但剪枝与去重后通常很快",
    "space": "O(n · 层状态数)",
    "pitfalls": [["BFS 而非 DFS", "DFS 会先搜到删除更多的解，BFS 保证「最少删除」"], ["visited 去重", "不同删法可能得到同一串，必须用 set 去重"]],
    "selfcheck": [["合法判断", "遍历中计数不能为负，结束时计数必须为 0，二者缺一不可。"], ["含字母怎么办？", "字母原样保留，只对括号做删除候选。"]],
}

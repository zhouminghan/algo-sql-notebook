from scripts.algo_gen import frame

PROBLEM = {
    "id": 18,
    "title": "最长有效括号",
    "diff": "hard",
    "tags": ["DP", "栈"],
    "leetcode": 32,
    "origin": "https://leetcode.cn/problems/longest-valid-parentheses/",
    "why": "求「连续」有效括号的最长长度，关键是要能算出每个右括号能向左延伸到哪。栈里存<strong>下标</strong>而不是括号本身：遇到匹配就弹出，栈顶下标就是当前段的前一个位置，长度 = i - 栈顶。",
    "desc": """<p>给定只包含 <code>(</code> 和 <code>)</code> 的字符串，找出最长有效（格式正确且连续）括号子串的长度。</p>
<p><strong>示例：</strong><br><code>s = "(()"</code> → <code>2</code>（最长是 <code>"()"</code>）<br><code>s = ")()())"</code> → <code>4</code>（最长是 <code>"()()"</code>）</p>""",
    "frames": [
    frame("① 栈底先放 -1 作为「段起点」哨兵", "drawStack", items=[{"val": "-1", "label": "栈底"}], type="stack", height=120),
    frame("② 遇 '(' 存下标 0、1", "drawStack", items=[{"val": "-1"}, {"val": "0"}, {"val": "1"}], type="stack", height=150),
    frame("③ 遇 ')' 弹栈匹配，长度 = 当前下标 - 栈顶", "drawTable", headers=["位置", "0", "1", "2", "3", "4", "5"], rows=[["字符", "(", "(", ")", ")", "(", ")"], ["最长", "", "", "2", "2", "", "4"]], width=560, height=140),
    ],
    "conclusion": "栈底永远是「当前有效段起点前一位」，每次成功匹配后用 i - 栈顶下标 更新答案，天然覆盖连续多段。",
    "py": """def longestValidParentheses(s):
    stack = [-1]               # 哨兵：段起点前一位
    ans = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:      # 段断了，重置起点
                stack.append(i)
            else:
                ans = max(ans, i - stack[-1])
    return ans""",
    "java": """public int longestValidParentheses(String s) {
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(-1);
    int ans = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == '(') stack.push(i);
        else {
            stack.pop();
            if (stack.isEmpty()) stack.push(i);
            else ans = Math.max(ans, i - stack.peek());
        }
    }
    return ans;
}""",
    "time": "O(n) — 每个字符入栈出栈一次",
    "space": "O(n) — 栈存下标",
    "pitfalls": [["栈存下标而非字符", "只有下标能算出长度；存字符只能判断合法性、算不出连续长度"], ["弹空后要 push 当前 i", "出现多余右括号时有效段被截断，把当前 i 当新起点，避免把两段错误接起来"]],
    "selfcheck": [["s = \"(()\" 的过程是怎样的？", "栈 [-1]；'(' 入 0、1 → [-1,0,1]；')' 弹 1，长度 2-0=2。最后 ans=2。"], ["为什么不直接数配对总数？", "题目要求「连续」，如 \")(\" 配对数为 0 但字符间不连续，栈下标法能正确处理段与段之间的断开。"]],
}

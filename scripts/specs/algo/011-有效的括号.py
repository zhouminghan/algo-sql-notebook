from scripts.algo_gen import frame

PROBLEM = {
    "id": 11,
    "title": "有效的括号",
    "diff": "easy",
    "tags": ["栈"],
    "leetcode": 20,
    "origin": "https://leetcode.cn/problems/valid-parentheses/",
    "why": "括号配对是典型的「后进先出」：最近出现的左括号，必须最先被对应的右括号闭合。用栈天然匹配——遇到左括号入栈，遇到右括号就弹出栈顶对比，顺序错了立刻失败。",
    "desc": """<p>给定一个只包括 <code>(</code>，<code>)</code>，<code>{</code>，<code>}</code>，<code>[</code>，<code>]</code> 的字符串 <code>s</code>，判断字符串是否有效。</p>
<p>有效需满足：左括号必须用<strong>相同类型</strong>的右括号闭合；左括号必须以<strong>正确的顺序</strong>闭合。</p>
<p><strong>示例：</strong><br><code>s = "()[]{}"</code> → <code>true</code><br><code>s = "(]"</code> → <code>false</code></p>""",
    "frames": [
    frame("① 遇 '(' 入栈", "drawStack", items=[{"val": "("}], type="stack", height=140),
    frame("② 遇 '[' 入栈（栈顶为 '['）", "drawStack", items=[{"val": "("}, {"val": "["}], type="stack", height=140),
    frame("③ 遇 ']'，与栈顶 '[' 匹配 → 出栈", "drawStack", items=[{"val": "("}], type="stack", height=140),
    frame("④ 遇 ')'，与栈顶 '(' 匹配 → 出栈，栈空 → 有效", "drawStack", items=[], type="stack", height=120),
    ],
    "conclusion": "一路匹配成功且最终栈为空，说明每个右括号都恰好闭合了最近的那个左括号。",
    "py": """def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs:          # 右括号：必须匹配栈顶
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:                    # 左括号：入栈
            stack.append(ch)
    return not stack            # 最后栈必须为空""",
    "java": """public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{'))
                return false;
        }
    }
    return stack.isEmpty();
}""",
    "time": "O(n) — 每个字符入栈/出栈一次",
    "space": "O(n) — 最坏情况全是左括号",
    "pitfalls": [["右括号要先判断栈空", "否则对 s = \"]\" 直接 pop 会越界（Java 抛异常）"], ["最后必须栈空", "忘写 return not stack 会把 \"(()\" 误判为有效"], ["不能只数个数", "像 \"([)]\" 左右括号个数都平衡，但顺序错，必须用栈保证顺序"]],
    "selfcheck": [["字符串 \"([)]\" 是否有效？", "无效。遇到 ')' 时栈顶是 '['，类型不匹配。它数量平衡但顺序错——这正是栈和计数器的区别。"], ["只用三种括号时，能否用三个计数器代替栈？", "不能。计数器无法感知「最近未闭合」的顺序，无法识别 \"([)]\" 这类错序；栈的 LIFO 特性恰好对应括号的嵌套结构。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 99,
    "title": "字符串解码",
    "diff": "medium",
    "tags": ["栈"],
    "leetcode": 394,
    "origin": "https://leetcode.cn/problems/decode-string/",
    "why": "嵌套结构（如 3[a2[c]]）适合栈。遇到数字、字符就累积，遇到 '[' 把当前倍数和已累积串入栈，遇到 ']' 弹出倍数与前置串拼接。",
    "desc": """<p>给定编码字符串，返回解码后的字符串。规则：<code>k[encoded_string]</code> 表示方括号内字符串重复 k 次。可以嵌套。</p>
<p><strong>示例：</strong><br><code>"3[a]2[bc]"</code> → <code>"aaabcbc"</code>；<code>"3[a2[c]]"</code> → <code>"accaccacc"</code></p>""",
    "frames": [
    frame("① 遇 '[' 把倍数与已累积串压栈", "drawStack", items=[{"val": "3"}, {"val": ""}], type="stack", height=140),
    frame("② 遇 ']' 弹出，拼接 repeat", "drawTable", headers=["步骤", "栈", "结果"], rows=[["读 3[a2[c", "3,'' ; 2,'a'", ""], ["读 ]", "3,''", "a+2c=acc"], ["读 ]", "", "acc×3"]], width=500, height=170),
    frame("③ 结果 accaccacc", "drawTable", headers=["", "结果"], rows=[["解码", {"val": "accaccacc", "highlight": True}]], width=460, height=110),
    ],
    "conclusion": "栈保存「进入括号前的上下文」，遇到右括号就把括号内容按倍数展开拼回去。",
    "py": """def decodeString(s):
    stack = []
    cur = ''
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == '[':
            stack.append((cur, num))   # 保存上下文
            cur, num = '', 0
        elif ch == ']':
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur""",
    "java": """public String decodeString(String s) {
    Deque<String> strStack = new ArrayDeque<>();
    Deque<Integer> numStack = new ArrayDeque<>();
    StringBuilder cur = new StringBuilder();
    int num = 0;
    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) num = num * 10 + (c - '0');
        else if (c == '[') { strStack.push(cur.toString()); numStack.push(num); cur = new StringBuilder(); num = 0; }
        else if (c == ']') { String prev = strStack.pop(); int k = numStack.pop(); StringBuilder t = new StringBuilder(prev); for (int i = 0; i < k; i++) t.append(cur); cur = t; }
        else cur.append(c);
    }
    return cur.toString();
}""",
    "time": "O(输出长度) — 每个字符处理一次",
    "space": "O(嵌套深度) — 栈",
    "pitfalls": [["数字可能是多位", "num = num*10 + digit，不能只读一位"], ["入栈保存上下文", "'[' 时保存当前串与倍数，' ]' 时弹出拼接"]],
    "selfcheck": [["嵌套 3[a2[c]] 过程？", "内层 2[c] 先解为 cc，再 a+cc=acc，最后 ×3 得 accaccacc。"], ["递归写法？", "可以用递归：读到 '[' 递归解码括号内容，读到 ']' 返回，思路对称。"]],
}

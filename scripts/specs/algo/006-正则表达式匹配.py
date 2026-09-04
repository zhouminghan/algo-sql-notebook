from scripts.algo_gen import frame

PROBLEM = {
    "id": 6,
    "title": "正则表达式匹配",
    "diff": "hard",
    "tags": ["DP"],
    "leetcode": 10,
    "origin": "https://leetcode.cn/problems/regular-expression-matching/",
    "why": "'.' 匹配任意字符，'*' 匹配前一个字符零次或多次。dp[i][j] 表示 s 前 i 个与 p 前 j 个是否匹配，按 p[j-1] 是不是 '*' 分两种情况递推。",
    "desc": "<p>给定字符串 <code>s</code> 和字符规律 <code>p</code>，实现支持 <code>.</code> 和 <code>*</code> 的正则匹配。<code>.</code> 匹配任意单个字符；<code>*</code> 匹配零个或多个前面的那个元素。</p><p><strong>示例：</strong><br><code>s=\"aab\", p=\"c*a*b\"</code> → <code>true</code>（c 重复 0 次，a 重复 2 次）</p>",
    "frames": [
    frame("① dp[i][j]：s 前 i 个与 p 前 j 个是否匹配", "drawTable", headers=["", "", "c", "*", "a", "*", "b"], rows=[["", "T", "T", "F", "F", "F", "F"], ["a", "F", "F", "F", "T", "T", "F"], ["a", "F", "F", "F", "T", "T", "F"], ["b", "F", "F", "F", "F", "T", "T"]], width=460, height=200),
    frame("② p[j-1]=='*'：看前一个字符匹配几次", "drawTable", headers=["情况", "转移"], rows=[["* 当 0 个", "dp[i][j-2]"], ["* 当多个", "dp[i-1][j] 且 s[i-1] 匹配 p[j-2]"]], height=100),
    frame("③ 普通字符/'.'：直接比对", "drawTable", headers=["p[j-1]", "条件"], rows=[["普通字符", "s[i-1]==p[j-1]"], ["'.'", "恒成立"]], height=100),
    ],
    "conclusion": "按 '是否 *' 分支递推，右下角 dp[m][n] 即答案。",
    "py": """def isMatch(s, p):
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True
    for j in range(1, n+1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2] or (dp[i-1][j] and (s[i-1] == p[j-2] or p[j-2] == '.'))
            else:
                dp[i][j] = dp[i-1][j-1] and (s[i-1] == p[j-1] or p[j-1] == '.')
    return dp[m][n]""",
    "java": """public boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m+1][n+1];
    dp[0][0] = true;
    for (int j = 1; j <= n; j++) if (p.charAt(j-1) == '*') dp[0][j] = dp[0][j-2];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j-1) == '*') {
                dp[i][j] = dp[i][j-2] || (dp[i-1][j] && (s.charAt(i-1) == p.charAt(j-2) || p.charAt(j-2) == '.'));
            } else {
                dp[i][j] = dp[i-1][j-1] && (s.charAt(i-1) == p.charAt(j-1) || p.charAt(j-1) == '.');
            }
        }
    return dp[m][n];
}""",
    "time": "O(m·n)",
    "space": "O(m·n)",
    "pitfalls": [["dp[0][j] 初始化", "s 为空但 p 形如 a*b* 时可能匹配，要单独处理 '前缀'"], ["'*' 两个来源", "当 0 个（dp[i][j-2]）和当多个（dp[i-1][j]），漏一个会错"]],
    "selfcheck": [["\"aab\" 与 \"c*a*b\" 为何匹配？", "c* 匹配 0 个 c，a* 匹配 2 个 a，最后 b 匹配 b。"], ["'.*' 匹配什么？", "任意字符重复任意次，等价匹配任意字符串。"]],
}

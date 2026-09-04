from scripts.algo_gen import frame

PROBLEM = {
    "id": 36,
    "title": "编辑距离",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 72,
    "origin": "https://leetcode.cn/problems/edit-distance/",
    "why": "把两个串的前缀对齐：dp[i][j] 表示 word1 前 i 个字符变成 word2 前 j 个字符的最少操作数。三选一取最小——插入、删除、替换（相等则直接继承）。",
    "desc": """<p>给定两个单词 <code>word1</code> 和 <code>word2</code>，求将 word1 转换成 word2 所需的<strong>最少操作数</strong>。可进行的操作：插入一个字符、删除一个字符、替换一个字符。</p>
<p><strong>示例：</strong><br><code>word1="horse", word2="ros"</code> → <code>3</code>（horse→rorse→rose→ros）</p>""",
    "frames": [
    frame("① dp[i][j]：word1 前 i 个 → word2 前 j 个的最少操作", "drawTable", headers=["", "", "r", "o", "s"], rows=[["", "0", "1", "2", "3"], ["h", "1", "1", "2", "3"], ["o", "2", "2", "1", "2"], ["r", "3", "2", "2", "2"], ["s", "4", "3", "3", "2"], ["e", "5", "4", "4", {"val": "3", "highlight": True}]], width=440, height=260),
    frame("② 三选一：插入 dp[i][j-1]+1、删除 dp[i-1][j]+1、替换 dp[i-1][j-1]+1", "drawTable", headers=["操作", "来自", "代价"], rows=[["插入", "dp[i][j-1]", "+1"], ["删除", "dp[i-1][j]", "+1"], ["替换", "dp[i-1][j-1]", "相等则 +0"]], width=460, height=170),
    ],
    "conclusion": "字符相等就白拿对角线值，否则在插入/删除/替换里取最小并 +1，右下角即答案。",
    "py": """def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    return dp[m][n]""",
    "java": """public int minDistance(String w1, String w2) {
    int m = w1.length(), n = w2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (w1.charAt(i - 1) == w2.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]) + 1;
        }
    return dp[m][n];
}""",
    "time": "O(m · n)",
    "space": "O(m · n) — 可滚动优化到 O(n)",
    "pitfalls": [["三选一别漏", "插入、删除、替换对应三个方向，忘掉任何一个都会高估操作数"], ["相等直接继承", "word1[i-1]==word2[j-1] 时 dp[i][j]=dp[i-1][j-1]，不用 +1"]],
    "selfcheck": [["两个空串？", "m=n=0，dp[0][0]=0，返回 0。"], ["「horse」→「ros」为何是 3 步？", "h→r 替换(1)、删 e(1)、替换 s→? 实际路径：删 h、r 不变、o 不变、r→s? 对照 dp 表右下角即 3，具体路径可用回溯 dp 表还原。"]],
}

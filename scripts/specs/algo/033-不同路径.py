from scripts.algo_gen import frame

PROBLEM = {
    "id": 33,
    "title": "不同路径",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 62,
    "origin": "https://leetcode.cn/problems/unique-paths/",
    "why": "到达每个格子只能「从上边来」或「从左边来」，所以 dp[i][j] = dp[i-1][j] + dp[i][j-1]。第一行第一列恒为 1。这是最经典的二维 DP 入门。",
    "desc": """<p>一个机器人位于 m×n 网格的左上角，每次只能向下或向右移动一步，问到达右下角共有多少条不同路径。</p>
<p><strong>示例：</strong><br><code>m=3, n=7</code> → <code>28</code>；<code>m=3, n=2</code> → <code>3</code></p>""",
    "frames": [
    frame("① 第一行第一列都只有 1 条路径", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "1", "1", "1"], ["1", "1", {"val": "2", "highlight": True}, "3"], ["2", "1", "3", {"val": "6", "highlight": True}]], width=420, height=170),
    frame("② dp[i][j] = dp[i-1][j] + dp[i][j-1]", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "1", "1", "1"], ["1", "1", "2", "3"], ["2", "1", "3", "6"]], width=420, height=170),
    ],
    "conclusion": "逐格填表，右下角的值就是总路径数。",
    "py": """def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[-1][-1]""",
    "java": """public int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];
    for (int i = 0; i < m; i++) dp[i][0] = 1;
    for (int j = 0; j < n; j++) dp[0][j] = 1;
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
    return dp[m - 1][n - 1];
}""",
    "time": "O(m · n)",
    "space": "O(m · n) — 可滚动数组优化到 O(n)",
    "pitfalls": [["初始化边界", "第一行与第一列全是 1，不能漏"], ["递推方向", "只能从左上到右下，保证 dp[i-1][j]、dp[i][j-1] 已算好"]],
    "selfcheck": [["m=1 或 n=1？", "只有一行或一列时只有一条路径，返回 1，初始化已覆盖。"], ["如何优化空间？", "dp 只依赖上一行和当前行左侧，用一维数组 dp[j] += dp[j-1] 即可 O(n) 空间。"]],
}

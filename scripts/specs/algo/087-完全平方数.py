from scripts.algo_gen import frame

PROBLEM = {
    "id": 87,
    "title": "完全平方数",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 279,
    "origin": "https://leetcode.cn/problems/perfect-squares/",
    "why": "最少完全平方数个数 = 最少硬币问题。dp[i] = min(dp[i - j*j]) + 1，j 遍历所有小于 i 的平方数。也可用 BFS（层数即个数）。",
    "desc": """<p>给定整数 <code>n</code>，返回和为 n 的完全平方数的最少数量。完全平方数是 1、4、9、16… 这样的数。</p>
<p><strong>示例：</strong><br><code>n=12</code> → <code>3</code>（4+4+4）；<code>n=13</code> → <code>2</code>（4+9）</p>""",
    "frames": [
    frame("① dp[i] = min(dp[i - 平方数]) + 1", "drawTable", headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], rows=[["dp", "0", "1", "2", "3", "1", "2", "3", "4", "2", "1", "2", "3", "3"]], width=800, height=130),
    frame("② n=12：12-4=8(dp=2)、12-9=3(dp=3)、12-1=11(dp=3)，min=2+1=3", "drawTable", headers=["减哪个平方", "剩余", "剩余 dp", "总数"], rows=[["1", "11", "3", "4"], ["4", "8", "2", "3"], ["9", "3", "3", "4"]], width=460, height=160),
    ],
    "conclusion": "枚举最后一个平方数，取剩余部分的最小拆分数 + 1。",
    "py": """def numSquares(n):
    dp = [0] + [float('inf')] * n
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1
    return dp[n]""",
    "java": """public int numSquares(int n) {
    int[] dp = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j * j <= i; j++)
            dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
    return dp[n];
}""",
    "time": "O(n · √n)",
    "space": "O(n)",
    "pitfalls": [["dp[0]=0", "边界 0 需要 0 个平方数"], ["枚举 j*j <= i", "只枚举不超过 i 的平方数"]],
    "selfcheck": [["BFS 怎么做？", "从 n 出发，每层减去一个平方数，第一次减到 0 的层数就是答案。"], ["四平方和定理？", "任意正整数可表为至多 4 个平方数之和，是这题的理论上界。"]],
}

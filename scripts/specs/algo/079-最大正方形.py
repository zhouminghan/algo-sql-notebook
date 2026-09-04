from scripts.algo_gen import frame

PROBLEM = {
    "id": 79,
    "title": "最大正方形",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 221,
    "origin": "https://leetcode.cn/problems/maximal-square/",
    "why": "以 (i,j) 为右下角的最大正方形边长，取决于左上、上、左三个方向的最小值 + 1。dp[i][j] = min(三个) + 1（当 grid=1），边长平方即面积。",
    "desc": """<p>在一个由 <code>'0'</code> 和 <code>'1'</code> 组成的二维矩阵内，找到只包含 1 的最大正方形，并返回其面积。</p>
<p><strong>示例：</strong><br><code>[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]</code> → <code>4</code></p>""",
    "frames": [
    frame("① dp[i][j] = 以 (i,j) 为右下角的最大边长", "drawTable", headers=["", "0", "1", "2", "3", "4"], rows=[["0", "1", "0", "1", "0", "0"], ["1", "1", "0", "1", "1", "1"], ["2", "1", "1", "1", "2", "2"], ["3", "1", "0", "0", "1", "0"]], width=500, height=190),
    frame("② 递推：min(左上, 上, 左) + 1", "drawTable", headers=["方向", "左上", "上", "左"], rows=[["dp 值", "1", "1", "1"], ["本格", "min(1,1,1)+1 = 2"]], width=460, height=140),
    frame("③ 最大边长 2，面积 4", "drawTable", headers=["", "值"], rows=[["最大边长", "2"], ["面积", {"val": "4", "highlight": True}]], width=420, height=130),
    ],
    "conclusion": "三个相邻 dp 的最小值决定能否「扩一格」，边长取最大后平方。",
    "py": """def maximalSquare(matrix):
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                max_side = max(max_side, dp[i][j])
    return max_side * max_side""",
    "java": """public int maximalSquare(char[][] matrix) {
    int m = matrix.length, n = matrix[0].length, side = 0;
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            if (matrix[i - 1][j - 1] == '1') {
                dp[i][j] = Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]) + 1;
                side = Math.max(side, dp[i][j]);
            }
    return side * side;
}""",
    "time": "O(m · n)",
    "space": "O(m · n) — 可滚动优化到 O(n)",
    "pitfalls": [["三个方向取 min", "取 max 会错误地把「L 形」当成正方形"], ["面积是边长平方", "返回 side*side，别直接返回边长"]],
    "selfcheck": [["为什么 min(三个)+1？", "以 (i,j) 为右下角的正方形，其上边、左边、左上角必须同时都能容纳 side-1 的正方形，取三者交集即 min。"], ["全 0 矩阵？", "side 保持 0，返回 0。"]],
}

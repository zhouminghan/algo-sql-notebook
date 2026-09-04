from scripts.algo_gen import frame

PROBLEM = {
    "id": 34,
    "title": "最小路径和",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 64,
    "origin": "https://leetcode.cn/problems/minimum-path-sum/",
    "why": "与「不同路径」同构，只是把「加法计数」换成「取最小值」：dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])。边界单独累加。",
    "desc": """<p>给定一个包含非负整数的 m×n 网格，找出一条从左上角到右下角的路径，使得路径上的数字总和最小。每次只能向下或向右移动。</p>
<p><strong>示例：</strong><br><code>[[1,3,1],[1,5,1],[4,2,1]]</code> → <code>7</code>（1→3→1→1→1）</p>""",
    "frames": [
    frame("① 原网格", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "1", "3", "1"], ["1", "1", "5", "1"], ["2", "4", "2", "1"]], width=420, height=170),
    frame("② dp 表：每格 = 自己 + min(上, 左)", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "1", "4", "5"], ["1", "2", "7", "6"], ["2", "6", "8", {"val": "7", "highlight": True}]], width=420, height=170),
    ],
    "conclusion": "每个格子选「上面来的」与「左边来的」中更小的那条路，累加自身值即可。",
    "py": """def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if i == 0:
                grid[i][j] += grid[i][j - 1]
            elif j == 0:
                grid[i][j] += grid[i - 1][j]
            else:
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
    return grid[-1][-1]""",
    "java": """public int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            if (i == 0 && j == 0) continue;
            if (i == 0) grid[i][j] += grid[i][j - 1];
            else if (j == 0) grid[i][j] += grid[i - 1][j];
            else grid[i][j] += Math.min(grid[i - 1][j], grid[i][j - 1]);
        }
    return grid[m - 1][n - 1];
}""",
    "time": "O(m · n)",
    "space": "O(1) — 原地累加",
    "pitfalls": [["边界累加", "第一行只能从左边来，第一列只能从上面来，要单独处理"], ["不能贪心", "局部选最小的格子不能保证全局最小，必须 DP 比较两条来路"]],
    "selfcheck": [["为什么不能每步都往较小数字走？", "贪心可能走进「当前小但后面大」的死胡同；DP 保证每个格子都取到「到它为止」的全局最小，最终必最优。"], ["有负数会怎样？", "本题保证非负；若含负数，DP 仍正确（只是路径和可为负），但「到终点最小」定义不变。"]],
}

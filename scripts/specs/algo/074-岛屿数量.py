from scripts.algo_gen import frame

PROBLEM = {
    "id": 74,
    "title": "岛屿数量",
    "diff": "medium",
    "tags": ["DFS"],
    "leetcode": 200,
    "origin": "https://leetcode.cn/problems/number-of-islands/",
    "why": "遍历每个格子，遇到 '1' 就启动 DFS，把相连的陆地全部「淹没」为 '0'（或标记已访问），计一个岛。每个格子访问一次，O(m·n)。",
    "desc": """<p>给定由 <code>'1'</code>（陆地）和 <code>'0'</code>（水）组成的二维网格，计算网格中岛屿的数量。岛屿被水包围，由水平或垂直相邻的陆地连接形成。</p>
<p><strong>示例：</strong><br><code>[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]</code> → <code>3</code></p>""",
    "frames": [
    frame("① 遇到陆地就 DFS 淹没整片", "drawTable", headers=["", "0", "1", "2", "3", "4"], rows=[["0", "1", "1", "0", "0", "0"], ["1", "1", "1", "0", "0", "0"], ["2", "0", "0", "1", "0", "0"], ["3", "0", "0", "0", "1", "1"]], width=500, height=190),
    frame("② 淹没后该岛计 1，继续扫描", "drawTable", headers=["", "0", "1", "2", "3", "4"], rows=[["0", "0", "0", "0", "0", "0"], ["1", "0", "0", "0", "0", "0"], ["2", "0", "0", {"val": "1", "highlight": True}, "0", "0"], ["3", "0", "0", "0", "1", "1"]], width=500, height=190),
    ],
    "conclusion": "一次 DFS 消灭一个连通块，计数就是岛屿数。",
    "py": """def numIslands(grid):
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '0'          # 淹没
        dfs(i + 1, j); dfs(i - 1, j); dfs(i, j + 1); dfs(i, j - 1)
    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                ans += 1
                dfs(i, j)
    return ans""",
    "java": """public int numIslands(char[][] grid) {
    int m = grid.length, n = grid[0].length, ans = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (grid[i][j] == '1') { ans++; dfs(grid, i, j); }
    return ans;
}
void dfs(char[][] g, int i, int j) {
    if (i < 0 || i >= g.length || j < 0 || j >= g[0].length || g[i][j] != '1') return;
    g[i][j] = '0';
    dfs(g, i + 1, j); dfs(g, i - 1, j); dfs(g, i, j + 1); dfs(g, i, j - 1);
}""",
    "time": "O(m · n)",
    "space": "O(m · n) — 递归栈最坏全陆地",
    "pitfalls": [["淹没或标记", "访问过必须置 '0' 或 visited，否则重复计数/死循环"], ["边界与越界", "四个方向先判界再判值"]],
    "selfcheck": [["BFS 版本？", "用队列把相连陆地依次入队处理，逻辑与 DFS 一致，只是遍历方式不同。"], ["为什么 DFS 递归不会重复访问？", "进入就置 '0'，后续递归不会再把它当作 '1'，天然去重。"]],
}

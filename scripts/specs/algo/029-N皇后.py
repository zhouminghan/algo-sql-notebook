from scripts.algo_gen import frame

PROBLEM = {
    "id": 29,
    "title": "N皇后",
    "diff": "hard",
    "tags": ["回溯"],
    "leetcode": 51,
    "origin": "https://leetcode.cn/problems/n-queens/",
    "why": "每行必须且只能放一个皇后，于是按行递归，每行尝试 n 列。用三个集合记录「列、主对角线、副对角线」是否被占，把判断冲突从 O(n) 降到 O(1)，大幅剪枝。",
    "desc": """<p>N 皇后问题：把 n 个皇后放在 n×n 棋盘上，使它们<strong>互不攻击</strong>（任意两个皇后不能在同一行、同一列或同一斜线上）。返回所有不同的解法。</p>
<p><strong>示例：</strong><br><code>n=4</code> 有 2 个解，其中一个：<code>[".Q..","...Q","Q...","..Q."]</code></p>""",
    "frames": [
    frame("① 按行放置，用三个集合记录被占的列/斜线", "drawTable", headers=["", "0", "1", "2", "3"], rows=[["0", "·", "Q", "·", "·"], ["1", "·", "·", "·", "Q"], ["2", "Q", "·", "·", "·"], ["3", "·", "·", "Q", "·"]], width=420, height=190),
    frame("② 斜线编号：主对角线 = row - col，副对角线 = row + col", "drawTable", headers=["位置", "r-c", "r+c"], rows=[["(0,1)", "-1", "1"], ["(1,3)", "-2", "4"], ["(2,0)", "2", "2"]], width=460, height=170),
    frame("③ 冲突就回溯，尝试下一列", "drawBacktrack", nodes=[{"val": "第0行", "x": 300, "y": 15, "color": "normal"}, {"val": "列1 ✓", "x": 150, "y": 85, "color": "path"}, {"val": "列0 ✓", "x": 450, "y": 85, "color": "path"}, {"val": "第1行列0 ✗", "x": 100, "y": 165, "color": "pruned"}, {"val": "第1行列2 ✓", "x": 210, "y": 165, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 150, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 450, "y2": 85, "color": "path"}, {"x1": 150, "y1": 85, "x2": 100, "y2": 165, "color": "pruned"}, {"x1": 150, "y1": 85, "x2": 210, "y2": 165, "color": "path"}], width=580, height=210),
    ],
    "conclusion": "行、列、两条斜线各用一个集合判重，冲突即刻回溯，搜完整棵树就得到全部解。",
    "py": """def solveNQueens(n):
    ans, board = [], [['.'] * n for _ in range(n)]
    cols, diag1, diag2 = set(), set(), set()
    def dfs(r):
        if r == n:
            ans.append([''.join(row) for row in board]); return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c); diag1.add(r - c); diag2.add(r + c); board[r][c] = 'Q'
            dfs(r + 1)
            board[r][c] = '.'; cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)
    dfs(0)
    return ans""",
    "java": """public List<List<String>> solveNQueens(int n) {
    List<List<String>> ans = new ArrayList<>();
    char[][] b = new char[n][n];
    for (char[] row : b) Arrays.fill(row, '.');
    dfs(0, n, b, new boolean[n], new boolean[2 * n], new boolean[2 * n], ans);
    return ans;
}
void dfs(int r, int n, char[][] b, boolean[] col, boolean[] d1, boolean[] d2, List<List<String>> ans) {
    if (r == n) {
        List<String> list = new ArrayList<>();
        for (char[] row : b) list.add(new String(row));
        ans.add(list); return;
    }
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r - c + n] || d2[r + c]) continue;
        col[c] = d1[r - c + n] = d2[r + c] = true; b[r][c] = 'Q';
        dfs(r + 1, n, b, col, d1, d2, ans);
        b[r][c] = '.'; col[c] = d1[r - c + n] = d2[r + c] = false;
    }
}""",
    "time": "O(n!) — 每行可放列数递减，剪枝后远小于 n^n",
    "space": "O(n) — 递归栈 + 三个判重数组",
    "pitfalls": [["斜线判重用集合/数组", "主对角线 r-c（可能为负，Java 需 +n 偏移），副对角线 r+c，两套都要查"], ["回溯要撤销", "三个判重集合与棋盘都要在递归返回后恢复，否则影响兄弟分支"]],
    "selfcheck": [["n=1 有解吗？", "有，只有 [\"Q\"] 一个解。n=2、n=3 无解，n=4 有 2 解。"], ["为什么按行放而不是任意放？", "任意放会有 n² 个格子可选，状态爆炸；按行放保证每行一个皇后，天然满足行互斥，状态降到 n^n 且配合列/斜线剪枝。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 41,
    "title": "单词搜索",
    "diff": "medium",
    "tags": ["回溯"],
    "leetcode": 79,
    "origin": "https://leetcode.cn/problems/word-search/",
    "why": "从每个格子出发做 DFS，向上下左右四个方向匹配单词的下一字符；走过的格子暂时标记，走不通就回溯还原，避免重复使用同一格。",
    "desc": """<p>给定 m×n 的字符网格 <code>board</code> 和字符串 <code>word</code>，判断 word 是否存在于网格中。单词必须按相邻单元格的字母构成（水平或垂直相邻），同一单元格不能用两次。</p>
<p><strong>示例：</strong><br><code>board=[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCCED"</code> → <code>true</code></p>""",
    "frames": [
    frame("① 从每个格子出发，向四周 DFS", "drawTable", headers=["", "0", "1", "2", "3"], rows=[["0", "A", "B", "C", "E"], ["1", "S", "F", "C", "S"], ["2", "A", "D", "E", "E"]], width=420, height=170),
    frame("② 匹配路径 A→B→C→C→E→D，走过的格子临时标记", "drawTable", headers=["", "0", "1", "2", "3"], rows=[["0", {"val": "A", "highlight": True}, {"val": "B", "highlight": True}, {"val": "C", "highlight": True}, "E"], ["1", "S", "F", {"val": "C", "highlight": True}, "S"], ["2", "A", {"val": "D", "highlight": True}, {"val": "E", "highlight": True}, "E"]], width=420, height=170),
    frame("③ 走不通就回溯，恢复标记，换方向", "drawBacktrack", nodes=[{"val": "A", "x": 300, "y": 15, "color": "path"}, {"val": "B", "x": 200, "y": 90, "color": "path"}, {"val": "C(上)", "x": 120, "y": 170, "color": "path"}, {"val": "走不通 ✗", "x": 360, "y": 170, "color": "pruned"}, {"val": "C(右)", "x": 210, "y": 245, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 200, "y2": 90, "color": "path"}, {"x1": 200, "y1": 90, "x2": 120, "y2": 170, "color": "path"}, {"x1": 120, "y1": 170, "x2": 360, "y2": 170, "color": "pruned"}, {"x1": 200, "y1": 90, "x2": 210, "y2": 245, "color": "path"}], width=560, height=280),
    ],
    "conclusion": "四个方向递归匹配 + 原地标记去重 + 失败回溯，遍历所有起点即可判断是否存在。",
    "py": """def exist(board, word):
    m, n = len(board), len(board[0])
    def dfs(i, j, k):
        if k == len(word):
            return True
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
            return False
        tmp = board[i][j]
        board[i][j] = '#'          # 标记已走
        found = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1)
                 or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
        board[i][j] = tmp          # 回溯还原
        return found
    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False""",
    "java": """public boolean exist(char[][] board, String word) {
    int m = board.length, n = board[0].length;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (dfs(board, word, i, j, 0)) return true;
    return false;
}
boolean dfs(char[][] b, String w, int i, int j, int k) {
    if (k == w.length()) return true;
    if (i < 0 || i >= b.length || j < 0 || j >= b[0].length || b[i][j] != w.charAt(k)) return false;
    char tmp = b[i][j]; b[i][j] = '#';
    boolean f = dfs(b, w, i + 1, j, k + 1) || dfs(b, w, i - 1, j, k + 1)
             || dfs(b, w, i, j + 1, k + 1) || dfs(b, w, i, j - 1, k + 1);
    b[i][j] = tmp;
    return f;
}""",
    "time": "O(m·n·3^L) — L 为单词长度，每步最多 3 个方向",
    "space": "O(L) — 递归深度",
    "pitfalls": [["标记与还原", "用 board[i][j]='#' 临时占用，返回前必须还原，否则兄弟分支被污染"], ["方向边界", "四个方向都要判越界，别漏 i、j 的范围检查"]],
    "selfcheck": [["同一格子能用两次吗？", "不能。标记 '#' 后，后续递归不会再匹配它，回溯时再还原给别的路径使用。"], ["多个起点怎么处理？", "外层双重循环对每个格子都尝试作为起点，只要有一个返回 true 即存在。"]],
}

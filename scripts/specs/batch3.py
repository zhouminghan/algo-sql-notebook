from scripts.algo_gen import frame


PROBLEMS = [
    # ---------------------------------------------------------------- 41
    {
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
            frame("① 从每个格子出发，向四周 DFS", "drawTable",
                  headers=["", "0", "1", "2", "3"],
                  rows=[["0", "A", "B", "C", "E"], ["1", "S", "F", "C", "S"], ["2", "A", "D", "E", "E"]], width=420, height=170),
            frame("② 匹配路径 A→B→C→C→E→D，走过的格子临时标记", "drawTable",
                  headers=["", "0", "1", "2", "3"],
                  rows=[["0", {"val": "A", "highlight": True}, {"val": "B", "highlight": True}, {"val": "C", "highlight": True}, "E"], ["1", "S", "F", {"val": "C", "highlight": True}, "S"], ["2", "A", {"val": "D", "highlight": True}, {"val": "E", "highlight": True}, "E"]], width=420, height=170),
            frame("③ 走不通就回溯，恢复标记，换方向", "drawBacktrack",
                  nodes=[{"val": "A", "x": 300, "y": 15, "color": "path"}, {"val": "B", "x": 200, "y": 90, "color": "path"}, {"val": "C(上)", "x": 120, "y": 170, "color": "path"}, {"val": "走不通 ✗", "x": 360, "y": 170, "color": "pruned"}, {"val": "C(右)", "x": 210, "y": 245, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 200, "y2": 90, "color": "path"}, {"x1": 200, "y1": 90, "x2": 120, "y2": 170, "color": "path"}, {"x1": 120, "y1": 170, "x2": 360, "y2": 170, "color": "pruned"}, {"x1": 200, "y1": 90, "x2": 210, "y2": 245, "color": "path"}],
                  width=560, height=280),
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
        "pitfalls": [
            ("标记与还原", "用 board[i][j]='#' 临时占用，返回前必须还原，否则兄弟分支被污染"),
            ("方向边界", "四个方向都要判越界，别漏 i、j 的范围检查"),
        ],
        "selfcheck": [
            ("同一格子能用两次吗？", "不能。标记 '#' 后，后续递归不会再匹配它，回溯时再还原给别的路径使用。"),
            ("多个起点怎么处理？", "外层双重循环对每个格子都尝试作为起点，只要有一个返回 true 即存在。"),
        ],
    },
    # ---------------------------------------------------------------- 42
    {
        "id": 42,
        "title": "柱状图中最大的矩形",
        "diff": "hard",
        "tags": ["单调栈"],
        "leetcode": 84,
        "origin": "https://leetcode.cn/problems/largest-rectangle-in-histogram/",
        "why": "对每根柱子，以它高度为高的最大矩形，向左右延伸到「第一个比它矮的柱子」为止。单调递增栈能在 O(n) 内同时找到每根柱子左右两侧最近更矮的位置。",
        "desc": """<p>给定 n 个非负整数表示柱状图的高度（每个柱宽 1），求图中能勾勒出的最大矩形面积。</p>
<p><strong>示例：</strong><br><code>heights=[2,1,5,6,2,3]</code> → <code>10</code></p>""",
        "frames": [
            frame("① 以高度 5 为高的矩形：左右延伸到第一个更矮处", "drawTwoPointers", arr=[2, 1, 5, 6, 2, 3], left=2, right=3, window={"start": 2, "end": 3}, width=560, height=150),
            frame("② 以高度 2（下标 4）为高：向左延伸到 1 之后，向右到末尾", "drawTwoPointers", arr=[2, 1, 5, 6, 2, 3], left=4, right=5, window={"start": 1, "end": 5}, width=560, height=150),
            frame("③ 单调栈：栈内高度递增，遇到更矮就弹出并结算", "drawStack", items=[{"val": "2"}, {"val": "5"}, {"val": "6"}], type="stack", height=170),
        ],
        "conclusion": "单调栈维护「递增高度」，每次弹出高度 h 时，其可扩展宽度 = 当前下标 - 新栈顶下标 - 1，面积 = h × 宽。",
        "py": """def largestRectangleArea(heights):
    stack = []
    ans = 0
    heights = heights + [0]        # 末尾加 0 逼出所有栈
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            ans = max(ans, heights[cur] * (i - left - 1))
        stack.append(i)
    return ans""",
        "java": """public int largestRectangleArea(int[] heights) {
    int n = heights.length, ans = 0;
    int[] h = new int[n + 1];
    System.arraycopy(heights, 0, h, 0, n);
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        while (!st.isEmpty() && h[st.peek()] > h[i]) {
            int cur = st.pop();
            int left = st.isEmpty() ? -1 : st.peek();
            ans = Math.max(ans, h[cur] * (i - left - 1));
        }
        st.push(i);
    }
    return ans;
}""",
        "time": "O(n) — 每个下标入栈出栈一次",
        "space": "O(n) — 栈",
        "pitfalls": [
            ("末尾补 0", "补一个高度 0 的哨兵，循环结束时能自动弹出所有剩余柱子结算"),
            ("宽度计算", "弹出 cur 后，新栈顶就是它左边最近的更矮位置，宽 = i - left - 1"),
        ],
        "selfcheck": [
            ("为什么用单调递增栈？", "栈内高度递增意味着每个柱子的「左边界」已知；遇到更矮柱子时，它就成了右侧边界，可立即结算被弹出的柱子。"),
            ("[2,1,2] 的最大矩形？", "高度 2 的矩形（下标 0 和 2 分别面积 2），以及高度 1 横跨全长的面积 3，答案为 3。"),
        ],
    },
    # ---------------------------------------------------------------- 43
    {
        "id": 43,
        "title": "最大矩形",
        "diff": "hard",
        "tags": ["单调栈"],
        "leetcode": 85,
        "origin": "https://leetcode.cn/problems/maximal-rectangle/",
        "why": "把矩阵每一行看成「柱状图」：以当前行为底，向上连续 1 的个数就是柱子高度。逐行构造 heights，对每行跑一次「柱状图最大矩形」的单调栈，取全局最大。",
        "desc": """<p>给定一个仅包含 0 和 1、大小为 m×n 的二维二进制矩阵，找出只包含 1 的最大矩形，并返回其面积。</p>
<p><strong>示例：</strong><br><code>[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]</code> → <code>6</code></p>""",
        "frames": [
            frame("① 以第 2 行为底，向上连续 1 构成柱状图", "drawTable",
                  headers=["", "0", "1", "2", "3", "4"],
                  rows=[["矩阵", "1", "0", "1", "0", "0"], ["1", "1", "0", "1", "1", "1"], ["2", "1", "1", "1", "1", "1"], ["heights", "3", "1", "3", "2", "2"]], width=500, height=200),
            frame("② 对该柱状图跑单调栈求最大矩形", "drawTwoPointers", arr=[3, 1, 3, 2, 2], left=0, right=4, width=520, height=140),
            frame("③ 逐行更新 heights，取全局最大面积", "drawTable",
                  headers=["行", "heights", "最大矩形"],
                  rows=[["0", "1,0,1,0,0", "1"], ["1", "2,0,2,1,1", "3"], ["2", "3,1,3,2,2", {"val": "6", "highlight": True}]], width=500, height=170),
        ],
        "conclusion": "把二维问题拆成「每一行作为底的柱状图问题」，复用单调栈模板，O(m·n) 求解。",
        "py": """def maximalRectangle(matrix):
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    heights = [0] * n
    ans = 0
    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        ans = max(ans, largestRectangleArea(heights))
    return ans


def largestRectangleArea(heights):
    stack, ans = [], 0
    hs = heights + [0]
    for i, h in enumerate(hs):
        while stack and hs[stack[-1]] > h:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            ans = max(ans, hs[cur] * (i - left - 1))
        stack.append(i)
    return ans""",
        "java": """public int maximalRectangle(char[][] matrix) {
    if (matrix.length == 0 || matrix[0].length == 0) return 0;
    int n = matrix[0].length, ans = 0;
    int[] h = new int[n];
    for (char[] row : matrix) {
        for (int j = 0; j < n; j++)
            h[j] = row[j] == '1' ? h[j] + 1 : 0;
        ans = Math.max(ans, largestRectangleArea(h));
    }
    return ans;
}
int largestRectangleArea(int[] heights) {
    int n = heights.length, ans = 0;
    int[] h = new int[n + 1];
    System.arraycopy(heights, 0, h, 0, n);
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        while (!st.isEmpty() && h[st.peek()] > h[i]) {
            int cur = st.pop(), left = st.isEmpty() ? -1 : st.peek();
            ans = Math.max(ans, h[cur] * (i - left - 1));
        }
        st.push(i);
    }
    return ans;
}""",
        "time": "O(m · n) — 每行一次单调栈",
        "space": "O(n) — 高度数组 + 栈",
        "pitfalls": [
            ("heights 遇 0 归零", "row[j]=='0' 时该列高度直接清零，不是保持原值"),
            ("复用 84 题", "先把「柱状图最大矩形」写对，本行逻辑只是逐行喂 heights"),
        ],
        "selfcheck": [
            ("为什么不是 O(m·n²)？", "每行单调栈 O(n)，共 m 行，总计 O(m·n)。"),
            ("第一行怎么算？", "heights 初始全 0，第一行遇到 1 就为 1、遇到 0 就为 0，自然形成柱状图。"),
        ],
    },
    # ---------------------------------------------------------------- 44
    {
        "id": 44,
        "title": "二叉树的中序遍历",
        "diff": "easy",
        "tags": ["树"],
        "leetcode": 94,
        "origin": "https://leetcode.cn/problems/binary-tree-inorder-traversal/",
        "why": "中序遍历的顺序是「左 → 根 → 右」。递归一行就够；迭代则用栈模拟「一直往左走，到底弹出访问，再转右子树」，是理解二叉树遍历的基础。",
        "desc": """<p>给定二叉树的根节点，返回它的<strong>中序</strong>遍历。</p>
<p><strong>示例：</strong><br>树 <code>[1,null,2,3]</code> → <code>[1,3,2]</code></p>""",
        "frames": [
            frame("① 中序：左 → 根 → 右", "drawTree",
                  nodes=[{"val": "1", "x": 300, "y": 40}, {"val": "2", "x": 420, "y": 130, "highlight": "active"}, {"val": "3", "x": 360, "y": 220, "highlight": "done"}],
                  edges=[{"x1": 300, "y1": 40, "x2": 420, "y2": 130}, {"x1": 420, "y1": 130, "x2": 360, "y2": 220}], width=520, height=260),
            frame("② 迭代：一直向左压栈，到底后弹出访问，再转右", "drawStack",
                  items=[{"val": "1"}, {"val": "2"}], type="stack", height=160),
            frame("③ 访问顺序 [1,3,2]", "drawTable", headers=["顺序", "0", "1", "2"], rows=[["值", "1", "3", "2"]], width=460, height=110),
        ],
        "conclusion": "「左-根-右」递归即答案；迭代栈版本在面试中常被要求手写。",
        "py": """def inorderTraversal(root):
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res""",
        "java": """public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        cur = st.pop();
        res.add(cur.val);
        cur = cur.right;
    }
    return res;
}""",
        "time": "O(n) — 每个节点访问一次",
        "space": "O(h) — 栈深度，h 为树高",
        "pitfalls": [
            ("遍历顺序", "先递归左子树、再访问根、最后右子树，顺序记牢"),
            ("迭代的 cur 移动", "压栈时 cur=cur.left，弹出访问后 cur=cur.right，缺一步就死循环"),
        ],
        "selfcheck": [
            ("空树？", "root 为 None，直接返回空列表。"),
            ("前序、后序与中序差在哪？", "只差「访问根」的时机：前序在入栈前访问，中序在出栈时访问，后序在左右都处理完再访问。"),
        ],
    },
    # ---------------------------------------------------------------- 45
    {
        "id": 45,
        "title": "不同的二叉搜索树",
        "diff": "medium",
        "tags": ["树"],
        "leetcode": 96,
        "origin": "https://leetcode.cn/problems/unique-binary-search-trees/",
        "why": "以 i 为根时，左子树有 i-1 个节点、右子树有 n-i 个节点，数量相乘再对 i 求和，即卡特兰数递推：G(n)=Σ G(i-1)·G(n-i)。",
        "desc": """<p>给定整数 n，求由 n 个节点组成且节点值从 1 到 n 互不相同的<strong>二叉搜索树</strong>有多少种。</p>
<p><strong>示例：</strong><br><code>n=3</code> → <code>5</code></p>""",
        "frames": [
            frame("① 以 i 为根：左子树 G(i-1) 种 × 右子树 G(n-i) 种", "drawTable",
                  headers=["根", "左子树", "右子树", "组合数"],
                  rows=[["1", "G(0)", "G(2)", "1×2=2"], ["2", "G(1)", "G(1)", "1×1=1"], ["3", "G(2)", "G(0)", "2×1=2"]], width=500, height=170),
            frame("② 卡特兰数：G(0)=1, G(1)=1, G(2)=2, G(3)=5", "drawTable",
                  headers=["n", "0", "1", "2", "3", "4"],
                  rows=[["G(n)", "1", "1", "2", "5", "14"]], width=520, height=110),
        ],
        "conclusion": "枚举根节点，左右子树数量相乘累加，DP 递推得到卡特兰数。",
        "py": """def numTrees(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j - 1] * dp[i - j]
    return dp[n]""",
        "java": """public int numTrees(int n) {
    int[] dp = new int[n + 1];
    dp[0] = dp[1] = 1;
    for (int i = 2; i <= n; i++)
        for (int j = 1; j <= i; j++)
            dp[i] += dp[j - 1] * dp[i - j];
    return dp[n];
}""",
        "time": "O(n²)",
        "space": "O(n)",
        "pitfalls": [
            ("G(0)=1", "空树算一种，边界定义成 1 递推才成立"),
            ("累加不是相乘整体", "每个根 j 贡献 dp[j-1]*dp[i-j]，要累加所有 j"),
        ],
        "selfcheck": [
            ("n=2 为什么是 2？", "以 1 为根：右子树 G(1)=1；以 2 为根：左子树 G(1)=1；合计 2。"),
            ("这题与「生成所有 BST」区别？", "本题只数个数（DP/卡特兰数）；生成所有 BST 需要递归构造左右子树并组合。"),
        ],
    },
    # ---------------------------------------------------------------- 46
    {
        "id": 46,
        "title": "验证二叉搜索树",
        "diff": "medium",
        "tags": ["BST"],
        "leetcode": 98,
        "origin": "https://leetcode.cn/problems/validate-binary-search-tree/",
        "why": "BST 要求「整棵左子树都小于根、整棵右子树都大于根」，只比较父子是不够的。递归时携带 (min, max) 上下界，把每个节点约束在开区间内。",
        "desc": """<p>给定二叉树的根节点，判断其是否是一个有效的二叉搜索树。有效 BST 定义：节点的左子树只含<strong>小于</strong>当前节点的数；右子树只含<strong>大于</strong>当前节点的数；所有左右子树自身也必须是 BST。</p>
<p><strong>示例：</strong><br><code>[2,1,3]</code> → <code>true</code>；<code>[5,1,4,null,null,3,6]</code> → <code>false</code></p>""",
        "frames": [
            frame("① 每个节点必须落在 (min, max) 区间内", "drawTree",
                  nodes=[{"val": "5", "x": 300, "y": 30}, {"val": "1", "x": 170, "y": 120}, {"val": "4", "x": 430, "y": 120, "highlight": "active"}, {"val": "3", "x": 360, "y": 210, "highlight": "done"}, {"val": "6", "x": 500, "y": 210}],
                  edges=[{"x1": 300, "y1": 30, "x2": 170, "y2": 120}, {"x1": 300, "y1": 30, "x2": 430, "y2": 120}, {"x1": 430, "y1": 120, "x2": 360, "y2": 210}, {"x1": 430, "y1": 120, "x2": 500, "y2": 210}], width=560, height=250),
            frame("② 只比较父子不够：3 虽小于父 4，但小于祖 5，越界", "drawTable",
                  headers=["节点", "应在区间", "实际", "合法?"],
                  rows=[["5", "(-∞,+∞)", "5", "✓"], ["4", "(5,+∞)", "4", "✓"], ["3", "(5,+∞)", "3", "✗"]], width=500, height=170),
        ],
        "conclusion": "递归时把祖先的约束作为上下界一路传下去，任何节点越界即判非法。",
        "py": """def isValidBST(root):
    def check(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))""",
        "java": """public boolean isValidBST(TreeNode root) {
    return check(root, null, null);
}
boolean check(TreeNode n, Integer lo, Integer hi) {
    if (n == null) return true;
    if (lo != null && n.val <= lo) return false;
    if (hi != null && n.val >= hi) return false;
    return check(n.left, lo, n.val) && check(n.right, n.val, hi);
}""",
        "time": "O(n) — 每个节点访问一次",
        "space": "O(h) — 递归栈",
        "pitfalls": [
            ("必须带上下界", "只判断 node.left < node < node.right 无法发现「右子树里有比根小的数」"),
            ("中序遍历法", "BST 中序遍历应严格递增，也可以边遍历边比较前驱，但需处理相等"),
        ],
        "selfcheck": [
            ("节点值相等算 BST 吗？", "不算。左子树必须「严格小于」、右子树「严格大于」，相等直接非法。"),
            ("[5,1,4,null,null,3,6] 为何 false？", "4 的右子树里有 3，而 3 < 根 5，违反了「右子树全部大于根」的约束。"),
        ],
    },
    # ---------------------------------------------------------------- 47
    {
        "id": 47,
        "title": "对称二叉树",
        "diff": "easy",
        "tags": ["树"],
        "leetcode": 101,
        "origin": "https://leetcode.cn/problems/symmetric-tree/",
        "why": "对称 = 左子树的左 == 右子树的右，且左子树的右 == 右子树的左。递归比较「镜像位置」的两个节点，或迭代用队列两两入队比较。",
        "desc": """<p>给定二叉树的根节点，检查它是否<strong>轴对称</strong>（镜像对称）。</p>
<p><strong>示例：</strong><br><code>[1,2,2,3,4,4,3]</code> → <code>true</code>；<code>[1,2,2,null,3,null,3]</code> → <code>false</code></p>""",
        "frames": [
            frame("① 镜像比较：左.left vs 右.right，左.right vs 右.left", "drawTree",
                  nodes=[{"val": "1", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110, "highlight": "active"}, {"val": "2", "x": 440, "y": 110, "highlight": "active"}, {"val": "3", "x": 100, "y": 200}, {"val": "4", "x": 220, "y": 200}, {"val": "4", "x": 380, "y": 200}, {"val": "3", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
            frame("② 递归比较镜像节点", "drawTable",
                  headers=["对比对", "左", "右", "相等?"],
                  rows=[["第一对", "2", "2", "✓"], ["第二对", "3", "3", "✓"], ["第三对", "4", "4", "✓"]], width=460, height=170),
        ],
        "conclusion": "把「是否对称」转化成「两棵镜像子树是否相等」，递归即可。",
        "py": """def isSymmetric(root):
    if not root:
        return True
    def mirror(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right)""",
        "java": """public boolean isSymmetric(TreeNode root) {
    return root == null || mirror(root.left, root.right);
}
boolean mirror(TreeNode a, TreeNode b) {
    if (a == null && b == null) return true;
    if (a == null || b == null || a.val != b.val) return false;
    return mirror(a.left, b.right) && mirror(a.right, b.left);
}""",
        "time": "O(n)",
        "space": "O(h)",
        "pitfalls": [
            ("比较的是镜像位置", "a.left 对应 b.right，a.right 对应 b.left，不是同名左右"),
            ("空节点成对判断", "一个空一个非空也返回 false，先判空再判值"),
        ],
        "selfcheck": [
            ("空树对称吗？", "对称，直接返回 true。"),
            ("[1,2,2,null,3,null,3] 为何 false？", "左侧 2 的右子 3 应对应右侧 2 的左子，但右侧没有左子，结构不对称。"),
        ],
    },
    # ---------------------------------------------------------------- 48
    {
        "id": 48,
        "title": "二叉树的层序遍历",
        "diff": "medium",
        "tags": ["BFS"],
        "leetcode": 102,
        "origin": "https://leetcode.cn/problems/binary-tree-level-order-traversal/",
        "why": "层序遍历 = 广度优先 BFS。用队列保存「当前层」的节点，每轮取出该层所有节点、收集值并把下一层入队，直到队列空。",
        "desc": """<p>给定二叉树根节点，返回其按<strong>层序</strong>遍历得到的节点值（即逐层从左到右访问）。</p>
<p><strong>示例：</strong><br><code>[3,9,20,null,null,15,7]</code> → <code>[[3],[9,20],[15,7]]</code></p>""",
        "frames": [
            frame("① 第一层只有根 3", "drawTree",
                  nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110}, {"val": "15", "x": 380, "y": 200}, {"val": "7", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
            frame("② 队列逐层处理：每层一次性取完", "drawStack",
                  items=[{"val": "3"}, {"val": "9"}, {"val": "20"}], type="queue", height=160),
            frame("③ 结果 [[3],[9,20],[15,7]]", "drawTable",
                  headers=["层", "值"],
                  rows=[["0", "3"], ["1", "9, 20"], ["2", "15, 7"]], width=420, height=160),
        ],
        "conclusion": "队列大小 = 当前层节点数，每次 for 一轮就是一层。",
        "py": """from collections import deque
def levelOrder(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):      # 当前层节点数
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res""",
        "java": """public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode n = q.poll();
            level.add(n.val);
            if (n.left != null) q.offer(n.left);
            if (n.right != null) q.offer(n.right);
        }
        res.add(level);
    }
    return res;
}""",
        "time": "O(n) — 每个节点入队出队一次",
        "space": "O(n) — 队列最大宽度",
        "pitfalls": [
            ("用 len(q) 固定层大小", "循环里队列在变，必须先用 size 记录当前层节点数，否则层边界会混"),
            ("空树返回 []", "root 为 None 直接返回空列表"),
        ],
        "selfcheck": [
            ("怎么按「之字形」遍历？", "在每层收集后根据奇偶层反转 level 即可，其余逻辑不变。"),
            ("DFS 能做层序吗？", "可以，递归时带上 depth 参数，把值追加到对应层的列表。"),
        ],
    },
    # ---------------------------------------------------------------- 49
    {
        "id": 49,
        "title": "二叉树的最大深度",
        "diff": "easy",
        "tags": ["树"],
        "leetcode": 104,
        "origin": "https://leetcode.cn/problems/maximum-depth-of-binary-tree/",
        "why": "树的最大深度 = 1 + max(左子树深度, 右子树深度)。递归自底向上求值，空节点深度为 0，一行即可。",
        "desc": """<p>给定二叉树，找出其<strong>最大深度</strong>。最大深度是从根节点到最远叶子节点的最长路径上的节点数。</p>
<p><strong>示例：</strong><br><code>[3,9,20,null,null,15,7]</code> → <code>3</code></p>""",
        "frames": [
            frame("① 深度 = 1 + max(左深, 右深)", "drawTree",
                  nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110}, {"val": "15", "x": 380, "y": 200, "highlight": "done"}, {"val": "7", "x": 500, "y": 200, "highlight": "done"}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
            frame("② 自底向上：叶子深 1，逐层 +1", "drawTable",
                  headers=["节点", "左深", "右深", "深度"],
                  rows=[["15", "0", "0", "1"], ["20", "1", "1", "2"], ["3", "1", "2", "3"]], width=460, height=170),
        ],
        "conclusion": "空节点深度 0，非空节点 = 左右子树较大者 + 1。",
        "py": """def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))""",
        "java": """public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}""",
        "time": "O(n)",
        "space": "O(h)",
        "pitfalls": [
            ("空节点返回 0", "否则空树会崩"),
            ("别和「最小深度」搞混", "最小深度还要处理单侧为空的情况，不是简单 min"),
        ],
        "selfcheck": [
            ("空树深度？", "0。"),
            ("一条链（退化链表）呢？", "深度就是节点个数 n，递归栈深度 O(n)。"),
        ],
    },
    # ---------------------------------------------------------------- 50
    {
        "id": 50,
        "title": "从前序与中序遍历构造二叉树",
        "diff": "medium",
        "tags": ["树"],
        "leetcode": 105,
        "origin": "https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/",
        "why": "前序的第一个元素必是根；在中序里找到根的位置，左边就是左子树、右边就是右子树。递归地切分两个序列，即可重建整棵树。",
        "desc": """<p>给定二叉树的前序遍历和中序遍历，构造并返回二叉树。假设树中没有重复元素。</p>
<p><strong>示例：</strong><br><code>preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]</code> → <code>[3,9,20,null,null,15,7]</code></p>""",
        "frames": [
            frame("① 前序第一个 3 是根，在中序里定位", "drawTable",
                  headers=["序列", "值"],
                  rows=[["preorder", "3,9,20,15,7"], ["inorder", "9,3,15,20,7"], ["根", "3"]], width=520, height=160),
            frame("② 中序里 3 左边 [9] 是左子树，右边 [15,20,7] 是右子树", "drawTable",
                  headers=["", "左子树", "根", "右子树"],
                  rows=[["inorder", "9", "3", "15,20,7"]], width=520, height=110),
            frame("③ 递归切分重建", "drawTree",
                  nodes=[{"val": "3", "x": 300, "y": 25}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110}, {"val": "15", "x": 380, "y": 200}, {"val": "7", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
        ],
        "conclusion": "根 → 中序定位 → 切出左右子树 → 递归，直到区间为空。",
        "py": """def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    def build(pl, pr, il, ir):
        if pl > pr:
            return None
        root = TreeNode(preorder[pl])
        k = idx[root.val]
        left_size = k - il
        root.left = build(pl + 1, pl + left_size, il, k - 1)
        root.right = build(pl + left_size + 1, pr, k + 1, ir)
        return root
    return build(0, len(preorder) - 1, 0, len(inorder) - 1)""",
        "java": """Map<Integer, Integer> idx = new HashMap<>();
public TreeNode buildTree(int[] pre, int[] in) {
    for (int i = 0; i < in.length; i++) idx.put(in[i], i);
    return build(pre, in, 0, pre.length - 1, 0, in.length - 1);
}
TreeNode build(int[] pre, int[] in, int pl, int pr, int il, int ir) {
    if (pl > pr) return null;
    TreeNode root = new TreeNode(pre[pl]);
    int k = idx.get(root.val), left = k - il;
    root.left = build(pre, in, pl + 1, pl + left, il, k - 1);
    root.right = build(pre, in, pl + left + 1, pr, k + 1, ir);
    return root;
}""",
        "time": "O(n) — 哈希定位根 O(1)，每节点一次",
        "space": "O(n) — 哈希表 + 递归栈",
        "pitfalls": [
            ("区间切分要对齐", "左子树大小 = k - il，前序里左子树区间是 pl+1 .. pl+left，算错一位全错"),
            ("用哈希加速定位", "每次线性 find 会退化成 O(n²)"),
        ],
        "selfcheck": [
            ("为什么前序+中序能唯一确定树？", "前序给根、中序给左右子树划分，层层递推唯一确定；只有前序+后序则不能唯一确定。"),
            ("树有重复元素呢？", "本题保证无重复；有重复则无法用哈希唯一定位根。"),
        ],
    },
    # ---------------------------------------------------------------- 51
    {
        "id": 51,
        "title": "将有序数组转换为二叉搜索树",
        "diff": "easy",
        "tags": ["BST"],
        "leetcode": 108,
        "origin": "https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/",
        "why": "要构造「高度平衡」的 BST，就每次取区间中点作为根，左半段建左子树、右半段建右子树，递归即可，天然平衡。",
        "desc": """<p>给定一个<strong>升序</strong>数组，将其转换为一棵<strong>高度平衡</strong>的二叉搜索树。高度平衡指每个节点左右子树高度差绝对值不超过 1。</p>
<p><strong>示例：</strong><br><code>[-10,-3,0,5,9]</code> → 一种答案为 <code>[0,-3,9,-10,null,5]</code></p>""",
        "frames": [
            frame("① 取中点 0 作根", "drawTable",
                  headers=["下标", "0", "1", "2", "3", "4"],
                  rows=[["数组", "-10", "-3", "0", "5", "9"], ["根", "", "", {"val": "0", "highlight": True}, "", ""]], width=500, height=130),
            frame("② 左半 [-10,-3] 中点 -3 作左根，右半 [5,9] 中点 5 作右根", "drawTree",
                  nodes=[{"val": "0", "x": 300, "y": 25}, {"val": "-3", "x": 160, "y": 110}, {"val": "5", "x": 440, "y": 110}, {"val": "-10", "x": 100, "y": 200}, {"val": "9", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
        ],
        "conclusion": "中点作根 + 左右递归，BST 有序性由数组有序性保证，平衡性由二分保证。",
        "py": """def sortedArrayToBST(nums):
    def build(l, r):
        if l > r:
            return None
        m = (l + r) // 2
        root = TreeNode(nums[m])
        root.left = build(l, m - 1)
        root.right = build(m + 1, r)
        return root
    return build(0, len(nums) - 1)""",
        "java": """public TreeNode sortedArrayToBST(int[] nums) {
    return build(nums, 0, nums.length - 1);
}
TreeNode build(int[] nums, int l, int r) {
    if (l > r) return null;
    int m = (l + r) >>> 1;
    TreeNode root = new TreeNode(nums[m]);
    root.left = build(nums, l, m - 1);
    root.right = build(nums, m + 1, r);
    return root;
}""",
        "time": "O(n) — 每个元素建一个节点",
        "space": "O(log n) — 递归栈（平衡树）",
        "pitfalls": [
            ("中点取整", "偶数长度取偏左或偏右都行，结果不唯一，都是合法平衡 BST"),
            ("递归边界", "l > r 表示区间空，返回 None；含等号时只剩一个节点"),
        ],
        "selfcheck": [
            ("答案唯一吗？", "不唯一。中点取 (l+r)//2 或 (l+r+1)//2 会得到不同但都合法的平衡 BST。"),
            ("为什么天然高度平衡？", "每次二分把区间对半切，左右子树规模最多差 1。"),
        ],
    },
    # ---------------------------------------------------------------- 52
    {
        "id": 52,
        "title": "二叉树展开为链表",
        "diff": "medium",
        "tags": ["树"],
        "leetcode": 114,
        "origin": "https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/",
        "why": "按「前序」的顺序把树展平成右链表。逆前序（右→左→根）遍历，用一个全局 prev 记录上一个访问节点，把当前节点右指针接到 prev、左指针置空即可，原地完成。",
        "desc": """<p>给定二叉树根节点，将其<strong>原地</strong>展开为单链表：展开后的链表顺序为前序遍历顺序，每个节点左指针为 null、右指针指向下一个节点。</p>
<p><strong>示例：</strong><br><code>[1,2,5,3,4,null,6]</code> → <code>[1,null,2,null,3,null,4,null,5,null,6]</code></p>""",
        "frames": [
            frame("① 原树：前序顺序 1→2→3→4→5→6", "drawTree",
                  nodes=[{"val": "1", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110}, {"val": "5", "x": 440, "y": 110}, {"val": "3", "x": 100, "y": 200}, {"val": "4", "x": 220, "y": 200}, {"val": "6", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
            frame("② 逆前序（右→左→根）串成右链", "drawLinkedList",
                  nodes=[{"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 5, "highlight": "done"}, {"val": 6, "highlight": "done"}], width=640, height=90),
        ],
        "conclusion": "逆前序保证「下一个该接的节点」已经处理完，prev 始终指向链表头部。",
        "py": """def flatten(root):
    prev = [None]
    def dfs(node):
        if not node:
            return
        dfs(node.right)     # 逆前序：右
        dfs(node.left)      # 左
        node.right = prev[0]  # 根：接上已串好的链表
        node.left = None
        prev[0] = node
    dfs(root)""",
        "java": """TreeNode prev = null;
public void flatten(TreeNode root) {
    if (root == null) return;
    flatten(root.right);
    flatten(root.left);
    root.right = prev;
    root.left = null;
    prev = root;
}""",
        "time": "O(n)",
        "space": "O(h) — 递归栈",
        "pitfalls": [
            ("左指针置空", "展平后每个节点 left 必须是 null，漏掉会残留旧结构"),
            ("先右后左", "逆前序顺序是 右→左→根，顺序错了链表次序不对"),
        ],
        "selfcheck": [
            ("为什么用逆前序而不是前序？", "前序先访问根时，它的右子树还没处理，根无法指向「已串好的后续」；逆序则保证后续已就绪。"),
            ("O(1) 额外空间做法？", "用「找左子树最右节点，把右子树挂过去」的原地拼接，可避免递归栈。"),
        ],
    },
    # ---------------------------------------------------------------- 53
    {
        "id": 53,
        "title": "杨辉三角",
        "diff": "easy",
        "tags": ["DP"],
        "leetcode": 118,
        "origin": "https://leetcode.cn/problems/pascals-triangle/",
        "why": "每行首尾是 1，中间每个数 = 上一行相邻两数之和。逐行生成即可，是典型的递推填表。",
        "desc": """<p>给定非负整数 <code>numRows</code>，生成杨辉三角的前 numRows 行。杨辉三角中每个数是它左上方和右上方的数之和。</p>
<p><strong>示例：</strong><br><code>numRows=5</code> → <code>[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]</code></p>""",
        "frames": [
            frame("① 每行首尾 1，中间 = 左上 + 右上", "drawTable",
                  headers=["行", "内容"],
                  rows=[["0", "1"], ["1", "1, 1"], ["2", "1, 2, 1"], ["3", "1, 3, 3, 1"], ["4", "1, 4, 6, 4, 1"]], width=460, height=230),
            frame("② 递推：cur[j] = prev[j-1] + prev[j]", "drawTable",
                  headers=["j", "0", "1", "2", "3", "4"],
                  rows=[["上一行", "1", "3", "3", "1", ""], ["本行", "1", {"val": "4", "highlight": True}, "6", "4", "1"]], width=460, height=140),
        ],
        "conclusion": "一行一行填，中间元素由上一行相邻两项相加得到。",
        "py": """def generate(numRows):
    res = []
    for i in range(numRows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = res[-1][j - 1] + res[-1][j]
        res.append(row)
    return res""",
        "java": """public List<List<Integer>> generate(int numRows) {
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < numRows; i++) {
        List<Integer> row = new ArrayList<>();
        for (int j = 0; j <= i; j++) {
            if (j == 0 || j == i) row.add(1);
            else row.add(res.get(i - 1).get(j - 1) + res.get(i - 1).get(j));
        }
        res.add(row);
    }
    return res;
}""",
        "time": "O(numRows²)",
        "space": "O(numRows²) — 结果本身",
        "pitfalls": [
            ("首尾处理", "j==0 或 j==i 时固定为 1，中间才相加"),
            ("用上一行", "本行依赖 res[-1]，确保上一行已生成"),
        ],
        "selfcheck": [
            ("numRows=0？", "返回空列表。"),
            ("第 n 行第 k 个数与组合数的关系？", "等于 C(n,k)，杨辉三角本质就是二项式系数的递推。"),
        ],
    },
    # ---------------------------------------------------------------- 54
    {
        "id": 54,
        "title": "买卖股票的最佳时机",
        "diff": "easy",
        "tags": ["贪心"],
        "leetcode": 121,
        "origin": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/",
        "why": "只能买卖一次。遍历时维护「到今天为止的最低买入价」min_price，每天用当前价减去最低价更新最大利润。一次遍历 O(n)。",
        "desc": """<p>给定数组 <code>prices</code>，第 i 个元素表示股票第 i 天的价格。你只能选择<strong>某一天买入</strong>并在未来某一天卖出，求能获得的最大利润；不能获利则返回 0。</p>
<p><strong>示例：</strong><br><code>[7,1,5,3,6,4]</code> → <code>5</code>（第 2 天 1 买入，第 5 天 6 卖出）</p>""",
        "frames": [
            frame("① 维护历史最低价 min_price", "drawTwoPointers", arr=[7, 1, 5, 3, 6, 4], left=1, right=4, window={"start": 1, "end": 4}, width=560, height=150),
            frame("② 每天利润 = 当天价 - min_price，取最大", "drawTable",
                  headers=["天", "0", "1", "2", "3", "4", "5"],
                  rows=[["价格", "7", "1", "5", "3", "6", "4"], ["最低", "7", "1", "1", "1", "1", "1"], ["利润", "0", "0", "4", "2", "5", "3"]], width=620, height=160),
            frame("③ 最大利润 = 5", "drawTwoPointers", arr=[7, 1, 5, 3, 6, 4], left=1, right=4, window={"start": 1, "end": 4}, width=560, height=150),
        ],
        "conclusion": "最低价只降不升，每天算一次「当前能赚多少」，全局取最大。",
        "py": """def maxProfit(prices):
    min_price = float('inf')
    ans = 0
    for p in prices:
        min_price = min(min_price, p)
        ans = max(ans, p - min_price)
    return ans""",
        "java": """public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, ans = 0;
    for (int p : prices) {
        minPrice = Math.min(minPrice, p);
        ans = Math.max(ans, p - minPrice);
    }
    return ans;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("先更新 min 再算利润", "先 min 后 ans，保证「同一天不买卖」的语义；顺序反过来不影响结果但含义易混"),
            ("不能获利返回 0", "价格一路下跌时 ans 保持 0"),
        ],
        "selfcheck": [
            ("为什么贪心是对的？", "最大利润的卖出日固定时，买入价应取它之前的历史最低；遍历时 min_price 恰好维护了这一点。"),
            ("可以买卖多次呢？", "那就是 122 题，把每段「上涨」的差价累加即可。"),
        ],
    },
    # ---------------------------------------------------------------- 55
    {
        "id": 55,
        "title": "二叉树中的最大路径和",
        "diff": "hard",
        "tags": ["树"],
        "leetcode": 124,
        "origin": "https://leetcode.cn/problems/binary-tree-maximum-path-sum/",
        "why": "路径可以不过根、只走一部分。递归时每个节点返回「以它为起点向下延伸的最大单边和」，同时用「左单边 + 自己 + 右单边」更新全局最大，负数边直接舍弃。",
        "desc": """<p>二叉树中的路径，是任意节点间、每个节点至多经过一次的序列。路径和是路径上节点值的总和。返回所有路径中的最大路径和。</p>
<p><strong>示例：</strong><br><code>[1,2,3]</code> → <code>6</code>（2→1→3）；<code>[-10,9,20,null,null,15,7]</code> → <code>42</code>（15→20→7）</p>""",
        "frames": [
            frame("① 每个节点返回「向下最大单边和」", "drawTree",
                  nodes=[{"val": "-10", "x": 300, "y": 25}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110, "highlight": "active"}, {"val": "15", "x": 380, "y": 200, "highlight": "done"}, {"val": "7", "x": 500, "y": 200, "highlight": "done"}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
            frame("② 20 的左右单边 15、7 都为正，弯折路径 15+20+7=42", "drawTable",
                  headers=["节点", "左单边", "右单边", "弯折和"],
                  rows=[["20", "15", "7", {"val": "42", "highlight": True}], ["-10", "9", "35", "34"]], width=500, height=140),
        ],
        "conclusion": "单边和 = max(0, 左单边) + max(0, 右单边) + 自身 更新答案；返回值只取较大一侧 + 自身。",
        "py": """def maxPathSum(root):
    ans = [float('-inf')]
    def dfs(node):
        if not node:
            return 0
        left = max(dfs(node.left), 0)    # 负边舍弃
        right = max(dfs(node.right), 0)
        ans[0] = max(ans[0], left + right + node.val)  # 弯折路径
        return max(left, right) + node.val             # 向上单边
    dfs(root)
    return ans[0]""",
        "java": """int ans = Integer.MIN_VALUE;
public int maxPathSum(TreeNode root) {
    dfs(root);
    return ans;
}
int dfs(TreeNode n) {
    if (n == null) return 0;
    int l = Math.max(dfs(n.left), 0);
    int r = Math.max(dfs(n.right), 0);
    ans = Math.max(ans, l + r + n.val);
    return Math.max(l, r) + n.val;
}""",
        "time": "O(n)",
        "space": "O(h)",
        "pitfalls": [
            ("负贡献舍弃", "单边和与 0 取 max，负子树直接不选"),
            ("返回值与答案分开", "返回「单边」给父节点用，答案用「弯折」更新，二者不能混"),
        ],
        "selfcheck": [
            ("全负节点怎么办？", "单边都被 0 截断，答案最终取到最大的那个负节点值（如 -3 是最大值）。"),
            ("路径一定要经过根吗？", "不一定。答案是全局任意路径，这正是递归要在每个节点都更新 ans 的原因。"),
        ],
    },
]

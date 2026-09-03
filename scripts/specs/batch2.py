from scripts.algo_gen import frame


PROBLEMS = [
    # ---------------------------------------------------------------- 26
    {
        "id": 26,
        "title": "全排列",
        "diff": "medium",
        "tags": ["回溯"],
        "leetcode": 46,
        "origin": "https://leetcode.cn/problems/permutations/",
        "why": "全排列是「每个位置选一个没用过的数」的决策树。回溯用 used 标记已选，选完 n 个就收集，再撤销选择换下一个，穷举所有顺序。",
        "desc": """<p>给定一个<strong>不含重复数字</strong>的数组 <code>nums</code>，返回其所有可能的全排列，可以按任意顺序返回。</p>
<p><strong>示例：</strong><br><code>nums=[1,2,3]</code> → <code>[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]</code></p>""",
        "frames": [
            frame("① 决策树：每层固定一个位置，选一个未用过的数", "drawBacktrack",
                  nodes=[{"val": "[]", "x": 300, "y": 15, "color": "normal"},
                         {"val": "[1]", "x": 90, "y": 85, "color": "path"}, {"val": "[2]", "x": 300, "y": 85, "color": "path"}, {"val": "[3]", "x": 510, "y": 85, "color": "path"},
                         {"val": "[1,2]", "x": 40, "y": 160, "color": "path"}, {"val": "[1,3]", "x": 140, "y": 160, "color": "path"},
                         {"val": "[1,2,3]", "x": 40, "y": 240, "color": "path"}, {"val": "[1,3,2]", "x": 140, "y": 240, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 90, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 300, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 510, "y2": 85, "color": "path"},
                         {"x1": 90, "y1": 85, "x2": 40, "y2": 160, "color": "path"}, {"x1": 90, "y1": 85, "x2": 140, "y2": 160, "color": "path"},
                         {"x1": 40, "y1": 160, "x2": 40, "y2": 240, "color": "path"}, {"x1": 140, "y1": 160, "x2": 140, "y2": 240, "color": "path"}],
                  width=580, height=280),
            frame("② 用 used 数组标记，避免同一个数重复选", "drawTable",
                  headers=["数字", "1", "2", "3"],
                  rows=[["used", "false", "false", "false"], ["选 1 后", {"val": "true", "highlight": True}, "false", "false"]], width=520, height=140),
        ],
        "conclusion": "每层从「未使用」的数里挑一个放进去，到底就收集并回溯，换下一个候选。",
        "py": """def permute(nums):
    ans = []
    n = len(nums)
    used = [False] * n
    def dfs(path):
        if len(path) == n:
            ans.append(path[:]); return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs(path)
            path.pop()
            used[i] = False
    dfs([])
    return ans""",
        "java": """public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> ans = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    dfs(nums, used, new ArrayList<>(), ans);
    return ans;
}
void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> ans) {
    if (path.size() == nums.length) { ans.add(new ArrayList<>(path)); return; }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true; path.add(nums[i]);
        dfs(nums, used, path, ans);
        path.remove(path.size() - 1); used[i] = false;
    }
}""",
        "time": "O(n · n!) — n! 个排列，每个复制一次",
        "space": "O(n) — 递归栈 + used 数组",
        "pitfalls": [
            ("回溯要同时撤销 used 和 path", "两者都要还原，否则同一分支残留会漏排列或产生重复"),
            ("收集时要 path[:] 拷贝", "path 是可变对象且后续会被修改，不拷贝会导致 ans 里全是同一个引用"),
        ],
        "selfcheck": [
            ("nums 有重复数字怎么办？", "这是「全排列 II」，需先排序再在循环里跳过「同级重复」（nums[i]==nums[i-1] 且 used[i-1] 为 false），否则会产生重复排列。"),
            ("为什么交换法也能做？", "固定第一个位置与后面逐个交换，再递归处理剩余部分；两种写法都基于「每个位置放一个数」的思想。"),
        ],
    },
    # ---------------------------------------------------------------- 27
    {
        "id": 27,
        "title": "旋转图像",
        "diff": "medium",
        "tags": ["数组"],
        "leetcode": 48,
        "origin": "https://leetcode.cn/problems/rotate-image/",
        "why": "顺时针旋转 90° 可以拆成两个简单操作：先沿主对角线翻转，再左右翻转。每步都有明确的坐标对应关系，原地完成，不需要额外矩阵。",
        "desc": """<p>给定一个 <code>n × n</code> 的二维矩阵表示图像，将其<strong>原地</strong>顺时针旋转 90 度。</p>
<p><strong>示例：</strong><br><code>[[1,2,3],[4,5,6],[7,8,9]]</code> → <code>[[7,4,1],[8,5,2],[9,6,3]]</code></p>""",
        "frames": [
            frame("① 原矩阵", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "1", "2", "3"], ["1", "4", "5", "6"], ["2", "7", "8", "9"]], width=420, height=170),
            frame("② 沿主对角线翻转（matrix[i][j] ↔ matrix[j][i]）", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "1", "4", "7"], ["1", {"val": "2", "highlight": True}, "5", "8"], ["2", {"val": "3", "highlight": True}, "6", "9"]], width=420, height=170),
            frame("③ 左右翻转 → 旋转结果", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "7", "4", "1"], ["1", "8", "5", "2"], ["2", "9", "6", "3"]], width=420, height=170),
        ],
        "conclusion": "先对角线翻转，再左右翻转，两步叠加正好等于顺时针 90°。",
        "py": """def rotate(matrix):
    n = len(matrix)
    for i in range(n):              # 主对角线翻转
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for i in range(n):              # 左右翻转
        matrix[i].reverse()""",
        "java": """public void rotate(int[][] matrix) {
    int n = matrix.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int t = matrix[i][j]; matrix[i][j] = matrix[j][i]; matrix[j][i] = t;
        }
    for (int i = 0; i < n; i++) {
        int l = 0, r = n - 1;
        while (l < r) { int t = matrix[i][l]; matrix[i][l] = matrix[i][r]; matrix[i][r] = t; l++; r--; }
    }
}""",
        "time": "O(n²) — 每个元素处理常数次",
        "space": "O(1) — 原地",
        "pitfalls": [
            ("对角线翻转只遍历上三角", "j 从 i+1 开始，否则交换两次等于没换"),
            ("逆时针要换顺序", "逆时针 90° 是先左右翻转再对角线翻转，方向别弄反"),
        ],
        "selfcheck": [
            ("为什么两步叠加等于旋转 90°？", "对角线翻转把 (i,j) 映到 (j,i)，左右翻转再把列镜像为 n-1-j，最终 (i,j)→(j,n-1-i)，正是顺时针 90° 的坐标变换。"),
            ("能否一次循环直接旋转？", "可以，按「一圈一圈」处理四个角的值循环交换，但两步分解更直观、不易错。"),
        ],
    },
    # ---------------------------------------------------------------- 28
    {
        "id": 28,
        "title": "字母异位词分组",
        "diff": "medium",
        "tags": ["哈希表"],
        "leetcode": 49,
        "origin": "https://leetcode.cn/problems/group-anagrams/",
        "why": "互为字母异位词的单词，排序后完全相同。把「排序后的串」作为 key 分组，每个单词 O(k log k) 排序 + O(1) 查表，即可把所有变位词归到一起。",
        "desc": """<p>给定一个字符串数组，将所有字母异位词组合在一起。字母异位词指由相同字母、相同个数重新排列得到的字符串。</p>
<p><strong>示例：</strong><br><code>["eat","tea","tan","ate","nat","bat"]</code> → <code>[["eat","tea","ate"],["tan","nat"],["bat"]]</code></p>""",
        "frames": [
            frame("① 每个词排序，作为分组 key", "drawTable",
                  headers=["单词", "排序后 key"],
                  rows=[["eat", "aet"], ["tea", "aet"], ["tan", "ant"], ["ate", "aet"], ["nat", "ant"], ["bat", "abt"]], width=460, height=240),
            frame("② key 相同归入同一组", "drawTable",
                  headers=["key", "组内单词"],
                  rows=[["aet", "eat, tea, ate"], ["ant", "tan, nat"], ["abt", "bat"]], width=460, height=170),
        ],
        "conclusion": "排序串就是变位词的「指纹」，同指纹的单词天然属于同一组。",
        "py": """from collections import defaultdict
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())""",
        "java": """public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        char[] a = s.toCharArray();
        Arrays.sort(a);
        String key = new String(a);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}""",
        "time": "O(n · k log k) — n 个词，每个长度 k 排序",
        "space": "O(n · k) — 存储所有字符串",
        "pitfalls": [
            ("key 要用排序后的完整串", "不能只统计字母出现次数但不排序（那样要自定义可哈希 key），排序串最简单直观"),
            ("返回形式", "只需返回分组后的列表，组内与组间顺序都无所谓"),
        ],
        "selfcheck": [
            ("能否用字母计数代替排序？", "可以，用 26 位计数数组转成不可变 key（如元组），时间可降到 O(nk)，但实现略繁，排序法更直观。"),
            ("\"\"（空串）和单字母词怎么处理？", "空串排序后仍为空串 key；单字母词各自成组，逻辑自然覆盖。"),
        ],
    },
    # ---------------------------------------------------------------- 29
    {
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
            frame("① 按行放置，用三个集合记录被占的列/斜线", "drawTable",
                  headers=["", "0", "1", "2", "3"],
                  rows=[["0", "·", "Q", "·", "·"], ["1", "·", "·", "·", "Q"], ["2", "Q", "·", "·", "·"], ["3", "·", "·", "Q", "·"]], width=420, height=190),
            frame("② 斜线编号：主对角线 = row - col，副对角线 = row + col", "drawTable",
                  headers=["位置", "r-c", "r+c"],
                  rows=[["(0,1)", "-1", "1"], ["(1,3)", "-2", "4"], ["(2,0)", "2", "2"]], width=460, height=170),
            frame("③ 冲突就回溯，尝试下一列", "drawBacktrack",
                  nodes=[{"val": "第0行", "x": 300, "y": 15, "color": "normal"},
                         {"val": "列1 ✓", "x": 150, "y": 85, "color": "path"}, {"val": "列0 ✓", "x": 450, "y": 85, "color": "path"},
                         {"val": "第1行列0 ✗", "x": 100, "y": 165, "color": "pruned"}, {"val": "第1行列2 ✓", "x": 210, "y": 165, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 150, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 450, "y2": 85, "color": "path"},
                         {"x1": 150, "y1": 85, "x2": 100, "y2": 165, "color": "pruned"}, {"x1": 150, "y1": 85, "x2": 210, "y2": 165, "color": "path"}],
                  width=580, height=210),
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
        "pitfalls": [
            ("斜线判重用集合/数组", "主对角线 r-c（可能为负，Java 需 +n 偏移），副对角线 r+c，两套都要查"),
            ("回溯要撤销", "三个判重集合与棋盘都要在递归返回后恢复，否则影响兄弟分支"),
        ],
        "selfcheck": [
            ("n=1 有解吗？", "有，只有 [\"Q\"] 一个解。n=2、n=3 无解，n=4 有 2 解。"),
            ("为什么按行放而不是任意放？", "任意放会有 n² 个格子可选，状态爆炸；按行放保证每行一个皇后，天然满足行互斥，状态降到 n^n 且配合列/斜线剪枝。"),
        ],
    },
    # ---------------------------------------------------------------- 30
    {
        "id": 30,
        "title": "最大子数组和",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 53,
        "origin": "https://leetcode.cn/problems/maximum-subarray/",
        "why": "Kadane 算法：以 i 结尾的最大子数组和，要么接着前面的（pre + x），要么另起炉灶（x）。每步取较大者，同时更新全局最大，一次遍历 O(n)。",
        "desc": """<p>给定一个整数数组，找出一个具有<strong>最大和</strong>的连续子数组，返回其最大和。</p>
<p><strong>示例：</strong><br><code>[-2,1,-3,4,-1,2,1,-5,4]</code> → <code>6</code>（子数组 <code>[4,-1,2,1]</code>）</p>""",
        "frames": [
            frame("① 到 i 为止：接前面 or 另起", "drawTwoPointers", arr=[-2, 1, -3, 4, -1, 2, 1, -5, 4], left=3, right=6, window={"start": 3, "end": 6}, width=720, height=140),
            frame("② 递推：dp[i] = max(dp[i-1]+x, x)", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8"],
                  rows=[["nums", "-2", "1", "-3", "4", "-1", "2", "1", "-5", "4"], ["dp", "-2", "1", "-2", "4", "3", "5", "6", "1", "5"]], width=760, height=150),
            frame("③ 全局最大 = max(dp) = 6", "drawTwoPointers", arr=[-2, 1, -3, 4, -1, 2, 1, -5, 4], left=3, right=6, window={"start": 3, "end": 6}, width=720, height=140),
        ],
        "conclusion": "「当前子数组和」一旦变负就果断丢弃、重新开始，过程中记录到的最大值就是答案。",
        "py": """def maxSubArray(nums):
    cur = ans = nums[0]
    for x in nums[1:]:
        cur = max(cur + x, x)   # 接前面 或 另起
        ans = max(ans, cur)
    return ans""",
        "java": """public int maxSubArray(int[] nums) {
    int cur = nums[0], ans = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(cur + nums[i], nums[i]);
        ans = Math.max(ans, cur);
    }
    return ans;
}""",
        "time": "O(n) — 一次遍历",
        "space": "O(1) — 只维护两个变量",
        "pitfalls": [
            ("全负数组", "cur 初始化为 nums[0] 并逐个比较，仍能返回最大的那个负数"),
            ("cur 变负要丢弃", "cur+x < x 时说明前面是累赘，应另起炉灶，这是 Kadane 的核心"),
        ],
        "selfcheck": [
            ("全负数组 [-2,-3,-1] 答案？", "-1。每步 cur 都会重置为当前更大的值，ans 保持 -1。"),
            ("需要记录子数组下标吗？", "本题只求最大和；若要下标，可在 cur 重置时记录起点，更新 ans 时记录终点。"),
        ],
    },
    # ---------------------------------------------------------------- 31
    {
        "id": 31,
        "title": "跳跃游戏",
        "diff": "medium",
        "tags": ["贪心"],
        "leetcode": 55,
        "origin": "https://leetcode.cn/problems/jump-game/",
        "why": "只要「能到达的最远下标」不断推进并最终 ≥ 末尾，就一定可达。贪心维护 farthest，比 DP 更简单，O(n) 即可。",
        "desc": """<p>给定非负整数数组 <code>nums</code>，最初位于第一个下标。每个元素表示在该位置可跳跃的最大长度。判断能否到达最后一个下标。</p>
<p><strong>示例：</strong><br><code>[2,3,1,1,4]</code> → <code>true</code><br><code>[3,2,1,0,4]</code> → <code>false</code></p>""",
        "frames": [
            frame("① 从 0 跳最远到 2", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=0, right=2, width=520, height=140),
            frame("② 途中更新最远：1→2、2→4、3→4", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=2, right=4, window={"start": 0, "end": 2}, width=520, height=140),
            frame("③ farthest=4 覆盖末尾 → 可达", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=4, right=4, window={"start": 0, "end": 4}, width=520, height=140),
        ],
        "conclusion": "只要当前位置还在「最远可达」范围内，就不断把最远可达向前推进；越过末尾即成功。",
        "py": """def canJump(nums):
    farthest = 0
    for i, x in enumerate(nums):
        if i > farthest:      # 当前位置都到不了
            return False
        farthest = max(farthest, i + x)
        if farthest >= len(nums) - 1:
            return True
    return True""",
        "java": """public boolean canJump(int[] nums) {
    int farthest = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > farthest) return false;
        farthest = Math.max(farthest, i + nums[i]);
        if (farthest >= nums.length - 1) return true;
    }
    return true;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("i > farthest 判不可达", "中间一旦出现「当前位置已超出最远可达」，后面全是死区，直接返回 false"),
            ("提前返回 true", "farthest >= n-1 即可提前结束，不用遍历到底"),
        ],
        "selfcheck": [
            ("[3,2,1,0,4] 为什么 false？", "最远只能到 3，而 nums[3]=0 无法前进到 4，卡死在 0。"),
            ("和「跳跃游戏 II」区别？", "I 只判断可达性（贪心维护 farthest）；II 求最少步数（需维护当前步边界 end）。"),
        ],
    },
    # ---------------------------------------------------------------- 32
    {
        "id": 32,
        "title": "合并区间",
        "diff": "medium",
        "tags": ["排序"],
        "leetcode": 56,
        "origin": "https://leetcode.cn/problems/merge-intervals/",
        "why": "先按左端点排序，重叠的区间在排序后必然相邻。一次遍历：当前区间与结果栈顶有重叠就扩展右端点，否则作为新区间入栈。",
        "desc": """<p>以数组 <code>intervals</code> 表示若干个区间的集合，其中 <code>intervals[i] = [start, end]</code>。合并所有重叠的区间，返回一个不重叠的区间数组。</p>
<p><strong>示例：</strong><br><code>[[1,3],[2,6],[8,10],[15,18]]</code> → <code>[[1,6],[8,10],[15,18]]</code></p>""",
        "frames": [
            frame("① 按左端点排序", "drawTable",
                  headers=["区间", "1", "2", "3", "4"],
                  rows=[["排序前", "[1,3]", "[2,6]", "[8,10]", "[15,18]"], ["排序后", "[1,3]", "[2,6]", "[8,10]", "[15,18]"]], width=520, height=150),
            frame("② [1,3] 与 [2,6] 重叠 → 合并为 [1,6]", "drawTable",
                  headers=["结果", "0", "1", "2"],
                  rows=[["合并后", {"val": "[1,6]", "highlight": True}, "[8,10]", "[15,18]"]], width=520, height=120),
            frame("③ [8,10] 与 [15,18] 不重叠，各自保留", "drawTable",
                  headers=["结果", "0", "1", "2"],
                  rows=[["最终", "[1,6]", "[8,10]", "[15,18]"]], width=520, height=120),
        ],
        "conclusion": "排序让「可能重叠的区间」相邻，合并判断只看当前区间与已合并区间的右端点。",
        "py": """def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for iv in intervals:
        if not res or res[-1][1] < iv[0]:
            res.append(iv)              # 无重叠
        else:
            res[-1][1] = max(res[-1][1], iv[1])  # 扩展右端点
    return res""",
        "java": """public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> res = new ArrayList<>();
    for (int[] iv : intervals) {
        if (res.isEmpty() || res.get(res.size() - 1)[1] < iv[0]) res.add(iv);
        else res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], iv[1]);
    }
    return res.toArray(new int[0][]);
}""",
        "time": "O(n log n) — 排序主导",
        "space": "O(n) — 结果数组",
        "pitfalls": [
            ("重叠判断", "res[-1][1] >= iv[0] 即重叠（含端点相接），右端点取 max 而非直接覆盖"),
            ("必须先排序", "不排序的话重叠区间不相邻，线性合并会漏并"),
        ],
        "selfcheck": [
            ("[1,4] 与 [4,5] 算重叠吗？", "算。4 相接，合并为 [1,5]，因为 res[-1][1] >= iv[0] 成立。"),
            ("区间完全被包含如 [1,4] 与 [2,3]？", "右端点取 max(4,3)=4，结果仍是 [1,4]，被包含的区间自然吸收。"),
        ],
    },
    # ---------------------------------------------------------------- 33
    {
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
            frame("① 第一行第一列都只有 1 条路径", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "1", "1", "1"], ["1", "1", {"val": "2", "highlight": True}, "3"], ["2", "1", "3", {"val": "6", "highlight": True}]], width=420, height=170),
            frame("② dp[i][j] = dp[i-1][j] + dp[i][j-1]", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "1", "1", "1"], ["1", "1", "2", "3"], ["2", "1", "3", "6"]], width=420, height=170),
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
        "pitfalls": [
            ("初始化边界", "第一行与第一列全是 1，不能漏"),
            ("递推方向", "只能从左上到右下，保证 dp[i-1][j]、dp[i][j-1] 已算好"),
        ],
        "selfcheck": [
            ("m=1 或 n=1？", "只有一行或一列时只有一条路径，返回 1，初始化已覆盖。"),
            ("如何优化空间？", "dp 只依赖上一行和当前行左侧，用一维数组 dp[j] += dp[j-1] 即可 O(n) 空间。"),
        ],
    },
    # ---------------------------------------------------------------- 34
    {
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
            frame("① 原网格", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "1", "3", "1"], ["1", "1", "5", "1"], ["2", "4", "2", "1"]], width=420, height=170),
            frame("② dp 表：每格 = 自己 + min(上, 左)", "drawTable",
                  headers=["", "0", "1", "2"],
                  rows=[["0", "1", "4", "5"], ["1", "2", "7", "6"], ["2", "6", "8", {"val": "7", "highlight": True}]], width=420, height=170),
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
        "pitfalls": [
            ("边界累加", "第一行只能从左边来，第一列只能从上面来，要单独处理"),
            ("不能贪心", "局部选最小的格子不能保证全局最小，必须 DP 比较两条来路"),
        ],
        "selfcheck": [
            ("为什么不能每步都往较小数字走？", "贪心可能走进「当前小但后面大」的死胡同；DP 保证每个格子都取到「到它为止」的全局最小，最终必最优。"),
            ("有负数会怎样？", "本题保证非负；若含负数，DP 仍正确（只是路径和可为负），但「到终点最小」定义不变。"),
        ],
    },
    # ---------------------------------------------------------------- 35
    {
        "id": 35,
        "title": "爬楼梯",
        "diff": "easy",
        "tags": ["DP"],
        "leetcode": 70,
        "origin": "https://leetcode.cn/problems/climbing-stairs/",
        "why": "到第 n 阶，最后一步要么跨 1 阶、要么跨 2 阶，所以 f(n) = f(n-1) + f(n-2)，就是斐波那契数列。用两个变量滚动即可 O(1) 空间。",
        "desc": """<p>假设你正在爬楼梯，需要 n 阶到达楼顶。每次可以爬 1 或 2 个台阶，问有多少种不同方法爬到楼顶。</p>
<p><strong>示例：</strong><br><code>n=2</code> → <code>2</code>（1+1、2）；<code>n=3</code> → <code>3</code>（1+1+1、1+2、2+1）</p>""",
        "frames": [
            frame("① 递推：f(n)=f(n-1)+f(n-2)", "drawTable",
                  headers=["n", "0", "1", "2", "3", "4", "5"],
                  rows=[["方法数", "1", "1", "2", "3", "5", "8"]], width=560, height=120),
            frame("② 第 n 阶来自「跨 1」或「跨 2」两种来路", "drawBacktrack",
                  nodes=[{"val": "n", "x": 300, "y": 15, "color": "normal"}, {"val": "n-1", "x": 200, "y": 90, "color": "path"}, {"val": "n-2", "x": 400, "y": 90, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 200, "y2": 90, "color": "path"}, {"x1": 300, "y1": 15, "x2": 400, "y2": 90, "color": "path"}],
                  width=520, height=150),
        ],
        "conclusion": "斐波那契数列，滚动两个变量不断前移。",
        "py": """def climbStairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a""",
        "java": """public int climbStairs(int n) {
    int a = 1, b = 1;
    for (int i = 0; i < n; i++) {
        int t = a + b;
        a = b; b = t;
    }
    return a;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("边界 f(0)=1", "把 f(0) 定义为 1 能让递推统一，n=1 返回 1"),
            ("别用朴素递归", "朴素递归是指数级；记忆化或迭代才是线性"),
        ],
        "selfcheck": [
            ("n=0 或 n=1？", "约定 f(0)=1、f(1)=1，代码里 a 初始 1 直接覆盖。"),
            ("如果一次能爬 1~3 阶呢？", "递推改为 f(n)=f(n-1)+f(n-2)+f(n-3)，滚动维护三个变量即可。"),
        ],
    },
    # ---------------------------------------------------------------- 36
    {
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
            frame("① dp[i][j]：word1 前 i 个 → word2 前 j 个的最少操作", "drawTable",
                  headers=["", "", "r", "o", "s"],
                  rows=[["", "0", "1", "2", "3"], ["h", "1", "1", "2", "3"], ["o", "2", "2", "1", "2"], ["r", "3", "2", "2", "2"], ["s", "4", "3", "3", "2"], ["e", "5", "4", "4", {"val": "3", "highlight": True}]], width=440, height=260),
            frame("② 三选一：插入 dp[i][j-1]+1、删除 dp[i-1][j]+1、替换 dp[i-1][j-1]+1", "drawTable",
                  headers=["操作", "来自", "代价"],
                  rows=[["插入", "dp[i][j-1]", "+1"], ["删除", "dp[i-1][j]", "+1"], ["替换", "dp[i-1][j-1]", "相等则 +0"]], width=460, height=170),
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
        "pitfalls": [
            ("三选一别漏", "插入、删除、替换对应三个方向，忘掉任何一个都会高估操作数"),
            ("相等直接继承", "word1[i-1]==word2[j-1] 时 dp[i][j]=dp[i-1][j-1]，不用 +1"),
        ],
        "selfcheck": [
            ("两个空串？", "m=n=0，dp[0][0]=0，返回 0。"),
            ("「horse」→「ros」为何是 3 步？", "h→r 替换(1)、删 e(1)、替换 s→? 实际路径：删 h、r 不变、o 不变、r→s? 对照 dp 表右下角即 3，具体路径可用回溯 dp 表还原。"),
        ],
    },
    # ---------------------------------------------------------------- 37
    {
        "id": 37,
        "title": "搜索二维矩阵",
        "diff": "medium",
        "tags": ["二分"],
        "leetcode": 74,
        "origin": "https://leetcode.cn/problems/search-a-2d-matrix/",
        "why": "矩阵每行升序且下一行首元素大于上一行末元素，把它「拍平」就是一个整体有序数组，直接对总长度做二分，下标换算成 (row, col)。",
        "desc": """<p>编写一个高效算法，判断 m×n 矩阵中是否存在目标值。矩阵特性：每行从左到右升序，且每行的第一个整数大于前一行的最后一个整数。</p>
<p><strong>示例：</strong><br><code>[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3</code> → <code>true</code></p>""",
        "frames": [
            frame("① 拍平成有序数组 [1,3,5,7,10,11,16,20,23,30,34,60]", "drawTable",
                  headers=["", "0", "1", "2", "3"],
                  rows=[["0", "1", "3", "5", "7"], ["1", "10", "11", "16", "20"], ["2", "23", "30", "34", "60"]], width=420, height=170),
            frame("② 整体二分，mid 换算成 (mid//n, mid%n)", "drawBinarySearch", arr=[1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60], left=0, mid=5, right=11, width=720, height=140),
        ],
        "conclusion": "把二维坐标映射到一维下标，标准二分直接复用。",
        "py": """def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    l, r = 0, m * n - 1
    while l <= r:
        mid = (l + r) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        if val < target:
            l = mid + 1
        else:
            r = mid - 1
    return False""",
        "java": """public boolean searchMatrix(int[][] matrix, int target) {
    int m = matrix.length, n = matrix[0].length;
    int l = 0, r = m * n - 1;
    while (l <= r) {
        int mid = (l + r) >>> 1;
        int val = matrix[mid / n][mid % n];
        if (val == target) return true;
        if (val < target) l = mid + 1; else r = mid - 1;
    }
    return false;
}""",
        "time": "O(log(m·n))",
        "space": "O(1)",
        "pitfalls": [
            ("下标换算", "row = mid // n，col = mid % n，行列别写反"),
            ("前提是整体有序", "本题特殊性质保证拍平有序；普通「每行每列升序」的矩阵要用不同的搜索方式（见搜索二维矩阵 II）"),
        ],
        "selfcheck": [
            ("target 比所有元素都大/小？", "二分区间自然收缩到 l > r，返回 False。"),
            ("m=1 时？", "退化为普通一维二分，mid//n=0 恒成立。"),
        ],
    },
    # ---------------------------------------------------------------- 38
    {
        "id": 38,
        "title": "颜色分类",
        "diff": "medium",
        "tags": ["双指针"],
        "leetcode": 75,
        "origin": "https://leetcode.cn/problems/sort-colors/",
        "why": "荷兰国旗问题：用三个指针 p0、p1、cur 一次遍历。0 换到 p0、2 换到 p2，1 自然留在中间，O(n) 时间 + O(1) 空间原地完成。",
        "desc": """<p>给定一个包含红色(0)、白色(1)、蓝色(2)的数组，<strong>原地</strong>按 0、1、2 的顺序排序（不能用库排序函数）。</p>
<p><strong>示例：</strong><br><code>[2,0,2,1,1,0]</code> → <code>[0,0,1,1,2,2]</code></p>""",
        "frames": [
            frame("① p0 指向下一个 0 的位置，p2 指向下一个 2 的位置", "drawTwoPointers", arr=[2, 0, 2, 1, 1, 0], left=0, right=5, width=560, height=140),
            frame("② cur 遇 0 与 p0 交换、遇 2 与 p2 交换", "drawTwoPointers", arr=[0, 0, 1, 1, 2, 2], left=2, right=3, width=560, height=140),
            frame("③ 结果 [0,0,1,1,2,2]", "drawTable", headers=["下标", "0", "1", "2", "3", "4", "5"], rows=[["结果", "0", "0", "1", "1", "2", "2"]], width=560, height=110),
        ],
        "conclusion": "p0 之前全 0，p2 之后全 2，cur 扫一遍把 0 前送、2 后送，1 留在中间。",
        "py": """def sortColors(nums):
    p0 = cur = 0
    p2 = len(nums) - 1
    while cur <= p2:
        if nums[cur] == 0:
            nums[cur], nums[p0] = nums[p0], nums[cur]
            p0 += 1; cur += 1
        elif nums[cur] == 2:
            nums[cur], nums[p2] = nums[p2], nums[cur]
            p2 -= 1          # cur 不前进，换来的数还要再判
        else:
            cur += 1""",
        "java": """public void sortColors(int[] nums) {
    int p0 = 0, cur = 0, p2 = nums.length - 1;
    while (cur <= p2) {
        if (nums[cur] == 0) { swap(nums, cur++, p0++); }
        else if (nums[cur] == 2) { swap(nums, cur, p2--); }
        else cur++;
    }
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }""",
        "time": "O(n) — 一次遍历",
        "space": "O(1)",
        "pitfalls": [
            ("遇 2 交换后 cur 不前移", "从 p2 换来的数还没检查过，cur 要留在原地再判断一次"),
            ("循环条件 cur <= p2", "cur 超过 p2 说明后面的 2 已就位，可以结束"),
        ],
        "selfcheck": [
            ("为什么遇 0 时 cur 可以前移？", "从 p0 换来的数一定是 1（因为 cur 扫过 p0 之前的都是 0/1），无需再判断。"),
            ("只有 0 和 1（无 2）呢？", "p2 分支永不触发，退化为简单的 0/1 分区。"),
        ],
    },
    # ---------------------------------------------------------------- 39
    {
        "id": 39,
        "title": "最小覆盖子串",
        "diff": "hard",
        "tags": ["滑动窗口"],
        "leetcode": 76,
        "origin": "https://leetcode.cn/problems/minimum-window-substring/",
        "why": "用滑动窗口在 s 上滑：右指针扩大窗口直到「覆盖 t 所有字符」，再左指针收缩到「刚好还覆盖」为止，记录最短。用哈希表计数判断是否覆盖。",
        "desc": """<p>给定字符串 <code>s</code> 和 <code>t</code>，返回 s 中涵盖 t 所有字符的最小子串；不存在则返回空串。</p>
<p><strong>示例：</strong><br><code>s="ADOBECODEBANC", t="ABC"</code> → <code>"BANC"</code></p>""",
        "frames": [
            frame("① 右指针扩大窗口，直到覆盖 t=ABC", "drawTwoPointers", arr=list("ADOBECODEBANC"), left=0, right=5, window={"start": 0, "end": 5}, width=720, height=150),
            frame("② 左指针收缩，记录最短覆盖窗口", "drawTwoPointers", arr=list("ADOBECODEBANC"), left=9, right=12, window={"start": 9, "end": 12}, width=720, height=150),
            frame("③ 最短子串 = \"BANC\"", "drawTable", headers=["窗口", "值"], rows=[["子串", "BANC"], ["长度", "4"]], width=420, height=130),
        ],
        "conclusion": "右扩到「覆盖」，左缩到「最小仍覆盖」，反复滑动取全局最短。",
        "py": """from collections import Counter
def minWindow(s, t):
    need = Counter(t)
    need_cnt = len(need)
    window = {}
    have = 0
    l = 0
    ans, ans_len = "", float("inf")
    for r, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == need_cnt:            # 已覆盖，尝试收缩
            if r - l + 1 < ans_len:
                ans, ans_len = s[l:r + 1], r - l + 1
            left_ch = s[l]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                have -= 1
            l += 1
    return ans""",
        "java": """public String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int needCnt = 0;
    for (int x : need) if (x > 0) needCnt++;
    int[] win = new int[128];
    int have = 0, l = 0, start = 0, len = Integer.MAX_VALUE;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (++win[c] == need[c]) have++;
        while (have == needCnt) {
            if (r - l + 1 < len) { start = l; len = r - l + 1; }
            char d = s.charAt(l);
            if (win[d] == need[d]) have--;
            win[d]--; l++;
        }
    }
    return len == Integer.MAX_VALUE ? "" : s.substring(start, start + len);
}""",
        "time": "O(|s|) — 左右指针各扫一遍",
        "space": "O(字符集) — 计数表",
        "pitfalls": [
            ("覆盖判定用 have==need_cnt", "只有某字符计数「恰好达到需求」时 have 才 +1，多了不重复加"),
            ("收缩时先减再判断", "移出左边界字符后，若其计数掉到需求以下，覆盖数 have 才 -1"),
        ],
        "selfcheck": [
            ("t 中字符有重复呢？", "need 记录每个字符需求次数，window 计数与之比较，重复字符必须凑够数量才算覆盖。"),
            ("s 中不存在覆盖子串？", "have 永远达不到 needCnt，ans 保持空串，最后返回 \"\"。"),
        ],
    },
    # ---------------------------------------------------------------- 40
    {
        "id": 40,
        "title": "子集",
        "diff": "medium",
        "tags": ["回溯"],
        "leetcode": 78,
        "origin": "https://leetcode.cn/problems/subsets/",
        "why": "每个元素有「选 / 不选」两种选择，子集共有 2^n 个。回溯按「从当前下标往后选」遍历，每进入一层就先把当前组合记下，就能无遗漏地收集所有子集。",
        "desc": """<p>给定一个<strong>不含重复元素</strong>的整数数组 <code>nums</code>，返回该数组所有可能的子集（幂集）。</p>
<p><strong>示例：</strong><br><code>nums=[1,2,3]</code> → <code>[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]</code></p>""",
        "frames": [
            frame("① 每个元素「选 / 不选」的决策树", "drawBacktrack",
                  nodes=[{"val": "[]", "x": 300, "y": 15, "color": "normal"},
                         {"val": "[1]", "x": 140, "y": 85, "color": "path"}, {"val": "[]", "x": 460, "y": 85, "color": "path"},
                         {"val": "[1,2]", "x": 60, "y": 160, "color": "path"}, {"val": "[1]", "x": 220, "y": 160, "color": "path"},
                         {"val": "[1,2,3]", "x": 60, "y": 240, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 140, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 460, "y2": 85, "color": "path"},
                         {"x1": 140, "y1": 85, "x2": 60, "y2": 160, "color": "path"}, {"x1": 140, "y1": 85, "x2": 220, "y2": 160, "color": "path"},
                         {"x1": 60, "y1": 160, "x2": 60, "y2": 240, "color": "path"}],
                  width=560, height=280),
            frame("② 每进入一层，当前 path 就是一个子集，立即收集", "drawTable",
                  headers=["层级", "path", "是否收集"],
                  rows=[["0", "[]", "✓"], ["1", "[1]", "✓"], ["2", "[1,2]", "✓"], ["3", "[1,2,3]", "✓"]], width=460, height=190),
        ],
        "conclusion": "「进入即收集」保证从空集到全集每个中间状态都不漏。",
        "py": """def subsets(nums):
    ans = []
    def dfs(start, path):
        ans.append(path[:])        # 每个状态都是子集
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1, path)       # 不重复：只往后选
            path.pop()
    dfs(0, [])
    return ans""",
        "java": """public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> ans = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), ans);
    return ans;
}
void dfs(int[] nums, int start, List<Integer> path, List<List<Integer>> ans) {
    ans.add(new ArrayList<>(path));
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);
        dfs(nums, i + 1, path, ans);
        path.remove(path.size() - 1);
    }
}""",
        "time": "O(n · 2^n) — 2^n 个子集，每个复制一次",
        "space": "O(n) — 递归栈",
        "pitfalls": [
            ("进入就收集", "不要等到叶子才收集，否则会漏掉中间态（如 [1]、[1,2]）"),
            ("start 下标去重", "从 start 往后选保证子集内部有序，避免 [1,2] 与 [2,1] 重复"),
        ],
        "selfcheck": [
            ("位运算怎么做这题？", "0 到 2^n-1 每个数对应一个子集，第 k 位为 1 表示选 nums[k]，时间 O(n·2^n)。"),
            ("nums 有重复元素呢？", "先排序，循环里跳过「同级重复」元素，避免生成重复子集。"),
        ],
    },
]

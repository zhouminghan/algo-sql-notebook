from scripts.algo_gen import frame


PROBLEMS = [
    # ---------------------------------------------------------------- 71
    {
        "id": 71,
        "title": "轮转数组",
        "diff": "medium",
        "tags": ["数组"],
        "leetcode": 189,
        "origin": "https://leetcode.cn/problems/rotate-array/",
        "why": "把数组向右轮转 k 位，等价于「整体反转 → 前 k 个反转 → 后 n-k 个反转」三步，原地 O(1) 空间。k 要先对 n 取模。",
        "desc": """<p>给定整数数组，将数组中的元素向右轮转 <code>k</code> 个位置。</p>
<p><strong>示例：</strong><br><code>nums=[1,2,3,4,5,6,7], k=3</code> → <code>[5,6,7,1,2,3,4]</code></p>""",
        "frames": [
            frame("① 整体反转 [7,6,5,4,3,2,1]", "drawTable",
                  headers=["下标", "0", "1", "2", "3", "4", "5", "6"],
                  rows=[["原数组", "1", "2", "3", "4", "5", "6", "7"], ["整体反转", "7", "6", "5", "4", "3", "2", "1"]], width=620, height=140),
            frame("② 前 k=3 个反转 → [5,6,7,...]", "drawTable",
                  headers=["下标", "0", "1", "2", "3", "4", "5", "6"],
                  rows=[["结果", "5", "6", "7", "4", "3", "2", "1"]], width=620, height=110),
            frame("③ 后 n-k 个反转 → [5,6,7,1,2,3,4]", "drawTable",
                  headers=["下标", "0", "1", "2", "3", "4", "5", "6"],
                  rows=[["最终", "5", "6", "7", "1", "2", "3", "4"]], width=620, height=110),
        ],
        "conclusion": "三次反转组合出「循环右移」效果，且完全原地。",
        "py": """def rotate(nums, k):
    n = len(nums)
    k %= n
    def rev(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1
    rev(0, n - 1)        # 整体
    rev(0, k - 1)        # 前 k
    rev(k, n - 1)        # 后 n-k""",
        "java": """public void rotate(int[] nums, int k) {
    int n = nums.length; k %= n;
    rev(nums, 0, n - 1);
    rev(nums, 0, k - 1);
    rev(nums, k, n - 1);
}
void rev(int[] a, int l, int r) {
    while (l < r) { int t = a[l]; a[l] = a[r]; a[r] = t; l++; r--; }
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("k 取模", "k 可能大于 n，先 k %= n，否则反转区间越界"),
            ("三步顺序", "先整体、再前 k、再后 n-k，顺序不能乱"),
        ],
        "selfcheck": [
            ("k=0 或 k=n？", "k%=n 后为 0，三次反转互相抵消，数组不变。"),
            ("左轮转怎么做？", "同理先整体反转，再反转「前 n-k」和「后 k」即可。"),
        ],
    },
    # ---------------------------------------------------------------- 72
    {
        "id": 72,
        "title": "打家劫舍",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 198,
        "origin": "https://leetcode.cn/problems/house-robber/",
        "why": "相邻房屋不能同时偷。dp[i] = max(dp[i-1], dp[i-2] + nums[i])：要么不偷当前、要么偷当前加上前两家的最优。滚动两个变量 O(1) 空间。",
        "desc": """<p>你是一排房屋，每间屋内有一定现金。相邻房屋装有报警器，如果相邻房屋同一晚被闯入会自动报警。求不触发警报的前提下能偷到的最高金额。</p>
<p><strong>示例：</strong><br><code>[1,2,3,1]</code> → <code>4</code>（偷 1 和 3）；<code>[2,7,9,3,1]</code> → <code>12</code></p>""",
        "frames": [
            frame("① dp[i] = max(dp[i-1], dp[i-2]+nums[i])", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4"],
                  rows=[["nums", "2", "7", "9", "3", "1"], ["dp", "2", "7", "11", "11", "12"]], width=520, height=130),
            frame("② 偷当前 = dp[i-2]+nums[i]，不偷 = dp[i-1]", "drawTable",
                  headers=["方案", "金额"],
                  rows=[["偷 nums[4]=1", "dp[2]+1=12"], ["不偷", "dp[3]=11"], ["取 max", {"val": "12", "highlight": True}]], width=460, height=150),
        ],
        "conclusion": "相邻约束让「当前偷不偷」只依赖前两家，滚动即可。",
        "py": """def rob(nums):
    prev2 = prev = 0
    for x in nums:
        prev2, prev = prev, max(prev, prev2 + x)
    return prev""",
        "java": """public int rob(int[] nums) {
    int prev2 = 0, prev = 0;
    for (int x : nums) {
        int cur = Math.max(prev, prev2 + x);
        prev2 = prev; prev = cur;
    }
    return prev;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("初始化 0", "prev2=prev=0，处理空数组与第一家"),
            ("别贪心隔一个偷", "隔一个偷未必最优，必须 DP 比较「偷当前」与「不偷当前」"),
        ],
        "selfcheck": [
            ("[2,1,1,2] 答案？", "偷 0 和 3 得 4。贪心隔一偷会错过。"),
            ("首尾相连（打家劫舍 II）呢？", "分别算「去掉第一家」和「去掉最后一家」取较大者。"),
        ],
    },
    # ---------------------------------------------------------------- 73
    {
        "id": 73,
        "title": "二叉树的右视图",
        "diff": "medium",
        "tags": ["BFS"],
        "leetcode": 199,
        "origin": "https://leetcode.cn/problems/binary-tree-right-side-view/",
        "why": "右视图 = 每一层最右边的节点。层序遍历时，每层最后一个访问到的节点就是该层右视图。",
        "desc": """<p>给定二叉树，想象站在它的<strong>右侧</strong>，返回从顶部到底部能看到的节点值。</p>
<p><strong>示例：</strong><br><code>[1,2,3,null,5,null,4]</code> → <code>[1,3,4]</code></p>""",
        "frames": [
            frame("① 每层最右的节点进入右视图", "drawTree",
                  nodes=[{"val": "1", "x": 300, "y": 25, "highlight": "active"}, {"val": "2", "x": 160, "y": 110}, {"val": "3", "x": 440, "y": 110, "highlight": "active"}, {"val": "5", "x": 200, "y": 200}, {"val": "4", "x": 480, "y": 200, "highlight": "active"}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 200, "y2": 200}, {"x1": 440, "y1": 110, "x2": 480, "y2": 200}], width=560, height=240),
            frame("② 层序遍历取每层最后一个", "drawTable",
                  headers=["层", "节点", "右视图"],
                  rows=[["0", "1", "1"], ["1", "2, 3", "3"], ["2", "5, 4", "4"]], width=460, height=160),
        ],
        "conclusion": "BFS 每层记录最后一个节点即可。",
        "py": """from collections import deque
def rightSideView(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        for i in range(len(q)):
            node = q.popleft()
            if i == len(q):      # 等价于每层最后一个
                res.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return res""",
        "java": """public List<Integer> rightSideView(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int size = q.size();
        for (int i = 0; i < size; i++) {
            TreeNode n = q.poll();
            if (i == size - 1) res.add(n.val);
            if (n.left != null) q.offer(n.left);
            if (n.right != null) q.offer(n.right);
        }
    }
    return res;
}""",
        "time": "O(n)",
        "space": "O(n) — 队列",
        "pitfalls": [
            ("取每层最后一个", "i == size-1 时收集，不是第一个"),
            ("空树返回 []", "root 为 None 直接返回空"),
        ],
        "selfcheck": [
            ("DFS 能做吗？", "可以，先右后左的 DFS，每个深度第一次访问到的节点就是右视图。"),
            ("为什么不用「一直往右走」？", "右视图不一定是右链，左子树的右子节点也可能被看到，必须逐层判断。"),
        ],
    },
    # ---------------------------------------------------------------- 74
    {
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
            frame("① 遇到陆地就 DFS 淹没整片", "drawTable",
                  headers=["", "0", "1", "2", "3", "4"],
                  rows=[["0", "1", "1", "0", "0", "0"], ["1", "1", "1", "0", "0", "0"], ["2", "0", "0", "1", "0", "0"], ["3", "0", "0", "0", "1", "1"]], width=500, height=190),
            frame("② 淹没后该岛计 1，继续扫描", "drawTable",
                  headers=["", "0", "1", "2", "3", "4"],
                  rows=[["0", "0", "0", "0", "0", "0"], ["1", "0", "0", "0", "0", "0"], ["2", "0", "0", {"val": "1", "highlight": True}, "0", "0"], ["3", "0", "0", "0", "1", "1"]], width=500, height=190),
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
        "pitfalls": [
            ("淹没或标记", "访问过必须置 '0' 或 visited，否则重复计数/死循环"),
            ("边界与越界", "四个方向先判界再判值"),
        ],
        "selfcheck": [
            ("BFS 版本？", "用队列把相连陆地依次入队处理，逻辑与 DFS 一致，只是遍历方式不同。"),
            ("为什么 DFS 递归不会重复访问？", "进入就置 '0'，后续递归不会再把它当作 '1'，天然去重。"),
        ],
    },
    # ---------------------------------------------------------------- 75
    {
        "id": 75,
        "title": "反转链表",
        "diff": "easy",
        "tags": ["链表"],
        "leetcode": 206,
        "origin": "https://leetcode.cn/problems/reverse-linked-list/",
        "why": "用 prev、cur 两个指针，每次把 cur.next 指回 prev，再双双前移。迭代 O(n) O(1)，是最基础的链表操作。",
        "desc": """<p>给定单链表的头节点，反转链表并返回反转后的头节点。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4,5]</code> → <code>[5,4,3,2,1]</code></p>""",
        "frames": [
            frame("① 原链表 1→2→3→4→5", "drawLinkedList",
                  nodes=[{"val": 1}, {"val": 2}, {"val": 3}, {"val": 4}, {"val": 5}], width=560, height=90),
            frame("② 逐节点反转指针方向", "drawLinkedList",
                  nodes=[{"val": 1, "highlight": "active"}, {"val": 2, "highlight": "active"}, {"val": 3, "highlight": "active"}, {"val": 4, "highlight": "active"}, {"val": 5, "highlight": "active"}], width=560, height=90),
            frame("③ 反转完成 5→4→3→2→1", "drawLinkedList",
                  nodes=[{"val": 5, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}], width=560, height=90),
        ],
        "conclusion": "先存下一个节点，再把当前指回前驱，循环到链表尾。",
        "py": """def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev""",
        "java": """public ListNode reverseList(ListNode head) {
    ListNode prev = null, cur = head;
    while (cur != null) {
        ListNode nxt = cur.next;
        cur.next = prev;
        prev = cur; cur = nxt;
    }
    return prev;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("先存 nxt", "改指针前必须先保存 cur.next，否则断链"),
            ("返回 prev", "循环结束 cur 为 null，prev 才是新头"),
        ],
        "selfcheck": [
            ("空链表 / 单节点？", "分别返回 None / 原节点，逻辑天然覆盖。"),
            ("递归写法？", "newHead = reverseList(head.next)，再 head.next.next = head、head.next = None。"),
        ],
    },
    # ---------------------------------------------------------------- 76
    {
        "id": 76,
        "title": "课程表",
        "diff": "medium",
        "tags": ["拓扑排序"],
        "leetcode": 207,
        "origin": "https://leetcode.cn/problems/course-schedule/",
        "why": "课程依赖构成有向图，能否修完 = 图是否无环（可拓扑排序）。Kahn 算法：统计入度，把入度为 0 的课入队，依次出队并把后续课入度减一；若最终修完所有课则无环。",
        "desc": """<p>你需要修 <code>numCourses</code> 门课。先修课程 <code>prerequisites[i] = [a, b]</code> 表示修 a 前必须先修 b。判断是否可能完成所有课程。</p>
<p><strong>示例：</strong><br><code>numCourses=2, [[1,0]]</code> → <code>true</code>；<code>[[1,0],[0,1]]</code> → <code>false</code>（互相依赖成环）</p>""",
        "frames": [
            frame("① 建图并统计入度", "drawTable",
                  headers=["课程", "先修", "入度"],
                  rows=[["0", "无", "0"], ["1", "0", "1"], ["2", "0, 1", "2"]], width=460, height=160),
            frame("② 入度 0 的课入队，出队后把后续课入度 -1", "drawStack",
                  items=[{"val": "0"}], type="queue", height=130),
            frame("③ 修完的课数 == 总数则无环可完成", "drawTable",
                  headers=["课程", "2, 0", "1, 1"],
                  rows=[["已修数", "0", "1", "2"]], width=420, height=120),
        ],
        "conclusion": "拓扑排序能排完全部课程 = 无环 = 可完成。",
        "py": """from collections import deque
def canFinish(numCourses, prerequisites):
    indeg = [0] * numCourses
    graph = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    count = 0
    while q:
        cur = q.popleft()
        count += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return count == numCourses""",
        "java": """public boolean canFinish(int n, int[][] prerequisites) {
    int[] indeg = new int[n];
    List<List<Integer>> g = new ArrayList<>();
    for (int i = 0; i < n; i++) g.add(new ArrayList<>());
    for (int[] p : prerequisites) { g.get(p[1]).add(p[0]); indeg[p[0]]++; }
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i);
    int count = 0;
    while (!q.isEmpty()) {
        int cur = q.poll(); count++;
        for (int nxt : g.get(cur)) if (--indeg[nxt] == 0) q.offer(nxt);
    }
    return count == n;
}""",
        "time": "O(V + E)",
        "space": "O(V + E) — 邻接表",
        "pitfalls": [
            ("边方向", "先修 b → 后修 a，建图方向是 b 指向 a，入度记在 a 上"),
            ("成环判定", "最终 count < n 说明有环，返回 false"),
        ],
        "selfcheck": [
            ("为什么拓扑排序能判环？", "无环图才能把所有入度逐步减到 0 并全部出队；有环的节点入度永远降不到 0。"),
            ("DFS 判环做法？", "三色标记：0 未访问、1 访问中、2 已完成，DFS 遇到「访问中」的节点即发现环。"),
        ],
    },
    # ---------------------------------------------------------------- 77
    {
        "id": 77,
        "title": "实现Trie(前缀树)",
        "diff": "medium",
        "tags": ["Trie"],
        "leetcode": 208,
        "origin": "https://leetcode.cn/problems/implement-trie-prefix-tree/",
        "why": "Trie 用「节点 = 字符」的多叉树存储单词，共享公共前缀。每个节点存子节点指针数组 + is_end 标记，插入/查找/前缀判断都是 O(单词长度)。",
        "desc": """<p>实现 Trie（前缀树），支持 <code>insert(word)</code>、<code>search(word)</code>（单词是否存在）、<code>startsWith(prefix)</code>（是否有该前缀）。</p>
<p><strong>示例：</strong><br><code>insert("apple")</code>；<code>search("apple")→true</code>；<code>search("app")→false</code>；<code>startsWith("app")→true</code></p>""",
        "frames": [
            frame("① 插入 apple、app：共享前缀 a-p-p", "drawTable",
                  headers=["单词", "路径"],
                  rows=[["apple", "a→p→p→l→e(终)"], ["app", "a→p→p(终)"]], width=500, height=140),
            frame("② 节点结构：children[26] + is_end", "drawTable",
                  headers=["节点", "children", "is_end"],
                  rows=[["'p'", "a~z 子指针", "false"], ["'e'", "…", "true"]], width=500, height=140),
        ],
        "conclusion": "逐字符向下走，最后一个字符的 is_end 决定「是完整单词还是仅前缀」。",
        "py": """class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False
    def insert(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True
    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end
    def startsWith(self, prefix):
        return self._walk(prefix) is not None
    def _walk(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node""",
        "java": """class Trie {
    Trie[] next = new Trie[26];
    boolean isEnd;
    public void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) node.next[i] = new Trie();
            node = node.next[i];
        }
        node.isEnd = true;
    }
    public boolean search(String word) {
        Trie n = walk(word);
        return n != null && n.isEnd;
    }
    public boolean startsWith(String prefix) { return walk(prefix) != null; }
    Trie walk(String s) {
        Trie node = this;
        for (char c : s.toCharArray()) {
            if (node.next[c - 'a'] == null) return null;
            node = node.next[c - 'a'];
        }
        return node;
    }
}""",
        "time": "插入/查找/前缀均 O(len)",
        "space": "O(节点数 × 字符集)",
        "pitfalls": [
            ("is_end 与前缀区分", "search 要求 is_end=true，startsWith 只要求路径存在"),
            ("字符下标", "小写字母用 c-'a' 映射到 0..25，哈希表版无需关心"),
        ],
        "selfcheck": [
            ("search(\"app\") 为何 false？", "路径 a-p-p 存在但 'p' 不是插入时的终点（is_end=false），所以只是前缀不是单词。"),
            ("Trie 的典型应用？", "自动补全、拼写检查、IP 路由最长前缀匹配、词频统计。"),
        ],
    },
    # ---------------------------------------------------------------- 78
    {
        "id": 78,
        "title": "数组中的第K个最大元素",
        "diff": "medium",
        "tags": ["堆"],
        "leetcode": 215,
        "origin": "https://leetcode.cn/problems/kth-largest-element-in-an-array/",
        "why": "维护一个大小为 k 的最小堆，遍历数组：堆不满就进，满了且当前值大于堆顶则替换。堆顶就是第 k 大。时间 O(n log k)，比全排序 O(n log n) 更优。",
        "desc": """<p>给定整数数组和整数 <code>k</code>，返回数组中第 <code>k</code> 个<strong>最大</strong>元素（排序后倒数第 k 个，而非第 k 个不同元素）。</p>
<p><strong>示例：</strong><br><code>[3,2,1,5,6,4], k=2</code> → <code>5</code></p>""",
        "frames": [
            frame("① 维护大小为 k=2 的最小堆", "drawStack",
                  items=[{"val": "3"}, {"val": "2"}], type="stack", height=140),
            frame("② 遍历：比堆顶大就替换，堆顶始终是「当前前 k 大里最小的」", "drawTable",
                  headers=["元素", "堆（前2大）", "堆顶"],
                  rows=[["1", "3,2", "2"], ["5", "5,3", "3"], ["6", "6,5", "5"], ["4", "6,5", "5"]], width=460, height=190),
            frame("③ 堆顶 5 即第 2 大", "drawTable",
                  headers=["", "值"],
                  rows=[["第 2 大", {"val": "5", "highlight": True}]], width=420, height=110),
        ],
        "conclusion": "小顶堆的堆顶是「前 k 大元素的最小者」，即第 k 大。",
        "py": """import heapq
def findKthLargest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]""",
        "java": """public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    for (int x : nums) {
        pq.offer(x);
        if (pq.size() > k) pq.poll();
    }
    return pq.peek();
}""",
        "time": "O(n log k)",
        "space": "O(k)",
        "pitfalls": [
            ("最小堆维护第 k 大", "堆顶是「最小的那个大值」，别用最大堆（那要找第 k 小）"),
            ("k 大小", "堆满 k 后每次 push 都要 pop 一个，保持规模 k"),
        ],
        "selfcheck": [
            ("快速选择做法？", "基于快排 partition，平均 O(n)，最坏 O(n²)，适合大数据量。"),
            ("第 k 大与第 k 小？", "第 k 大 = 第 (n-k+1) 小；求第 k 小则用最大堆。"),
        ],
    },
    # ---------------------------------------------------------------- 79
    {
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
            frame("① dp[i][j] = 以 (i,j) 为右下角的最大边长", "drawTable",
                  headers=["", "0", "1", "2", "3", "4"],
                  rows=[["0", "1", "0", "1", "0", "0"], ["1", "1", "0", "1", "1", "1"], ["2", "1", "1", "1", "2", "2"], ["3", "1", "0", "0", "1", "0"]], width=500, height=190),
            frame("② 递推：min(左上, 上, 左) + 1", "drawTable",
                  headers=["方向", "左上", "上", "左"],
                  rows=[["dp 值", "1", "1", "1"], ["本格", "min(1,1,1)+1 = 2"]], width=460, height=140),
            frame("③ 最大边长 2，面积 4", "drawTable",
                  headers=["", "值"],
                  rows=[["最大边长", "2"], ["面积", {"val": "4", "highlight": True}]], width=420, height=130),
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
        "pitfalls": [
            ("三个方向取 min", "取 max 会错误地把「L 形」当成正方形"),
            ("面积是边长平方", "返回 side*side，别直接返回边长"),
        ],
        "selfcheck": [
            ("为什么 min(三个)+1？", "以 (i,j) 为右下角的正方形，其上边、左边、左上角必须同时都能容纳 side-1 的正方形，取三者交集即 min。"),
            ("全 0 矩阵？", "side 保持 0，返回 0。"),
        ],
    },
    # ---------------------------------------------------------------- 80
    {
        "id": 80,
        "title": "翻转二叉树",
        "diff": "easy",
        "tags": ["树"],
        "leetcode": 226,
        "origin": "https://leetcode.cn/problems/invert-binary-tree/",
        "why": "翻转 = 对每个节点交换左右子树。递归先交换当前节点左右孩子，再递归翻转左右子树；或先递归再交换都可。",
        "desc": """<p>给定二叉树根节点，翻转这棵二叉树，返回其根节点（镜像）。</p>
<p><strong>示例：</strong><br><code>[4,2,7,1,3,6,9]</code> → <code>[4,7,2,9,6,3,1]</code></p>""",
        "frames": [
            frame("① 原树", "drawTree",
                  nodes=[{"val": "4", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110}, {"val": "7", "x": 440, "y": 110}, {"val": "1", "x": 100, "y": 200}, {"val": "3", "x": 220, "y": 200}, {"val": "6", "x": 380, "y": 200}, {"val": "9", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
            frame("② 交换每个节点的左右子树", "drawTree",
                  nodes=[{"val": "4", "x": 300, "y": 25}, {"val": "7", "x": 160, "y": 110}, {"val": "2", "x": 440, "y": 110}, {"val": "9", "x": 100, "y": 200}, {"val": "6", "x": 220, "y": 200}, {"val": "3", "x": 380, "y": 200}, {"val": "1", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
        ],
        "conclusion": "每个节点做一次左右交换，递归到整棵树。",
        "py": """def invertTree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invertTree(root.left)
    invertTree(root.right)
    return root""",
        "java": """public TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    TreeNode t = root.left;
    root.left = root.right;
    root.right = t;
    invertTree(root.left);
    invertTree(root.right);
    return root;
}""",
        "time": "O(n)",
        "space": "O(h)",
        "pitfalls": [
            ("先交换再递归", "交换当前节点后，左右子树位置已变，递归顺序仍各走一遍即可"),
            ("空树", "root 为 None 直接返回"),
        ],
        "selfcheck": [
            ("迭代做法？", "用队列做 BFS，每取出一个节点就交换其左右孩子。"),
            ("翻转两次？", "翻转两次回到原树，翻转是自身的逆操作。"),
        ],
    },
    # ---------------------------------------------------------------- 81
    {
        "id": 81,
        "title": "二叉搜索树中第K小的元素",
        "diff": "medium",
        "tags": ["BST"],
        "leetcode": 230,
        "origin": "https://leetcode.cn/problems/kth-smallest-element-in-a-bst/",
        "why": "BST 中序遍历严格递增，第 k 个访问到的节点就是第 k 小。迭代中序（或递归计数）到第 k 个即停，不必遍历整棵树。",
        "desc": """<p>给定二叉搜索树的根节点和一个整数 <code>k</code>，返回树中第 <code>k</code> 小的元素（从 1 开始计数）。</p>
<p><strong>示例：</strong><br>树 <code>[3,1,4,null,2]</code>, <code>k=1</code> → <code>1</code>；<code>k=3</code> → <code>3</code></p>""",
        "frames": [
            frame("① 中序遍历顺序：1,2,3,4", "drawTree",
                  nodes=[{"val": "3", "x": 300, "y": 25}, {"val": "1", "x": 160, "y": 110}, {"val": "4", "x": 440, "y": 110}, {"val": "2", "x": 210, "y": 200, "highlight": "done"}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 210, "y2": 200}], width=520, height=240),
            frame("② 第 k 个访问到的即第 k 小", "drawTable",
                  headers=["次序", "1", "2", "3", "4"],
                  rows=[["节点", "1", "2", "3", "4"]], width=460, height=110),
        ],
        "conclusion": "中序第 k 个节点就是答案，计数到 k 提前停止。",
        "py": """def kthSmallest(root, k):
    stack = []
    cur = root
    while True:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right""",
        "java": """public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root;
    while (true) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        cur = st.pop();
        if (--k == 0) return cur.val;
        cur = cur.right;
    }
}""",
        "time": "O(h + k) — 访问到第 k 个即停",
        "space": "O(h) — 栈",
        "pitfalls": [
            ("中序第 k 个", "中序严格递增是前提，遍历到第 k 个返回"),
            ("迭代避免全遍历", "找到第 k 个立刻返回，不必走完整棵树"),
        ],
        "selfcheck": [
            ("k 越界？", "题目保证 k 有效（1 ≤ k ≤ 节点数），无需处理。"),
            ("进阶：频繁插入删除的 BST？", "给节点维护「左子树大小」计数，O(h) 定位第 k 小。"),
        ],
    },
    # ---------------------------------------------------------------- 82
    {
        "id": 82,
        "title": "回文链表",
        "diff": "easy",
        "tags": ["链表"],
        "leetcode": 234,
        "origin": "https://leetcode.cn/problems/palindrome-linked-list/",
        "why": "快慢指针找中点 → 反转后半段 → 与前半段逐个比较。O(n) 时间 + O(1) 空间，比转数组更省空间。",
        "desc": """<p>给定单链表的头节点，判断它是否是回文链表。</p>
<p><strong>示例：</strong><br><code>[1,2,2,1]</code> → <code>true</code>；<code>[1,2]</code> → <code>false</code></p>""",
        "frames": [
            frame("① 找中点，反转后半段", "drawLinkedList",
                  nodes=[{"val": 1}, {"val": 2, "highlight": "active"}, {"val": 2}, {"val": 1}], width=520, height=90),
            frame("② 后半段反转后为 1→2", "drawLinkedList",
                  nodes=[{"val": 1}, {"val": 2}, {"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}], width=520, height=90),
            frame("③ 前后两段逐个比较，全等即回文", "drawTable",
                  headers=["位置", "前段", "后段", "相等?"],
                  rows=[["0", "1", "1", "✓"], ["1", "2", "2", "✓"]], width=460, height=140),
        ],
        "conclusion": "反转后半段后，与前半段逐节点比对，全部相等即回文。",
        "py": """def isPalindrome(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow      # 反转后半
    while cur:
        nxt = cur.next
        cur.next, prev, cur = prev, cur, nxt
    a, b = head, prev
    while b:
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return True""",
        "java": """public boolean isPalindrome(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode prev = null, cur = slow;
    while (cur != null) { ListNode n = cur.next; cur.next = prev; prev = cur; cur = n; }
    ListNode a = head, b = prev;
    while (b != null) {
        if (a.val != b.val) return false;
        a = a.next; b = b.next;
    }
    return true;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("只比较后半段长度", "while b 以后半段为准，奇数长度时中间节点不参与比较"),
            ("反转从 slow 开始", "slow 是后半段起点，反转后 prev 是后半段新头"),
        ],
        "selfcheck": [
            ("[1,2] 为何 false？", "中点 slow=2，反转后半还是 2，比较 1 vs 2 不等。"),
            ("转数组做法？", "把值收集到数组用双指针比较，空间 O(n)，简单但非 O(1)。"),
        ],
    },
    # ---------------------------------------------------------------- 83
    {
        "id": 83,
        "title": "二叉树的最近公共祖先",
        "diff": "medium",
        "tags": ["树"],
        "leetcode": 236,
        "origin": "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/",
        "why": "自底向上递归：若当前节点是 p 或 q 就返回它；否则看左右子树是否各找到一个。两边都找到 → 当前就是 LCA；只一边找到 → 返回那一边。",
        "desc": """<p>给定二叉树，找到该树中两个指定节点的<strong>最近公共祖先</strong>（LCA）。</p>
<p><strong>示例：</strong><br>树 <code>[3,5,1,6,2,0,8,null,null,7,4]</code>，p=5, q=1 → <code>3</code>；p=5, q=4 → <code>5</code></p>""",
        "frames": [
            frame("① 自底向上：左右各找到一个，当前即 LCA", "drawTree",
                  nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "5", "x": 160, "y": 110, "highlight": "done"}, {"val": "1", "x": 440, "y": 110, "highlight": "done"}, {"val": "6", "x": 100, "y": 200}, {"val": "2", "x": 220, "y": 200}, {"val": "0", "x": 380, "y": 200}, {"val": "8", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
            frame("② 只一边找到，继续上抛", "drawTable",
                  headers=["情况", "返回值"],
                  rows=[["当前是 p/q", "当前节点"], ["两边都有", "当前节点(LCA)"], ["只有一边", "那一侧的结果"]], width=500, height=160),
        ],
        "conclusion": "递归返回「找到的 p/q 或 LCA」，两边会师处就是最近公共祖先。",
        "py": """def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left or right""",
        "java": """public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode l = lowestCommonAncestor(root.left, p, q);
    TreeNode r = lowestCommonAncestor(root.right, p, q);
    if (l != null && r != null) return root;
    return l != null ? l : r;
}""",
        "time": "O(n)",
        "space": "O(h)",
        "pitfalls": [
            ("返回条件", "root 为 p 或 q 直接返回，意味着「找到了」向上传递"),
            ("两边会师", "left 和 right 都非空时当前节点就是 LCA"),
        ],
        "selfcheck": [
            ("p 是 q 的祖先？", "递归到 p 直接返回 p，上层继续上抛 p，结果正确。"),
            ("p、q 都在同一侧？", "只有那一侧返回值非空，继续上抛，直到某一层两侧都命中。"),
        ],
    },
    # ---------------------------------------------------------------- 84
    {
        "id": 84,
        "title": "除自身以外数组的乘积",
        "diff": "medium",
        "tags": ["前缀积"],
        "leetcode": 238,
        "origin": "https://leetcode.cn/problems/product-of-array-except-self/",
        "why": "答案[i] = 左边所有数的乘积 × 右边所有数的乘积。先从左到右累乘左前缀，再从右到左累乘右前缀，两遍 O(n)，不用除法、O(1) 额外空间。",
        "desc": """<p>给定整数数组，返回数组 <code>answer</code>，其中 <code>answer[i]</code> 等于 nums 中除 <code>nums[i]</code> 之外其余各元素的乘积。要求 O(n) 时间且<strong>不能使用除法</strong>。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4]</code> → <code>[24,12,8,6]</code></p>""",
        "frames": [
            frame("① 左前缀积：answer[i] 先存左边乘积", "drawTable",
                  headers=["i", "0", "1", "2", "3"],
                  rows=[["nums", "1", "2", "3", "4"], ["左前缀", "1", "1", "2", "6"]], width=460, height=130),
            frame("② 从右到左乘右前缀", "drawTable",
                  headers=["i", "0", "1", "2", "3"],
                  rows=[["右前缀", "24", "12", "4", "1"], ["结果", "24", "12", "8", "6"]], width=460, height=130),
        ],
        "conclusion": "左一遍 + 右一遍，两次前缀乘积合成就得到「除自己外」的乘积。",
        "py": """def productExceptSelf(nums):
    n = len(nums)
    ans = [1] * n
    left = 1
    for i in range(n):
        ans[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= right
        right *= nums[i]
    return ans""",
        "java": """public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    int left = 1;
    for (int i = 0; i < n; i++) { ans[i] = left; left *= nums[i]; }
    int right = 1;
    for (int i = n - 1; i >= 0; i--) { ans[i] *= right; right *= nums[i]; }
    return ans;
}""",
        "time": "O(n) — 两遍遍历",
        "space": "O(1) — 输出数组不计入额外空间",
        "pitfalls": [
            ("不能用除法", "除法的 0 元素会除零，且题目明令禁止"),
            ("左右两遍", "先左后右，ans[i] 先存左边积，再乘右边积"),
        ],
        "selfcheck": [
            ("数组含 0 呢？", "两遍前缀法天然处理 0，不需要特判；除法则会出错。"),
            ("空间能更省吗？", "输出数组本身不算额外空间，已是 O(1) 额外空间的最优解。"),
        ],
    },
    # ---------------------------------------------------------------- 85
    {
        "id": 85,
        "title": "滑动窗口最大值",
        "diff": "hard",
        "tags": ["单调队列"],
        "leetcode": 239,
        "origin": "https://leetcode.cn/problems/sliding-window-maximum/",
        "why": "用「单调递减队列」存窗口内的候选最大值下标：队首是当前窗口最大。新元素入队前，把队尾所有更小的弹出（它们永无出头之日）；队首滑出窗口就移除。O(n)。",
        "desc": """<p>给定整数数组 <code>nums</code>，滑动窗口大小为 <code>k</code>，窗口从最左侧滑动到最右侧，每次只移动一位。返回每个窗口的最大值。</p>
<p><strong>示例：</strong><br><code>[1,3,-1,-3,5,3,6,7], k=3</code> → <code>[3,3,5,5,6,7]</code></p>""",
        "frames": [
            frame("① 窗口 [1,3,-1] 最大 3", "drawTwoPointers", arr=[1, 3, -1, -3, 5, 3, 6, 7], left=0, right=2, window={"start": 0, "end": 2}, width=700, height=150),
            frame("② 单调递减队列：队首恒为窗口最大", "drawStack",
                  items=[{"val": "3"}, {"val": "-1"}], type="queue", height=140),
            frame("③ 每滑一格输出队首，结果 [3,3,5,5,6,7]", "drawTable",
                  headers=["窗口", "0-2", "1-3", "2-4", "3-5", "4-6", "5-7"],
                  rows=[["最大值", "3", "3", "5", "5", "6", "7"]], width=620, height=120),
        ],
        "conclusion": "单调队列让「窗口最大值」始终在队首，滑入滑出都 O(1)，整体 O(n)。",
        "py": """from collections import deque
def maxSlidingWindow(nums, k):
    q = deque()      # 存下标，队首对应最大值
    ans = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()               # 弹掉更小的
        q.append(i)
        if q[0] < i - k + 1:      # 队首滑出窗口
            q.popleft()
        if i >= k - 1:
            ans.append(nums[q[0]])
    return ans""",
        "java": """public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] ans = new int[n - k + 1];
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!q.isEmpty() && nums[q.peekLast()] <= nums[i]) q.pollLast();
        q.offerLast(i);
        if (q.peekFirst() < i - k + 1) q.pollFirst();
        if (i >= k - 1) ans[i - k + 1] = nums[q.peekFirst()];
    }
    return ans;
}""",
        "time": "O(n) — 每个元素入队出队一次",
        "space": "O(k) — 队列",
        "pitfalls": [
            ("弹队尾更小元素", "用 <= 保证严格递减，新元素下标更大、更「长寿」，旧小值无用"),
            ("队首过期移除", "判断 q[0] < i-k+1 时把滑出窗口的下标从队首移除"),
        ],
        "selfcheck": [
            ("为什么存下标而非值？", "需要判断「队首是否还在窗口内」，只有下标能算出来。"),
            ("暴力做法复杂度？", "每个窗口扫一遍是 O(nk)，单调队列优化到 O(n)。"),
        ],
    },
]

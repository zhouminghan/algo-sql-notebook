from scripts.algo_gen import frame


PROBLEMS = [
    # ---------------------------------------------------------------- 86
    {
        "id": 86,
        "title": "搜索二维矩阵 II",
        "diff": "medium",
        "tags": ["二分"],
        "leetcode": 240,
        "origin": "https://leetcode.cn/problems/search-a-2d-matrix-ii/",
        "why": "矩阵每行每列都升序。从左下角出发：比 target 小就向右，比 target 大就向上，每次排除一行或一列，O(m+n) 即可，无需二分。",
        "desc": """<p>编写一个高效算法，搜索 m×n 矩阵中的目标值。矩阵每行从左到右升序、每列从上到下升序。</p>
<p><strong>示例：</strong><br><code>[[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target=5</code> → <code>true</code></p>""",
        "frames": [
            frame("① 从左下角出发", "drawTable",
                  headers=["", "0", "1", "2", "3", "4"],
                  rows=[["0", "1", "4", "7", "11", "15"], ["1", "2", "5", "8", "12", "19"], ["2", "3", "6", "9", "16", "22"], ["3", "10", "13", "14", "17", "24"], ["4", "18", "21", "23", "26", "30"]], width=500, height=220),
            frame("② 比 target 小向右，比 target 大向上", "drawTable",
                  headers=["", "0", "1", "2", "3", "4"],
                  rows=[["0", "1", "4", "7", "11", "15"], ["1", "2", {"val": "5", "highlight": True}, "8", "12", "19"], ["2", "3", "6", "9", "16", "22"], ["3", "10", "13", "14", "17", "24"], ["4", "18", "21", "23", "26", "30"]], width=500, height=220),
        ],
        "conclusion": "左下角是「行最小、列最大」的分水岭，每次都能确定性地排除一行或一列。",
        "py": """def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    i, j = m - 1, 0
    while i >= 0 and j < n:
        if matrix[i][j] == target:
            return True
        if matrix[i][j] < target:
            j += 1        # 向右
        else:
            i -= 1        # 向上
    return False""",
        "java": """public boolean searchMatrix(int[][] matrix, int target) {
    int i = matrix.length - 1, j = 0;
    while (i >= 0 && j < matrix[0].length) {
        if (matrix[i][j] == target) return true;
        if (matrix[i][j] < target) j++; else i--;
    }
    return false;
}""",
        "time": "O(m + n)",
        "space": "O(1)",
        "pitfalls": [
            ("从左下角出发", "左上角两个方向都更大，无法决策；左下角一清二楚"),
            ("移动方向", "小→右，大→上，不要反"),
        ],
        "selfcheck": [
            ("为什么不能整体二分？", "矩阵整体并非有序（行尾不一定小于下行首），只有行内和列内有序，所以用「Z 字形」排除法。"),
            ("右上角出发行吗？", "可以，对称：比 target 小向下、比 target 大向左。"),
        ],
    },
    # ---------------------------------------------------------------- 87
    {
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
            frame("① dp[i] = min(dp[i - 平方数]) + 1", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                  rows=[["dp", "0", "1", "2", "3", "1", "2", "3", "4", "2", "1", "2", "3", "3"]], width=800, height=130),
            frame("② n=12：12-4=8(dp=2)、12-9=3(dp=3)、12-1=11(dp=3)，min=2+1=3", "drawTable",
                  headers=["减哪个平方", "剩余", "剩余 dp", "总数"],
                  rows=[["1", "11", "3", "4"], ["4", "8", "2", "3"], ["9", "3", "3", "4"]], width=460, height=160),
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
        "pitfalls": [
            ("dp[0]=0", "边界 0 需要 0 个平方数"),
            ("枚举 j*j <= i", "只枚举不超过 i 的平方数"),
        ],
        "selfcheck": [
            ("BFS 怎么做？", "从 n 出发，每层减去一个平方数，第一次减到 0 的层数就是答案。"),
            ("四平方和定理？", "任意正整数可表为至多 4 个平方数之和，是这题的理论上界。"),
        ],
    },
    # ---------------------------------------------------------------- 88
    {
        "id": 88,
        "title": "移动零",
        "diff": "easy",
        "tags": ["双指针"],
        "leetcode": 283,
        "origin": "https://leetcode.cn/problems/move-zeroes/",
        "why": "快慢双指针：slow 指向「下一个非零该放的位置」，fast 扫描数组。遇非零就交换到 slow 并前进，最后 slow 之后全是 0。原地 O(n)。",
        "desc": """<p>给定整数数组，将所有 <code>0</code> 移动到数组末尾，同时保持非零元素的相对顺序。必须原地操作。</p>
<p><strong>示例：</strong><br><code>[0,1,0,3,12]</code> → <code>[1,3,12,0,0]</code></p>""",
        "frames": [
            frame("① slow 指向下一个非零位置，fast 扫描", "drawTwoPointers", arr=[0, 1, 0, 3, 12], left=0, right=1, width=520, height=140),
            frame("② 遇非零交换到 slow，slow 前进", "drawTwoPointers", arr=[1, 0, 0, 3, 12], left=1, right=2, width=520, height=140),
            frame("③ 结果 [1,3,12,0,0]", "drawTable",
                  headers=["下标", "0", "1", "2", "3", "4"],
                  rows=[["结果", "1", "3", "12", "0", "0"]], width=520, height=110),
        ],
        "conclusion": "非零元素依次「压实」到前面，剩余位置补 0。",
        "py": """def moveZeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1""",
        "java": """public void moveZeroes(int[] nums) {
    int slow = 0;
    for (int fast = 0; fast < nums.length; fast++)
        if (nums[fast] != 0) { int t = nums[slow]; nums[slow] = nums[fast]; nums[fast] = t; slow++; }
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("保持相对顺序", "用交换而非「先删后补」，顺序自然保持"),
            ("slow 含义", "slow 是下一个非零该放的位置，也是当前非零区间的长度"),
        ],
        "selfcheck": [
            ("全 0 数组？", "fast 全程不触发交换，slow=0，数组不变。"),
            ("能否先统计 0 个数再整体移动？", "可以，但双指针交换更直观且一步到位。"),
        ],
    },
    # ---------------------------------------------------------------- 89
    {
        "id": 89,
        "title": "寻找重复数",
        "diff": "medium",
        "tags": ["快慢指针"],
        "leetcode": 287,
        "origin": "https://leetcode.cn/problems/find-the-duplicate-number/",
        "why": "数组元素在 [1,n] 且只有一个重复，把「下标 i → nums[i]」看成链表的 next 指针，重复数就是环的入口。用环形链表 II 的快慢指针求解，O(n) O(1)。",
        "desc": """<p>给定包含 <code>n+1</code> 个整数的数组，数字都在 <code>[1,n]</code> 范围内，其中<strong>只有一个数字重复出现</strong>（可能重复多次）。找出这个重复数。要求不修改数组、O(1) 额外空间。</p>
<p><strong>示例：</strong><br><code>[1,3,4,2,2]</code> → <code>2</code>；<code>[3,1,3,4,2]</code> → <code>3</code></p>""",
        "frames": [
            frame("① 把 i → nums[i] 当链表 next，重复数即环入口", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4"],
                  rows=[["nums", "1", "3", "4", "2", "2"], ["next", "1", "3", "4", "2", "2"]], width=520, height=130),
            frame("② 快慢指针找相遇点", "drawTwoPointers", arr=[1, 3, 4, 2, 2], left=0, right=2, width=520, height=140),
            frame("③ 从头同速再走，相遇即重复数 2", "drawTable",
                  headers=["步骤", "指针 A", "指针 B"],
                  rows=[["0", "0", "相遇点"], ["1", "1", "4"], ["2", "3", "2"], ["3", "2", "2 相遇 ✓"]], width=460, height=190),
        ],
        "conclusion": "值域 [1,n] 保证 next 不出界且必有环，环入口就是重复数。",
        "py": """def findDuplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    p = nums[0]
    while p != slow:
        p = nums[p]
        slow = nums[slow]
    return p""",
        "java": """public int findDuplicate(int[] nums) {
    int slow = nums[0], fast = nums[0];
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);
    int p = nums[0];
    while (p != slow) { p = nums[p]; slow = nums[slow]; }
    return p;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("next 用 nums 本身", "slow = nums[slow]，fast = nums[nums[fast]]，别直接下标加减"),
            ("入口即答案", "环入口是重复数，因为只有重复数被多个节点指向"),
        ],
        "selfcheck": [
            ("为什么必有环？", "n+1 个值落在 [1,n]，鸽巢原理必有重复；从下标 0 出发的 next 链最终进入由重复数构成的环。"),
            ("二分法怎么做？", "统计 ≤mid 的个数，若大于 mid 说明重复在左半，O(n log n)，也能 O(1) 空间。"),
        ],
    },
    # ---------------------------------------------------------------- 90
    {
        "id": 90,
        "title": "数据流的中位数",
        "diff": "hard",
        "tags": ["堆"],
        "leetcode": 295,
        "origin": "https://leetcode.cn/problems/find-median-from-data-stream/",
        "why": "用两个堆：大顶堆放较小的一半，小顶堆放较大的一半。保持两者大小差 ≤1，中位数要么是大顶堆堆顶、要么是两堆顶均值。插入 O(log n)。",
        "desc": """<p>实现 MedianFinder，动态插入整数并随时返回当前所有数字的中位数。</p>
<p><strong>示例：</strong><br>依次加入 <code>1,2,3</code>，中位数分别为 <code>1, 1.5, 2</code></p>""",
        "frames": [
            frame("① 大顶堆存较小一半，小顶堆存较大一半", "drawTable",
                  headers=["堆", "较小一半(大顶)", "较大一半(小顶)"],
                  rows=[["加入 1,2,3 后", "2,1", "3"]], width=500, height=130),
            frame("② 平衡：两堆大小差 ≤1", "drawTable",
                  headers=["操作", "大顶堆", "小顶堆"],
                  rows=[["加 1", "1", ""], ["加 2", "1", "2"], ["加 3", "1", "2,3 → 平衡"]], width=500, height=160),
            frame("③ 中位数 = 堆顶 或 两堆顶均值", "drawTable",
                  headers=["总数", "中位数"],
                  rows=[["奇数", "大顶堆堆顶"], ["偶数", "(两堆顶)/2"]], width=460, height=130),
        ],
        "conclusion": "两个堆把数据切成两半，中位数永远在堆顶附近。",
        "py": """import heapq
class MedianFinder:
    def __init__(self):
        self.small = []   # 大顶堆（存负值）
        self.large = []   # 小顶堆
    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2""",
        "java": """class MedianFinder {
    PriorityQueue<Integer> small = new PriorityQueue<>((a, b) -> b - a);
    PriorityQueue<Integer> large = new PriorityQueue<>();
    public void addNum(int num) {
        small.offer(num);
        large.offer(small.poll());
        if (large.size() > small.size()) small.offer(large.poll());
    }
    public double findMedian() {
        if (small.size() > large.size()) return small.peek();
        return (small.peek() + large.peek()) / 2.0;
    }
}""",
        "time": "addNum O(log n)，findMedian O(1)",
        "space": "O(n)",
        "pitfalls": [
            ("Python 大顶堆用负值", "heapq 只有小顶堆，存 -num 模拟大顶堆"),
            ("平衡方向", "插入后让 large 不超过 small，保证 small 要么等大要么多一个"),
        ],
        "selfcheck": [
            ("偶数个中位数？", "两堆等大时取两堆顶平均值。"),
            ("奇数个中位数？", "small 多一个，中位数就是 small 堆顶（较小一半的最大值）。"),
        ],
    },
    # ---------------------------------------------------------------- 91
    {
        "id": 91,
        "title": "二叉树的序列化与反序列化",
        "diff": "hard",
        "tags": ["树"],
        "leetcode": 297,
        "origin": "https://leetcode.cn/problems/serialize-and-deserialize-binary-tree/",
        "why": "用前序遍历序列化，空节点记为特殊占位符（如 '#'）。反序列化时按同样顺序递归重建——遇到 '#' 返回空，否则读值建节点再建左右子树。",
        "desc": """<p>设计算法将二叉树序列化为字符串、并反序列化回原树结构，不限定序列化格式。</p>
<p><strong>示例：</strong><br><code>[1,2,3,null,null,4,5]</code> → 序列化后能还原为同一棵树</p>""",
        "frames": [
            frame("① 前序遍历 + '#' 占位空节点", "drawTree",
                  nodes=[{"val": "1", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110}, {"val": "3", "x": 440, "y": 110}, {"val": "4", "x": 380, "y": 200}, {"val": "5", "x": 500, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
            frame("② 序列化串：1,2,#,#,3,4,#,#,5,#,#", "drawTable",
                  headers=["顺序", "1", "2", "#", "#", "3", "4", "#", "#", "5", "#", "#"],
                  rows=[["含义", "根", "左", "空", "空", "右", "左", "空", "空", "右", "空", "空"]], width=720, height=140),
        ],
        "conclusion": "前序 + 空占位能唯一确定树，反序列化按同一递归顺序重建。",
        "py": """class Codec:
    def serialize(self, root):
        def dfs(node):
            if not node:
                vals.append('#')
                return
            vals.append(str(node.val))
            dfs(node.left); dfs(node.right)
        vals = []
        dfs(root)
        return ','.join(vals)
    def deserialize(self, data):
        it = iter(data.split(','))
        def build():
            v = next(it)
            if v == '#':
                return None
            node = TreeNode(int(v))
            node.left = build()
            node.right = build()
            return node
        return build()""",
        "java": """public class Codec {
    public String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        s(root, sb);
        return sb.toString();
    }
    void s(TreeNode n, StringBuilder sb) {
        if (n == null) { sb.append("#,"); return; }
        sb.append(n.val).append(",");
        s(n.left, sb); s(n.right, sb);
    }
    int i = 0;
    public TreeNode deserialize(String data) {
        String[] a = data.split(",");
        return d(a);
    }
    TreeNode d(String[] a) {
        if (a[i].equals("#")) { i++; return null; }
        TreeNode n = new TreeNode(Integer.parseInt(a[i++])); 
        n.left = d(a); n.right = d(a);
        return n;
    }
}""",
        "time": "序列化与反序列化均 O(n)",
        "space": "O(n)",
        "pitfalls": [
            ("空节点占位", "没有 '#' 占位无法区分「左空右有」的结构，反序列化会错位"),
            ("反序列化顺序一致", "递归顺序必须与序列化完全一致（前序对前序）"),
        ],
        "selfcheck": [
            ("为什么前序+空占位能唯一还原？", "前序给定根、左右顺序，空占位标出子树边界，递归重建唯一。"),
            ("BFS 序列化可以吗？", "可以，按层输出并保留空节点，反序列化用队列逐层接。"),
        ],
    },
    # ---------------------------------------------------------------- 92
    {
        "id": 92,
        "title": "最长递增子序列",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 300,
        "origin": "https://leetcode.cn/problems/longest-increasing-subsequence/",
        "why": "dp[i] = 以 nums[i] 结尾的最长递增子序列长度，遍历前面所有更小元素取最大 +1。O(n²)；或用「贪心 + 二分」维护一个递增 tails 数组做到 O(n log n)。",
        "desc": """<p>给定整数数组，找到其中最长严格递增子序列的长度（子序列不要求连续）。</p>
<p><strong>示例：</strong><br><code>[10,9,2,5,3,7,101,18]</code> → <code>4</code>（[2,3,7,101]）</p>""",
        "frames": [
            frame("① dp[i] = max(前面更小元素的 dp) + 1", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4", "5", "6", "7"],
                  rows=[["nums", "10", "9", "2", "5", "3", "7", "101", "18"], ["dp", "1", "1", "1", "2", "2", "3", "4", "4"]], width=700, height=130),
            frame("② 贪心 tails：维护最小结尾的递增序列", "drawTable",
                  headers=["遍历", "tails"],
                  rows=[["2", "[2]"], ["5", "[2,5]"], ["3", "[2,3]"], ["7", "[2,3,7]"], ["101", "[2,3,7,101]"]], width=460, height=210),
        ],
        "conclusion": "DP 版直观；二分版把「找前面更小」优化成「找 tails 中插入位置」，O(n log n)。",
        "py": """import bisect
def lengthOfLIS(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)""",
        "java": """public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int x : nums) {
        int l = 0, r = size;
        while (l < r) { int m = (l + r) >>> 1; if (tails[m] < x) l = m + 1; else r = m; }
        tails[l] = x;
        if (l == size) size++;
    }
    return size;
}""",
        "time": "O(n log n)",
        "space": "O(n)",
        "pitfalls": [
            ("tails 不是真实子序列", "它只维护「最小结尾」，长度正确但内容可能不是某条真实子序列"),
            ("严格递增用 bisect_left", "相等元素要替换而非追加，否则会算成非严格递增"),
        ],
        "selfcheck": [
            ("为什么 tails 长度等于答案？", "tails 的每个槽位代表「长度为 k 的子序列的最小可能结尾」，能放更多槽位即答案。"),
            ("要输出具体子序列？", "二分法需额外记录前驱；DP 版记录 prev 可回溯。"),
        ],
    },
    # ---------------------------------------------------------------- 93
    {
        "id": 93,
        "title": "删除无效的括号",
        "diff": "hard",
        "tags": ["BFS"],
        "leetcode": 301,
        "origin": "https://leetcode.cn/problems/remove-invalid-parentheses/",
        "why": "要删「最少」的括号，按层 BFS：每次尝试删一个括号得到下一层，一旦某层出现合法串，该层就是最小删除层，收集该层所有合法串即可。",
        "desc": """<p>给定只含 <code>(</code> 和 <code>)</code> 以及小写字母的字符串，删除<strong>最少数量的</strong>无效括号，使剩余字符串合法。返回所有可能的结果。</p>
<p><strong>示例：</strong><br><code>"()())()"</code> → <code>["(())()","()()()"]</code>；<code>"(a)())()"</code> → <code>["(a())()","(a)()()"]</code></p>""",
        "frames": [
            frame("① 按层 BFS：每删一个括号一层", "drawBacktrack",
                  nodes=[{"val": "()())()", "x": 300, "y": 15, "color": "normal"},
                         {"val": "删1个(4个候选)", "x": 160, "y": 95, "color": "path"},
                         {"val": "(())() ✓", "x": 90, "y": 175, "color": "path"}, {"val": "()()() ✓", "x": 230, "y": 175, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 160, "y2": 95, "color": "path"}, {"x1": 160, "y1": 95, "x2": 90, "y2": 175, "color": "path"}, {"x1": 160, "y1": 95, "x2": 230, "y2": 175, "color": "path"}],
                  width=560, height=220),
            frame("② 用计数判断合法：左加右减，中途不为负、最后为 0", "drawTable",
                  headers=["串", "计数", "合法?"],
                  rows=[["(())()", "0", "✓"], ["()()()", "0", "✓"], ["())(()", "中途负", "✗"]], width=460, height=160),
        ],
        "conclusion": "BFS 保证先找到的就是删除最少的，用 visited 去重避免重复状态。",
        "py": """def removeInvalidParentheses(s):
    def valid(t):
        cnt = 0
        for ch in t:
            if ch == '(': cnt += 1
            elif ch == ')':
                cnt -= 1
                if cnt < 0: return False
        return cnt == 0
    level = {s}
    while True:
        ans = [t for t in level if valid(t)]
        if ans:
            return ans
        nxt = set()
        for t in level:
            for i in range(len(t)):
                if t[i] not in '()': continue
                nxt.add(t[:i] + t[i + 1:])
        level = nxt""",
        "java": """public List<String> removeInvalidParentheses(String s) {
    List<String> ans = new ArrayList<>();
    Set<String> level = new HashSet<>();
    level.add(s);
    while (true) {
        for (String t : level) if (valid(t)) ans.add(t);
        if (!ans.isEmpty()) return ans;
        Set<String> nxt = new HashSet<>();
        for (String t : level)
            for (int i = 0; i < t.length(); i++)
                if (t.charAt(i) == '(' || t.charAt(i) == ')')
                    nxt.add(t.substring(0, i) + t.substring(i + 1));
        level = nxt;
    }
}
boolean valid(String t) {
    int cnt = 0;
    for (char c : t.toCharArray()) {
        if (c == '(') cnt++;
        else if (c == ')' && --cnt < 0) return false;
    }
    return cnt == 0;
}""",
        "time": "最坏 O(n · 2^n)，但剪枝与去重后通常很快",
        "space": "O(n · 层状态数)",
        "pitfalls": [
            ("BFS 而非 DFS", "DFS 会先搜到删除更多的解，BFS 保证「最少删除」"),
            ("visited 去重", "不同删法可能得到同一串，必须用 set 去重"),
        ],
        "selfcheck": [
            ("合法判断", "遍历中计数不能为负，结束时计数必须为 0，二者缺一不可。"),
            ("含字母怎么办？", "字母原样保留，只对括号做删除候选。"),
        ],
    },
    # ---------------------------------------------------------------- 94
    {
        "id": 94,
        "title": "买卖股票最佳时机含冷冻期",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 309,
        "origin": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/",
        "why": "卖出后次日不能买入。用三状态 DP：hold（持有）、sold（刚卖出）、rest（空仓休息）。每天三态互相转移，最终答案是 max(sold, rest)。",
        "desc": """<p>可以多次买卖，但卖出后存在<strong>一天冷冻期</strong>：卖出股票的次日不能买入。求最大利润。</p>
<p><strong>示例：</strong><br><code>[1,2,3,0,2]</code> → <code>3</code>（买 1 卖 2、冷冻、买 0 卖 2）</p>""",
        "frames": [
            frame("① 三状态：持有 hold / 刚卖 sold / 空仓 rest", "drawTable",
                  headers=["天", "1", "2", "3", "0", "2"],
                  rows=[["hold", "-1", "-1", "-1", "1", "1"], ["sold", "0", "1", "2", "-1", "3"], ["rest", "0", "0", "1", "2", "2"]], width=520, height=160),
            frame("② 状态转移", "drawTable",
                  headers=["转移", "公式"],
                  rows=[["持有", "max(昨天持有, 昨天空仓 - 今日价)"], ["刚卖", "昨天持有 + 今日价"], ["空仓", "max(昨天空仓, 昨天刚卖)"]], width=540, height=160),
            frame("③ 答案 = max(sold, rest) = 3", "drawTwoPointers", arr=[1, 2, 3, 0, 2], left=0, right=1, window={"start": 0, "end": 1}, width=520, height=140),
        ],
        "conclusion": "冷冻期体现在「买入只能来自空仓状态」，即不能昨天刚卖今天买。",
        "py": """def maxProfit(prices):
    hold = float('-inf')
    sold = rest = 0
    for p in prices:
        new_hold = max(hold, rest - p)
        new_sold = hold + p
        new_rest = max(rest, sold)
        hold, sold, rest = new_hold, new_sold, new_rest
    return max(sold, rest)""",
        "java": """public int maxProfit(int[] prices) {
    int hold = Integer.MIN_VALUE, sold = 0, rest = 0;
    for (int p : prices) {
        int nh = Math.max(hold, rest - p);
        int ns = hold + p;
        int nr = Math.max(rest, sold);
        hold = nh; sold = ns; rest = nr;
    }
    return Math.max(sold, rest);
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("买入依赖 rest", "new_hold 用 rest-p 而非 sold-p，体现冷冻期"),
            ("状态同时更新", "先算新值再统一赋值，避免同一天状态串味"),
        ],
        "selfcheck": [
            ("为什么要有 sold 状态？", "若只有持有/空仓，无法表达「昨天刚卖今天不能买」，sold 专门标记刚卖出。"),
            ("最后一天可能持有吗？", "不可能是最优，答案取 max(sold, rest)，排除仍持有未卖出的情况。"),
        ],
    },
    # ---------------------------------------------------------------- 95
    {
        "id": 95,
        "title": "戳气球",
        "diff": "hard",
        "tags": ["DP"],
        "leetcode": 312,
        "origin": "https://leetcode.cn/problems/burst-balloons/",
        "why": "正着戳会改变邻居、子问题不独立。反过来：设 dp[i][j] 为「开区间 (i,j) 内能得到的最大硬币」，枚举最后戳的气球 k，dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j])。",
        "desc": """<p>有 n 个气球排成一排，每个气球上有数字 nums[i]。戳破第 i 个气球可得 <code>nums[i-1] * nums[i] * nums[i+1]</code> 枚硬币（越界处视为 1）。求最多硬币数。</p>
<p><strong>示例：</strong><br><code>[3,1,5,8]</code> → <code>167</code>（1→5→3→8 顺序）</p>""",
        "frames": [
            frame("① 两端补 1，dp[i][j] 为开区间 (i,j) 最大硬币", "drawTable",
                  headers=["", "1", "3", "1", "5", "8", "1"],
                  rows=[["补1后", "1", "3", "1", "5", "8", "1"]], width=560, height=110),
            frame("② 枚举最后戳 k：dp[i][j]=dp[i][k]+dp[k][j]+nums[i]*nums[k]*nums[j]", "drawTable",
                  headers=["区间", "最后戳 k", "两侧", "金币"],
                  rows=[["(0,2)", "k=1(值3)", "1*3*1", "3"]], width=500, height=130),
            frame("③ 按区间长度递增填表，答案 dp[0][n+1]", "drawTable",
                  headers=["", "答案"],
                  rows=[["最大硬币", {"val": "167", "highlight": True}]], width=420, height=110),
        ],
        "conclusion": "把「最后戳谁」当决策点，两侧区间互不影响，区间 DP 经典模型。",
        "py": """def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
    return dp[0][n - 1]""",
        "java": """public int maxCoins(int[] nums) {
    int m = nums.length;
    int[] a = new int[m + 2];
    a[0] = a[m + 1] = 1;
    System.arraycopy(nums, 0, a, 1, m);
    int n = m + 2;
    int[][] dp = new int[n][n];
    for (int len = 3; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            for (int k = i + 1; k < j; k++)
                dp[i][j] = Math.max(dp[i][j], dp[i][k] + dp[k][j] + a[i] * a[k] * a[j]);
        }
    return dp[0][n - 1];
}""",
        "time": "O(n³)",
        "space": "O(n²)",
        "pitfalls": [
            ("枚举「最后戳」而非「第一个戳」", "戳第一个会改变两侧邻居，子问题耦合；最后戳则两侧已固定为 i、j"),
            ("两端补 1", "越界视为 1，补 1 后公式统一"),
        ],
        "selfcheck": [
            ("为什么区间长度从 3 开始？", "开区间 (i,j) 至少要有中间一个气球 k，即 j-i≥2。"),
            ("回溯思路 vs 正着贪心？", "贪心不行；区间 DP 把「最后戳谁」作为划分，保证子问题独立。"),
        ],
    },
    # ---------------------------------------------------------------- 96
    {
        "id": 96,
        "title": "零钱兑换",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 322,
        "origin": "https://leetcode.cn/problems/coin-change/",
        "why": "凑出金额 i 的最少硬币数 dp[i] = min(dp[i - coin]) + 1。完全背包模型，硬币可无限用，逐金额填表，无法凑出则 -1。",
        "desc": """<p>给定不同面额的硬币 <code>coins</code> 和一个总金额 <code>amount</code>，计算凑出该金额所需的最少硬币个数。无解返回 -1。</p>
<p><strong>示例：</strong><br><code>coins=[1,2,5], amount=11</code> → <code>3</code>（5+5+1）；<code>coins=[2], amount=3</code> → <code>-1</code></p>""",
        "frames": [
            frame("① dp[i] = min(dp[i-coin]) + 1", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
                  rows=[["dp", "0", "1", "1", "2", "2", "1", "2", "2", "3", "3", "2", "3"]], width=800, height=130),
            frame("② amount=11：11-5=6(dp=2)、11-2=9(dp=3)、11-1=10(dp=2)，min=2+1=3", "drawTable",
                  headers=["选硬币", "剩余", "剩余 dp", "总数"],
                  rows=[["1", "10", "2", "3"], ["2", "9", "3", "4"], ["5", "6", "2", "3"]], width=460, height=160),
        ],
        "conclusion": "每种硬币都试一遍，取「剩余金额最优 + 1」的最小值。",
        "py": """def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if i >= c:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
        "java": """public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++)
        for (int c : coins)
            if (i >= c) dp[i] = Math.min(dp[i], dp[i - c] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}""",
        "time": "O(amount · len(coins))",
        "space": "O(amount)",
        "pitfalls": [
            ("无解返回 -1", "用 amount+1 或 inf 初始化，最后判断是否被更新"),
            ("硬币可重复使用", "内层是金额循环，每个金额重新遍历所有硬币，等价完全背包"),
        ],
        "selfcheck": [
            ("coins=[2], amount=3？", "dp[3] 一直无法更新（3-2=1 无解），返回 -1。"),
            ("最少个数 vs 组合总数？", "本题求最少（取 min）；组合总数是另一个经典 DP，求累加和。"),
        ],
    },
    # ---------------------------------------------------------------- 97
    {
        "id": 97,
        "title": "打家劫舍 III",
        "diff": "medium",
        "tags": ["树", "DP"],
        "leetcode": 337,
        "origin": "https://leetcode.cn/problems/house-robber-iii/",
        "why": "房屋排成二叉树，父子不能同时偷。每个节点返回 (偷它, 不偷它) 两个值：偷 = 自己 + 左右「不偷」，不偷 = max(左偷/不偷) + max(右偷/不偷)。自底向上。",
        "desc": """<p>所有房屋排成一棵二叉树，相邻（直接相连）房屋被同时闯入会报警。求能偷到的最高金额。</p>
<p><strong>示例：</strong><br><code>[3,2,3,null,3,null,1]</code> → <code>7</code>（偷 3+3+1）</p>""",
        "frames": [
            frame("① 每个节点返回 (偷, 不偷)", "drawTree",
                  nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "2", "x": 160, "y": 110}, {"val": "3", "x": 440, "y": 110, "highlight": "done"}, {"val": "3", "x": 210, "y": 200, "highlight": "done"}, {"val": "1", "x": 480, "y": 200}],
                  edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 210, "y2": 200}, {"x1": 440, "y1": 110, "x2": 480, "y2": 200}], width=560, height=240),
            frame("② 偷 = 自己 + 左右不偷；不偷 = max(左) + max(右)", "drawTable",
                  headers=["节点", "偷", "不偷"],
                  rows=[["叶 3", "3", "0"], ["节点 2", "2+3=5", "3"], ["根 3", "3+0+? 看子树", "…"]], width=460, height=170),
        ],
        "conclusion": "树形 DP 自底向上，每个节点维护「偷/不偷」两个状态，根取较大者。",
        "py": """def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)
        lt, lf = dfs(node.left)
        rt, rf = dfs(node.right)
        take = node.val + lf + rf          # 偷：左右都不能偷
        skip = max(lt, lf) + max(rt, rf)   # 不偷：左右各自取最大
        return (take, skip)
    return max(dfs(root))""",
        "java": """public int rob(TreeNode root) {
    int[] res = dfs(root);
    return Math.max(res[0], res[1]);
}
int[] dfs(TreeNode n) {
    if (n == null) return new int[]{0, 0};
    int[] l = dfs(n.left), r = dfs(n.right);
    int take = n.val + l[1] + r[1];
    int skip = Math.max(l[0], l[1]) + Math.max(r[0], r[1]);
    return new int[]{take, skip};
}""",
        "time": "O(n)",
        "space": "O(h)",
        "pitfalls": [
            ("偷必须跳过孩子", "take = 自己 + 左右「不偷」值，不是 max(左右)"),
            ("不偷时孩子可偷可不偷", "skip 对每个孩子取 max(偷, 不偷)"),
        ],
        "selfcheck": [
            ("为什么自底向上？", "父节点的决策依赖孩子两个状态，必须先把子树算完。"),
            ("根节点答案？", "返回 max(根偷, 根不偷)。"),
        ],
    },
    # ---------------------------------------------------------------- 98
    {
        "id": 98,
        "title": "前K个高频元素",
        "diff": "medium",
        "tags": ["堆"],
        "leetcode": 347,
        "origin": "https://leetcode.cn/problems/top-k-frequent-elements/",
        "why": "先统计频率，再用大小为 k 的最小堆维护「频率最高的 k 个」：堆满且新频率更高就替换。最后堆里就是答案，时间 O(n log k)。",
        "desc": """<p>给定整数数组和整数 <code>k</code>，返回出现频率<strong>前 k 高</strong>的元素。</p>
<p><strong>示例：</strong><br><code>[1,1,1,2,2,3], k=2</code> → <code>[1,2]</code></p>""",
        "frames": [
            frame("① 统计频率", "drawTable",
                  headers=["元素", "1", "2", "3"],
                  rows=[["频率", "3", "2", "1"]], width=420, height=110),
            frame("② 维护大小为 k 的最小堆（按频率）", "drawTable",
                  headers=["元素", "频率", "是否在堆"],
                  rows=[["1", "3", "✓"], ["2", "2", "✓"], ["3", "1", "被淘汰"]], width=460, height=150),
            frame("③ 堆中即前 k 高 [1,2]", "drawTable",
                  headers=["", "元素"],
                  rows=[["前 2 高", "1, 2"]], width=420, height=110),
        ],
        "conclusion": "最小堆按频率排序，堆顶是「前 k 高里最低的」，低于它的直接淘汰。",
        "py": """import heapq
from collections import Counter
def topKFrequent(nums, k):
    freq = Counter(nums)
    heap = []
    for num, cnt in freq.items():
        heapq.heappush(heap, (cnt, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for cnt, num in heap]""",
        "java": """public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    PriorityQueue<Integer> pq = new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
    for (int x : freq.keySet()) {
        pq.offer(x);
        if (pq.size() > k) pq.poll();
    }
    int[] ans = new int[k];
    for (int i = 0; i < k; i++) ans[i] = pq.poll();
    return ans;
}""",
        "time": "O(n log k)",
        "space": "O(n)",
        "pitfalls": [
            ("堆按频率比较", "堆元素是 (cnt, num) 或自定义比较器，别按元素值比较"),
            ("堆满即弹最小", "维护 k 个最高频，弹掉堆顶（频率最低者）"),
        ],
        "selfcheck": [
            ("桶排序做法？", "按频率分桶（下标=频率），从高到低收集，O(n)，适合频率范围小的情况。"),
            ("频率相同怎么排序？", "顺序无所谓，题目不要求同频元素的具体次序。"),
        ],
    },
    # ---------------------------------------------------------------- 99
    {
        "id": 99,
        "title": "字符串解码",
        "diff": "medium",
        "tags": ["栈"],
        "leetcode": 394,
        "origin": "https://leetcode.cn/problems/decode-string/",
        "why": "嵌套结构（如 3[a2[c]]）适合栈。遇到数字、字符就累积，遇到 '[' 把当前倍数和已累积串入栈，遇到 ']' 弹出倍数与前置串拼接。",
        "desc": """<p>给定编码字符串，返回解码后的字符串。规则：<code>k[encoded_string]</code> 表示方括号内字符串重复 k 次。可以嵌套。</p>
<p><strong>示例：</strong><br><code>"3[a]2[bc]"</code> → <code>"aaabcbc"</code>；<code>"3[a2[c]]"</code> → <code>"accaccacc"</code></p>""",
        "frames": [
            frame("① 遇 '[' 把倍数与已累积串压栈", "drawStack",
                  items=[{"val": "3"}, {"val": ""}], type="stack", height=140),
            frame("② 遇 ']' 弹出，拼接 repeat", "drawTable",
                  headers=["步骤", "栈", "结果"],
                  rows=[["读 3[a2[c", "3,'' ; 2,'a'", ""], ["读 ]", "3,''", "a+2c=acc"], ["读 ]", "", "acc×3"]], width=500, height=170),
            frame("③ 结果 accaccacc", "drawTable",
                  headers=["", "结果"],
                  rows=[["解码", {"val": "accaccacc", "highlight": True}]], width=460, height=110),
        ],
        "conclusion": "栈保存「进入括号前的上下文」，遇到右括号就把括号内容按倍数展开拼回去。",
        "py": """def decodeString(s):
    stack = []
    cur = ''
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == '[':
            stack.append((cur, num))   # 保存上下文
            cur, num = '', 0
        elif ch == ']':
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur""",
        "java": """public String decodeString(String s) {
    Deque<String> strStack = new ArrayDeque<>();
    Deque<Integer> numStack = new ArrayDeque<>();
    StringBuilder cur = new StringBuilder();
    int num = 0;
    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) num = num * 10 + (c - '0');
        else if (c == '[') { strStack.push(cur.toString()); numStack.push(num); cur = new StringBuilder(); num = 0; }
        else if (c == ']') { String prev = strStack.pop(); int k = numStack.pop(); StringBuilder t = new StringBuilder(prev); for (int i = 0; i < k; i++) t.append(cur); cur = t; }
        else cur.append(c);
    }
    return cur.toString();
}""",
        "time": "O(输出长度) — 每个字符处理一次",
        "space": "O(嵌套深度) — 栈",
        "pitfalls": [
            ("数字可能是多位", "num = num*10 + digit，不能只读一位"),
            ("入栈保存上下文", "'[' 时保存当前串与倍数，' ]' 时弹出拼接"),
        ],
        "selfcheck": [
            ("嵌套 3[a2[c]] 过程？", "内层 2[c] 先解为 cc，再 a+cc=acc，最后 ×3 得 accaccacc。"),
            ("递归写法？", "可以用递归：读到 '[' 递归解码括号内容，读到 ']' 返回，思路对称。"),
        ],
    },
    # ---------------------------------------------------------------- 100
    {
        "id": 100,
        "title": "除法求值",
        "diff": "medium",
        "tags": ["图"],
        "leetcode": 399,
        "origin": "https://leetcode.cn/problems/evaluate-division/",
        "why": "把每个变量看成图节点，a/b=2 既是 a→b 权 2、又是 b→a 权 1/2。查询 a/c 就是图上 a 到 c 的路径权值之积，用 BFS/DFS 求路径。",
        "desc": """<p>给定变量对数组 <code>equations</code> 和实数值数组 <code>values</code>，其中 equations[i]=[A,B] 表示 A/B=values[i]。再给定查询 queries，返回每个查询的结果，无法确定则 -1。</p>
<p><strong>示例：</strong><br><code>[["a","b"],["b","c"]], values=[2,3], queries=[["a","c"],["b","a"]]</code> → <code>[6.0, 0.5]</code></p>""",
        "frames": [
            frame("① 建图：a→b 权 2，b→a 权 1/2", "drawGraph",
                  vertices=[{"label": "a", "x": 100, "y": 150, "color": "active"}, {"label": "b", "x": 300, "y": 150, "color": "visited"}, {"label": "c", "x": 500, "y": 150, "color": "unvisited"}],
                  edges=[{"from": "a", "to": "b", "weight": "2"}, {"from": "b", "to": "c", "weight": "3"}], width=600, height=220),
            frame("② a/c = a→b→c 权值相乘 = 2×3=6", "drawTable",
                  headers=["查询", "路径", "结果"],
                  rows=[["a/c", "a→b→c", "2×3=6"], ["b/a", "b→a", "1/2=0.5"]], width=460, height=140),
        ],
        "conclusion": "除法关系组成带权无向图，查询就是两点间路径权值乘积。",
        "py": """from collections import defaultdict, deque
def calcEquation(equations, values, queries):
    g = defaultdict(dict)
    for (a, b), v in zip(equations, values):
        g[a][b] = v
        g[b][a] = 1 / v
    def bfs(s, t):
        if s not in g or t not in g:
            return -1.0
        q = deque([(s, 1.0)])
        seen = {s}
        while q:
            node, val = q.popleft()
            if node == t:
                return val
            for nxt, w in g[node].items():
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, val * w))
        return -1.0
    return [bfs(s, t) for s, t in queries]""",
        "java": """public double[] calcEquation(List<List<String>> eq, double[] vals, List<List<String>> qs) {
    Map<String, Map<String, Double>> g = new HashMap<>();
    for (int i = 0; i < eq.size(); i++) {
        String a = eq.get(i).get(0), b = eq.get(i).get(1);
        g.computeIfAbsent(a, k -> new HashMap<>()).put(b, vals[i]);
        g.computeIfAbsent(b, k -> new HashMap<>()).put(a, 1 / vals[i]);
    }
    double[] ans = new double[qs.size()];
    for (int i = 0; i < qs.size(); i++)
        ans[i] = bfs(g, qs.get(i).get(0), qs.get(i).get(1));
    return ans;
}
double bfs(Map<String, Map<String, Double>> g, String s, String t) {
    if (!g.containsKey(s) || !g.containsKey(t)) return -1.0;
    Queue<Object[]> q = new LinkedList<>();
    Set<String> seen = new HashSet<>();
    q.offer(new Object[]{s, 1.0}); seen.add(s);
    while (!q.isEmpty()) {
        Object[] cur = q.poll();
        String node = (String) cur[0]; double val = (Double) cur[1];
        if (node.equals(t)) return val;
        for (Map.Entry<String, Double> e : g.get(node).entrySet())
            if (seen.add(e.getKey())) q.offer(new Object[]{e.getKey(), val * e.getValue()});
    }
    return -1.0;
}""",
        "time": "O(q · (V+E)) — 每个查询一次 BFS",
        "space": "O(V+E)",
        "pitfalls": [
            ("反向边取倒数", "a/b=v 必须同时建 b/a=1/v，否则单向不连通"),
            ("未知变量返回 -1", "查询端点不在图中直接 -1.0"),
        ],
        "selfcheck": [
            ("Floyd 预处理？", "可以预计算所有点对最短路（这里是权值积），把每个查询降到 O(1)。"),
            ("结果精度？", "浮点除法有精度误差，题目用容差判断，返回 double 即可。"),
        ],
    },
]

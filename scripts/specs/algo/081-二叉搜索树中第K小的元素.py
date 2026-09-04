from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 中序遍历顺序：1,2,3,4", "drawTree", nodes=[{"val": "3", "x": 300, "y": 25}, {"val": "1", "x": 160, "y": 110}, {"val": "4", "x": 440, "y": 110}, {"val": "2", "x": 210, "y": 200, "highlight": "done"}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 210, "y2": 200}], width=520, height=240),
    frame("② 第 k 个访问到的即第 k 小", "drawTable", headers=["次序", "1", "2", "3", "4"], rows=[["节点", "1", "2", "3", "4"]], width=460, height=110),
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
    "pitfalls": [["中序第 k 个", "中序严格递增是前提，遍历到第 k 个返回"], ["迭代避免全遍历", "找到第 k 个立刻返回，不必走完整棵树"]],
    "selfcheck": [["k 越界？", "题目保证 k 有效（1 ≤ k ≤ 节点数），无需处理。"], ["进阶：频繁插入删除的 BST？", "给节点维护「左子树大小」计数，O(h) 定位第 k 小。"]],
}

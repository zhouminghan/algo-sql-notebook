from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 第一层只有根 3", "drawTree", nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110}, {"val": "15", "x": 380, "y": 200}, {"val": "7", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
    frame("② 队列逐层处理：每层一次性取完", "drawStack", items=[{"val": "3"}, {"val": "9"}, {"val": "20"}], type="queue", height=160),
    frame("③ 结果 [[3],[9,20],[15,7]]", "drawTable", headers=["层", "值"], rows=[["0", "3"], ["1", "9, 20"], ["2", "15, 7"]], width=420, height=160),
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
    "pitfalls": [["用 len(q) 固定层大小", "循环里队列在变，必须先用 size 记录当前层节点数，否则层边界会混"], ["空树返回 []", "root 为 None 直接返回空列表"]],
    "selfcheck": [["怎么按「之字形」遍历？", "在每层收集后根据奇偶层反转 level 即可，其余逻辑不变。"], ["DFS 能做层序吗？", "可以，递归时带上 depth 参数，把值追加到对应层的列表。"]],
}

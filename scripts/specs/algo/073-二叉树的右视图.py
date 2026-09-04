from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 每层最右的节点进入右视图", "drawTree", nodes=[{"val": "1", "x": 300, "y": 25, "highlight": "active"}, {"val": "2", "x": 160, "y": 110}, {"val": "3", "x": 440, "y": 110, "highlight": "active"}, {"val": "5", "x": 200, "y": 200}, {"val": "4", "x": 480, "y": 200, "highlight": "active"}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 200, "y2": 200}, {"x1": 440, "y1": 110, "x2": 480, "y2": 200}], width=560, height=240),
    frame("② 层序遍历取每层最后一个", "drawTable", headers=["层", "节点", "右视图"], rows=[["0", "1", "1"], ["1", "2, 3", "3"], ["2", "5, 4", "4"]], width=460, height=160),
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
    "pitfalls": [["取每层最后一个", "i == size-1 时收集，不是第一个"], ["空树返回 []", "root 为 None 直接返回空"]],
    "selfcheck": [["DFS 能做吗？", "可以，先右后左的 DFS，每个深度第一次访问到的节点就是右视图。"], ["为什么不用「一直往右走」？", "右视图不一定是右链，左子树的右子节点也可能被看到，必须逐层判断。"]],
}

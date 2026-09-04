from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 中序：左 → 根 → 右", "drawTree", nodes=[{"val": "1", "x": 300, "y": 40}, {"val": "2", "x": 420, "y": 130, "highlight": "active"}, {"val": "3", "x": 360, "y": 220, "highlight": "done"}], edges=[{"x1": 300, "y1": 40, "x2": 420, "y2": 130}, {"x1": 420, "y1": 130, "x2": 360, "y2": 220}], width=520, height=260),
    frame("② 迭代：一直向左压栈，到底后弹出访问，再转右", "drawStack", items=[{"val": "1"}, {"val": "2"}], type="stack", height=160),
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
    "pitfalls": [["遍历顺序", "先递归左子树、再访问根、最后右子树，顺序记牢"], ["迭代的 cur 移动", "压栈时 cur=cur.left，弹出访问后 cur=cur.right，缺一步就死循环"]],
    "selfcheck": [["空树？", "root 为 None，直接返回空列表。"], ["前序、后序与中序差在哪？", "只差「访问根」的时机：前序在入栈前访问，中序在出栈时访问，后序在左右都处理完再访问。"]],
}

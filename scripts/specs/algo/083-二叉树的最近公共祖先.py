from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 自底向上：左右各找到一个，当前即 LCA", "drawTree", nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "5", "x": 160, "y": 110, "highlight": "done"}, {"val": "1", "x": 440, "y": 110, "highlight": "done"}, {"val": "6", "x": 100, "y": 200}, {"val": "2", "x": 220, "y": 200}, {"val": "0", "x": 380, "y": 200}, {"val": "8", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
    frame("② 只一边找到，继续上抛", "drawTable", headers=["情况", "返回值"], rows=[["当前是 p/q", "当前节点"], ["两边都有", "当前节点(LCA)"], ["只有一边", "那一侧的结果"]], width=500, height=160),
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
    "pitfalls": [["返回条件", "root 为 p 或 q 直接返回，意味着「找到了」向上传递"], ["两边会师", "left 和 right 都非空时当前节点就是 LCA"]],
    "selfcheck": [["p 是 q 的祖先？", "递归到 p 直接返回 p，上层继续上抛 p，结果正确。"], ["p、q 都在同一侧？", "只有那一侧返回值非空，继续上抛，直到某一层两侧都命中。"]],
}

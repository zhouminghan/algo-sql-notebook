from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 深度 = 1 + max(左深, 右深)", "drawTree", nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110}, {"val": "15", "x": 380, "y": 200, "highlight": "done"}, {"val": "7", "x": 500, "y": 200, "highlight": "done"}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
    frame("② 自底向上：叶子深 1，逐层 +1", "drawTable", headers=["节点", "左深", "右深", "深度"], rows=[["15", "0", "0", "1"], ["20", "1", "1", "2"], ["3", "1", "2", "3"]], width=460, height=170),
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
    "pitfalls": [["空节点返回 0", "否则空树会崩"], ["别和「最小深度」搞混", "最小深度还要处理单侧为空的情况，不是简单 min"]],
    "selfcheck": [["空树深度？", "0。"], ["一条链（退化链表）呢？", "深度就是节点个数 n，递归栈深度 O(n)。"]],
}

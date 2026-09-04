from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 镜像比较：左.left vs 右.right，左.right vs 右.left", "drawTree", nodes=[{"val": "1", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110, "highlight": "active"}, {"val": "2", "x": 440, "y": 110, "highlight": "active"}, {"val": "3", "x": 100, "y": 200}, {"val": "4", "x": 220, "y": 200}, {"val": "4", "x": 380, "y": 200}, {"val": "3", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
    frame("② 递归比较镜像节点", "drawTable", headers=["对比对", "左", "右", "相等?"], rows=[["第一对", "2", "2", "✓"], ["第二对", "3", "3", "✓"], ["第三对", "4", "4", "✓"]], width=460, height=170),
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
    "pitfalls": [["比较的是镜像位置", "a.left 对应 b.right，a.right 对应 b.left，不是同名左右"], ["空节点成对判断", "一个空一个非空也返回 false，先判空再判值"]],
    "selfcheck": [["空树对称吗？", "对称，直接返回 true。"], ["[1,2,2,null,3,null,3] 为何 false？", "左侧 2 的右子 3 应对应右侧 2 的左子，但右侧没有左子，结构不对称。"]],
}

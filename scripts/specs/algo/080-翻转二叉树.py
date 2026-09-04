from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 原树", "drawTree", nodes=[{"val": "4", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110}, {"val": "7", "x": 440, "y": 110}, {"val": "1", "x": 100, "y": 200}, {"val": "3", "x": 220, "y": 200}, {"val": "6", "x": 380, "y": 200}, {"val": "9", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
    frame("② 交换每个节点的左右子树", "drawTree", nodes=[{"val": "4", "x": 300, "y": 25}, {"val": "7", "x": 160, "y": 110}, {"val": "2", "x": 440, "y": 110}, {"val": "9", "x": 100, "y": 200}, {"val": "6", "x": 220, "y": 200}, {"val": "3", "x": 380, "y": 200}, {"val": "1", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
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
    "pitfalls": [["先交换再递归", "交换当前节点后，左右子树位置已变，递归顺序仍各走一遍即可"], ["空树", "root 为 None 直接返回"]],
    "selfcheck": [["迭代做法？", "用队列做 BFS，每取出一个节点就交换其左右孩子。"], ["翻转两次？", "翻转两次回到原树，翻转是自身的逆操作。"]],
}

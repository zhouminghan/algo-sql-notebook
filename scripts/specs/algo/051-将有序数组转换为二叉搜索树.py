from scripts.algo_gen import frame

PROBLEM = {
    "id": 51,
    "title": "将有序数组转换为二叉搜索树",
    "diff": "easy",
    "tags": ["BST"],
    "leetcode": 108,
    "origin": "https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/",
    "why": "要构造「高度平衡」的 BST，就每次取区间中点作为根，左半段建左子树、右半段建右子树，递归即可，天然平衡。",
    "desc": """<p>给定一个<strong>升序</strong>数组，将其转换为一棵<strong>高度平衡</strong>的二叉搜索树。高度平衡指每个节点左右子树高度差绝对值不超过 1。</p>
<p><strong>示例：</strong><br><code>[-10,-3,0,5,9]</code> → 一种答案为 <code>[0,-3,9,-10,null,5]</code></p>""",
    "frames": [
    frame("① 取中点 0 作根", "drawTable", headers=["下标", "0", "1", "2", "3", "4"], rows=[["数组", "-10", "-3", "0", "5", "9"], ["根", "", "", {"val": "0", "highlight": True}, "", ""]], width=500, height=130),
    frame("② 左半 [-10,-3] 中点 -3 作左根，右半 [5,9] 中点 5 作右根", "drawTree", nodes=[{"val": "0", "x": 300, "y": 25}, {"val": "-3", "x": 160, "y": 110}, {"val": "5", "x": 440, "y": 110}, {"val": "-10", "x": 100, "y": 200}, {"val": "9", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
    ],
    "conclusion": "中点作根 + 左右递归，BST 有序性由数组有序性保证，平衡性由二分保证。",
    "py": """def sortedArrayToBST(nums):
    def build(l, r):
        if l > r:
            return None
        m = (l + r) // 2
        root = TreeNode(nums[m])
        root.left = build(l, m - 1)
        root.right = build(m + 1, r)
        return root
    return build(0, len(nums) - 1)""",
    "java": """public TreeNode sortedArrayToBST(int[] nums) {
    return build(nums, 0, nums.length - 1);
}
TreeNode build(int[] nums, int l, int r) {
    if (l > r) return null;
    int m = (l + r) >>> 1;
    TreeNode root = new TreeNode(nums[m]);
    root.left = build(nums, l, m - 1);
    root.right = build(nums, m + 1, r);
    return root;
}""",
    "time": "O(n) — 每个元素建一个节点",
    "space": "O(log n) — 递归栈（平衡树）",
    "pitfalls": [["中点取整", "偶数长度取偏左或偏右都行，结果不唯一，都是合法平衡 BST"], ["递归边界", "l > r 表示区间空，返回 None；含等号时只剩一个节点"]],
    "selfcheck": [["答案唯一吗？", "不唯一。中点取 (l+r)//2 或 (l+r+1)//2 会得到不同但都合法的平衡 BST。"], ["为什么天然高度平衡？", "每次二分把区间对半切，左右子树规模最多差 1。"]],
}

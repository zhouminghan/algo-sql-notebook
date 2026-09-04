from scripts.algo_gen import frame

PROBLEM = {
    "id": 46,
    "title": "验证二叉搜索树",
    "diff": "medium",
    "tags": ["BST"],
    "leetcode": 98,
    "origin": "https://leetcode.cn/problems/validate-binary-search-tree/",
    "why": "BST 要求「整棵左子树都小于根、整棵右子树都大于根」，只比较父子是不够的。递归时携带 (min, max) 上下界，把每个节点约束在开区间内。",
    "desc": """<p>给定二叉树的根节点，判断其是否是一个有效的二叉搜索树。有效 BST 定义：节点的左子树只含<strong>小于</strong>当前节点的数；右子树只含<strong>大于</strong>当前节点的数；所有左右子树自身也必须是 BST。</p>
<p><strong>示例：</strong><br><code>[2,1,3]</code> → <code>true</code>；<code>[5,1,4,null,null,3,6]</code> → <code>false</code></p>""",
    "frames": [
    frame("① 每个节点必须落在 (min, max) 区间内", "drawTree", nodes=[{"val": "5", "x": 300, "y": 30}, {"val": "1", "x": 170, "y": 120}, {"val": "4", "x": 430, "y": 120, "highlight": "active"}, {"val": "3", "x": 360, "y": 210, "highlight": "done"}, {"val": "6", "x": 500, "y": 210}], edges=[{"x1": 300, "y1": 30, "x2": 170, "y2": 120}, {"x1": 300, "y1": 30, "x2": 430, "y2": 120}, {"x1": 430, "y1": 120, "x2": 360, "y2": 210}, {"x1": 430, "y1": 120, "x2": 500, "y2": 210}], width=560, height=250),
    frame("② 只比较父子不够：3 虽小于父 4，但小于祖 5，越界", "drawTable", headers=["节点", "应在区间", "实际", "合法?"], rows=[["5", "(-∞,+∞)", "5", "✓"], ["4", "(5,+∞)", "4", "✓"], ["3", "(5,+∞)", "3", "✗"]], width=500, height=170),
    ],
    "conclusion": "递归时把祖先的约束作为上下界一路传下去，任何节点越界即判非法。",
    "py": """def isValidBST(root):
    def check(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))""",
    "java": """public boolean isValidBST(TreeNode root) {
    return check(root, null, null);
}
boolean check(TreeNode n, Integer lo, Integer hi) {
    if (n == null) return true;
    if (lo != null && n.val <= lo) return false;
    if (hi != null && n.val >= hi) return false;
    return check(n.left, lo, n.val) && check(n.right, n.val, hi);
}""",
    "time": "O(n) — 每个节点访问一次",
    "space": "O(h) — 递归栈",
    "pitfalls": [["必须带上下界", "只判断 node.left < node < node.right 无法发现「右子树里有比根小的数」"], ["中序遍历法", "BST 中序遍历应严格递增，也可以边遍历边比较前驱，但需处理相等"]],
    "selfcheck": [["节点值相等算 BST 吗？", "不算。左子树必须「严格小于」、右子树「严格大于」，相等直接非法。"], ["[5,1,4,null,null,3,6] 为何 false？", "4 的右子树里有 3，而 3 < 根 5，违反了「右子树全部大于根」的约束。"]],
}

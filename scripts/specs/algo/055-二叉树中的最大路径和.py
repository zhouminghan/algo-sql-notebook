from scripts.algo_gen import frame

PROBLEM = {
    "id": 55,
    "title": "二叉树中的最大路径和",
    "diff": "hard",
    "tags": ["树"],
    "leetcode": 124,
    "origin": "https://leetcode.cn/problems/binary-tree-maximum-path-sum/",
    "why": "路径可以不过根、只走一部分。递归时每个节点返回「以它为起点向下延伸的最大单边和」，同时用「左单边 + 自己 + 右单边」更新全局最大，负数边直接舍弃。",
    "desc": """<p>二叉树中的路径，是任意节点间、每个节点至多经过一次的序列。路径和是路径上节点值的总和。返回所有路径中的最大路径和。</p>
<p><strong>示例：</strong><br><code>[1,2,3]</code> → <code>6</code>（2→1→3）；<code>[-10,9,20,null,null,15,7]</code> → <code>42</code>（15→20→7）</p>""",
    "frames": [
    frame("① 每个节点返回「向下最大单边和」", "drawTree", nodes=[{"val": "-10", "x": 300, "y": 25}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110, "highlight": "active"}, {"val": "15", "x": 380, "y": 200, "highlight": "done"}, {"val": "7", "x": 500, "y": 200, "highlight": "done"}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
    frame("② 20 的左右单边 15、7 都为正，弯折路径 15+20+7=42", "drawTable", headers=["节点", "左单边", "右单边", "弯折和"], rows=[["20", "15", "7", {"val": "42", "highlight": True}], ["-10", "9", "35", "34"]], width=500, height=140),
    ],
    "conclusion": "单边和 = max(0, 左单边) + max(0, 右单边) + 自身 更新答案；返回值只取较大一侧 + 自身。",
    "py": """def maxPathSum(root):
    ans = [float('-inf')]
    def dfs(node):
        if not node:
            return 0
        left = max(dfs(node.left), 0)    # 负边舍弃
        right = max(dfs(node.right), 0)
        ans[0] = max(ans[0], left + right + node.val)  # 弯折路径
        return max(left, right) + node.val             # 向上单边
    dfs(root)
    return ans[0]""",
    "java": """int ans = Integer.MIN_VALUE;
public int maxPathSum(TreeNode root) {
    dfs(root);
    return ans;
}
int dfs(TreeNode n) {
    if (n == null) return 0;
    int l = Math.max(dfs(n.left), 0);
    int r = Math.max(dfs(n.right), 0);
    ans = Math.max(ans, l + r + n.val);
    return Math.max(l, r) + n.val;
}""",
    "time": "O(n)",
    "space": "O(h)",
    "pitfalls": [["负贡献舍弃", "单边和与 0 取 max，负子树直接不选"], ["返回值与答案分开", "返回「单边」给父节点用，答案用「弯折」更新，二者不能混"]],
    "selfcheck": [["全负节点怎么办？", "单边都被 0 截断，答案最终取到最大的那个负节点值（如 -3 是最大值）。"], ["路径一定要经过根吗？", "不一定。答案是全局任意路径，这正是递归要在每个节点都更新 ans 的原因。"]],
}

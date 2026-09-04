from scripts.algo_gen import frame

PROBLEM = {
    "id": 97,
    "title": "打家劫舍 III",
    "diff": "medium",
    "tags": ["树", "DP"],
    "leetcode": 337,
    "origin": "https://leetcode.cn/problems/house-robber-iii/",
    "why": "房屋排成二叉树，父子不能同时偷。每个节点返回 (偷它, 不偷它) 两个值：偷 = 自己 + 左右「不偷」，不偷 = max(左偷/不偷) + max(右偷/不偷)。自底向上。",
    "desc": """<p>所有房屋排成一棵二叉树，相邻（直接相连）房屋被同时闯入会报警。求能偷到的最高金额。</p>
<p><strong>示例：</strong><br><code>[3,2,3,null,3,null,1]</code> → <code>7</code>（偷 3+3+1）</p>""",
    "frames": [
    frame("① 每个节点返回 (偷, 不偷)", "drawTree", nodes=[{"val": "3", "x": 300, "y": 25, "highlight": "active"}, {"val": "2", "x": 160, "y": 110}, {"val": "3", "x": 440, "y": 110, "highlight": "done"}, {"val": "3", "x": 210, "y": 200, "highlight": "done"}, {"val": "1", "x": 480, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 210, "y2": 200}, {"x1": 440, "y1": 110, "x2": 480, "y2": 200}], width=560, height=240),
    frame("② 偷 = 自己 + 左右不偷；不偷 = max(左) + max(右)", "drawTable", headers=["节点", "偷", "不偷"], rows=[["叶 3", "3", "0"], ["节点 2", "2+3=5", "3"], ["根 3", "3+0+? 看子树", "…"]], width=460, height=170),
    ],
    "conclusion": "树形 DP 自底向上，每个节点维护「偷/不偷」两个状态，根取较大者。",
    "py": """def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)
        lt, lf = dfs(node.left)
        rt, rf = dfs(node.right)
        take = node.val + lf + rf          # 偷：左右都不能偷
        skip = max(lt, lf) + max(rt, rf)   # 不偷：左右各自取最大
        return (take, skip)
    return max(dfs(root))""",
    "java": """public int rob(TreeNode root) {
    int[] res = dfs(root);
    return Math.max(res[0], res[1]);
}
int[] dfs(TreeNode n) {
    if (n == null) return new int[]{0, 0};
    int[] l = dfs(n.left), r = dfs(n.right);
    int take = n.val + l[1] + r[1];
    int skip = Math.max(l[0], l[1]) + Math.max(r[0], r[1]);
    return new int[]{take, skip};
}""",
    "time": "O(n)",
    "space": "O(h)",
    "pitfalls": [["偷必须跳过孩子", "take = 自己 + 左右「不偷」值，不是 max(左右)"], ["不偷时孩子可偷可不偷", "skip 对每个孩子取 max(偷, 不偷)"]],
    "selfcheck": [["为什么自底向上？", "父节点的决策依赖孩子两个状态，必须先把子树算完。"], ["根节点答案？", "返回 max(根偷, 根不偷)。"]],
}

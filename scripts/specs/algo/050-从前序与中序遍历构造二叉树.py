from scripts.algo_gen import frame

PROBLEM = {
    "id": 50,
    "title": "从前序与中序遍历构造二叉树",
    "diff": "medium",
    "tags": ["树"],
    "leetcode": 105,
    "origin": "https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/",
    "why": "前序的第一个元素必是根；在中序里找到根的位置，左边就是左子树、右边就是右子树。递归地切分两个序列，即可重建整棵树。",
    "desc": """<p>给定二叉树的前序遍历和中序遍历，构造并返回二叉树。假设树中没有重复元素。</p>
<p><strong>示例：</strong><br><code>preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]</code> → <code>[3,9,20,null,null,15,7]</code></p>""",
    "frames": [
    frame("① 前序第一个 3 是根，在中序里定位", "drawTable", headers=["序列", "值"], rows=[["preorder", "3,9,20,15,7"], ["inorder", "9,3,15,20,7"], ["根", "3"]], width=520, height=160),
    frame("② 中序里 3 左边 [9] 是左子树，右边 [15,20,7] 是右子树", "drawTable", headers=["", "左子树", "根", "右子树"], rows=[["inorder", "9", "3", "15,20,7"]], width=520, height=110),
    frame("③ 递归切分重建", "drawTree", nodes=[{"val": "3", "x": 300, "y": 25}, {"val": "9", "x": 160, "y": 110}, {"val": "20", "x": 440, "y": 110}, {"val": "15", "x": 380, "y": 200}, {"val": "7", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 440, "y1": 110, "x2": 380, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=560, height=240),
    ],
    "conclusion": "根 → 中序定位 → 切出左右子树 → 递归，直到区间为空。",
    "py": """def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    def build(pl, pr, il, ir):
        if pl > pr:
            return None
        root = TreeNode(preorder[pl])
        k = idx[root.val]
        left_size = k - il
        root.left = build(pl + 1, pl + left_size, il, k - 1)
        root.right = build(pl + left_size + 1, pr, k + 1, ir)
        return root
    return build(0, len(preorder) - 1, 0, len(inorder) - 1)""",
    "java": """Map<Integer, Integer> idx = new HashMap<>();
public TreeNode buildTree(int[] pre, int[] in) {
    for (int i = 0; i < in.length; i++) idx.put(in[i], i);
    return build(pre, in, 0, pre.length - 1, 0, in.length - 1);
}
TreeNode build(int[] pre, int[] in, int pl, int pr, int il, int ir) {
    if (pl > pr) return null;
    TreeNode root = new TreeNode(pre[pl]);
    int k = idx.get(root.val), left = k - il;
    root.left = build(pre, in, pl + 1, pl + left, il, k - 1);
    root.right = build(pre, in, pl + left + 1, pr, k + 1, ir);
    return root;
}""",
    "time": "O(n) — 哈希定位根 O(1)，每节点一次",
    "space": "O(n) — 哈希表 + 递归栈",
    "pitfalls": [["区间切分要对齐", "左子树大小 = k - il，前序里左子树区间是 pl+1 .. pl+left，算错一位全错"], ["用哈希加速定位", "每次线性 find 会退化成 O(n²)"]],
    "selfcheck": [["为什么前序+中序能唯一确定树？", "前序给根、中序给左右子树划分，层层递推唯一确定；只有前序+后序则不能唯一确定。"], ["树有重复元素呢？", "本题保证无重复；有重复则无法用哈希唯一定位根。"]],
}

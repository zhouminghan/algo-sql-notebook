from scripts.algo_gen import frame

PROBLEM = {
    "id": 52,
    "title": "二叉树展开为链表",
    "diff": "medium",
    "tags": ["树"],
    "leetcode": 114,
    "origin": "https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/",
    "why": "按「前序」的顺序把树展平成右链表。逆前序（右→左→根）遍历，用一个全局 prev 记录上一个访问节点，把当前节点右指针接到 prev、左指针置空即可，原地完成。",
    "desc": """<p>给定二叉树根节点，将其<strong>原地</strong>展开为单链表：展开后的链表顺序为前序遍历顺序，每个节点左指针为 null、右指针指向下一个节点。</p>
<p><strong>示例：</strong><br><code>[1,2,5,3,4,null,6]</code> → <code>[1,null,2,null,3,null,4,null,5,null,6]</code></p>""",
    "frames": [
    frame("① 原树：前序顺序 1→2→3→4→5→6", "drawTree", nodes=[{"val": "1", "x": 300, "y": 25}, {"val": "2", "x": 160, "y": 110}, {"val": "5", "x": 440, "y": 110}, {"val": "3", "x": 100, "y": 200}, {"val": "4", "x": 220, "y": 200}, {"val": "6", "x": 500, "y": 200}], edges=[{"x1": 300, "y1": 25, "x2": 160, "y2": 110}, {"x1": 300, "y1": 25, "x2": 440, "y2": 110}, {"x1": 160, "y1": 110, "x2": 100, "y2": 200}, {"x1": 160, "y1": 110, "x2": 220, "y2": 200}, {"x1": 440, "y1": 110, "x2": 500, "y2": 200}], width=600, height=240),
    frame("② 逆前序（右→左→根）串成右链", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 5, "highlight": "done"}, {"val": 6, "highlight": "done"}], width=640, height=90),
    ],
    "conclusion": "逆前序保证「下一个该接的节点」已经处理完，prev 始终指向链表头部。",
    "py": """def flatten(root):
    prev = [None]
    def dfs(node):
        if not node:
            return
        dfs(node.right)     # 逆前序：右
        dfs(node.left)      # 左
        node.right = prev[0]  # 根：接上已串好的链表
        node.left = None
        prev[0] = node
    dfs(root)""",
    "java": """TreeNode prev = null;
public void flatten(TreeNode root) {
    if (root == null) return;
    flatten(root.right);
    flatten(root.left);
    root.right = prev;
    root.left = null;
    prev = root;
}""",
    "time": "O(n)",
    "space": "O(h) — 递归栈",
    "pitfalls": [["左指针置空", "展平后每个节点 left 必须是 null，漏掉会残留旧结构"], ["先右后左", "逆前序顺序是 右→左→根，顺序错了链表次序不对"]],
    "selfcheck": [["为什么用逆前序而不是前序？", "前序先访问根时，它的右子树还没处理，根无法指向「已串好的后续」；逆序则保证后续已就绪。"], ["O(1) 额外空间做法？", "用「找左子树最右节点，把右子树挂过去」的原地拼接，可避免递归栈。"]],
}

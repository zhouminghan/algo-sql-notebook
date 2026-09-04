from scripts.algo_gen import frame

PROBLEM = {
    "id": 61,
    "title": "环形链表",
    "diff": "easy",
    "tags": ["快慢指针"],
    "leetcode": 141,
    "origin": "https://leetcode.cn/problems/linked-list-cycle/",
    "why": "快慢指针（Floyd 判圈）：慢指针走一步、快指针走两步。若无环，快指针先到 null；若有环，快慢指针必在环内相遇。",
    "desc": """<p>给定链表头节点，判断链表中是否有环。</p>
<p><strong>示例：</strong><br><code>[3,2,0,-4]</code>（尾部连接到下标 1）→ <code>true</code></p>""",
    "frames": [
    frame("① 慢指针走 1 步、快指针走 2 步", "drawLinkedList", nodes=[{"val": 3, "highlight": "active"}, {"val": 2}, {"val": 0}, {"val": -4}], pointers=[{"label": "slow", "x": 40, "y": 90, "targetX": 40, "targetY": 55, "color": "red"}, {"label": "fast", "x": 150, "y": 90, "targetX": 150, "targetY": 55, "color": "gray"}], width=560, height=120),
    frame("② 无环：fast 先到 null，返回 false", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 3, "showNull": True}], width=460, height=90),
    frame("③ 有环：快慢指针在环内必相遇", "drawTable", headers=["轮次", "slow 位置", "fast 位置"], rows=[["0", "3", "3"], ["1", "2", "0"], ["2", "0", "2"], ["3", "-4", "-4 相遇 ✓"]], width=460, height=190),
    ],
    "conclusion": "若有环，fast 相对 slow 每次逼近一步，必然追及；无环则 fast 先到空。",
    "py": """def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False""",
    "java": """public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}""",
    "time": "O(n) — 无环走到底；有环在 O(n) 步内相遇",
    "space": "O(1)",
    "pitfalls": [["循环条件", "while fast and fast.next 都要判空，否则 fast.next.next 空指针"], ["相遇即判环", "slow == fast 说明存在环，不需走到 null"]],
    "selfcheck": [["为什么快慢指针一定相遇？", "有环时快慢都进入环，fast 每次多走一步，两者距离逐步缩小到 0，必然追及。"], ["哈希表做法？", "遍历时把访问过的节点存 Set，遇到重复即说明有环，但空间 O(n)。"]],
}

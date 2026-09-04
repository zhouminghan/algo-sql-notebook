from scripts.algo_gen import frame

PROBLEM = {
    "id": 62,
    "title": "环形链表 II",
    "diff": "medium",
    "tags": ["快慢指针"],
    "leetcode": 142,
    "origin": "https://leetcode.cn/problems/linked-list-cycle-ii/",
    "why": "先快慢指针判环并找到相遇点，再把一个指针放回头节点，两个指针同速前进，再次相遇处就是环的入口。这是 Floyd 算法的经典结论。",
    "desc": """<p>给定链表头节点，返回链表开始入环的<strong>第一个节点</strong>。若无环，返回 null。</p>
<p><strong>示例：</strong><br><code>[3,2,0,-4]</code>（尾部连接下标 1）→ 返回节点 <code>2</code></p>""",
    "frames": [
    frame("① 快慢指针相遇（在环内某点）", "drawLinkedList", nodes=[{"val": 3}, {"val": 2, "highlight": "active"}, {"val": 0}, {"val": -4}], width=520, height=90),
    frame("② 一个指针放回头，两指针同速前进", "drawTable", headers=["步骤", "指针 A", "指针 B"], rows=[["0", "head(3)", "相遇点"], ["1", "2", "0"], ["2", "0", "-4"], ["3", "-4", "2"], ["4", "2", "2 相遇 ✓"]], width=460, height=220),
    frame("③ 相遇点即环入口 2", "drawLinkedList", nodes=[{"val": 3}, {"val": 2, "highlight": "done"}, {"val": 0}, {"val": -4}], width=520, height=90),
    ],
    "conclusion": "相遇点到入口的距离，恰好等于头到入口的距离，于是同速二刷即得入口。",
    "py": """def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            p = head
            while p != slow:
                p = p.next
                slow = slow.next
            return p
    return None""",
    "java": """public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next; fast = fast.next.next;
        if (slow == fast) {
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;
        }
    }
    return null;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["两阶段", "先判环找相遇点，再从头同速找入口，两步不能省"], ["无环返回 null", "快指针到空说明无环"]],
    "selfcheck": [["为什么从头同速走会相遇在入口？", "设头到入口 a、环长 b，相遇时 slow 走了 a+x，fast 走了 2(a+x)；快慢相遇条件推出「头到入口的距离 == 相遇点沿环到入口的距离」。"], ["环形链表 I 与 II 区别？", "I 只判有无环；II 要返回入口节点，多一次同速二刷。"]],
}

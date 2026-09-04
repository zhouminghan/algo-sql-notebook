from scripts.algo_gen import frame

PROBLEM = {
    "id": 10,
    "title": "删除链表的倒数第N个结点",
    "diff": "medium",
    "tags": ["链表", "双指针"],
    "leetcode": 19,
    "origin": "https://leetcode.cn/problems/remove-nth-node-from-end-of-list/",
    "why": "用 dummy 哨兵 + 快慢指针：fast 先走 n 步，然后 fast/slow 同步前进，fast 到末尾时 slow 正好在倒数第 n 个的前一个，直接跳过它。",
    "desc": "<p>给定链表头节点，删除链表<strong>倒数第 n 个</strong>结点，返回链表的头节点。</p><p><strong>示例：</strong><br><code>[1,2,3,4,5], n=2</code> → <code>[1,2,3,5]</code></p>",
    "frames": [
    frame("① fast 先走 n=2 步", "drawLinkedList", nodes=[{"val": "d"}, {"val": "1"}, {"val": "2"}, {"val": "3", "highlight": "active"}, {"val": "4"}, {"val": "5"}], width=560),
    frame("② fast/slow 同步走，fast 到尾", "drawLinkedList", nodes=[{"val": "d"}, {"val": "1"}, {"val": "2"}, {"val": "3", "highlight": "done"}, {"val": "4"}, {"val": "5"}], width=560),
    frame("③ slow.next = slow.next.next 跳过 4", "drawLinkedList", nodes=[{"val": "1", "highlight": "done"}, {"val": "2", "highlight": "done"}, {"val": "3", "highlight": "done"}, {"val": "5", "highlight": "done"}], width=560),
    ],
    "conclusion": "dummy 处理删头结点，快慢指针定位倒数第 n 个的前驱。",
    "py": """def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next""",
    "java": """public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0, head), fast = dummy, slow = dummy;
    for (int i = 0; i < n; i++) fast = fast.next;
    while (fast.next != null) { fast = fast.next; slow = slow.next; }
    slow.next = slow.next.next;
    return dummy.next;
}""",
    "time": "O(L) — 一遍遍历",
    "space": "O(1)",
    "pitfalls": [["用 dummy", "删的可能是头结点，dummy 统一处理返回 dummy.next"], ["fast 先走 n 步", "这样 slow 停在待删节点的前驱，才能 slow.next=slow.next.next"]],
    "selfcheck": [["删头结点怎么办？", "dummy 保证 slow 从头前驱出发，删头也统一。"], ["n 等于链表长度？", "fast 走 n 步到 null，循环不进入，slow 停在 dummy，删掉头。"]],
}

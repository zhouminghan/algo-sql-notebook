from scripts.algo_gen import frame

PROBLEM = {
    "id": 75,
    "title": "反转链表",
    "diff": "easy",
    "tags": ["链表"],
    "leetcode": 206,
    "origin": "https://leetcode.cn/problems/reverse-linked-list/",
    "why": "用 prev、cur 两个指针，每次把 cur.next 指回 prev，再双双前移。迭代 O(n) O(1)，是最基础的链表操作。",
    "desc": """<p>给定单链表的头节点，反转链表并返回反转后的头节点。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4,5]</code> → <code>[5,4,3,2,1]</code></p>""",
    "frames": [
    frame("① 原链表 1→2→3→4→5", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 3}, {"val": 4}, {"val": 5}], width=560, height=90),
    frame("② 逐节点反转指针方向", "drawLinkedList", nodes=[{"val": 1, "highlight": "active"}, {"val": 2, "highlight": "active"}, {"val": 3, "highlight": "active"}, {"val": 4, "highlight": "active"}, {"val": 5, "highlight": "active"}], width=560, height=90),
    frame("③ 反转完成 5→4→3→2→1", "drawLinkedList", nodes=[{"val": 5, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}], width=560, height=90),
    ],
    "conclusion": "先存下一个节点，再把当前指回前驱，循环到链表尾。",
    "py": """def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev""",
    "java": """public ListNode reverseList(ListNode head) {
    ListNode prev = null, cur = head;
    while (cur != null) {
        ListNode nxt = cur.next;
        cur.next = prev;
        prev = cur; cur = nxt;
    }
    return prev;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["先存 nxt", "改指针前必须先保存 cur.next，否则断链"], ["返回 prev", "循环结束 cur 为 null，prev 才是新头"]],
    "selfcheck": [["空链表 / 单节点？", "分别返回 None / 原节点，逻辑天然覆盖。"], ["递归写法？", "newHead = reverseList(head.next)，再 head.next.next = head、head.next = None。"]],
}

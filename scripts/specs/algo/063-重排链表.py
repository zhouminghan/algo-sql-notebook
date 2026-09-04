from scripts.algo_gen import frame

PROBLEM = {
    "id": 63,
    "title": "重排链表",
    "diff": "medium",
    "tags": ["链表"],
    "leetcode": 143,
    "origin": "https://leetcode.cn/problems/reorder-list/",
    "why": "目标顺序是「首、尾、次首、次尾…」。三步：找中点 → 反转后半段 → 交替合并两段。每步都是链表基础操作。",
    "desc": """<p>给定单链表，将其重排为 <code>L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …</code> 的形式，不能只改值，必须改变节点结构。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4]</code> → <code>[1,4,2,3]</code>；<code>[1,2,3,4,5]</code> → <code>[1,5,2,4,3]</code></p>""",
    "frames": [
    frame("① 找中点，切成前后两半", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 3, "highlight": "active"}, {"val": 4}, {"val": 5}], width=560, height=90),
    frame("② 反转后半段 3→4→5 变成 5→4→3", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 5, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}], width=560, height=90),
    frame("③ 交替合并：1→5→2→4→3", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 5, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}], width=560, height=90),
    ],
    "conclusion": "找中点、反转后半、交替拼接，三步组合出「首尾交替」的效果。",
    "py": """def reorderList(head):
    if not head:
        return
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    # 反转后半
    prev, cur = None, slow.next
    slow.next = None
    while cur:
        nxt = cur.next
        cur.next, prev, cur = prev, cur, nxt
    # 交替合并
    a, b = head, prev
    while b:
        a.next, a = b, a.next
        b.next, b = a, b.next""",
    "java": """public void reorderList(ListNode head) {
    if (head == null) return;
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode prev = null, cur = slow.next;
    slow.next = null;
    while (cur != null) { ListNode n = cur.next; cur.next = prev; prev = cur; cur = n; }
    ListNode a = head, b = prev;
    while (b != null) { ListNode na = a.next, nb = b.next; a.next = b; b.next = na; a = na; b = nb; }
}""",
    "time": "O(n) — 三步各扫一遍",
    "space": "O(1)",
    "pitfalls": [["找中点断开", "slow 停在中间，slow.next = None 把前后两段切断"], ["合并时保存后继", "交替拼接前先存 a.next、b.next，否则指针被覆盖丢失"]],
    "selfcheck": [["偶数长度 [1,2,3,4]？", "中点 slow=2，后半反转得 4→3，合并得 1→4→2→3。"], ["奇数长度 [1,2,3,4,5]？", "中点 slow=3，后半 4→5 反转 5→4，合并 1→5→2→4，剩 3 作尾。"]],
}

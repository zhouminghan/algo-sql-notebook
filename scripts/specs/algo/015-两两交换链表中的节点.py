from scripts.algo_gen import frame

PROBLEM = {
    "id": 15,
    "title": "两两交换链表中的节点",
    "diff": "medium",
    "tags": ["链表"],
    "leetcode": 24,
    "origin": "https://leetcode.cn/problems/swap-nodes-in-pairs/",
    "why": "交换相邻两节点要同时改三条 next 指针，顺序一旦搞反就会断链。用 dummy 哨兵 + 三个指针（pre、first、second）按固定顺序翻转，边界清晰不易错。",
    "desc": """<p>给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。不能只改节点内部的值，必须实际进行节点交换。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4]</code> → <code>[2,1,4,3]</code></p>""",
    "frames": [
    frame("① 原链表 1→2→3→4", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 3}, {"val": 4}], width=520, height=90),
    frame("② 交换 1、2：pre→2→1→(3)", "drawLinkedList", nodes=[{"val": 2, "highlight": "active"}, {"val": 1, "highlight": "active"}, {"val": 3}, {"val": 4}], width=520, height=90),
    frame("③ 交换 3、4，完成", "drawLinkedList", nodes=[{"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}], width=520, height=90),
    ],
    "conclusion": "每组交换前先「记住」组后的节点，再按 2→1→后组 的顺序接好，指针就不会断。",
    "py": """def swapPairs(head):
    dummy = ListNode(0, head)
    pre = dummy
    while pre.next and pre.next.next:
        a, b = pre.next, pre.next.next
        pre.next, a.next, b.next = b, b.next, a
        pre = a
    return dummy.next""",
    "java": """public ListNode swapPairs(ListNode head) {
    ListNode dummy = new ListNode(0, head), pre = dummy;
    while (pre.next != null && pre.next.next != null) {
        ListNode a = pre.next, b = a.next;
        a.next = b.next;
        b.next = a;
        pre.next = b;
        pre = a;
    }
    return dummy.next;
}""",
    "time": "O(n) — 每对节点交换一次",
    "space": "O(1) — 只改指针",
    "pitfalls": [["指针赋值顺序", "先把 a.next 指向 b.next（保住后续节点），再让 b.next = a，否则会丢链"], ["循环条件", "pre.next and pre.next.next 都非空才成对交换，只剩一个节点时保持不动"]],
    "selfcheck": [["链表长度为奇数（如 [1,2,3]）结果是什么？", "交换 1、2 后 pre 指向 2，此时 pre.next=3 但 pre.next.next 为空，循环结束，结果为 [2,1,3]。"], ["为什么不能只交换值？", "题目要求实际交换节点；而且值交换无法处理带随机指针等复杂节点，指针交换才是通用做法。"]],
}

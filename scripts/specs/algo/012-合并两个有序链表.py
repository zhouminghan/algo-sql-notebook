from scripts.algo_gen import frame

PROBLEM = {
    "id": 12,
    "title": "合并两个有序链表",
    "diff": "easy",
    "tags": ["链表"],
    "leetcode": 21,
    "origin": "https://leetcode.cn/problems/merge-two-sorted-lists/",
    "why": "两个链表都已有序，合并就等价于「每次从两个头结点里取较小的那个」不断拼接。引入一个 dummy 哨兵节点，可以避免对「新链表的头是谁」做特殊判断。",
    "desc": """<p>将两个<strong>升序</strong>链表合并为一个新的升序链表并返回。新链表由给定两个链表的所有节点拼接组成。</p>
<p><strong>示例：</strong><br><code>l1 = [1,2,4]</code>，<code>l2 = [1,3,4]</code> → <code>[1,1,2,3,4,4]</code></p>""",
    "frames": [
    frame("① 两个头 1 和 1 比较，取 l1 的 1", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}], width=560, height=90),
    frame("② l1 头=2 > l2 头=1，取 l2 的 1", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 1, "highlight": "done"}], width=560, height=90),
    frame("③ 依次取 2→3→4，最后 l2 空，接上 l1 剩余 4", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 4, "highlight": "done"}], width=680, height=90),
    ],
    "conclusion": "每次取较小头、步进对应链表；当一条链走完，把另一条剩余部分整体接上即可。",
    "py": """def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next, l1 = l1, l1.next
        else:
            cur.next, l2 = l2, l2.next
        cur = cur.next
    cur.next = l1 or l2   # 剩余部分整体接上
    return dummy.next""",
    "java": """public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), cur = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
        else                  { cur.next = l2; l2 = l2.next; }
        cur = cur.next;
    }
    cur.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}""",
    "time": "O(m + n) — 每个节点访问一次",
    "space": "O(1) — 只改指针，不额外分配节点",
    "pitfalls": [["用 dummy 哨兵", "避免「第一个节点从 l1 还是 l2 取」的分支，返回 dummy.next 即可"], ["循环结束后接剩余", "忘写 cur.next = l1 or l2 会丢掉较长链表的尾巴"]],
    "selfcheck": [["两条链表一空一非空怎么处理？", "while 条件直接不成立，cur.next = l1 or l2 把非空链表整体接上，返回 dummy.next，逻辑天然覆盖。"], ["递归写法怎么写？", "merge(l1,l2)：若 l1 空返回 l2，l2 空返回 l1；否则取较小者为头，其 next = merge(较小者.next, 另一个)。"]],
}

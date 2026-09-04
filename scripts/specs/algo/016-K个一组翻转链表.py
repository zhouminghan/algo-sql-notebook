from scripts.algo_gen import frame

PROBLEM = {
    "id": 16,
    "title": "K个一组翻转链表",
    "diff": "hard",
    "tags": ["链表"],
    "leetcode": 25,
    "origin": "https://leetcode.cn/problems/reverse-nodes-in-k-group/",
    "why": "整段翻转是「翻转链表」的推广：先数出 K 个节点，不足 K 就不翻；够 K 就用头插法/三指针翻转这一段，再把上一段的尾巴接到新头。核心是「分组 + 段内翻转 + 接缝处理」。",
    "desc": """<p>给链表的每 <code>k</code> 个节点一组进行翻转，返回修改后的链表。<code>k</code> 是正整数且小于等于链表长度。如果节点总数不是 <code>k</code> 的整数倍，最后剩余的节点保持原样。</p>
<p><strong>示例：</strong><br><code>head = [1,2,3,4,5], k = 2</code> → <code>[2,1,4,3,5]</code><br><code>k = 3</code> → <code>[3,2,1,4,5]</code></p>""",
    "frames": [
    frame("① 先数出 K=2 个节点：1、2", "drawLinkedList", nodes=[{"val": 1, "highlight": "active"}, {"val": 2, "highlight": "active"}, {"val": 3}, {"val": 4}, {"val": 5}], width=560, height=90),
    frame("② 翻转该组：2→1，再接回 3", "drawLinkedList", nodes=[{"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 3}, {"val": 4}, {"val": 5}], width=560, height=90),
    frame("③ 下一组 3、4 翻转，尾组 5 不足 K 保持原样", "drawLinkedList", nodes=[{"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 5}], width=560, height=90),
    ],
    "conclusion": "每组先判断「是否凑满 K」，够 K 翻、不够 K 停；翻转后把组头接到上一组尾部即可。",
    "py": """def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    pre = dummy
    while True:
        tail = pre
        for _ in range(k):               # 数 K 个
            tail = tail.next
            if not tail:
                return dummy.next        # 不足 K，不再翻转
        nxt = tail.next
        cur, prev = pre.next, nxt
        while cur is not nxt:            # 段内翻转
            tmp = cur.next
            cur.next, prev, cur = prev, cur, tmp
        pre.next, pre = tail, pre.next   # 接缝
    """,
    "java": """public ListNode reverseKGroup(ListNode head, int k) {
    ListNode dummy = new ListNode(0, head), pre = dummy;
    while (true) {
        ListNode tail = pre;
        for (int i = 0; i < k; i++) { tail = tail.next; if (tail == null) return dummy.next; }
        ListNode nxt = tail.next, cur = pre.next, prev = nxt;
        while (cur != nxt) { ListNode tmp = cur.next; cur.next = prev; prev = cur; cur = tmp; }
        ListNode newHead = pre.next;
        pre.next = tail; pre = newHead;
    }
}""",
    "time": "O(n) — 每个节点恰好处理一次",
    "space": "O(1) — 原地翻转",
    "pitfalls": [["不足 K 要原样保留", "先数 K 再决定是否翻转；边翻边发现不足 K 会翻乱尾巴"], ["翻转后接缝", "每段翻完要把「上一段尾」接到本段新头，并把本段新尾接到下一段"]],
    "selfcheck": [["k=1 时结果是什么？", "每 1 个一组翻转等于不翻转，直接返回原链表。"], ["为什么每段翻转用 cur != nxt 而不是 cur？", "因为翻转段的「终点」是下一段的头 nxt，cur 走到 nxt 就表示本段翻完，这样不会越界翻到下一段。"]],
}

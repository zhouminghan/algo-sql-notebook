from scripts.algo_gen import frame

PROBLEM = {
    "id": 14,
    "title": "合并K个升序链表",
    "diff": "hard",
    "tags": ["堆", "链表"],
    "leetcode": 23,
    "origin": "https://leetcode.cn/problems/merge-k-sorted-lists/",
    "why": "K 条有序链表的合并，每一轮都要知道「K 个当前头里谁最小」。最小堆正好 O(log K) 取出最小值，再用 dummy 哨兵逐个拼接，比两两合并更简洁高效。",
    "desc": """<p>给定一个链表数组，每个链表都已按<strong>升序</strong>排列。将所有链表合并为一个升序链表并返回。</p>
<p><strong>示例：</strong><br><code>lists = [[1,4,5],[1,3,4],[2,6]]</code> → <code>[1,1,2,3,4,4,5,6]</code></p>""",
    "frames": [
    frame("① 三条链的头入堆：1、1、2", "drawTable", headers=["链表", "当前头", "内容"], rows=[["L1", {"val": "1", "highlight": True}, "1→4→5"], ["L2", {"val": "1", "highlight": True}, "1→3→4"], ["L3", {"val": "2", "highlight": True}, "2→6"]], width=520, height=160),
    frame("② 弹出最小头 1，接进结果，压入其 next=4", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}], width=560, height=90),
    frame("③ 不断弹出最小头拼接，直到堆空", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 5, "highlight": "done"}, {"val": 6, "highlight": "done"}], width=720, height=90),
    ],
    "conclusion": "堆里始终保存「每条链当前最小头」，反复 pop 最小 + push 其后继，直到所有节点都被取出。",
    "py": """import heapq
def mergeKLists(lists):
    dummy = ListNode(0)
    cur = dummy
    heap = []
    for i, node in enumerate(lists):      # 用 i 避免节点值相等时的比较问题
        if node:
            heapq.heappush(heap, (node.val, i, node))
    while heap:
        _, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next""",
    "java": """public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
    for (ListNode n : lists) if (n != null) pq.offer(n);
    ListNode dummy = new ListNode(0), cur = dummy;
    while (!pq.isEmpty()) {
        ListNode n = pq.poll();
        cur.next = n; cur = cur.next;
        if (n.next != null) pq.offer(n.next);
    }
    return dummy.next;
}""",
    "time": "O(N log K) — N 为总节点数，堆操作 O(log K)",
    "space": "O(K) — 堆中最多 K 个节点",
    "pitfalls": [["堆元素比较问题", "Python 元组里若节点值相等，会去比较 ListNode 导致报错，需加下标 i 兜底"], ["初始入堆要判空", "lists 里可能含空链表，空链表不入堆"]],
    "selfcheck": [["如果 K 条链表里有空链表会怎样？", "只把非空链表头入堆即可；若全部为空，堆为空，直接返回 dummy.next = None。"], ["为什么复杂度是 O(N log K) 而不是 O(NK)？", "每次取最小是 O(log K)（堆），共 N 个节点，所以 N log K；暴力每次线性扫 K 个头才是 O(NK)。"]],
}

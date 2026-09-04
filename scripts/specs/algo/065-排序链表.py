from scripts.algo_gen import frame

PROBLEM = {
    "id": 65,
    "title": "排序链表",
    "diff": "medium",
    "tags": ["链表", "归并"],
    "leetcode": 148,
    "origin": "https://leetcode.cn/problems/sort-list/",
    "why": "链表不能随机访问，快排不便；归并排序天然适合链表：找中点切成两半，递归排序，再合并两个有序链表。时间 O(n log n)、空间 O(log n) 递归栈。",
    "desc": """<p>给定链表头节点，将其按<strong>升序</strong>排列并返回排序后的链表。要求 O(n log n) 时间。</p>
<p><strong>示例：</strong><br><code>[4,2,1,3]</code> → <code>[1,2,3,4]</code></p>""",
    "frames": [
    frame("① 快慢指针找中点，切两半", "drawLinkedList", nodes=[{"val": 4}, {"val": 2, "highlight": "active"}, {"val": 1}, {"val": 3}], width=520, height=90),
    frame("② 两半各自递归排序：4→2 变 2→4；1→3 保持", "drawTable", headers=["段", "排序前", "排序后"], rows=[["左半", "4→2", "2→4"], ["右半", "1→3", "1→3"]], width=460, height=140),
    frame("③ 归并两个有序链表", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}], width=520, height=90),
    ],
    "conclusion": "找中点 → 递归排序 → 归并，自顶向下的链表归并排序。",
    "py": """def sortList(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:      # 找中点
        slow, fast = slow.next, fast.next.next
    mid = slow.next
    slow.next = None               # 切断
    left = sortList(head)
    right = sortList(mid)
    return merge(left, right)

def merge(a, b):
    dummy = ListNode(0)
    cur = dummy
    while a and b:
        if a.val < b.val:
            cur.next, a = a, a.next
        else:
            cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next""",
    "java": """public ListNode sortList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode slow = head, fast = head.next;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode mid = slow.next;
    slow.next = null;
    return merge(sortList(head), sortList(mid));
}
ListNode merge(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), cur = dummy;
    while (a != null && b != null) {
        if (a.val < b.val) { cur.next = a; a = a.next; }
        else { cur.next = b; b = b.next; }
        cur = cur.next;
    }
    cur.next = (a != null) ? a : b;
    return dummy.next;
}""",
    "time": "O(n log n) — 归并",
    "space": "O(log n) — 递归栈",
    "pitfalls": [["找中点用 fast=head.next", "这样偶数长度时 slow 停在前半段尾，切分更均衡，避免死循环"], ["切断 mid", "slow.next=None 必须切断，否则递归区间重叠"]],
    "selfcheck": [["为什么快排不适合链表？", "链表无法 O(1) 随机访问，分区成本高；归并只需顺序遍历，更适合链表。"], ["O(1) 空间的自底向上归并？", "按长度 1,2,4… 逐段两两归并，可省递归栈。"]],
}

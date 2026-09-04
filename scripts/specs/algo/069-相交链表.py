from scripts.algo_gen import frame

PROBLEM = {
    "id": 69,
    "title": "相交链表",
    "diff": "easy",
    "tags": ["链表"],
    "leetcode": 160,
    "origin": "https://leetcode.cn/problems/intersection-of-two-linked-lists/",
    "why": "两个指针分别从 A、B 出发，走到头就换到另一条链继续走。若相交，两指针走的总路程相等，必在交点相遇；若不相交，最后同时为 null。",
    "desc": """<p>给定两个单链表的头节点，找出并返回它们相交的起始节点；不相交则返回 null。</p>
<p><strong>示例：</strong><br>listA=[4,1,8,4,5], listB=[5,6,1,8,4,5]（在 8 相交）→ 返回节点 8</p>""",
    "frames": [
    frame("① 两条链长度不同，直接同步走会错过交点", "drawLinkedList", nodes=[{"val": 4}, {"val": 1}, {"val": 8, "highlight": "active"}, {"val": 4}, {"val": 5}], width=560, height=90),
    frame("② 指针走到头就换到另一条链，路程对齐", "drawTable", headers=["步", "指针 a", "指针 b"], rows=[["0", "A头(4)", "B头(5)"], ["1", "1", "6"], ["2", "8", "1"], ["3", "4", "8 相遇 ✓"]], width=460, height=190),
    frame("③ 相交点 8；不相交则最终同到 null", "drawLinkedList", nodes=[{"val": 4}, {"val": 1}, {"val": 8, "highlight": "done"}], width=460, height=90),
    ],
    "conclusion": "「走完自己再走对方」让两指针总路程相等，交点必然相遇。",
    "py": """def getIntersectionNode(headA, headB):
    a, b = headA, headB
    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a""",
    "java": """public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    ListNode a = headA, b = headB;
    while (a != b) {
        a = (a == null) ? headB : a.next;
        b = (b == null) ? headA : b.next;
    }
    return a;
}""",
    "time": "O(m + n)",
    "space": "O(1)",
    "pitfalls": [["走到头换链", "a 到 null 后跳 headB，而不是停在 null"], ["终止条件", "循环 a != b；不相交时二者最终都为 null，自然退出"]],
    "selfcheck": [["不相交会死循环吗？", "不会。两指针各走 m+n 步后同时到达 null，a==b 退出。"], ["哈希表做法？", "把 A 的节点存 Set，遍历 B 找第一个在 Set 中的节点，空间 O(m)。"]],
}

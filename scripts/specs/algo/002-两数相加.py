from scripts.algo_gen import frame

PROBLEM = {
    "id": 2,
    "title": "两数相加",
    "diff": "medium",
    "tags": ["链表", "数学"],
    "leetcode": 2,
    "origin": "https://leetcode.cn/problems/add-two-numbers/",
    "why": "两个链表是逆序存的数，加法本就从低位到高位。用 dummy 哨兵逐位相加，carry 进位，一条链走完接另一条，最后多出来的进位再补一个节点。",
    "desc": "<p>给定两个<strong>非空</strong>链表表示两个非负整数，每位数字按<strong>逆序</strong>存储（如 342 存为 2→4→3）。将两数相加并返回同样逆序的链表。</p><p><strong>示例：</strong><br><code>l1=[2,4,3], l2=[5,6,4]</code> → <code>[7,0,8]</code>（342+465=807）</p>",
    "frames": [
    frame("① 个位：2+5=7，无进位", "drawLinkedList", nodes=[{"val": "7", "highlight": "done"}], width=460),
    frame("② 十位：4+6=10，写 0 进 1", "drawLinkedList", nodes=[{"val": "7", "highlight": "done"}, {"val": "0", "highlight": "active"}], width=460),
    frame("③ 百位：3+4+进位1=8，结果 7→0→8", "drawLinkedList", nodes=[{"val": "7", "highlight": "done"}, {"val": "0", "highlight": "done"}, {"val": "8", "highlight": "done"}], width=460),
    ],
    "conclusion": "逐位相加 + 进位，两条链同步前进，最后进位非零再补节点。",
    "py": """def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    cur = dummy
    carry = 0
    while l1 or l2 or carry:
        s = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
        carry = s // 10
        cur.next = ListNode(s % 10)
        cur = cur.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next""",
    "java": """public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), cur = dummy;
    int carry = 0;
    while (l1 != null || l2 != null || carry != 0) {
        int s = (l1 != null ? l1.val : 0) + (l2 != null ? l2.val : 0) + carry;
        carry = s / 10;
        cur.next = new ListNode(s % 10);
        cur = cur.next;
        if (l1 != null) l1 = l1.next;
        if (l2 != null) l2 = l2.next;
    }
    return dummy.next;
}""",
    "time": "O(max(m,n)) — 遍历较长的链",
    "space": "O(max(m,n)) — 结果链",
    "pitfalls": [["循环条件要含 carry", "最后 99+1 这类，两条链走完但 carry=1，必须再补一个节点"], ["空节点当 0", "一条链先走完，后续当作 0 参与相加"]],
    "selfcheck": [["342+465 的过程？", "2+5=7；4+6=10 写 0 进 1；3+4+1=8，结果 7→0→8。"], ["为什么逆序存？", "逆序让加法从链表头开始逐位对齐，正是手算加法的顺序。"]],
}

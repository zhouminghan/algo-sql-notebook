from scripts.algo_gen import frame

PROBLEM = {
    "id": 82,
    "title": "回文链表",
    "diff": "easy",
    "tags": ["链表"],
    "leetcode": 234,
    "origin": "https://leetcode.cn/problems/palindrome-linked-list/",
    "why": "快慢指针找中点 → 反转后半段 → 与前半段逐个比较。O(n) 时间 + O(1) 空间，比转数组更省空间。",
    "desc": """<p>给定单链表的头节点，判断它是否是回文链表。</p>
<p><strong>示例：</strong><br><code>[1,2,2,1]</code> → <code>true</code>；<code>[1,2]</code> → <code>false</code></p>""",
    "frames": [
    frame("① 找中点，反转后半段", "drawLinkedList", nodes=[{"val": 1}, {"val": 2, "highlight": "active"}, {"val": 2}, {"val": 1}], width=520, height=90),
    frame("② 后半段反转后为 1→2", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}], width=520, height=90),
    frame("③ 前后两段逐个比较，全等即回文", "drawTable", headers=["位置", "前段", "后段", "相等?"], rows=[["0", "1", "1", "✓"], ["1", "2", "2", "✓"]], width=460, height=140),
    ],
    "conclusion": "反转后半段后，与前半段逐节点比对，全部相等即回文。",
    "py": """def isPalindrome(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow      # 反转后半
    while cur:
        nxt = cur.next
        cur.next, prev, cur = prev, cur, nxt
    a, b = head, prev
    while b:
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return True""",
    "java": """public boolean isPalindrome(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode prev = null, cur = slow;
    while (cur != null) { ListNode n = cur.next; cur.next = prev; prev = cur; cur = n; }
    ListNode a = head, b = prev;
    while (b != null) {
        if (a.val != b.val) return false;
        a = a.next; b = b.next;
    }
    return true;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["只比较后半段长度", "while b 以后半段为准，奇数长度时中间节点不参与比较"], ["反转从 slow 开始", "slow 是后半段起点，反转后 prev 是后半段新头"]],
    "selfcheck": [["[1,2] 为何 false？", "中点 slow=2，反转后半还是 2，比较 1 vs 2 不等。"], ["转数组做法？", "把值收集到数组用双指针比较，空间 O(n)，简单但非 O(1)。"]],
}

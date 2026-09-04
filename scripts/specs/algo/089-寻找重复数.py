from scripts.algo_gen import frame

PROBLEM = {
    "id": 89,
    "title": "寻找重复数",
    "diff": "medium",
    "tags": ["快慢指针"],
    "leetcode": 287,
    "origin": "https://leetcode.cn/problems/find-the-duplicate-number/",
    "why": "数组元素在 [1,n] 且只有一个重复，把「下标 i → nums[i]」看成链表的 next 指针，重复数就是环的入口。用环形链表 II 的快慢指针求解，O(n) O(1)。",
    "desc": """<p>给定包含 <code>n+1</code> 个整数的数组，数字都在 <code>[1,n]</code> 范围内，其中<strong>只有一个数字重复出现</strong>（可能重复多次）。找出这个重复数。要求不修改数组、O(1) 额外空间。</p>
<p><strong>示例：</strong><br><code>[1,3,4,2,2]</code> → <code>2</code>；<code>[3,1,3,4,2]</code> → <code>3</code></p>""",
    "frames": [
    frame("① 把 i → nums[i] 当链表 next，重复数即环入口", "drawTable", headers=["i", "0", "1", "2", "3", "4"], rows=[["nums", "1", "3", "4", "2", "2"], ["next", "1", "3", "4", "2", "2"]], width=520, height=130),
    frame("② 快慢指针找相遇点", "drawTwoPointers", arr=[1, 3, 4, 2, 2], left=0, right=2, width=520, height=140),
    frame("③ 从头同速再走，相遇即重复数 2", "drawTable", headers=["步骤", "指针 A", "指针 B"], rows=[["0", "0", "相遇点"], ["1", "1", "4"], ["2", "3", "2"], ["3", "2", "2 相遇 ✓"]], width=460, height=190),
    ],
    "conclusion": "值域 [1,n] 保证 next 不出界且必有环，环入口就是重复数。",
    "py": """def findDuplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    p = nums[0]
    while p != slow:
        p = nums[p]
        slow = nums[slow]
    return p""",
    "java": """public int findDuplicate(int[] nums) {
    int slow = nums[0], fast = nums[0];
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);
    int p = nums[0];
    while (p != slow) { p = nums[p]; slow = nums[slow]; }
    return p;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["next 用 nums 本身", "slow = nums[slow]，fast = nums[nums[fast]]，别直接下标加减"], ["入口即答案", "环入口是重复数，因为只有重复数被多个节点指向"]],
    "selfcheck": [["为什么必有环？", "n+1 个值落在 [1,n]，鸽巢原理必有重复；从下标 0 出发的 next 链最终进入由重复数构成的环。"], ["二分法怎么做？", "统计 ≤mid 的个数，若大于 mid 说明重复在左半，O(n log n)，也能 O(1) 空间。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 38,
    "title": "颜色分类",
    "diff": "medium",
    "tags": ["双指针"],
    "leetcode": 75,
    "origin": "https://leetcode.cn/problems/sort-colors/",
    "why": "荷兰国旗问题：用三个指针 p0、p1、cur 一次遍历。0 换到 p0、2 换到 p2，1 自然留在中间，O(n) 时间 + O(1) 空间原地完成。",
    "desc": """<p>给定一个包含红色(0)、白色(1)、蓝色(2)的数组，<strong>原地</strong>按 0、1、2 的顺序排序（不能用库排序函数）。</p>
<p><strong>示例：</strong><br><code>[2,0,2,1,1,0]</code> → <code>[0,0,1,1,2,2]</code></p>""",
    "frames": [
    frame("① p0 指向下一个 0 的位置，p2 指向下一个 2 的位置", "drawTwoPointers", arr=[2, 0, 2, 1, 1, 0], left=0, right=5, width=560, height=140),
    frame("② cur 遇 0 与 p0 交换、遇 2 与 p2 交换", "drawTwoPointers", arr=[0, 0, 1, 1, 2, 2], left=2, right=3, width=560, height=140),
    frame("③ 结果 [0,0,1,1,2,2]", "drawTable", headers=["下标", "0", "1", "2", "3", "4", "5"], rows=[["结果", "0", "0", "1", "1", "2", "2"]], width=560, height=110),
    ],
    "conclusion": "p0 之前全 0，p2 之后全 2，cur 扫一遍把 0 前送、2 后送，1 留在中间。",
    "py": """def sortColors(nums):
    p0 = cur = 0
    p2 = len(nums) - 1
    while cur <= p2:
        if nums[cur] == 0:
            nums[cur], nums[p0] = nums[p0], nums[cur]
            p0 += 1; cur += 1
        elif nums[cur] == 2:
            nums[cur], nums[p2] = nums[p2], nums[cur]
            p2 -= 1          # cur 不前进，换来的数还要再判
        else:
            cur += 1""",
    "java": """public void sortColors(int[] nums) {
    int p0 = 0, cur = 0, p2 = nums.length - 1;
    while (cur <= p2) {
        if (nums[cur] == 0) { swap(nums, cur++, p0++); }
        else if (nums[cur] == 2) { swap(nums, cur, p2--); }
        else cur++;
    }
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }""",
    "time": "O(n) — 一次遍历",
    "space": "O(1)",
    "pitfalls": [["遇 2 交换后 cur 不前移", "从 p2 换来的数还没检查过，cur 要留在原地再判断一次"], ["循环条件 cur <= p2", "cur 超过 p2 说明后面的 2 已就位，可以结束"]],
    "selfcheck": [["为什么遇 0 时 cur 可以前移？", "从 p0 换来的数一定是 1（因为 cur 扫过 p0 之前的都是 0/1），无需再判断。"], ["只有 0 和 1（无 2）呢？", "p2 分支永不触发，退化为简单的 0/1 分区。"]],
}

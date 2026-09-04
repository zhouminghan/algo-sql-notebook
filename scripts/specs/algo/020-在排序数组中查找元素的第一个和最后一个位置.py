from scripts.algo_gen import frame

PROBLEM = {
    "id": 20,
    "title": "在排序数组中查找元素的第一个和最后一个位置",
    "diff": "medium",
    "tags": ["二分"],
    "leetcode": 34,
    "origin": "https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/",
    "why": "「第一个」和「最后一个」分别是两个不同的二分目标：找左边界时把命中也继续往左收敛，找右边界时继续往右收敛。两次二分各管一边，互不干扰。",
    "desc": """<p>给定一个<strong>非递减</strong>排列的整数数组 <code>nums</code> 和一个目标值 <code>target</code>，找出 target 在数组中的<strong>开始位置</strong>和<strong>结束位置</strong>。不存在则返回 <code>[-1, -1]</code>。要求 O(log n)。</p>
<p><strong>示例：</strong><br><code>nums=[5,7,7,8,8,10], target=8</code> → <code>[3,4]</code></p>""",
    "frames": [
    frame("① 找左边界：命中 8 也继续向左", "drawBinarySearch", arr=[5, 7, 7, 8, 8, 10], left=0, mid=3, right=5, width=560, height=140),
    frame("② 左边界收敛到下标 3", "drawBinarySearch", arr=[5, 7, 7, 8, 8, 10], left=0, mid=2, right=3, excludedRanges=[{"start": 4, "end": 5}], width=560, height=140),
    frame("③ 找右边界：命中 8 继续向右，收敛到 4", "drawBinarySearch", arr=[5, 7, 7, 8, 8, 10], left=3, mid=4, right=5, width=560, height=140),
    ],
    "conclusion": "左边界 = 第一个 >= target 的位置，右边界 = 最后一个 <= target 的位置，两次二分分别求得。",
    "py": """def searchRange(nums, target):
    def left_bound():
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] < target: l = m + 1
            else: r = m - 1
        return l
    def right_bound():
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] <= target: l = m + 1
            else: r = m - 1
        return r
    lo = left_bound()
    hi = right_bound()
    if lo <= hi:
        return [lo, hi]
    return [-1, -1]""",
    "java": """public int[] searchRange(int[] nums, int target) {
    int lo = left(nums, target), hi = right(nums, target);
    if (lo <= hi) return new int[]{lo, hi};
    return new int[]{-1, -1};
}
int left(int[] a, int t) {
    int l = 0, r = a.length - 1;
    while (l <= r) { int m = (l + r) >>> 1; if (a[m] < t) l = m + 1; else r = m - 1; }
    return l;
}
int right(int[] a, int t) {
    int l = 0, r = a.length - 1;
    while (l <= r) { int m = (l + r) >>> 1; if (a[m] <= t) l = m + 1; else r = m - 1; }
    return r;
}""",
    "time": "O(log n) — 两次独立二分",
    "space": "O(1)",
    "pitfalls": [["左右边界写法不同", "左边界用 < 收缩，右边界用 <= 收缩，只差一个等号，写反会偏移一位"], ["结果校验", "左边界可能越界或 nums[lo] != target，需判断 lo <= hi 才返回，否则 [-1,-1]"]],
    "selfcheck": [["target 不存在时左右边界会怎样？", "左边界会指向「第一个大于 target」的位置，右边界指向「最后一个小于 target」的位置，此时 lo > hi，返回 [-1,-1]。"], ["数组里 target 只出现一次呢？", "左右边界会收敛到同一个下标，lo == hi，返回 [i, i]。"]],
}

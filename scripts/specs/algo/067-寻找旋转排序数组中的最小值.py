from scripts.algo_gen import frame

PROBLEM = {
    "id": 67,
    "title": "寻找旋转排序数组中的最小值",
    "diff": "medium",
    "tags": ["二分"],
    "leetcode": 153,
    "origin": "https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/",
    "why": "旋转数组的最小值就是「断层」位置。二分比较 nums[mid] 与 nums[r]：若 mid 比右端大，说明最小值在右半；否则在左半（含 mid）。",
    "desc": """<p>给定一个<strong>元素值互不相同</strong>且升序排列的数组，在某处旋转后（如 <code>[0,1,2,4,5,6,7]</code> 变为 <code>[4,5,6,7,0,1,2]</code>），找出其中最小元素。要求 O(log n)。</p>
<p><strong>示例：</strong><br><code>[3,4,5,1,2]</code> → <code>1</code>；<code>[4,5,6,7,0,1,2]</code> → <code>0</code></p>""",
    "frames": [
    frame("① 比较 mid 与右端：5 > 2 → 最小值在右半", "drawBinarySearch", arr=[3, 4, 5, 1, 2], left=0, mid=2, right=4, width=520, height=140),
    frame("② 收缩到右半 [1,2]，mid=1，1 <= 2 → 在左半", "drawBinarySearch", arr=[3, 4, 5, 1, 2], left=3, mid=3, right=4, excludedRanges=[{"start": 0, "end": 2}], width=520, height=140),
    frame("③ 收敛到 left=right，即最小值 1", "drawBinarySearch", arr=[3, 4, 5, 1, 2], left=3, mid=3, right=3, excludedRanges=[{"start": 0, "end": 2}], width=520, height=140),
    ],
    "conclusion": "mid 与右端比较决定收缩方向，直到 l==r 即最小值。",
    "py": """def findMin(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if nums[m] > nums[r]:   # 断层在右半
            l = m + 1
        else:                   # 断层在左半（含 m）
            r = m
    return nums[l]""",
    "java": """public int findMin(int[] nums) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int m = (l + r) >>> 1;
        if (nums[m] > nums[r]) l = m + 1; else r = m;
    }
    return nums[l];
}""",
    "time": "O(log n)",
    "space": "O(1)",
    "pitfalls": [["与右端比较", "与 nums[r] 比较最直观；与左端比较需额外处理未旋转情况"], ["r = m 而不是 m-1", "nums[m] <= nums[r] 时 m 可能正是最小值，不能跳过"]],
    "selfcheck": [["完全没旋转（升序）？", "nums[m] 恒 <= nums[r]，r 一路左移，最终 l=0 返回最小值 nums[0]。"], ["含重复元素呢？", "那就是 154 题，遇到 nums[m]==nums[r] 需 r-- 逐退，无法纯二分。"]],
}

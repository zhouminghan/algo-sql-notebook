from scripts.algo_gen import frame

PROBLEM = {
    "id": 19,
    "title": "搜索旋转排序数组",
    "diff": "medium",
    "tags": ["二分"],
    "leetcode": 33,
    "origin": "https://leetcode.cn/problems/search-in-rotated-sorted-array/",
    "why": "数组虽被旋转，但「左半有序或右半有序」总有一半成立。二分时先判断哪半边有序，再看 target 是否落在有序的那半边，据此收缩区间，把 O(n) 降到 O(log n)。",
    "desc": """<p>整数数组 <code>nums</code> 原本是升序排列，在某个下标处旋转（例如 <code>[0,1,2,4,5,6,7]</code> 在下标 3 处旋转变成 <code>[4,5,6,7,0,1,2]</code>）。给定旋转后的数组和一个目标值 <code>target</code>，若数组中存在则返回下标，否则返回 <code>-1</code>。要求 O(log n)。</p>
<p><strong>示例：</strong><br><code>nums=[4,5,6,7,0,1,2], target=0</code> → <code>4</code></p>""",
    "frames": [
    frame("① L=0, M=3(nums=7), R=6：左半 [4,5,6,7] 有序", "drawBinarySearch", arr=[4, 5, 6, 7, 0, 1, 2], left=0, mid=3, right=6, width=560, height=140),
    frame("② target=0 不在左半 → L=M+1=4", "drawBinarySearch", arr=[4, 5, 6, 7, 0, 1, 2], left=4, mid=5, right=6, excludedRanges=[{"start": 0, "end": 3}], width=560, height=140),
    frame("③ 右半 [0,1,2] 有序，target=0 命中 M=4", "drawBinarySearch", arr=[4, 5, 6, 7, 0, 1, 2], left=4, mid=4, right=6, excludedRanges=[{"start": 0, "end": 3}], width=560, height=140),
    ],
    "conclusion": "每轮锁定「有序的那一半」判断 target 是否在内，在内则收敛到那一半，否则跳到另一半，循环往复。",
    "py": """def search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[l] <= nums[m]:          # 左半有序
            if nums[l] <= target < nums[m]:
                r = m - 1
            else:
                l = m + 1
        else:                           # 右半有序
            if nums[m] < target <= nums[r]:
                l = m + 1
            else:
                r = m - 1
    return -1""",
    "java": """public int search(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l <= r) {
        int m = (l + r) >>> 1;
        if (nums[m] == target) return m;
        if (nums[l] <= nums[m]) {
            if (nums[l] <= target && target < nums[m]) r = m - 1; else l = m + 1;
        } else {
            if (nums[m] < target && target <= nums[r]) l = m + 1; else r = m - 1;
        }
    }
    return -1;
}""",
    "time": "O(log n) — 每次二分砍掉一半",
    "space": "O(1)",
    "pitfalls": [["判断有序用 nums[l] <= nums[m]", "必须带等号，处理只剩两个元素时 l==m 的情况"], ["target 区间判断要闭开", "左半用 nums[l] <= target < nums[m]，右半用 nums[m] < target <= nums[r]，边界不能搞混"]],
    "selfcheck": [["nums 完全没旋转（升序）怎么办？", "nums[l] <= nums[m] 恒成立，退化为标准二分，仍正确。"], ["target 不存在会返回什么？", "区间逐渐收缩到 l > r 退出循环，返回 -1。"]],
}

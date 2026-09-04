from scripts.algo_gen import frame

PROBLEM = {
    "id": 21,
    "title": "搜索插入位置",
    "diff": "easy",
    "tags": ["二分"],
    "leetcode": 35,
    "origin": "https://leetcode.cn/problems/search-insert-position/",
    "why": "目标值不存在时要返回它「应该插入的位置」，这恰好就是「第一个 >= target 的下标」。标准二分的下界 l 最终就停在这里，天然给出答案。",
    "desc": """<p>给定一个排序数组和一个目标值，在数组中找到目标值并返回其索引；如果不存在，返回它按顺序插入的位置。</p>
<p><strong>示例：</strong><br><code>nums=[1,3,5,6], target=5</code> → <code>2</code><br><code>target=2</code> → <code>1</code>（应插在 1 和 3 之间）</p>""",
    "frames": [
    frame("① target=2：L=0, M=1(3), R=3，2 < 3 → R=M-1", "drawBinarySearch", arr=[1, 3, 5, 6], left=0, mid=1, right=3, width=520, height=140),
    frame("② L=0, M=0(1), R=0，1 < 2 → L=M+1=1", "drawBinarySearch", arr=[1, 3, 5, 6], left=0, mid=0, right=0, width=520, height=140),
    frame("③ 循环结束，L=1 即插入位置", "drawTwoPointers", arr=[1, 3, 5, 6], left=1, right=1, width=520, height=140),
    ],
    "conclusion": "二分结束后 l 就是「第一个 >= target」的位置——找到时是它本身，没找到时是插入点。",
    "py": """def searchInsert(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return l""",
    "java": """public int searchInsert(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l <= r) {
        int m = (l + r) >>> 1;
        if (nums[m] < target) l = m + 1; else r = m - 1;
    }
    return l;
}""",
    "time": "O(log n)",
    "space": "O(1)",
    "pitfalls": [["返回 l 而不是 m", "m 是中间指针，循环结束时 l 才是最终下界；返回 m 会得到中间值"], ["target 比所有元素都大", "l 一路右移，最终等于 len(nums)，正好是末尾插入位置"]],
    "selfcheck": [["target 比所有元素都小呢？", "r 一路左移到 -1，l 保持 0，返回 0，插到最前面。"], ["为什么不用「先找等于、找不到再线性找插入点」？", "那样最坏 O(n)；二分下界 l 本身就是插入点，一次二分 O(log n) 搞定。"]],
}

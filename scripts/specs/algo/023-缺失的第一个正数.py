from scripts.algo_gen import frame

PROBLEM = {
    "id": 23,
    "title": "缺失的第一个正数",
    "diff": "hard",
    "tags": ["哈希表"],
    "leetcode": 41,
    "origin": "https://leetcode.cn/problems/first-missing-positive/",
    "why": "答案一定落在 [1, n+1]（n 为数组长度）。用「原地哈希」把每个正数 x 放到下标 x-1 处，一趟交换后，第一个「下标 i 上不是 i+1」的位置就是答案，O(n) 时间 + O(1) 空间。",
    "desc": """<p>给定一个未排序的整数数组，找出其中<strong>没有出现的最小的正整数</strong>。要求时间复杂度 O(n) 且只用常数级额外空间。</p>
<p><strong>示例：</strong><br><code>[1,2,0] → 3</code>；<code>[3,4,-1,1] → 2</code>；<code>[7,8,9,11,12] → 1</code></p>""",
    "frames": [
    frame("① 目标：把正数 x 放到下标 x-1（原地哈希）", "drawTable", headers=["下标", "0", "1", "2", "3"], rows=[["原数组", "3", "4", "-1", "1"], ["应放", "1", "-", "3", "4"]], width=520, height=140),
    frame("② 交换：3 与 nums[2] 换、4 与 nums[3] 换、1 与 nums[0] 换", "drawTable", headers=["下标", "0", "1", "2", "3"], rows=[["归位后", {"val": "1", "highlight": True}, "-1", "3", "4"]], width=520, height=120),
    frame("③ 第一个 nums[i] != i+1 的位置 i=1 → 缺失 2", "drawTwoPointers", arr=[1, -1, 3, 4], left=1, right=1, width=520, height=140),
    ],
    "conclusion": "把每个 [1,n] 内的数送回「自己该在的位置」，再扫一遍看谁没归位，那个位置 +1 就是答案。",
    "py": """def firstMissingPositive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1""",
    "java": """public int firstMissingPositive(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
            int j = nums[i] - 1, t = nums[i]; nums[i] = nums[j]; nums[j] = t;
        }
    }
    for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;
    return n + 1;
}""",
    "time": "O(n) — 每个数最多被交换一次到正确位置",
    "space": "O(1) — 原地",
    "pitfalls": [["用 while 不是 if", "交换后当前位置可能又来了一个该归位的数，必须继续换，if 只换一次会漏"], ["交换条件要防死循环", "nums[nums[i]-1] != nums[i] 避免两个相等值反复换"], ["忽略越界的数", "负数、0、大于 n 的数不参与归位，直接跳过"]],
    "selfcheck": [["为什么答案上界是 n+1？", "[1,n] 一共 n 个坑，若 1..n 全都出现，缺失的最小正数只能是 n+1。"], ["[3,4,-1,1] 归位过程？", "i=0 时 3 与 nums[2]=-1 换；继续 while，nums[0]=-1 越界跳过；i=3 时 1 与 nums[0] 换 → [1,-1,3,4]，再扫到 i=1 的 -1，返回 2。"]],
}

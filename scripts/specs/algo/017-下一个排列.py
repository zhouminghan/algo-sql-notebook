from scripts.algo_gen import frame

PROBLEM = {
    "id": 17,
    "title": "下一个排列",
    "diff": "medium",
    "tags": ["数组"],
    "leetcode": 31,
    "origin": "https://leetcode.cn/problems/next-permutation/",
    "why": "「下一个排列」要找到比当前字典序大、且大得最少的一个。方法很固定：从右往左找第一个「降序对」，把它右边的较大者交换过来，再把右边反转成升序（最小化）。",
    "desc": """<p>整数数组的一个排列，就是将其所有成员按任意顺序排列。例如 <code>arr = [1,2,3]</code> 的排列有 <code>[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]</code>。</p>
<p>给定一个排列，将其<strong>原地</strong>重新排列为字典序的<strong>下一个</strong>排列；如果已经是最大排列，则重排为最小排列。</p>
<p><strong>示例：</strong><br><code>[1,2,3] → [1,3,2]</code>；<code>[3,2,1] → [1,2,3]</code>；<code>[1,1,5] → [1,5,1]</code></p>""",
    "frames": [
    frame("① 从右找第一个「上升」位置 i（nums[i] < nums[i+1]）", "drawTwoPointers", arr=[1, 2, 3], left=1, right=2, width=520, height=140),
    frame("② 在右侧找比 nums[i]=2 大的最小数 3，交换", "drawTable", headers=["索引", "0", "1", "2"], rows=[["交换前", "1", "2", "3"], ["交换后", "1", {"val": "3", "highlight": True}, {"val": "2", "highlight": True}]], width=520, height=140),
    frame("③ 把 i 右侧反转成升序（最小化）", "drawTable", headers=["索引", "0", "1", "2"], rows=[["结果", "1", "3", "2"]], width=520, height=120),
    ],
    "conclusion": "找到「最靠右的可增大位置」，用右侧最小的较大值替换，再让右边升序，就得到恰好多一点的下一个排列。",
    "py": """def nextPermutation(nums):
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:   # 找上升点
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:              # 找右侧较大者
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    l, r = i + 1, n - 1                        # 反转右侧
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1; r -= 1""",
    "java": """public void nextPermutation(int[] nums) {
    int n = nums.length, i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) j--;
        int t = nums[i]; nums[i] = nums[j]; nums[j] = t;
    }
    for (int l = i + 1, r = n - 1; l < r; l++, r--) {
        int t = nums[l]; nums[l] = nums[r]; nums[r] = t;
    }
}""",
    "time": "O(n) — 至多三次扫描",
    "space": "O(1) — 原地交换",
    "pitfalls": [["找上升点用 < 不用 <=", "while nums[i] >= nums[i+1] 要跳过相等情况，否则遇到 [1,1,5] 会找错位置"], ["已最大时反转整个数组", "i 走到 -1 说明完全降序，直接反转整个数组回到最小排列"]],
    "selfcheck": [["为什么交换后还要把右侧反转？", "交换只保证「变大」，右侧当前是降序（最大），反转为升序（最小）才能保证这是「恰好多一点」的下一个。"], ["[3,2,1] 的下一排列是什么？", "从右到左一路降序，i=-1，直接反转整个数组得 [1,2,3]，即回到最小。"]],
}

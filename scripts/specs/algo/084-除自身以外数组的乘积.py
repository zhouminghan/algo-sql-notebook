from scripts.algo_gen import frame

PROBLEM = {
    "id": 84,
    "title": "除自身以外数组的乘积",
    "diff": "medium",
    "tags": ["前缀积"],
    "leetcode": 238,
    "origin": "https://leetcode.cn/problems/product-of-array-except-self/",
    "why": "答案[i] = 左边所有数的乘积 × 右边所有数的乘积。先从左到右累乘左前缀，再从右到左累乘右前缀，两遍 O(n)，不用除法、O(1) 额外空间。",
    "desc": """<p>给定整数数组，返回数组 <code>answer</code>，其中 <code>answer[i]</code> 等于 nums 中除 <code>nums[i]</code> 之外其余各元素的乘积。要求 O(n) 时间且<strong>不能使用除法</strong>。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4]</code> → <code>[24,12,8,6]</code></p>""",
    "frames": [
    frame("① 左前缀积：answer[i] 先存左边乘积", "drawTable", headers=["i", "0", "1", "2", "3"], rows=[["nums", "1", "2", "3", "4"], ["左前缀", "1", "1", "2", "6"]], width=460, height=130),
    frame("② 从右到左乘右前缀", "drawTable", headers=["i", "0", "1", "2", "3"], rows=[["右前缀", "24", "12", "4", "1"], ["结果", "24", "12", "8", "6"]], width=460, height=130),
    ],
    "conclusion": "左一遍 + 右一遍，两次前缀乘积合成就得到「除自己外」的乘积。",
    "py": """def productExceptSelf(nums):
    n = len(nums)
    ans = [1] * n
    left = 1
    for i in range(n):
        ans[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= right
        right *= nums[i]
    return ans""",
    "java": """public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    int left = 1;
    for (int i = 0; i < n; i++) { ans[i] = left; left *= nums[i]; }
    int right = 1;
    for (int i = n - 1; i >= 0; i--) { ans[i] *= right; right *= nums[i]; }
    return ans;
}""",
    "time": "O(n) — 两遍遍历",
    "space": "O(1) — 输出数组不计入额外空间",
    "pitfalls": [["不能用除法", "除法的 0 元素会除零，且题目明令禁止"], ["左右两遍", "先左后右，ans[i] 先存左边积，再乘右边积"]],
    "selfcheck": [["数组含 0 呢？", "两遍前缀法天然处理 0，不需要特判；除法则会出错。"], ["空间能更省吗？", "输出数组本身不算额外空间，已是 O(1) 额外空间的最优解。"]],
}

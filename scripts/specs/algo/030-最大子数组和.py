from scripts.algo_gen import frame

PROBLEM = {
    "id": 30,
    "title": "最大子数组和",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 53,
    "origin": "https://leetcode.cn/problems/maximum-subarray/",
    "why": "Kadane 算法：以 i 结尾的最大子数组和，要么接着前面的（pre + x），要么另起炉灶（x）。每步取较大者，同时更新全局最大，一次遍历 O(n)。",
    "desc": """<p>给定一个整数数组，找出一个具有<strong>最大和</strong>的连续子数组，返回其最大和。</p>
<p><strong>示例：</strong><br><code>[-2,1,-3,4,-1,2,1,-5,4]</code> → <code>6</code>（子数组 <code>[4,-1,2,1]</code>）</p>""",
    "frames": [
    frame("① 到 i 为止：接前面 or 另起", "drawTwoPointers", arr=[-2, 1, -3, 4, -1, 2, 1, -5, 4], left=3, right=6, window={"start": 3, "end": 6}, width=720, height=140),
    frame("② 递推：dp[i] = max(dp[i-1]+x, x)", "drawTable", headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8"], rows=[["nums", "-2", "1", "-3", "4", "-1", "2", "1", "-5", "4"], ["dp", "-2", "1", "-2", "4", "3", "5", "6", "1", "5"]], width=760, height=150),
    frame("③ 全局最大 = max(dp) = 6", "drawTwoPointers", arr=[-2, 1, -3, 4, -1, 2, 1, -5, 4], left=3, right=6, window={"start": 3, "end": 6}, width=720, height=140),
    ],
    "conclusion": "「当前子数组和」一旦变负就果断丢弃、重新开始，过程中记录到的最大值就是答案。",
    "py": """def maxSubArray(nums):
    cur = ans = nums[0]
    for x in nums[1:]:
        cur = max(cur + x, x)   # 接前面 或 另起
        ans = max(ans, cur)
    return ans""",
    "java": """public int maxSubArray(int[] nums) {
    int cur = nums[0], ans = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(cur + nums[i], nums[i]);
        ans = Math.max(ans, cur);
    }
    return ans;
}""",
    "time": "O(n) — 一次遍历",
    "space": "O(1) — 只维护两个变量",
    "pitfalls": [["全负数组", "cur 初始化为 nums[0] 并逐个比较，仍能返回最大的那个负数"], ["cur 变负要丢弃", "cur+x < x 时说明前面是累赘，应另起炉灶，这是 Kadane 的核心"]],
    "selfcheck": [["全负数组 [-2,-3,-1] 答案？", "-1。每步 cur 都会重置为当前更大的值，ans 保持 -1。"], ["需要记录子数组下标吗？", "本题只求最大和；若要下标，可在 cur 重置时记录起点，更新 ans 时记录终点。"]],
}

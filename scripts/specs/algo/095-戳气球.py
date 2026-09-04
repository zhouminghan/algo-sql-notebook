from scripts.algo_gen import frame

PROBLEM = {
    "id": 95,
    "title": "戳气球",
    "diff": "hard",
    "tags": ["DP"],
    "leetcode": 312,
    "origin": "https://leetcode.cn/problems/burst-balloons/",
    "why": "正着戳会改变邻居、子问题不独立。反过来：设 dp[i][j] 为「开区间 (i,j) 内能得到的最大硬币」，枚举最后戳的气球 k，dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j])。",
    "desc": """<p>有 n 个气球排成一排，每个气球上有数字 nums[i]。戳破第 i 个气球可得 <code>nums[i-1] * nums[i] * nums[i+1]</code> 枚硬币（越界处视为 1）。求最多硬币数。</p>
<p><strong>示例：</strong><br><code>[3,1,5,8]</code> → <code>167</code>（1→5→3→8 顺序）</p>""",
    "frames": [
    frame("① 两端补 1，dp[i][j] 为开区间 (i,j) 最大硬币", "drawTable", headers=["", "1", "3", "1", "5", "8", "1"], rows=[["补1后", "1", "3", "1", "5", "8", "1"]], width=560, height=110),
    frame("② 枚举最后戳 k：dp[i][j]=dp[i][k]+dp[k][j]+nums[i]*nums[k]*nums[j]", "drawTable", headers=["区间", "最后戳 k", "两侧", "金币"], rows=[["(0,2)", "k=1(值3)", "1*3*1", "3"]], width=500, height=130),
    frame("③ 按区间长度递增填表，答案 dp[0][n+1]", "drawTable", headers=["", "答案"], rows=[["最大硬币", {"val": "167", "highlight": True}]], width=420, height=110),
    ],
    "conclusion": "把「最后戳谁」当决策点，两侧区间互不影响，区间 DP 经典模型。",
    "py": """def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
    return dp[0][n - 1]""",
    "java": """public int maxCoins(int[] nums) {
    int m = nums.length;
    int[] a = new int[m + 2];
    a[0] = a[m + 1] = 1;
    System.arraycopy(nums, 0, a, 1, m);
    int n = m + 2;
    int[][] dp = new int[n][n];
    for (int len = 3; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            for (int k = i + 1; k < j; k++)
                dp[i][j] = Math.max(dp[i][j], dp[i][k] + dp[k][j] + a[i] * a[k] * a[j]);
        }
    return dp[0][n - 1];
}""",
    "time": "O(n³)",
    "space": "O(n²)",
    "pitfalls": [["枚举「最后戳」而非「第一个戳」", "戳第一个会改变两侧邻居，子问题耦合；最后戳则两侧已固定为 i、j"], ["两端补 1", "越界视为 1，补 1 后公式统一"]],
    "selfcheck": [["为什么区间长度从 3 开始？", "开区间 (i,j) 至少要有中间一个气球 k，即 j-i≥2。"], ["回溯思路 vs 正着贪心？", "贪心不行；区间 DP 把「最后戳谁」作为划分，保证子问题独立。"]],
}

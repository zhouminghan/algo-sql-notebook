from scripts.algo_gen import frame

PROBLEM = {
    "id": 72,
    "title": "打家劫舍",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 198,
    "origin": "https://leetcode.cn/problems/house-robber/",
    "why": "相邻房屋不能同时偷。dp[i] = max(dp[i-1], dp[i-2] + nums[i])：要么不偷当前、要么偷当前加上前两家的最优。滚动两个变量 O(1) 空间。",
    "desc": """<p>你是一排房屋，每间屋内有一定现金。相邻房屋装有报警器，如果相邻房屋同一晚被闯入会自动报警。求不触发警报的前提下能偷到的最高金额。</p>
<p><strong>示例：</strong><br><code>[1,2,3,1]</code> → <code>4</code>（偷 1 和 3）；<code>[2,7,9,3,1]</code> → <code>12</code></p>""",
    "frames": [
    frame("① dp[i] = max(dp[i-1], dp[i-2]+nums[i])", "drawTable", headers=["i", "0", "1", "2", "3", "4"], rows=[["nums", "2", "7", "9", "3", "1"], ["dp", "2", "7", "11", "11", "12"]], width=520, height=130),
    frame("② 偷当前 = dp[i-2]+nums[i]，不偷 = dp[i-1]", "drawTable", headers=["方案", "金额"], rows=[["偷 nums[4]=1", "dp[2]+1=12"], ["不偷", "dp[3]=11"], ["取 max", {"val": "12", "highlight": True}]], width=460, height=150),
    ],
    "conclusion": "相邻约束让「当前偷不偷」只依赖前两家，滚动即可。",
    "py": """def rob(nums):
    prev2 = prev = 0
    for x in nums:
        prev2, prev = prev, max(prev, prev2 + x)
    return prev""",
    "java": """public int rob(int[] nums) {
    int prev2 = 0, prev = 0;
    for (int x : nums) {
        int cur = Math.max(prev, prev2 + x);
        prev2 = prev; prev = cur;
    }
    return prev;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["初始化 0", "prev2=prev=0，处理空数组与第一家"], ["别贪心隔一个偷", "隔一个偷未必最优，必须 DP 比较「偷当前」与「不偷当前」"]],
    "selfcheck": [["[2,1,1,2] 答案？", "偷 0 和 3 得 4。贪心隔一偷会错过。"], ["首尾相连（打家劫舍 II）呢？", "分别算「去掉第一家」和「去掉最后一家」取较大者。"]],
}

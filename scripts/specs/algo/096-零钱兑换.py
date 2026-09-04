from scripts.algo_gen import frame

PROBLEM = {
    "id": 96,
    "title": "零钱兑换",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 322,
    "origin": "https://leetcode.cn/problems/coin-change/",
    "why": "凑出金额 i 的最少硬币数 dp[i] = min(dp[i - coin]) + 1。完全背包模型，硬币可无限用，逐金额填表，无法凑出则 -1。",
    "desc": """<p>给定不同面额的硬币 <code>coins</code> 和一个总金额 <code>amount</code>，计算凑出该金额所需的最少硬币个数。无解返回 -1。</p>
<p><strong>示例：</strong><br><code>coins=[1,2,5], amount=11</code> → <code>3</code>（5+5+1）；<code>coins=[2], amount=3</code> → <code>-1</code></p>""",
    "frames": [
    frame("① dp[i] = min(dp[i-coin]) + 1", "drawTable", headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"], rows=[["dp", "0", "1", "1", "2", "2", "1", "2", "2", "3", "3", "2", "3"]], width=800, height=130),
    frame("② amount=11：11-5=6(dp=2)、11-2=9(dp=3)、11-1=10(dp=2)，min=2+1=3", "drawTable", headers=["选硬币", "剩余", "剩余 dp", "总数"], rows=[["1", "10", "2", "3"], ["2", "9", "3", "4"], ["5", "6", "2", "3"]], width=460, height=160),
    ],
    "conclusion": "每种硬币都试一遍，取「剩余金额最优 + 1」的最小值。",
    "py": """def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if i >= c:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
    "java": """public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++)
        for (int c : coins)
            if (i >= c) dp[i] = Math.min(dp[i], dp[i - c] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}""",
    "time": "O(amount · len(coins))",
    "space": "O(amount)",
    "pitfalls": [["无解返回 -1", "用 amount+1 或 inf 初始化，最后判断是否被更新"], ["硬币可重复使用", "内层是金额循环，每个金额重新遍历所有硬币，等价完全背包"]],
    "selfcheck": [["coins=[2], amount=3？", "dp[3] 一直无法更新（3-2=1 无解），返回 -1。"], ["最少个数 vs 组合总数？", "本题求最少（取 min）；组合总数是另一个经典 DP，求累加和。"]],
}

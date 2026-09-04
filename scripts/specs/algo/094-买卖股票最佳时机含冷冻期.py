from scripts.algo_gen import frame

PROBLEM = {
    "id": 94,
    "title": "买卖股票最佳时机含冷冻期",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 309,
    "origin": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/",
    "why": "卖出后次日不能买入。用三状态 DP：hold（持有）、sold（刚卖出）、rest（空仓休息）。每天三态互相转移，最终答案是 max(sold, rest)。",
    "desc": """<p>可以多次买卖，但卖出后存在<strong>一天冷冻期</strong>：卖出股票的次日不能买入。求最大利润。</p>
<p><strong>示例：</strong><br><code>[1,2,3,0,2]</code> → <code>3</code>（买 1 卖 2、冷冻、买 0 卖 2）</p>""",
    "frames": [
    frame("① 三状态：持有 hold / 刚卖 sold / 空仓 rest", "drawTable", headers=["天", "1", "2", "3", "0", "2"], rows=[["hold", "-1", "-1", "-1", "1", "1"], ["sold", "0", "1", "2", "-1", "3"], ["rest", "0", "0", "1", "2", "2"]], width=520, height=160),
    frame("② 状态转移", "drawTable", headers=["转移", "公式"], rows=[["持有", "max(昨天持有, 昨天空仓 - 今日价)"], ["刚卖", "昨天持有 + 今日价"], ["空仓", "max(昨天空仓, 昨天刚卖)"]], width=540, height=160),
    frame("③ 答案 = max(sold, rest) = 3", "drawTwoPointers", arr=[1, 2, 3, 0, 2], left=0, right=1, window={"start": 0, "end": 1}, width=520, height=140),
    ],
    "conclusion": "冷冻期体现在「买入只能来自空仓状态」，即不能昨天刚卖今天买。",
    "py": """def maxProfit(prices):
    hold = float('-inf')
    sold = rest = 0
    for p in prices:
        new_hold = max(hold, rest - p)
        new_sold = hold + p
        new_rest = max(rest, sold)
        hold, sold, rest = new_hold, new_sold, new_rest
    return max(sold, rest)""",
    "java": """public int maxProfit(int[] prices) {
    int hold = Integer.MIN_VALUE, sold = 0, rest = 0;
    for (int p : prices) {
        int nh = Math.max(hold, rest - p);
        int ns = hold + p;
        int nr = Math.max(rest, sold);
        hold = nh; sold = ns; rest = nr;
    }
    return Math.max(sold, rest);
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["买入依赖 rest", "new_hold 用 rest-p 而非 sold-p，体现冷冻期"], ["状态同时更新", "先算新值再统一赋值，避免同一天状态串味"]],
    "selfcheck": [["为什么要有 sold 状态？", "若只有持有/空仓，无法表达「昨天刚卖今天不能买」，sold 专门标记刚卖出。"], ["最后一天可能持有吗？", "不可能是最优，答案取 max(sold, rest)，排除仍持有未卖出的情况。"]],
}

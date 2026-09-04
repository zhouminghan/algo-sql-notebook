from scripts.algo_gen import frame

PROBLEM = {
    "id": 54,
    "title": "买卖股票的最佳时机",
    "diff": "easy",
    "tags": ["贪心"],
    "leetcode": 121,
    "origin": "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/",
    "why": "只能买卖一次。遍历时维护「到今天为止的最低买入价」min_price，每天用当前价减去最低价更新最大利润。一次遍历 O(n)。",
    "desc": """<p>给定数组 <code>prices</code>，第 i 个元素表示股票第 i 天的价格。你只能选择<strong>某一天买入</strong>并在未来某一天卖出，求能获得的最大利润；不能获利则返回 0。</p>
<p><strong>示例：</strong><br><code>[7,1,5,3,6,4]</code> → <code>5</code>（第 2 天 1 买入，第 5 天 6 卖出）</p>""",
    "frames": [
    frame("① 维护历史最低价 min_price", "drawTwoPointers", arr=[7, 1, 5, 3, 6, 4], left=1, right=4, window={"start": 1, "end": 4}, width=560, height=150),
    frame("② 每天利润 = 当天价 - min_price，取最大", "drawTable", headers=["天", "0", "1", "2", "3", "4", "5"], rows=[["价格", "7", "1", "5", "3", "6", "4"], ["最低", "7", "1", "1", "1", "1", "1"], ["利润", "0", "0", "4", "2", "5", "3"]], width=620, height=160),
    frame("③ 最大利润 = 5", "drawTwoPointers", arr=[7, 1, 5, 3, 6, 4], left=1, right=4, window={"start": 1, "end": 4}, width=560, height=150),
    ],
    "conclusion": "最低价只降不升，每天算一次「当前能赚多少」，全局取最大。",
    "py": """def maxProfit(prices):
    min_price = float('inf')
    ans = 0
    for p in prices:
        min_price = min(min_price, p)
        ans = max(ans, p - min_price)
    return ans""",
    "java": """public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, ans = 0;
    for (int p : prices) {
        minPrice = Math.min(minPrice, p);
        ans = Math.max(ans, p - minPrice);
    }
    return ans;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["先更新 min 再算利润", "先 min 后 ans，保证「同一天不买卖」的语义；顺序反过来不影响结果但含义易混"], ["不能获利返回 0", "价格一路下跌时 ans 保持 0"]],
    "selfcheck": [["为什么贪心是对的？", "最大利润的卖出日固定时，买入价应取它之前的历史最低；遍历时 min_price 恰好维护了这一点。"], ["可以买卖多次呢？", "那就是 122 题，把每段「上涨」的差价累加即可。"]],
}

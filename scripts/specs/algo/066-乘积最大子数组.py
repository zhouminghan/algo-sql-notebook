from scripts.algo_gen import frame

PROBLEM = {
    "id": 66,
    "title": "乘积最大子数组",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 152,
    "origin": "https://leetcode.cn/problems/maximum-product-subarray/",
    "why": "乘积会因负数翻转：当前最小可能变最大。同时维护「以 i 结尾的最大乘积」和「最小乘积」，遇到负数交换两者再乘，取全局最大。",
    "desc": """<p>给定整数数组，找出乘积最大的连续子数组，返回该乘积。</p>
<p><strong>示例：</strong><br><code>[2,3,-2,4]</code> → <code>6</code>（[2,3]）；<code>[-2,0,-1]</code> → <code>0</code></p>""",
    "frames": [
    frame("① 同时维护 cur_max 与 cur_min", "drawTable", headers=["i", "0", "1", "2", "3"], rows=[["nums", "2", "3", "-2", "4"], ["cur_max", "2", "6", "-2", "4"], ["cur_min", "2", "3", "-12", "-48"]], width=520, height=150),
    frame("② 遇负数：max 与 min 互换再乘", "drawTable", headers=["步骤", "操作", "cur_max", "cur_min"], rows=[["-2 到来", "swap", "6→-12", "-12→6"]], width=460, height=130),
    frame("③ 全局最大 = 6", "drawTwoPointers", arr=[2, 3, -2, 4], left=0, right=1, window={"start": 0, "end": 1}, width=520, height=140),
    ],
    "conclusion": "最大最小一起维护，负数一来就互换，再与当前值比较更新。",
    "py": """def maxProduct(nums):
    ans = cur_max = cur_min = nums[0]
    for x in nums[1:]:
        if x < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)
        cur_min = min(x, cur_min * x)
        ans = max(ans, cur_max)
    return ans""",
    "java": """public int maxProduct(int[] nums) {
    int ans = nums[0], curMax = nums[0], curMin = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        if (x < 0) { int t = curMax; curMax = curMin; curMin = t; }
        curMax = Math.max(x, curMax * x);
        curMin = Math.min(x, curMin * x);
        ans = Math.max(ans, curMax);
    }
    return ans;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["同时维护最小值", "负数乘最小可能得到最大，只维护最大值会漏"], ["遇 0 重开", "x=0 时 cur_max=cur_min=0，下一个数自动另起炉灶"]],
    "selfcheck": [["[-2,0,-1] 为何是 0？", "以 0 为界，cur 归零，后面 -1 单段最大 -1，全局仍 0。"], ["为什么不能像最大子数组和那样只维护一个值？", "和是线性叠加，负贡献直接丢弃；乘积遇负会「翻倍变正」，必须保留最小乘积以防翻转。"]],
}

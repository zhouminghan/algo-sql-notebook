from scripts.algo_gen import frame

PROBLEM = {
    "id": 92,
    "title": "最长递增子序列",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 300,
    "origin": "https://leetcode.cn/problems/longest-increasing-subsequence/",
    "why": "dp[i] = 以 nums[i] 结尾的最长递增子序列长度，遍历前面所有更小元素取最大 +1。O(n²)；或用「贪心 + 二分」维护一个递增 tails 数组做到 O(n log n)。",
    "desc": """<p>给定整数数组，找到其中最长严格递增子序列的长度（子序列不要求连续）。</p>
<p><strong>示例：</strong><br><code>[10,9,2,5,3,7,101,18]</code> → <code>4</code>（[2,3,7,101]）</p>""",
    "frames": [
    frame("① dp[i] = max(前面更小元素的 dp) + 1", "drawTable", headers=["i", "0", "1", "2", "3", "4", "5", "6", "7"], rows=[["nums", "10", "9", "2", "5", "3", "7", "101", "18"], ["dp", "1", "1", "1", "2", "2", "3", "4", "4"]], width=700, height=130),
    frame("② 贪心 tails：维护最小结尾的递增序列", "drawTable", headers=["遍历", "tails"], rows=[["2", "[2]"], ["5", "[2,5]"], ["3", "[2,3]"], ["7", "[2,3,7]"], ["101", "[2,3,7,101]"]], width=460, height=210),
    ],
    "conclusion": "DP 版直观；二分版把「找前面更小」优化成「找 tails 中插入位置」，O(n log n)。",
    "py": """import bisect
def lengthOfLIS(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)""",
    "java": """public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int x : nums) {
        int l = 0, r = size;
        while (l < r) { int m = (l + r) >>> 1; if (tails[m] < x) l = m + 1; else r = m; }
        tails[l] = x;
        if (l == size) size++;
    }
    return size;
}""",
    "time": "O(n log n)",
    "space": "O(n)",
    "pitfalls": [["tails 不是真实子序列", "它只维护「最小结尾」，长度正确但内容可能不是某条真实子序列"], ["严格递增用 bisect_left", "相等元素要替换而非追加，否则会算成非严格递增"]],
    "selfcheck": [["为什么 tails 长度等于答案？", "tails 的每个槽位代表「长度为 k 的子序列的最小可能结尾」，能放更多槽位即答案。"], ["要输出具体子序列？", "二分法需额外记录前驱；DP 版记录 prev 可回溯。"]],
}

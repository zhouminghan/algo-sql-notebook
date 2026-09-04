from scripts.algo_gen import frame

PROBLEM = {
    "id": 56,
    "title": "最长连续序列",
    "diff": "medium",
    "tags": ["哈希表"],
    "leetcode": 128,
    "origin": "https://leetcode.cn/problems/longest-consecutive-sequence/",
    "why": "要求 O(n)。把数组放进集合，只从「序列起点」（num-1 不在集合里）开始向后数连续长度，每个元素最多被访问两次，避免排序的 O(n log n)。",
    "desc": """<p>给定一个未排序的整数数组，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。要求时间复杂度 O(n)。</p>
<p><strong>示例：</strong><br><code>[100,4,200,1,3,2]</code> → <code>4</code>（最长连续序列是 <code>[1,2,3,4]</code>）</p>""",
    "frames": [
    frame("① 放入集合，快速判断某个数是否存在", "drawTable", headers=["集合", "1", "2", "3", "4", "100", "200"], rows=[["存在", "✓", "✓", "✓", "✓", "✓", "✓"]], width=560, height=110),
    frame("② 只有「起点」（前一个数不在集合）才开始计数", "drawTable", headers=["数", "num-1 在?", "是起点?", "连续长度"], rows=[["1", "✗", "✓", "4"], ["4", "✓(3在)", "✗", "-"], ["100", "✗", "✓", "1"], ["200", "✗", "✓", "1"]], width=560, height=190),
    frame("③ 最长连续序列 [1,2,3,4]，长度 4", "drawTable", headers=["连续序列", "1", "2", "3", "4"], rows=[["是否在集合", "✓", "✓", "✓", "✓"]], width=560, height=120),
    ],
    "conclusion": "只从每个连续段的起点开始向后数，保证总工作量 O(n)。",
    "py": """def longestConsecutive(nums):
    s = set(nums)
    ans = 0
    for x in s:
        if x - 1 not in s:        # 只从起点开始
            cur, length = x, 1
            while cur + 1 in s:
                cur += 1
                length += 1
            ans = max(ans, length)
    return ans""",
    "java": """public int longestConsecutive(int[] nums) {
    Set<Integer> s = new HashSet<>();
    for (int x : nums) s.add(x);
    int ans = 0;
    for (int x : s) {
        if (!s.contains(x - 1)) {
            int cur = x, len = 1;
            while (s.contains(cur + 1)) { cur++; len++; }
            ans = Math.max(ans, len);
        }
    }
    return ans;
}""",
    "time": "O(n) — 每个元素至多被内层 while 访问两次",
    "space": "O(n) — 集合",
    "pitfalls": [["只从起点数", "若对每个数都向后数，会重复计算，最坏 O(n²)"], ["去重", "用 set 自动去重，重复元素不影响长度"]],
    "selfcheck": [["为什么复杂度仍是 O(n)？", "每个连续段只在其起点被数一次，段内每个元素最多被「向后找」访问一次，总访问量 ≤ 2n。"], ["空数组？", "返回 0。"]],
}

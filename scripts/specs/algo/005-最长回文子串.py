from scripts.algo_gen import frame

PROBLEM = {
    "id": 5,
    "title": "最长回文子串",
    "diff": "medium",
    "tags": ["DP", "双指针"],
    "leetcode": 5,
    "origin": "https://leetcode.cn/problems/longest-palindromic-substring/",
    "why": "中心扩展：回文串以某个字符（奇数长）或某两个字符之间（偶数长）为中心。枚举 2n-1 个中心，向两边扩展，记录最长。比 DP 更省空间、更直观。",
    "desc": "<p>给定字符串，找出其中<strong>最长</strong>的回文子串。</p><p><strong>示例：</strong><br><code>\"babad\"</code> → <code>\"bab\"</code>（或 \"aba\"）；<code>\"cbbd\"</code> → <code>\"bb\"</code></p>",
    "frames": [
    frame("① 奇数中心：以 b 向两边扩展 bab", "drawTwoPointers", arr=["b", "a", "b", "a", "d"], left=0, right=2, window={"start": 0, "end": 2}, height=130),
    frame("② 偶数中心：cbbd 中以 bb 之间为中心", "drawTwoPointers", arr=["c", "b", "b", "d"], left=1, right=2, window={"start": 1, "end": 2}, height=130),
    frame("③ 枚举所有中心，记录最长", "drawTwoPointers", arr=["b", "a", "b", "a", "d"], left=0, right=2, window={"start": 0, "end": 2}, height=130),
    ],
    "conclusion": "每个中心向两侧扩展，相等则继续，记录最长区间。",
    "py": """def longestPalindrome(s):
    n = len(s)
    start, max_len = 0, 1
    def expand(l, r):
        nonlocal start, max_len
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 > max_len:
                start, max_len = l, r - l + 1
            l -= 1; r += 1
    for i in range(n):
        expand(i, i)     # 奇数
        expand(i, i + 1) # 偶数
    return s[start:start + max_len]""",
    "java": """public String longestPalindrome(String s) {
    int n = s.length(), start = 0, maxLen = 1;
    for (int i = 0; i < n; i++) {
        int[] a = expand(s, i, i);
        int[] b = expand(s, i, i + 1);
        if (a[1] > maxLen) { start = a[0]; maxLen = a[1]; }
        if (b[1] > maxLen) { start = b[0]; maxLen = b[1]; }
    }
    return s.substring(start, start + maxLen);
}
int[] expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return new int[]{l + 1, r - l - 1};
}""",
    "time": "O(n²) — 2n-1 个中心各扩展 O(n)",
    "space": "O(1)",
    "pitfalls": [["奇偶中心都要试", "只试奇数会漏掉 \"cbbd\"→\"bb\" 这种偶数回文"], ["边界", "扩展时先判 l>=0 和 r<n"]],
    "selfcheck": [["\"cbbd\" 答案？", "\"bb\"，偶数中心 i=1 与 i+1 之间扩展得到。"], ["DP 做法？", "dp[i][j] 表示 s[i..j] 是否回文，由 dp[i+1][j-1] 推，O(n²) 时间 O(n²) 空间。"]],
}

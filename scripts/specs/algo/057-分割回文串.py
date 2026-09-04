from scripts.algo_gen import frame

PROBLEM = {
    "id": 57,
    "title": "分割回文串",
    "diff": "medium",
    "tags": ["回溯"],
    "leetcode": 131,
    "origin": "https://leetcode.cn/problems/palindrome-partitioning/",
    "why": "在字符串上枚举切割点：当前前缀是回文就切下，剩余部分递归分割。用回溯收集所有方案，配合回文预判避免重复判断。",
    "desc": """<p>给定字符串 <code>s</code>，将 s 分割成若干子串，使每个子串都是<strong>回文串</strong>。返回所有可能的分割方案。</p>
<p><strong>示例：</strong><br><code>s="aab"</code> → <code>[["a","a","b"],["aa","b"]]</code></p>""",
    "frames": [
    frame("① 在每个位置决定「切 / 不切」", "drawBacktrack", nodes=[{"val": "aab", "x": 300, "y": 15, "color": "normal"}, {"val": "a|ab", "x": 150, "y": 90, "color": "path"}, {"val": "aa|b", "x": 450, "y": 90, "color": "path"}, {"val": "a|a|b ✓", "x": 90, "y": 170, "color": "path"}, {"val": "a|ab ✗", "x": 210, "y": 170, "color": "pruned"}, {"val": "aa|b ✓", "x": 450, "y": 170, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 150, "y2": 90, "color": "path"}, {"x1": 300, "y1": 15, "x2": 450, "y2": 90, "color": "path"}, {"x1": 150, "y1": 90, "x2": 90, "y2": 170, "color": "path"}, {"x1": 150, "y1": 90, "x2": 210, "y2": 170, "color": "pruned"}, {"x1": 450, "y1": 90, "x2": 450, "y2": 170, "color": "path"}], width=560, height=220),
    frame("② 前缀回文才切下，否则剪枝", "drawTable", headers=["前缀", "回文?", "动作"], rows=[["a", "✓", "切下，递归 \"ab\""], ["aa", "✓", "切下，递归 \"b\""], ["aab", "✗", "不切"]], width=500, height=160),
    ],
    "conclusion": "枚举每个切点，前缀是回文就继续分割剩余部分，递归到底即得一种方案。",
    "py": """def partition(s):
    n = len(s)
    ans, path = [], []
    def dfs(start):
        if start == n:
            ans.append(path[:]); return
        for end in range(start, n):
            sub = s[start:end + 1]
            if sub == sub[::-1]:       # 前缀回文
                path.append(sub)
                dfs(end + 1)
                path.pop()
    dfs(0)
    return ans""",
    "java": """public List<List<String>> partition(String s) {
    List<List<String>> ans = new ArrayList<>();
    dfs(s, 0, new ArrayList<>(), ans);
    return ans;
}
void dfs(String s, int start, List<String> path, List<List<String>> ans) {
    if (start == s.length()) { ans.add(new ArrayList<>(path)); return; }
    for (int end = start; end < s.length(); end++) {
        if (isPal(s, start, end)) {
            path.add(s.substring(start, end + 1));
            dfs(s, end + 1, path, ans);
            path.remove(path.size() - 1);
        }
    }
}
boolean isPal(String s, int l, int r) {
    while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}""",
    "time": "O(n · 2^n) — 最坏每个前缀都是回文（如全 a）",
    "space": "O(n) — 递归栈 + path",
    "pitfalls": [["回溯恢复 path", "切下后要 pop，否则方案之间互相污染"], ["前缀回文判断", "用双指针或 sub==sub[::-1] 判断，别漏单字符（恒为回文）"]],
    "selfcheck": [["s 全相同字符如 \"aaa\"？", "每个前缀都回文，方案数为 2^(n-1)，这是最坏情况。"], ["如何优化回文判断？", "用 DP 预计算 pal[i][j]，把 isPal 从 O(n) 降到 O(1)。"]],
}

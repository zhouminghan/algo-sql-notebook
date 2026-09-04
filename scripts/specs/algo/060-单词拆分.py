from scripts.algo_gen import frame

PROBLEM = {
    "id": 60,
    "title": "单词拆分",
    "diff": "medium",
    "tags": ["DP"],
    "leetcode": 139,
    "origin": "https://leetcode.cn/problems/word-break/",
    "why": "dp[i] 表示 s 的前 i 个字符能否由词典拼出。dp[i] = 存在某个词典词，使得 dp[i-len] 为真且 s[i-len:i] 等于该词。逐位递推。",
    "desc": """<p>给定字符串 <code>s</code> 和字符串列表 <code>wordDict</code>，判断 s 是否能被空格拆分为一个或多个在词典中出现的单词。词典中单词可重复使用。</p>
<p><strong>示例：</strong><br><code>s="leetcode", wordDict=["leet","code"]</code> → <code>true</code>；<code>s="catsandog", wordDict=["cats","dog","sand","and","cat"]</code> → <code>false</code></p>""",
    "frames": [
    frame("① dp[i]：前 i 个字符能否拆分", "drawTable", headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8"], rows=[["dp", "T", "F", "F", "F", "T", "F", "F", "F", "T"]], width=700, height=120),
    frame("② dp[8] 由 dp[4] 且 s[4:8]=\"code\" 推出", "drawTable", headers=["子串", "leet", "code"], rows=[["在词典?", "✓", "✓"], ["起点 dp", "dp[0]=T", "dp[4]=T"]], width=460, height=140),
    ],
    "conclusion": "枚举结尾 i 与词长，能对上且前缀可拆就置真，最后看 dp[n]。",
    "py": """def wordBreak(s, wordDict):
    words = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for w in words:
            if i >= len(w) and dp[i - len(w)] and s[i - len(w):i] == w:
                dp[i] = True
                break
    return dp[n]""",
    "java": """public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> words = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i <= n; i++)
        for (String w : words)
            if (i >= w.length() && dp[i - w.length()] && s.substring(i - w.length(), i).equals(w)) {
                dp[i] = true; break;
            }
    return dp[n];
}""",
    "time": "O(n · m) — m 为词典单词数",
    "space": "O(n)",
    "pitfalls": [["dp[0]=True", "空前缀可拆分是递推起点"], ["用集合存词典", "list 查找 O(m)，set 查找 O(1)"]],
    "selfcheck": [["单词可重复使用吗？", "可以。词典是集合，只要子串匹配且前缀可拆，就能置真。"], ["\"catsandog\" 为何 false？", "cat→sand 可行但剩余 \"og\" 无法拆分；cats→and 后 \"og\" 也拆不了；dog 结尾则前缀 \"catsan\" 无法拆。"]],
}

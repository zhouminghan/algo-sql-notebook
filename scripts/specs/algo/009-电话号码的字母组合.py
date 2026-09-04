from scripts.algo_gen import frame

PROBLEM = {
    "id": 9,
    "title": "电话号码的字母组合",
    "diff": "medium",
    "tags": ["回溯", "哈希表"],
    "leetcode": 17,
    "origin": "https://leetcode.cn/problems/letter-combinations-of-a-phone-number/",
    "why": "每个数字对应几个字母，组合就是「每个位置选一个字母」的决策树。回溯逐位枚举，到底收集一个组合，再撤销换下一个。",
    "desc": "<p>给定仅含数字 2-9 的字符串，返回它能表示的所有字母组合。数字到字母的映射与电话按键相同。</p><p><strong>示例：</strong><br><code>\"23\"</code> → <code>[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]</code></p>",
    "frames": [
    frame("① 数字到字母的映射", "drawTable", headers=["数字", "2", "3"], rows=[["字母", "abc", "def"]], height=90),
    frame("② 决策树：每位选一个字母", "drawBacktrack", nodes=[{"val": "\"\"", "x": 300, "y": 15, "color": "normal"}, {"val": "a", "x": 150, "y": 85, "color": "path"}, {"val": "b", "x": 300, "y": 85, "color": "normal"}, {"val": "c", "x": 450, "y": 85, "color": "normal"}, {"val": "ad", "x": 100, "y": 160, "color": "path"}, {"val": "ae", "x": 160, "y": 160, "color": "path"}, {"val": "af", "x": 220, "y": 160, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 150, "y2": 85, "color": "path"}, {"x1": 150, "y1": 85, "x2": 100, "y2": 160, "color": "path"}, {"x1": 150, "y1": 85, "x2": 160, "y2": 160, "color": "path"}, {"x1": 150, "y1": 85, "x2": 220, "y2": 160, "color": "path"}], width=560, height=200),
    frame("③ 3×3=9 种组合", "drawTable", headers=["组合数", "9"], rows=[["ad,ae,af,bd,be,bf,cd,ce,cf", ""]], height=90),
    ],
    "conclusion": "每位枚举字母，深度等于数字个数，到底即收集。",
    "py": """def letterCombinations(digits):
    if not digits:
        return []
    mp = {'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    ans = []
    def dfs(i, path):
        if i == len(digits):
            ans.append(''.join(path)); return
        for ch in mp[digits[i]]:
            path.append(ch)
            dfs(i + 1, path)
            path.pop()
    dfs(0, [])
    return ans""",
    "java": """public List<String> letterCombinations(String digits) {
    if (digits.isEmpty()) return new ArrayList<>();
    String[] mp = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    List<String> ans = new ArrayList<>();
    dfs(digits, 0, new StringBuilder(), mp, ans);
    return ans;
}
void dfs(String d, int i, StringBuilder sb, String[] mp, List<String> ans) {
    if (i == d.length()) { ans.add(sb.toString()); return; }
    for (char c : mp[d.charAt(i) - '0'].toCharArray()) {
        sb.append(c); dfs(d, i + 1, sb, mp, ans); sb.deleteCharAt(sb.length() - 1);
    }
}""",
    "time": "O(3^m·4^n) — 组合数级别",
    "space": "O(组合数长度)",
    "pitfalls": [["空串返回 []", "digits 为空直接返回空列表，不能返回 [\"\"]"], ["回溯撤销", "path.append 后要 pop，否则路径串到别的分支"]],
    "selfcheck": [["\"23\" 为什么是 9 种？", "2 有 3 个字母、3 有 3 个字母，3×3=9。"], ["7 和 9 有几个字母？", "都是 4 个（pqrs / wxyz），其余是 3 个。"]],
}

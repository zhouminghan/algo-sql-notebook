from scripts.algo_gen import frame

PROBLEM = {
    "id": 3,
    "title": "无重复字符的最长子串",
    "diff": "medium",
    "tags": ["滑动窗口", "哈希表"],
    "leetcode": 3,
    "origin": "https://leetcode.cn/problems/longest-substring-without-repeating-characters/",
    "why": "维护一个「无重复字符」的窗口，右指针扩张、左指针在遇到重复时收缩。用哈希集合记录窗口内字符，O(n) 一次扫完。",
    "desc": "<p>给定字符串，找出其中<strong>不含重复字符</strong>的最长子串的长度。</p><p><strong>示例：</strong><br><code>\"abcabcbb\"</code> → <code>3</code>（abc）；<code>\"bbbbb\"</code> → <code>1</code></p>",
    "frames": [
    frame("① 右指针扩张，字符进集合", "drawTwoPointers", arr=["a", "b", "c", "a", "b", "c", "b", "b"], left=0, right=2, window={"start": 0, "end": 2}, height=130),
    frame("② 遇到重复 a，左指针收缩到重复之后", "drawTwoPointers", arr=["a", "b", "c", "a", "b", "c", "b", "b"], left=3, right=3, window={"start": 1, "end": 3}, height=130),
    frame("③ 全程记录窗口最大长度", "drawTwoPointers", arr=["a", "b", "c", "a", "b", "c", "b", "b"], left=5, right=7, window={"start": 5, "end": 7}, height=130),
    ],
    "conclusion": "窗口内始终无重复，右扩左缩，记录最大宽度。",
    "py": """def lengthOfLongestSubstring(s):
    window = set()
    l = ans = 0
    for r, ch in enumerate(s):
        while ch in window:
            window.remove(s[l])
            l += 1
        window.add(ch)
        ans = max(ans, r - l + 1)
    return ans""",
    "java": """public int lengthOfLongestSubstring(String s) {
    Set<Character> set = new HashSet<>();
    int l = 0, ans = 0;
    for (int r = 0; r < s.length(); r++) {
        while (set.contains(s.charAt(r))) set.remove(s.charAt(l++));
        set.add(s.charAt(r));
        ans = Math.max(ans, r - l + 1);
    }
    return ans;
}""",
    "time": "O(n) — 左右指针各走一遍",
    "space": "O(字符集) — 集合",
    "pitfalls": [["左指针要 while 收缩", "重复字符可能在窗口内部，需一直删到把重复字符移除为止"], ["更新答案的时机", "每次右扩后都要用 r-l+1 更新最大"]],
    "selfcheck": [["\"pwwkew\" 答案？", "3（wke）。遇到第二个 w 时左指针跳到第一个 w 之后。"], ["为什么用 while 不用 if？", "重复字符位置不确定，if 只删一个可能删不掉窗口里的那个重复字符。"]],
}

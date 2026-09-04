from scripts.algo_gen import frame

PROBLEM = {
    "id": 39,
    "title": "最小覆盖子串",
    "diff": "hard",
    "tags": ["滑动窗口"],
    "leetcode": 76,
    "origin": "https://leetcode.cn/problems/minimum-window-substring/",
    "why": "用滑动窗口在 s 上滑：右指针扩大窗口直到「覆盖 t 所有字符」，再左指针收缩到「刚好还覆盖」为止，记录最短。用哈希表计数判断是否覆盖。",
    "desc": """<p>给定字符串 <code>s</code> 和 <code>t</code>，返回 s 中涵盖 t 所有字符的最小子串；不存在则返回空串。</p>
<p><strong>示例：</strong><br><code>s="ADOBECODEBANC", t="ABC"</code> → <code>"BANC"</code></p>""",
    "frames": [
    frame("① 右指针扩大窗口，直到覆盖 t=ABC", "drawTwoPointers", arr=["A", "D", "O", "B", "E", "C", "O", "D", "E", "B", "A", "N", "C"], left=0, right=5, window={"start": 0, "end": 5}, width=720, height=150),
    frame("② 左指针收缩，记录最短覆盖窗口", "drawTwoPointers", arr=["A", "D", "O", "B", "E", "C", "O", "D", "E", "B", "A", "N", "C"], left=9, right=12, window={"start": 9, "end": 12}, width=720, height=150),
    frame("③ 最短子串 = \"BANC\"", "drawTable", headers=["窗口", "值"], rows=[["子串", "BANC"], ["长度", "4"]], width=420, height=130),
    ],
    "conclusion": "右扩到「覆盖」，左缩到「最小仍覆盖」，反复滑动取全局最短。",
    "py": """from collections import Counter
def minWindow(s, t):
    need = Counter(t)
    need_cnt = len(need)
    window = {}
    have = 0
    l = 0
    ans, ans_len = "", float("inf")
    for r, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == need_cnt:            # 已覆盖，尝试收缩
            if r - l + 1 < ans_len:
                ans, ans_len = s[l:r + 1], r - l + 1
            left_ch = s[l]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                have -= 1
            l += 1
    return ans""",
    "java": """public String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int needCnt = 0;
    for (int x : need) if (x > 0) needCnt++;
    int[] win = new int[128];
    int have = 0, l = 0, start = 0, len = Integer.MAX_VALUE;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (++win[c] == need[c]) have++;
        while (have == needCnt) {
            if (r - l + 1 < len) { start = l; len = r - l + 1; }
            char d = s.charAt(l);
            if (win[d] == need[d]) have--;
            win[d]--; l++;
        }
    }
    return len == Integer.MAX_VALUE ? "" : s.substring(start, start + len);
}""",
    "time": "O(|s|) — 左右指针各扫一遍",
    "space": "O(字符集) — 计数表",
    "pitfalls": [["覆盖判定用 have==need_cnt", "只有某字符计数「恰好达到需求」时 have 才 +1，多了不重复加"], ["收缩时先减再判断", "移出左边界字符后，若其计数掉到需求以下，覆盖数 have 才 -1"]],
    "selfcheck": [["t 中字符有重复呢？", "need 记录每个字符需求次数，window 计数与之比较，重复字符必须凑够数量才算覆盖。"], ["s 中不存在覆盖子串？", "have 永远达不到 needCnt，ans 保持空串，最后返回 \"\"。"]],
}

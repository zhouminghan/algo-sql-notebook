from scripts.algo_gen import frame

PROBLEM = {
    "id": 28,
    "title": "字母异位词分组",
    "diff": "medium",
    "tags": ["哈希表"],
    "leetcode": 49,
    "origin": "https://leetcode.cn/problems/group-anagrams/",
    "why": "互为字母异位词的单词，排序后完全相同。把「排序后的串」作为 key 分组，每个单词 O(k log k) 排序 + O(1) 查表，即可把所有变位词归到一起。",
    "desc": """<p>给定一个字符串数组，将所有字母异位词组合在一起。字母异位词指由相同字母、相同个数重新排列得到的字符串。</p>
<p><strong>示例：</strong><br><code>["eat","tea","tan","ate","nat","bat"]</code> → <code>[["eat","tea","ate"],["tan","nat"],["bat"]]</code></p>""",
    "frames": [
    frame("① 每个词排序，作为分组 key", "drawTable", headers=["单词", "排序后 key"], rows=[["eat", "aet"], ["tea", "aet"], ["tan", "ant"], ["ate", "aet"], ["nat", "ant"], ["bat", "abt"]], width=460, height=240),
    frame("② key 相同归入同一组", "drawTable", headers=["key", "组内单词"], rows=[["aet", "eat, tea, ate"], ["ant", "tan, nat"], ["abt", "bat"]], width=460, height=170),
    ],
    "conclusion": "排序串就是变位词的「指纹」，同指纹的单词天然属于同一组。",
    "py": """from collections import defaultdict
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())""",
    "java": """public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        char[] a = s.toCharArray();
        Arrays.sort(a);
        String key = new String(a);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}""",
    "time": "O(n · k log k) — n 个词，每个长度 k 排序",
    "space": "O(n · k) — 存储所有字符串",
    "pitfalls": [["key 要用排序后的完整串", "不能只统计字母出现次数但不排序（那样要自定义可哈希 key），排序串最简单直观"], ["返回形式", "只需返回分组后的列表，组内与组间顺序都无所谓"]],
    "selfcheck": [["能否用字母计数代替排序？", "可以，用 26 位计数数组转成不可变 key（如元组），时间可降到 O(nk)，但实现略繁，排序法更直观。"], ["\"\"（空串）和单字母词怎么处理？", "空串排序后仍为空串 key；单字母词各自成组，逻辑自然覆盖。"]],
}

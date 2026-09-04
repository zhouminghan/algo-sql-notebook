from scripts.algo_gen import frame

PROBLEM = {
    "id": 32,
    "title": "合并区间",
    "diff": "medium",
    "tags": ["排序"],
    "leetcode": 56,
    "origin": "https://leetcode.cn/problems/merge-intervals/",
    "why": "先按左端点排序，重叠的区间在排序后必然相邻。一次遍历：当前区间与结果栈顶有重叠就扩展右端点，否则作为新区间入栈。",
    "desc": """<p>以数组 <code>intervals</code> 表示若干个区间的集合，其中 <code>intervals[i] = [start, end]</code>。合并所有重叠的区间，返回一个不重叠的区间数组。</p>
<p><strong>示例：</strong><br><code>[[1,3],[2,6],[8,10],[15,18]]</code> → <code>[[1,6],[8,10],[15,18]]</code></p>""",
    "frames": [
    frame("① 按左端点排序", "drawTable", headers=["区间", "1", "2", "3", "4"], rows=[["排序前", "[1,3]", "[2,6]", "[8,10]", "[15,18]"], ["排序后", "[1,3]", "[2,6]", "[8,10]", "[15,18]"]], width=520, height=150),
    frame("② [1,3] 与 [2,6] 重叠 → 合并为 [1,6]", "drawTable", headers=["结果", "0", "1", "2"], rows=[["合并后", {"val": "[1,6]", "highlight": True}, "[8,10]", "[15,18]"]], width=520, height=120),
    frame("③ [8,10] 与 [15,18] 不重叠，各自保留", "drawTable", headers=["结果", "0", "1", "2"], rows=[["最终", "[1,6]", "[8,10]", "[15,18]"]], width=520, height=120),
    ],
    "conclusion": "排序让「可能重叠的区间」相邻，合并判断只看当前区间与已合并区间的右端点。",
    "py": """def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for iv in intervals:
        if not res or res[-1][1] < iv[0]:
            res.append(iv)              # 无重叠
        else:
            res[-1][1] = max(res[-1][1], iv[1])  # 扩展右端点
    return res""",
    "java": """public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> res = new ArrayList<>();
    for (int[] iv : intervals) {
        if (res.isEmpty() || res.get(res.size() - 1)[1] < iv[0]) res.add(iv);
        else res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], iv[1]);
    }
    return res.toArray(new int[0][]);
}""",
    "time": "O(n log n) — 排序主导",
    "space": "O(n) — 结果数组",
    "pitfalls": [["重叠判断", "res[-1][1] >= iv[0] 即重叠（含端点相接），右端点取 max 而非直接覆盖"], ["必须先排序", "不排序的话重叠区间不相邻，线性合并会漏并"]],
    "selfcheck": [["[1,4] 与 [4,5] 算重叠吗？", "算。4 相接，合并为 [1,5]，因为 res[-1][1] >= iv[0] 成立。"], ["区间完全被包含如 [1,4] 与 [2,3]？", "右端点取 max(4,3)=4，结果仍是 [1,4]，被包含的区间自然吸收。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 53,
    "title": "杨辉三角",
    "diff": "easy",
    "tags": ["DP"],
    "leetcode": 118,
    "origin": "https://leetcode.cn/problems/pascals-triangle/",
    "why": "每行首尾是 1，中间每个数 = 上一行相邻两数之和。逐行生成即可，是典型的递推填表。",
    "desc": """<p>给定非负整数 <code>numRows</code>，生成杨辉三角的前 numRows 行。杨辉三角中每个数是它左上方和右上方的数之和。</p>
<p><strong>示例：</strong><br><code>numRows=5</code> → <code>[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]</code></p>""",
    "frames": [
    frame("① 每行首尾 1，中间 = 左上 + 右上", "drawTable", headers=["行", "内容"], rows=[["0", "1"], ["1", "1, 1"], ["2", "1, 2, 1"], ["3", "1, 3, 3, 1"], ["4", "1, 4, 6, 4, 1"]], width=460, height=230),
    frame("② 递推：cur[j] = prev[j-1] + prev[j]", "drawTable", headers=["j", "0", "1", "2", "3", "4"], rows=[["上一行", "1", "3", "3", "1", ""], ["本行", "1", {"val": "4", "highlight": True}, "6", "4", "1"]], width=460, height=140),
    ],
    "conclusion": "一行一行填，中间元素由上一行相邻两项相加得到。",
    "py": """def generate(numRows):
    res = []
    for i in range(numRows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = res[-1][j - 1] + res[-1][j]
        res.append(row)
    return res""",
    "java": """public List<List<Integer>> generate(int numRows) {
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < numRows; i++) {
        List<Integer> row = new ArrayList<>();
        for (int j = 0; j <= i; j++) {
            if (j == 0 || j == i) row.add(1);
            else row.add(res.get(i - 1).get(j - 1) + res.get(i - 1).get(j));
        }
        res.add(row);
    }
    return res;
}""",
    "time": "O(numRows²)",
    "space": "O(numRows²) — 结果本身",
    "pitfalls": [["首尾处理", "j==0 或 j==i 时固定为 1，中间才相加"], ["用上一行", "本行依赖 res[-1]，确保上一行已生成"]],
    "selfcheck": [["numRows=0？", "返回空列表。"], ["第 n 行第 k 个数与组合数的关系？", "等于 C(n,k)，杨辉三角本质就是二项式系数的递推。"]],
}

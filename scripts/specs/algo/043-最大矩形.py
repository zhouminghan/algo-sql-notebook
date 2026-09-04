from scripts.algo_gen import frame

PROBLEM = {
    "id": 43,
    "title": "最大矩形",
    "diff": "hard",
    "tags": ["单调栈"],
    "leetcode": 85,
    "origin": "https://leetcode.cn/problems/maximal-rectangle/",
    "why": "把矩阵每一行看成「柱状图」：以当前行为底，向上连续 1 的个数就是柱子高度。逐行构造 heights，对每行跑一次「柱状图最大矩形」的单调栈，取全局最大。",
    "desc": """<p>给定一个仅包含 0 和 1、大小为 m×n 的二维二进制矩阵，找出只包含 1 的最大矩形，并返回其面积。</p>
<p><strong>示例：</strong><br><code>[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]</code> → <code>6</code></p>""",
    "frames": [
    frame("① 以第 2 行为底，向上连续 1 构成柱状图", "drawTable", headers=["", "0", "1", "2", "3", "4"], rows=[["矩阵", "1", "0", "1", "0", "0"], ["1", "1", "0", "1", "1", "1"], ["2", "1", "1", "1", "1", "1"], ["heights", "3", "1", "3", "2", "2"]], width=500, height=200),
    frame("② 对该柱状图跑单调栈求最大矩形", "drawTwoPointers", arr=[3, 1, 3, 2, 2], left=0, right=4, width=520, height=140),
    frame("③ 逐行更新 heights，取全局最大面积", "drawTable", headers=["行", "heights", "最大矩形"], rows=[["0", "1,0,1,0,0", "1"], ["1", "2,0,2,1,1", "3"], ["2", "3,1,3,2,2", {"val": "6", "highlight": True}]], width=500, height=170),
    ],
    "conclusion": "把二维问题拆成「每一行作为底的柱状图问题」，复用单调栈模板，O(m·n) 求解。",
    "py": """def maximalRectangle(matrix):
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    heights = [0] * n
    ans = 0
    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        ans = max(ans, largestRectangleArea(heights))
    return ans


def largestRectangleArea(heights):
    stack, ans = [], 0
    hs = heights + [0]
    for i, h in enumerate(hs):
        while stack and hs[stack[-1]] > h:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            ans = max(ans, hs[cur] * (i - left - 1))
        stack.append(i)
    return ans""",
    "java": """public int maximalRectangle(char[][] matrix) {
    if (matrix.length == 0 || matrix[0].length == 0) return 0;
    int n = matrix[0].length, ans = 0;
    int[] h = new int[n];
    for (char[] row : matrix) {
        for (int j = 0; j < n; j++)
            h[j] = row[j] == '1' ? h[j] + 1 : 0;
        ans = Math.max(ans, largestRectangleArea(h));
    }
    return ans;
}
int largestRectangleArea(int[] heights) {
    int n = heights.length, ans = 0;
    int[] h = new int[n + 1];
    System.arraycopy(heights, 0, h, 0, n);
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        while (!st.isEmpty() && h[st.peek()] > h[i]) {
            int cur = st.pop(), left = st.isEmpty() ? -1 : st.peek();
            ans = Math.max(ans, h[cur] * (i - left - 1));
        }
        st.push(i);
    }
    return ans;
}""",
    "time": "O(m · n) — 每行一次单调栈",
    "space": "O(n) — 高度数组 + 栈",
    "pitfalls": [["heights 遇 0 归零", "row[j]=='0' 时该列高度直接清零，不是保持原值"], ["复用 84 题", "先把「柱状图最大矩形」写对，本行逻辑只是逐行喂 heights"]],
    "selfcheck": [["为什么不是 O(m·n²)？", "每行单调栈 O(n)，共 m 行，总计 O(m·n)。"], ["第一行怎么算？", "heights 初始全 0，第一行遇到 1 就为 1、遇到 0 就为 0，自然形成柱状图。"]],
}

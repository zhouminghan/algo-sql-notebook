from scripts.algo_gen import frame

PROBLEM = {
    "id": 42,
    "title": "柱状图中最大的矩形",
    "diff": "hard",
    "tags": ["单调栈"],
    "leetcode": 84,
    "origin": "https://leetcode.cn/problems/largest-rectangle-in-histogram/",
    "why": "对每根柱子，以它高度为高的最大矩形，向左右延伸到「第一个比它矮的柱子」为止。单调递增栈能在 O(n) 内同时找到每根柱子左右两侧最近更矮的位置。",
    "desc": """<p>给定 n 个非负整数表示柱状图的高度（每个柱宽 1），求图中能勾勒出的最大矩形面积。</p>
<p><strong>示例：</strong><br><code>heights=[2,1,5,6,2,3]</code> → <code>10</code></p>""",
    "frames": [
    frame("① 以高度 5 为高的矩形：左右延伸到第一个更矮处", "drawTwoPointers", arr=[2, 1, 5, 6, 2, 3], left=2, right=3, window={"start": 2, "end": 3}, width=560, height=150),
    frame("② 以高度 2（下标 4）为高：向左延伸到 1 之后，向右到末尾", "drawTwoPointers", arr=[2, 1, 5, 6, 2, 3], left=4, right=5, window={"start": 1, "end": 5}, width=560, height=150),
    frame("③ 单调栈：栈内高度递增，遇到更矮就弹出并结算", "drawStack", items=[{"val": "2"}, {"val": "5"}, {"val": "6"}], type="stack", height=170),
    ],
    "conclusion": "单调栈维护「递增高度」，每次弹出高度 h 时，其可扩展宽度 = 当前下标 - 新栈顶下标 - 1，面积 = h × 宽。",
    "py": """def largestRectangleArea(heights):
    stack = []
    ans = 0
    heights = heights + [0]        # 末尾加 0 逼出所有栈
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            ans = max(ans, heights[cur] * (i - left - 1))
        stack.append(i)
    return ans""",
    "java": """public int largestRectangleArea(int[] heights) {
    int n = heights.length, ans = 0;
    int[] h = new int[n + 1];
    System.arraycopy(heights, 0, h, 0, n);
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        while (!st.isEmpty() && h[st.peek()] > h[i]) {
            int cur = st.pop();
            int left = st.isEmpty() ? -1 : st.peek();
            ans = Math.max(ans, h[cur] * (i - left - 1));
        }
        st.push(i);
    }
    return ans;
}""",
    "time": "O(n) — 每个下标入栈出栈一次",
    "space": "O(n) — 栈",
    "pitfalls": [["末尾补 0", "补一个高度 0 的哨兵，循环结束时能自动弹出所有剩余柱子结算"], ["宽度计算", "弹出 cur 后，新栈顶就是它左边最近的更矮位置，宽 = i - left - 1"]],
    "selfcheck": [["为什么用单调递增栈？", "栈内高度递增意味着每个柱子的「左边界」已知；遇到更矮柱子时，它就成了右侧边界，可立即结算被弹出的柱子。"], ["[2,1,2] 的最大矩形？", "高度 2 的矩形（下标 0 和 2 分别面积 2），以及高度 1 横跨全长的面积 3，答案为 3。"]],
}

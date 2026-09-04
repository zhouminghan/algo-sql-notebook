from scripts.algo_gen import frame

PROBLEM = {
    "id": 24,
    "title": "接雨水",
    "diff": "hard",
    "tags": ["双指针"],
    "leetcode": 42,
    "origin": "https://leetcode.cn/problems/trapping-rain-water/",
    "why": "每根柱子上能接多少水，由「左右两边最高柱子中的较矮者」决定。用左右双指针维护 leftMax / rightMax，谁小就结算谁，一次遍历 O(n)，无需提前建两个数组。",
    "desc": """<p>给定 <code>n</code> 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。</p>
<p><strong>示例：</strong><br><code>height=[0,1,0,2,1,0,1,3,2,1,2,1]</code> → <code>6</code></p>""",
    "frames": [
    frame("① 左指针在 0，右指针在末尾，维护 leftMax/rightMax", "drawTwoPointers", arr=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], left=0, right=11, width=720, height=140),
    frame("② leftMax < rightMax 时结算左指针，并右移", "drawTwoPointers", arr=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], left=4, right=11, window={"start": 2, "end": 3}, width=720, height=140),
    frame("③ 直到两指针相遇，累计雨水 = 6", "drawTwoPointers", arr=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], left=7, right=7, width=720, height=140),
    ],
    "conclusion": "每步只结算「较矮那侧」的柱子：它能接的水 = 该侧当前最高 - 自身高度，指针向中间推进直到相遇。",
    "py": """def trap(height):
    l, r = 0, len(height) - 1
    left_max = right_max = 0
    ans = 0
    while l < r:
        left_max = max(left_max, height[l])
        right_max = max(right_max, height[r])
        if left_max < right_max:
            ans += left_max - height[l]
            l += 1
        else:
            ans += right_max - height[r]
            r -= 1
    return ans""",
    "java": """public int trap(int[] height) {
    int l = 0, r = height.length - 1, leftMax = 0, rightMax = 0, ans = 0;
    while (l < r) {
        leftMax = Math.max(leftMax, height[l]);
        rightMax = Math.max(rightMax, height[r]);
        if (leftMax < rightMax) { ans += leftMax - height[l]; l++; }
        else                    { ans += rightMax - height[r]; r--; }
    }
    return ans;
}""",
    "time": "O(n) — 每个柱子访问一次",
    "space": "O(1)",
    "pitfalls": [["结算哪一侧", "leftMax < rightMax 时，左柱的水量由 leftMax 决定，与更远的右墙无关——这是双指针正确的关键"], ["先更新 max 再结算", "height[l] 可能比 leftMax 高，此时 leftMax - height[l] = 0，不会减出负数"]],
    "selfcheck": [["为什么 leftMax < rightMax 时可以直接结算左柱？", "因为右边一定存在一根 >= rightMax > leftMax 的墙，左柱的水只受 leftMax 限制，右墙具体多高不再重要。"], ["单调递增的数组能接水吗？", "不能。leftMax 永远 <= 右侧，每次 leftMax-height[l] 在更新后都为 0，答案为 0。"]],
}

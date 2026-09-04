from scripts.algo_gen import frame

PROBLEM = {
    "id": 7,
    "title": "盛最多水的容器",
    "diff": "medium",
    "tags": ["双指针", "贪心"],
    "leetcode": 11,
    "origin": "https://leetcode.cn/problems/container-with-most-water/",
    "why": "面积 = 两柱距离 × 较矮柱高。双指针从两端向中间收，每次移动较矮的一侧——因为移动较高侧不可能让面积更大，O(n) 一次扫完。",
    "desc": "<p>给定数组 <code>height</code>，第 i 个元素表示第 i 条垂线的高度。找出其中两条线，与 x 轴构成的容器能装<strong>最多</strong>的水。</p><p><strong>示例：</strong><br><code>[1,8,6,2,5,4,8,3,7]</code> → <code>49</code></p>",
    "frames": [
    frame("① 两端指针，面积 = 距离 × 较矮高", "drawTwoPointers", arr=[1, 8, 6, 2, 5, 4, 8, 3, 7], left=0, right=8, height=130),
    frame("② 移动较矮的一侧，继续算面积", "drawTwoPointers", arr=[1, 8, 6, 2, 5, 4, 8, 3, 7], left=1, right=8, height=130),
    frame("③ 直到指针相遇，记录最大面积 49", "drawTwoPointers", arr=[1, 8, 6, 2, 5, 4, 8, 3, 7], left=1, right=6, height=130),
    ],
    "conclusion": "每次放弃较矮的边，因为更高的边才可能带来更大面积。",
    "py": """def maxArea(height):
    l, r = 0, len(height)-1
    ans = 0
    while l < r:
        ans = max(ans, (r-l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return ans""",
    "java": """public int maxArea(int[] h) {
    int l = 0, r = h.length - 1, ans = 0;
    while (l < r) {
        ans = Math.max(ans, (r - l) * Math.min(h[l], h[r]));
        if (h[l] < h[r]) l++; else r--;
    }
    return ans;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["移动较矮侧", "移动较高侧宽度减小、高度不会更高，面积只可能更小"], ["面积用 min 高度", "瓶颈是较矮的柱子，不是平均或较高者"]],
    "selfcheck": [["为什么移动较矮侧一定对？", "宽度必然减 1，只有抬高较矮边才可能补偿宽度损失。"], ["全相等高度 [1,1,1]？", "任意两边面积相同，答案是 2。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 31,
    "title": "跳跃游戏",
    "diff": "medium",
    "tags": ["贪心"],
    "leetcode": 55,
    "origin": "https://leetcode.cn/problems/jump-game/",
    "why": "只要「能到达的最远下标」不断推进并最终 ≥ 末尾，就一定可达。贪心维护 farthest，比 DP 更简单，O(n) 即可。",
    "desc": """<p>给定非负整数数组 <code>nums</code>，最初位于第一个下标。每个元素表示在该位置可跳跃的最大长度。判断能否到达最后一个下标。</p>
<p><strong>示例：</strong><br><code>[2,3,1,1,4]</code> → <code>true</code><br><code>[3,2,1,0,4]</code> → <code>false</code></p>""",
    "frames": [
    frame("① 从 0 跳最远到 2", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=0, right=2, width=520, height=140),
    frame("② 途中更新最远：1→2、2→4、3→4", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=2, right=4, window={"start": 0, "end": 2}, width=520, height=140),
    frame("③ farthest=4 覆盖末尾 → 可达", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=4, right=4, window={"start": 0, "end": 4}, width=520, height=140),
    ],
    "conclusion": "只要当前位置还在「最远可达」范围内，就不断把最远可达向前推进；越过末尾即成功。",
    "py": """def canJump(nums):
    farthest = 0
    for i, x in enumerate(nums):
        if i > farthest:      # 当前位置都到不了
            return False
        farthest = max(farthest, i + x)
        if farthest >= len(nums) - 1:
            return True
    return True""",
    "java": """public boolean canJump(int[] nums) {
    int farthest = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > farthest) return false;
        farthest = Math.max(farthest, i + nums[i]);
        if (farthest >= nums.length - 1) return true;
    }
    return true;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["i > farthest 判不可达", "中间一旦出现「当前位置已超出最远可达」，后面全是死区，直接返回 false"], ["提前返回 true", "farthest >= n-1 即可提前结束，不用遍历到底"]],
    "selfcheck": [["[3,2,1,0,4] 为什么 false？", "最远只能到 3，而 nums[3]=0 无法前进到 4，卡死在 0。"], ["和「跳跃游戏 II」区别？", "I 只判断可达性（贪心维护 farthest）；II 求最少步数（需维护当前步边界 end）。"]],
}

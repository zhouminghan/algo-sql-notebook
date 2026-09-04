from scripts.algo_gen import frame

PROBLEM = {
    "id": 25,
    "title": "跳跃游戏 II",
    "diff": "medium",
    "tags": ["贪心"],
    "leetcode": 45,
    "origin": "https://leetcode.cn/problems/jump-game-ii/",
    "why": "求最少步数，贪心思路是「每走一步都尽量覆盖最远」。维护当前步能覆盖的边界 end，走到边界就 +1 步并更新下一跳的最远边界，保证步数最少。",
    "desc": """<p>给定一个非负整数数组 <code>nums</code>，最初位于数组第一个下标。数组中的每个元素代表你在该位置可以跳跃的最大长度。求到达最后一个下标的最少跳跃次数。保证可达。</p>
<p><strong>示例：</strong><br><code>nums=[2,3,1,1,4]</code> → <code>2</code>（0→1→4）</p>""",
    "frames": [
    frame("① 从 0 跳：最远可达 2，end=2", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=0, right=2, width=520, height=140),
    frame("② 走到边界 end=2 时，步数 +1，新最远 = max(1+2, 2+1)=4", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=2, right=4, width=520, height=140),
    frame("③ 最远已覆盖末尾，共 2 步", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=4, right=4, window={"start": 1, "end": 4}, width=520, height=140),
    ],
    "conclusion": "把「当前位置能到的最远」不断更新，每当走到本步边界就记一步并切换到新的最远边界。",
    "py": """def jump(nums):
    n = len(nums)
    steps = end = farthest = 0
    for i in range(n - 1):       # 最后一位不用跳
        farthest = max(farthest, i + nums[i])
        if i == end:
            steps += 1
            end = farthest
    return steps""",
    "java": """public int jump(int[] nums) {
    int steps = 0, end = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        if (i == end) { steps++; end = farthest; }
    }
    return steps;
}""",
    "time": "O(n) — 一次遍历",
    "space": "O(1)",
    "pitfalls": [["循环到 n-2 即可", "最后一个位置不需要再起跳，遍历到 n-1 可能多算一步"], ["i == end 才加步数", "走到当前覆盖边界才确认必须再跳一次，提前加会算多"]],
    "selfcheck": [["为什么这是最优步数？", "每步的边界 end 都是「这一步能覆盖的最远范围」，在边界处切换 = 用最少步数换最大覆盖，贪心即最优。"], ["nums=[0] 呢？", "n=1，循环不执行，返回 0，已经在终点。"]],
}

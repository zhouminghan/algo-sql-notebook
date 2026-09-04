from scripts.algo_gen import frame

PROBLEM = {
    "id": 40,
    "title": "子集",
    "diff": "medium",
    "tags": ["回溯"],
    "leetcode": 78,
    "origin": "https://leetcode.cn/problems/subsets/",
    "why": "每个元素有「选 / 不选」两种选择，子集共有 2^n 个。回溯按「从当前下标往后选」遍历，每进入一层就先把当前组合记下，就能无遗漏地收集所有子集。",
    "desc": """<p>给定一个<strong>不含重复元素</strong>的整数数组 <code>nums</code>，返回该数组所有可能的子集（幂集）。</p>
<p><strong>示例：</strong><br><code>nums=[1,2,3]</code> → <code>[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]</code></p>""",
    "frames": [
    frame("① 每个元素「选 / 不选」的决策树", "drawBacktrack", nodes=[{"val": "[]", "x": 300, "y": 15, "color": "normal"}, {"val": "[1]", "x": 140, "y": 85, "color": "path"}, {"val": "[]", "x": 460, "y": 85, "color": "path"}, {"val": "[1,2]", "x": 60, "y": 160, "color": "path"}, {"val": "[1]", "x": 220, "y": 160, "color": "path"}, {"val": "[1,2,3]", "x": 60, "y": 240, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 140, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 460, "y2": 85, "color": "path"}, {"x1": 140, "y1": 85, "x2": 60, "y2": 160, "color": "path"}, {"x1": 140, "y1": 85, "x2": 220, "y2": 160, "color": "path"}, {"x1": 60, "y1": 160, "x2": 60, "y2": 240, "color": "path"}], width=560, height=280),
    frame("② 每进入一层，当前 path 就是一个子集，立即收集", "drawTable", headers=["层级", "path", "是否收集"], rows=[["0", "[]", "✓"], ["1", "[1]", "✓"], ["2", "[1,2]", "✓"], ["3", "[1,2,3]", "✓"]], width=460, height=190),
    ],
    "conclusion": "「进入即收集」保证从空集到全集每个中间状态都不漏。",
    "py": """def subsets(nums):
    ans = []
    def dfs(start, path):
        ans.append(path[:])        # 每个状态都是子集
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1, path)       # 不重复：只往后选
            path.pop()
    dfs(0, [])
    return ans""",
    "java": """public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> ans = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), ans);
    return ans;
}
void dfs(int[] nums, int start, List<Integer> path, List<List<Integer>> ans) {
    ans.add(new ArrayList<>(path));
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);
        dfs(nums, i + 1, path, ans);
        path.remove(path.size() - 1);
    }
}""",
    "time": "O(n · 2^n) — 2^n 个子集，每个复制一次",
    "space": "O(n) — 递归栈",
    "pitfalls": [["进入就收集", "不要等到叶子才收集，否则会漏掉中间态（如 [1]、[1,2]）"], ["start 下标去重", "从 start 往后选保证子集内部有序，避免 [1,2] 与 [2,1] 重复"]],
    "selfcheck": [["位运算怎么做这题？", "0 到 2^n-1 每个数对应一个子集，第 k 位为 1 表示选 nums[k]，时间 O(n·2^n)。"], ["nums 有重复元素呢？", "先排序，循环里跳过「同级重复」元素，避免生成重复子集。"]],
}

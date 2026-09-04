from scripts.algo_gen import frame

PROBLEM = {
    "id": 26,
    "title": "全排列",
    "diff": "medium",
    "tags": ["回溯"],
    "leetcode": 46,
    "origin": "https://leetcode.cn/problems/permutations/",
    "why": "全排列是「每个位置选一个没用过的数」的决策树。回溯用 used 标记已选，选完 n 个就收集，再撤销选择换下一个，穷举所有顺序。",
    "desc": """<p>给定一个<strong>不含重复数字</strong>的数组 <code>nums</code>，返回其所有可能的全排列，可以按任意顺序返回。</p>
<p><strong>示例：</strong><br><code>nums=[1,2,3]</code> → <code>[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]</code></p>""",
    "frames": [
    frame("① 决策树：每层固定一个位置，选一个未用过的数", "drawBacktrack", nodes=[{"val": "[]", "x": 300, "y": 15, "color": "normal"}, {"val": "[1]", "x": 90, "y": 85, "color": "path"}, {"val": "[2]", "x": 300, "y": 85, "color": "path"}, {"val": "[3]", "x": 510, "y": 85, "color": "path"}, {"val": "[1,2]", "x": 40, "y": 160, "color": "path"}, {"val": "[1,3]", "x": 140, "y": 160, "color": "path"}, {"val": "[1,2,3]", "x": 40, "y": 240, "color": "path"}, {"val": "[1,3,2]", "x": 140, "y": 240, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 90, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 300, "y2": 85, "color": "path"}, {"x1": 300, "y1": 15, "x2": 510, "y2": 85, "color": "path"}, {"x1": 90, "y1": 85, "x2": 40, "y2": 160, "color": "path"}, {"x1": 90, "y1": 85, "x2": 140, "y2": 160, "color": "path"}, {"x1": 40, "y1": 160, "x2": 40, "y2": 240, "color": "path"}, {"x1": 140, "y1": 160, "x2": 140, "y2": 240, "color": "path"}], width=580, height=280),
    frame("② 用 used 数组标记，避免同一个数重复选", "drawTable", headers=["数字", "1", "2", "3"], rows=[["used", "false", "false", "false"], ["选 1 后", {"val": "true", "highlight": True}, "false", "false"]], width=520, height=140),
    ],
    "conclusion": "每层从「未使用」的数里挑一个放进去，到底就收集并回溯，换下一个候选。",
    "py": """def permute(nums):
    ans = []
    n = len(nums)
    used = [False] * n
    def dfs(path):
        if len(path) == n:
            ans.append(path[:]); return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs(path)
            path.pop()
            used[i] = False
    dfs([])
    return ans""",
    "java": """public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> ans = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    dfs(nums, used, new ArrayList<>(), ans);
    return ans;
}
void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> ans) {
    if (path.size() == nums.length) { ans.add(new ArrayList<>(path)); return; }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true; path.add(nums[i]);
        dfs(nums, used, path, ans);
        path.remove(path.size() - 1); used[i] = false;
    }
}""",
    "time": "O(n · n!) — n! 个排列，每个复制一次",
    "space": "O(n) — 递归栈 + used 数组",
    "pitfalls": [["回溯要同时撤销 used 和 path", "两者都要还原，否则同一分支残留会漏排列或产生重复"], ["收集时要 path[:] 拷贝", "path 是可变对象且后续会被修改，不拷贝会导致 ans 里全是同一个引用"]],
    "selfcheck": [["nums 有重复数字怎么办？", "这是「全排列 II」，需先排序再在循环里跳过「同级重复」（nums[i]==nums[i-1] 且 used[i-1] 为 false），否则会产生重复排列。"], ["为什么交换法也能做？", "固定第一个位置与后面逐个交换，再递归处理剩余部分；两种写法都基于「每个位置放一个数」的思想。"]],
}

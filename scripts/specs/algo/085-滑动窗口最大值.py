from scripts.algo_gen import frame

PROBLEM = {
    "id": 85,
    "title": "滑动窗口最大值",
    "diff": "hard",
    "tags": ["单调队列"],
    "leetcode": 239,
    "origin": "https://leetcode.cn/problems/sliding-window-maximum/",
    "why": "用「单调递减队列」存窗口内的候选最大值下标：队首是当前窗口最大。新元素入队前，把队尾所有更小的弹出（它们永无出头之日）；队首滑出窗口就移除。O(n)。",
    "desc": """<p>给定整数数组 <code>nums</code>，滑动窗口大小为 <code>k</code>，窗口从最左侧滑动到最右侧，每次只移动一位。返回每个窗口的最大值。</p>
<p><strong>示例：</strong><br><code>[1,3,-1,-3,5,3,6,7], k=3</code> → <code>[3,3,5,5,6,7]</code></p>""",
    "frames": [
    frame("① 窗口 [1,3,-1] 最大 3", "drawTwoPointers", arr=[1, 3, -1, -3, 5, 3, 6, 7], left=0, right=2, window={"start": 0, "end": 2}, width=700, height=150),
    frame("② 单调递减队列：队首恒为窗口最大", "drawStack", items=[{"val": "3"}, {"val": "-1"}], type="queue", height=140),
    frame("③ 每滑一格输出队首，结果 [3,3,5,5,6,7]", "drawTable", headers=["窗口", "0-2", "1-3", "2-4", "3-5", "4-6", "5-7"], rows=[["最大值", "3", "3", "5", "5", "6", "7"]], width=620, height=120),
    ],
    "conclusion": "单调队列让「窗口最大值」始终在队首，滑入滑出都 O(1)，整体 O(n)。",
    "py": """from collections import deque
def maxSlidingWindow(nums, k):
    q = deque()      # 存下标，队首对应最大值
    ans = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()               # 弹掉更小的
        q.append(i)
        if q[0] < i - k + 1:      # 队首滑出窗口
            q.popleft()
        if i >= k - 1:
            ans.append(nums[q[0]])
    return ans""",
    "java": """public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] ans = new int[n - k + 1];
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!q.isEmpty() && nums[q.peekLast()] <= nums[i]) q.pollLast();
        q.offerLast(i);
        if (q.peekFirst() < i - k + 1) q.pollFirst();
        if (i >= k - 1) ans[i - k + 1] = nums[q.peekFirst()];
    }
    return ans;
}""",
    "time": "O(n) — 每个元素入队出队一次",
    "space": "O(k) — 队列",
    "pitfalls": [["弹队尾更小元素", "用 <= 保证严格递减，新元素下标更大、更「长寿」，旧小值无用"], ["队首过期移除", "判断 q[0] < i-k+1 时把滑出窗口的下标从队首移除"]],
    "selfcheck": [["为什么存下标而非值？", "需要判断「队首是否还在窗口内」，只有下标能算出来。"], ["暴力做法复杂度？", "每个窗口扫一遍是 O(nk)，单调队列优化到 O(n)。"]],
}

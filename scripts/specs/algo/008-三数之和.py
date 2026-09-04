from scripts.algo_gen import frame

PROBLEM = {
    "id": 8,
    "title": "三数之和",
    "diff": "medium",
    "tags": ["双指针", "排序"],
    "leetcode": 15,
    "origin": "https://leetcode.cn/problems/3sum/",
    "why": "固定一个数，剩下的两个数用双指针在有序数组里夹逼，把 O(n³) 降到 O(n²)。排序 + 去重（跳过相同值）避免重复三元组。",
    "desc": "<p>给定整数数组，找出所有和为 0 且<strong>不重复</strong>的三元组 <code>[nums[i], nums[j], nums[k]]</code>。</p><p><strong>示例：</strong><br><code>[-1,0,1,2,-1,-4]</code> → <code>[[-1,-1,2],[-1,0,1]]</code></p>",
    "frames": [
    frame("① 排序后固定第一个数 -1", "drawTwoPointers", arr=[-4, -1, -1, 0, 1, 2], left=1, right=5, height=130),
    frame("② 双指针夹逼，和为 0 收集", "drawTwoPointers", arr=[-4, -1, -1, 0, 1, 2], left=1, right=5, height=130),
    frame("③ 跳过重复值去重", "drawTwoPointers", arr=[-4, -1, -1, 0, 1, 2], left=2, right=5, height=130),
    ],
    "conclusion": "排序 → 固定一个 → 双指针找两数和，去重全靠跳过相同值。",
    "py": """def threeSum(nums):
    nums.sort()
    n = len(nums)
    ans = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0: l += 1
            elif s > 0: r -= 1
            else:
                ans.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l+1]: l += 1
                while l < r and nums[r] == nums[r-1]: r -= 1
                l += 1; r -= 1
    return ans""",
    "java": """public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> ans = new ArrayList<>();
    int n = nums.length;
    for (int i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue;
        int l = i + 1, r = n - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (s < 0) l++;
            else if (s > 0) r--;
            else {
                ans.add(Arrays.asList(nums[i], nums[l], nums[r]));
                while (l < r && nums[l] == nums[l+1]) l++;
                while (l < r && nums[r] == nums[r-1]) r--;
                l++; r--;
            }
        }
    }
    return ans;
}""",
    "time": "O(n²)",
    "space": "O(1)（不算结果）",
    "pitfalls": [["三处去重", "外层固定值、内层左右指针都要跳过重复，缺一处就出重复三元组"], ["先排序", "双指针夹逼的前提是数组有序"]],
    "selfcheck": [["[-1,0,1,2,-1,-4] 的两个答案？", "[-1,-1,2] 和 [-1,0,1]。"], ["为什么 O(n²) 不是 O(n³)？", "固定一数 O(n)，双指针 O(n)，相乘 O(n²)。"]],
}

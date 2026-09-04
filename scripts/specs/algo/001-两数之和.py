from scripts.algo_gen import frame

PROBLEM = {
    "id": 1,
    "title": "两数之和",
    "diff": "easy",
    "tags": ["数组", "哈希表"],
    "leetcode": 1,
    "origin": "https://leetcode.cn/problems/two-sum/",
    "why": "暴力双循环是 O(n²)。用哈希表一边遍历一边查「补数」，把查找从 O(n) 降到 O(1)，一次遍历 O(n) 就能出结果。",
    "desc": "<p>给定一个整数数组 <code>nums</code> 和一个整数目标值 <code>target</code>，请你在该数组中找出<strong>和为目标值</strong>的那 <strong>两个</strong>整数，并返回它们的数组下标。假设每种输入只对应一个答案，且不能使用两次相同元素。</p><p><strong>示例：</strong><br><code>nums=[2,7,11,15], target=9</code> → <code>[0,1]</code></p>",
    "frames": [
    frame("① i=0，nums[0]=2，补数 7 不在表 → 存入 2→0", "drawTwoSumMap", arr=[2, 7, 11, 15], map=[{"key": "2", "val": "0", "new": True}], currentIdx=0, complement=7, action="7 不在表中 → 存入 (2 → 0)", width=420),
    frame("② i=1，nums[1]=7，补数 2 命中！", "drawTwoSumMap", arr=[2, 7, 11, 15], map=[{"key": "2", "val": "0"}], currentIdx=1, complement=2, highlight="2", action="2 命中！→ 返回 [0,1]", width=420),
    frame("③ 一次遍历，边查边存", "drawTwoSumMap", arr=[2, 7, 11, 15], map=[{"key": "2", "val": "0"}, {"key": "7", "val": "1"}], currentIdx=2, complement=-2, action="先查 complement 再存，避免同一元素被用两次", width=420),
    ],
    "conclusion": "先查补数、再存当前值，一次遍历即可命中。",
    "py": """def twoSum(nums, target):
    seen = {}  # val -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
    "java": """public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int c = target - nums[i];
        if (map.containsKey(c)) return new int[]{map.get(c), i};
        map.put(nums[i], i);
    }
    return new int[]{};
}""",
    "time": "O(n) — 一次遍历",
    "space": "O(n) — 哈希表",
    "pitfalls": [["先查后存", "先存再查可能把同一个元素用两次（如 target=6, nums=[3,2,4] 会错误返回 [0,0]）"], ["哈希冲突", "Java HashMap 链表过长会转红黑树，但两数之和场景不会触发"]],
    "selfcheck": [["nums 有重复元素如 [3,3] 还正确吗？", "正确。i=0 时表空查不到 3，存 (3,0)；i=1 时查 complement=3 命中，返回 [0,1]。"], ["要返回所有不重复配对怎么办？", "排序 + 双指针，或用 Set 去重配对结果。"]],
}

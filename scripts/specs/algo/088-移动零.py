from scripts.algo_gen import frame

PROBLEM = {
    "id": 88,
    "title": "移动零",
    "diff": "easy",
    "tags": ["双指针"],
    "leetcode": 283,
    "origin": "https://leetcode.cn/problems/move-zeroes/",
    "why": "快慢双指针：slow 指向「下一个非零该放的位置」，fast 扫描数组。遇非零就交换到 slow 并前进，最后 slow 之后全是 0。原地 O(n)。",
    "desc": """<p>给定整数数组，将所有 <code>0</code> 移动到数组末尾，同时保持非零元素的相对顺序。必须原地操作。</p>
<p><strong>示例：</strong><br><code>[0,1,0,3,12]</code> → <code>[1,3,12,0,0]</code></p>""",
    "frames": [
    frame("① slow 指向下一个非零位置，fast 扫描", "drawTwoPointers", arr=[0, 1, 0, 3, 12], left=0, right=1, width=520, height=140),
    frame("② 遇非零交换到 slow，slow 前进", "drawTwoPointers", arr=[1, 0, 0, 3, 12], left=1, right=2, width=520, height=140),
    frame("③ 结果 [1,3,12,0,0]", "drawTable", headers=["下标", "0", "1", "2", "3", "4"], rows=[["结果", "1", "3", "12", "0", "0"]], width=520, height=110),
    ],
    "conclusion": "非零元素依次「压实」到前面，剩余位置补 0。",
    "py": """def moveZeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1""",
    "java": """public void moveZeroes(int[] nums) {
    int slow = 0;
    for (int fast = 0; fast < nums.length; fast++)
        if (nums[fast] != 0) { int t = nums[slow]; nums[slow] = nums[fast]; nums[fast] = t; slow++; }
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["保持相对顺序", "用交换而非「先删后补」，顺序自然保持"], ["slow 含义", "slow 是下一个非零该放的位置，也是当前非零区间的长度"]],
    "selfcheck": [["全 0 数组？", "fast 全程不触发交换，slow=0，数组不变。"], ["能否先统计 0 个数再整体移动？", "可以，但双指针交换更直观且一步到位。"]],
}

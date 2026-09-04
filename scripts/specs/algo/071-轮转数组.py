from scripts.algo_gen import frame

PROBLEM = {
    "id": 71,
    "title": "轮转数组",
    "diff": "medium",
    "tags": ["数组"],
    "leetcode": 189,
    "origin": "https://leetcode.cn/problems/rotate-array/",
    "why": "把数组向右轮转 k 位，等价于「整体反转 → 前 k 个反转 → 后 n-k 个反转」三步，原地 O(1) 空间。k 要先对 n 取模。",
    "desc": """<p>给定整数数组，将数组中的元素向右轮转 <code>k</code> 个位置。</p>
<p><strong>示例：</strong><br><code>nums=[1,2,3,4,5,6,7], k=3</code> → <code>[5,6,7,1,2,3,4]</code></p>""",
    "frames": [
    frame("① 整体反转 [7,6,5,4,3,2,1]", "drawTable", headers=["下标", "0", "1", "2", "3", "4", "5", "6"], rows=[["原数组", "1", "2", "3", "4", "5", "6", "7"], ["整体反转", "7", "6", "5", "4", "3", "2", "1"]], width=620, height=140),
    frame("② 前 k=3 个反转 → [5,6,7,...]", "drawTable", headers=["下标", "0", "1", "2", "3", "4", "5", "6"], rows=[["结果", "5", "6", "7", "4", "3", "2", "1"]], width=620, height=110),
    frame("③ 后 n-k 个反转 → [5,6,7,1,2,3,4]", "drawTable", headers=["下标", "0", "1", "2", "3", "4", "5", "6"], rows=[["最终", "5", "6", "7", "1", "2", "3", "4"]], width=620, height=110),
    ],
    "conclusion": "三次反转组合出「循环右移」效果，且完全原地。",
    "py": """def rotate(nums, k):
    n = len(nums)
    k %= n
    def rev(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1
    rev(0, n - 1)        # 整体
    rev(0, k - 1)        # 前 k
    rev(k, n - 1)        # 后 n-k""",
    "java": """public void rotate(int[] nums, int k) {
    int n = nums.length; k %= n;
    rev(nums, 0, n - 1);
    rev(nums, 0, k - 1);
    rev(nums, k, n - 1);
}
void rev(int[] a, int l, int r) {
    while (l < r) { int t = a[l]; a[l] = a[r]; a[r] = t; l++; r--; }
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["k 取模", "k 可能大于 n，先 k %= n，否则反转区间越界"], ["三步顺序", "先整体、再前 k、再后 n-k，顺序不能乱"]],
    "selfcheck": [["k=0 或 k=n？", "k%=n 后为 0，三次反转互相抵消，数组不变。"], ["左轮转怎么做？", "同理先整体反转，再反转「前 n-k」和「后 k」即可。"]],
}

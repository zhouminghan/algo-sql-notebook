from scripts.algo_gen import frame

PROBLEM = {
    "id": 4,
    "title": "寻找两个正序数组的中位数",
    "diff": "hard",
    "tags": ["二分查找", "数组"],
    "leetcode": 4,
    "origin": "https://leetcode.cn/problems/median-of-two-sorted-arrays/",
    "why": "不合并数组，直接在较短的数组上二分一个「切分点」i，另一个切分点 j 由 i 推出；左半所有元素 ≤ 右半所有元素即找到中位数。O(log(min(m,n)))。",
    "desc": "<p>给定两个大小分别为 m 和 n 的正序数组 <code>nums1</code> 和 <code>nums2</code>，返回这两个数组的<strong>中位数</strong>。要求 O(log(m+n))。</p><p><strong>示例：</strong><br><code>nums1=[1,3], nums2=[2]</code> → <code>2.0</code>；<code>[1,2],[3,4]</code> → <code>2.5</code></p>",
    "frames": [
    frame("① 在较短数组上二分切分点 i", "drawBinarySearch", arr=[1, 3, 2], left=0, mid=1, right=2, height=120),
    frame("② 左半 [1] 与右半 [3,2] 比较边界", "drawTable", headers=["nums1", "", "nums2", ""], rows=[["1", "3", "2", ""], ["i=1", "", "j=1", ""]], height=90),
    frame("③ 奇偶分情况取中位数", "drawTable", headers=["情况", "中位数"], rows=[["奇数", "max(左半)"], ["偶数", "(max(左)+min(右))/2"]], height=100),
    ],
    "conclusion": "二分切分点，保证左半最大值 ≤ 右半最小值，按奇偶取中位数。",
    "py": """def findMedianSortedArrays(a, b):
    if len(a) > len(b): a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        l1 = a[i-1] if i > 0 else float('-inf')
        r1 = a[i] if i < m else float('inf')
        l2 = b[j-1] if j > 0 else float('-inf')
        r2 = b[j] if j < n else float('inf')
        if l1 <= r2 and l2 <= r1:
            if (m + n) % 2:
                return max(l1, l2)
            return (max(l1, l2) + min(r1, r2)) / 2
        if l1 > r2: hi = i - 1
        else: lo = i + 1
    return 0.0""",
    "java": """public double findMedianSortedArrays(int[] a, int[] b) {
    if (a.length > b.length) { int[] t = a; a = b; b = t; }
    int m = a.length, n = b.length, half = (m + n + 1) / 2;
    int lo = 0, hi = m;
    while (lo <= hi) {
        int i = (lo + hi) >>> 1, j = half - i;
        double l1 = i > 0 ? a[i-1] : Integer.MIN_VALUE;
        double r1 = i < m ? a[i] : Integer.MAX_VALUE;
        double l2 = j > 0 ? b[j-1] : Integer.MIN_VALUE;
        double r2 = j < n ? b[j] : Integer.MAX_VALUE;
        if (l1 <= r2 && l2 <= r1)
            return (m + n) % 2 == 1 ? Math.max(l1, l2) : (Math.max(l1, l2) + Math.min(r1, r2)) / 2.0;
        if (l1 > r2) hi = i - 1; else lo = i + 1;
    }
    return 0.0;
}""",
    "time": "O(log(min(m,n)))",
    "space": "O(1)",
    "pitfalls": [["在较短数组上二分", "保证 j=half-i 非负"], ["边界用 ±inf", "i=0 或 i=m 时左/右半为空，用无穷代替避免特判"]],
    "selfcheck": [["nums1=[1,2], nums2=[3,4]？", "i=1,j=1，左半 {1,3} 右半 {2,4}，偶数取 (3+2)/2=2.5。"], ["为什么不用合并？", "合并是 O(m+n)，二分切分是 O(log min)，且不产生额外数组。"]],
}

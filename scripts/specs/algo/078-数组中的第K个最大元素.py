from scripts.algo_gen import frame

PROBLEM = {
    "id": 78,
    "title": "数组中的第K个最大元素",
    "diff": "medium",
    "tags": ["堆"],
    "leetcode": 215,
    "origin": "https://leetcode.cn/problems/kth-largest-element-in-an-array/",
    "why": "维护一个大小为 k 的最小堆，遍历数组：堆不满就进，满了且当前值大于堆顶则替换。堆顶就是第 k 大。时间 O(n log k)，比全排序 O(n log n) 更优。",
    "desc": """<p>给定整数数组和整数 <code>k</code>，返回数组中第 <code>k</code> 个<strong>最大</strong>元素（排序后倒数第 k 个，而非第 k 个不同元素）。</p>
<p><strong>示例：</strong><br><code>[3,2,1,5,6,4], k=2</code> → <code>5</code></p>""",
    "frames": [
    frame("① 维护大小为 k=2 的最小堆", "drawStack", items=[{"val": "3"}, {"val": "2"}], type="stack", height=140),
    frame("② 遍历：比堆顶大就替换，堆顶始终是「当前前 k 大里最小的」", "drawTable", headers=["元素", "堆（前2大）", "堆顶"], rows=[["1", "3,2", "2"], ["5", "5,3", "3"], ["6", "6,5", "5"], ["4", "6,5", "5"]], width=460, height=190),
    frame("③ 堆顶 5 即第 2 大", "drawTable", headers=["", "值"], rows=[["第 2 大", {"val": "5", "highlight": True}]], width=420, height=110),
    ],
    "conclusion": "小顶堆的堆顶是「前 k 大元素的最小者」，即第 k 大。",
    "py": """import heapq
def findKthLargest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]""",
    "java": """public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    for (int x : nums) {
        pq.offer(x);
        if (pq.size() > k) pq.poll();
    }
    return pq.peek();
}""",
    "time": "O(n log k)",
    "space": "O(k)",
    "pitfalls": [["最小堆维护第 k 大", "堆顶是「最小的那个大值」，别用最大堆（那要找第 k 小）"], ["k 大小", "堆满 k 后每次 push 都要 pop 一个，保持规模 k"]],
    "selfcheck": [["快速选择做法？", "基于快排 partition，平均 O(n)，最坏 O(n²)，适合大数据量。"], ["第 k 大与第 k 小？", "第 k 大 = 第 (n-k+1) 小；求第 k 小则用最大堆。"]],
}

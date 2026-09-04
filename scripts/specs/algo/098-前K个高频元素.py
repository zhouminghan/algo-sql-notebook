from scripts.algo_gen import frame

PROBLEM = {
    "id": 98,
    "title": "前K个高频元素",
    "diff": "medium",
    "tags": ["堆"],
    "leetcode": 347,
    "origin": "https://leetcode.cn/problems/top-k-frequent-elements/",
    "why": "先统计频率，再用大小为 k 的最小堆维护「频率最高的 k 个」：堆满且新频率更高就替换。最后堆里就是答案，时间 O(n log k)。",
    "desc": """<p>给定整数数组和整数 <code>k</code>，返回出现频率<strong>前 k 高</strong>的元素。</p>
<p><strong>示例：</strong><br><code>[1,1,1,2,2,3], k=2</code> → <code>[1,2]</code></p>""",
    "frames": [
    frame("① 统计频率", "drawTable", headers=["元素", "1", "2", "3"], rows=[["频率", "3", "2", "1"]], width=420, height=110),
    frame("② 维护大小为 k 的最小堆（按频率）", "drawTable", headers=["元素", "频率", "是否在堆"], rows=[["1", "3", "✓"], ["2", "2", "✓"], ["3", "1", "被淘汰"]], width=460, height=150),
    frame("③ 堆中即前 k 高 [1,2]", "drawTable", headers=["", "元素"], rows=[["前 2 高", "1, 2"]], width=420, height=110),
    ],
    "conclusion": "最小堆按频率排序，堆顶是「前 k 高里最低的」，低于它的直接淘汰。",
    "py": """import heapq
from collections import Counter
def topKFrequent(nums, k):
    freq = Counter(nums)
    heap = []
    for num, cnt in freq.items():
        heapq.heappush(heap, (cnt, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for cnt, num in heap]""",
    "java": """public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    PriorityQueue<Integer> pq = new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
    for (int x : freq.keySet()) {
        pq.offer(x);
        if (pq.size() > k) pq.poll();
    }
    int[] ans = new int[k];
    for (int i = 0; i < k; i++) ans[i] = pq.poll();
    return ans;
}""",
    "time": "O(n log k)",
    "space": "O(n)",
    "pitfalls": [["堆按频率比较", "堆元素是 (cnt, num) 或自定义比较器，别按元素值比较"], ["堆满即弹最小", "维护 k 个最高频，弹掉堆顶（频率最低者）"]],
    "selfcheck": [["桶排序做法？", "按频率分桶（下标=频率），从高到低收集，O(n)，适合频率范围小的情况。"], ["频率相同怎么排序？", "顺序无所谓，题目不要求同频元素的具体次序。"]],
}

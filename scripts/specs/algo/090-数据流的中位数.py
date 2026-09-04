from scripts.algo_gen import frame

PROBLEM = {
    "id": 90,
    "title": "数据流的中位数",
    "diff": "hard",
    "tags": ["堆"],
    "leetcode": 295,
    "origin": "https://leetcode.cn/problems/find-median-from-data-stream/",
    "why": "用两个堆：大顶堆放较小的一半，小顶堆放较大的一半。保持两者大小差 ≤1，中位数要么是大顶堆堆顶、要么是两堆顶均值。插入 O(log n)。",
    "desc": """<p>实现 MedianFinder，动态插入整数并随时返回当前所有数字的中位数。</p>
<p><strong>示例：</strong><br>依次加入 <code>1,2,3</code>，中位数分别为 <code>1, 1.5, 2</code></p>""",
    "frames": [
    frame("① 大顶堆存较小一半，小顶堆存较大一半", "drawTable", headers=["堆", "较小一半(大顶)", "较大一半(小顶)"], rows=[["加入 1,2,3 后", "2,1", "3"]], width=500, height=130),
    frame("② 平衡：两堆大小差 ≤1", "drawTable", headers=["操作", "大顶堆", "小顶堆"], rows=[["加 1", "1", ""], ["加 2", "1", "2"], ["加 3", "1", "2,3 → 平衡"]], width=500, height=160),
    frame("③ 中位数 = 堆顶 或 两堆顶均值", "drawTable", headers=["总数", "中位数"], rows=[["奇数", "大顶堆堆顶"], ["偶数", "(两堆顶)/2"]], width=460, height=130),
    ],
    "conclusion": "两个堆把数据切成两半，中位数永远在堆顶附近。",
    "py": """import heapq
class MedianFinder:
    def __init__(self):
        self.small = []   # 大顶堆（存负值）
        self.large = []   # 小顶堆
    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2""",
    "java": """class MedianFinder {
    PriorityQueue<Integer> small = new PriorityQueue<>((a, b) -> b - a);
    PriorityQueue<Integer> large = new PriorityQueue<>();
    public void addNum(int num) {
        small.offer(num);
        large.offer(small.poll());
        if (large.size() > small.size()) small.offer(large.poll());
    }
    public double findMedian() {
        if (small.size() > large.size()) return small.peek();
        return (small.peek() + large.peek()) / 2.0;
    }
}""",
    "time": "addNum O(log n)，findMedian O(1)",
    "space": "O(n)",
    "pitfalls": [["Python 大顶堆用负值", "heapq 只有小顶堆，存 -num 模拟大顶堆"], ["平衡方向", "插入后让 large 不超过 small，保证 small 要么等大要么多一个"]],
    "selfcheck": [["偶数个中位数？", "两堆等大时取两堆顶平均值。"], ["奇数个中位数？", "small 多一个，中位数就是 small 堆顶（较小一半的最大值）。"]],
}

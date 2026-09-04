from scripts.algo_gen import frame

PROBLEM = {
    "id": 64,
    "title": "LRU缓存",
    "diff": "medium",
    "tags": ["哈希表", "链表"],
    "leetcode": 146,
    "origin": "https://leetcode.cn/problems/lru-cache/",
    "why": "LRU 需要「O(1) 查找 + O(1) 移动最近使用」。Python 用 OrderedDict（move_to_end + popitem），Java 用 LinkedHashMap（accessOrder），哈希 + 双向链表天生支持。",
    "desc": """<p>设计并实现满足 LRU（最近最少使用）缓存约束的数据结构：实现 <code>get(key)</code> 和 <code>put(key, value)</code>，get/put 均 O(1)。当缓存容量达到上限时，删除<strong>最久未使用</strong>的关键字。</p>
<p><strong>示例：</strong><br>容量 2：<code>put(1,1), put(2,2), get(1)→1, put(3,3), get(2)→-1</code></p>""",
    "frames": [
    frame("① 容量 2：put(1,1), put(2,2)，顺序 [1,2]", "drawTable", headers=["key", "1", "2"], rows=[["value", "1", "2"], ["序", "旧", "新"]], width=420, height=130),
    frame("② get(1) 命中，把 1 移到最新 → [2,1]", "drawTable", headers=["key", "2", "1"], rows=[["value", "2", "1"], ["序", "旧", "新"]], width=420, height=130),
    frame("③ put(3,3) 满容量，淘汰最旧 2 → [1,3]", "drawTable", headers=["key", "1", "3"], rows=[["value", "1", "3"], ["序", "旧", "新"]], width=420, height=130),
    ],
    "conclusion": "访问即「移到最新」，淘汰即「删最旧」，OrderedDict/LinkedHashMap 一行搞定。",
    "py": """from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.d = OrderedDict()
    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)      # 移到最新
        return self.d[key]
    def put(self, key, value):
        if key in self.d:
            self.d.move_to_end(key)
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False)  # 删最旧""",
    "java": """class LRUCache extends LinkedHashMap<Integer, Integer> {
    private final int cap;
    public LRUCache(int capacity) { super(capacity, 0.75f, true); this.cap = capacity; }
    public int get(int key) { return super.getOrDefault(key, -1); }
    public void put(int key, int value) { super.put(key, value); }
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > cap;
    }
}""",
    "time": "get/put 均 O(1)",
    "space": "O(capacity)",
    "pitfalls": [["get 命中要 move_to_end", "否则不会刷新「最近使用」顺序，淘汰会删错"], ["淘汰最旧用 popitem(last=False)", "last=False 表示删队首（最久未使用）"]],
    "selfcheck": [["put 已存在的 key？", "更新值并移到最新，不增加数量。"], ["Java 手写版？", "用 HashMap + 双向链表：map 存节点引用，链表头尾维护顺序，get 时摘节点插到头。"]],
}

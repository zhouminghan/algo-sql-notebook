from scripts.algo_gen import frame

PROBLEM = {
    "id": 59,
    "title": "随机链表的复制",
    "diff": "medium",
    "tags": ["链表"],
    "leetcode": 138,
    "origin": "https://leetcode.cn/problems/copy-list-with-random-pointer/",
    "why": "链表节点多了 random 指针，直接拷贝会搞不清「新节点指向谁」。用哈希表建立「旧节点 → 新节点」映射，两遍遍历分别接 next 和 random。",
    "desc": """<p>给定一个链表，每个节点包含一个额外随机指针 <code>random</code>，可指向链表中任意节点或 null。构造这个链表的<strong>深拷贝</strong>。</p>
<p><strong>示例：</strong><br><code>[[7,null],[13,0],[11,4],[10,2],[1,0]]</code> → 对应深拷贝</p>""",
    "frames": [
    frame("① 第一遍：为每个旧节点创建新节点，建立映射", "drawTable", headers=["旧节点", "7", "13", "11", "10", "1"], rows=[["新节点", "7'", "13'", "11'", "10'", "1'"]], width=520, height=110),
    frame("② 第二遍：按映射接 next 与 random", "drawLinkedList", nodes=[{"val": "7", "highlight": "active"}, {"val": "13"}, {"val": "11"}, {"val": "10"}, {"val": "1"}], width=560, height=90),
    ],
    "conclusion": "哈希映射让「旧指针」能翻译成「新指针」，拷贝 next 和 random 都不丢。",
    "py": """def copyRandomList(head):
    if not head:
        return None
    mp = {}
    cur = head
    while cur:                     # 第一遍建节点
        mp[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                     # 第二遍接指针
        mp[cur].next = mp.get(cur.next)
        mp[cur].random = mp.get(cur.random)
        cur = cur.next
    return mp[head]""",
    "java": """public Node copyRandomList(Node head) {
    if (head == null) return null;
    Map<Node, Node> mp = new HashMap<>();
    for (Node cur = head; cur != null; cur = cur.next) mp.put(cur, new Node(cur.val));
    for (Node cur = head; cur != null; cur = cur.next) {
        mp.get(cur).next = mp.get(cur.next);
        mp.get(cur).random = mp.get(cur.random);
    }
    return mp.get(head);
}""",
    "time": "O(n) — 两遍遍历",
    "space": "O(n) — 哈希表",
    "pitfalls": [["两遍分开", "第一遍只建节点不接指针，第二遍再 next/random，避免引用尚未创建的节点"], ["random 可为 null", "mp.get(None) 返回 None，正好对应 null"]],
    "selfcheck": [["O(1) 空间做法？", "把新节点插在旧节点后面（交错），再用「旧.random.next」取新 random，最后拆链，可省哈希表。"], ["为什么不能只复制 next？", "random 可能指向任意节点，不建立映射就无法在新链表里找到对应节点。"]],
}

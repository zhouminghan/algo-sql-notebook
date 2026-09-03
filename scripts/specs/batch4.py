from scripts.algo_gen import frame


PROBLEMS = [
    # ---------------------------------------------------------------- 56
    {
        "id": 56,
        "title": "最长连续序列",
        "diff": "medium",
        "tags": ["哈希表"],
        "leetcode": 128,
        "origin": "https://leetcode.cn/problems/longest-consecutive-sequence/",
        "why": "要求 O(n)。把数组放进集合，只从「序列起点」（num-1 不在集合里）开始向后数连续长度，每个元素最多被访问两次，避免排序的 O(n log n)。",
        "desc": """<p>给定一个未排序的整数数组，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。要求时间复杂度 O(n)。</p>
<p><strong>示例：</strong><br><code>[100,4,200,1,3,2]</code> → <code>4</code>（最长连续序列是 <code>[1,2,3,4]</code>）</p>""",
        "frames": [
            frame("① 放入集合，快速判断某个数是否存在", "drawTable",
                  headers=["集合", "1", "2", "3", "4", "100", "200"],
                  rows=[["存在", "✓", "✓", "✓", "✓", "✓", "✓"]], width=560, height=110),
            frame("② 只有「起点」（前一个数不在集合）才开始计数", "drawTable",
                  headers=["数", "num-1 在?", "是起点?", "连续长度"],
                  rows=[["1", "✗", "✓", "4"], ["4", "✓(3在)", "✗", "-"], ["100", "✗", "✓", "1"], ["200", "✗", "✓", "1"]], width=560, height=190),
            frame("③ 最长连续序列 [1,2,3,4]，长度 4", "drawTable",
                  headers=["连续序列", "1", "2", "3", "4"],
                  rows=[["是否在集合", "✓", "✓", "✓", "✓"]], width=560, height=120),
        ],
        "conclusion": "只从每个连续段的起点开始向后数，保证总工作量 O(n)。",
        "py": """def longestConsecutive(nums):
    s = set(nums)
    ans = 0
    for x in s:
        if x - 1 not in s:        # 只从起点开始
            cur, length = x, 1
            while cur + 1 in s:
                cur += 1
                length += 1
            ans = max(ans, length)
    return ans""",
        "java": """public int longestConsecutive(int[] nums) {
    Set<Integer> s = new HashSet<>();
    for (int x : nums) s.add(x);
    int ans = 0;
    for (int x : s) {
        if (!s.contains(x - 1)) {
            int cur = x, len = 1;
            while (s.contains(cur + 1)) { cur++; len++; }
            ans = Math.max(ans, len);
        }
    }
    return ans;
}""",
        "time": "O(n) — 每个元素至多被内层 while 访问两次",
        "space": "O(n) — 集合",
        "pitfalls": [
            ("只从起点数", "若对每个数都向后数，会重复计算，最坏 O(n²)"),
            ("去重", "用 set 自动去重，重复元素不影响长度"),
        ],
        "selfcheck": [
            ("为什么复杂度仍是 O(n)？", "每个连续段只在其起点被数一次，段内每个元素最多被「向后找」访问一次，总访问量 ≤ 2n。"),
            ("空数组？", "返回 0。"),
        ],
    },
    # ---------------------------------------------------------------- 57
    {
        "id": 57,
        "title": "分割回文串",
        "diff": "medium",
        "tags": ["回溯"],
        "leetcode": 131,
        "origin": "https://leetcode.cn/problems/palindrome-partitioning/",
        "why": "在字符串上枚举切割点：当前前缀是回文就切下，剩余部分递归分割。用回溯收集所有方案，配合回文预判避免重复判断。",
        "desc": """<p>给定字符串 <code>s</code>，将 s 分割成若干子串，使每个子串都是<strong>回文串</strong>。返回所有可能的分割方案。</p>
<p><strong>示例：</strong><br><code>s="aab"</code> → <code>[["a","a","b"],["aa","b"]]</code></p>""",
        "frames": [
            frame("① 在每个位置决定「切 / 不切」", "drawBacktrack",
                  nodes=[{"val": "aab", "x": 300, "y": 15, "color": "normal"},
                         {"val": "a|ab", "x": 150, "y": 90, "color": "path"}, {"val": "aa|b", "x": 450, "y": 90, "color": "path"},
                         {"val": "a|a|b ✓", "x": 90, "y": 170, "color": "path"}, {"val": "a|ab ✗", "x": 210, "y": 170, "color": "pruned"},
                         {"val": "aa|b ✓", "x": 450, "y": 170, "color": "path"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 150, "y2": 90, "color": "path"}, {"x1": 300, "y1": 15, "x2": 450, "y2": 90, "color": "path"},
                         {"x1": 150, "y1": 90, "x2": 90, "y2": 170, "color": "path"}, {"x1": 150, "y1": 90, "x2": 210, "y2": 170, "color": "pruned"},
                         {"x1": 450, "y1": 90, "x2": 450, "y2": 170, "color": "path"}],
                  width=560, height=220),
            frame("② 前缀回文才切下，否则剪枝", "drawTable",
                  headers=["前缀", "回文?", "动作"],
                  rows=[["a", "✓", "切下，递归 \"ab\""], ["aa", "✓", "切下，递归 \"b\""], ["aab", "✗", "不切"]], width=500, height=160),
        ],
        "conclusion": "枚举每个切点，前缀是回文就继续分割剩余部分，递归到底即得一种方案。",
        "py": """def partition(s):
    n = len(s)
    ans, path = [], []
    def dfs(start):
        if start == n:
            ans.append(path[:]); return
        for end in range(start, n):
            sub = s[start:end + 1]
            if sub == sub[::-1]:       # 前缀回文
                path.append(sub)
                dfs(end + 1)
                path.pop()
    dfs(0)
    return ans""",
        "java": """public List<List<String>> partition(String s) {
    List<List<String>> ans = new ArrayList<>();
    dfs(s, 0, new ArrayList<>(), ans);
    return ans;
}
void dfs(String s, int start, List<String> path, List<List<String>> ans) {
    if (start == s.length()) { ans.add(new ArrayList<>(path)); return; }
    for (int end = start; end < s.length(); end++) {
        if (isPal(s, start, end)) {
            path.add(s.substring(start, end + 1));
            dfs(s, end + 1, path, ans);
            path.remove(path.size() - 1);
        }
    }
}
boolean isPal(String s, int l, int r) {
    while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}""",
        "time": "O(n · 2^n) — 最坏每个前缀都是回文（如全 a）",
        "space": "O(n) — 递归栈 + path",
        "pitfalls": [
            ("回溯恢复 path", "切下后要 pop，否则方案之间互相污染"),
            ("前缀回文判断", "用双指针或 sub==sub[::-1] 判断，别漏单字符（恒为回文）"),
        ],
        "selfcheck": [
            ("s 全相同字符如 \"aaa\"？", "每个前缀都回文，方案数为 2^(n-1)，这是最坏情况。"),
            ("如何优化回文判断？", "用 DP 预计算 pal[i][j]，把 isPal 从 O(n) 降到 O(1)。"),
        ],
    },
    # ---------------------------------------------------------------- 58
    {
        "id": 58,
        "title": "只出现一次的数字",
        "diff": "easy",
        "tags": ["位运算"],
        "leetcode": 136,
        "origin": "https://leetcode.cn/problems/single-number/",
        "why": "异或 XOR 的两个性质：a⊕a=0、a⊕0=a，且满足交换律结合律。把数组所有数异或起来，成对出现的数两两抵消为 0，剩下的就是只出现一次的那个数。",
        "desc": """<p>给定一个<strong>非空</strong>整数数组，除某个元素只出现一次外，其余每个元素均出现<strong>两次</strong>。找出那个只出现一次的元素。要求线性时间 + 常数空间。</p>
<p><strong>示例：</strong><br><code>[2,2,1]</code> → <code>1</code>；<code>[4,1,2,1,2]</code> → <code>4</code></p>""",
        "frames": [
            frame("① XOR：a⊕a=0，成对相消", "drawTable",
                  headers=["数", "二进制", "⊕ 结果"],
                  rows=[["初始", "0", "0"], ["2", "10", "10"], ["2", "10", "0"], ["1", "01", "01"]], width=460, height=190),
            frame("② [4,1,2,1,2] 全部异或 = 4", "drawTable",
                  headers=["步骤", "⊕ 当前", "累计"],
                  rows=[["4", "100", "100"], ["1", "001", "101"], ["2", "010", "111"], ["1", "001", "110"], ["2", "010", "100=4"]], width=460, height=220),
        ],
        "conclusion": "全部异或一遍，重复数字抵消，唯一数字保留。",
        "py": """def singleNumber(nums):
    ans = 0
    for x in nums:
        ans ^= x
    return ans""",
        "java": """public int singleNumber(int[] nums) {
    int ans = 0;
    for (int x : nums) ans ^= x;
    return ans;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("初始化为 0", "0⊕x=x，初始化 0 不影响结果"),
            ("XOR 性质", "成对元素必抵消，顺序无关，交换律结合律保证"),
        ],
        "selfcheck": [
            ("为什么 XOR 天然适用？", "相同数异或为 0，且异或满足交换结合律，遍历顺序无所谓，成对项全部归零。"),
            ("有三个数只出现一次呢？", "那是「只出现一次的数字 III / 数组」变体，需要分组或按位统计，单靠整体 XOR 不够。"),
        ],
    },
    # ---------------------------------------------------------------- 59
    {
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
            frame("① 第一遍：为每个旧节点创建新节点，建立映射", "drawTable",
                  headers=["旧节点", "7", "13", "11", "10", "1"],
                  rows=[["新节点", "7'", "13'", "11'", "10'", "1'"]], width=520, height=110),
            frame("② 第二遍：按映射接 next 与 random", "drawLinkedList",
                  nodes=[{"val": "7", "highlight": "active"}, {"val": "13"}, {"val": "11"}, {"val": "10"}, {"val": "1"}], width=560, height=90),
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
        "pitfalls": [
            ("两遍分开", "第一遍只建节点不接指针，第二遍再 next/random，避免引用尚未创建的节点"),
            ("random 可为 null", "mp.get(None) 返回 None，正好对应 null"),
        ],
        "selfcheck": [
            ("O(1) 空间做法？", "把新节点插在旧节点后面（交错），再用「旧.random.next」取新 random，最后拆链，可省哈希表。"),
            ("为什么不能只复制 next？", "random 可能指向任意节点，不建立映射就无法在新链表里找到对应节点。"),
        ],
    },
    # ---------------------------------------------------------------- 60
    {
        "id": 60,
        "title": "单词拆分",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 139,
        "origin": "https://leetcode.cn/problems/word-break/",
        "why": "dp[i] 表示 s 的前 i 个字符能否由词典拼出。dp[i] = 存在某个词典词，使得 dp[i-len] 为真且 s[i-len:i] 等于该词。逐位递推。",
        "desc": """<p>给定字符串 <code>s</code> 和字符串列表 <code>wordDict</code>，判断 s 是否能被空格拆分为一个或多个在词典中出现的单词。词典中单词可重复使用。</p>
<p><strong>示例：</strong><br><code>s="leetcode", wordDict=["leet","code"]</code> → <code>true</code>；<code>s="catsandog", wordDict=["cats","dog","sand","and","cat"]</code> → <code>false</code></p>""",
        "frames": [
            frame("① dp[i]：前 i 个字符能否拆分", "drawTable",
                  headers=["i", "0", "1", "2", "3", "4", "5", "6", "7", "8"],
                  rows=[["dp", "T", "F", "F", "F", "T", "F", "F", "F", "T"]], width=700, height=120),
            frame("② dp[8] 由 dp[4] 且 s[4:8]=\"code\" 推出", "drawTable",
                  headers=["子串", "leet", "code"],
                  rows=[["在词典?", "✓", "✓"], ["起点 dp", "dp[0]=T", "dp[4]=T"]], width=460, height=140),
        ],
        "conclusion": "枚举结尾 i 与词长，能对上且前缀可拆就置真，最后看 dp[n]。",
        "py": """def wordBreak(s, wordDict):
    words = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for w in words:
            if i >= len(w) and dp[i - len(w)] and s[i - len(w):i] == w:
                dp[i] = True
                break
    return dp[n]""",
        "java": """public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> words = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i <= n; i++)
        for (String w : words)
            if (i >= w.length() && dp[i - w.length()] && s.substring(i - w.length(), i).equals(w)) {
                dp[i] = true; break;
            }
    return dp[n];
}""",
        "time": "O(n · m) — m 为词典单词数",
        "space": "O(n)",
        "pitfalls": [
            ("dp[0]=True", "空前缀可拆分是递推起点"),
            ("用集合存词典", "list 查找 O(m)，set 查找 O(1)"),
        ],
        "selfcheck": [
            ("单词可重复使用吗？", "可以。词典是集合，只要子串匹配且前缀可拆，就能置真。"),
            ("\"catsandog\" 为何 false？", "cat→sand 可行但剩余 \"og\" 无法拆分；cats→and 后 \"og\" 也拆不了；dog 结尾则前缀 \"catsan\" 无法拆。"),
        ],
    },
    # ---------------------------------------------------------------- 61
    {
        "id": 61,
        "title": "环形链表",
        "diff": "easy",
        "tags": ["快慢指针"],
        "leetcode": 141,
        "origin": "https://leetcode.cn/problems/linked-list-cycle/",
        "why": "快慢指针（Floyd 判圈）：慢指针走一步、快指针走两步。若无环，快指针先到 null；若有环，快慢指针必在环内相遇。",
        "desc": """<p>给定链表头节点，判断链表中是否有环。</p>
<p><strong>示例：</strong><br><code>[3,2,0,-4]</code>（尾部连接到下标 1）→ <code>true</code></p>""",
        "frames": [
            frame("① 慢指针走 1 步、快指针走 2 步", "drawLinkedList",
                  nodes=[{"val": 3, "highlight": "active"}, {"val": 2}, {"val": 0}, {"val": -4}], pointers=[{"label": "slow", "x": 40, "y": 90, "targetX": 40, "targetY": 55, "color": "red"}, {"label": "fast", "x": 150, "y": 90, "targetX": 150, "targetY": 55, "color": "gray"}], width=560, height=120),
            frame("② 无环：fast 先到 null，返回 false", "drawLinkedList",
                  nodes=[{"val": 1}, {"val": 2}, {"val": 3, "showNull": True}], width=460, height=90),
            frame("③ 有环：快慢指针在环内必相遇", "drawTable",
                  headers=["轮次", "slow 位置", "fast 位置"],
                  rows=[["0", "3", "3"], ["1", "2", "0"], ["2", "0", "2"], ["3", "-4", "-4 相遇 ✓"]], width=460, height=190),
        ],
        "conclusion": "若有环，fast 相对 slow 每次逼近一步，必然追及；无环则 fast 先到空。",
        "py": """def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False""",
        "java": """public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}""",
        "time": "O(n) — 无环走到底；有环在 O(n) 步内相遇",
        "space": "O(1)",
        "pitfalls": [
            ("循环条件", "while fast and fast.next 都要判空，否则 fast.next.next 空指针"),
            ("相遇即判环", "slow == fast 说明存在环，不需走到 null"),
        ],
        "selfcheck": [
            ("为什么快慢指针一定相遇？", "有环时快慢都进入环，fast 每次多走一步，两者距离逐步缩小到 0，必然追及。"),
            ("哈希表做法？", "遍历时把访问过的节点存 Set，遇到重复即说明有环，但空间 O(n)。"),
        ],
    },
    # ---------------------------------------------------------------- 62
    {
        "id": 62,
        "title": "环形链表 II",
        "diff": "medium",
        "tags": ["快慢指针"],
        "leetcode": 142,
        "origin": "https://leetcode.cn/problems/linked-list-cycle-ii/",
        "why": "先快慢指针判环并找到相遇点，再把一个指针放回头节点，两个指针同速前进，再次相遇处就是环的入口。这是 Floyd 算法的经典结论。",
        "desc": """<p>给定链表头节点，返回链表开始入环的<strong>第一个节点</strong>。若无环，返回 null。</p>
<p><strong>示例：</strong><br><code>[3,2,0,-4]</code>（尾部连接下标 1）→ 返回节点 <code>2</code></p>""",
        "frames": [
            frame("① 快慢指针相遇（在环内某点）", "drawLinkedList",
                  nodes=[{"val": 3}, {"val": 2, "highlight": "active"}, {"val": 0}, {"val": -4}], width=520, height=90),
            frame("② 一个指针放回头，两指针同速前进", "drawTable",
                  headers=["步骤", "指针 A", "指针 B"],
                  rows=[["0", "head(3)", "相遇点"], ["1", "2", "0"], ["2", "0", "-4"], ["3", "-4", "2"], ["4", "2", "2 相遇 ✓"]], width=460, height=220),
            frame("③ 相遇点即环入口 2", "drawLinkedList",
                  nodes=[{"val": 3}, {"val": 2, "highlight": "done"}, {"val": 0}, {"val": -4}], width=520, height=90),
        ],
        "conclusion": "相遇点到入口的距离，恰好等于头到入口的距离，于是同速二刷即得入口。",
        "py": """def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            p = head
            while p != slow:
                p = p.next
                slow = slow.next
            return p
    return None""",
        "java": """public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next; fast = fast.next.next;
        if (slow == fast) {
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;
        }
    }
    return null;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("两阶段", "先判环找相遇点，再从头同速找入口，两步不能省"),
            ("无环返回 null", "快指针到空说明无环"),
        ],
        "selfcheck": [
            ("为什么从头同速走会相遇在入口？", "设头到入口 a、环长 b，相遇时 slow 走了 a+x，fast 走了 2(a+x)；快慢相遇条件推出「头到入口的距离 == 相遇点沿环到入口的距离」。"),
            ("环形链表 I 与 II 区别？", "I 只判有无环；II 要返回入口节点，多一次同速二刷。"),
        ],
    },
    # ---------------------------------------------------------------- 63
    {
        "id": 63,
        "title": "重排链表",
        "diff": "medium",
        "tags": ["链表"],
        "leetcode": 143,
        "origin": "https://leetcode.cn/problems/reorder-list/",
        "why": "目标顺序是「首、尾、次首、次尾…」。三步：找中点 → 反转后半段 → 交替合并两段。每步都是链表基础操作。",
        "desc": """<p>给定单链表，将其重排为 <code>L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …</code> 的形式，不能只改值，必须改变节点结构。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4]</code> → <code>[1,4,2,3]</code>；<code>[1,2,3,4,5]</code> → <code>[1,5,2,4,3]</code></p>""",
        "frames": [
            frame("① 找中点，切成前后两半", "drawLinkedList",
                  nodes=[{"val": 1}, {"val": 2}, {"val": 3, "highlight": "active"}, {"val": 4}, {"val": 5}], width=560, height=90),
            frame("② 反转后半段 3→4→5 变成 5→4→3", "drawLinkedList",
                  nodes=[{"val": 1}, {"val": 2}, {"val": 5, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}], width=560, height=90),
            frame("③ 交替合并：1→5→2→4→3", "drawLinkedList",
                  nodes=[{"val": 1, "highlight": "done"}, {"val": 5, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}], width=560, height=90),
        ],
        "conclusion": "找中点、反转后半、交替拼接，三步组合出「首尾交替」的效果。",
        "py": """def reorderList(head):
    if not head:
        return
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    # 反转后半
    prev, cur = None, slow.next
    slow.next = None
    while cur:
        nxt = cur.next
        cur.next, prev, cur = prev, cur, nxt
    # 交替合并
    a, b = head, prev
    while b:
        a.next, a = b, a.next
        b.next, b = a, b.next""",
        "java": """public void reorderList(ListNode head) {
    if (head == null) return;
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode prev = null, cur = slow.next;
    slow.next = null;
    while (cur != null) { ListNode n = cur.next; cur.next = prev; prev = cur; cur = n; }
    ListNode a = head, b = prev;
    while (b != null) { ListNode na = a.next, nb = b.next; a.next = b; b.next = na; a = na; b = nb; }
}""",
        "time": "O(n) — 三步各扫一遍",
        "space": "O(1)",
        "pitfalls": [
            ("找中点断开", "slow 停在中间，slow.next = None 把前后两段切断"),
            ("合并时保存后继", "交替拼接前先存 a.next、b.next，否则指针被覆盖丢失"),
        ],
        "selfcheck": [
            ("偶数长度 [1,2,3,4]？", "中点 slow=2，后半反转得 4→3，合并得 1→4→2→3。"),
            ("奇数长度 [1,2,3,4,5]？", "中点 slow=3，后半 4→5 反转 5→4，合并 1→5→2→4，剩 3 作尾。"),
        ],
    },
    # ---------------------------------------------------------------- 64
    {
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
            frame("① 容量 2：put(1,1), put(2,2)，顺序 [1,2]", "drawTable",
                  headers=["key", "1", "2"],
                  rows=[["value", "1", "2"], ["序", "旧", "新"]], width=420, height=130),
            frame("② get(1) 命中，把 1 移到最新 → [2,1]", "drawTable",
                  headers=["key", "2", "1"],
                  rows=[["value", "2", "1"], ["序", "旧", "新"]], width=420, height=130),
            frame("③ put(3,3) 满容量，淘汰最旧 2 → [1,3]", "drawTable",
                  headers=["key", "1", "3"],
                  rows=[["value", "1", "3"], ["序", "旧", "新"]], width=420, height=130),
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
        "pitfalls": [
            ("get 命中要 move_to_end", "否则不会刷新「最近使用」顺序，淘汰会删错"),
            ("淘汰最旧用 popitem(last=False)", "last=False 表示删队首（最久未使用）"),
        ],
        "selfcheck": [
            ("put 已存在的 key？", "更新值并移到最新，不增加数量。"),
            ("Java 手写版？", "用 HashMap + 双向链表：map 存节点引用，链表头尾维护顺序，get 时摘节点插到头。"),
        ],
    },
    # ---------------------------------------------------------------- 65
    {
        "id": 65,
        "title": "排序链表",
        "diff": "medium",
        "tags": ["链表", "归并"],
        "leetcode": 148,
        "origin": "https://leetcode.cn/problems/sort-list/",
        "why": "链表不能随机访问，快排不便；归并排序天然适合链表：找中点切成两半，递归排序，再合并两个有序链表。时间 O(n log n)、空间 O(log n) 递归栈。",
        "desc": """<p>给定链表头节点，将其按<strong>升序</strong>排列并返回排序后的链表。要求 O(n log n) 时间。</p>
<p><strong>示例：</strong><br><code>[4,2,1,3]</code> → <code>[1,2,3,4]</code></p>""",
        "frames": [
            frame("① 快慢指针找中点，切两半", "drawLinkedList",
                  nodes=[{"val": 4}, {"val": 2, "highlight": "active"}, {"val": 1}, {"val": 3}], width=520, height=90),
            frame("② 两半各自递归排序：4→2 变 2→4；1→3 保持", "drawTable",
                  headers=["段", "排序前", "排序后"],
                  rows=[["左半", "4→2", "2→4"], ["右半", "1→3", "1→3"]], width=460, height=140),
            frame("③ 归并两个有序链表", "drawLinkedList",
                  nodes=[{"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}], width=520, height=90),
        ],
        "conclusion": "找中点 → 递归排序 → 归并，自顶向下的链表归并排序。",
        "py": """def sortList(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:      # 找中点
        slow, fast = slow.next, fast.next.next
    mid = slow.next
    slow.next = None               # 切断
    left = sortList(head)
    right = sortList(mid)
    return merge(left, right)

def merge(a, b):
    dummy = ListNode(0)
    cur = dummy
    while a and b:
        if a.val < b.val:
            cur.next, a = a, a.next
        else:
            cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next""",
        "java": """public ListNode sortList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode slow = head, fast = head.next;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode mid = slow.next;
    slow.next = null;
    return merge(sortList(head), sortList(mid));
}
ListNode merge(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), cur = dummy;
    while (a != null && b != null) {
        if (a.val < b.val) { cur.next = a; a = a.next; }
        else { cur.next = b; b = b.next; }
        cur = cur.next;
    }
    cur.next = (a != null) ? a : b;
    return dummy.next;
}""",
        "time": "O(n log n) — 归并",
        "space": "O(log n) — 递归栈",
        "pitfalls": [
            ("找中点用 fast=head.next", "这样偶数长度时 slow 停在前半段尾，切分更均衡，避免死循环"),
            ("切断 mid", "slow.next=None 必须切断，否则递归区间重叠"),
        ],
        "selfcheck": [
            ("为什么快排不适合链表？", "链表无法 O(1) 随机访问，分区成本高；归并只需顺序遍历，更适合链表。"),
            ("O(1) 空间的自底向上归并？", "按长度 1,2,4… 逐段两两归并，可省递归栈。"),
        ],
    },
    # ---------------------------------------------------------------- 66
    {
        "id": 66,
        "title": "乘积最大子数组",
        "diff": "medium",
        "tags": ["DP"],
        "leetcode": 152,
        "origin": "https://leetcode.cn/problems/maximum-product-subarray/",
        "why": "乘积会因负数翻转：当前最小可能变最大。同时维护「以 i 结尾的最大乘积」和「最小乘积」，遇到负数交换两者再乘，取全局最大。",
        "desc": """<p>给定整数数组，找出乘积最大的连续子数组，返回该乘积。</p>
<p><strong>示例：</strong><br><code>[2,3,-2,4]</code> → <code>6</code>（[2,3]）；<code>[-2,0,-1]</code> → <code>0</code></p>""",
        "frames": [
            frame("① 同时维护 cur_max 与 cur_min", "drawTable",
                  headers=["i", "0", "1", "2", "3"],
                  rows=[["nums", "2", "3", "-2", "4"], ["cur_max", "2", "6", "-2", "4"], ["cur_min", "2", "3", "-12", "-48"]], width=520, height=150),
            frame("② 遇负数：max 与 min 互换再乘", "drawTable",
                  headers=["步骤", "操作", "cur_max", "cur_min"],
                  rows=[["-2 到来", "swap", "6→-12", "-12→6"]], width=460, height=130),
            frame("③ 全局最大 = 6", "drawTwoPointers", arr=[2, 3, -2, 4], left=0, right=1, window={"start": 0, "end": 1}, width=520, height=140),
        ],
        "conclusion": "最大最小一起维护，负数一来就互换，再与当前值比较更新。",
        "py": """def maxProduct(nums):
    ans = cur_max = cur_min = nums[0]
    for x in nums[1:]:
        if x < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)
        cur_min = min(x, cur_min * x)
        ans = max(ans, cur_max)
    return ans""",
        "java": """public int maxProduct(int[] nums) {
    int ans = nums[0], curMax = nums[0], curMin = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        if (x < 0) { int t = curMax; curMax = curMin; curMin = t; }
        curMax = Math.max(x, curMax * x);
        curMin = Math.min(x, curMin * x);
        ans = Math.max(ans, curMax);
    }
    return ans;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("同时维护最小值", "负数乘最小可能得到最大，只维护最大值会漏"),
            ("遇 0 重开", "x=0 时 cur_max=cur_min=0，下一个数自动另起炉灶"),
        ],
        "selfcheck": [
            ("[-2,0,-1] 为何是 0？", "以 0 为界，cur 归零，后面 -1 单段最大 -1，全局仍 0。"),
            ("为什么不能像最大子数组和那样只维护一个值？", "和是线性叠加，负贡献直接丢弃；乘积遇负会「翻倍变正」，必须保留最小乘积以防翻转。"),
        ],
    },
    # ---------------------------------------------------------------- 67
    {
        "id": 67,
        "title": "寻找旋转排序数组中的最小值",
        "diff": "medium",
        "tags": ["二分"],
        "leetcode": 153,
        "origin": "https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/",
        "why": "旋转数组的最小值就是「断层」位置。二分比较 nums[mid] 与 nums[r]：若 mid 比右端大，说明最小值在右半；否则在左半（含 mid）。",
        "desc": """<p>给定一个<strong>元素值互不相同</strong>且升序排列的数组，在某处旋转后（如 <code>[0,1,2,4,5,6,7]</code> 变为 <code>[4,5,6,7,0,1,2]</code>），找出其中最小元素。要求 O(log n)。</p>
<p><strong>示例：</strong><br><code>[3,4,5,1,2]</code> → <code>1</code>；<code>[4,5,6,7,0,1,2]</code> → <code>0</code></p>""",
        "frames": [
            frame("① 比较 mid 与右端：5 > 2 → 最小值在右半", "drawBinarySearch", arr=[3, 4, 5, 1, 2], left=0, mid=2, right=4, width=520, height=140),
            frame("② 收缩到右半 [1,2]，mid=1，1 <= 2 → 在左半", "drawBinarySearch", arr=[3, 4, 5, 1, 2], left=3, mid=3, right=4, excludedRanges=[{"start": 0, "end": 2}], width=520, height=140),
            frame("③ 收敛到 left=right，即最小值 1", "drawBinarySearch", arr=[3, 4, 5, 1, 2], left=3, mid=3, right=3, excludedRanges=[{"start": 0, "end": 2}], width=520, height=140),
        ],
        "conclusion": "mid 与右端比较决定收缩方向，直到 l==r 即最小值。",
        "py": """def findMin(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if nums[m] > nums[r]:   # 断层在右半
            l = m + 1
        else:                   # 断层在左半（含 m）
            r = m
    return nums[l]""",
        "java": """public int findMin(int[] nums) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int m = (l + r) >>> 1;
        if (nums[m] > nums[r]) l = m + 1; else r = m;
    }
    return nums[l];
}""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            ("与右端比较", "与 nums[r] 比较最直观；与左端比较需额外处理未旋转情况"),
            ("r = m 而不是 m-1", "nums[m] <= nums[r] 时 m 可能正是最小值，不能跳过"),
        ],
        "selfcheck": [
            ("完全没旋转（升序）？", "nums[m] 恒 <= nums[r]，r 一路左移，最终 l=0 返回最小值 nums[0]。"),
            ("含重复元素呢？", "那就是 154 题，遇到 nums[m]==nums[r] 需 r-- 逐退，无法纯二分。"),
        ],
    },
    # ---------------------------------------------------------------- 68
    {
        "id": 68,
        "title": "最小栈",
        "diff": "medium",
        "tags": ["栈"],
        "leetcode": 155,
        "origin": "https://leetcode.cn/problems/min-stack/",
        "why": "普通栈只能取栈顶。用「辅助栈」同步记录每个状态下的最小值：压入时把 min(当前值, 之前最小值) 一起入辅助栈，pop 时同步弹出，getMin 取辅助栈顶 O(1)。",
        "desc": """<p>设计一个支持 push、pop、top 操作，并能在常数时间内检索到最小元素的栈。</p>
<p><strong>示例：</strong><br><code>push(-2), push(0), push(-3), getMin()→-3, pop(), top()→0, getMin()→-2</code></p>""",
        "frames": [
            frame("① 数据栈与辅助栈同步", "drawStack",
                  items=[{"val": "-2"}, {"val": "0"}, {"val": "-3"}], type="stack", height=180),
            frame("② 辅助栈存「到当前为止的最小值」", "drawStack",
                  items=[{"val": "-2"}, {"val": "-2"}, {"val": "-3"}], type="stack", height=180),
            frame("③ pop 后辅助栈同步弹出，getMin = -2", "drawStack",
                  items=[{"val": "-2"}, {"val": "-2"}], type="stack", height=150),
        ],
        "conclusion": "每个元素入栈时，把「当前最小值」一并存进辅助栈，弹出时同步，getMin 恒为辅助栈顶。",
        "py": """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val):
        self.stack.append(val)
        self.min_stack.append(val if not self.min_stack else min(val, self.min_stack[-1]))
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()
    def top(self):
        return self.stack[-1]
    def getMin(self):
        return self.min_stack[-1]""",
        "java": """class MinStack {
    Deque<Integer> st = new ArrayDeque<>(), mn = new ArrayDeque<>();
    public void push(int val) {
        st.push(val);
        mn.push(mn.isEmpty() ? val : Math.min(val, mn.peek()));
    }
    public void pop() { st.pop(); mn.pop(); }
    public int top() { return st.peek(); }
    public int getMin() { return mn.peek(); }
}""",
        "time": "所有操作 O(1)",
        "space": "O(n) — 两个栈",
        "pitfalls": [
            ("pop 同步", "数据栈与辅助栈必须同时 pop，否则 getMin 错位"),
            ("push 的 min 判断", "辅助栈为空时直接入栈，否则取 min(val, 当前最小)"),
        ],
        "selfcheck": [
            ("重复的最小值怎么处理？", "每次都入栈，即使相等也入，保证栈深一致、弹出对位。"),
            ("能省空间吗？", "可以只在新最小值 <= 当前最小才入辅助栈，弹出时相等才弹出，但实现稍复杂。"),
        ],
    },
    # ---------------------------------------------------------------- 69
    {
        "id": 69,
        "title": "相交链表",
        "diff": "easy",
        "tags": ["链表"],
        "leetcode": 160,
        "origin": "https://leetcode.cn/problems/intersection-of-two-linked-lists/",
        "why": "两个指针分别从 A、B 出发，走到头就换到另一条链继续走。若相交，两指针走的总路程相等，必在交点相遇；若不相交，最后同时为 null。",
        "desc": """<p>给定两个单链表的头节点，找出并返回它们相交的起始节点；不相交则返回 null。</p>
<p><strong>示例：</strong><br>listA=[4,1,8,4,5], listB=[5,6,1,8,4,5]（在 8 相交）→ 返回节点 8</p>""",
        "frames": [
            frame("① 两条链长度不同，直接同步走会错过交点", "drawLinkedList",
                  nodes=[{"val": 4}, {"val": 1}, {"val": 8, "highlight": "active"}, {"val": 4}, {"val": 5}], width=560, height=90),
            frame("② 指针走到头就换到另一条链，路程对齐", "drawTable",
                  headers=["步", "指针 a", "指针 b"],
                  rows=[["0", "A头(4)", "B头(5)"], ["1", "1", "6"], ["2", "8", "1"], ["3", "4", "8 相遇 ✓"]], width=460, height=190),
            frame("③ 相交点 8；不相交则最终同到 null", "drawLinkedList",
                  nodes=[{"val": 4}, {"val": 1}, {"val": 8, "highlight": "done"}], width=460, height=90),
        ],
        "conclusion": "「走完自己再走对方」让两指针总路程相等，交点必然相遇。",
        "py": """def getIntersectionNode(headA, headB):
    a, b = headA, headB
    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a""",
        "java": """public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    ListNode a = headA, b = headB;
    while (a != b) {
        a = (a == null) ? headB : a.next;
        b = (b == null) ? headA : b.next;
    }
    return a;
}""",
        "time": "O(m + n)",
        "space": "O(1)",
        "pitfalls": [
            ("走到头换链", "a 到 null 后跳 headB，而不是停在 null"),
            ("终止条件", "循环 a != b；不相交时二者最终都为 null，自然退出"),
        ],
        "selfcheck": [
            ("不相交会死循环吗？", "不会。两指针各走 m+n 步后同时到达 null，a==b 退出。"),
            ("哈希表做法？", "把 A 的节点存 Set，遍历 B 找第一个在 Set 中的节点，空间 O(m)。"),
        ],
    },
    # ---------------------------------------------------------------- 70
    {
        "id": 70,
        "title": "多数元素",
        "diff": "easy",
        "tags": ["投票"],
        "leetcode": 169,
        "origin": "https://leetcode.cn/problems/majority-element/",
        "why": "Boyer-Moore 投票：维护候选人和计数。遇到相同数 +1、不同数 -1，计数归零就换候选人。多数元素出现次数超过一半，最终幸存者必是它。",
        "desc": """<p>给定大小为 n 的数组，返回其中的<strong>多数元素</strong>。多数元素指在数组中出现次数<strong>大于 ⌊n/2⌋</strong> 的元素。保证一定存在。</p>
<p><strong>示例：</strong><br><code>[2,2,1,1,1,2,2]</code> → <code>2</code></p>""",
        "frames": [
            frame("① 候选人 cand，计数 count：相同 +1、不同 -1", "drawTable",
                  headers=["步骤", "元素", "cand", "count"],
                  rows=[["1", "2", "2", "1"], ["2", "2", "2", "2"], ["3", "1", "2", "1"], ["4", "1", "2", "0"], ["5", "1", "1", "1"], ["6", "2", "1", "0"], ["7", "2", "2", "1"]], width=460, height=240),
            frame("② 最终幸存者 2 即多数元素", "drawTwoPointers", arr=[2, 2, 1, 1, 1, 2, 2], left=0, right=6, width=520, height=130),
        ],
        "conclusion": "多数元素出现次数过半，「抵消」不掉，投票结束后仍存活。",
        "py": """def majorityElement(nums):
    cand = count = 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand""",
        "java": """public int majorityElement(int[] nums) {
    int cand = 0, count = 0;
    for (int x : nums) {
        if (count == 0) cand = x;
        count += (x == cand) ? 1 : -1;
    }
    return cand;
}""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            ("count==0 换候选人", "抵消完后，下一个元素成为新候选人"),
            ("前提是多数元素存在", "题目保证一定存在；若不确定，最后要再遍历验证一次"),
        ],
        "selfcheck": [
            ("为什么投票法成立？", "多数元素次数 > n/2，任何其它元素集合的总数都 < n/2，抵消到最后必有剩余，且剩余者就是多数。"),
            ("若不一定存在多数元素？", "投票后需再扫描一遍确认 cand 次数是否真的 > n/2，否则返回无解。"),
        ],
    },
]

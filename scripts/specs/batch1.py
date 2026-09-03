from scripts.algo_gen import frame


PROBLEMS = [
    # ---------------------------------------------------------------- 11
    {
        "id": 11,
        "title": "有效的括号",
        "diff": "easy",
        "tags": ["栈"],
        "leetcode": 20,
        "origin": "https://leetcode.cn/problems/valid-parentheses/",
        "why": "括号配对是典型的「后进先出」：最近出现的左括号，必须最先被对应的右括号闭合。用栈天然匹配——遇到左括号入栈，遇到右括号就弹出栈顶对比，顺序错了立刻失败。",
        "desc": """<p>给定一个只包括 <code>(</code>，<code>)</code>，<code>{</code>，<code>}</code>，<code>[</code>，<code>]</code> 的字符串 <code>s</code>，判断字符串是否有效。</p>
<p>有效需满足：左括号必须用<strong>相同类型</strong>的右括号闭合；左括号必须以<strong>正确的顺序</strong>闭合。</p>
<p><strong>示例：</strong><br><code>s = "()[]{}"</code> → <code>true</code><br><code>s = "(]"</code> → <code>false</code></p>""",
        "frames": [
            frame("① 遇 '(' 入栈", "drawStack", items=[{"val": "("}], type="stack", height=140),
            frame("② 遇 '[' 入栈（栈顶为 '['）", "drawStack", items=[{"val": "("}, {"val": "["}], type="stack", height=140),
            frame("③ 遇 ']'，与栈顶 '[' 匹配 → 出栈", "drawStack", items=[{"val": "("}], type="stack", height=140),
            frame("④ 遇 ')'，与栈顶 '(' 匹配 → 出栈，栈空 → 有效", "drawStack", items=[], type="stack", height=120),
        ],
        "conclusion": "一路匹配成功且最终栈为空，说明每个右括号都恰好闭合了最近的那个左括号。",
        "py": """def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs:          # 右括号：必须匹配栈顶
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:                    # 左括号：入栈
            stack.append(ch)
    return not stack            # 最后栈必须为空""",
        "java": """public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{'))
                return false;
        }
    }
    return stack.isEmpty();
}""",
        "time": "O(n) — 每个字符入栈/出栈一次",
        "space": "O(n) — 最坏情况全是左括号",
        "pitfalls": [
            ("右括号要先判断栈空", "否则对 s = \"]\" 直接 pop 会越界（Java 抛异常）"),
            ("最后必须栈空", "忘写 return not stack 会把 \"(()\" 误判为有效"),
            ("不能只数个数", "像 \"([)]\" 左右括号个数都平衡，但顺序错，必须用栈保证顺序"),
        ],
        "selfcheck": [
            ("字符串 \"([)]\" 是否有效？", "无效。遇到 ')' 时栈顶是 '['，类型不匹配。它数量平衡但顺序错——这正是栈和计数器的区别。"),
            ("只用三种括号时，能否用三个计数器代替栈？", "不能。计数器无法感知「最近未闭合」的顺序，无法识别 \"([)]\" 这类错序；栈的 LIFO 特性恰好对应括号的嵌套结构。"),
        ],
    },
    # ---------------------------------------------------------------- 12
    {
        "id": 12,
        "title": "合并两个有序链表",
        "diff": "easy",
        "tags": ["链表"],
        "leetcode": 21,
        "origin": "https://leetcode.cn/problems/merge-two-sorted-lists/",
        "why": "两个链表都已有序，合并就等价于「每次从两个头结点里取较小的那个」不断拼接。引入一个 dummy 哨兵节点，可以避免对「新链表的头是谁」做特殊判断。",
        "desc": """<p>将两个<strong>升序</strong>链表合并为一个新的升序链表并返回。新链表由给定两个链表的所有节点拼接组成。</p>
<p><strong>示例：</strong><br><code>l1 = [1,2,4]</code>，<code>l2 = [1,3,4]</code> → <code>[1,1,2,3,4,4]</code></p>""",
        "frames": [
            frame("① 两个头 1 和 1 比较，取 l1 的 1", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}], width=560, height=90),
            frame("② l1 头=2 > l2 头=1，取 l2 的 1", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 1, "highlight": "done"}], width=560, height=90),
            frame("③ 依次取 2→3→4，最后 l2 空，接上 l1 剩余 4", "drawLinkedList", nodes=[{"val": 1, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 4, "highlight": "done"}], width=680, height=90),
        ],
        "conclusion": "每次取较小头、步进对应链表；当一条链走完，把另一条剩余部分整体接上即可。",
        "py": """def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next, l1 = l1, l1.next
        else:
            cur.next, l2 = l2, l2.next
        cur = cur.next
    cur.next = l1 or l2   # 剩余部分整体接上
    return dummy.next""",
        "java": """public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), cur = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
        else                  { cur.next = l2; l2 = l2.next; }
        cur = cur.next;
    }
    cur.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}""",
        "time": "O(m + n) — 每个节点访问一次",
        "space": "O(1) — 只改指针，不额外分配节点",
        "pitfalls": [
            ("用 dummy 哨兵", "避免「第一个节点从 l1 还是 l2 取」的分支，返回 dummy.next 即可"),
            ("循环结束后接剩余", "忘写 cur.next = l1 or l2 会丢掉较长链表的尾巴"),
        ],
        "selfcheck": [
            ("两条链表一空一非空怎么处理？", "while 条件直接不成立，cur.next = l1 or l2 把非空链表整体接上，返回 dummy.next，逻辑天然覆盖。"),
            ("递归写法怎么写？", "merge(l1,l2)：若 l1 空返回 l2，l2 空返回 l1；否则取较小者为头，其 next = merge(较小者.next, 另一个)。"),
        ],
    },
    # ---------------------------------------------------------------- 13
    {
        "id": 13,
        "title": "括号生成",
        "diff": "medium",
        "tags": ["回溯"],
        "leetcode": 22,
        "origin": "https://leetcode.cn/problems/generate-parentheses/",
        "why": "生成所有合法括号组合，本质是一棵决策树：每一步要么放 '(' 要么放 ')'。两条剪枝规则保证结果合法——左括号数量不超过 n，右括号数量不超过当前左括号数（否则会「先右后左」不匹配）。",
        "desc": """<p>数字 <code>n</code> 代表生成括号的对数，设计一个函数，返回所有可能的并且<strong>有效的</strong>括号组合。</p>
<p><strong>示例：</strong><br><code>n = 3</code> → <code>["((()))","(()())","(())()","()(())","()()()"]</code></p>""",
        "frames": [
            frame("① 决策树：每步放 '(' 或 ')'，剪掉非法分支", "drawBacktrack",
                  nodes=[
                      {"val": "", "x": 300, "y": 20, "color": "normal"},
                      {"val": "(", "x": 160, "y": 80, "color": "path"},
                      {"val": "((", "x": 60, "y": 150, "color": "path"},
                      {"val": "(((", "x": 30, "y": 220, "color": "path"},
                      {"val": "((()", "x": 140, "y": 290, "color": "path"},
                      {"val": "()", "x": 480, "y": 150, "color": "path"},
                      {"val": "())", "x": 540, "y": 220, "color": "pruned"},
                  ],
                  edges=[
                      {"x1": 300, "y1": 20, "x2": 160, "y2": 80, "color": "path"},
                      {"x1": 300, "y1": 20, "x2": 480, "y2": 150, "color": "path"},
                      {"x1": 160, "y1": 80, "x2": 60, "y2": 150, "color": "path"},
                      {"x1": 60, "y1": 150, "x2": 30, "y2": 220, "color": "path"},
                      {"x1": 30, "y1": 220, "x2": 140, "y2": 290, "color": "path"},
                      {"x1": 480, "y1": 150, "x2": 540, "y2": 220, "color": "pruned"},
                  ],
                  width=620, height=320),
            frame("② n=1：先 '(' 再 ')'，得 ()", "drawBacktrack",
                  nodes=[{"val": "", "x": 300, "y": 20, "color": "normal"}, {"val": "(", "x": 220, "y": 90, "color": "path"}, {"val": "()", "x": 220, "y": 170, "color": "path"}],
                  edges=[{"x1": 300, "y1": 20, "x2": 220, "y2": 90, "color": "path"}, {"x1": 220, "y1": 90, "x2": 220, "y2": 170, "color": "path"}],
                  width=620, height=220),
        ],
        "conclusion": "「左括号数 ≤ n」与「右括号数 ≤ 左括号数」两条约束贯穿整棵树，走到 2n 长度就收集一个答案。",
        "py": """def generateParenthesis(n):
    ans = []
    def dfs(s, left, right):
        if len(s) == 2 * n:
            ans.append(s); return
        if left < n:                       # 还能放左括号
            dfs(s + '(', left + 1, right)
        if right < left:                   # 右括号不能超过左括号
            dfs(s + ')', left, right + 1)
    dfs('', 0, 0)
    return ans""",
        "java": """public List<String> generateParenthesis(int n) {
    List<String> ans = new ArrayList<>();
    dfs(new StringBuilder(), 0, 0, n, ans);
    return ans;
}
void dfs(StringBuilder sb, int left, int right, int n, List<String> ans) {
    if (sb.length() == 2 * n) { ans.add(sb.toString()); return; }
    if (left < n) { sb.append('('); dfs(sb, left + 1, right, n, ans); sb.deleteCharAt(sb.length() - 1); }
    if (right < left) { sb.append(')'); dfs(sb, left, right + 1, n, ans); sb.deleteCharAt(sb.length() - 1); }
}""",
        "time": "O(C(2n,n)/(n+1) · n) — 卡特兰数个答案，每个答案长 2n",
        "space": "O(n) — 递归栈深度 2n",
        "pitfalls": [
            ("剪枝条件写反", "右括号条件是 right < left 而非 right < n，否则会生成 \")(\" 这种非法开头"),
            ("回溯要恢复现场", "用可变字符串（StringBuilder）时，递归返回后要 deleteCharAt 撤销本次选择"),
        ],
        "selfcheck": [
            ("为什么第二个条件不是 right < n 而是 right < left？", "right < n 只限制总量，无法阻止右括号出现在左括号之前（如 ')(('）；right < left 保证任意前缀里右括号都不多于左括号，这正是合法的充要条件。"),
            ("n=1 会生成什么？", "先放 '('，此时 right(0) < left(1) 可放 ')'，得 '()'；没有其他分支，结果唯一。"),
        ],
    },
    # ---------------------------------------------------------------- 14
    {
        "id": 14,
        "title": "合并K个升序链表",
        "diff": "hard",
        "tags": ["堆", "链表"],
        "leetcode": 23,
        "origin": "https://leetcode.cn/problems/merge-k-sorted-lists/",
        "why": "K 条有序链表的合并，每一轮都要知道「K 个当前头里谁最小」。最小堆正好 O(log K) 取出最小值，再用 dummy 哨兵逐个拼接，比两两合并更简洁高效。",
        "desc": """<p>给定一个链表数组，每个链表都已按<strong>升序</strong>排列。将所有链表合并为一个升序链表并返回。</p>
<p><strong>示例：</strong><br><code>lists = [[1,4,5],[1,3,4],[2,6]]</code> → <code>[1,1,2,3,4,4,5,6]</code></p>""",
        "frames": [
            frame("① 三条链的头入堆：1、1、2", "drawTable",
                  headers=["链表", "当前头", "内容"],
                  rows=[["L1", {"val": "1", "highlight": True}, "1→4→5"], ["L2", {"val": "1", "highlight": True}, "1→3→4"], ["L3", {"val": "2", "highlight": True}, "2→6"]],
                  width=520, height=160),
            frame("② 弹出最小头 1，接进结果，压入其 next=4", "drawLinkedList",
                  nodes=[{"val": 1, "highlight": "done"}], width=560, height=90),
            frame("③ 不断弹出最小头拼接，直到堆空", "drawLinkedList",
                  nodes=[{"val": 1, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 2, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 5, "highlight": "done"}, {"val": 6, "highlight": "done"}], width=720, height=90),
        ],
        "conclusion": "堆里始终保存「每条链当前最小头」，反复 pop 最小 + push 其后继，直到所有节点都被取出。",
        "py": """import heapq
def mergeKLists(lists):
    dummy = ListNode(0)
    cur = dummy
    heap = []
    for i, node in enumerate(lists):      # 用 i 避免节点值相等时的比较问题
        if node:
            heapq.heappush(heap, (node.val, i, node))
    while heap:
        _, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next""",
        "java": """public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
    for (ListNode n : lists) if (n != null) pq.offer(n);
    ListNode dummy = new ListNode(0), cur = dummy;
    while (!pq.isEmpty()) {
        ListNode n = pq.poll();
        cur.next = n; cur = cur.next;
        if (n.next != null) pq.offer(n.next);
    }
    return dummy.next;
}""",
        "time": "O(N log K) — N 为总节点数，堆操作 O(log K)",
        "space": "O(K) — 堆中最多 K 个节点",
        "pitfalls": [
            ("堆元素比较问题", "Python 元组里若节点值相等，会去比较 ListNode 导致报错，需加下标 i 兜底"),
            ("初始入堆要判空", "lists 里可能含空链表，空链表不入堆"),
        ],
        "selfcheck": [
            ("如果 K 条链表里有空链表会怎样？", "只把非空链表头入堆即可；若全部为空，堆为空，直接返回 dummy.next = None。"),
            ("为什么复杂度是 O(N log K) 而不是 O(NK)？", "每次取最小是 O(log K)（堆），共 N 个节点，所以 N log K；暴力每次线性扫 K 个头才是 O(NK)。"),
        ],
    },
    # ---------------------------------------------------------------- 15
    {
        "id": 15,
        "title": "两两交换链表中的节点",
        "diff": "medium",
        "tags": ["链表"],
        "leetcode": 24,
        "origin": "https://leetcode.cn/problems/swap-nodes-in-pairs/",
        "why": "交换相邻两节点要同时改三条 next 指针，顺序一旦搞反就会断链。用 dummy 哨兵 + 三个指针（pre、first、second）按固定顺序翻转，边界清晰不易错。",
        "desc": """<p>给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。不能只改节点内部的值，必须实际进行节点交换。</p>
<p><strong>示例：</strong><br><code>[1,2,3,4]</code> → <code>[2,1,4,3]</code></p>""",
        "frames": [
            frame("① 原链表 1→2→3→4", "drawLinkedList", nodes=[{"val": 1}, {"val": 2}, {"val": 3}, {"val": 4}], width=520, height=90),
            frame("② 交换 1、2：pre→2→1→(3)", "drawLinkedList", nodes=[{"val": 2, "highlight": "active"}, {"val": 1, "highlight": "active"}, {"val": 3}, {"val": 4}], width=520, height=90),
            frame("③ 交换 3、4，完成", "drawLinkedList", nodes=[{"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}], width=520, height=90),
        ],
        "conclusion": "每组交换前先「记住」组后的节点，再按 2→1→后组 的顺序接好，指针就不会断。",
        "py": """def swapPairs(head):
    dummy = ListNode(0, head)
    pre = dummy
    while pre.next and pre.next.next:
        a, b = pre.next, pre.next.next
        pre.next, a.next, b.next = b, b.next, a
        pre = a
    return dummy.next""",
        "java": """public ListNode swapPairs(ListNode head) {
    ListNode dummy = new ListNode(0, head), pre = dummy;
    while (pre.next != null && pre.next.next != null) {
        ListNode a = pre.next, b = a.next;
        a.next = b.next;
        b.next = a;
        pre.next = b;
        pre = a;
    }
    return dummy.next;
}""",
        "time": "O(n) — 每对节点交换一次",
        "space": "O(1) — 只改指针",
        "pitfalls": [
            ("指针赋值顺序", "先把 a.next 指向 b.next（保住后续节点），再让 b.next = a，否则会丢链"),
            ("循环条件", "pre.next and pre.next.next 都非空才成对交换，只剩一个节点时保持不动"),
        ],
        "selfcheck": [
            ("链表长度为奇数（如 [1,2,3]）结果是什么？", "交换 1、2 后 pre 指向 2，此时 pre.next=3 但 pre.next.next 为空，循环结束，结果为 [2,1,3]。"),
            ("为什么不能只交换值？", "题目要求实际交换节点；而且值交换无法处理带随机指针等复杂节点，指针交换才是通用做法。"),
        ],
    },
    # ---------------------------------------------------------------- 16
    {
        "id": 16,
        "title": "K个一组翻转链表",
        "diff": "hard",
        "tags": ["链表"],
        "leetcode": 25,
        "origin": "https://leetcode.cn/problems/reverse-nodes-in-k-group/",
        "why": "整段翻转是「翻转链表」的推广：先数出 K 个节点，不足 K 就不翻；够 K 就用头插法/三指针翻转这一段，再把上一段的尾巴接到新头。核心是「分组 + 段内翻转 + 接缝处理」。",
        "desc": """<p>给链表的每 <code>k</code> 个节点一组进行翻转，返回修改后的链表。<code>k</code> 是正整数且小于等于链表长度。如果节点总数不是 <code>k</code> 的整数倍，最后剩余的节点保持原样。</p>
<p><strong>示例：</strong><br><code>head = [1,2,3,4,5], k = 2</code> → <code>[2,1,4,3,5]</code><br><code>k = 3</code> → <code>[3,2,1,4,5]</code></p>""",
        "frames": [
            frame("① 先数出 K=2 个节点：1、2", "drawLinkedList", nodes=[{"val": 1, "highlight": "active"}, {"val": 2, "highlight": "active"}, {"val": 3}, {"val": 4}, {"val": 5}], width=560, height=90),
            frame("② 翻转该组：2→1，再接回 3", "drawLinkedList", nodes=[{"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 3}, {"val": 4}, {"val": 5}], width=560, height=90),
            frame("③ 下一组 3、4 翻转，尾组 5 不足 K 保持原样", "drawLinkedList", nodes=[{"val": 2, "highlight": "done"}, {"val": 1, "highlight": "done"}, {"val": 4, "highlight": "done"}, {"val": 3, "highlight": "done"}, {"val": 5}], width=560, height=90),
        ],
        "conclusion": "每组先判断「是否凑满 K」，够 K 翻、不够 K 停；翻转后把组头接到上一组尾部即可。",
        "py": """def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    pre = dummy
    while True:
        tail = pre
        for _ in range(k):               # 数 K 个
            tail = tail.next
            if not tail:
                return dummy.next        # 不足 K，不再翻转
        nxt = tail.next
        cur, prev = pre.next, nxt
        while cur is not nxt:            # 段内翻转
            tmp = cur.next
            cur.next, prev, cur = prev, cur, tmp
        pre.next, pre = tail, pre.next   # 接缝
    """,
        "java": """public ListNode reverseKGroup(ListNode head, int k) {
    ListNode dummy = new ListNode(0, head), pre = dummy;
    while (true) {
        ListNode tail = pre;
        for (int i = 0; i < k; i++) { tail = tail.next; if (tail == null) return dummy.next; }
        ListNode nxt = tail.next, cur = pre.next, prev = nxt;
        while (cur != nxt) { ListNode tmp = cur.next; cur.next = prev; prev = cur; cur = tmp; }
        ListNode newHead = pre.next;
        pre.next = tail; pre = newHead;
    }
}""",
        "time": "O(n) — 每个节点恰好处理一次",
        "space": "O(1) — 原地翻转",
        "pitfalls": [
            ("不足 K 要原样保留", "先数 K 再决定是否翻转；边翻边发现不足 K 会翻乱尾巴"),
            ("翻转后接缝", "每段翻完要把「上一段尾」接到本段新头，并把本段新尾接到下一段"),
        ],
        "selfcheck": [
            ("k=1 时结果是什么？", "每 1 个一组翻转等于不翻转，直接返回原链表。"),
            ("为什么每段翻转用 cur != nxt 而不是 cur？", "因为翻转段的「终点」是下一段的头 nxt，cur 走到 nxt 就表示本段翻完，这样不会越界翻到下一段。"),
        ],
    },
    # ---------------------------------------------------------------- 17
    {
        "id": 17,
        "title": "下一个排列",
        "diff": "medium",
        "tags": ["数组"],
        "leetcode": 31,
        "origin": "https://leetcode.cn/problems/next-permutation/",
        "why": "「下一个排列」要找到比当前字典序大、且大得最少的一个。方法很固定：从右往左找第一个「降序对」，把它右边的较大者交换过来，再把右边反转成升序（最小化）。",
        "desc": """<p>整数数组的一个排列，就是将其所有成员按任意顺序排列。例如 <code>arr = [1,2,3]</code> 的排列有 <code>[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]</code>。</p>
<p>给定一个排列，将其<strong>原地</strong>重新排列为字典序的<strong>下一个</strong>排列；如果已经是最大排列，则重排为最小排列。</p>
<p><strong>示例：</strong><br><code>[1,2,3] → [1,3,2]</code>；<code>[3,2,1] → [1,2,3]</code>；<code>[1,1,5] → [1,5,1]</code></p>""",
        "frames": [
            frame("① 从右找第一个「上升」位置 i（nums[i] < nums[i+1]）", "drawTwoPointers", arr=[1, 2, 3], left=1, right=2, width=520, height=140),
            frame("② 在右侧找比 nums[i]=2 大的最小数 3，交换", "drawTable",
                  headers=["索引", "0", "1", "2"], rows=[["交换前", "1", "2", "3"], ["交换后", "1", {"val": "3", "highlight": True}, {"val": "2", "highlight": True}]], width=520, height=140),
            frame("③ 把 i 右侧反转成升序（最小化）", "drawTable",
                  headers=["索引", "0", "1", "2"], rows=[["结果", "1", "3", "2"]], width=520, height=120),
        ],
        "conclusion": "找到「最靠右的可增大位置」，用右侧最小的较大值替换，再让右边升序，就得到恰好多一点的下一个排列。",
        "py": """def nextPermutation(nums):
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:   # 找上升点
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:              # 找右侧较大者
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    l, r = i + 1, n - 1                        # 反转右侧
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1; r -= 1""",
        "java": """public void nextPermutation(int[] nums) {
    int n = nums.length, i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) j--;
        int t = nums[i]; nums[i] = nums[j]; nums[j] = t;
    }
    for (int l = i + 1, r = n - 1; l < r; l++, r--) {
        int t = nums[l]; nums[l] = nums[r]; nums[r] = t;
    }
}""",
        "time": "O(n) — 至多三次扫描",
        "space": "O(1) — 原地交换",
        "pitfalls": [
            ("找上升点用 < 不用 <=", "while nums[i] >= nums[i+1] 要跳过相等情况，否则遇到 [1,1,5] 会找错位置"),
            ("已最大时反转整个数组", "i 走到 -1 说明完全降序，直接反转整个数组回到最小排列"),
        ],
        "selfcheck": [
            ("为什么交换后还要把右侧反转？", "交换只保证「变大」，右侧当前是降序（最大），反转为升序（最小）才能保证这是「恰好多一点」的下一个。"),
            ("[3,2,1] 的下一排列是什么？", "从右到左一路降序，i=-1，直接反转整个数组得 [1,2,3]，即回到最小。"),
        ],
    },
    # ---------------------------------------------------------------- 18
    {
        "id": 18,
        "title": "最长有效括号",
        "diff": "hard",
        "tags": ["DP", "栈"],
        "leetcode": 32,
        "origin": "https://leetcode.cn/problems/longest-valid-parentheses/",
        "why": "求「连续」有效括号的最长长度，关键是要能算出每个右括号能向左延伸到哪。栈里存<strong>下标</strong>而不是括号本身：遇到匹配就弹出，栈顶下标就是当前段的前一个位置，长度 = i - 栈顶。",
        "desc": """<p>给定只包含 <code>(</code> 和 <code>)</code> 的字符串，找出最长有效（格式正确且连续）括号子串的长度。</p>
<p><strong>示例：</strong><br><code>s = "(()"</code> → <code>2</code>（最长是 <code>"()"</code>）<br><code>s = ")()())"</code> → <code>4</code>（最长是 <code>"()()"</code>）</p>""",
        "frames": [
            frame("① 栈底先放 -1 作为「段起点」哨兵", "drawStack", items=[{"val": "-1", "label": "栈底"}], type="stack", height=120),
            frame("② 遇 '(' 存下标 0、1", "drawStack", items=[{"val": "-1"}, {"val": "0"}, {"val": "1"}], type="stack", height=150),
            frame("③ 遇 ')' 弹栈匹配，长度 = 当前下标 - 栈顶", "drawTable",
                  headers=["位置", "0", "1", "2", "3", "4", "5"],
                  rows=[["字符", "(", "(", ")", ")", "(", ")"], ["最长", "", "", "2", "2", "", "4"]], width=560, height=140),
        ],
        "conclusion": "栈底永远是「当前有效段起点前一位」，每次成功匹配后用 i - 栈顶下标 更新答案，天然覆盖连续多段。",
        "py": """def longestValidParentheses(s):
    stack = [-1]               # 哨兵：段起点前一位
    ans = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:      # 段断了，重置起点
                stack.append(i)
            else:
                ans = max(ans, i - stack[-1])
    return ans""",
        "java": """public int longestValidParentheses(String s) {
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(-1);
    int ans = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == '(') stack.push(i);
        else {
            stack.pop();
            if (stack.isEmpty()) stack.push(i);
            else ans = Math.max(ans, i - stack.peek());
        }
    }
    return ans;
}""",
        "time": "O(n) — 每个字符入栈出栈一次",
        "space": "O(n) — 栈存下标",
        "pitfalls": [
            ("栈存下标而非字符", "只有下标能算出长度；存字符只能判断合法性、算不出连续长度"),
            ("弹空后要 push 当前 i", "出现多余右括号时有效段被截断，把当前 i 当新起点，避免把两段错误接起来"),
        ],
        "selfcheck": [
            ("s = \"(()\" 的过程是怎样的？", "栈 [-1]；'(' 入 0、1 → [-1,0,1]；')' 弹 1，长度 2-0=2。最后 ans=2。"),
            ("为什么不直接数配对总数？", "题目要求「连续」，如 \")(\" 配对数为 0 但字符间不连续，栈下标法能正确处理段与段之间的断开。"),
        ],
    },
    # ---------------------------------------------------------------- 19
    {
        "id": 19,
        "title": "搜索旋转排序数组",
        "diff": "medium",
        "tags": ["二分"],
        "leetcode": 33,
        "origin": "https://leetcode.cn/problems/search-in-rotated-sorted-array/",
        "why": "数组虽被旋转，但「左半有序或右半有序」总有一半成立。二分时先判断哪半边有序，再看 target 是否落在有序的那半边，据此收缩区间，把 O(n) 降到 O(log n)。",
        "desc": """<p>整数数组 <code>nums</code> 原本是升序排列，在某个下标处旋转（例如 <code>[0,1,2,4,5,6,7]</code> 在下标 3 处旋转变成 <code>[4,5,6,7,0,1,2]</code>）。给定旋转后的数组和一个目标值 <code>target</code>，若数组中存在则返回下标，否则返回 <code>-1</code>。要求 O(log n)。</p>
<p><strong>示例：</strong><br><code>nums=[4,5,6,7,0,1,2], target=0</code> → <code>4</code></p>""",
        "frames": [
            frame("① L=0, M=3(nums=7), R=6：左半 [4,5,6,7] 有序", "drawBinarySearch", arr=[4, 5, 6, 7, 0, 1, 2], left=0, mid=3, right=6, width=560, height=140),
            frame("② target=0 不在左半 → L=M+1=4", "drawBinarySearch", arr=[4, 5, 6, 7, 0, 1, 2], left=4, mid=5, right=6, excludedRanges=[{"start": 0, "end": 3}], width=560, height=140),
            frame("③ 右半 [0,1,2] 有序，target=0 命中 M=4", "drawBinarySearch", arr=[4, 5, 6, 7, 0, 1, 2], left=4, mid=4, right=6, excludedRanges=[{"start": 0, "end": 3}], width=560, height=140),
        ],
        "conclusion": "每轮锁定「有序的那一半」判断 target 是否在内，在内则收敛到那一半，否则跳到另一半，循环往复。",
        "py": """def search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        if nums[l] <= nums[m]:          # 左半有序
            if nums[l] <= target < nums[m]:
                r = m - 1
            else:
                l = m + 1
        else:                           # 右半有序
            if nums[m] < target <= nums[r]:
                l = m + 1
            else:
                r = m - 1
    return -1""",
        "java": """public int search(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l <= r) {
        int m = (l + r) >>> 1;
        if (nums[m] == target) return m;
        if (nums[l] <= nums[m]) {
            if (nums[l] <= target && target < nums[m]) r = m - 1; else l = m + 1;
        } else {
            if (nums[m] < target && target <= nums[r]) l = m + 1; else r = m - 1;
        }
    }
    return -1;
}""",
        "time": "O(log n) — 每次二分砍掉一半",
        "space": "O(1)",
        "pitfalls": [
            ("判断有序用 nums[l] <= nums[m]", "必须带等号，处理只剩两个元素时 l==m 的情况"),
            ("target 区间判断要闭开", "左半用 nums[l] <= target < nums[m]，右半用 nums[m] < target <= nums[r]，边界不能搞混"),
        ],
        "selfcheck": [
            ("nums 完全没旋转（升序）怎么办？", "nums[l] <= nums[m] 恒成立，退化为标准二分，仍正确。"),
            ("target 不存在会返回什么？", "区间逐渐收缩到 l > r 退出循环，返回 -1。"),
        ],
    },
    # ---------------------------------------------------------------- 20
    {
        "id": 20,
        "title": "在排序数组中查找元素的第一个和最后一个位置",
        "diff": "medium",
        "tags": ["二分"],
        "leetcode": 34,
        "origin": "https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/",
        "why": "「第一个」和「最后一个」分别是两个不同的二分目标：找左边界时把命中也继续往左收敛，找右边界时继续往右收敛。两次二分各管一边，互不干扰。",
        "desc": """<p>给定一个<strong>非递减</strong>排列的整数数组 <code>nums</code> 和一个目标值 <code>target</code>，找出 target 在数组中的<strong>开始位置</strong>和<strong>结束位置</strong>。不存在则返回 <code>[-1, -1]</code>。要求 O(log n)。</p>
<p><strong>示例：</strong><br><code>nums=[5,7,7,8,8,10], target=8</code> → <code>[3,4]</code></p>""",
        "frames": [
            frame("① 找左边界：命中 8 也继续向左", "drawBinarySearch", arr=[5, 7, 7, 8, 8, 10], left=0, mid=3, right=5, width=560, height=140),
            frame("② 左边界收敛到下标 3", "drawBinarySearch", arr=[5, 7, 7, 8, 8, 10], left=0, mid=2, right=3, excludedRanges=[{"start": 4, "end": 5}], width=560, height=140),
            frame("③ 找右边界：命中 8 继续向右，收敛到 4", "drawBinarySearch", arr=[5, 7, 7, 8, 8, 10], left=3, mid=4, right=5, width=560, height=140),
        ],
        "conclusion": "左边界 = 第一个 >= target 的位置，右边界 = 最后一个 <= target 的位置，两次二分分别求得。",
        "py": """def searchRange(nums, target):
    def left_bound():
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] < target: l = m + 1
            else: r = m - 1
        return l
    def right_bound():
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] <= target: l = m + 1
            else: r = m - 1
        return r
    lo = left_bound()
    hi = right_bound()
    if lo <= hi:
        return [lo, hi]
    return [-1, -1]""",
        "java": """public int[] searchRange(int[] nums, int target) {
    int lo = left(nums, target), hi = right(nums, target);
    if (lo <= hi) return new int[]{lo, hi};
    return new int[]{-1, -1};
}
int left(int[] a, int t) {
    int l = 0, r = a.length - 1;
    while (l <= r) { int m = (l + r) >>> 1; if (a[m] < t) l = m + 1; else r = m - 1; }
    return l;
}
int right(int[] a, int t) {
    int l = 0, r = a.length - 1;
    while (l <= r) { int m = (l + r) >>> 1; if (a[m] <= t) l = m + 1; else r = m - 1; }
    return r;
}""",
        "time": "O(log n) — 两次独立二分",
        "space": "O(1)",
        "pitfalls": [
            ("左右边界写法不同", "左边界用 < 收缩，右边界用 <= 收缩，只差一个等号，写反会偏移一位"),
            ("结果校验", "左边界可能越界或 nums[lo] != target，需判断 lo <= hi 才返回，否则 [-1,-1]"),
        ],
        "selfcheck": [
            ("target 不存在时左右边界会怎样？", "左边界会指向「第一个大于 target」的位置，右边界指向「最后一个小于 target」的位置，此时 lo > hi，返回 [-1,-1]。"),
            ("数组里 target 只出现一次呢？", "左右边界会收敛到同一个下标，lo == hi，返回 [i, i]。"),
        ],
    },
    # ---------------------------------------------------------------- 21
    {
        "id": 21,
        "title": "搜索插入位置",
        "diff": "easy",
        "tags": ["二分"],
        "leetcode": 35,
        "origin": "https://leetcode.cn/problems/search-insert-position/",
        "why": "目标值不存在时要返回它「应该插入的位置」，这恰好就是「第一个 >= target 的下标」。标准二分的下界 l 最终就停在这里，天然给出答案。",
        "desc": """<p>给定一个排序数组和一个目标值，在数组中找到目标值并返回其索引；如果不存在，返回它按顺序插入的位置。</p>
<p><strong>示例：</strong><br><code>nums=[1,3,5,6], target=5</code> → <code>2</code><br><code>target=2</code> → <code>1</code>（应插在 1 和 3 之间）</p>""",
        "frames": [
            frame("① target=2：L=0, M=1(3), R=3，2 < 3 → R=M-1", "drawBinarySearch", arr=[1, 3, 5, 6], left=0, mid=1, right=3, width=520, height=140),
            frame("② L=0, M=0(1), R=0，1 < 2 → L=M+1=1", "drawBinarySearch", arr=[1, 3, 5, 6], left=0, mid=0, right=0, width=520, height=140),
            frame("③ 循环结束，L=1 即插入位置", "drawTwoPointers", arr=[1, 3, 5, 6], left=1, right=1, width=520, height=140),
        ],
        "conclusion": "二分结束后 l 就是「第一个 >= target」的位置——找到时是它本身，没找到时是插入点。",
        "py": """def searchInsert(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return l""",
        "java": """public int searchInsert(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l <= r) {
        int m = (l + r) >>> 1;
        if (nums[m] < target) l = m + 1; else r = m - 1;
    }
    return l;
}""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            ("返回 l 而不是 m", "m 是中间指针，循环结束时 l 才是最终下界；返回 m 会得到中间值"),
            ("target 比所有元素都大", "l 一路右移，最终等于 len(nums)，正好是末尾插入位置"),
        ],
        "selfcheck": [
            ("target 比所有元素都小呢？", "r 一路左移到 -1，l 保持 0，返回 0，插到最前面。"),
            ("为什么不用「先找等于、找不到再线性找插入点」？", "那样最坏 O(n)；二分下界 l 本身就是插入点，一次二分 O(log n) 搞定。"),
        ],
    },
    # ---------------------------------------------------------------- 22
    {
        "id": 22,
        "title": "组合总和",
        "diff": "medium",
        "tags": ["回溯"],
        "leetcode": 39,
        "origin": "https://leetcode.cn/problems/combination-sum/",
        "why": "每个数可以无限次使用，本质是「无限背包」式的搜索树。回溯时用一个 start 下标保证「不重复组合」（只从当前及之后的数选），再用剩余和剪枝，及时砍掉超出的分支。",
        "desc": """<p>给定<strong>无重复元素</strong>的数组 <code>candidates</code> 和目标数 <code>target</code>，找出所有和为 target 的组合。<code>candidates</code> 中的数字可以<strong>无限制重复</strong>选取，且解集不能包含重复组合。</p>
<p><strong>示例：</strong><br><code>candidates=[2,3,6,7], target=7</code> → <code>[[2,2,3],[7]]</code></p>""",
        "frames": [
            frame("① 搜索树：从当前下标往后选，和为 target 就收集", "drawBacktrack",
                  nodes=[{"val": "[]", "x": 300, "y": 15, "color": "normal"},
                         {"val": "[2]", "x": 170, "y": 80, "color": "path"},
                         {"val": "[2,2]", "x": 80, "y": 150, "color": "path"},
                         {"val": "[2,2,3]", "x": 60, "y": 225, "color": "path"},
                         {"val": "[7]", "x": 470, "y": 150, "color": "path"},
                         {"val": "[2,2,2,2]", "x": 200, "y": 225, "color": "pruned"}],
                  edges=[{"x1": 300, "y1": 15, "x2": 170, "y2": 80, "color": "path"},
                         {"x1": 170, "y1": 80, "x2": 80, "y2": 150, "color": "path"},
                         {"x1": 80, "y1": 150, "x2": 60, "y2": 225, "color": "path"},
                         {"x1": 80, "y1": 150, "x2": 200, "y2": 225, "color": "pruned"},
                         {"x1": 300, "y1": 15, "x2": 470, "y2": 150, "color": "path"}],
                  width=560, height=260),
            frame("② 剪枝：剩余和 < 当前数，就不再往下搜", "drawBacktrack",
                  nodes=[{"val": "rest=4", "x": 300, "y": 20, "color": "normal"},
                         {"val": "选 6 (rest=-2) ✗", "x": 480, "y": 100, "color": "pruned"},
                         {"val": "选 3 (rest=1)", "x": 200, "y": 100, "color": "path"},
                         {"val": "选 1 ✗", "x": 100, "y": 180, "color": "pruned"}],
                  edges=[{"x1": 300, "y1": 20, "x2": 480, "y2": 100, "color": "pruned"},
                         {"x1": 300, "y1": 20, "x2": 200, "y2": 100, "color": "path"},
                         {"x1": 200, "y1": 100, "x2": 100, "y2": 180, "color": "pruned"}],
                  width=560, height=220),
        ],
        "conclusion": "「从当前下标往后选」保证组合不重复；「剩余和不足即剪枝」把指数级搜索大幅收窄。",
        "py": """def combinationSum(candidates, target):
    candidates.sort()          # 排序后便于剪枝
    ans = []
    def dfs(start, path, rest):
        if rest == 0:
            ans.append(path[:]); return
        for i in range(start, len(candidates)):
            if candidates[i] > rest:   # 已排序，后面更大，剪枝
                break
            path.append(candidates[i])
            dfs(i, path, rest - candidates[i])   # 可重复，i 不 +1
            path.pop()
    dfs(0, [], target)
    return ans""",
        "java": """public List<List<Integer>> combinationSum(int[] candidates, int target) {
    Arrays.sort(candidates);
    List<List<Integer>> ans = new ArrayList<>();
    dfs(candidates, target, 0, new ArrayList<>(), ans);
    return ans;
}
void dfs(int[] c, int rest, int start, List<Integer> path, List<List<Integer>> ans) {
    if (rest == 0) { ans.add(new ArrayList<>(path)); return; }
    for (int i = start; i < c.length; i++) {
        if (c[i] > rest) break;
        path.add(c[i]);
        dfs(c, rest - c[i], i, path, ans);
        path.remove(path.size() - 1);
    }
}""",
        "time": "O(n^(t/min)) — 组合数级别，t 为 target，min 为最小候选",
        "space": "O(target/min) — 递归深度",
        "pitfalls": [
            ("去重靠 start 下标", "递归传 i 而不是 i+1 表示可重复；若从 0 开始会生成重复组合"),
            ("回溯恢复现场", "path.append 后必须 path.pop()，否则路径串到别的分支"),
            ("先排序再剪枝", "不排序无法用 break 提前终止"),
        ],
        "selfcheck": [
            ("candidates=[2,3,6,7], target=7 的两个答案怎么来的？", "[2,2,3] 来自一路选 2 再选 3；[7] 来自直接选 7。选 [2,3,2] 这类重复顺序被 start 下标挡掉了。"),
            ("为什么这题不像「无重复组合」那样纠结顺序？", "start 下标保证只往「当前及之后」选，组合内部天然有序，顺序不同不会重复出现。"),
        ],
    },
    # ---------------------------------------------------------------- 23
    {
        "id": 23,
        "title": "缺失的第一个正数",
        "diff": "hard",
        "tags": ["哈希表"],
        "leetcode": 41,
        "origin": "https://leetcode.cn/problems/first-missing-positive/",
        "why": "答案一定落在 [1, n+1]（n 为数组长度）。用「原地哈希」把每个正数 x 放到下标 x-1 处，一趟交换后，第一个「下标 i 上不是 i+1」的位置就是答案，O(n) 时间 + O(1) 空间。",
        "desc": """<p>给定一个未排序的整数数组，找出其中<strong>没有出现的最小的正整数</strong>。要求时间复杂度 O(n) 且只用常数级额外空间。</p>
<p><strong>示例：</strong><br><code>[1,2,0] → 3</code>；<code>[3,4,-1,1] → 2</code>；<code>[7,8,9,11,12] → 1</code></p>""",
        "frames": [
            frame("① 目标：把正数 x 放到下标 x-1（原地哈希）", "drawTable",
                  headers=["下标", "0", "1", "2", "3"],
                  rows=[["原数组", "3", "4", "-1", "1"], ["应放", "1", "-", "3", "4"]], width=520, height=140),
            frame("② 交换：3 与 nums[2] 换、4 与 nums[3] 换、1 与 nums[0] 换", "drawTable",
                  headers=["下标", "0", "1", "2", "3"],
                  rows=[["归位后", {"val": "1", "highlight": True}, "-1", "3", "4"]], width=520, height=120),
            frame("③ 第一个 nums[i] != i+1 的位置 i=1 → 缺失 2", "drawTwoPointers", arr=[1, -1, 3, 4], left=1, right=1, width=520, height=140),
        ],
        "conclusion": "把每个 [1,n] 内的数送回「自己该在的位置」，再扫一遍看谁没归位，那个位置 +1 就是答案。",
        "py": """def firstMissingPositive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1""",
        "java": """public int firstMissingPositive(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
            int j = nums[i] - 1, t = nums[i]; nums[i] = nums[j]; nums[j] = t;
        }
    }
    for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;
    return n + 1;
}""",
        "time": "O(n) — 每个数最多被交换一次到正确位置",
        "space": "O(1) — 原地",
        "pitfalls": [
            ("用 while 不是 if", "交换后当前位置可能又来了一个该归位的数，必须继续换，if 只换一次会漏"),
            ("交换条件要防死循环", "nums[nums[i]-1] != nums[i] 避免两个相等值反复换"),
            ("忽略越界的数", "负数、0、大于 n 的数不参与归位，直接跳过"),
        ],
        "selfcheck": [
            ("为什么答案上界是 n+1？", "[1,n] 一共 n 个坑，若 1..n 全都出现，缺失的最小正数只能是 n+1。"),
            ("[3,4,-1,1] 归位过程？", "i=0 时 3 与 nums[2]=-1 换；继续 while，nums[0]=-1 越界跳过；i=3 时 1 与 nums[0] 换 → [1,-1,3,4]，再扫到 i=1 的 -1，返回 2。"),
        ],
    },
    # ---------------------------------------------------------------- 24
    {
        "id": 24,
        "title": "接雨水",
        "diff": "hard",
        "tags": ["双指针"],
        "leetcode": 42,
        "origin": "https://leetcode.cn/problems/trapping-rain-water/",
        "why": "每根柱子上能接多少水，由「左右两边最高柱子中的较矮者」决定。用左右双指针维护 leftMax / rightMax，谁小就结算谁，一次遍历 O(n)，无需提前建两个数组。",
        "desc": """<p>给定 <code>n</code> 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。</p>
<p><strong>示例：</strong><br><code>height=[0,1,0,2,1,0,1,3,2,1,2,1]</code> → <code>6</code></p>""",
        "frames": [
            frame("① 左指针在 0，右指针在末尾，维护 leftMax/rightMax", "drawTwoPointers", arr=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], left=0, right=11, width=720, height=140),
            frame("② leftMax < rightMax 时结算左指针，并右移", "drawTwoPointers", arr=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], left=4, right=11, window={"start": 2, "end": 3}, width=720, height=140),
            frame("③ 直到两指针相遇，累计雨水 = 6", "drawTwoPointers", arr=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], left=7, right=7, width=720, height=140),
        ],
        "conclusion": "每步只结算「较矮那侧」的柱子：它能接的水 = 该侧当前最高 - 自身高度，指针向中间推进直到相遇。",
        "py": """def trap(height):
    l, r = 0, len(height) - 1
    left_max = right_max = 0
    ans = 0
    while l < r:
        left_max = max(left_max, height[l])
        right_max = max(right_max, height[r])
        if left_max < right_max:
            ans += left_max - height[l]
            l += 1
        else:
            ans += right_max - height[r]
            r -= 1
    return ans""",
        "java": """public int trap(int[] height) {
    int l = 0, r = height.length - 1, leftMax = 0, rightMax = 0, ans = 0;
    while (l < r) {
        leftMax = Math.max(leftMax, height[l]);
        rightMax = Math.max(rightMax, height[r]);
        if (leftMax < rightMax) { ans += leftMax - height[l]; l++; }
        else                    { ans += rightMax - height[r]; r--; }
    }
    return ans;
}""",
        "time": "O(n) — 每个柱子访问一次",
        "space": "O(1)",
        "pitfalls": [
            ("结算哪一侧", "leftMax < rightMax 时，左柱的水量由 leftMax 决定，与更远的右墙无关——这是双指针正确的关键"),
            ("先更新 max 再结算", "height[l] 可能比 leftMax 高，此时 leftMax - height[l] = 0，不会减出负数"),
        ],
        "selfcheck": [
            ("为什么 leftMax < rightMax 时可以直接结算左柱？", "因为右边一定存在一根 >= rightMax > leftMax 的墙，左柱的水只受 leftMax 限制，右墙具体多高不再重要。"),
            ("单调递增的数组能接水吗？", "不能。leftMax 永远 <= 右侧，每次 leftMax-height[l] 在更新后都为 0，答案为 0。"),
        ],
    },
    # ---------------------------------------------------------------- 25
    {
        "id": 25,
        "title": "跳跃游戏 II",
        "diff": "medium",
        "tags": ["贪心"],
        "leetcode": 45,
        "origin": "https://leetcode.cn/problems/jump-game-ii/",
        "why": "求最少步数，贪心思路是「每走一步都尽量覆盖最远」。维护当前步能覆盖的边界 end，走到边界就 +1 步并更新下一跳的最远边界，保证步数最少。",
        "desc": """<p>给定一个非负整数数组 <code>nums</code>，最初位于数组第一个下标。数组中的每个元素代表你在该位置可以跳跃的最大长度。求到达最后一个下标的最少跳跃次数。保证可达。</p>
<p><strong>示例：</strong><br><code>nums=[2,3,1,1,4]</code> → <code>2</code>（0→1→4）</p>""",
        "frames": [
            frame("① 从 0 跳：最远可达 2，end=2", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=0, right=2, width=520, height=140),
            frame("② 走到边界 end=2 时，步数 +1，新最远 = max(1+2, 2+1)=4", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=2, right=4, width=520, height=140),
            frame("③ 最远已覆盖末尾，共 2 步", "drawTwoPointers", arr=[2, 3, 1, 1, 4], left=4, right=4, window={"start": 1, "end": 4}, width=520, height=140),
        ],
        "conclusion": "把「当前位置能到的最远」不断更新，每当走到本步边界就记一步并切换到新的最远边界。",
        "py": """def jump(nums):
    n = len(nums)
    steps = end = farthest = 0
    for i in range(n - 1):       # 最后一位不用跳
        farthest = max(farthest, i + nums[i])
        if i == end:
            steps += 1
            end = farthest
    return steps""",
        "java": """public int jump(int[] nums) {
    int steps = 0, end = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        if (i == end) { steps++; end = farthest; }
    }
    return steps;
}""",
        "time": "O(n) — 一次遍历",
        "space": "O(1)",
        "pitfalls": [
            ("循环到 n-2 即可", "最后一个位置不需要再起跳，遍历到 n-1 可能多算一步"),
            ("i == end 才加步数", "走到当前覆盖边界才确认必须再跳一次，提前加会算多"),
        ],
        "selfcheck": [
            ("为什么这是最优步数？", "每步的边界 end 都是「这一步能覆盖的最远范围」，在边界处切换 = 用最少步数换最大覆盖，贪心即最优。"),
            ("nums=[0] 呢？", "n=1，循环不执行，返回 0，已经在终点。"),
        ],
    },
]

from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① 数据栈与辅助栈同步", "drawStack", items=[{"val": "-2"}, {"val": "0"}, {"val": "-3"}], type="stack", height=180),
    frame("② 辅助栈存「到当前为止的最小值」", "drawStack", items=[{"val": "-2"}, {"val": "-2"}, {"val": "-3"}], type="stack", height=180),
    frame("③ pop 后辅助栈同步弹出，getMin = -2", "drawStack", items=[{"val": "-2"}, {"val": "-2"}], type="stack", height=150),
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
    "pitfalls": [["pop 同步", "数据栈与辅助栈必须同时 pop，否则 getMin 错位"], ["push 的 min 判断", "辅助栈为空时直接入栈，否则取 min(val, 当前最小)"]],
    "selfcheck": [["重复的最小值怎么处理？", "每次都入栈，即使相等也入，保证栈深一致、弹出对位。"], ["能省空间吗？", "可以只在新最小值 <= 当前最小才入辅助栈，弹出时相等才弹出，但实现稍复杂。"]],
}

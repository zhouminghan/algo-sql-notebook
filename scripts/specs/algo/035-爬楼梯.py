from scripts.algo_gen import frame

PROBLEM = {
    "id": 35,
    "title": "爬楼梯",
    "diff": "easy",
    "tags": ["DP"],
    "leetcode": 70,
    "origin": "https://leetcode.cn/problems/climbing-stairs/",
    "why": "到第 n 阶，最后一步要么跨 1 阶、要么跨 2 阶，所以 f(n) = f(n-1) + f(n-2)，就是斐波那契数列。用两个变量滚动即可 O(1) 空间。",
    "desc": """<p>假设你正在爬楼梯，需要 n 阶到达楼顶。每次可以爬 1 或 2 个台阶，问有多少种不同方法爬到楼顶。</p>
<p><strong>示例：</strong><br><code>n=2</code> → <code>2</code>（1+1、2）；<code>n=3</code> → <code>3</code>（1+1+1、1+2、2+1）</p>""",
    "frames": [
    frame("① 递推：f(n)=f(n-1)+f(n-2)", "drawTable", headers=["n", "0", "1", "2", "3", "4", "5"], rows=[["方法数", "1", "1", "2", "3", "5", "8"]], width=560, height=120),
    frame("② 第 n 阶来自「跨 1」或「跨 2」两种来路", "drawBacktrack", nodes=[{"val": "n", "x": 300, "y": 15, "color": "normal"}, {"val": "n-1", "x": 200, "y": 90, "color": "path"}, {"val": "n-2", "x": 400, "y": 90, "color": "path"}], edges=[{"x1": 300, "y1": 15, "x2": 200, "y2": 90, "color": "path"}, {"x1": 300, "y1": 15, "x2": 400, "y2": 90, "color": "path"}], width=520, height=150),
    ],
    "conclusion": "斐波那契数列，滚动两个变量不断前移。",
    "py": """def climbStairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a""",
    "java": """public int climbStairs(int n) {
    int a = 1, b = 1;
    for (int i = 0; i < n; i++) {
        int t = a + b;
        a = b; b = t;
    }
    return a;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["边界 f(0)=1", "把 f(0) 定义为 1 能让递推统一，n=1 返回 1"], ["别用朴素递归", "朴素递归是指数级；记忆化或迭代才是线性"]],
    "selfcheck": [["n=0 或 n=1？", "约定 f(0)=1、f(1)=1，代码里 a 初始 1 直接覆盖。"], ["如果一次能爬 1~3 阶呢？", "递推改为 f(n)=f(n-1)+f(n-2)+f(n-3)，滚动维护三个变量即可。"]],
}

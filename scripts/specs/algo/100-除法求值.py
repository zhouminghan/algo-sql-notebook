from scripts.algo_gen import frame

PROBLEM = {
    "id": 100,
    "title": "除法求值",
    "diff": "medium",
    "tags": ["图"],
    "leetcode": 399,
    "origin": "https://leetcode.cn/problems/evaluate-division/",
    "why": "把每个变量看成图节点，a/b=2 既是 a→b 权 2、又是 b→a 权 1/2。查询 a/c 就是图上 a 到 c 的路径权值之积，用 BFS/DFS 求路径。",
    "desc": """<p>给定变量对数组 <code>equations</code> 和实数值数组 <code>values</code>，其中 equations[i]=[A,B] 表示 A/B=values[i]。再给定查询 queries，返回每个查询的结果，无法确定则 -1。</p>
<p><strong>示例：</strong><br><code>[["a","b"],["b","c"]], values=[2,3], queries=[["a","c"],["b","a"]]</code> → <code>[6.0, 0.5]</code></p>""",
    "frames": [
    frame("① 建图：a→b 权 2，b→a 权 1/2", "drawGraph", vertices=[{"label": "a", "x": 100, "y": 150, "color": "active"}, {"label": "b", "x": 300, "y": 150, "color": "visited"}, {"label": "c", "x": 500, "y": 150, "color": "unvisited"}], edges=[{"from": "a", "to": "b", "weight": "2"}, {"from": "b", "to": "c", "weight": "3"}], width=600, height=220),
    frame("② a/c = a→b→c 权值相乘 = 2×3=6", "drawTable", headers=["查询", "路径", "结果"], rows=[["a/c", "a→b→c", "2×3=6"], ["b/a", "b→a", "1/2=0.5"]], width=460, height=140),
    ],
    "conclusion": "除法关系组成带权无向图，查询就是两点间路径权值乘积。",
    "py": """from collections import defaultdict, deque
def calcEquation(equations, values, queries):
    g = defaultdict(dict)
    for (a, b), v in zip(equations, values):
        g[a][b] = v
        g[b][a] = 1 / v
    def bfs(s, t):
        if s not in g or t not in g:
            return -1.0
        q = deque([(s, 1.0)])
        seen = {s}
        while q:
            node, val = q.popleft()
            if node == t:
                return val
            for nxt, w in g[node].items():
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, val * w))
        return -1.0
    return [bfs(s, t) for s, t in queries]""",
    "java": """public double[] calcEquation(List<List<String>> eq, double[] vals, List<List<String>> qs) {
    Map<String, Map<String, Double>> g = new HashMap<>();
    for (int i = 0; i < eq.size(); i++) {
        String a = eq.get(i).get(0), b = eq.get(i).get(1);
        g.computeIfAbsent(a, k -> new HashMap<>()).put(b, vals[i]);
        g.computeIfAbsent(b, k -> new HashMap<>()).put(a, 1 / vals[i]);
    }
    double[] ans = new double[qs.size()];
    for (int i = 0; i < qs.size(); i++)
        ans[i] = bfs(g, qs.get(i).get(0), qs.get(i).get(1));
    return ans;
}
double bfs(Map<String, Map<String, Double>> g, String s, String t) {
    if (!g.containsKey(s) || !g.containsKey(t)) return -1.0;
    Queue<Object[]> q = new LinkedList<>();
    Set<String> seen = new HashSet<>();
    q.offer(new Object[]{s, 1.0}); seen.add(s);
    while (!q.isEmpty()) {
        Object[] cur = q.poll();
        String node = (String) cur[0]; double val = (Double) cur[1];
        if (node.equals(t)) return val;
        for (Map.Entry<String, Double> e : g.get(node).entrySet())
            if (seen.add(e.getKey())) q.offer(new Object[]{e.getKey(), val * e.getValue()});
    }
    return -1.0;
}""",
    "time": "O(q · (V+E)) — 每个查询一次 BFS",
    "space": "O(V+E)",
    "pitfalls": [["反向边取倒数", "a/b=v 必须同时建 b/a=1/v，否则单向不连通"], ["未知变量返回 -1", "查询端点不在图中直接 -1.0"]],
    "selfcheck": [["Floyd 预处理？", "可以预计算所有点对最短路（这里是权值积），把每个查询降到 O(1)。"], ["结果精度？", "浮点除法有精度误差，题目用容差判断，返回 double 即可。"]],
}

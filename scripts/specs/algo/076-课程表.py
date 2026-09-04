from scripts.algo_gen import frame

PROBLEM = {
    "id": 76,
    "title": "课程表",
    "diff": "medium",
    "tags": ["拓扑排序"],
    "leetcode": 207,
    "origin": "https://leetcode.cn/problems/course-schedule/",
    "why": "课程依赖构成有向图，能否修完 = 图是否无环（可拓扑排序）。Kahn 算法：统计入度，把入度为 0 的课入队，依次出队并把后续课入度减一；若最终修完所有课则无环。",
    "desc": """<p>你需要修 <code>numCourses</code> 门课。先修课程 <code>prerequisites[i] = [a, b]</code> 表示修 a 前必须先修 b。判断是否可能完成所有课程。</p>
<p><strong>示例：</strong><br><code>numCourses=2, [[1,0]]</code> → <code>true</code>；<code>[[1,0],[0,1]]</code> → <code>false</code>（互相依赖成环）</p>""",
    "frames": [
    frame("① 建图并统计入度", "drawTable", headers=["课程", "先修", "入度"], rows=[["0", "无", "0"], ["1", "0", "1"], ["2", "0, 1", "2"]], width=460, height=160),
    frame("② 入度 0 的课入队，出队后把后续课入度 -1", "drawStack", items=[{"val": "0"}], type="queue", height=130),
    frame("③ 修完的课数 == 总数则无环可完成", "drawTable", headers=["课程", "2, 0", "1, 1"], rows=[["已修数", "0", "1", "2"]], width=420, height=120),
    ],
    "conclusion": "拓扑排序能排完全部课程 = 无环 = 可完成。",
    "py": """from collections import deque
def canFinish(numCourses, prerequisites):
    indeg = [0] * numCourses
    graph = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    count = 0
    while q:
        cur = q.popleft()
        count += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return count == numCourses""",
    "java": """public boolean canFinish(int n, int[][] prerequisites) {
    int[] indeg = new int[n];
    List<List<Integer>> g = new ArrayList<>();
    for (int i = 0; i < n; i++) g.add(new ArrayList<>());
    for (int[] p : prerequisites) { g.get(p[1]).add(p[0]); indeg[p[0]]++; }
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i);
    int count = 0;
    while (!q.isEmpty()) {
        int cur = q.poll(); count++;
        for (int nxt : g.get(cur)) if (--indeg[nxt] == 0) q.offer(nxt);
    }
    return count == n;
}""",
    "time": "O(V + E)",
    "space": "O(V + E) — 邻接表",
    "pitfalls": [["边方向", "先修 b → 后修 a，建图方向是 b 指向 a，入度记在 a 上"], ["成环判定", "最终 count < n 说明有环，返回 false"]],
    "selfcheck": [["为什么拓扑排序能判环？", "无环图才能把所有入度逐步减到 0 并全部出队；有环的节点入度永远降不到 0。"], ["DFS 判环做法？", "三色标记：0 未访问、1 访问中、2 已完成，DFS 遇到「访问中」的节点即发现环。"]],
}

from scripts.algo_gen import frame

PROBLEM = {
    "id": 27,
    "title": "旋转图像",
    "diff": "medium",
    "tags": ["数组"],
    "leetcode": 48,
    "origin": "https://leetcode.cn/problems/rotate-image/",
    "why": "顺时针旋转 90° 可以拆成两个简单操作：先沿主对角线翻转，再左右翻转。每步都有明确的坐标对应关系，原地完成，不需要额外矩阵。",
    "desc": """<p>给定一个 <code>n × n</code> 的二维矩阵表示图像，将其<strong>原地</strong>顺时针旋转 90 度。</p>
<p><strong>示例：</strong><br><code>[[1,2,3],[4,5,6],[7,8,9]]</code> → <code>[[7,4,1],[8,5,2],[9,6,3]]</code></p>""",
    "frames": [
    frame("① 原矩阵", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "1", "2", "3"], ["1", "4", "5", "6"], ["2", "7", "8", "9"]], width=420, height=170),
    frame("② 沿主对角线翻转（matrix[i][j] ↔ matrix[j][i]）", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "1", "4", "7"], ["1", {"val": "2", "highlight": True}, "5", "8"], ["2", {"val": "3", "highlight": True}, "6", "9"]], width=420, height=170),
    frame("③ 左右翻转 → 旋转结果", "drawTable", headers=["", "0", "1", "2"], rows=[["0", "7", "4", "1"], ["1", "8", "5", "2"], ["2", "9", "6", "3"]], width=420, height=170),
    ],
    "conclusion": "先对角线翻转，再左右翻转，两步叠加正好等于顺时针 90°。",
    "py": """def rotate(matrix):
    n = len(matrix)
    for i in range(n):              # 主对角线翻转
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for i in range(n):              # 左右翻转
        matrix[i].reverse()""",
    "java": """public void rotate(int[][] matrix) {
    int n = matrix.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int t = matrix[i][j]; matrix[i][j] = matrix[j][i]; matrix[j][i] = t;
        }
    for (int i = 0; i < n; i++) {
        int l = 0, r = n - 1;
        while (l < r) { int t = matrix[i][l]; matrix[i][l] = matrix[i][r]; matrix[i][r] = t; l++; r--; }
    }
}""",
    "time": "O(n²) — 每个元素处理常数次",
    "space": "O(1) — 原地",
    "pitfalls": [["对角线翻转只遍历上三角", "j 从 i+1 开始，否则交换两次等于没换"], ["逆时针要换顺序", "逆时针 90° 是先左右翻转再对角线翻转，方向别弄反"]],
    "selfcheck": [["为什么两步叠加等于旋转 90°？", "对角线翻转把 (i,j) 映到 (j,i)，左右翻转再把列镜像为 n-1-j，最终 (i,j)→(j,n-1-i)，正是顺时针 90° 的坐标变换。"], ["能否一次循环直接旋转？", "可以，按「一圈一圈」处理四个角的值循环交换，但两步分解更直观、不易错。"]],
}

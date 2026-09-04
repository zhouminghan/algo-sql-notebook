from scripts.algo_gen import frame

PROBLEM = {
    "id": 86,
    "title": "搜索二维矩阵 II",
    "diff": "medium",
    "tags": ["二分"],
    "leetcode": 240,
    "origin": "https://leetcode.cn/problems/search-a-2d-matrix-ii/",
    "why": "矩阵每行每列都升序。从左下角出发：比 target 小就向右，比 target 大就向上，每次排除一行或一列，O(m+n) 即可，无需二分。",
    "desc": """<p>编写一个高效算法，搜索 m×n 矩阵中的目标值。矩阵每行从左到右升序、每列从上到下升序。</p>
<p><strong>示例：</strong><br><code>[[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target=5</code> → <code>true</code></p>""",
    "frames": [
    frame("① 从左下角出发", "drawTable", headers=["", "0", "1", "2", "3", "4"], rows=[["0", "1", "4", "7", "11", "15"], ["1", "2", "5", "8", "12", "19"], ["2", "3", "6", "9", "16", "22"], ["3", "10", "13", "14", "17", "24"], ["4", "18", "21", "23", "26", "30"]], width=500, height=220),
    frame("② 比 target 小向右，比 target 大向上", "drawTable", headers=["", "0", "1", "2", "3", "4"], rows=[["0", "1", "4", "7", "11", "15"], ["1", "2", {"val": "5", "highlight": True}, "8", "12", "19"], ["2", "3", "6", "9", "16", "22"], ["3", "10", "13", "14", "17", "24"], ["4", "18", "21", "23", "26", "30"]], width=500, height=220),
    ],
    "conclusion": "左下角是「行最小、列最大」的分水岭，每次都能确定性地排除一行或一列。",
    "py": """def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    i, j = m - 1, 0
    while i >= 0 and j < n:
        if matrix[i][j] == target:
            return True
        if matrix[i][j] < target:
            j += 1        # 向右
        else:
            i -= 1        # 向上
    return False""",
    "java": """public boolean searchMatrix(int[][] matrix, int target) {
    int i = matrix.length - 1, j = 0;
    while (i >= 0 && j < matrix[0].length) {
        if (matrix[i][j] == target) return true;
        if (matrix[i][j] < target) j++; else i--;
    }
    return false;
}""",
    "time": "O(m + n)",
    "space": "O(1)",
    "pitfalls": [["从左下角出发", "左上角两个方向都更大，无法决策；左下角一清二楚"], ["移动方向", "小→右，大→上，不要反"]],
    "selfcheck": [["为什么不能整体二分？", "矩阵整体并非有序（行尾不一定小于下行首），只有行内和列内有序，所以用「Z 字形」排除法。"], ["右上角出发行吗？", "可以，对称：比 target 小向下、比 target 大向左。"]],
}

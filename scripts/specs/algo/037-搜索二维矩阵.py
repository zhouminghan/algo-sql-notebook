from scripts.algo_gen import frame

PROBLEM = {
    "id": 37,
    "title": "搜索二维矩阵",
    "diff": "medium",
    "tags": ["二分"],
    "leetcode": 74,
    "origin": "https://leetcode.cn/problems/search-a-2d-matrix/",
    "why": "矩阵每行升序且下一行首元素大于上一行末元素，把它「拍平」就是一个整体有序数组，直接对总长度做二分，下标换算成 (row, col)。",
    "desc": """<p>编写一个高效算法，判断 m×n 矩阵中是否存在目标值。矩阵特性：每行从左到右升序，且每行的第一个整数大于前一行的最后一个整数。</p>
<p><strong>示例：</strong><br><code>[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3</code> → <code>true</code></p>""",
    "frames": [
    frame("① 拍平成有序数组 [1,3,5,7,10,11,16,20,23,30,34,60]", "drawTable", headers=["", "0", "1", "2", "3"], rows=[["0", "1", "3", "5", "7"], ["1", "10", "11", "16", "20"], ["2", "23", "30", "34", "60"]], width=420, height=170),
    frame("② 整体二分，mid 换算成 (mid//n, mid%n)", "drawBinarySearch", arr=[1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60], left=0, mid=5, right=11, width=720, height=140),
    ],
    "conclusion": "把二维坐标映射到一维下标，标准二分直接复用。",
    "py": """def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    l, r = 0, m * n - 1
    while l <= r:
        mid = (l + r) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        if val < target:
            l = mid + 1
        else:
            r = mid - 1
    return False""",
    "java": """public boolean searchMatrix(int[][] matrix, int target) {
    int m = matrix.length, n = matrix[0].length;
    int l = 0, r = m * n - 1;
    while (l <= r) {
        int mid = (l + r) >>> 1;
        int val = matrix[mid / n][mid % n];
        if (val == target) return true;
        if (val < target) l = mid + 1; else r = mid - 1;
    }
    return false;
}""",
    "time": "O(log(m·n))",
    "space": "O(1)",
    "pitfalls": [["下标换算", "row = mid // n，col = mid % n，行列别写反"], ["前提是整体有序", "本题特殊性质保证拍平有序；普通「每行每列升序」的矩阵要用不同的搜索方式（见搜索二维矩阵 II）"]],
    "selfcheck": [["target 比所有元素都大/小？", "二分区间自然收缩到 l > r，返回 False。"], ["m=1 时？", "退化为普通一维二分，mid//n=0 恒成立。"]],
}

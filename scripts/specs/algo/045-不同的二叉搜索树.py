from scripts.algo_gen import frame

PROBLEM = {
    "id": 45,
    "title": "不同的二叉搜索树",
    "diff": "medium",
    "tags": ["树"],
    "leetcode": 96,
    "origin": "https://leetcode.cn/problems/unique-binary-search-trees/",
    "why": "以 i 为根时，左子树有 i-1 个节点、右子树有 n-i 个节点，数量相乘再对 i 求和，即卡特兰数递推：G(n)=Σ G(i-1)·G(n-i)。",
    "desc": """<p>给定整数 n，求由 n 个节点组成且节点值从 1 到 n 互不相同的<strong>二叉搜索树</strong>有多少种。</p>
<p><strong>示例：</strong><br><code>n=3</code> → <code>5</code></p>""",
    "frames": [
    frame("① 以 i 为根：左子树 G(i-1) 种 × 右子树 G(n-i) 种", "drawTable", headers=["根", "左子树", "右子树", "组合数"], rows=[["1", "G(0)", "G(2)", "1×2=2"], ["2", "G(1)", "G(1)", "1×1=1"], ["3", "G(2)", "G(0)", "2×1=2"]], width=500, height=170),
    frame("② 卡特兰数：G(0)=1, G(1)=1, G(2)=2, G(3)=5", "drawTable", headers=["n", "0", "1", "2", "3", "4"], rows=[["G(n)", "1", "1", "2", "5", "14"]], width=520, height=110),
    ],
    "conclusion": "枚举根节点，左右子树数量相乘累加，DP 递推得到卡特兰数。",
    "py": """def numTrees(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j - 1] * dp[i - j]
    return dp[n]""",
    "java": """public int numTrees(int n) {
    int[] dp = new int[n + 1];
    dp[0] = dp[1] = 1;
    for (int i = 2; i <= n; i++)
        for (int j = 1; j <= i; j++)
            dp[i] += dp[j - 1] * dp[i - j];
    return dp[n];
}""",
    "time": "O(n²)",
    "space": "O(n)",
    "pitfalls": [["G(0)=1", "空树算一种，边界定义成 1 递推才成立"], ["累加不是相乘整体", "每个根 j 贡献 dp[j-1]*dp[i-j]，要累加所有 j"]],
    "selfcheck": [["n=2 为什么是 2？", "以 1 为根：右子树 G(1)=1；以 2 为根：左子树 G(1)=1；合计 2。"], ["这题与「生成所有 BST」区别？", "本题只数个数（DP/卡特兰数）；生成所有 BST 需要递归构造左右子树并组合。"]],
}

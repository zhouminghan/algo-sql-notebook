from scripts.algo_gen import frame

PROBLEM = {
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
    frame("① XOR：a⊕a=0，成对相消", "drawTable", headers=["数", "二进制", "⊕ 结果"], rows=[["初始", "0", "0"], ["2", "10", "10"], ["2", "10", "0"], ["1", "01", "01"]], width=460, height=190),
    frame("② [4,1,2,1,2] 全部异或 = 4", "drawTable", headers=["步骤", "⊕ 当前", "累计"], rows=[["4", "100", "100"], ["1", "001", "101"], ["2", "010", "111"], ["1", "001", "110"], ["2", "010", "100=4"]], width=460, height=220),
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
    "pitfalls": [["初始化为 0", "0⊕x=x，初始化 0 不影响结果"], ["XOR 性质", "成对元素必抵消，顺序无关，交换律结合律保证"]],
    "selfcheck": [["为什么 XOR 天然适用？", "相同数异或为 0，且异或满足交换结合律，遍历顺序无所谓，成对项全部归零。"], ["有三个数只出现一次呢？", "那是「只出现一次的数字 III / 数组」变体，需要分组或按位统计，单靠整体 XOR 不够。"]],
}

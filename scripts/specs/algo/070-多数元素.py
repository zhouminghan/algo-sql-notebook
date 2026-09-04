from scripts.algo_gen import frame

PROBLEM = {
    "id": 70,
    "title": "多数元素",
    "diff": "easy",
    "tags": ["投票"],
    "leetcode": 169,
    "origin": "https://leetcode.cn/problems/majority-element/",
    "why": "Boyer-Moore 投票：维护候选人和计数。遇到相同数 +1、不同数 -1，计数归零就换候选人。多数元素出现次数超过一半，最终幸存者必是它。",
    "desc": """<p>给定大小为 n 的数组，返回其中的<strong>多数元素</strong>。多数元素指在数组中出现次数<strong>大于 ⌊n/2⌋</strong> 的元素。保证一定存在。</p>
<p><strong>示例：</strong><br><code>[2,2,1,1,1,2,2]</code> → <code>2</code></p>""",
    "frames": [
    frame("① 候选人 cand，计数 count：相同 +1、不同 -1", "drawTable", headers=["步骤", "元素", "cand", "count"], rows=[["1", "2", "2", "1"], ["2", "2", "2", "2"], ["3", "1", "2", "1"], ["4", "1", "2", "0"], ["5", "1", "1", "1"], ["6", "2", "1", "0"], ["7", "2", "2", "1"]], width=460, height=240),
    frame("② 最终幸存者 2 即多数元素", "drawTwoPointers", arr=[2, 2, 1, 1, 1, 2, 2], left=0, right=6, width=520, height=130),
    ],
    "conclusion": "多数元素出现次数过半，「抵消」不掉，投票结束后仍存活。",
    "py": """def majorityElement(nums):
    cand = count = 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand""",
    "java": """public int majorityElement(int[] nums) {
    int cand = 0, count = 0;
    for (int x : nums) {
        if (count == 0) cand = x;
        count += (x == cand) ? 1 : -1;
    }
    return cand;
}""",
    "time": "O(n)",
    "space": "O(1)",
    "pitfalls": [["count==0 换候选人", "抵消完后，下一个元素成为新候选人"], ["前提是多数元素存在", "题目保证一定存在；若不确定，最后要再遍历验证一次"]],
    "selfcheck": [["为什么投票法成立？", "多数元素次数 > n/2，任何其它元素集合的总数都 < n/2，抵消到最后必有剩余，且剩余者就是多数。"], ["若不一定存在多数元素？", "投票后需再扫描一遍确认 cand 次数是否真的 > n/2，否则返回无解。"]],
}

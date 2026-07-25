"""
LeetCode 1 — 两数之和 (Two Sum)
🟢 简单 | 哈希表

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出
和为目标值 target 的那两个整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

示例 1: nums = [2,7,11,15], target = 9  → 返回 [0,1]
示例 2: nums = [3,2,4], target = 6       → 返回 [1,2]
示例 3: nums = [3,3], target = 6         → 返回 [0,1]

目标: O(n) 时间复杂度
"""

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # ===== 在这里写你的代码 =====
        pass
        # =========================


# ===== 本地测试（写完代码后直接运行） =====
if __name__ == "__main__":
    s = Solution()

    # Case 1
    result = s.twoSum([2, 7, 11, 15], 9)
    assert result == [0, 1], f"Case 1 失败: {result}"
    print(f"Case 1 ✅: {result}")

    # Case 2
    result = s.twoSum([3, 2, 4], 6)
    assert result == [1, 2], f"Case 2 失败: {result}"
    print(f"Case 2 ✅: {result}")

    # Case 3
    result = s.twoSum([3, 3], 6)
    assert result == [0, 1], f"Case 3 失败: {result}"
    print(f"Case 3 ✅: {result}")

    print("\n🎉 全部测试通过!")

// 题目唯一数据源（index 列表、README、页面导航均从此读取）
// 修改题目：只改这里；新增页面文件后在此登记 file 即可自动上架
window.PROBLEMS = {
 "algo": [
  {
   "id": 1,
   "title": "两数之和",
   "diff": "easy",
   "tags": [
    "数组",
    "哈希表"
   ],
   "file": "algo/001-两数之和.html",
   "leetcode": 1,
   "cat": "哈希"
  },
  {
   "id": 2,
   "title": "两数相加",
   "diff": "medium",
   "tags": [
    "链表"
   ],
   "file": "algo/002-两数相加.html",
   "leetcode": 2,
   "cat": "链表"
  },
  {
   "id": 3,
   "title": "无重复字符的最长子串",
   "diff": "medium",
   "tags": [
    "滑动窗口",
    "哈希表"
   ],
   "file": "algo/003-无重复字符的最长子串.html",
   "leetcode": 3,
   "cat": "滑动窗口"
  },
  {
   "id": 4,
   "title": "寻找两个正序数组的中位数",
   "diff": "hard",
   "tags": [
    "二分"
   ],
   "file": "algo/004-寻找两个正序数组的中位数.html",
   "leetcode": 4,
   "cat": "二分查找"
  },
  {
   "id": 5,
   "title": "最长回文子串",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/005-最长回文子串.html",
   "leetcode": 5,
   "cat": "动态规划"
  },
  {
   "id": 6,
   "title": "正则表达式匹配",
   "diff": "hard",
   "tags": [
    "DP"
   ],
   "file": "algo/006-正则表达式匹配.html",
   "leetcode": 10,
   "cat": "动态规划"
  },
  {
   "id": 7,
   "title": "盛最多水的容器",
   "diff": "medium",
   "tags": [
    "双指针",
    "贪心"
   ],
   "file": "algo/007-盛最多水的容器.html",
   "leetcode": 11,
   "cat": "双指针"
  },
  {
   "id": 8,
   "title": "三数之和",
   "diff": "medium",
   "tags": [
    "双指针"
   ],
   "file": "algo/008-三数之和.html",
   "leetcode": 15,
   "cat": "双指针"
  },
  {
   "id": 9,
   "title": "电话号码的字母组合",
   "diff": "medium",
   "tags": [
    "回溯",
    "哈希表"
   ],
   "file": "algo/009-电话号码的字母组合.html",
   "leetcode": 17,
   "cat": "回溯"
  },
  {
   "id": 10,
   "title": "删除链表的倒数第N个结点",
   "diff": "medium",
   "tags": [
    "链表",
    "双指针"
   ],
   "file": "algo/010-删除链表的倒数第N个结点.html",
   "leetcode": 19,
   "cat": "链表"
  },
  {
   "id": 11,
   "title": "有效的括号",
   "diff": "easy",
   "tags": [
    "栈"
   ],
   "file": "algo/011-有效的括号.html",
   "leetcode": 20,
   "cat": "栈"
  },
  {
   "id": 12,
   "title": "合并两个有序链表",
   "diff": "easy",
   "tags": [
    "链表"
   ],
   "file": "algo/012-合并两个有序链表.html",
   "leetcode": 21,
   "cat": "链表"
  },
  {
   "id": 13,
   "title": "括号生成",
   "diff": "medium",
   "tags": [
    "回溯"
   ],
   "file": "algo/013-括号生成.html",
   "leetcode": 22,
   "cat": "回溯"
  },
  {
   "id": 14,
   "title": "合并K个升序链表",
   "diff": "hard",
   "tags": [
    "堆",
    "链表"
   ],
   "file": "algo/014-合并K个升序链表.html",
   "leetcode": 23,
   "cat": "堆"
  },
  {
   "id": 15,
   "title": "两两交换链表中的节点",
   "diff": "medium",
   "tags": [
    "链表"
   ],
   "file": "algo/015-两两交换链表中的节点.html",
   "leetcode": 24,
   "cat": "链表"
  },
  {
   "id": 16,
   "title": "K个一组翻转链表",
   "diff": "hard",
   "tags": [
    "链表"
   ],
   "file": "algo/016-K个一组翻转链表.html",
   "leetcode": 25,
   "cat": "链表"
  },
  {
   "id": 17,
   "title": "下一个排列",
   "diff": "medium",
   "tags": [
    "数组"
   ],
   "file": "algo/017-下一个排列.html",
   "leetcode": 31,
   "cat": "数组"
  },
  {
   "id": 18,
   "title": "最长有效括号",
   "diff": "hard",
   "tags": [
    "DP"
   ],
   "file": "algo/018-最长有效括号.html",
   "leetcode": 32,
   "cat": "栈"
  },
  {
   "id": 19,
   "title": "搜索旋转排序数组",
   "diff": "medium",
   "tags": [
    "二分"
   ],
   "file": "algo/019-搜索旋转排序数组.html",
   "leetcode": 33,
   "cat": "二分查找"
  },
  {
   "id": 20,
   "title": "在排序数组中查找元素的第一个和最后一个位置",
   "diff": "medium",
   "tags": [
    "二分"
   ],
   "file": "algo/020-在排序数组中查找元素的第一个和最后一个位置.html",
   "leetcode": 34,
   "cat": "二分查找"
  },
  {
   "id": 21,
   "title": "搜索插入位置",
   "diff": "easy",
   "tags": [
    "二分"
   ],
   "file": "algo/021-搜索插入位置.html",
   "leetcode": 35,
   "cat": "二分查找"
  },
  {
   "id": 22,
   "title": "组合总和",
   "diff": "medium",
   "tags": [
    "回溯"
   ],
   "file": "algo/022-组合总和.html",
   "leetcode": 39,
   "cat": "回溯"
  },
  {
   "id": 23,
   "title": "缺失的第一个正数",
   "diff": "hard",
   "tags": [
    "哈希表"
   ],
   "file": "algo/023-缺失的第一个正数.html",
   "leetcode": 41,
   "cat": "数组"
  },
  {
   "id": 24,
   "title": "接雨水",
   "diff": "hard",
   "tags": [
    "单调栈"
   ],
   "file": "algo/024-接雨水.html",
   "leetcode": 42,
   "cat": "双指针"
  },
  {
   "id": 25,
   "title": "跳跃游戏 II",
   "diff": "medium",
   "tags": [
    "贪心"
   ],
   "file": "algo/025-跳跃游戏 II.html",
   "leetcode": 45,
   "cat": "贪心"
  },
  {
   "id": 26,
   "title": "全排列",
   "diff": "medium",
   "tags": [
    "回溯"
   ],
   "file": "algo/026-全排列.html",
   "leetcode": 46,
   "cat": "回溯"
  },
  {
   "id": 27,
   "title": "旋转图像",
   "diff": "medium",
   "tags": [
    "数组"
   ],
   "file": "algo/027-旋转图像.html",
   "leetcode": 48,
   "cat": "矩阵"
  },
  {
   "id": 28,
   "title": "字母异位词分组",
   "diff": "medium",
   "tags": [
    "哈希表"
   ],
   "file": "algo/028-字母异位词分组.html",
   "leetcode": 49,
   "cat": "哈希"
  },
  {
   "id": 29,
   "title": "N皇后",
   "diff": "hard",
   "tags": [
    "回溯"
   ],
   "file": "algo/029-N皇后.html",
   "leetcode": 51,
   "cat": "回溯"
  },
  {
   "id": 30,
   "title": "最大子数组和",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/030-最大子数组和.html",
   "leetcode": 53,
   "cat": "动态规划"
  },
  {
   "id": 31,
   "title": "跳跃游戏",
   "diff": "medium",
   "tags": [
    "贪心"
   ],
   "file": "algo/031-跳跃游戏.html",
   "leetcode": 55,
   "cat": "贪心"
  },
  {
   "id": 32,
   "title": "合并区间",
   "diff": "medium",
   "tags": [
    "排序"
   ],
   "file": "algo/032-合并区间.html",
   "leetcode": 56,
   "cat": "数组"
  },
  {
   "id": 33,
   "title": "不同路径",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/033-不同路径.html",
   "leetcode": 62,
   "cat": "动态规划"
  },
  {
   "id": 34,
   "title": "最小路径和",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/034-最小路径和.html",
   "leetcode": 64,
   "cat": "动态规划"
  },
  {
   "id": 35,
   "title": "爬楼梯",
   "diff": "easy",
   "tags": [
    "DP"
   ],
   "file": "algo/035-爬楼梯.html",
   "leetcode": 70,
   "cat": "动态规划"
  },
  {
   "id": 36,
   "title": "编辑距离",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/036-编辑距离.html",
   "leetcode": 72,
   "cat": "动态规划"
  },
  {
   "id": 37,
   "title": "搜索二维矩阵",
   "diff": "medium",
   "tags": [
    "二分"
   ],
   "file": "algo/037-搜索二维矩阵.html",
   "leetcode": 74,
   "cat": "二分查找"
  },
  {
   "id": 38,
   "title": "颜色分类",
   "diff": "medium",
   "tags": [
    "双指针"
   ],
   "file": "algo/038-颜色分类.html",
   "leetcode": 75,
   "cat": "双指针"
  },
  {
   "id": 39,
   "title": "最小覆盖子串",
   "diff": "hard",
   "tags": [
    "滑动窗口"
   ],
   "file": "algo/039-最小覆盖子串.html",
   "leetcode": 76,
   "cat": "滑动窗口"
  },
  {
   "id": 40,
   "title": "子集",
   "diff": "medium",
   "tags": [
    "回溯"
   ],
   "file": "algo/040-子集.html",
   "leetcode": 78,
   "cat": "回溯"
  },
  {
   "id": 41,
   "title": "单词搜索",
   "diff": "medium",
   "tags": [
    "回溯"
   ],
   "file": "algo/041-单词搜索.html",
   "leetcode": 79,
   "cat": "回溯"
  },
  {
   "id": 42,
   "title": "柱状图中最大的矩形",
   "diff": "hard",
   "tags": [
    "单调栈"
   ],
   "file": "algo/042-柱状图中最大的矩形.html",
   "leetcode": 84,
   "cat": "栈"
  },
  {
   "id": 43,
   "title": "最大矩形",
   "diff": "hard",
   "tags": [
    "单调栈"
   ],
   "file": "algo/043-最大矩形.html",
   "leetcode": 85,
   "cat": "栈"
  },
  {
   "id": 44,
   "title": "二叉树的中序遍历",
   "diff": "easy",
   "tags": [
    "树"
   ],
   "file": "algo/044-二叉树的中序遍历.html",
   "leetcode": 94,
   "cat": "二叉树"
  },
  {
   "id": 45,
   "title": "不同的二叉搜索树",
   "diff": "medium",
   "tags": [
    "树"
   ],
   "file": "algo/045-不同的二叉搜索树.html",
   "leetcode": 96,
   "cat": "二叉树"
  },
  {
   "id": 46,
   "title": "验证二叉搜索树",
   "diff": "medium",
   "tags": [
    "BST"
   ],
   "file": "algo/046-验证二叉搜索树.html",
   "leetcode": 98,
   "cat": "二叉树"
  },
  {
   "id": 47,
   "title": "对称二叉树",
   "diff": "easy",
   "tags": [
    "树"
   ],
   "file": "algo/047-对称二叉树.html",
   "leetcode": 101,
   "cat": "二叉树"
  },
  {
   "id": 48,
   "title": "二叉树的层序遍历",
   "diff": "medium",
   "tags": [
    "BFS"
   ],
   "file": "algo/048-二叉树的层序遍历.html",
   "leetcode": 102,
   "cat": "二叉树"
  },
  {
   "id": 49,
   "title": "二叉树的最大深度",
   "diff": "easy",
   "tags": [
    "树"
   ],
   "file": "algo/049-二叉树的最大深度.html",
   "leetcode": 104,
   "cat": "二叉树"
  },
  {
   "id": 50,
   "title": "从前序与中序遍历构造二叉树",
   "diff": "medium",
   "tags": [
    "树"
   ],
   "file": "algo/050-从前序与中序遍历构造二叉树.html",
   "leetcode": 105,
   "cat": "二叉树"
  },
  {
   "id": 51,
   "title": "将有序数组转换为二叉搜索树",
   "diff": "easy",
   "tags": [
    "BST"
   ],
   "file": "algo/051-将有序数组转换为二叉搜索树.html",
   "leetcode": 108,
   "cat": "二叉树"
  },
  {
   "id": 52,
   "title": "二叉树展开为链表",
   "diff": "medium",
   "tags": [
    "树"
   ],
   "file": "algo/052-二叉树展开为链表.html",
   "leetcode": 114,
   "cat": "二叉树"
  },
  {
   "id": 53,
   "title": "杨辉三角",
   "diff": "easy",
   "tags": [
    "DP"
   ],
   "file": "algo/053-杨辉三角.html",
   "leetcode": 118,
   "cat": "动态规划"
  },
  {
   "id": 54,
   "title": "买卖股票的最佳时机",
   "diff": "easy",
   "tags": [
    "贪心"
   ],
   "file": "algo/054-买卖股票的最佳时机.html",
   "leetcode": 121,
   "cat": "贪心"
  },
  {
   "id": 55,
   "title": "二叉树中的最大路径和",
   "diff": "hard",
   "tags": [
    "树"
   ],
   "file": "algo/055-二叉树中的最大路径和.html",
   "leetcode": 124,
   "cat": "二叉树"
  },
  {
   "id": 56,
   "title": "最长连续序列",
   "diff": "medium",
   "tags": [
    "哈希表"
   ],
   "file": "algo/056-最长连续序列.html",
   "leetcode": 128,
   "cat": "哈希"
  },
  {
   "id": 57,
   "title": "分割回文串",
   "diff": "medium",
   "tags": [
    "回溯"
   ],
   "file": "algo/057-分割回文串.html",
   "leetcode": 131,
   "cat": "回溯"
  },
  {
   "id": 58,
   "title": "只出现一次的数字",
   "diff": "easy",
   "tags": [
    "位运算"
   ],
   "file": "algo/058-只出现一次的数字.html",
   "leetcode": 136,
   "cat": "位运算"
  },
  {
   "id": 59,
   "title": "随机链表的复制",
   "diff": "medium",
   "tags": [
    "链表"
   ],
   "file": "algo/059-随机链表的复制.html",
   "leetcode": 138,
   "cat": "链表"
  },
  {
   "id": 60,
   "title": "单词拆分",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/060-单词拆分.html",
   "leetcode": 139,
   "cat": "动态规划"
  },
  {
   "id": 61,
   "title": "环形链表",
   "diff": "easy",
   "tags": [
    "快慢指针"
   ],
   "file": "algo/061-环形链表.html",
   "leetcode": 141,
   "cat": "链表"
  },
  {
   "id": 62,
   "title": "环形链表 II",
   "diff": "medium",
   "tags": [
    "快慢指针"
   ],
   "file": "algo/062-环形链表 II.html",
   "leetcode": 142,
   "cat": "链表"
  },
  {
   "id": 63,
   "title": "重排链表",
   "diff": "medium",
   "tags": [
    "链表"
   ],
   "file": "algo/063-重排链表.html",
   "leetcode": 143,
   "cat": "链表"
  },
  {
   "id": 64,
   "title": "LRU缓存",
   "diff": "medium",
   "tags": [
    "哈希表",
    "链表"
   ],
   "file": "algo/064-LRU缓存.html",
   "leetcode": 146,
   "cat": "链表"
  },
  {
   "id": 65,
   "title": "排序链表",
   "diff": "medium",
   "tags": [
    "链表",
    "归并"
   ],
   "file": "algo/065-排序链表.html",
   "leetcode": 148,
   "cat": "链表"
  },
  {
   "id": 66,
   "title": "乘积最大子数组",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/066-乘积最大子数组.html",
   "leetcode": 152,
   "cat": "动态规划"
  },
  {
   "id": 67,
   "title": "寻找旋转排序数组中的最小值",
   "diff": "medium",
   "tags": [
    "二分"
   ],
   "file": "algo/067-寻找旋转排序数组中的最小值.html",
   "leetcode": 153,
   "cat": "二分查找"
  },
  {
   "id": 68,
   "title": "最小栈",
   "diff": "medium",
   "tags": [
    "栈"
   ],
   "file": "algo/068-最小栈.html",
   "leetcode": 155,
   "cat": "栈"
  },
  {
   "id": 69,
   "title": "相交链表",
   "diff": "easy",
   "tags": [
    "链表"
   ],
   "file": "algo/069-相交链表.html",
   "leetcode": 160,
   "cat": "链表"
  },
  {
   "id": 70,
   "title": "多数元素",
   "diff": "easy",
   "tags": [
    "投票"
   ],
   "file": "algo/070-多数元素.html",
   "leetcode": 169,
   "cat": "数组"
  },
  {
   "id": 71,
   "title": "轮转数组",
   "diff": "medium",
   "tags": [
    "数组"
   ],
   "file": "algo/071-轮转数组.html",
   "leetcode": 189,
   "cat": "数组"
  },
  {
   "id": 72,
   "title": "打家劫舍",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/072-打家劫舍.html",
   "leetcode": 198,
   "cat": "动态规划"
  },
  {
   "id": 73,
   "title": "二叉树的右视图",
   "diff": "medium",
   "tags": [
    "BFS"
   ],
   "file": "algo/073-二叉树的右视图.html",
   "leetcode": 199,
   "cat": "二叉树"
  },
  {
   "id": 74,
   "title": "岛屿数量",
   "diff": "medium",
   "tags": [
    "DFS"
   ],
   "file": "algo/074-岛屿数量.html",
   "leetcode": 200,
   "cat": "图"
  },
  {
   "id": 75,
   "title": "反转链表",
   "diff": "easy",
   "tags": [
    "链表"
   ],
   "file": "algo/075-反转链表.html",
   "leetcode": 206,
   "cat": "链表"
  },
  {
   "id": 76,
   "title": "课程表",
   "diff": "medium",
   "tags": [
    "拓扑排序"
   ],
   "file": "algo/076-课程表.html",
   "leetcode": 207,
   "cat": "图"
  },
  {
   "id": 77,
   "title": "实现Trie(前缀树)",
   "diff": "medium",
   "tags": [
    "Trie"
   ],
   "file": "algo/077-实现Trie(前缀树).html",
   "leetcode": 208,
   "cat": "字符串"
  },
  {
   "id": 78,
   "title": "数组中的第K个最大元素",
   "diff": "medium",
   "tags": [
    "堆"
   ],
   "file": "algo/078-数组中的第K个最大元素.html",
   "leetcode": 215,
   "cat": "堆"
  },
  {
   "id": 79,
   "title": "最大正方形",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/079-最大正方形.html",
   "leetcode": 221,
   "cat": "动态规划"
  },
  {
   "id": 80,
   "title": "翻转二叉树",
   "diff": "easy",
   "tags": [
    "树"
   ],
   "file": "algo/080-翻转二叉树.html",
   "leetcode": 226,
   "cat": "二叉树"
  },
  {
   "id": 81,
   "title": "二叉搜索树中第K小的元素",
   "diff": "medium",
   "tags": [
    "BST"
   ],
   "file": "algo/081-二叉搜索树中第K小的元素.html",
   "leetcode": 230,
   "cat": "二叉树"
  },
  {
   "id": 82,
   "title": "回文链表",
   "diff": "easy",
   "tags": [
    "链表"
   ],
   "file": "algo/082-回文链表.html",
   "leetcode": 234,
   "cat": "链表"
  },
  {
   "id": 83,
   "title": "二叉树的最近公共祖先",
   "diff": "medium",
   "tags": [
    "树"
   ],
   "file": "algo/083-二叉树的最近公共祖先.html",
   "leetcode": 236,
   "cat": "二叉树"
  },
  {
   "id": 84,
   "title": "除自身以外数组的乘积",
   "diff": "medium",
   "tags": [
    "前缀积"
   ],
   "file": "algo/084-除自身以外数组的乘积.html",
   "leetcode": 238,
   "cat": "数组"
  },
  {
   "id": 85,
   "title": "滑动窗口最大值",
   "diff": "hard",
   "tags": [
    "单调队列"
   ],
   "file": "algo/085-滑动窗口最大值.html",
   "leetcode": 239,
   "cat": "滑动窗口"
  },
  {
   "id": 86,
   "title": "搜索二维矩阵 II",
   "diff": "medium",
   "tags": [
    "二分"
   ],
   "file": "algo/086-搜索二维矩阵 II.html",
   "leetcode": 240,
   "cat": "矩阵"
  },
  {
   "id": 87,
   "title": "完全平方数",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/087-完全平方数.html",
   "leetcode": 279,
   "cat": "动态规划"
  },
  {
   "id": 88,
   "title": "移动零",
   "diff": "easy",
   "tags": [
    "双指针"
   ],
   "file": "algo/088-移动零.html",
   "leetcode": 283,
   "cat": "双指针"
  },
  {
   "id": 89,
   "title": "寻找重复数",
   "diff": "medium",
   "tags": [
    "快慢指针"
   ],
   "file": "algo/089-寻找重复数.html",
   "leetcode": 287,
   "cat": "数组"
  },
  {
   "id": 90,
   "title": "数据流的中位数",
   "diff": "hard",
   "tags": [
    "堆"
   ],
   "file": "algo/090-数据流的中位数.html",
   "leetcode": 295,
   "cat": "堆"
  },
  {
   "id": 91,
   "title": "二叉树的序列化与反序列化",
   "diff": "hard",
   "tags": [
    "树"
   ],
   "file": "algo/091-二叉树的序列化与反序列化.html",
   "leetcode": 297,
   "cat": "二叉树"
  },
  {
   "id": 92,
   "title": "最长递增子序列",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/092-最长递增子序列.html",
   "leetcode": 300,
   "cat": "动态规划"
  },
  {
   "id": 93,
   "title": "删除无效的括号",
   "diff": "hard",
   "tags": [
    "BFS"
   ],
   "file": "algo/093-删除无效的括号.html",
   "leetcode": 301,
   "cat": "回溯"
  },
  {
   "id": 94,
   "title": "买卖股票最佳时机含冷冻期",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/094-买卖股票最佳时机含冷冻期.html",
   "leetcode": 309,
   "cat": "动态规划"
  },
  {
   "id": 95,
   "title": "戳气球",
   "diff": "hard",
   "tags": [
    "DP"
   ],
   "file": "algo/095-戳气球.html",
   "leetcode": 312,
   "cat": "动态规划"
  },
  {
   "id": 96,
   "title": "零钱兑换",
   "diff": "medium",
   "tags": [
    "DP"
   ],
   "file": "algo/096-零钱兑换.html",
   "leetcode": 322,
   "cat": "动态规划"
  },
  {
   "id": 97,
   "title": "打家劫舍 III",
   "diff": "medium",
   "tags": [
    "树",
    "DP"
   ],
   "file": "algo/097-打家劫舍 III.html",
   "leetcode": 337,
   "cat": "二叉树"
  },
  {
   "id": 98,
   "title": "前K个高频元素",
   "diff": "medium",
   "tags": [
    "堆"
   ],
   "file": "algo/098-前K个高频元素.html",
   "leetcode": 347,
   "cat": "堆"
  },
  {
   "id": 99,
   "title": "字符串解码",
   "diff": "medium",
   "tags": [
    "栈"
   ],
   "file": "algo/099-字符串解码.html",
   "leetcode": 394,
   "cat": "栈"
  },
  {
   "id": 100,
   "title": "除法求值",
   "diff": "medium",
   "tags": [
    "图"
   ],
   "file": "algo/100-除法求值.html",
   "leetcode": 399,
   "cat": "图"
  }
 ],
 "sql": [
  {
   "id": 1,
   "title": "连续登录天数",
   "diff": "medium",
   "tags": [
    "窗口函数",
    "日期"
   ],
   "file": "sql/001-连续登录天数.html"
  },
  {
   "id": 2,
   "title": "SHEIN新客回访复购分析",
   "diff": "hard",
   "tags": [
    "多表JOIN",
    "窗口函数",
    "条件聚合"
   ],
   "file": "sql/002-shein新客回访复购分析.html"
  },
  {
   "id": 3,
   "title": "SHEIN平台合并与过滤",
   "diff": "easy",
   "tags": [
    "CASE WHEN",
    "JOIN",
    "聚合过滤"
   ],
   "file": "sql/003-shein平台合并与过滤.html"
  },
  {
   "id": 4,
   "title": "SHEIN库存售罄天数分析",
   "diff": "medium",
   "tags": [
    "窗口函数",
    "日期计算",
    "聚合"
   ],
   "file": "sql/004-shein库存售罄天数分析.html"
  },
  {
   "id": 5,
   "title": "互相关注用户对",
   "diff": "medium",
   "tags": [
    "自连接",
    "字节"
   ],
   "file": "sql/005-字节互相关注用户对.html"
  }
 ]
};

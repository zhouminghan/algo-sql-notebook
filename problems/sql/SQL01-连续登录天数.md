# SQL01 — 连续登录天数

> ROW_NUMBER + DATE_SUB 分组技巧 | 🟡 中等 | 窗口函数

---

## 一、建表语句与测试数据

```sql
CREATE TABLE t1_login_log (
    user_id    string COMMENT '用户ID',
    login_date string COMMENT '登录日期'
) COMMENT '用户登录日志表';

INSERT INTO t1_login_log VALUES
('u01', '2026-07-01'),
('u01', '2026-07-02'),
('u01', '2026-07-03'),
('u01', '2026-07-05'),
('u01', '2026-07-06'),
('u02', '2026-07-01'),
('u02', '2026-07-02'),
('u02', '2026-07-04'),
('u03', '2026-07-01'),
('u03', '2026-07-02'),
('u03', '2026-07-03'),
('u03', '2026-07-04'),
('u03', '2026-07-05'),
('u03', '2026-07-06'),
('u04', '2026-07-01'),
('u04', '2026-07-03'),
('u04', '2026-07-05');
```

---

## 二、题目描述

**表**：`t1_login_log`（用户登录日志表）  
**字段**：`user_id`（用户ID）、`login_date`（登录日期）

**要求**：找出每个用户的 **最大连续登录天数**。

> **连续登录**：相邻日期间隔刚好为1天。  
> 示例：07-01 → 07-02 → 07-03 算连续3天，07-01 → 07-03 中间断了，不算连续。

---

## 三、解题思路

核心：**连续日期的 login_date − ROW_NUMBER() 结果是相同的日期**。

以 `u01` 为例演示：

```
login_date  | rn | DATE_SUB(login_date, rn) | 连续区间
2026-07-01  | 1  | 2026-06-30               | ← 组A
2026-07-02  | 2  | 2026-06-30               | ← 组A
2026-07-03  | 3  | 2026-06-30               | ← 组A
2026-07-05  | 4  | 2026-07-01               | ← 组B (断了)
2026-07-06  | 5  | 2026-07-01               | ← 组B
```

同一个 DATE_SUB 结果的日期就是连续的 → 按 `(user_id, grp_date)` 分组 `COUNT(*)` 即连续天数。

**步骤**：
1. `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date)` 生成行号 rn
2. `DATE_SUB(login_date, rn)` 生成分组标记 grp_date
3. 按 `(user_id, grp_date)` 分组，`COUNT(*)` 得到每个连续区间的天数
4. 取每个用户的 `MAX(天数值)` 即最大连续登录天数

---

## 四、最终 SQL

```sql
WITH ranked AS (
    SELECT
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM t1_login_log
),
grouped AS (
    SELECT
        user_id,
        login_date,
        rn,
        DATE_SUB(login_date, rn) AS grp_date
    FROM ranked
),
counts AS (
    SELECT
        user_id,
        grp_date,
        COUNT(*) AS consecutive_days
    FROM grouped
    GROUP BY user_id, grp_date
)
SELECT
    user_id,
    MAX(consecutive_days) AS max_consecutive_days
FROM counts
GROUP BY user_id
ORDER BY user_id;
```

---

## 五、执行结果示例

| user_id | max_consecutive_days |
|---------|---------------------|
| u01     | 3                   |
| u02     | 2                   |
| u03     | 6                   |
| u04     | 1                   |

**结果解读**：
- u01：07-01~07-03 连续3天，07-05~07-06 连续2天 → 最大3天
- u02：07-01~07-02 连续2天，07-04 单独1天 → 最大2天
- u03：07-01~07-06 全部连续 → 6天
- u04：07-01、07-03、07-05 全部断裂 → 最大1天

---

## 六、常见坑点与扩展

- **坑点1**：原始数据可能同一天有多条登录记录，第一步需 `SELECT DISTINCT` 去重，否则同一天多条记录会被算成多个 rn，打乱 DATE_SUB 分组逻辑。
- **坑点2**：`DATE_SUB(login_date, rn)` 是核心，记不住就记口诀——「连续日期的日期减行号，结果都一样」。
- **坑点3**：如果用 `LAG` 取上一条日期来判断是否连续，也能做但更复杂，不如 DATE_SUB 简洁。
- **扩展**：
  - 改成「连续登录 ≥N 天的用户」→ 最后加 `HAVING MAX(consecutive_days) >= N`
  - 允许间隔 ≤1 天也算连续 → 用 `LAG` 取上一条日期，差值 ≤2 天归为同一组
  - Hive/SparkSQL 中 `DATE_SUB` 语法为 `date_sub(login_date, rn)`

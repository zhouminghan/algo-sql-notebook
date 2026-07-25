-- ============================================
-- SQL01 — 连续登录天数 (MySQL版)
-- 用法:
--   mysql -h 127.0.0.1 -u root -p123456 sql_practice < SQL01-连续登录天数.sql
--   或在 mysql 终端里: source SQL01-连续登录天数.sql
--   或逐段复制粘贴到 mysql 终端执行
-- ============================================

-- 先看一眼数据
SELECT * FROM t1_login_log ORDER BY user_id, login_date;

-- ===== 下面写你的 SQL =====
-- 提示: 用 ROW_NUMBER() + DATE_SUB 分组技巧
-- 期望输出: u01|3  u02|2  u03|6  u04|1

SELECT '👆 数据在上面，在下面写你的查询' AS hint;

-- ===== 答案参考: 取消注释运行 =====
-- WITH ranked AS (
--     SELECT user_id, login_date,
--         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
--     FROM t1_login_log
-- ),
-- grouped AS (
--     SELECT user_id, login_date, rn,
--         DATE_SUB(login_date, INTERVAL rn DAY) AS grp_date
--     FROM ranked
-- ),
-- counts AS (
--     SELECT user_id, grp_date, COUNT(*) AS days
--     FROM grouped
--     GROUP BY user_id, grp_date
-- )
-- SELECT user_id, MAX(days) AS max_consecutive_days
-- FROM counts
-- GROUP BY user_id
-- ORDER BY user_id;

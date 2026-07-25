-- ============================================
-- SQL01 — 连续登录天数（答案）
-- mysql -h 127.0.0.1 -u root -p123456 sql_practice < SQL01-answer.sql
-- ============================================

WITH ranked AS (
    SELECT user_id, login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM t1_login_log
),
grouped AS (
    SELECT user_id, login_date, rn,
        DATE_SUB(login_date, INTERVAL rn DAY) AS grp_date
    FROM ranked
),
counts AS (
    SELECT user_id, grp_date, COUNT(*) AS days
    FROM grouped
    GROUP BY user_id, grp_date
)
SELECT user_id, MAX(days) AS max_consecutive_days
FROM counts
GROUP BY user_id
ORDER BY user_id;

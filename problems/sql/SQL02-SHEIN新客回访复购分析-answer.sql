-- ============================================
-- SQL02 — SHEIN新客回访复购分析（答案）
-- mysql -h 127.0.0.1 -u root -p123456 sql_practice < SQL02-answer.sql
-- ============================================

WITH first_order AS (
    SELECT
        user_id,
        MIN(pay_time) AS first_pay,
        DATE_FORMAT(MIN(pay_time), '%Y-%m') AS first_month
    FROM t2_order_detail
    GROUP BY user_id
),
first_cate_raw AS (
    SELECT DISTINCT
        f.user_id, f.first_month, f.first_pay, o.cate_nm
    FROM first_order f
    JOIN t2_order_detail o
        ON f.user_id = o.user_id AND o.pay_time = f.first_pay
),
first_cate_agg AS (
    SELECT
        user_id, first_month, first_pay,
        GROUP_CONCAT(DISTINCT cate_nm ORDER BY cate_nm) AS cates
    FROM first_cate_raw
    GROUP BY user_id, first_month, first_pay
),
user_cat AS (
    SELECT
        user_id, first_month, first_pay,
        CASE
            WHEN cates = 'women'           THEN 'A'
            WHEN cates = 'men,women'       THEN 'B'
            ELSE 'C'
        END AS category
    FROM first_cate_agg
),
new_cust AS (
    SELECT * FROM user_cat WHERE first_month >= '2020-01'
),
cust_flag AS (
    SELECT
        nc.*,
        EXISTS (
            SELECT 1 FROM t2_user_visit_di v
            WHERE v.user_id = nc.user_id
              AND v.dt >= DATE_FORMAT(nc.first_pay, '%Y%m%d')
              AND v.dt <= DATE_FORMAT(
                    DATE_ADD(STR_TO_DATE(nc.first_pay, '%Y-%m-%d %H:%i'),
                             INTERVAL 30 DAY), '%Y%m%d')
        ) AS has_visit,
        EXISTS (
            SELECT 1 FROM t2_order_detail o2
            WHERE o2.user_id = nc.user_id
              AND o2.pay_time > nc.first_pay
              AND o2.pay_time <= DATE_ADD(
                    STR_TO_DATE(nc.first_pay, '%Y-%m-%d %H:%i'),
                    INTERVAL 30 DAY)
        ) AS has_repurchase
    FROM new_cust nc
),
monthly AS (
    SELECT
        first_month, category,
        COUNT(DISTINCT user_id) AS cust_cnt,
        COUNT(DISTINCT CASE WHEN has_visit      THEN user_id END) AS visit_cnt,
        COUNT(DISTINCT CASE WHEN has_repurchase THEN user_id END) AS repurchase_cnt
    FROM cust_flag
    GROUP BY first_month, category
),
repurchase_cate AS (
    SELECT
        nc.first_month, nc.category, o.cate_nm,
        COUNT(DISTINCT nc.user_id) AS buyers,
        ROW_NUMBER() OVER (
            PARTITION BY nc.first_month, nc.category
            ORDER BY COUNT(DISTINCT nc.user_id) DESC, o.cate_nm
        ) AS rn
    FROM new_cust nc
    JOIN t2_order_detail o
        ON nc.user_id = o.user_id
       AND o.pay_time > nc.first_pay
       AND o.pay_time <= DATE_ADD(
            STR_TO_DATE(nc.first_pay, '%Y-%m-%d %H:%i'),
            INTERVAL 30 DAY)
    WHERE nc.first_month >= '2020-01'
    GROUP BY nc.first_month, nc.category, o.cate_nm
),
top3 AS (
    SELECT
        first_month, category,
        GROUP_CONCAT(cate_nm ORDER BY rn SEPARATOR ',') AS top3_cates
    FROM repurchase_cate
    WHERE rn <= 3
    GROUP BY first_month, category
)
SELECT
    m.first_month        AS 首单月份,
    m.category           AS 首单品类,
    m.cust_cnt           AS 新客人数,
    m.visit_cnt          AS 回访人数,
    CONCAT(ROUND(m.visit_cnt * 100.0 / m.cust_cnt, 0), '%') AS 回访率,
    m.repurchase_cnt     AS 复购人数,
    CONCAT(ROUND(m.repurchase_cnt * 100.0 / m.cust_cnt, 0), '%') AS 复购率,
    COALESCE(t.top3_cates, '') AS 复购的top3品类
FROM monthly m
LEFT JOIN top3 t
    ON m.first_month = t.first_month AND m.category = t.category
ORDER BY m.first_month, m.category;

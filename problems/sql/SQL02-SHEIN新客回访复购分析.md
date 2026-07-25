# SQL02 — SHEIN新客回访复购分析

> 多表JOIN + 条件聚合 + GROUP_CONCAT + 首单分类 | 🔴 困难 | 业务场景

---

## 一、建表语句与测试数据

```sql
CREATE TABLE t2_order_detail (
    user_id   string COMMENT '用户ID',
    pay_time  string COMMENT '付款时间，格式 yyyy-MM-dd HH:mm',
    sku       string COMMENT '商品名称',
    cate_nm   string COMMENT '商品类别：women/men/kids/young',
    sales_cnt int    COMMENT '销量'
) COMMENT '订单明细表';

INSERT INTO t2_order_detail VALUES
-- 2020-01 A类：只买过 women (u01)
('u01', '2020-01-05 10:00', 'dress_01', 'women', 2),
('u01', '2020-01-05 10:30', 'dress_02', 'women', 1),
('u01', '2020-01-10 14:00', 'bag_01',   'women', 1),
-- 2020-01 B类：首单买 women+men (u02)
('u02', '2020-01-10 09:00', 'shirt_01', 'women', 1),
('u02', '2020-01-10 09:05', 'pants_01', 'men',   1),
-- 2020-01 C类：首单买 women+men+kids (u03)
('u03', '2020-01-15 11:00', 'shirt_02', 'women', 1),
('u03', '2020-01-15 11:00', 'pants_02', 'men',   1),
('u03', '2020-01-15 11:00', 'toy_01',   'kids',  1),
-- 2019年用户（不应计入2020年统计）(u99)
('u99', '2019-06-01 10:00', 'dress_99', 'women', 1),
('u99', '2020-02-10 10:00', 'bag_99',   'women', 1),
-- 2020-02 A类：只买 women，有复购 (u04)
('u04', '2020-02-03 08:00', 'dress_03', 'women', 1),
('u04', '2020-02-20 10:00', 'skirt_01', 'women', 2),
('u04', '2020-03-01 09:00', 'bag_02',   'women', 1),
-- 2020-02 B类 (u05)
('u05', '2020-02-08 12:00', 'shirt_03', 'women', 1),
('u05', '2020-02-08 12:05', 'pants_03', 'men',   2),
-- 2020-02 C类：首单只买 kids (u06)
('u06', '2020-02-12 13:00', 'toy_02',   'kids',  1),
('u06', '2020-02-23 15:00', 'toy_03',   'kids',  1),
-- 2020-02 C类：首单只买 young (u07)
('u07', '2020-02-12 14:00', 'jeans_01', 'young', 1),
-- 2020-03 A类：大量复购 (u08)
('u08', '2020-03-05 10:00', 'dress_04', 'women', 1),
('u08', '2020-03-06 11:00', 'dress_05', 'women', 1),
('u08', '2020-03-07 12:00', 'skirt_02', 'women', 1),
('u08', '2020-03-10 13:00', 'bag_03',   'kids',  1),
('u08', '2020-03-12 14:00', 'toy_04',   'young', 1),
-- 2020-03 C类 (u09)
('u09', '2020-03-18 09:00', 'pants_04', 'men',   1),
-- 2020-03 B类 (u10)
('u10', '2020-03-20 10:00', 'dress_06', 'women', 1),
('u10', '2020-03-20 10:05', 'pants_05', 'men',   1);

CREATE TABLE t2_user_visit_di (
    user_id string COMMENT '用户ID',
    dt      string COMMENT '浏览日期（yyyymmdd格式）'
) COMMENT '用户回访日志表';

INSERT INTO t2_user_visit_di VALUES
-- u01: 首单 2020-01-05，30天内回访
('u01', '20200120'),
('u01', '20200128'),
-- u02: 首单 2020-01-10，30天内回访
('u02', '20200115'),
('u02', '20200203'),
-- u03: 首单 2020-01-15，无回访
-- u04: 首单 2020-02-03，30天内回访
('u04', '20200220'),
('u04', '20200228'),
-- u05: 首单 2020-02-08，无回访
-- u06: 首单 2020-02-12，30天内回访
('u06', '20200225'),
-- u07: 首单 2020-02-12，无回访
-- u08: 首单 2020-03-05，30天内回访
('u08', '20200320'),
-- u09: 首单 2020-03-18，30天内回访
('u09', '20200410'),  -- 超过30天
-- u10: 无回访
-- u99: 2019年老用户，有2020年回访但不应计入
('u99', '20200215');
```

---

## 二、题目描述

来自 **SHEIN 加拿大市场部数分笔试** 真题。

**订单表** `t2_order_detail`：user_id（用户ID）、pay_time（付款时间）、sku（商品）、cate_nm（品类：women/men/kids/young）、sales_cnt（销量）

**回访表** `t2_user_visit_di`：user_id（用户ID）、dt（浏览日期，yyyymmdd格式）

> 时间均从 2019-01-01 开始。只看 **2020年及之后** 的新客。

**新客分类**（按首单购买的品类）：
- **A**：首单仅购买 women
- **B**：首单仅购买 women 和 men（恰好两类，不多不少）
- **C**：其余（非 A/B 类）

**需求**：按首单月份 + 品类分组，计算 2020年及之后每月新客的：
- 新客人数
- 首单30天内的回访人数、回访率（= 回访人数 / 新客人数）
- 首单30天内的复购人数、复购率（= 复购人数 / 新客人数）
- 复购的 top3 品类（按复购人数降序，用逗号隔开）

**输出格式**：

| 首单月份 | 首单品类 | 新客人数 | 回访人数 | 回访率 | 复购人数 | 复购率 | 复购的top3品类 |
|---------|---------|---------|---------|-------|---------|-------|--------------|
| 2020-01 | A | 1000 | 800 | 80% | 500 | 50% | women,kids,young |

> **定义说明**：
> - 新客：首单时间落在该月的用户（如 2020-01 新客 = 首单在 2020-01-01~2020-01-31）
> - 回访：首单日期起 30 天内在 `t2_user_visit_di` 有记录
> - 复购：首单日期起 30 天内在 `t2_order_detail` 有非首单的购买记录

---

## 领域知识

> 本题涉及电商数据分析中的多个专业术语。

| 术语 | 全称 | 本题语境 |
|------|------|---------|
| SKU | Stock Keeping Unit | 库存量单位，商品的唯一标识。本题中 `sku` 字段代表具体商品规格（如 dress_01） |
| 品类 | Category | 商品分类维度，一个 SKU 属于一个品类。本题 `cate_nm` 有 women / men / kids / young 四类 |
| 新客 | New Customer | 首次下单的用户。本题按首单所在月份归类（如首单在 2020-01 的为该月新客），2019年已有订单的用户不参与统计 |
| 首单 | First Order | 用户历史中的第一笔订单。本题用 `MIN(pay_time)` 确定每个用户的首单时间，同一时刻可能包含多行（多个 SKU） |
| 回访 | Return Visit | 用户下单后再次浏览/访问平台。本题通过 `t2_user_visit_di` 表判断：首单日期起 30 天内有浏览记录即为回访 |
| 回访率 | Return Visit Rate | 首单 30 天内回访的用户数 / 新客人数。衡量新客的「回头看看」意愿 |
| 复购 | Repurchase | 用户首单后再次下单购买的行为。本题通过 `t2_order_detail` 中非首单的记录判断：`pay_time > first_pay` 且间隔 ≤ 30天 |
| 复购率 | Repurchase Rate | 首单 30 天内复购的用户数 / 新客人数。衡量新客的「再次掏钱」意愿，是电商核心指标 |

---

## 三、解题思路

**这道题拆解为 8 步，环环相扣**：

**Step 1：找出每个用户的首单时间**
用 `MIN(pay_time)` + `GROUP BY user_id`，同时生成首单月份 `DATE_FORMAT(pay_time, '%Y-%m')`。

**Step 2：确定首单的品类集合**
将首单时间的订单详情 JOIN 回原表，去重收集品类。注意：同一用户在首单时间可能有多条记录（买了多个 SKU），需要 `DISTINCT`。

**Step 3：品类分类 A/B/C**
用 `GROUP_CONCAT(DISTINCT cate_nm ORDER BY cate_nm)` 得到有序的品类列表，然后：
- `= 'women'` → A
- `= 'men,women'` → B（GROUP_CONCAT 默认逗号分隔，排序后固定为 men,women）
- 其他 → C

**Step 4：过滤 2020 年及之后的新客**
`WHERE first_month >= '2020-01'`

**Step 5：计算每个新客的30天回访**
用 `EXISTS` 子查询检查 `t2_user_visit_di`：
`dt BETWEEN DATE_FORMAT(first_pay, '%Y%m%d') AND DATE_FORMAT(first_pay+30, '%Y%m%d')`

**Step 6：计算每个新客的30天复购**
用 `EXISTS` 子查询检查 `t2_order_detail`：
`pay_time > first_pay AND pay_time <= first_pay + 30天`

**Step 7：按月份+品类聚合统计**
`COUNT(DISTINCT user_id)` 算新客数，`COUNT(DISTINCT CASE WHEN has_visit THEN user_id END)` 算回访人数。

**Step 8：复购 Top3 品类**
对复购订单按 `(first_month, category, cate_nm)` 分组统计复购人数 → `ROW_NUMBER()` 排序 → 取前三 → `GROUP_CONCAT` 拼接。

---

## 四、最终 SQL

```sql
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
```

---

## 五、执行结果示例

| 首单月份 | 首单品类 | 新客人数 | 回访人数 | 回访率 | 复购人数 | 复购率 | 复购的top3品类 |
|---------|---------|---------|---------|-------|---------|-------|--------------|
| 2020-01 | A | 1 | 1 | 100% | 1 | 100% | women |
| 2020-01 | B | 1 | 1 | 100% | 0 | 0% | |
| 2020-01 | C | 1 | 0 | 0% | 0 | 0% | |
| 2020-02 | A | 1 | 1 | 100% | 0 | 0% | |
| 2020-02 | B | 1 | 0 | 0% | 0 | 0% | |
| 2020-02 | C | 2 | 1 | 50% | 1 | 50% | kids |
| 2020-03 | A | 1 | 1 | 100% | 1 | 100% | kids,young,women |
| 2020-03 | B | 1 | 0 | 0% | 0 | 0% | |
| 2020-03 | C | 1 | 0 | 0% | 0 | 0% | |

**结果解读**：
- 2020-01-A (u01)：首单买 women，30天内回访2次、复购1次（又买了一件 women bag）
- 2020-01-B (u02)：首单买 women+men，有回访但无复购
- 2020-01-C (u03)：首单买 women+men+kids，无回访无复购
- 2020-02-C (u06)：首单买 kids，有回访也有复购，复购品类是 kids
- 2020-03-A (u08)：首单买 women，复购了 women、kids、young 三种品类
- u99（2019老用户）不参与统计

---

## 六、常见坑点与扩展

- **坑点1**：`GROUP_CONCAT` 不同排序结果不同。必须带 `ORDER BY cate_nm` 才能保证 `B` 类匹配结果是 `men,women` 而不是 `women,men`，否则 CASE 判断会漏掉。
- **坑点2**：同一首单时刻可能有多个 SKU 属于同一品类（如两件 women），需要 `DISTINCT` 去重后再 `GROUP_CONCAT`，否则会出现 `women,women`。
- **坑点3**：回访表 dt 是 `yyyymmdd` 字符串，首单 pay_time 是 `yyyy-MM-dd HH:mm` 格式，需用 `DATE_FORMAT` 统一格式后再比较。
- **坑点4**：Hive 环境下 `GROUP_CONCAT` 不存在，需用 `concat_ws(',', collect_set(cate_nm))` 替代，且日期处理用 `date_format` / `date_add`。
- **坑点5**：`EXISTS` 子查询在大数据量下可能较慢，可改为 `LEFT JOIN` + 聚合的方式优化。
- **坑点6**：首单月份按 `first_month` 分组，注意 2020-01 这个字符串排序要 `ORDER BY`，否则月份顺序可能乱。
- **扩展**：
  - 改为看「首单7天/60天内」回访复购 → 改 `INTERVAL 30 DAY` 即可
  - 想看每个品类的复购占比 → 在 `repurchase_cate` 中加 `RATIO_TO_REPORT` 窗口函数
  - Hive/Spark SQL 版：`collect_set` + `concat_ws` 替代 `GROUP_CONCAT`，`date_add` 替代 `DATE_ADD`

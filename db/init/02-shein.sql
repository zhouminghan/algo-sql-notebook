-- ==========================================
-- SQL02: SHEIN新客回访复购分析
-- ==========================================
DROP TABLE IF EXISTS t2_order_detail;
CREATE TABLE t2_order_detail (
    user_id   VARCHAR(64),
    pay_time  DATETIME,
    sku       VARCHAR(128),
    cate_nm   VARCHAR(32),
    sales_cnt INT
);
COMMENT ON TABLE t2_order_detail IS '订单明细表';
COMMENT ON COLUMN t2_order_detail.user_id IS '用户ID';
COMMENT ON COLUMN t2_order_detail.pay_time IS '付款时间';
COMMENT ON COLUMN t2_order_detail.sku IS '商品名称';
COMMENT ON COLUMN t2_order_detail.cate_nm IS '商品类别：women/men/kids/young';
COMMENT ON COLUMN t2_order_detail.sales_cnt IS '销量';

INSERT INTO t2_order_detail VALUES
-- 2020-01 A类：只买过 women (u01)
('u01', '2020-01-05 10:00:00', 'dress_01', 'women', 2),
('u01', '2020-01-05 10:30:00', 'dress_02', 'women', 1),
('u01', '2020-01-10 14:00:00', 'bag_01',   'women', 1),
-- 2020-01 B类：首单买 women+men (u02)
('u02', '2020-01-10 09:00:00', 'shirt_01', 'women', 1),
('u02', '2020-01-10 09:05:00', 'pants_01', 'men',   1),
-- 2020-01 C类：首单买 women+men+kids (u03)
('u03', '2020-01-15 11:00:00', 'shirt_02', 'women', 1),
('u03', '2020-01-15 11:00:00', 'pants_02', 'men',   1),
('u03', '2020-01-15 11:00:00', 'toy_01',   'kids',  1),
-- 2019年用户（不应计入2020年统计）(u99)
('u99', '2019-06-01 10:00:00', 'dress_99', 'women', 1),
('u99', '2020-02-10 10:00:00', 'bag_99',   'women', 1),
-- 2020-02 A类：只买 women，有复购 (u04)
('u04', '2020-02-03 08:00:00', 'dress_03', 'women', 1),
('u04', '2020-02-20 10:00:00', 'skirt_01', 'women', 2),
('u04', '2020-03-01 09:00:00', 'bag_02',   'women', 1),
-- 2020-02 B类 (u05)
('u05', '2020-02-08 12:00:00', 'shirt_03', 'women', 1),
('u05', '2020-02-08 12:05:00', 'pants_03', 'men',   2),
-- 2020-02 C类：首单只买 kids (u06)
('u06', '2020-02-12 13:00:00', 'toy_02',   'kids',  1),
('u06', '2020-02-23 15:00:00', 'toy_03',   'kids',  1),
-- 2020-02 C类：首单只买 young (u07)
('u07', '2020-02-12 14:00:00', 'jeans_01', 'young', 1),
-- 2020-03 A类：大量复购 (u08)
('u08', '2020-03-05 10:00:00', 'dress_04', 'women', 1),
('u08', '2020-03-06 11:00:00', 'dress_05', 'women', 1),
('u08', '2020-03-07 12:00:00', 'skirt_02', 'women', 1),
('u08', '2020-03-10 13:00:00', 'bag_03',   'kids',  1),
('u08', '2020-03-12 14:00:00', 'toy_04',   'young', 1),
-- 2020-03 C类 (u09)
('u09', '2020-03-18 09:00:00', 'pants_04', 'men',   1),
-- 2020-03 B类 (u10)
('u10', '2020-03-20 10:00:00', 'dress_06', 'women', 1),
('u10', '2020-03-20 10:05:00', 'pants_05', 'men',   1);

-- ==========================================
-- 用户回访表
-- ==========================================
DROP TABLE IF EXISTS t2_user_visit_di;
CREATE TABLE t2_user_visit_di (
    user_id VARCHAR(64),
    dt      VARCHAR(8)
);
COMMENT ON TABLE t2_user_visit_di IS '用户回访日志表';
COMMENT ON COLUMN t2_user_visit_di.user_id IS '用户ID';
COMMENT ON COLUMN t2_user_visit_di.dt IS '浏览日期（yyyymmdd格式）';

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
-- u09: 首单 2020-03-18，30天后回访
('u09', '20200410'),
-- u99: 2019年老用户回访
('u99', '20200215');

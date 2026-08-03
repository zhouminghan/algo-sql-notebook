-- ============================================================
-- SQL02-SHEIN新客回访复购分析 · DDL + 测试数据（归档）
-- 原始来源: db/init/02-shein.sql
-- PG COMMENT ON 语法已转换为行内注释（兼容 MySQL / SQLite）
-- ============================================================

CREATE TABLE t2_shein_orders (
  id SERIAL PRIMARY KEY,          -- 自增主键
  user_id VARCHAR(10) NOT NULL,       -- 用户ID
  order_id VARCHAR(20) NOT NULL,      -- 订单ID
  order_date DATE NOT NULL,           -- 下单日期
  amount DECIMAL(10,2) NOT NULL       -- 订单金额
);

INSERT INTO t2_shein_orders (user_id, order_id, order_date, amount) VALUES
  ('u01', 'ORD001', '2024-01-01', 150.00),
  ('u01', 'ORD002', '2024-01-05', 200.00),
  ('u01', 'ORD003', '2024-02-01', 120.00),
  ('u02', 'ORD004', '2024-01-01', 80.00),
  ('u02', 'ORD005', '2024-01-10', 90.00),
  ('u03', 'ORD006', '2024-01-15', 300.00),
  ('u03', 'ORD007', '2024-01-20', 50.00),
  ('u03', 'ORD008', '2024-02-05', 180.00);

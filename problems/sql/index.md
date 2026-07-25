# 🗄️ SQL 高级场景题 — 完整索引

> 30 道高频 SQL 场景题，覆盖窗口函数、连续问题、留存分析、漏斗分析等。
> 标记：⏳ 待做 | 🔥 进行中 | ✅ 已掌握 | ⚠️ 需复习 | ❌ 不会
>
> **建表规范**：题号 N → 表名 `tN_xxx`；同一题多表 → `tN_1_xxx`, `tN_2_xxx`

---

## 🐳 Docker MySQL 环境

```bash
# 启动 MySQL（首次自动建表+灌数据）
docker compose up -d

# 连接
mysql -h 127.0.0.1 -u root -p123456 sql_practice

# 做题 — 复制 .sql 文件内容粘贴到 mysql 终端

# 停止
docker compose down
```

## 📂 目录结构

```
SQL高级场景/
├── docker-compose.yml                    # MySQL 8.0，端口 3306
├── init/                                 # 每题一个建表文件
│   ├── 01-login.sql                      # SQL01 建表 + 数据
│   └── 02-xxx.sql                        # SQL02（新增时创建）
├── index.md                              # 题目索引
└── SQL01-连续登录天数/
    ├── README.md                         # 微信风格文章
    ├── SQL01-连续登录天数.sql              # 做题模板
    └── SQL01-answer.sql                  # 参考答案
```

新加题目时：在 `init/` 下新建 `02-xxx.sql`（建表+DATA）→ `docker compose down -v && docker compose up -d` 重建。

---

## 一、窗口函数专题（8题）

| # | 场景 | 核心考点 | 状态 |
|---|------|---------|------|
| SQL01 | 连续登录天数 | `ROW_NUMBER` + `DATE_SUB` 分组技巧 | ⏳ |
| SQL02 | 用户最大连续下单天数 | 同上 + 分组聚合 | ⏳ |
| SQL03 | 行转列 / 列转行 | `CASE WHEN` + `UNION ALL` / `LATERAL VIEW EXPLODE` | ⏳ |
| SQL04 | TopN 问题（每个分组取前N） | `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)` | ⏳ |
| SQL05 | 累计求和（截止每天的总量） | `SUM() OVER(ORDER BY ...)` | ⏳ |
| SQL06 | 环比/同比计算 | `LAG` / `LEAD` 窗口函数 | ⏳ |
| SQL07 | 移动平均（近7天均值） | `AVG() OVER(ROWS BETWEEN ...)` | ⏳ |
| SQL08 | 分组内排名（并列/不并列） | `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` | ⏳ |

## 二、留存 & 漏斗分析（6题）

| # | 场景 | 核心考点 | 状态 |
|---|------|---------|------|
| SQL09 | 次日/3日/7日留存率 | `LEFT JOIN` + 日期计算 | ⏳ |
| SQL10 | 新用户留存曲线 | 首日 `MIN(date)` + 留存计算 | ⏳ |
| SQL11 | 转化漏斗分析 | 多步骤 `COUNT(DISTINCT)` 聚合 | ⏳ |
| SQL12 | 用户行为路径分析 | `LAG` + 路径拼接 | ⏳ |
| SQL13 | 沉默用户唤醒分析 | 最后活跃日期 + 时间差 | ⏳ |
| SQL14 | 同期群分析（Cohort） | 首月分组 + 逐月留存 | ⏳ |

## 三、复杂 Join & 子查询（5题）

| # | 场景 | 核心考点 | 状态 |
|---|------|---------|------|
| SQL15 | 好友关系（共同好友） | 自连接 + `INTERSECT` | ⏳ |
| SQL16 | 部门工资前三高 | `DENSE_RANK` + 子查询 | ⏳ |
| SQL17 | 行程取消率 | 多表 JOIN + 条件聚合 | ⏳ |
| SQL18 | 体育馆人流量高峰 | 连续条件 + 自连接 | ⏳ |
| SQL19 | 树节点类型判断 | `CASE WHEN` + 子查询 | ⏳ |

## 四、数据倾斜 & 性能优化（5题）

| # | 场景 | 核心考点 | 状态 |
|---|------|---------|------|
| SQL20 | JOIN 数据倾斜处理 | 热点Key打散 / MapJoin | ⏳ |
| SQL21 | 大表 JOIN 小表优化 | Broadcast Join / Map Join | ⏳ |
| SQL22 | GROUP BY 数据倾斜 | 两阶段聚合 / 随机前缀 | ⏳ |
| SQL23 | COUNT DISTINCT 优化 | 先 GROUP BY 再 COUNT | ⏳ |
| SQL24 | 笛卡尔积规避 | 关联条件检查 | ⏳ |

## 五、实际业务场景（6题）

| # | 场景 | 核心考点 | 状态 |
|---|------|---------|------|
| SQL25 | 直播间同时在线峰值 | 进入/离开事件 + `SUM` 累加 | ⏳ |
| SQL26 | 用户消费分群（RFM模型） | 多维度打分 + `CASE WHEN` | ⏳ |
| SQL27 | 订单对账（多源数据核对） | `FULL OUTER JOIN` | ⏳ |
| SQL28 | AB实验指标计算 | 分组聚合 + 统计检验思路 | ⏳ |
| SQL29 | 拉链表设计与查询 | 时间区间查询：`start_date <= x < end_date` | ⏳ |
| SQL30 | 数仓分层场景 SQL | ODS→DWD→DWS→ADS 典型 SQL | ⏳ |

---

## 📊 统计

| 分类 | 题数 |
|------|------|
| 窗口函数 | 8 |
| 留存 & 漏斗 | 6 |
| 复杂 Join | 5 |
| 性能优化 | 5 |
| 实际业务 | 6 |

## 🎯 做题顺序建议

1. **先过窗口函数**（SQL01-SQL08）— 这是 SQL 面试的绝对核心
2. **再做留存/漏斗**（SQL09-SQL14）— 高频业务场景
3. **攻克复杂 Join**（SQL15-SQL19）— 考察 SQL 功底
4. **理解性能优化**（SQL20-SQL24）— 加分项
5. **过一遍业务场景**（SQL25-SQL30）— 综合应用

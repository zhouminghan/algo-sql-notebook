---
name: sql-to-page
description: |
  将 SQL 题 Markdown（problems/sql/）渲染为交互式 HTML 页面。
  Trigger：用户说「生成 SQL 题页面」「渲染一道 SQL 题」「sql-to-page」「入库」等。
---

# sql-to-page Skill

将 `problems/sql/` 下的 Markdown 题目文件渲染为 `output/sql/` 下的交互式 HTML 页面。

## 流程

### 输入

- `problems/sql/{problem_id}.md`（必读：本章的「Markdown 节结构」规范）
- `problems/sql/{problem_id}-answer.sql`（参考答案）
- `db/init/{NN}-{name}.sql`（建表 + 测试数据，必读：本章的「Init SQL 规范」）

### 输出

- `output/sql/{problem_id}.html`

### 步骤

1. **搜索原题**：用 agent-reach 获取原题描述和期望输出（网络搜索/小红书/面经等）
2. **创建 Markdown**：按本章「Markdown 节结构」创建 `problems/sql/{problem_id}.md`，缺段必补
3. **创建建表 SQL**：按本章「Init SQL 规范」创建 `db/init/{NN}-{name}.sql`
4. **创建答案 SQL**：`problems/sql/{problem_id}-answer.sql`
5. **更新索引**：`problems/sql/index.md` 中更新对应行
6. **运行渲染**：
   ```bash
   cd /Users/minghan/Documents/knowledge/workspace/algo-practice
   python render.py {problem_id}
   ```
7. **验证**：确认 `output/sql/{problem_id}.html` 已生成，且：
   - 场景描述完整
   - 领域知识区块存在（有表格则展开检查）
   - 表结构显示所有表（多表场景检查每个表都有）
   - 示例数据按表分组，行数和列数正确
   - 期望结果表格完整
   - 解题思路和参考答案折叠正常

## 题目规范

### 表命名规范

- 题号 N → 表名 `tN_xxx`
- 同一题多表 → `tN_1_xxx`, `tN_2_xxx`

### 建表文件

- `db/init/{NN}-{name}.sql`，其中 NN 为两位数题号
- 支持多张表：多个 `CREATE TABLE` + 各自 `INSERT INTO`，render.py 自动按表分组解析

---

## Markdown 节结构（强制格式）

每个 SQL 题 Markdown 必须包含以下 7 节，顺序固定：

```
# SQL{NN} — {题目名称}
> {标签1} + {标签2} | 🔴/🟡/🟢 {难度} | {分类}

---

## 一、建表语句与测试数据
（展示建表 SQL + INSERT，实际数据在 db/init/XX-xxx.sql 中）

---

## 二、题目描述
（场景 + 表字段 + 需求 + 输出格式）

---

## 领域知识
（业务术语表格，至少 4 个术语，格式见下）

---

## 三、解题思路
（分步讲解，8步以内）

---

## 四、最终 SQL
（完整参考答案）

---

## 五、执行结果示例
（期望输出表格 + 结果解读）

---

## 六、常见坑点与扩展
（至少 3 条坑点 + 扩展场景）
```

### 领域知识节格式

```markdown
## 领域知识

> 本题涉及 {领域} 中的多个专业术语。

| 术语 | 全称 | 本题语境 |
|------|------|---------|
| {术语} | {英文全称} | {1-2句话说明在本题目中的具体含义} |
```

- **最少 4 个术语**，最多 8 个
- 说明必须包含「本题中」的具体语境
- 涉及计算公式的术语（如复购率、留存率）必须写出公式
- 表格用 `|------|------|---------|` 分隔行（会被 render.py 自动过滤）
- 前端渲染为折叠块「📖 领域知识」，默认折叠

### Init SQL 规范

```sql
-- ==========================================
-- SQL{NN}: {题目名称}
-- ==========================================
DROP TABLE IF EXISTS t{N}_xxx;
CREATE TABLE t{N}_xxx (
    col1  VARCHAR(64),
    col2  DATETIME,
    ...
);
COMMENT ON TABLE t{N}_xxx IS '表说明';
COMMENT ON COLUMN t{N}_xxx.col1 IS '列说明';

INSERT INTO t{N}_xxx VALUES
-- 注释说明（括号不被解析）
('val1', 'val2', ...),
('val1', 'val2', ...);

-- 多表场景：继续 DROP + CREATE + INSERT
DROP TABLE IF EXISTS t{N}_yyy;
...
```

**关键约束**：
- SQL 注释用 `-- ` 开头（render.py 会过滤注释行，避免注释中的括号被误解析）
- 每个表一个 `INSERT INTO` 语句
- `DROP TABLE IF EXISTS` 放在 `CREATE TABLE` 前面
- PostgreSQL COMMENT 可选但推荐添加

---

## 验收清单

- [ ] Markdown 7 节完整，顺序正确
- [ ] 领域知识 ≥ 4 个术语，每个含全称 + 本题语境
- [ ] Init SQL 每个表有独立 INSERT，注释行用 `--` 开头
- [ ] 答案 SQL 文件存在且可直接执行
- [ ] `python render.py {problem_id}` 无报错
- [ ] 输出 HTML 中表结构显示所有表
- [ ] 示例数据按表分组、列数正确、无多余行
- [ ] 领域知识折叠块无分隔行残留

## 用例

```
用户：把 SQL01-连续登录天数 渲染成 SQL 题页面
AI：检查 problems/sql/SQL01-连续登录天数.md → 格式完整 → render.py SQL01-连续登录天数 → 确认 output/sql/SQL01-连续登录天数.html 已生成
```

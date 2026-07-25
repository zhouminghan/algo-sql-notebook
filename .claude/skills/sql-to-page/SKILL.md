---
name: sql-to-page
description: |
  将 SQL 题 Markdown（problems/sql/）解析为 JSON，
  然后运行 render.py 渲染成 output/sql/*.html。
  Trigger：用户说「生成 SQL 题页面」「渲染一道 SQL 题」「sql-to-page」等。
---

# sql-to-page Skill

将 `problems/sql/` 下的 Markdown 题目文件渲染为 `output/sql/` 下的交互式 HTML 页面。

## 流程

### 输入

- `problems/sql/{problem_id}.md`（格式见 `.claude/CLAUDE.md` 中的「SQL 题 Markdown」规范）
- `problems/sql/{problem_id}-answer.sql`（参考答案）
- `db/init/XX-xxx.sql`（建表 + 测试数据，见 `.claude/CLAUDE.md` 中的格式规范）

### 输出

- `output/sql/{problem_id}.html`

### 步骤

1. **检查并补全 Markdown**：确认题目包含必需段落（场景描述、解题思路、关键点）。
   - 如缺少某段，根据题目内容补充。
2. **确认建表 SQL**：检查 `db/init/` 下是否有对应的初始化文件，如无则新建。
3. **确认答案 SQL**：检查 `problems/sql/{problem_id}-answer.sql`，如无则补充。
4. **运行渲染**：
   ```bash
   cd /Users/minghan/Documents/knowledge/workspace/algo-practice
   python render.py {problem_id}
   ```
5. **验证**：确认 `output/sql/{problem_id}.html` 文件已生成且不为空。

## 题目规范

### 表命名规范

- 题号 N → 表名 `tN_xxx`
- 同一题多表 → `tN_1_xxx`, `tN_2_xxx`

### 建表文件

- `db/init/{NN}-{name}.sql`，其中 NN 为两位数题号

## 用例

```
用户：把 SQL01-连续登录天数 渲染成 SQL 题页面
AI：检查 problems/sql/SQL01-连续登录天数.md → 格式完整 → render.py SQL01-连续登录天数 → 确认 output/sql/SQL01-连续登录天数.html 已生成
```

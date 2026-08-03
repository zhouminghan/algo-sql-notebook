# Algo Practice · 操作协议 v3.0

## 架构

**纯静态 + 共享模板** — Markdown → render.py → HTML。

```
frontend/
├── shared/
│   ├── base.css       ← CSS变量 + 布局 + Modal + 分割条 + 响应式
│   ├── progress.js    ← localStorage 进度（algo/sql 共用）
│   └── splitter.js    ← 双面板拖拽（algo/sql 共用）
├── algo/
│   └── template.html  ← 算法特有：双语言编辑器 + walkthrough
├── sql/
│   └── template.html  ← SQL 特有：SQL编辑器 + DDL + 表格walkthrough
└── index.html
```

修复 shared/ 中的文件 → 算法和 SQL 模板同时生效。

无 Docker、无 PostgreSQL、无 FastAPI。

## 入口

计划文件（唯一真相来源）：
`/Users/minghan/Documents/brain/wiki/1-Projects/每日一题交互式刷题平台.md`

## Harness（验证器，不参与产出）

```
Layer 1: python verify.py          ← 静态检查（括号/占位符/结构）
Layer 2: agent-browser             ← 浏览器截图 + console 错误检查
Layer 3: python -m http.server     ← 冒烟测试（HTTP 200）
```

验证器 = CLI exit code（0 或非 0），不靠 LLM 自评。

## 自测闭环（Loop）

```
1. 写代码 / 改模板
2. python render.py
3. python verify.py
   ├── exit ≠ 0 → 读 stderr → 定位 → 修复 → 回到 2（最多 3 轮）
   └── exit = 0 ↓
4. 启动 server.py + agent-browser 截图
   ├── 有 console error → 定位 → 修复 → 回到 2
   └── 无 console error ↓
5. 完成
```

**禁止**：不跑 verify 就说"修好了"；同一错误连修两次不换策略；脑补渲染结果。

## 渲染命令

- 算法题：`python render.py 001-两数之和`
- SQL 题：`python render.py SQL01-连续登录天数`
- walkthrough JSON：`python render.py SQL01-连续登录天数 -w output/SQL01-连续登录天数-walkthrough.json`
- 全量渲染：`python render.py`

## Walkthrough 规则

```
output/{problem_id}-walkthrough.json (pre-computed)
  ├── 算法题：{ steps: [{hint, line, status, num, comp, seen, idx}] }
  └── SQL 题： { db_init_sql: "...", steps: [{label, desc, sql, columns, rows, hl}] }

算法题生成函数在 render.py 的 _WALKTHROUGH_GENERATORS 表中。
SQL 题 walkthrough JSON 必须手动 pre-compute。
```

## 单题闭环

```
1. 确定题目 → 写 problems/{type}/{PID}.md
2. python render.py PID
3. python verify.py
4. verify 失败 → 读 stderr → 定位 → 修复 → 回到 2（最多 3 轮）
5. 通过 → 下一题
```

## 限制

- 模板改 shared/ 文件 → 两个模板同时生效
- SQL 纯静态（无在线执行），DDL 复制到本地验证
- 进度用 `shared/progress.js`（localStorage），无 API 依赖
- `render.py` 不连接 PostgreSQL

## 已验证模块

| 模块 | 文件 |
|------|------|
| 渲染引擎 | render.py (MD直驱) |
| 共享样式 | frontend/shared/base.css |
| 共享进度 | frontend/shared/progress.js |
| 共享分割条 | frontend/shared/splitter.js |
| 算法模板 | frontend/algo/template.html |
| SQL 模板 | frontend/sql/template.html |
| 首页 | frontend/index.html |
| CodeMirror | frontend/lib/ (已本地化) |
| 验证脚本 | verify.py |
| 开发服务器 | server.py |
| Walkthrough JSON | output/*-walkthrough.json |

## 待做（按优先级）

1. agent-browser 自测闭环实际部署（Layer 2）
2. 前 5 道算法题批量生成
3. 余下 95 道算法题批量生成
4. walkthrough JSON 全部 pre-compute
5. CSS Grid 表格动画
6. SVG 图标

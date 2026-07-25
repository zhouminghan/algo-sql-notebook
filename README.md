# 📅 每日一题

> 力扣 Hot 100 算法题 + SQL 高级场景题，Docker 本地部署交互式刷题平台。
> 开始日期：2026-07-22
> 📋 计划文档：[每日一题交互式刷题平台](../../wiki/1-Projects/每日一题交互式刷题平台.md)

---

## 🚀 快速开始

```bash
# 1. 启动平台
docker compose up -d

# 2. 打开浏览器
open http://localhost:3000

# 3. 初始化 SQL 表（首次启动后执行一次）
curl -X POST http://localhost:3000/api/sql/init-tables
```

---

## 📂 目录结构

```
algo-practice/
├── docker-compose.yml          # PostgreSQL + FastAPI
├── web/
│   ├── main.py                 # FastAPI 后端
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html              # 首页（进度概览 + 题目列表）
│   ├── algo/
│   │   ├── template.html       # 算法题通用模板
│   │   └── fallback.html       # 未渲染时的回退页
│   └── sql/
│       ├── template.html       # SQL 题通用模板
│       └── fallback.html
├── problems/                   # 题目源文件（Markdown）
│   ├── algo/                   # 算法题（100道）
│   └── sql/                    # SQL 题（30道）
├── db/init/                    # SQL 建表 + 测试数据
├── output/                     # 渲染输出（HTML + progress.json）
│   ├── algo/
│   ├── sql/
│   └── progress.json
├── render.py                   # Markdown → HTML 渲染引擎
└── .claude/                    # Agent 配置
    ├── CLAUDE.md
    └── skills/
```

---

## 🔄 工作流

### 新加算法题

1. 在 `problems/algo/` 下创建 `001-题目名.md`
2. 按规范填写（题目描述 + 解题思路 + Python/Java 解法 + 关键点 + 易错点）
3. 运行 `python render.py 001-题目名` 生成 HTML
4. 访问 `http://localhost:3000/algo/001-题目名`

### 新加 SQL 题

1. 在 `problems/sql/` 下创建 `SQL01-题目名.md`
2. 在 `db/init/` 下创建对应的建表文件（如 `01-login.sql`）
3. 在 `problems/sql/` 下创建答案文件 `SQL01-题目名-answer.sql`
4. 运行 `python render.py SQL01-题目名` 生成 HTML
5. 运行 `curl -X POST http://localhost:3000/api/sql/init-tables` 重建表
6. 访问 `http://localhost:3000/sql/SQL01-题目名`

### 渲染全部题目

```bash
python render.py
```

---

## 📊 进度

| 模块 | 已完成 | 总题数 | 进度 |
|------|--------|--------|------|
| 力扣 Hot 100 | 1 | 100 | 1% |
| SQL 高级场景 | 1 | 30 | 3% |

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 容器编排 | Docker Compose |
| 后端 | Python FastAPI + asyncpg |
| 数据库 | PostgreSQL 16 |
| 前端 | 原生 HTML/CSS/JS（零依赖） |
| 渲染 | Python（render.py，模板替换） |

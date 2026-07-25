# Algo Practice · 操作协议

## 入口

计划文件（唯一真相来源）：
`/Users/minghan/Documents/brain/wiki/1-Projects/每日一题交互式刷题平台.md`

## 核心规则

1. **先读计划** → 再写代码。计划在 Obsidian。
2. **改完就跑** `python verify.py`，exit 0 才算完。
3. 提交时不关 Docker。模板/output 是 volume 挂载，**不需要 `--build`**。
4. 每次改动必须在 Obsidian plan 中追加「落地记录」。

## 单题闭环（每道算法题）

```
1. 根据 index.md 确定题目 → web_search 获取原题描述/题解 → 写 problems/algo/XXX.md
2. python render.py XXX-题目名
3. python verify.py
4. verify 失败 → 读 stderr → 定位 → 修复 → 回到第2步（最多3轮）
5. 通过 → 下一题
```

## 批量闭环

```
1. 逐题循环上述流程
2. 同题3轮不过 → 跳过 → 记入 .codebuddy/ISSUES.md
3. 全部完成 → 报告统计（成功/跳过/耗时）
```

## 禁止行为

- 不跑 verify 就说"修好了"
- 不读 stderr 就重试（同一错误连修两次不换策略）
- 自己脑内"估计"渲染结果（必须执行 CLI）

## 已验证模块

| 模块 | 文件 |
|------|------|
| Docker | docker-compose.yml, web/Dockerfile |
| FastAPI | web/main.py (6端点) |
| PostgreSQL | db/init/ (2题建表) |
| 渲染引擎 | render.py (MD直驱) |
| 算法模板 | frontend/algo/template.html |
| SQL 模板 | frontend/sql/template.html |
| 首页 | frontend/index.html |
| CodeMirror | frontend/lib/ (已本地化) |
| 验证脚本 | verify.py |
| 问题记录 | .codebuddy/ISSUES.md |
| Algo Skill | .codebuddy/skills/algo-to-page/SKILL.md |
| SQL Skill | .codebuddy/skills/sql-to-page/SKILL.md |

## 待做（按优先级）

1. 前5道算法题批量生成（闭环验证）
2. 余下95道算法题批量生成
3. walkthrough JSON 外置化（去硬编码）
4. CSS Grid 表格动画
5. SVG 图标

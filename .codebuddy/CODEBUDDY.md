# Algo Practice · 每日一题刷题平台

## 核心规则

- **先读计划，再写代码**。计划文件在 Obsidian：`/Users/minghan/Documents/brain/wiki/1-Projects/每日一题交互式刷题平台.md`
- 每次改动必须同步更新 Obsidian 计划文件中的「落地记录」章节
- 改完代码必须跑 `python verify.py`，通过才能提交
- 提交时不关 Docker（页面不中断）
- 模板/output 是 volume 挂载，**不需要 `--build`**，只需 `python render.py`
- `.codebuddy/ISSUES.md` 记录已修复的 bug + 根因 + 验证方式，避免重复

## 当前架构（简化版）

```
problems/algo/XXX.md  →  render.py  →  output/algo/XXX.html
problems/sql/XXX.md   →  render.py  →  output/sql/XXX.html
                                ↘  PostgreSQL（SQL walkthrough 真实数据）
```

- Markdown 直驱渲染，跳过 JSON 中间层
- CodeMirror 走 CDN（有 fallback 降级）
- 弹窗播放器（算法代码行高亮 + SQL 表格步骤）
- 拖拽分隔线（左右面板 + SQL 编辑器/结果区）

## 已验证的功能

| 功能 | 状态 |
|------|:--:|
| Docker + FastAPI + PostgreSQL | ✅ |
| 算法题模板（CodeMirror + 查看题解 + 步骤演示） | ✅ |
| SQL 题模板（CodeMirror + 真执行 + 步骤播放器） | ✅ |
| 弹窗步骤播放器（算法代码步进 + SQL 5步法） | ✅ |
| 首页列表 + 进度条 + 难度过滤 | ✅ |
| 自动验证脚本 verify.py | ✅ |
| 已知问题记录 ISSUES.md | ✅ |

## 待执行

- Day 7: 批量生成 99 道算法题
- SQL 分步动画增强（CSS Grid 表格过渡）

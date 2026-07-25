---
name: algo-to-page
description: |
  将算法题 Markdown（problems/algo/）解析为 JSON，
  然后运行 render.py 渲染成 output/algo/*.html。
  Trigger：用户说「生成算法题页面」「渲染一道算法题」「algo-to-page」等。
---

# algo-to-page Skill

将 `problems/algo/` 下的 Markdown 题目文件渲染为 `output/algo/` 下的交互式 HTML 页面。

## 流程

### 输入

- `problems/algo/{problem_id}.md`（格式见 `.claude/CLAUDE.md` 中的「算法题 Markdown」规范）

### 输出

- `output/algo/{problem_id}.html`

### 步骤

1. **检查并补全 Markdown**：确认题目包含所有必需段落（题目描述、解题思路、Python 解法、Java 解法、关键点、易错点）。
   - 如缺少某段，根据题目内容补充。
2. **运行渲染**：
   ```bash
   cd /Users/minghan/Documents/knowledge/workspace/algo-practice
   python render.py {problem_id}
   ```
3. **验证**：确认 `output/algo/{problem_id}.html` 文件已生成且不为空。

## 题目规范

见 `.claude/CLAUDE.md` 中的「题目格式规范」。

## 用例

```
用户：把 001-两数之和 渲染成 HTML
AI：检查 problems/algo/001-两数之和.md → 格式完整 → 运行 python render.py 001-两数之和 → 确认 output/algo/001-两数之和.html 已生成
```

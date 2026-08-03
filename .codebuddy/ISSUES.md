# 已知问题清单 & 避坑记录

> 每次修复一个 bug 后记录在这里，避免重复犯同样的错误。

## 用户反馈（2026-07-26）

### 1. 描述中的 `` `code` `` 未渲染
- 用户原话：「题目给定整数数组numbers，这里的这个numbers这个代码块并没有成功地做一个渲染」
- 根因：`parse_algo_md` 只做了 `escape_html` 没做 `_inline_md`
- 修复：`escape_html(desc_clean)` → `_inline_md(escape_html(desc_clean))`

### 2. walkthrough 表格匹配检测 bug + 列太碎
- 用户原话：「这里的这个表格，什么索引啊，Numbers I呀，补数啊，看起来怪怪的」
- 根因：第一轮循环没存储 seen，found_step 永远为 -1，匹配永不被检测
- 修复：第一轮加 `seen[n] = i`，第二轮前重置 `seen = {}`
- 表头简化：6列→5列（#/当前值/补数/seen/结果），合并索引+值列

### 3. 左右部署局调整
- 用户原话：「解题思路对比可以挪到右侧」
- 已移至右面板，答案折叠区→关键点之间

### 5. 关键点/易错点 `**加粗**` 未渲染
- 用户原话：「关键点这边也有markdown的那种加粗的那种引号展示」
- 修复：keypoints/gotchas 都加 `_inline_md()` 转换

### 6. 弹窗未显示测试用例 + 上下布局
- 用户原话：「播放没有指明输入和输出... 代码块下面是一个空白的地方」
- 修复：steps JSON 加 `example` 字段，弹窗顶部显示测试用例
- 布局：左右→上下（代码35%上，步骤65%下，不留空白）

---

## 已修复 · 已验证

### 1. 示例数据表头显示「列1」「列2」
- **根因**: `parse_init_sql_data` 写死了通用列头
- **修复**: 合并到 `parse_init_sql_schema_and_data`，从 CREATE TABLE 取真实列名
- **验证**: `verify.py` 检查 `table-info` 元素存在

### 2. 答案双重 `<pre>` 标签
- **根因**: `render.py` 多包了一层 `<pre>`
- **修复**: 去掉 render.py 的 `<pre>`，只在模板中包一层
- **验证**: `verify.py` 检查 `<pre><pre>` 不存在

### 3. Java 模板花括号不配对
- **根因**: `extract_code_template` 没有补 class 闭花括号
- **修复**: 在 method_done 后补 `}` 
- **验证**: 肉眼检查

### 4. MySQL COMMENT 语法 → PostgreSQL
- **根因**: `db/init/01-login.sql` 用了 MySQL COMMENT 语法
- **修复**: 改为 `COMMENT ON TABLE/COLUMN` 语法
- **验证**: Docker 启动不报错

### 5. CodeMirror CDN 不可用时页面报错
- **根因**: 没有 fallback
- **修复**: `hasCM` 检查 + 降级为 textarea
- **验证**: 模拟 CDN 不可用

### 6. SQL 宽表溢出边框
- **根因**: 表格没有 overflow 处理
- **修复**: `.expected-table` / `.table-info` 加 `overflow-x:auto`
- **验证**: 肉眼检查 SQL02 8列表格

### 7. SQL 描述中 Markdown 未渲染
- **根因**: 简单按行 `<p>` 输出，不支持列表/表格/粗体
- **修复**: `_parse_md_description` 完整 MD 子集解析
- **验证**: `verify.py` 检查 scenario 内无 `**` 原始标记

### 8. 查看题解 + Tab切换后 Java 答案空白
- **根因**: `switchLang` 没 refresh 答案编辑器
- **修复**: 切 Tab 时如果答案面板开着就 refresh
- **验证**: 手动测试

### 9. 播放按钮不显示
- **根因**: JS 条件隐藏逻辑 + 浏览器缓存
- **修复**: 按钮始终显示 + `openPlayback` 处理缺失数据 + 页面底部 console.log 版本时间戳
- **验证**: `verify.py` 检查 `playback-trigger` 存在

---

## 待修复

（暂无）

---

## 调试技巧

1. **改完代码后跑 `python verify.py`**，检查所有页面
2. **看页面是否最新版**: 打开浏览器控制台，搜索 `page build`，对比 `python render.py` 的输出时间
3. **强制刷新**: Cmd+Shift+R（Mac）/ Ctrl+Shift+R（Windows）
4. **Docker 不需要 `--build`**：模板和 output 是 volume 挂载的，只需 `python render.py`

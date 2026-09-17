# algo-sql-notebook

**算法 + SQL 图解题库** · 每题一页 · 图解优先 · 纯静态零构建 · 可离线打开

🌐 在线访问：<https://zhouminghan.github.io/algo-sql-notebook/>

---

## 内容

| 分区 | 题量 | 来源 | 每题包含 |
|------|------|------|----------|
| 算法 | 100 | LeetCode Hot 100 | 为什么用这个思路 / 题目描述 / **N 帧图解** / Python + Java 最优解 / 复杂度 / 易错点 / 自我检验 |
| SQL | 6 | 字节 · SHEIN · B 站机试题 | 业务背景 / 源数据表 / **N 帧 CTE 拆解** / 完整答案 / 易错点 / 举一反三 / 本地复现 DDL |

「图解即思路」是本站的重点：SQL 题的每一帧 = 一个 CTE 定义 + 一张分区着色的结果表，
所有帧的代码按顺序拼接就是完整答案；算法题用链表 / 树 / 指针 / DP 表等 SVG 图示分步演示。

## 页面能力

- **左侧分类导航**：算法 / SQL 两个 Tab，按分类分组（哈希、双指针、动态规划…），显示每题完成状态
- **搜索**：侧栏搜索框支持题目 / 分类 / 标签，`/` 快捷键聚焦；**一次搜索会同时搜算法和 SQL**，
  命中结果按题库分区列出，Tab 上的数字会变成命中数
- **右侧本页目录**：宽屏（≥1240px）显示，滚动自动高亮当前分节
- **主题**：亮 / 暗双主题，跟随系统 + 手动记忆
- **阅读进度**：打开过的题目标记 ✓，顶栏显示「已读 x / 106」；分类标题上显示「已读 x/y」，
  点顶栏进度可以「全部标为已读 / 重置进度」
- **代码复制**：一键复制，Python / Java 标签页切换
- **移动端**：侧栏变抽屉，正文单列，图解等比缩放
- **打印**：自动隐藏导航、展开折叠块、保留正文与图解与链接地址

## 本地预览

```bash
git clone https://github.com/zhouminghan/algo-sql-notebook.git
cd algo-sql-notebook
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

不需要安装任何依赖，也没有构建步骤 —— 直接打开 `index.html` 也能用（建议用上面的 http 方式，避免浏览器对本地文件的安全限制）。

## 目录结构

```
├── index.html                题库总览（算法/SQL Tab、难度筛选、分类卡片）
├── algo/  sql/               题目页面（生成产物，共 106 个）
├── assets/
│   ├── css/style.css         设计系统（全部 CSS 变量 + 组件样式）
│   ├── js/problems.js        题目元数据唯一数据源
│   ├── js/common.js          页面外壳（顶栏 / 侧栏 / 目录 / 主题 / 进度）
│   ├── js/draw-utils.js      SVG 图解库（20+ 绘图函数）
│   └── vendor/               highlight.js（本地化，离线可用）
├── scripts/
│   ├── algo_gen.py           算法题生成器   specs/algo/*.py  -> algo/*.html
│   ├── sql_gen.py            SQL 题生成器   specs/sql/*.html -> sql/*.html
│   ├── check_site.py         静态自检（结构 / 令牌 / head / 标题层级 / 分类词表）
│   ├── smoke.mjs             运行时冒烟（Playwright：全站页面 + 交互 + 断点 + 打印）
│   ├── test.sh               一条命令跑完上面两个门禁
│   ├── clean.sh              清理工作区里的本地垃圾（默认预览）
│   └── specs/                题目内容源（改内容只改这里）
├── 404.html                  GitHub Pages 404 兜底页
├── design-system/            UI/UX 设计系统（MASTER.md）
└── docs/design-system.md     设计系统落地说明
```

### 仓库卫生

`.gitignore` 只忽略「本地产生 / 可再生产」的东西：Python 缓存、`.codex/`（本地 skill 软链）、
`node_modules/`、编辑器与系统文件、日志与临时文件、`.env*`、虚拟环境。
**站点产物（`index.html`、`algo/`、`sql/`、`assets/`）必须入库** —— GitHub Pages 直接发布这份仓库。

```bash
bash scripts/clean.sh           # 预览工作区里的本地垃圾
bash scripts/clean.sh --force   # 清掉（默认已被 .gitignore 忽略）
```

`python3 scripts/check_site.py` 会校验 `.gitignore` 是否覆盖了常见垃圾类型，并在真的出现时提醒。

## 改内容 / 加题

- **改一道题的正文** → 编辑 `scripts/specs/algo/*.py` 或 `scripts/specs/sql/*.html`，然后重新生成
- **改题目信息**（题号 / 难度 / 标签 / 分类）→ 编辑 `assets/js/problems.js`
- **改外观 / 布局** → 编辑 `assets/css/style.css`，页面外壳逻辑在 `assets/js/common.js`
- 详细步骤、字段含义、验收清单见 **[AGENTS.md](AGENTS.md)**

```bash
python3 -m scripts.algo_gen     # 重新生成 100 道算法题（注意 -m）
python3 scripts/sql_gen.py      # 重新生成 6 道 SQL 题

# 跑门禁（二者都要过）
bash scripts/test.sh            # = 静态自检 + 运行时冒烟，一条命令
bash scripts/test.sh --fast     # 冒烟只抽 8 页，改小东西时用
```

也可以分开跑：`python3 scripts/check_site.py`（静态）、`node scripts/smoke.mjs`（运行时）。
冒烟测试用 Playwright 驱动 headless Chromium 直接跑 `file://` 页面，不需要先起服务器；
依赖定位顺序见 `AGENTS.md` 第 5 节。

## 设计系统

风格为 **Swiss / Minimalism**：克制的灰蓝配色、1px 分隔线、紧凑的 8px 间距体系、
清晰的排版层级，不依赖任何第三方 CSS 框架。

- 全部颜色 / 间距 / 圆角 / 阴影都是 `style.css` 顶部的 CSS 变量，亮暗两套
- 组件层只引用变量，不写死数值；`check_site.py` 会校验变量是否都有定义
- 令牌表与组件约定：**[docs/design-system.md](docs/design-system.md)**
- 由 `ui-ux-pro-max` skill 生成并持久化的原始设计系统：`design-system/algosql-notebook/MASTER.md`

## 技术栈

原生 HTML + CSS + JavaScript（ES5 语法，无框架、无打包、无 CDN 依赖）、
highlight.js 本地化、内联 SVG 绘图（颜色全部走 CSS 变量，自动适配亮暗主题）。

## 许可

个人学习笔记，题目版权归 LeetCode / 各公司原题所有。

# AGENTS.md —— 给 Codex / 其他 AI 助手的接手说明

本文件是**操作手册**：这个项目怎么组织、改东西要动哪几个文件、改完怎么验收。
面向读者的整体介绍在 `README.md`，视觉规范在 `docs/design-system.md`。

---

## 1. 项目是什么

`algo-sql-notebook` 是一个**纯静态、零构建**的题解站：

- 100 道 LeetCode Hot 100 算法题 + 6 道 SQL 机试题（字节 / SHEIN / B 站），共 **106 个题目页**
- 每题一个独立 URL（静态 HTML），可直接分享、离线打开、被搜索引擎收录
- 部署在 GitHub Pages，没有任何服务端、没有 npm、没有打包步骤

**硬约束（改动时不要破坏）**

| 约束 | 说明 |
|------|------|
| 零构建 | 不引入 webpack/vite/npm 依赖；浏览器直接跑源码 |
| 离线可用 | 不引外部 CDN、不引 webfont；第三方库放 `assets/vendor/` |
| 每题一页 | 不合并成单页 SPA，不把内容塞进一个 HTML |
| 内容与外壳分离 | 题目页里**只写正文**，导航/题头/目录由 `assets/js/common.js` 注入 |

---

## 2. 目录与「三份真相」

```
index.html                 题库总览（算法/SQL Tab + 难度筛选 + 分类卡片）
404.html                   GitHub Pages 的 404 兜底页（自包含路径处理）
algo/NNN-标题.html          算法题页面（生成产物，勿手改）
sql/NNN-标题.html           SQL 题页面（生成产物，勿手改）

assets/css/style.css       设计系统：全部 CSS 变量 + 全部组件样式
assets/favicon.svg         站点图标（所有页面 head 都引用它）
assets/js/problems.js      题目元数据唯一数据源（id/title/diff/tags/cat/file）
assets/js/common.js        页面外壳：顶栏、左侧栏、右侧目录、主题、进度、复制
assets/js/draw-utils.js    SVG 图解库（链表/树/DP 表/窗口函数/Join…）
assets/vendor/             highlight.js 及其主题（本地化）

scripts/algo_gen.py        算法题生成器（specs/algo/*.py  ->  algo/*.html）
scripts/sql_gen.py         SQL 题生成器（specs/sql/*.html  ->  sql/*.html）
scripts/check_site.py      静态自检：结构 / 令牌 / head / 标题层级 / 分类词表（提交前必跑）
scripts/smoke.mjs          运行时冒烟：Playwright 跑全部页面 + 交互 + 断点 + 打印
scripts/test.sh            一条命令跑完上面两个门禁（bash scripts/test.sh [--fast]）
scripts/clean.sh           清理工作区里的本地垃圾（默认预览，--force 才真删）
scripts/migrate_sql_pages.py  一次性迁移工具（历史手写页 -> 内容源，--force 才覆盖）

scripts/specs/algo/*.py    算法题内容源：题面/图解帧/代码/复杂度/易错点/自检
scripts/specs/sql/*.html   SQL 题内容源：正文 + 图解脚本（不含页面外壳）

design-system/algosql-notebook/MASTER.md   UI/UX 设计系统（ui-ux-pro-max skill 产出）
docs/design-system.md      设计系统在本项目的落地说明
```

**三份真相，各管一段，不要互相复制**

1. `assets/js/problems.js` —— 有哪些题、题号、难度、标签、分类、文件名
2. `scripts/specs/**` —— 每道题的正文内容
3. `assets/css/style.css` —— 长什么样

---

## 3. 页面外壳是怎么来的（关键设计）

题目页的 HTML 里**没有**导航栏、没有题头、没有目录。以 `algo/001-两数之和.html` 为例：

```html
<body>
<div class="why-box">…为什么用这个思路…</div>
<h3>题目描述</h3>
…
<script> /* 只负责把 SVG 图解画进 .frame-canvas */ </script>
</body>
```

`assets/js/common.js` 在运行时把它包成完整页面：

```
body
 ├── a.skip-link          键盘用户跳转到正文
 ├── header.topbar        品牌 / 已读进度 / 主题切换（移动端多一个汉堡按钮）
 ├── button.scrim         移动端抽屉遮罩
 └── div.shell            两栏网格
      ├── aside.sidebar   算法·SQL 两个 Tab + 分类分组 + 搜索
      └── main.main
           └── div.content-wrap
                ├── article.content      题头 + 正文 + 上一题/下一题
                └── aside.rail           ≥1240px 才显示：本页目录 + 题目信息
```

由此得到的推论：

- **改外壳只改 `common.js` / `style.css`**，106 个页面同时生效，不要逐个页面改
- 页面里出现 `<h1>`、`.topbar`、`.sidebar` 说明有人把外壳写进了正文，属于 bug
- **分节标题必须是 `<h2>`**（h1 = 题目标题，h3/h4 只能出现在 h2 之后）。正文的 `<h2>` 会被自动加上
  `id="sec-N"` 并生成右侧目录，所以**不要手动写 id**，也不要跳级
- 页面靠 `<meta name="asn-file" content="algo/001-…html">` 认领自己，缺了会导致侧栏不高亮、上下题错位
- 外壳注入的其它运行时能力：`#asn-live`（无障碍播报）、顶栏进度弹层（全部已读 / 重置）、
  `beforeprint` 展开折叠块、侧栏只滚自身容器（**不要用 `scrollIntoView`，会把整页拖下去**）

---

## 4. 常见任务

### 4.1 新增一道算法题

1. 复制 `scripts/specs/algo/` 里任一文件为 `NNN-标题.py`，填 `PROBLEM` 字典
   （字段：`id/title/diff/tags/leetcode/origin/why/desc/frames/conclusion/py/java/time/space/pitfalls/selfcheck`）
2. 在 `assets/js/problems.js` 的 `algo` 数组补一条（`id/title/diff/tags/cat`，`file` 由生成器回写）
3. 生成：`python3 -m scripts.algo_gen`（**必须用 `-m`**，spec 里有 `from scripts.algo_gen import frame`）
4. 自检：`python3 scripts/check_site.py`

图解帧用 `frame("帧标签", "drawTwoPointers", ...)`，可用函数见 `assets/js/draw-utils.js` 末尾的导出列表。

### 4.2 新增一道 SQL 题

1. 新建 `scripts/specs/sql/NNN-标题.html`：写正文（`<h3>` 分节 + `.frame-card` 图解帧 + 末尾一段 `<script>` 画图）
   - 可参考现有 6 个内容源；图解画布容器统一写成 `<div class="frame-canvas" id="frameN-svg"></div>`
2. 在 `assets/js/problems.js` 的 `sql` 数组补一条（`file` 必须与内容源同名，`cat` 用已有分类或新增）
3. 生成：`python3 scripts/sql_gen.py`
4. 自检：`python3 scripts/check_site.py`

### 4.3 改 UI / 新增组件

1. 先读 `docs/design-system.md`（令牌表 + 组件约定），必要时读 `design-system/algosql-notebook/MASTER.md`
2. **只用 CSS 变量**，不要写死颜色/间距；新增变量必须写进 `style.css` 的 `:root` 与 `[data-theme="dark"]`
3. 自检会校验「页面引用的 `var(--x)` 是否都有定义」，缺了会直接报错
4. 验收：见第 5 节

### 4.4 题目分类调整

分类顺序与中文名写死在 `assets/js/common.js` 顶部的 `CAT_ORDER`；题目归属写在 `problems.js` 的 `cat` 字段。
**新增分类必须同时改 `CAT_ORDER`**——`check_site.py` 会校验 `problems.js` 里的 `cat` 是否都在词表内，
拼错或漏声明会直接报错（而不是静默把分组丢到列表末尾）。

> SQL 目前只有 6 题，分类刻意保持粗粒度（窗口函数 3 / 多表 JOIN 1 / 自连接 1 / 过滤与聚合 1）；
> 题目变多时再按需拆分，不要为了「看起来均衡」硬拆。

---

## 5. 验收清单（改完必须跑）

```bash
# 1. 生成最新页面（改了内容源就要跑）
python3 -m scripts.algo_gen
python3 scripts/sql_gen.py

# 2. 门禁：静态自检 + 运行时冒烟（必须全绿）
bash scripts/test.sh            # 等价于下面两条
# python3 scripts/check_site.py
# node scripts/smoke.mjs        # 走 file:// 不需要起服务；--fast 抽 8 页

# 3. 本地预览（沙箱内需要授权 bind 端口）
python3 -m http.server 8000
```

自检覆盖：`problems.js` 字段与唯一性、页面存在性、`asn-file` 一致性、
本地资源与站内链接可达、内容源↔页面一一对应、CSS 变量可解析、不再引用 pico.css、
head 规范（favicon / og:title / highlight 必须 defer）、标题层级不跳级、
分类必须落在 `common.js` 的词表内、404 页存在且带 `<base>` 注入。

冒烟覆盖：106 页的外壳注入 / 图解渲染 / 目录生成 / 控制台无报错 / 首屏不被滚走 / 无横向溢出，
首页搜索（跨 Tab）与进度弹层、代码语言切换、目录滚动高亮、折叠块、主题切换，
四个断点的布局与移动端触控目标尺寸，以及打印（**自动挑出图解最多的 5 页** + 一道 SQL 题 + 首页，
逐页验证「折叠块自动展开 / 打印样式隐藏导航 / 图解不横向滚动 / 真能导出 PDF」）。

> Playwright 依赖定位顺序：`$PLAYWRIGHT_HOME` → 项目 `node_modules` → 本机 ChatGPT.app 内置运行时；
> Chromium 走 `$CHROME_EXE` 或 `~/Library/Caches/ms-playwright` 缓存。若报「找不到 playwright」，
> 用 `npm i -D playwright` 装一份即可，脚本不用改。

**视觉验收（自检过了不等于好看）**：至少看 4 个宽度 + 2 个主题

| 宽度 | 检查点 |
|------|--------|
| 1440px | 左侧栏 + 正文 + 右侧目录三栏；正文两侧留白对称，无大片空白 |
| 1024px | 右侧目录隐藏，正文居中；顶部进度条仍在 |
| 390px | 左侧栏变抽屉（汉堡按钮），正文单列，图解不缩放（宽表横向滚动） |
| 亮/暗 | 主题按钮切换即时生效；代码块、标签、图解在暗色下对比度正常 |

浏览器控制台必须无报错（`tab.dev.logs()`）。

---

## 6. 约定与坑

- **生成产物不要手改**：`algo/*.html`、`sql/*.html` 会被生成器覆盖；要改内容就改 `scripts/specs/**`
- **不要重排 `problems.js`**：生成器会读回并重写该文件（保持 JSON 结构 + `window.PROBLEMS =` 前缀）
- **不要引第三方 CSS 框架**：历史上用过 Pico.css，已下线；仓库自检会拦截重新引入
- **图标用内联 SVG**（`common.js` 的 `ICONS`），不要用 emoji
- **移动优先断点**：900px（抽屉）、1024px（侧栏不变窄）、1240px（出现右侧目录）
- **无障碍**：焦点必须可见（`:focus-visible`）、交互元素给 `aria-label`、目录高亮带 `aria-current`
- **标题层级**：h1 题目标题 → h2 分节 → h3/h4 子标题，不跳级（`check_site.py` 会拦）
- **触控目标**：移动端（≤900px）可点元素 ≥40px 高 —— 顶栏图标按钮、侧栏题目行、折叠块标题都在这个规则里；
  桌面端保持紧凑（34px 图标按钮、31px 行高）不要一起放大
- **打印**：折叠块靠 `beforeprint` 展开（CSS 无法改变 `<details>` 的展开态）；`404.html` 用内联脚本注入
  `<base>`，因为 Pages 会在任意深度的 URL 上渲染它，相对路径会解析错
- **动画克制**：统一 `--dur: 160ms`，并尊重 `prefers-reduced-motion`
- **`common.js` 里的事件用委托**：页面内容由生成器产出，直接绑定容易漏
- `.codex/` 被 gitignore（本地 skill 目录，含 `ui-ux-pro-max` 软链），不要提交

### 仓库卫生（`.gitignore` 只忽略「本地产生 / 可再生产」的东西）

入库的：`index.html`、`404.html`、`algo/`、`sql/`、`assets/`、`scripts/`（含内容源）、
`docs/`、`design-system/`、`AGENTS.md`、`README.md`、`.nojekyll`。
**站点产物必须入库**——GitHub Pages 直接发布这份仓库，忽略掉就没有内容了。

忽略的：Python 缓存（`__pycache__/`、`*.py[cod]`）、`.codex/`（本地 skill 软链）、
`node_modules/`、`.playwright-cli/`、编辑器与系统文件、日志与临时文件、`.env*`、虚拟环境。

- 跑完生成器会出现 `__pycache__`：`bash scripts/clean.sh --force` 清掉；`scripts/test.sh` 已设
  `PYTHONDONTWRITEBYTECODE=1`，跑门禁本身不再产生缓存
- `check_site.py` 会校验 `.gitignore` 是否覆盖了 7 类常见垃圾（反例已测：注释掉规则即报错），
  并在工作区真出现垃圾时给出警告
- `.nojekyll` 是 GitHub Pages 的标记文件（告诉它不要走 Jekyll 处理），**不要删**

---

## 7. 已知边界（未验证 / 待办）

- 图解画布 `.frame-canvas` 用 `width: fit-content` 贴合图形：表格类自然铺满卡片，节点类不再拖一块空底纹。
  **窄屏（≤640px）刻意不缩放图解**，宽表改为画布内横向滚动 —— 按比例缩到 40% 的表格等于不可读
- 图解宽度由绘制时的 `U.frameCardWidth(id)` 决定（已扣除卡片与画布内边距）；若某帧在桌面端出现「图形比卡片窄很多」，说明该 spec 写死了 width 而没有用它
- 打印验证覆盖「图解最多的 5 页 + SQL + 首页」共 7 页（折叠块、样式、PDF 导出都过），
  但**没有逐页比对 PDF 的分页观感**：长图解跨页时仍可能出现断行不好看的情况
- 冒烟测试覆盖结构与交互，**不检查「好不好看」**：配色、留白、字体观感仍需人工看图

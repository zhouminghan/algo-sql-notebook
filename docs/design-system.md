# 设计系统落地说明

本文件说明 `assets/css/style.css` 里的令牌与组件约定，以及它们与
`design-system/algosql-notebook/MASTER.md`（`ui-ux-pro-max` skill 产出）的对应关系。

**改 UI 前先读这里。** 规则只有一条最重要：**只用变量，不写死数值**。

---

## 1. 起点：skill 给出的设计方向

```bash
python3 "$SKILL/scripts/search.py" "coding interview practice 题库 knowledge base developer reference" \
  --design-system --persist --variance 4 --motion 3 --density 8 \
  -p "AlgoSQL Notebook" --output-dir .
```

| 维度 | skill 建议 | 本项目取值 |
|------|-----------|-----------|
| 风格 | Minimalism & Swiss Style | ✅ 采纳 |
| 密度 | 8/10（紧凑、仪表盘式） | ✅ 采纳（间距 4→48px 八级） |
| 动效 | 3/10（克制微交互） | ✅ 采纳（统一 160ms） |
| 配色 | 中性灰 + 链接蓝 `#2563EB`，底 `#F8FAFC`，边框 `#E2E8F0` | ✅ 采纳，并推导出暗色一套 |
| 字体 | Atkinson Hyperlegible（Google Fonts） | ❌ **有意偏离**：会引入外部 webfont，破坏「离线可用 + 零 CDN」约束；改用系统字体栈（含 PingFang SC / 微软雅黑，中文覆盖更好） |

---

## 2. 令牌（唯一入口）

全部定义在 `assets/css/style.css` 顶部：`:root`（亮色）与 `[data-theme="dark"]`（暗色）两份。

| 组 | 变量 | 用途 |
|----|------|------|
| 表面 | `--bg` `--surface` `--surface-2` `--surface-3` | 页面底 / 卡片 / 次级面 / 三级面（hover、进度槽） |
| 文字 | `--text` `--text-2` `--muted` | 正文 / 次要正文 / 弱化说明 |
| 线条 | `--border` `--border-strong` | 分隔线 / 需要强调的线（滚动条、虚线框） |
| 强调 | `--accent` `--accent-hover` `--accent-soft` `--accent-border` `--on-accent` | 链接、激活态、选中底色、强调色上的文字 |
| 语义 | `--easy/--medium/--hard`（各带 `-bg` `-border`）、`--done` `--danger` | 难度标签、完成态、错误态 |
| 图解 | `--color-highlight` `--color-done` `--color-neutral` `--color-pointer` `--color-null` `--color-bg-frame` `--color-border` `--color-tag-bg` `--color-tag-text` | `draw-utils.js` 生成的 SVG 全靠这些上色（**改主题只需改这里，图会跟着变**） |
| 尺寸 | `--sp-1…--sp-8`（4/8/12/16/20/24/32/48） | 所有 padding / margin / gap |
| 圆角 | `--radius-xs/-sm/--radius/--radius-lg` | 5/7/10/14px；控件 5-7，卡片 10，容器 14 |
| 布局 | `--topbar-h` `--sidebar-w` `--rail-w` `--content-max` | 顶栏 48 / 侧栏 264 / 右侧目录 236 / 内容 1090 |
| 动效 | `--dur` `--ease` | 统一 160ms + `cubic-bezier(.4,0,.2,1)` |

> `check_site.py` 会扫描所有 HTML/JS，确保每个 `var(--x)` 都在 `style.css` 里定义过
> —— 删掉一个变量却忘了改引用，会在自检阶段直接报错。

### 间距节奏

组件内 8/12px，组件间 16/20px，分节间 32px，页面级 48px。
「密度 8」的含义就是：**宁可紧凑，不要空旷**——大片留白是上一版的失败点。

---

## 3. 布局骨架

```
.shell            grid: [--sidebar-w] [1fr]
 ├── .sidebar      sticky，内部 .sb-head(标签页) / .sb-search / .sb-scroll(分组列表)
 └── .main         padding 24/24/48
      └── .content-wrap   max-width 1090，水平居中
           ├── .content   正文列
           └── .rail      ≥1240px 出现；内部 .rail-inner sticky top=topbar+20
```

两个容易踩的点：

1. `.content-wrap` **不能**写 `align-items: start`——那样 `.rail` 只有自身内容高，
   sticky 会在滚过约 300px 后失效。默认 `stretch` 才能让右侧目录全程吸附。
2. `.content-wrap` 用 `margin: 0 auto` 居中。内容列若贴左边，在 1440px 屏幕上
   右半屏就是一片空白——这正是改版前的观感问题。

断点：`900px`（侧栏→抽屉）、`1024px`（收窄内边距、隐藏品牌副标题）、
`1240px`（出现右侧目录）、`640px`（单列、隐藏进度条）。

### 图解在窄屏的处理（衡量过的取舍）

`.frame-canvas` 在桌面端 `width: fit-content`，图解按 `U.frameCardWidth(id)` 精确排版，
文字保持 13px。≤640px 时不缩放图解，而是让画布 `overflow-x: auto` 横向滚动：

- 实测过：若按容器等比缩放，764px 宽的 SQL 表格在 390px 屏上会被压到 308px，
  13px 的单元格文字变成约 5px —— 等于不可读
- 现在的规则是「装得下就居中显示，装不下就滚动」，图形文字始终是书写尺寸
- 实现细节：窄屏下画布从 `flex` 切回 `block`，因为 flex 居中在 overflow 时会裁掉左侧内容

---

## 4. 组件约定

| 组件 | 类名 | 规则 |
|------|------|------|
| 图标按钮 | `.icon-btn` | **无边框**，hover 只加底色；用户明确否掉了「一堆描边按钮」 |
| 筛选胶囊 | `.filter-chip` | 默认灰底无边框，选中态填充 `--accent` |
| 标签页 | `.sb-tab` / `.catalog-tab` / `.tab-btn` | 容器灰底 + 选中项白底或下划线，不用边框分隔 |
| 卡片 | `.prob-card` / `.frame-card` / `.rail-card` | 1px `--border` + `--shadow-xs`，hover 只换边框色与底色，不做位移 |
| 图解帧 | `.frame-card` > `.frame-label` + `.frame-canvas` | **`.frame-canvas` 是关键**：`width:fit-content` 让底纹贴合图形（表格类铺满卡片、节点类不再拖空底纹）；窄屏改为横向滚动，不把图解缩到看不清 |
| 代码块 | `pre` / `.copy-btn` / `.code-tabs` | 复制按钮默认透明，hover/聚焦才出现（移动端常驻） |
| 折叠块 | `<details>` + `.collapsible-body` / `.selfcheck-box` | 用原生 details 控制显隐，箭头由 CSS 伪元素画，不写 JS |
| 右栏目录 | `.toc` | 当前分节加 `.active` 与 `aria-current="true"`，由 `common.js` 按滚动位置计算 |
| 进度弹层 | `.popover` + `.tb-progress-trigger` | 顶栏进度可点，弹出「全部标为已读 / 重置进度」；Esc 与点外部关闭 |
| 搜索分区标题 | `.sb-dir-head` / `.catalog-dir-head` | 跨 Tab 搜索时按算法/SQL 打粘性小标题，Tab 数字切换为命中数 |
| 按钮式链接 | `.link-btn`（`.ghost` 为次要态） | 404 页等处使用；实心主色，不用描边 |

### 无障碍与触控

- 标题层级固定为 **h1（题目标题）→ h2（分节）→ h3/h4（子标题）**，不跳级；`check_site.py` 会拦
- 所有可点元素走 `:focus-visible` 焦点环；搜索/筛选/进度变化通过 `#asn-live`（`role=status`，
  `aria-live=polite`）播报结果数
- 移动端（≤900px）触控目标 ≥40px：图标按钮 40×40、侧栏题目行 ≥40、折叠块标题 44；
  **桌面端不跟着放大**（34px 图标按钮 / 31px 行高），保持紧凑

### 打印

- 隐藏顶栏/侧栏/右栏/复制按钮/筛选器，正文单列、字号 11.5pt
- 折叠块由 `common.js` 的 `beforeprint` 展开（CSS 无法改变 `<details>` 的展开态），`afterprint` 复原
- 外链会补印 URL；图解画布取消横向滚动，按行宽缩放

---

## 5. 验收

```bash
python3 scripts/check_site.py     # 结构 + 令牌自检，必须 0 错误
```

人工视觉验收的宽度与检查点见 `AGENTS.md` 第 5 节。
自检通过 ≠ 好看：**必须真的在浏览器里看 1440 / 1024 / 390 三个宽度和亮暗两套主题。**

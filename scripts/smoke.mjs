#!/usr/bin/env node
/**
 * 运行时冒烟测试（Playwright + headless Chromium，直接跑 file:// 页面）
 *
 * 覆盖静态自检（check_site.py）管不到的部分：
 *   · 页面外壳真的注入成功、图解真的画出来、控制台没有报错
 *   · 首屏不被自动滚走、没有横向溢出
 *   · 四个断点的布局（右侧目录 / 抽屉 / 触控目标尺寸）
 *   · 关键交互：搜索（跨算法+SQL）、Tab 切换、主题、代码语言、折叠块、进度弹层
 *   · 打印：打印样式生效 + beforeprint 会展开折叠块 + 真能导出 PDF
 *
 * 用法：
 *   node scripts/smoke.mjs                # 全量
 *   node scripts/smoke.mjs --fast         # 只抽 8 道题
 *   node scripts/smoke.mjs --only 001     # 只测文件名含 001 的题
 *
 * Playwright 位置：优先 $PLAYWRIGHT_HOME，其次项目 node_modules，
 * 最后回退到本机 ChatGPT.app 内置的运行时。Chromium 走 $CHROME_EXE 或本机缓存。
 */
import { createRequire } from 'node:module';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = process.argv.slice(2);
const FAST = ARGS.includes('--fast');
const ONLY = ARGS.includes('--only') ? ARGS[ARGS.indexOf('--only') + 1] : null;

/* ---------- 依赖定位 ---------- */
function loadPlaywright() {
  const roots = [
    process.env.PLAYWRIGHT_HOME,
    path.join(ROOT, 'node_modules'),
    '/Applications/ChatGPT.app/Contents/Resources/cua_node/lib/node_modules',
  ].filter(Boolean);
  for (const r of roots) {
    try { return require(path.join(r, 'playwright')); } catch (e) { /* 继续找 */ }
  }
  try { return require('playwright'); } catch (e) {}
  console.error('找不到 playwright。设置 PLAYWRIGHT_HOME 或在项目里 npm i -D playwright。');
  process.exit(2);
}

function findChromium() {
  if (process.env.CHROME_EXE && existsSync(process.env.CHROME_EXE)) return process.env.CHROME_EXE;
  const cache = path.join(process.env.HOME || '', 'Library/Caches/ms-playwright');
  if (!existsSync(cache)) return undefined;
  const dirs = readdirSync(cache)
    .filter((d) => d.startsWith('chromium'))
    .sort()
    .reverse();
  for (const d of dirs) {
    for (const rel of [
      'chrome-headless-shell-mac-arm64/chrome-headless-shell',
      'chrome-headless-shell-mac-x64/chrome-headless-shell',
      'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
      'chrome-mac-arm64/Chromium.app/Contents/MacOS/Chromium',
    ]) {
      const p = path.join(cache, d, rel);
      if (existsSync(p)) return p;
    }
  }
  return undefined;
}

/* ---------- 结果收集 ---------- */
const failures = [];
const notes = [];
function check(ok, label) {
  if (!ok) failures.push(label);
  return ok;
}

/* ---------- 主流程 ---------- */
const { chromium } = loadPlaywright();
const url = (rel) => pathToFileURL(path.join(ROOT, rel)).href;

const problems = JSON.parse(
  (() => {
    const t = require('node:fs').readFileSync(path.join(ROOT, 'assets/js/problems.js'), 'utf8');
    return t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1);
  })()
);
let pages = [...problems.algo, ...problems.sql].map((p) => p.file);
if (ONLY) pages = pages.filter((f) => f.includes(ONLY));
else if (FAST) pages = [...pages.slice(0, 4), ...pages.slice(-4)];

const browser = await chromium.launch({
  headless: true,
  executablePath: findChromium(),
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});

const consoleErrors = [];
const pageErrors = [];
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(`${page.url()}: ${m.text().slice(0, 120)}`); });
page.on('pageerror', (e) => pageErrors.push(`${page.url()}: ${String(e.message).slice(0, 120)}`));

/* ===== 1. 全站页面结构 ===== */
let badPages = [];
const canvasByFile = new Map();   // 后面挑「图解最多」的几页做打印验证
for (const file of pages) {
  consoleErrors.length = 0;
  pageErrors.length = 0;
  await page.goto(url(file), { waitUntil: 'load' });
  await page.waitForTimeout(300);
  const r = await page.evaluate(() => {
    const qa = (s) => Array.from(document.querySelectorAll(s));
    const rail = document.querySelector('.rail');
    const canvases = qa('.frame-canvas');
    const svgs = qa('.frame-canvas > svg');
    const live = document.getElementById('asn-live');
    return {
      topbar: !!document.querySelector('.topbar'),
      h1: (document.querySelector('.ph-main h1') || {}).textContent || '',
      active: qa('.lesson-link.active').length,
      toc: qa('.toc a').length,
      railShown: !!rail && getComputedStyle(rail).display !== 'none',
      canvases: canvases.length,
      svgs: svgs.length,
      highlighted: qa('pre code.hljs').length,
      scrollY: Math.round(window.scrollY),
      overflowX: document.documentElement.scrollWidth > window.innerWidth,
      live: !!live && live.getAttribute('aria-live') === 'polite',
      headings: qa('h2').length,
    };
  });
  const ok =
    r.topbar && r.h1 && r.active === 1 && r.toc >= 3 && r.railShown &&
    r.canvases === r.svgs && r.scrollY === 0 && !r.overflowX && r.live &&
    r.headings >= 3 && consoleErrors.length === 0 && pageErrors.length === 0;
  if (!ok) {
    badPages.push(`${file} ${JSON.stringify({ ...r, consoleErrors, pageErrors })}`);
  }
  canvasByFile.set(file, r.canvases);
}
check(badPages.length === 0, `页面运行时检查（${badPages.length}/${pages.length} 失败）`);
if (badPages.length) notes.push(...badPages.slice(0, 6));

/* ===== 2. 首页 + 搜索跨 Tab + 进度弹层 ===== */
await page.goto(url('index.html'), { waitUntil: 'load' });
await page.waitForTimeout(300);
const idx = await page.evaluate(() => ({
  cards: document.querySelectorAll('.prob-card').length,
  groups: document.querySelectorAll('.cat-section').length,
  chapters: Array.from(document.querySelectorAll('.cat-section .cat-name')).map((e) => e.textContent),
}));
check(idx.cards === problems.algo.length, `首页算法卡片数（${idx.cards} vs ${problems.algo.length}）`);
const tabCounts = await page.evaluate(() =>
  Array.from(document.querySelectorAll('.catalog-tab')).map((b) => b.textContent.trim()));
check(
  tabCounts[0].includes(String(problems.algo.length)) && tabCounts[1].includes(String(problems.sql.length)),
  `首页两个 Tab 显示题量（${tabCounts.join(' / ')}）`
);

// SQL tab
await page.click('.catalog-tab[data-dir="sql"]');
await page.waitForTimeout(200);
check((await page.locator('.prob-card').count()) === problems.sql.length, '首页切到 SQL tab 后卡片数正确');

// 跨 Tab 搜索：在 SQL tab 下搜只有算法题才有的关键词
await page.click('.catalog-tab[data-dir="algo"]');
await page.fill('.nav-search', '动态规划');
await page.waitForTimeout(250);
const search = await page.evaluate(() => ({
  dirHeads: Array.from(document.querySelectorAll('.catalog-dir-head')).map((e) => e.textContent.trim()),
  sbDirHeads: Array.from(document.querySelectorAll('.sb-dir-head')).map((e) => e.textContent.trim()),
  groups: Array.from(document.querySelectorAll('.cat-section .cat-name')).map((e) => e.textContent),
  algoCount: document.querySelector('.catalog-tab[data-dir="algo"] .sb-tab-count').textContent,
  sqlCount: document.querySelector('.catalog-tab[data-dir="sql"] .sb-tab-count').textContent,
  live: document.getElementById('asn-live').textContent,
}));
check(search.groups.includes('动态规划'), '搜索「动态规划」命中算法分组');
check(search.live.includes('找到'), `搜索会向屏幕阅读器播报（${search.live}）`);
await page.fill('.nav-search', '窗口函数');
await page.waitForTimeout(250);
const crossSearch = await page.evaluate(() => Array.from(document.querySelectorAll('.cat-section .cat-name')).map((e) => e.textContent));
check(crossSearch.includes('窗口函数'), '在算法 tab 下也能搜到 SQL 题（跨 Tab 搜索）');

// 进度弹层
await page.fill('.nav-search', '');
await page.waitForTimeout(200);
await page.click('.tb-progress-trigger');
await page.waitForTimeout(150);
check(await page.isVisible('.popover[data-open="true"]'), '点击进度可打开弹层');
await page.click('.popover button:has-text("全部标为已读")');
await page.waitForTimeout(250);
const afterAll = await page.textContent('.tb-progress-text');
check(/已读 106 \/ 106/.test(afterAll), `「全部标为已读」生效（${afterAll}）`);
await page.click('.tb-progress-trigger');
await page.click('.popover button:has-text("重置阅读进度")');
await page.waitForTimeout(250);
const afterReset = await page.textContent('.tb-progress-text');
check(/已读 0 \/ 106/.test(afterReset), `「重置阅读进度」生效（${afterReset}）`);

// 分类上的进度显示
await page.click('.prob-card-link >> nth=0');
await page.waitForTimeout(300);
await page.goto(url('index.html'), { waitUntil: 'load' });
await page.waitForTimeout(300);
check((await page.locator('.cat-section .count .done').count()) > 0, '分类标题上显示「已读 x/y」');

/* ===== 3. 题目页交互 ===== */
await page.goto(url('algo/001-两数之和.html'), { waitUntil: 'load' });
await page.waitForTimeout(300);
check((await page.locator('pre code.hljs').count()) > 0, 'highlight.js（defer）加载后代码高亮生效');
await page.click('.tab-btn[data-lang="java"]');
await page.waitForTimeout(150);
check(await page.isVisible('.code-pane[data-lang="java"]'), 'Python/Java 代码切换');
// 目录滚动高亮
const tocBefore = await page.textContent('.toc a.active');
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await page.waitForTimeout(400);
const tocAfter = await page.textContent('.toc a.active');
check(tocBefore !== tocAfter, `右侧目录随滚动高亮（${tocBefore} → ${tocAfter}）`);
// 折叠块
await page.evaluate(() => window.scrollTo(0, 0));
const det = page.locator('details.selfcheck-box').first();
await det.locator('summary').click();
await page.waitForTimeout(120);
check(!(await det.evaluate((d) => d.open)), '折叠块可以收起');
// 主题
await page.click('[data-theme-toggle]');
await page.waitForTimeout(150);
check((await page.getAttribute('html', 'data-theme')) === 'dark', '主题切换到暗色');
await page.click('[data-theme-toggle]');

/* ===== 4. 断点 ===== */
async function atWidth(w) {
  await page.setViewportSize({ width: w, height: 900 });
  await page.goto(url('algo/076-课程表.html'), { waitUntil: 'load' });
  await page.waitForTimeout(350);
  return page.evaluate(() => {
    const rail = document.querySelector('.rail');
    const sb = document.querySelector('.sidebar');
    const nav = document.querySelector('.mobile-nav-btn');
    const row = document.querySelector('.sb-items .lesson-link');
    return {
      rail: rail ? getComputedStyle(rail).display : 'none',
      sidebar: getComputedStyle(sb).position,
      nav: getComputedStyle(nav).display,
      navBox: (() => { const b = nav.getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; })(),
      rowH: Math.round(row.getBoundingClientRect().height),
      overflowX: document.documentElement.scrollWidth > window.innerWidth,
    };
  });
}
const w1440 = await atWidth(1440);
const w1240 = await atWidth(1240);
const w1024 = await atWidth(1024);
const w768 = await atWidth(768);
const w390 = await atWidth(390);
check(w1440.rail === 'block' && w1240.rail === 'block', '≥1240px 显示右侧目录');
check(w1024.rail === 'none', '1024px 隐藏右侧目录');
check(w768.nav === 'flex' && w768.sidebar === 'fixed', '≤900px 侧栏变抽屉 + 显示汉堡按钮');
check([w1440, w1240, w1024, w768, w390].every((w) => !w.overflowX), '各断点都没有横向溢出');
check(w390.navBox[1] >= 40 && w390.navBox[0] >= 40, `移动端汉堡按钮触控目标 ≥40px（${w390.navBox.join('×')}）`);
check(w390.rowH >= 40, `移动端题目行高 ≥40px（${w390.rowH}）`);
// 抽屉开合
await page.click('.mobile-nav-btn');
await page.waitForTimeout(300);
check(await page.evaluate(() => document.body.classList.contains('nav-open')), '移动端抽屉可打开');
await page.keyboard.press('Escape');
await page.waitForTimeout(300);
check(await page.evaluate(() => !document.body.classList.contains('nav-open')), 'Esc 可关闭抽屉');

/* ===== 5. 打印：挑图解最多的 5 页 + 一道 SQL 题 + 首页，逐页导出 PDF ===== */
await page.setViewportSize({ width: 1440, height: 900 });
const heavyPages = [...canvasByFile.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map((e) => e[0]);
const printPages = [...new Set([...heavyPages, 'sql/001-连续登录天数.html', 'index.html'])];
let pdfBytes = 0;
let pdfMaxPages = 0;
let detailsTotal = 0;
for (const file of printPages) {
  await page.goto(url(file), { waitUntil: 'load' });
  await page.waitForTimeout(300);
  await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
  await page.waitForTimeout(120);
  const st = await page.evaluate(() => ({
    allOpen: Array.from(document.querySelectorAll('details')).every((d) => d.open),
    details: document.querySelectorAll('details').length,
  }));
  check(st.allOpen, `${file}：打印前展开全部折叠块（${st.details} 个）`);
  detailsTotal += st.details;

  await page.emulateMedia({ media: 'print' });
  const css = await page.evaluate(() => ({
    topbar: getComputedStyle(document.querySelector('.topbar')).display,
    sidebar: getComputedStyle(document.querySelector('.sidebar')).display,
    // 首页没有图解画布，此时该项视为通过
    canvas: (() => {
      const c = document.querySelector('.frame-canvas');
      return !c || getComputedStyle(c).overflowX === 'visible';
    })(),
  }));
  check(css.topbar === 'none' && css.sidebar === 'none', `${file}：打印样式隐藏顶栏与侧栏`);
  check(css.canvas, `${file}：打印时图解不横向滚动`);
  await page.emulateMedia({ media: null });

  const pdf = await page.pdf({ printBackground: true, format: 'A4' });
  const pdfPages = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  check(pdf.length > 15000 && pdfPages >= 1, `${file}：导出 PDF（${Math.round(pdf.length / 1024)}KB / ${pdfPages}页）`);
  pdfBytes += pdf.length;
  pdfMaxPages = Math.max(pdfMaxPages, pdfPages);
}

/* ===== 6. 404 ===== */
await page.goto(url('404.html'), { waitUntil: 'load' });
await page.waitForTimeout(300);
const nf = await page.evaluate(() => ({
  title: document.title,
  hasShell: !!document.querySelector('.topbar'),
  link: (document.querySelector('.link-btn') || {}).getAttribute?.('href') || '',
}));
check(nf.title.includes('404') && nf.hasShell && nf.link.includes('index.html'), '404 页可正常渲染且能回到首页');

/* ---------- 报告 ---------- */
await ctx.close();
await browser.close();

console.log('\nalgo-sql-notebook · 运行时冒烟测试');
console.log(`  页面            ${pages.length} 个题目页 + index + 404`);
console.log(`  外壳/图解/控制台 ${pages.length - badPages.length}/${pages.length} 通过`);
console.log(`  首页与搜索      ${idx.groups} 个分类分组，跨 Tab 搜索与进度弹层已覆盖`);
console.log(`  断点            1440/1240/1024/768/390`);
console.log(`  打印            ${printPages.length} 页（图解最多的 ${heavyPages.length} 页 + SQL + 首页）：`
  + `展开 ${detailsTotal} 个折叠块、样式生效、共导出 ${Math.round(pdfBytes / 1024)}KB PDF（单页最多 ${pdfMaxPages} 页）`);
if (notes.length) console.log('\n失败明细：\n  ' + notes.join('\n  '));
if (failures.length) {
  console.log('\n未通过：\n  x ' + failures.join('\n  x '));
  console.log(`\nFAIL：${failures.length} 项`);
  process.exit(1);
}
console.log('\nPASS：全部检查通过');

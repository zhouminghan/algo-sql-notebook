/**
 * algo-sql-notebook — 公共运行时
 * 布局：全宽顶栏（品牌 + 进度 + 主题）+ 左侧目录树 + 右侧内容 + 底部上一题/下一题
 * 依赖：assets/js/problems.js（window.PROBLEMS）
 */
(function () {
  'use strict';

  var LS_THEME = 'asn-theme';
  var LS_DONE = 'asn-done';

  var PROBLEMS = window.PROBLEMS || { algo: [], sql: [] };
  var ALL = PROBLEMS.algo.concat(PROBLEMS.sql);
  var BY_FILE = {};
  ALL.forEach(function (p) { if (p.file) BY_FILE[p.file] = p; });

  var DIFF_MAP = { easy: '简单', medium: '中等', hard: '困难' };
  var DIFF_CLASS = { easy: 'tag-easy', medium: 'tag-medium', hard: 'tag-hard' };

  // ---------------- SVG 图标（替代 emoji） ----------------
  function icon(inner, extra) {
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"' + (extra ? ' ' + extra : '') + '>' + inner + '</svg>';
  }
  var ICONS = {
    brand: icon('<path d="M8 7l-5 5 5 5"/><path d="M16 7l5 5-5 5"/>'),
    moon: icon('<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'),
    sun: icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/>'),
    search: icon('<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>'),
    chevron: icon('<path d="M9 18l6-6-6-6"/>'),
    check: icon('<path d="M20 6 9 17l-5-5"/>'),
  };

  // ---------------- 本地存储 ----------------
  function readList(key) { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) { return []; } }
  function writeList(key, list) { try { localStorage.setItem(key, JSON.stringify(list)); } catch (e) {} }
  function getDone() { return readList(LS_DONE); }
  function isDone(file) { return getDone().indexOf(file) !== -1; }
  function setDone(file) {
    var list = getDone();
    if (!file || list.indexOf(file) !== -1) return;
    list.push(file); writeList(LS_DONE, list);
  }

  // ---------------- 复制 ----------------
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      try {
        var ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.left = '-9999px';
        document.body.appendChild(ta); ta.focus(); ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        ok ? resolve() : reject(new Error('execCommand copy failed'));
      } catch (e) { reject(e); }
    });
  }
  function copyCode(btn, codeId) {
    var node = document.getElementById(codeId);
    if (!node) return;
    copyText(node.textContent).then(function () {
      if (!btn) return;
      var old = btn.textContent;
      btn.textContent = '已复制'; btn.classList.add('copied');
      setTimeout(function () { btn.textContent = old; btn.classList.remove('copied'); }, 1500);
    }).catch(function () {
      if (btn) { btn.textContent = '复制失败'; setTimeout(function () { btn.textContent = '复制'; }, 1500); }
    });
  }

  // ---------------- 主题 ----------------
  function currentTheme() { return document.documentElement.getAttribute('data-theme') || 'light'; }
  function applyTheme(theme, persist) {
    document.documentElement.setAttribute('data-theme', theme);
    if (persist) { try { localStorage.setItem(LS_THEME, theme); } catch (e) {} }
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.innerHTML = theme === 'dark' ? ICONS.sun : ICONS.moon;
      btn.setAttribute('aria-label', theme === 'dark' ? '切换到亮色' : '切换到暗色');
      btn.title = theme === 'dark' ? '切换到亮色' : '切换到暗色';
    });
  }
  function initTheme() {
    applyTheme(currentTheme(), false);
    try {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function (e) { if (!localStorage.getItem(LS_THEME)) applyTheme(e.matches ? 'dark' : 'light', false); };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    } catch (e) {}
  }

  function currentFile() {
    var meta = document.querySelector('meta[name="asn-file"]');
    if (meta) return meta.getAttribute('content');
    var m = decodeURIComponent(location.pathname).match(/(algo|sql)\/[^/]+$/);
    return m ? m[0] : null;
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  // ---------------- 顶栏 ----------------
  function buildTopbar(isIndex) {
    var bar = el('header', 'topbar');
    var brandWrap = el('div', 'tb-brand');
    var brand = el('a', 'brand');
    brand.href = isIndex ? 'index.html' : '../index.html';
    brand.innerHTML = ICONS.brand + '<span class="brand-name">algo-sql-notebook</span>';
    brandWrap.appendChild(brand);
    brandWrap.appendChild(el('div', 'brand-sub', '算法 + SQL 图解题库'));
    bar.appendChild(brandWrap);

    var right = el('div', 'tb-right');
    var done = ALL.filter(function (p) { return p.file && isDone(p.file); }).length;
    var total = ALL.filter(function (p) { return p.file; }).length;
    var prog = el('div', 'tb-progress');
    prog.appendChild(el('span', 'tb-progress-text', '已读 ' + done + ' / ' + total));
    var track = el('div', 'prog-track');
    var fill = el('div', 'prog-fill');
    fill.style.width = (total ? Math.round(done / total * 100) : 0) + '%';
    track.appendChild(fill);
    prog.appendChild(track);
    right.appendChild(prog);

    var themeBtn = el('button', 'theme-btn');
    themeBtn.type = 'button';
    themeBtn.setAttribute('data-theme-toggle', '');
    right.appendChild(themeBtn);

    bar.appendChild(brandWrap);
    bar.appendChild(right);
    return bar;
  }

  // ---------------- 目录列表（按题号平铺 + 分类标签） ----------------
  function lessonLink(p, currentFile, isIndex) {
    var a = el('a', 'lesson-link');
    // 相对路径：首页→完整路径；同目录→文件名；跨目录→../algo/ 或 ../sql/
    if (isIndex) {
      a.href = p.file;
    } else {
      var curDir = currentFile.split('/')[0];
      var t = p.file.split('/');
      a.href = (t[0] === curDir) ? t[1] : '../' + p.file;
    }
    a.appendChild(el('span', 'lesson-num', String(p.id).padStart(3, '0')));
    a.appendChild(el('span', 'lesson-title', p.title));
    var cat = p.cat || (p.tags && p.tags[0]) || '';
    if (cat) a.appendChild(el('span', 'lesson-tag', cat));
    if (p.file === currentFile) a.classList.add('active');
    if (isDone(p.file)) a.classList.add('done');
    return a;
  }

  function buildNavList(currentFile) {
    var nav = el('nav', 'nav-tree');
    var isIndex = !currentFile;
    nav.appendChild(el('div', 'nav-section-head', '算法'));
    PROBLEMS.algo.forEach(function (p) { if (p.file) nav.appendChild(lessonLink(p, currentFile, isIndex)); });
    nav.appendChild(el('div', 'nav-section-head', 'SQL 高级题'));
    PROBLEMS.sql.forEach(function (p) { if (p.file) nav.appendChild(lessonLink(p, currentFile, isIndex)); });
    return nav;
  }

  function buildSidebar(currentFile) {
    var aside = el('aside', 'sidebar');
    var searchWrap = el('div', 'search-wrap');
    var searchIcon = el('span', 'search-icon');
    searchIcon.innerHTML = ICONS.search;
    var input = el('input', 'nav-search');
    input.type = 'search';
    input.placeholder = '搜索题目';
    input.setAttribute('aria-label', '搜索题目');
    searchWrap.appendChild(searchIcon);
    searchWrap.appendChild(input);
    aside.appendChild(searchWrap);

    aside.appendChild(buildNavList(currentFile));

    input.addEventListener('input', function () {
      filterTree(input.value.trim().toLowerCase());
      try { window.dispatchEvent(new CustomEvent('asn:search', { detail: input.value.trim() })); } catch (e) {}
    });
    return aside;
  }

  function filterTree(q) {
    document.querySelectorAll('.nav-tree .lesson-link').forEach(function (a) {
      var hit = !q || a.textContent.toLowerCase().indexOf(q) !== -1;
      a.style.display = hit ? '' : 'none';
    });
    document.querySelectorAll('.nav-tree .nav-section-head').forEach(function (h) {
      var any = false;
      var next = h.nextElementSibling;
      while (next && next.classList && next.classList.contains('lesson-link')) {
        if (next.style.display !== 'none') { any = true; break; }
        next = next.nextElementSibling;
      }
      h.style.display = any ? '' : 'none';
    });
  }

  // ---------------- 题头 / 底栏 ----------------
  function buildProblemHeader(p) {
    var wrap = el('div', 'problem-header');
    wrap.appendChild(el('span', 'problem-number', String(p.id).padStart(3, '0')));
    var main = el('div', 'ph-main');
    main.appendChild(el('h1', null, p.title));
    var meta = el('div', 'ph-meta');
    meta.appendChild(el('span', 'tag-badge ' + DIFF_CLASS[p.diff], DIFF_MAP[p.diff]));
    (p.tags || []).forEach(function (t) { meta.appendChild(el('span', 'tag-badge tag-ds', t)); });
    if (p.leetcode) meta.appendChild(el('a', 'leetcode-chip', 'LeetCode ' + p.leetcode));
    main.appendChild(meta);
    wrap.appendChild(main);
    return wrap;
  }

  function footBtn(cls, problem, arrow) {
    if (!problem) return el('span', 'lf-btn ' + cls + ' disabled', arrow);
    var a = el('a', 'lf-btn ' + cls, arrow);
    a.href = problem.file.split('/').pop();
    a.appendChild(el('span', 'lf-title', problem.title));
    return a;
  }

  function buildLessonFoot(p) {
    var foot = el('footer', 'lesson-foot');
    var list = PROBLEMS[p.dir].filter(function (x) { return x.file; });
    var idx = list.findIndex(function (x) { return x.file === p.file; });
    foot.appendChild(footBtn('prev', list[idx - 1], '← 上一题'));
    foot.appendChild(footBtn('next', list[idx + 1], '下一题 →'));
    return foot;
  }

  // ---------------- Python/Java 代码标签页 ----------------
  function enhanceCodeTabs(root) {
    var groups = [];
    var cur = [];
    function flush() { if (cur.length >= 2) groups.push(cur); cur = []; }
    root.querySelectorAll('h4').forEach(function (h4) {
      var lang = h4.textContent.trim().toLowerCase();
      if (lang === 'python' || lang === 'java') {
        var w = h4.nextElementSibling;
        if (w && w.classList && w.classList.contains('code-block-wrapper')) {
          cur.push({ h4: h4, w: w, lang: lang });
          return;
        }
      }
      flush();
    });
    flush();

    groups.forEach(function (g) {
      var container = document.createElement('div');
      container.className = 'code-tabs';
      var head = document.createElement('div');
      head.className = 'code-tabs-head';
      g.forEach(function (item, i) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'tab-btn' + (i === 0 ? ' active' : '');
        btn.textContent = item.lang === 'python' ? 'Python' : 'Java';
        btn.setAttribute('data-lang', item.lang);
        head.appendChild(btn);
        item.w.classList.add('code-pane');
        item.w.setAttribute('data-lang', item.lang);
        if (i !== 0) item.w.classList.add('hidden');
      });
      container.appendChild(head);
      var anchor = g[0].h4;
      anchor.parentNode.insertBefore(container, anchor);
      g.forEach(function (item) {
        item.h4.remove();
        container.appendChild(item.w);
      });
    });
  }

  // ---------------- 挂载 ----------------
  function mountShell() {
    var file = currentFile();
    var isIndex = !file;
    var body = document.body;
    var topbar = buildTopbar(isIndex);
    var sidebar = buildSidebar(file);
    var layout = el('div', 'layout');
    var main;

    if (file) {
      var p = BY_FILE[file];
      if (!p) return;
      p.dir = file.split('/')[0];
      setDone(file);
      main = el('main', 'content');
      main.appendChild(buildProblemHeader(p));
      Array.prototype.slice.call(body.children).forEach(function (node) {
        if (node.tagName === 'SCRIPT') return;
        main.appendChild(node);
      });
      main.appendChild(buildLessonFoot(p));
    } else {
      main = body.querySelector('main') || el('main', 'content');
    }

    layout.appendChild(sidebar);
    layout.appendChild(main);
    body.insertBefore(topbar, body.firstChild);
    body.appendChild(layout);

    // 目录树滚动到当前题
    var active = sidebar.querySelector('.lesson-link.active');
    if (active && active.scrollIntoView) active.scrollIntoView({ block: 'center' });

    applyTheme(currentTheme(), false);
    enhanceCodeTabs(document.body);
  }

  // ---------------- 事件 ----------------
  function bindGlobalEvents() {
    document.addEventListener('click', function (e) {
      var themeBtn = e.target.closest ? e.target.closest('[data-theme-toggle]') : null;
      if (themeBtn) { applyTheme(currentTheme() === 'dark' ? 'light' : 'dark', true); return; }
      var tabBtn = e.target.closest ? e.target.closest('.tab-btn') : null;
      if (tabBtn) {
        var container = tabBtn.closest('.code-tabs');
        if (!container) return;
        var lang = tabBtn.getAttribute('data-lang');
        container.querySelectorAll('.tab-btn').forEach(function (b) {
          b.classList.toggle('active', b === tabBtn);
        });
        container.querySelectorAll('.code-pane').forEach(function (p) {
          p.classList.toggle('hidden', p.getAttribute('data-lang') !== lang);
        });
      }
    });
  }

  window.ASN = {
    PROBLEMS: PROBLEMS, getDone: getDone, isDone: isDone,
    applyTheme: applyTheme, currentTheme: currentTheme,
    ICONS: ICONS
  };
  window.copyCode = copyCode;

  function boot() {
    initTheme();
    bindGlobalEvents();
    mountShell();
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 0);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

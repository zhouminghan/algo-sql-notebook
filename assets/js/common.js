/**
 * algo-sql-notebook — 公共运行时
 * 布局：全宽顶栏（品牌 + 进度 + 主题）+ 左侧目录树 + 右侧内容 + 底部上一题/下一题
 * 依赖：assets/js/problems.js（window.PROBLEMS）
 */
(function () {
  'use strict';

  var LS_THEME = 'asn-theme';
  var LS_DONE = 'asn-done';
  var LS_STAR = 'asn-star';

  var PROBLEMS = window.PROBLEMS || { algo: [], sql: [] };
  var ALL = PROBLEMS.algo.concat(PROBLEMS.sql);
  var BY_FILE = {};
  ALL.forEach(function (p) { if (p.file) BY_FILE[p.file] = p; });

  var DIFF_MAP = { easy: '简单', medium: '中等', hard: '困难' };
  var DIFF_CLASS = { easy: 'tag-easy', medium: 'tag-medium', hard: 'tag-hard' };

  // ---------------- 本地存储 ----------------
  function readList(key) { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) { return []; } }
  function writeList(key, list) { try { localStorage.setItem(key, JSON.stringify(list)); } catch (e) {} }
  function getDone() { return readList(LS_DONE); }
  function getStar() { return readList(LS_STAR); }
  function isDone(file) { return getDone().indexOf(file) !== -1; }
  function isStar(file) { return getStar().indexOf(file) !== -1; }
  function setDone(file) {
    var list = getDone();
    if (!file || list.indexOf(file) !== -1) return;
    list.push(file); writeList(LS_DONE, list);
  }
  function toggleStar(file) {
    var list = getStar();
    var i = list.indexOf(file);
    if (i === -1) list.push(file); else list.splice(i, 1);
    writeList(LS_STAR, list);
    return i === -1;
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
      btn.textContent = '✅ 已复制'; btn.classList.add('copied');
      setTimeout(function () { btn.textContent = old; btn.classList.remove('copied'); }, 1500);
    }).catch(function () {
      if (btn) { btn.textContent = '⚠️ 复制失败'; setTimeout(function () { btn.textContent = '📋 复制'; }, 1500); }
    });
  }

  // ---------------- 主题 ----------------
  function currentTheme() { return document.documentElement.getAttribute('data-theme') || 'light'; }
  function applyTheme(theme, persist) {
    document.documentElement.setAttribute('data-theme', theme);
    if (persist) { try { localStorage.setItem(LS_THEME, theme); } catch (e) {} }
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.setAttribute('aria-label', theme === 'dark' ? '切换到亮色' : '切换到暗色');
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
    var brand = el('a', 'brand', 'algo-sql-notebook');
    brand.href = isIndex ? 'index.html' : '../index.html';
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

  // ---------------- 目录树 ----------------
  function lessonLink(p, currentFile) {
    var a = el('a', 'lesson-link', String(p.id).padStart(3, '0') + '  ' + p.title);
    a.href = p.file.split('/').pop();
    if (p.file === currentFile) a.classList.add('active');
    if (isDone(p.file)) a.classList.add('done');
    return a;
  }

  function topicBlock(title, lessons, currentFile, defaultOpen) {
    var block = el('div', 'topic-block');
    if (!defaultOpen) block.classList.add('collapsed');
    var head = el('button', 'topic-head');
    head.type = 'button';
    head.appendChild(el('span', 'topic-caret', '▸'));
    head.appendChild(el('span', 'topic-name', title));
    head.appendChild(el('span', 'topic-count', String(lessons.length)));
    block.appendChild(head);
    var list = el('div', 'lesson-list');
    lessons.forEach(function (p) { list.appendChild(lessonLink(p, currentFile)); });
    block.appendChild(list);
    head.addEventListener('click', function () { block.classList.toggle('collapsed'); });
    return block;
  }

  function buildNavTree(currentFile) {
    var nav = el('nav', 'nav-tree');

    // 算法：按分类分组
    var algoGroup = el('div', 'nav-group');
    var algoHead = el('button', 'nav-group-head');
    algoHead.type = 'button';
    algoHead.appendChild(el('span', 'topic-caret', '▸'));
    algoHead.appendChild(el('span', 'topic-name', '💻 算法'));
    algoGroup.appendChild(algoHead);
    var algoBody = el('div', 'nav-group-body');
    var byCat = {};
    PROBLEMS.algo.forEach(function (p) {
      if (!p.file) return;
      var c = p.cat || '其他';
      (byCat[c] = byCat[c] || []).push(p);
    });
    Object.keys(byCat).forEach(function (c) {
      var containsCurrent = byCat[c].some(function (p) { return p.file === currentFile; });
      algoBody.appendChild(topicBlock(c, byCat[c], currentFile, containsCurrent || !currentFile));
    });
    algoGroup.appendChild(algoBody);
    algoHead.addEventListener('click', function () { algoGroup.classList.toggle('collapsed'); });
    nav.appendChild(algoGroup);

    // SQL：单组
    var sqlGroup = el('div', 'nav-group');
    var sqlHead = el('button', 'nav-group-head');
    sqlHead.type = 'button';
    sqlHead.appendChild(el('span', 'topic-caret', '▸'));
    sqlHead.appendChild(el('span', 'topic-name', '🗄️ SQL 高级题'));
    sqlGroup.appendChild(sqlHead);
    var sqlBody = el('div', 'nav-group-body');
    var sqlList = PROBLEMS.sql.filter(function (p) { return p.file; });
    var sqlContains = sqlList.some(function (p) { return p.file === currentFile; });
    sqlBody.appendChild(topicBlock('全部', sqlList, currentFile, sqlContains || !currentFile));
    sqlGroup.appendChild(sqlBody);
    sqlHead.addEventListener('click', function () { sqlGroup.classList.toggle('collapsed'); });
    if (currentFile && currentFile.indexOf('algo/') === 0) sqlGroup.classList.add('collapsed');
    nav.appendChild(sqlGroup);

    return nav;
  }

  function buildSidebar(currentFile) {
    var aside = el('aside', 'sidebar');
    var searchWrap = el('div', 'search-wrap');
    var input = el('input', 'nav-search');
    input.type = 'search';
    input.placeholder = '搜索题目…';
    input.setAttribute('aria-label', '搜索题目');
    searchWrap.appendChild(input);
    aside.appendChild(searchWrap);

    var route = el('div', 'route-wrap');
    route.appendChild(el('span', 'route-label', '题库导航'));
    aside.appendChild(route);

    aside.appendChild(buildNavTree(currentFile));

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
      var block = a.closest('.topic-block');
      if (block) {
        var anyVisible = Array.prototype.some.call(block.querySelectorAll('.lesson-link'), function (x) { return x.style.display !== 'none'; });
        block.style.display = anyVisible ? '' : 'none';
        if (q && hit) block.classList.remove('collapsed');
      }
      var group = a.closest('.nav-group');
      if (group) {
        var anyGroup = Array.prototype.some.call(group.querySelectorAll('.lesson-link'), function (x) { return x.style.display !== 'none'; });
        group.style.display = anyGroup ? '' : 'none';
      }
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
    var star = el('button', 'lf-star');
    star.type = 'button';
    star.setAttribute('data-star-file', p.file);
    star.textContent = isStar(p.file) ? '★ 已收藏' : '☆ 收藏';
    if (isStar(p.file)) star.classList.add('on');
    foot.appendChild(star);
    foot.appendChild(footBtn('next', list[idx + 1], '下一题 →'));
    return foot;
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
  }

  // ---------------- 事件 ----------------
  function bindGlobalEvents() {
    document.addEventListener('click', function (e) {
      var themeBtn = e.target.closest ? e.target.closest('[data-theme-toggle]') : null;
      if (themeBtn) { applyTheme(currentTheme() === 'dark' ? 'light' : 'dark', true); return; }
      var starBtn = e.target.closest ? e.target.closest('[data-star-file]') : null;
      if (starBtn) {
        var on = toggleStar(starBtn.getAttribute('data-star-file'));
        starBtn.textContent = on ? '★ 已收藏' : '☆ 收藏';
        starBtn.classList.toggle('on', on);
        try { window.dispatchEvent(new CustomEvent('asn:star')); } catch (e) {}
      }
    });
  }

  window.ASN = {
    PROBLEMS: PROBLEMS, getDone: getDone, isDone: isDone,
    getStar: getStar, isStar: isStar, toggleStar: toggleStar,
    applyTheme: applyTheme, currentTheme: currentTheme
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

/**
 * algo-sql-notebook —— 页面外壳（Shell）
 * ---------------------------------------------------------------------------
 * 职责：把「只有正文的静态 HTML」包成完整应用外壳。
 *
 *   顶栏（品牌 / 进度 / 主题）
 *   ├── 左侧栏：算法·SQL 两个 Tab + 分类分组 + 搜索
 *   └── 主区：题头 + 正文 + 右侧 rail（本页目录 / 题目信息）+ 上一下一
 *
 * 数据源：assets/js/problems.js（window.PROBLEMS），页面自身只写正文。
 * 无框架、无构建；所有状态存 localStorage。
 */
(function () {
  'use strict';

  var LS = {
    theme: 'asn-theme',
    done: 'asn-done',
    tab: 'asn-tab',
    diff: 'asn-diff',
    groups: 'asn-groups'
  };

  var PROBLEMS = window.PROBLEMS || { algo: [], sql: [] };
  var DIR_LABEL = { algo: '算法', sql: 'SQL' };
  var DIR_ORDER = ['algo', 'sql'];
  var CAT_ORDER = {
    algo: ['哈希', '双指针', '滑动窗口', '数组', '矩阵', '字符串', '链表', '二叉树',
      '图', '回溯', '二分查找', '栈', '堆', '贪心', '动态规划', '位运算'],
    sql: ['窗口函数', '多表 JOIN', '自连接', '过滤与聚合', '日期计算']
  };
  var DIFF_MAP = { easy: '简单', medium: '中等', hard: '困难' };
  var DIFF_CLASS = { easy: 'tag-easy', medium: 'tag-medium', hard: 'tag-hard' };

  /* ======================================================================
     SVG 图标（不使用 emoji）
     ====================================================================== */
  function icon(inner, extra) {
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"' +
      (extra ? ' ' + extra : '') + '>' + inner + '</svg>';
  }
  var ICONS = {
    brand: icon('<path d="M8 7l-5 5 5 5"/><path d="M16 7l5 5-5 5"/>'),
    moon: icon('<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'),
    sun: icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/>'),
    search: icon('<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>'),
    chevron: icon('<path d="M9 18l6-6-6-6"/>'),
    check: icon('<path d="M20 6 9 17l-5-5"/>'),
    menu: icon('<path d="M3 6h18"/><path d="M3 12h18"/><path d="M3 18h18"/>'),
    external: icon('<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14 21 3"/>')
  };

  /* ======================================================================
     本地存储 / 状态
     ====================================================================== */
  function readJSON(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key) || 'null') || fallback; }
    catch (e) { return fallback; }
  }
  function writeJSON(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }

  var doneSet = {};
  readJSON(LS.done, []).forEach(function (f) { doneSet[f] = true; });
  function isDone(file) { return !!doneSet[file]; }
  function markDone(file) {
    if (!file || doneSet[file]) return false;
    doneSet[file] = true;
    var list = Object.keys(doneSet);
    writeJSON(LS.done, list);
    return true;
  }
  function doneCount() {
    return ALL.filter(function (p) { return p.file && isDone(p.file); }).length;
  }
  function markAllDone() {
    ALL.forEach(function (p) { if (p.file) doneSet[p.file] = true; });
    writeJSON(LS.done, Object.keys(doneSet));
    emit('progress');
  }
  function resetProgress() {
    doneSet = {};
    writeJSON(LS.done, []);
    emit('progress');
  }
  function readCount(items) {
    var n = 0;
    items.forEach(function (p) { if (isDone(p.file)) n++; });
    return n;
  }

  var state = {
    tab: readJSON(LS.tab, 'algo'),
    diff: readJSON(LS.diff, 'all'),
    query: ''
  };
  if (DIR_ORDER.indexOf(state.tab) === -1) state.tab = 'algo';

  var listeners = {};
  function on(evt, fn) { (listeners[evt] = listeners[evt] || []).push(fn); }
  function emit(evt) { (listeners[evt] || []).forEach(function (fn) { fn(); }); }
  function setTab(dir, persist) {
    if (DIR_ORDER.indexOf(dir) === -1 || state.tab === dir) return;
    state.tab = dir;
    if (persist !== false) writeJSON(LS.tab, dir);
    emit('tab');
  }
  function setDiff(diff) {
    if (state.diff === diff) return;
    state.diff = diff;
    writeJSON(LS.diff, diff);
    emit('diff');
  }
  function setQuery(q) {
    if (state.query === q) return;
    state.query = q;
    emit('query');
  }

  /* ======================================================================
     数据
     ====================================================================== */
  var ALL = [];
  DIR_ORDER.forEach(function (dir) {
    (PROBLEMS[dir] || []).forEach(function (p) {
      if (!p.file) return;
      p.dir = dir;
      ALL.push(p);
    });
  });
  var BY_FILE = {};
  ALL.forEach(function (p) { BY_FILE[p.file] = p; });

  /** 按分类分组，保持 CAT_ORDER 的稳定顺序 */
  function groupByCat(dir) {
    var list = (PROBLEMS[dir] || []).filter(function (p) { return p.file; });
    var buckets = {};
    list.forEach(function (p) {
      var cat = p.cat || (p.tags && p.tags[0]) || '其他';
      (buckets[cat] = buckets[cat] || []).push(p);
    });
    var order = CAT_ORDER[dir] || [];
    var names = order.filter(function (c) { return buckets[c]; });
    Object.keys(buckets).forEach(function (c) {
      if (names.indexOf(c) === -1) names.push(c);
    });
    return names.map(function (name) {
      return { name: name, items: buckets[name] };
    });
  }

  function matches(p, dir) {
    if (dir && p.dir !== dir) return false;
    if (state.diff !== 'all' && p.diff !== state.diff) return false;
    if (state.query) {
      var hay = (p.id + ' ' + p.title + ' ' + (p.tags || []).join(' ') + ' ' + (p.cat || '')).toLowerCase();
      if (hay.indexOf(state.query.toLowerCase()) === -1) return false;
    }
    return true;
  }

  /* ======================================================================
     工具
     ====================================================================== */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }
  function html(tag, cls, markup) {
    var n = el(tag, cls);
    n.innerHTML = markup;
    return n;
  }
  function pad3(n) { return String(n).padStart(3, '0'); }

  /** 屏幕阅读器播报（搜索命中数、进度变化等） */
  function announce(msg) {
    var live = document.getElementById('asn-live');
    if (live) live.textContent = msg;
  }
  function relHref(file, isIndex) {
    if (isIndex) return file;
    var curDir = currentFile().split('/')[0];
    var parts = file.split('/');
    return parts[0] === curDir ? parts[1] : '../' + file;
  }
  function currentFile() {
    var meta = document.querySelector('meta[name="asn-file"]');
    if (meta) return meta.getAttribute('content');
    var m = decodeURIComponent(location.pathname).match(/(algo|sql)\/[^/]+$/);
    return m ? m[0] : null;
  }

  /* ======================================================================
     主题
     ====================================================================== */
  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }
  function applyTheme(theme, persist) {
    document.documentElement.setAttribute('data-theme', theme);
    if (persist) writeJSON(LS.theme, theme);
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.innerHTML = theme === 'dark' ? ICONS.sun : ICONS.moon;
      var label = theme === 'dark' ? '切换到亮色主题' : '切换到暗色主题';
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
    });
  }
  function initTheme() {
    applyTheme(currentTheme(), false);
    try {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function (e) {
        if (!localStorage.getItem(LS.theme)) applyTheme(e.matches ? 'dark' : 'light', false);
      };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    } catch (e) {}
  }

  /* ======================================================================
     顶栏
     ====================================================================== */
  function buildTopbar(isIndex) {
    var bar = el('header', 'topbar');

    var navBtn = html('button', 'icon-btn mobile-nav-btn', ICONS.menu);
    navBtn.type = 'button';
    navBtn.setAttribute('aria-label', '打开题目导航');
    navBtn.setAttribute('aria-expanded', 'false');
    navBtn.setAttribute('aria-controls', 'sidebar');
    bar.appendChild(navBtn);

    var brandWrap = el('div', 'tb-brand');
    var brand = el('a', 'brand');
    brand.href = isIndex ? 'index.html' : '../index.html';
    brand.innerHTML = ICONS.brand + '<span>algo-sql-notebook</span>';
    brandWrap.appendChild(brand);
    brandWrap.appendChild(el('span', 'brand-sub', '算法 + SQL 图解题库'));
    bar.appendChild(brandWrap);

    bar.appendChild(el('div', 'tb-spacer'));

    var right = el('div', 'tb-right');
    var prog = el('div', 'tb-progress');
    var total = ALL.length;

    var trigger = el('button', 'tb-progress-trigger');
    trigger.type = 'button';
    trigger.setAttribute('aria-haspopup', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.setAttribute('aria-label', '阅读进度，点击管理');
    trigger.appendChild(el('span', 'tb-progress-text', '已读 ' + doneCount() + ' / ' + total));
    var track = el('div', 'prog-track');
    var fill = el('div', 'prog-fill');
    fill.style.width = (total ? Math.round(doneCount() / total * 100) : 0) + '%';
    track.appendChild(fill);
    trigger.appendChild(track);
    prog.appendChild(trigger);

    var pop = el('div', 'popover');
    pop.setAttribute('role', 'menu');
    pop.appendChild(el('div', 'popover-title', '阅读进度'));
    [['全部标为已读', markAllDone], ['重置阅读进度', resetProgress]].forEach(function (pair) {
      var item = el('button', null, pair[0]);
      item.type = 'button';
      item.setAttribute('role', 'menuitem');
      item.addEventListener('click', function () {
        pair[1]();
        setPopover(pop, false);
        announce(pair[0] + '：已读 ' + doneCount() + ' / ' + total);
      });
      pop.appendChild(item);
    });
    prog.appendChild(pop);
    right.appendChild(prog);

    var themeBtn = el('button', 'icon-btn');
    themeBtn.type = 'button';
    themeBtn.setAttribute('data-theme-toggle', '');
    right.appendChild(themeBtn);

    bar.appendChild(right);
    return bar;
  }

  function refreshProgress() {
    var total = ALL.length;
    var text = document.querySelector('.tb-progress-text');
    if (text) text.textContent = '已读 ' + doneCount() + ' / ' + total;
    var fill = document.querySelector('.prog-fill');
    if (fill) fill.style.width = (total ? Math.round(doneCount() / total * 100) : 0) + '%';
  }

  /* ---------------- 进度弹层 ---------------- */
  function setPopover(pop, open) {
    if (!pop) return;
    pop.dataset.open = String(!!open);
    var trigger = pop.parentNode && pop.parentNode.querySelector('.tb-progress-trigger');
    if (trigger) trigger.setAttribute('aria-expanded', String(!!open));
  }
  function closePopovers() {
    document.querySelectorAll('.popover[data-open="true"]').forEach(function (p) { setPopover(p, false); });
  }

  /* ======================================================================
     侧边栏：Tab + 搜索 + 分类分组
     ====================================================================== */
  var sidebarEls = null;

  function buildSidebar(isIndex) {
    var aside = el('aside', 'sidebar');
    aside.id = 'sidebar';
    aside.setAttribute('aria-label', '题目导航');

    var head = el('div', 'sb-head');
    var tabs = el('div', 'sb-tabs');
    tabs.setAttribute('role', 'tablist');
    DIR_ORDER.forEach(function (dir) {
      var btn = el('button', 'sb-tab');
      btn.type = 'button';
      btn.setAttribute('role', 'tab');
      btn.dataset.dir = dir;
      btn.innerHTML = DIR_LABEL[dir] +
        '<span class="sb-tab-count">' + (PROBLEMS[dir] || []).filter(function (p) { return p.file; }).length + '</span>';
      btn.addEventListener('click', function () { setTab(dir); closeNav(); });
      tabs.appendChild(btn);
    });
    head.appendChild(tabs);
    aside.appendChild(head);

    var search = el('div', 'sb-search');
    search.appendChild(html('span', 'icon', ICONS.search));
    var input = el('input', 'nav-search');
    input.type = 'search';
    input.placeholder = '搜索题目 / 分类 / 标签';
    input.setAttribute('aria-label', '搜索题目');
    input.value = state.query;
    input.addEventListener('input', function () {
      setQuery(input.value.trim());
      syncSearchInputs(input.value);
    });
    search.appendChild(input);
    aside.appendChild(search);

    var scroll = el('div', 'sb-scroll');
    var groups = el('nav', 'sb-groups');
    groups.setAttribute('aria-label', '题目列表');
    scroll.appendChild(groups);
    aside.appendChild(scroll);

    sidebarEls = { aside: aside, tabs: tabs, input: input, groups: groups, scroll: scroll };
    renderSidebar(isIndex);
    return aside;
  }

  function groupOpenState() { return readJSON(LS.groups, {}); }
  function setGroupOpen(dir, name, open) {
    var s = groupOpenState();
    s[dir + '::' + name] = !!open;
    writeJSON(LS.groups, s);
  }

  function totalOf(dir) {
    return (PROBLEMS[dir] || []).filter(function (p) { return p.file; }).length;
  }

  /** 生成一个分类分组（含「已读 x/y」），该分组没有命中项时返回 null */
  function groupNode(dir, group, cur, isIndex) {
    var items = group.items.filter(function (p) { return matches(p, dir); });
    if (!items.length) return null;

    var hasActive = items.some(function (p) { return p.file === cur; });
    var open = groupOpenState()[dir + '::' + group.name];
    if (open === undefined) open = true;   // 默认展开
    if (state.query || hasActive) open = true;

    var wrap = el('div', 'sb-group');
    wrap.dataset.open = String(!!open);

    var btn = el('button', 'sb-group-head');
    btn.type = 'button';
    btn.setAttribute('aria-expanded', String(!!open));
    btn.appendChild(html('span', 'caret', ICONS.chevron));
    btn.appendChild(el('span', 'sb-group-name', group.name));

    var read = readCount(items);
    var count = el('span', 'sb-group-count');
    if (read) {
      count.innerHTML = '<span class="done">' + read + '</span>/' + items.length;
      if (read === items.length) count.classList.add('all-done');
      count.setAttribute('title', '已读 ' + read + ' / 共 ' + items.length);
    } else {
      count.textContent = String(items.length);
    }
    btn.appendChild(count);

    btn.addEventListener('click', function () {
      var next = wrap.dataset.open !== 'true';
      wrap.dataset.open = String(next);
      btn.setAttribute('aria-expanded', String(next));
      setGroupOpen(dir, group.name, next);
    });
    wrap.appendChild(btn);

    var list = el('div', 'sb-items');
    items.forEach(function (p) {
      var a = el('a', 'lesson-link');
      a.href = relHref(p.file, isIndex);
      a.appendChild(el('span', 'lesson-num', pad3(p.id)));
      a.appendChild(el('span', 'lesson-title', p.title));
      a.appendChild(html('span', 'lesson-check', ICONS.check));
      if (p.file === cur) a.classList.add('active');
      if (isDone(p.file)) a.classList.add('done');
      list.appendChild(a);
    });
    wrap.appendChild(list);
    return { node: wrap, count: items.length };
  }

  function renderSidebar(isIndex) {
    if (!sidebarEls) return;
    var cur = currentFile();
    var groups = sidebarEls.groups;
    var q = state.query;
    // 搜索时跨题库：算法和 SQL 的命中一起列出来，按分区加粘性小标题
    var dirs = q ? DIR_ORDER : [state.tab];
    var totals = { algo: 0, sql: 0 };
    var shown = 0;

    groups.innerHTML = '';
    dirs.forEach(function (dir) {
      var built = [];
      groupByCat(dir).forEach(function (group) {
        var r = groupNode(dir, group, cur, isIndex);
        if (r) { built.push(r.node); totals[dir] += r.count; }
      });
      if (!built.length) return;
      if (q) {
        var head = el('div', 'sb-dir-head');
        head.appendChild(el('span', null, DIR_LABEL[dir]));
        head.appendChild(el('span', 'n', totals[dir] + ' 题'));
        groups.appendChild(head);
      }
      built.forEach(function (n) { groups.appendChild(n); });
      shown += built.length;
    });

    if (!shown) groups.appendChild(el('p', 'sb-empty', q ? '没有匹配的题目' : '暂无题目'));

    // Tab 上的数字：平时是题量，搜索时变成命中数
    sidebarEls.tabs.querySelectorAll('.sb-tab').forEach(function (b) {
      b.setAttribute('aria-selected', String(b.dataset.dir === state.tab));
      var n = b.querySelector('.sb-tab-count');
      if (n) n.textContent = q ? String(totals[b.dataset.dir] || 0) : String(totalOf(b.dataset.dir));
    });

    announce(q
      ? '找到 ' + (totals.algo + totals.sql) + ' 道题目'
      : DIR_LABEL[state.tab] + '共 ' + totalOf(state.tab) + ' 题');

    // 只滚侧栏容器自己。用 scrollIntoView 会把整个文档一起滚下去，
    // 导致首次打开题目页时正文被顶下去 80~140px（不是从顶部开始读）。
    var active = groups.querySelector('.lesson-link.active');
    var scroller = sidebarEls.scroll;
    if (active && scroller) {
      var sr = scroller.getBoundingClientRect();
      var ar = active.getBoundingClientRect();
      scroller.scrollTop += (ar.top - sr.top) - (sr.height - ar.height) / 2;
    }
  }

  function syncSearchInputs(value) {
    document.querySelectorAll('.nav-search').forEach(function (i) {
      if (i.value !== value) i.value = value;
    });
  }

  /* ---------------- 移动端抽屉 ---------------- */
  function openNav() {
    document.body.classList.add('nav-open');
    var btn = document.querySelector('.mobile-nav-btn');
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }
  function closeNav() {
    document.body.classList.remove('nav-open');
    var btn = document.querySelector('.mobile-nav-btn');
    if (btn) btn.setAttribute('aria-expanded', 'false');
  }
  function toggleNav() {
    if (document.body.classList.contains('nav-open')) closeNav();
    else openNav();
  }

  /* ======================================================================
     题头 / rail / 页脚
     ====================================================================== */
  function buildProblemHeader(p) {
    var wrap = el('div', 'problem-header');
    wrap.appendChild(el('span', 'problem-number', pad3(p.id)));
    var main = el('div', 'ph-main');
    main.appendChild(el('h1', null, p.title));
    var meta = el('div', 'ph-meta');
    meta.appendChild(el('span', 'tag-badge ' + DIFF_CLASS[p.diff], DIFF_MAP[p.diff]));
    (p.tags || []).forEach(function (t) { meta.appendChild(el('span', 'tag-badge tag-ds', t)); });
    if (p.leetcode) {
      var a = html('a', 'leetcode-chip', 'LeetCode ' + p.leetcode);
      a.href = leetcodeUrl(p);
      a.target = '_blank';
      a.rel = 'noopener';
      meta.appendChild(a);
    }
    main.appendChild(meta);
    wrap.appendChild(main);
    return wrap;
  }

  /** 从正文 h3 生成右侧目录，并做滚动高亮 */
  function buildRail(content, p, isIndex) {
    var headings = Array.prototype.slice.call(content.querySelectorAll('h2'));
    var rail = el('aside', 'rail');
    var inner = el('div', 'rail-inner');

    if (headings.length) {
      var tocWrap = el('nav', 'rail-card');
      tocWrap.setAttribute('aria-label', '本页目录');
      tocWrap.appendChild(el('div', 'rail-title', '本页目录'));
      var ul = el('ul', 'toc');
      headings.forEach(function (h, i) {
        if (!h.id) h.id = 'sec-' + (i + 1);
        var li = el('li');
        var a = el('a', null, h.textContent.trim());
        a.href = '#' + h.id;
        a.dataset.target = h.id;
        li.appendChild(a);
        ul.appendChild(li);
      });
      tocWrap.appendChild(ul);
      inner.appendChild(tocWrap);

      // 滚动高亮：取「最后一个已经滚过顶栏的分节」，任何位置都有唯一高亮项
      (function () {
        var links = {};
        var items = [];
        ul.querySelectorAll('a').forEach(function (a) {
          links[a.dataset.target] = a;
          items.push(a.dataset.target);
        });
        var ticking = false;

        function update() {
          var line = 96;                 // 顶栏高度 + 余量
          var current = items[0];
          for (var i = 0; i < headings.length; i++) {
            if (headings[i].getBoundingClientRect().top <= line) current = headings[i].id;
            else break;
          }
          Object.keys(links).forEach(function (id) {
            var on = id === current;
            links[id].classList.toggle('active', on);
            if (on) links[id].setAttribute('aria-current', 'true');
            else links[id].removeAttribute('aria-current');
          });
        }
        function onScroll() {
          if (ticking) return;
          ticking = true;
          requestAnimationFrame(function () { ticking = false; update(); });
        }
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', onScroll);
        update();
      })();
    }

    // 题目信息卡
    var card = el('div', 'rail-card');
    card.appendChild(el('div', 'rail-title', '题目信息'));
    var meta = el('div', 'rail-meta');
    function row(key, valEl) {
      var r = el('div', 'rail-meta-row');
      r.appendChild(el('span', 'rail-meta-key', key));
      var v = el('span', 'rail-meta-val');
      if (typeof valEl === 'string') v.textContent = valEl;
      else v.appendChild(valEl);
      r.appendChild(v);
      meta.appendChild(r);
    }
    row('分类', p.cat || '—');
    row('难度', DIFF_MAP[p.diff] || '—');
    if (p.leetcode) row('原题', tabLink('LeetCode ↗', leetcodeUrl(p)));
    card.appendChild(meta);

    var links = el('div', 'rail-links');
    var home = el('a', null, '← 返回题库总览');
    home.href = isIndex ? 'index.html' : '../index.html';
    links.appendChild(home);
    card.appendChild(links);
    inner.appendChild(card);

    rail.appendChild(inner);
    return rail;
  }

  function tabLink(text, href) {
    var a = el('a', null, text);
    a.href = href;
    a.target = '_blank';
    a.rel = 'noopener';
    return a;
  }

  function leetcodeUrl(p) {
    return p.lcUrl || 'https://leetcode.cn/problemset/';
  }

  function footBtn(cls, problem, dirText) {
    var node = el(problem ? 'a' : 'span', 'lf-btn ' + cls);
    if (!problem) node.classList.add('disabled');
    else node.href = problem.file.split('/').pop();
    node.appendChild(el('span', 'lf-dir', dirText));
    if (problem) node.appendChild(el('span', 'lf-title', problem.title));
    return node;
  }

  function buildLessonFoot(p) {
    var foot = el('footer', 'lesson-foot');
    var list = (PROBLEMS[p.dir] || []).filter(function (x) { return x.file; });
    var idx = list.findIndex(function (x) { return x.file === p.file; });
    foot.appendChild(footBtn('prev', list[idx - 1], '← 上一题'));
    foot.appendChild(footBtn('next', list[idx + 1], '下一题 →'));
    return foot;
  }

  /* ======================================================================
     正文增强：Python / Java 语言切换
     ====================================================================== */
  function enhanceCodeTabs(root) {
    var groups = [];
    var cur = [];
    function flush() { if (cur.length >= 2) groups.push(cur); cur = []; }

    root.querySelectorAll('h4').forEach(function (h4) {
      var lang = h4.textContent.trim().toLowerCase();
      var next = h4.nextElementSibling;
      if ((lang === 'python' || lang === 'java') && next && next.classList &&
          next.classList.contains('code-block-wrapper')) {
        cur.push({ h4: h4, wrap: next, lang: lang });
        return;
      }
      flush();
    });
    flush();

    groups.forEach(function (group) {
      var container = el('div', 'code-tabs');
      var head = el('div', 'code-tabs-head');
      group.forEach(function (item, i) {
        var btn = el('button', 'tab-btn' + (i === 0 ? ' active' : ''),
          item.lang === 'python' ? 'Python' : 'Java');
        btn.type = 'button';
        btn.setAttribute('data-lang', item.lang);
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', String(i === 0));
        head.appendChild(btn);
        item.wrap.classList.add('code-pane');
        item.wrap.setAttribute('data-lang', item.lang);
        if (i !== 0) item.wrap.classList.add('hidden');
      });
      container.appendChild(head);
      group[0].h4.parentNode.insertBefore(container, group[0].h4);
      group.forEach(function (item) {
        item.h4.remove();
        container.appendChild(item.wrap);
      });
    });
  }

  function switchCodeTab(btn) {
    var container = btn.closest('.code-tabs');
    if (!container) return;
    var lang = btn.getAttribute('data-lang');
    container.querySelectorAll('.tab-btn').forEach(function (b) {
      var on = b === btn;
      b.classList.toggle('active', on);
      b.setAttribute('aria-selected', String(on));
    });
    container.querySelectorAll('.code-pane').forEach(function (pane) {
      pane.classList.toggle('hidden', pane.getAttribute('data-lang') !== lang);
    });
  }

  /* ======================================================================
     复制代码
     ====================================================================== */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        ok ? resolve() : reject(new Error('copy failed'));
      } catch (e) { reject(e); }
    });
  }
  function copyCode(btn, codeId) {
    var node = document.getElementById(codeId);
    if (!node) return;
    copyText(node.textContent).then(function () {
      if (!btn) return;
      if (!btn.dataset.label) btn.dataset.label = btn.textContent;
      btn.textContent = '已复制';
      btn.classList.add('copied');
      setTimeout(function () {
        btn.textContent = btn.dataset.label;
        btn.classList.remove('copied');
      }, 1500);
    }).catch(function () {
      if (!btn) return;
      btn.textContent = '复制失败';
      setTimeout(function () { btn.textContent = btn.dataset.label || '复制'; }, 1500);
    });
  }

  /* ======================================================================
     首页：题库总览
     ====================================================================== */
  var catalogEls = null;

  function initCatalog() {
    var root = document.getElementById('catalog');
    if (!root) return;

    var stats = document.getElementById('heroStats');
    var tabsBox = document.getElementById('catalogTabs');
    var chips = document.getElementById('diffChips');
    catalogEls = { root: root, tabs: tabsBox, chips: chips, empty: document.getElementById('emptyState') };

    if (tabsBox) {
      DIR_ORDER.forEach(function (dir) {
        var count = (PROBLEMS[dir] || []).filter(function (p) { return p.file; }).length;
        var btn = el('button', 'catalog-tab');
        btn.type = 'button';
        btn.setAttribute('role', 'tab');
        btn.dataset.dir = dir;
        btn.innerHTML = DIR_LABEL[dir] + '<span class="sb-tab-count">' + count + '</span>';
        btn.addEventListener('click', function () { setTab(dir); });
        tabsBox.appendChild(btn);
      });
    }

    if (chips) {
      chips.addEventListener('click', function (e) {
        var btn = e.target.closest('button[data-diff]');
        if (btn) setDiff(btn.dataset.diff);
      });
    }

    on('tab', renderCatalog);
    on('diff', renderCatalog);
    on('query', renderCatalog);
    on('done', renderStats);

    function renderStats() {
      if (!stats) return;
      var algo = (PROBLEMS.algo || []).filter(function (p) { return p.file; }).length;
      var sql = (PROBLEMS.sql || []).filter(function (p) { return p.file; }).length;
      stats.innerHTML = '';
      var cells = [
        [algo, '算法题'],
        [sql, 'SQL 题'],
        [doneCount(), '已阅读']
      ];
      cells.forEach(function (c) {
        var box = el('div', 'hero-stat');
        box.appendChild(el('b', null, String(c[0])));
        box.appendChild(el('span', null, c[1]));
        stats.appendChild(box);
      });
    }

    catalogEls.renderStats = renderStats;
    renderStats();
    renderCatalog();
  }

  function renderCatalog() {
    if (!catalogEls) return;
    var q = state.query;
    var dirs = q ? DIR_ORDER : [state.tab];
    var totals = { algo: 0, sql: 0 };
    var total = 0;

    catalogEls.tabs.querySelectorAll('.catalog-tab').forEach(function (b) {
      b.setAttribute('aria-selected', String(b.dataset.dir === state.tab));
    });
    if (catalogEls.chips) {
      catalogEls.chips.querySelectorAll('button[data-diff]').forEach(function (b) {
        b.classList.toggle('active', b.dataset.diff === state.diff);
      });
    }

    catalogEls.root.innerHTML = '';
    dirs.forEach(function (dir) {
      var built = [];
      groupByCat(dir).forEach(function (group) {
        var items = group.items.filter(function (p) { return matches(p, dir); });
        if (!items.length) return;
        totals[dir] += items.length;

        var sec = el('details', 'cat-section');
        sec.open = true;
        var sum = document.createElement('summary');
        sum.appendChild(el('span', 'cat-name', group.name));
        var read = readCount(items);
        var count = el('span', 'count');
        if (read) {
          count.innerHTML = '已读 <span class="done">' + read + '</span>/' + items.length;
        } else {
          count.textContent = items.length + ' 题';
        }
        sum.appendChild(count);
        sec.appendChild(sum);

        var ul = el('ul', 'prob-grid');
        items.forEach(function (p) {
          var li = el('li', 'prob-card' + (isDone(p.file) ? ' is-done' : ''));
          var a = el('a', 'prob-card-link');
          a.href = p.file;
          var top = el('div', 'prob-card-top');
          top.appendChild(el('span', 'prob-card-num', pad3(p.id)));
          top.appendChild(el('span', 'prob-card-title', p.title));
          top.appendChild(html('span', 'prob-check', ICONS.check));
          a.appendChild(top);
          var meta = el('div', 'prob-card-meta');
          meta.appendChild(el('span', 'tag-badge ' + DIFF_CLASS[p.diff], DIFF_MAP[p.diff]));
          (p.tags || []).slice(0, 2).forEach(function (t) {
            meta.appendChild(el('span', 'tag-badge tag-ds', t));
          });
          a.appendChild(meta);
          li.appendChild(a);
          ul.appendChild(li);
        });
        sec.appendChild(ul);
        built.push(sec);
      });

      if (!built.length) return;
      if (q) {
        var head = el('div', 'catalog-dir-head');
        head.appendChild(el('span', null, DIR_LABEL[dir]));
        head.appendChild(el('span', 'n', totals[dir] + ' 题命中'));
        catalogEls.root.appendChild(head);
      }
      built.forEach(function (sec) { catalogEls.root.appendChild(sec); });
      total += totals[dir];
    });

    catalogEls.tabs.querySelectorAll('.catalog-tab').forEach(function (b) {
      // 搜索时显示命中数，平时显示题量（未被渲染的分区也要显示总量）
      var n = b.querySelector('.sb-tab-count');
      if (n) n.textContent = q ? String(totals[b.dataset.dir] || 0) : String(totalOf(b.dataset.dir));
    });

    if (catalogEls.empty) {
      catalogEls.empty.style.display = total ? 'none' : 'block';
    }
  }

  /* ======================================================================
     挂载
     ====================================================================== */
  function buildShell(isIndex, file) {
    var body = document.body;
    var main = el('main', 'main');
    main.id = 'main';

    var wrap = el('div', 'content-wrap');
    var content = el('article', 'content');
    var rail = null;

    if (file) {
      var p = BY_FILE[file];
      if (p) {
        content.appendChild(buildProblemHeader(p));

        // 把静态正文搬进 content
        Array.prototype.slice.call(body.children).forEach(function (node) {
          if (node.tagName === 'SCRIPT') return;
          if (node.classList && (node.classList.contains('topbar') ||
              node.classList.contains('shell') || node.classList.contains('scrim'))) return;
          content.appendChild(node);
        });

        content.appendChild(buildLessonFoot(p));
        rail = buildRail(content, p, isIndex);
        markDone(file);
      } else {
        Array.prototype.slice.call(body.children).forEach(function (node) {
          if (node.tagName !== 'SCRIPT') content.appendChild(node);
        });
      }
    } else {
      Array.prototype.slice.call(body.children).forEach(function (node) {
        if (node.tagName === 'SCRIPT') return;
        content.appendChild(node);
      });
    }

    if (rail) wrap.classList.add('has-rail');
    wrap.appendChild(content);
    if (rail) wrap.appendChild(rail);
    main.appendChild(wrap);

    var shell = el('div', 'shell');
    shell.appendChild(buildSidebar(isIndex));
    shell.appendChild(main);

    var live = el('div', 'sr-only');
    live.id = 'asn-live';
    live.setAttribute('role', 'status');
    live.setAttribute('aria-live', 'polite');
    body.appendChild(live);

    var skip = el('a', 'skip-link', '跳到正文');
    skip.href = '#main';
    body.appendChild(skip);

    var scrim = el('button', 'scrim');
    scrim.type = 'button';
    scrim.setAttribute('aria-label', '关闭导航');
    scrim.addEventListener('click', closeNav);
    body.appendChild(scrim);

    body.insertBefore(buildTopbar(isIndex), body.firstChild);
    body.appendChild(shell);

    return { main: main, content: content };
  }

  function bindGlobalEvents() {
    document.addEventListener('click', function (e) {
      var t = e.target;
      if (!t.closest) return;

      var themeBtn = t.closest('[data-theme-toggle]');
      if (themeBtn) {
        applyTheme(currentTheme() === 'dark' ? 'light' : 'dark', true);
        return;
      }

      var navBtn = t.closest('.mobile-nav-btn');
      if (navBtn) { toggleNav(); return; }

      var progBtn = t.closest('.tb-progress-trigger');
      if (progBtn) {
        var pop = progBtn.parentNode.querySelector('.popover');
        var willOpen = !pop || pop.dataset.open !== 'true';
        closePopovers();
        setPopover(pop, willOpen);
        return;
      }
      if (!t.closest('.popover')) closePopovers();

      var tabBtn = t.closest('.tab-btn');
      if (tabBtn) { switchCodeTab(tabBtn); return; }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeNav(); closePopovers(); }
      if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
        var input = document.querySelector('.nav-search');
        if (input) { e.preventDefault(); input.focus(); }
      }
    });

    // 点击侧栏链接后自动收起抽屉（移动端）
    document.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('.lesson-link') && window.innerWidth <= 900) closeNav();
    });

    // 打印前展开所有折叠块（否则打印稿会丢掉「自我检验 / 本地复现」的内容）
    window.addEventListener('beforeprint', function () {
      Array.prototype.slice.call(document.querySelectorAll('details:not([open])')).forEach(function (d) {
        d.dataset.wasClosed = '1';
        d.open = true;
      });
    });
    window.addEventListener('afterprint', function () {
      Array.prototype.slice.call(document.querySelectorAll('details[data-was-closed]')).forEach(function (d) {
        d.open = false;
        delete d.dataset.wasClosed;
      });
    });
  }

  function boot() {
    var file = currentFile();
    var isIndex = !file;

    initTheme();
    bindGlobalEvents();
    buildShell(isIndex, file);
    enhanceCodeTabs(document.body);

    if (isIndex) initCatalog();
    else refreshProgress();

    on('tab', function () { renderSidebar(isIndex); });
    on('query', function () { renderSidebar(isIndex); });
    on('progress', function () {
      refreshProgress();
      renderSidebar(isIndex);
      if (catalogEls) { catalogEls.renderStats(); renderCatalog(); }
    });

    if (!isIndex) {
      var prob = BY_FILE[file];
      if (prob) {
        state.tab = prob.dir;
        renderSidebar(isIndex);
      }
    }

    // 布局稳定后再触发一次 resize：图解表格按新容器宽度重绘
    requestAnimationFrame(function () {
      window.dispatchEvent(new Event('resize'));
      // 兜底：没有锚点时确保首屏停在顶部（平滑滚动历史位置会残留）
      if (!location.hash) window.scrollTo(0, 0);
    });
  }

  window.ASN = {
    PROBLEMS: PROBLEMS,
    ALL: ALL,
    ICONS: ICONS,
    isDone: isDone,
    getDone: function () { return Object.keys(doneSet); },
    doneCount: doneCount,
    applyTheme: applyTheme,
    currentTheme: currentTheme,
    on: on,
    setTab: setTab
  };
  window.copyCode = copyCode;

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

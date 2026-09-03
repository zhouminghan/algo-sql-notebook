/**
 * algo-sql-notebook — 公共 SVG 绘图库
 * 纯 SVG 内联渲染，通过 CSS 变量适配暗色/亮色模式。
 * 每个函数接受数据参数，返回可嵌入页面的 SVG 字符串。
 * 用法：document.getElementById('target').innerHTML = drawLinkedList({...});
 */

// ============================================================
// 内部工具函数
// ============================================================

/** 创建一个带 viewBox 的 SVG 容器 */
function svgWrap(width, height, inner) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" 
    width="100%" style="max-width:${width}px; font-family:system-ui,monospace;">${inner}</svg>`;
}

/** 转义 XML 特殊字符，防止单元格/标签内容破坏 SVG 结构 */
function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** 箭头 marker 定义 */
const ARROW_MARKER = `
<defs>
  <marker id="arrow-red" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="var(--color-pointer)" />
  </marker>
  <marker id="arrow-gray" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="var(--color-neutral)" />
  </marker>
</defs>`;

// ============================================================
// 链表可视化
// nodes: [{val, highlight: 'active'|'done'|null}]
// pointers: [{label, x, y, targetX, targetY, color: 'red'|'gray'}]
// ============================================================
function drawLinkedList({ nodes = [], pointers = [], width = 600, height = 120 } = {}) {
  const nodeW = 80, nodeH = 40, gap = 30, startX = 40, y = 40;
  let svgInner = ARROW_MARKER;
  
  nodes.forEach((n, i) => {
    const x = startX + i * (nodeW + gap);
    let cls = 'node-box';
    if (n.highlight === 'active') cls = 'node-active';
    else if (n.highlight === 'done') cls = 'node-done';
    // 节点主体
    svgInner += `<rect x="${x}" y="${y}" width="${nodeW}" height="${nodeH}" class="${cls}" rx="6"/>`;
    // 分隔线
    svgInner += `<line x1="${x + nodeW/2}" y1="${y}" x2="${x + nodeW/2}" y2="${y + nodeH}" stroke="var(--color-border)" stroke-width="1"/>`;
    // 值
    svgInner += `<text x="${x + nodeW/4}" y="${y + nodeH/2 + 4}" text-anchor="middle" class="node-val">${esc(n.val)}</text>`;
    // next 指示
    if (i < nodes.length - 1) {
      const nextX = x + nodeW;
      const nextY = y + nodeH / 2;
      const arrowEnd = startX + (i + 1) * (nodeW + gap);
      svgInner += `<line x1="${nextX}" y1="${nextY}" x2="${arrowEnd - 2}" y2="${nextY}" class="ptr-arrow" marker-end="url(#arrow-red)"/>`;
    }
    // null 终止
    if (i === nodes.length - 1 && n.showNull !== false) {
      svgInner += `<text x="${x + nodeW + 15}" y="${y + nodeH/2 + 4}" class="node-val" fill="var(--color-null)">NULL</text>`;
    }
  });

  // 指针标注
  pointers.forEach(p => {
    const color = p.color === 'red' ? 'var(--color-pointer)' : 'var(--color-neutral)';
    svgInner += `<text x="${p.x}" y="${p.y}" class="ptr-label" fill="${color}">${p.label}</text>`;
  });

  return svgWrap(width, height, svgInner);
}

// ============================================================
// 二叉树可视化
// nodes: [{val, x, y, highlight: 'active'|'done'|null}]
// edges: [{x1,y1,x2,y2}]
// ============================================================
function drawTree({ nodes = [], edges = [], width = 600, height = 300 } = {}) {
  let svgInner = ARROW_MARKER;
  
  edges.forEach(e => {
    svgInner += `<line x1="${e.x1}" y1="${e.y1}" x2="${e.x2}" y2="${e.y2}" class="edge"/>`;
  });
  
  nodes.forEach(n => {
    let cls = 'tree-node';
    if (n.highlight === 'active') cls = 'tree-active';
    else if (n.highlight === 'done') cls = 'tree-done';
    svgInner += `<circle cx="${n.x}" cy="${n.y}" r="18" class="${cls}"/>`;
    svgInner += `<text x="${n.x}" y="${n.y + 5}" text-anchor="middle" class="node-val">${esc(n.val)}</text>`;
  });
  
  return svgWrap(width, height, svgInner);
}

// ============================================================
// 图 + BFS/DFS
// vertices: [{label, x, y, color: 'active'|'visited'|'unvisited'}]
// edges: [{from, to, weight?, highlight?}]
// sidePanel: {title, items: []} — 队列/栈状态侧栏
// ============================================================
function drawGraph({ vertices = [], edges = [], sidePanel = null, width = 640, height = 300 } = {}) {
  let svgInner = ARROW_MARKER;
  const vMap = {};
  vertices.forEach(v => { vMap[v.label] = v; });
  
  edges.forEach(e => {
    const f = vMap[e.from], t = vMap[e.to];
    if (!f || !t) return;
    const color = e.highlight ? 'var(--color-pointer)' : 'var(--color-neutral)';
    svgInner += `<line x1="${f.x}" y1="${f.y}" x2="${t.x}" y2="${t.y}" stroke="${color}" stroke-width="2"/>`;
    if (e.weight) {
      const mx = (f.x + t.x) / 2, my = (f.y + t.y) / 2 - 8;
      svgInner += `<text x="${mx}" y="${my}" text-anchor="middle" class="idx-label">${e.weight}</text>`;
    }
  });
  
  vertices.forEach(v => {
    const colorMap = { active: 'var(--color-highlight)', visited: 'var(--color-done)', unvisited: 'var(--color-neutral)' };
    const fill = colorMap[v.color] || 'var(--color-neutral)';
    svgInner += `<circle cx="${v.x}" cy="${v.y}" r="20" fill="${fill}" opacity="0.2" stroke="${fill}" stroke-width="2"/>`;
    svgInner += `<text x="${v.x}" y="${v.y + 5}" text-anchor="middle" class="node-val">${v.label}</text>`;
  });
  
  if (sidePanel) {
    const px = width - 150;
    svgInner += `<text x="${px}" y="25" class="idx-label" font-weight="bold">${sidePanel.title}</text>`;
    svgInner += `<rect x="${px - 10}" y="30" width="140" height="${sidePanel.items.length * 24 + 10}" fill="none" stroke="var(--color-border)" rx="4"/>`;
    sidePanel.items.forEach((item, i) => {
      // ... queue/stack entries
    });
  }
  
  return svgWrap(width, height, svgInner);
}

// ============================================================
// DP 表格 + 填表方向
// table: {headers: [], rows: [[{val, highlight}]], arrows: [{x1,y1,x2,y2,dir}]}
// ============================================================
function drawDPTable({ headers = [], rows = [], arrows = [], width = 600, height = 0 } = {}) {
  const cellW = 56, cellH = 36, startX = 30, startY = 40;
  const realH = Math.max(height, startY + rows.length * cellH + 40);
  let svgInner = ARROW_MARKER;
  
  // 表头
  headers.forEach((h, i) => {
    svgInner += `<rect x="${startX + i * cellW}" y="${startY}" width="${cellW}" height="${cellH}" class="cell" fill="var(--color-tag-bg)"/>`;
    svgInner += `<text x="${startX + i * cellW + cellW/2}" y="${startY + cellH/2 + 4}" text-anchor="middle" class="node-val">${h}</text>`;
  });
  
  // 数据行
  rows.forEach((row, ri) => {
    row.forEach((cell, ci) => {
      const x = startX + ci * cellW;
      const y = startY + cellH + ri * cellH;
      const cls = cell.highlight ? 'cell-highlight' : 'cell';
      svgInner += `<rect x="${x}" y="${y}" width="${cellW}" height="${cellH}" class="${cls}"/>`;
      svgInner += `<text x="${x + cellW/2}" y="${y + cellH/2 + 4}" text-anchor="middle" class="node-val">${cell.val !== undefined ? cell.val : ''}</text>`;
    });
  });
  
  // 填表方向箭头
  arrows.forEach(a => {
    svgInner += `<line x1="${a.x1}" y1="${a.y1}" x2="${a.x2}" y2="${a.y2}" stroke="var(--color-pointer)" stroke-width="1.5" stroke-dasharray="4,2"/>`;
  });
  
  return svgWrap(width, realH, svgInner);
}

// ============================================================
// 哈希表（数组 → 链表 → 红黑树演进）
// buckets: [{index, entries: [{key,val,isTreeNode?}]}]
// highlight: {bucketIndex, entryIndex, getPath: [{x1,y1,x2,y2}]}
// ============================================================
function drawHashmap({ buckets = [], highlight = null, width = 600, height = 300, title = '' } = {}) {
  const bucketW = 200, bucketX = 30, bucketStartY = 30, bucketGap = 28, entryH = 24;
  let svgInner = ARROW_MARKER;
  
  if (title) {
    svgInner += `<text x="15" y="18" class="idx-label" font-weight="bold">${title}</text>`;
  }
  
  buckets.forEach((b, bi) => {
    const by = bucketStartY + bi * bucketGap;
    // 桶槽
    svgInner += `<rect x="${bucketX}" y="${by}" width="30" height="20" fill="none" stroke="var(--color-border)" rx="3"/>`;
    svgInner += `<text x="${bucketX + 15}" y="${by + 14}" text-anchor="middle" class="node-val" font-size="10">${b.index}</text>`;
    
    // 链表/树节点（统一渲染；树节点用 rx 全圆角示意）
    let ex = bucketX + 35;
    b.entries.forEach((entry, ei) => {
      const ey = by;
      const isHighlight = highlight && highlight.bucketIndex === bi && highlight.entryIndex === ei;
      const rx = entry.isTreeNode ? 10 : 3;
      svgInner += `<rect x="${ex}" y="${ey}" width="44" height="${entryH}" class="${isHighlight ? 'node-active' : 'node-box'}" rx="${rx}"/>`;
      svgInner += `<text x="${ex + 22}" y="${ey + 16}" text-anchor="middle" class="node-val" font-size="10">${esc(entry.key)}:${esc(entry.val)}</text>`;
      
      // 节点间箭头
      if (ei < b.entries.length - 1) {
        const arrowX = ex + 44;
        svgInner += `<line x1="${arrowX}" y1="${ey + 12}" x2="${arrowX + 16}" y2="${ey + 12}" class="ptr-arrow" marker-end="url(#arrow-red)"/>`;
        ex = arrowX + 20;
      } else {
        ex = ex + 50;
      }
    });
  });

  // 查找路径箭头
  if (highlight && highlight.getPath) {
    highlight.getPath.forEach(p => {
      svgInner += `<line x1="${p.x1}" y1="${p.y1}" x2="${p.x2}" y2="${p.y2}" stroke="var(--color-pointer)" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arrow-red)"/>`;
    });
  }
  
  return svgWrap(width, Math.max(height, bucketStartY + buckets.length * bucketGap + 30), svgInner);
}

// ============================================================
// 栈/队列/单调栈
// items: [{val, label?}], type: 'stack'|'queue', pushEvent?, popEvent?
// ============================================================
function drawStack({ items = [], type = 'stack', width = 300, height = 250 } = {}) {
  const cellW = 100, cellH = 30, cx = (width - cellW) / 2;
  let svgInner = ARROW_MARKER;
  
  items.forEach((item, i) => {
    const y = type === 'stack' ? height - 40 - i * (cellH + 2) : 20 + i * (cellH + 2);
    svgInner += `<rect x="${cx}" y="${y}" width="${cellW}" height="${cellH}" class="node-box" rx="4"/>`;
    svgInner += `<text x="${cx + cellW/2}" y="${y + cellH/2 + 4}" text-anchor="middle" class="node-val">${item.val}</text>`;
    if (item.label) {
      svgInner += `<text x="${cx - 5}" y="${y + cellH/2 + 4}" text-anchor="end" class="idx-label">${item.label}</text>`;
    }
  });
  
  if (type === 'stack') {
    svgInner += `<text x="${cx + cellW/2}" y="${height - 50 - items.length * (cellH + 2)}" text-anchor="middle" class="ptr-label">↑ push / pop</text>`;
  } else {
    svgInner += `<text x="${cx - 15}" y="${15}" text-anchor="end" class="ptr-label">enqueue →</text>`;
    svgInner += `<text x="${cx + cellW + 15}" y="${15}" class="ptr-label">→ dequeue</text>`;
  }
  
  return svgWrap(width, height, svgInner);
}

// ============================================================
// 双指针 / 滑动窗口
// arr: [value], left, right, window?: {start, end}
// ============================================================
function drawTwoPointers({ arr = [], left = 0, right = 0, window = null, width = 600, height = 120 } = {}) {
  const cellW = 40, cellH = 36, startX = 30, cellY = 45;
  let svgInner = ARROW_MARKER;
  const totalW = arr.length * cellW;
  const adjustedW = Math.max(width, startX + totalW + 30);
  
  // 窗口高亮
  if (window) {
    const wx = startX + window.start * cellW;
    const ww = (window.end - window.start + 1) * cellW;
    svgInner += `<rect x="${wx}" y="${cellY}" width="${ww}" height="${cellH}" fill="var(--color-highlight)" opacity="0.15" rx="4"/>`;
  }
  
  arr.forEach((val, i) => {
    const x = startX + i * cellW;
    const isHi = i === left || i === right;
    svgInner += `<rect x="${x}" y="${cellY}" width="${cellW}" height="${cellH}" class="${isHi ? 'cell-highlight' : 'cell'}" rx="2"/>`;
    svgInner += `<text x="${x + cellW/2}" y="${cellY + cellH/2 + 4}" text-anchor="middle" class="node-val">${esc(val)}</text>`;
    svgInner += `<text x="${x + cellW/2}" y="${cellY - 5}" text-anchor="middle" class="idx-label">${i}</text>`;
  });
  
  // 指针箭头
  [['left', left, 'var(--color-done)'], ['right', right, 'var(--color-pointer)']].forEach(([label, idx, color]) => {
    const px = startX + idx * cellW + cellW / 2;
    svgInner += `<text x="${px}" y="${cellY + cellH + 20}" text-anchor="middle" class="ptr-label" fill="${color}">${label}=${idx}</text>`;
    svgInner += `<line x1="${px}" y1="${cellY + cellH}" x2="${px}" y2="${cellY + cellH + 10}" stroke="${color}" stroke-width="1.5"/>`;
  });
  
  return svgWrap(adjustedW, height, svgInner);
}

// ============================================================
// 二分查找区间收缩
// arr: [value], left, mid, right, excludedRanges: [{start,end}]
// ============================================================
function drawBinarySearch({ arr = [], left = 0, mid = 0, right = 0, excludedRanges = [], width = 600, height = 120 } = {}) {
  const cellW = 40, cellH = 36, startX = 30, cellY = 45;
  let svgInner = ARROW_MARKER;
  const totalW = arr.length * cellW;
  const adjustedW = Math.max(width, startX + totalW + 30);
  
  // 排除区域变灰
  excludedRanges.forEach(r => {
    const ex = startX + r.start * cellW;
    const ew = (r.end - r.start + 1) * cellW;
    svgInner += `<rect x="${ex}" y="${cellY}" width="${ew}" height="${cellH}" fill="var(--color-neutral)" opacity="0.15" rx="2"/>`;
  });
  
  arr.forEach((val, i) => {
    const x = startX + i * cellW;
    let cls = 'cell';
    if (i === mid) cls = 'cell-highlight';
    svgInner += `<rect x="${x}" y="${cellY}" width="${cellW}" height="${cellH}" class="${cls}" rx="2"/>`;
    svgInner += `<text x="${x + cellW/2}" y="${cellY + cellH/2 + 4}" text-anchor="middle" class="node-val">${esc(val)}</text>`;
    svgInner += `<text x="${x + cellW/2}" y="${cellY - 5}" text-anchor="middle" class="idx-label">${i}</text>`;
  });
  
  // L / M / R 指针
  [
    ['L', left, 'var(--color-done)'],
    ['M', mid, 'var(--color-highlight)'],
    ['R', right, 'var(--color-pointer)']
  ].forEach(([label, idx, color]) => {
    const px = startX + idx * cellW + cellW / 2;
    svgInner += `<text x="${px}" y="${cellY + cellH + 20}" text-anchor="middle" class="ptr-label" fill="${color}">${label}=${idx}</text>`;
    svgInner += `<line x1="${px}" y1="${cellY + cellH}" x2="${px}" y2="${cellY + cellH + 10}" stroke="${color}" stroke-width="1.5"/>`;
  });
  
  return svgWrap(adjustedW, height, svgInner);
}

// ============================================================
// 回溯递归树
// nodes: [{val, x, y, color: 'path'|'pruned'|'normal'}]
// edges: [{x1,y1,x2,y2,color}]
// ============================================================
function drawBacktrack({ nodes = [], edges = [], width = 600, height = 350 } = {}) {
  let svgInner = ARROW_MARKER;
  
  edges.forEach(e => {
    const color = e.color === 'path' ? 'var(--color-highlight)' : e.color === 'pruned' ? 'var(--color-null)' : 'var(--color-neutral)';
    const dash = e.color === 'pruned' ? ' stroke-dasharray="4,3"' : '';
    svgInner += `<line x1="${e.x1}" y1="${e.y1}" x2="${e.x2}" y2="${e.y2}" stroke="${color}" stroke-width="1.5"${dash}/>`;
  });
  
  nodes.forEach(n => {
    const colorMap = { path: 'var(--color-highlight)', pruned: 'var(--color-null)', normal: 'var(--color-neutral)' };
    const stroke = colorMap[n.color] || 'var(--color-neutral)';
    const fill = n.color === 'pruned' ? 'none' : (n.color === 'path' ? 'var(--color-highlight)' : 'var(--color-bg-frame)');
    svgInner += `<circle cx="${n.x}" cy="${n.y}" r="14" fill="${fill}" stroke="${stroke}" stroke-width="1.5" opacity="${n.color === 'pruned' ? 0.4 : 1}"/>`;
    if (n.color === 'pruned') {
      svgInner += `<text x="${n.x}" y="${n.y + 5}" text-anchor="middle" class="node-val" fill="var(--color-null)">×</text>`;
    } else {
      svgInner += `<text x="${n.x}" y="${n.y + 4}" text-anchor="middle" class="node-val" font-size="10">${n.val}</text>`;
    }
  });
  
  return svgWrap(width, height, svgInner);
}

// ============================================================
// 通用数据表格
// headers: [string], rows: [[string]]
// ============================================================
function drawTable({ headers = [], rows = [], width = 600, height = 0 } = {}) {
  const cellH = 32, colW = Math.max(80, Math.floor((width - 20) / Math.max(headers.length, 1)));
  const startX = 10, startY = 25;
  const totalH = Math.max(height, startY + (rows.length + 1) * cellH + 10);
  let svgInner = '';
  
  // 表头
  headers.forEach((h, i) => {
    svgInner += `<rect x="${startX + i * colW}" y="${startY}" width="${colW}" height="${cellH}" class="cell" fill="var(--color-tag-bg)" stroke="var(--color-border)"/>`;
    svgInner += `<text x="${startX + i * colW + colW/2}" y="${startY + cellH/2 + 5}" text-anchor="middle" class="node-val" font-weight="bold">${h}</text>`;
  });
  
  rows.forEach((row, ri) => {
    row.forEach((cell, ci) => {
      const x = startX + ci * colW;
      const y = startY + (ri + 1) * cellH;
      svgInner += `<rect x="${x}" y="${y}" width="${colW}" height="${cellH}" fill="none" stroke="var(--color-border)"/>`;
      const val = typeof cell === 'string' ? cell : (cell && cell.val !== undefined ? cell.val : '');
      const cls = (typeof cell === 'object' && cell.highlight) ? 'cell-highlight' : '';
      if (cls) svgInner += `<rect x="${x}" y="${y}" width="${colW}" height="${cellH}" class="${cls}"/>`;
      svgInner += `<text x="${x + colW/2}" y="${y + cellH/2 + 5}" text-anchor="middle" class="node-val" font-size="11">${val}</text>`;
    });
  });
  
  return svgWrap(width, totalH, svgInner);
}

// ============================================================
// SQL 前后对比双表格 — 核心函数
// before: {headers, rows}
// after: {headers, rows}
// ============================================================
function diffTable({ before = {}, after = {}, width = 600, height = 0 } = {}) {
  const halfW = (width - 30) / 2;
  let svgInner = ARROW_MARKER;
  
  const beforeH = 25 + (before.rows ? before.rows.length + 1 : 1) * 32 + 10;
  const afterH = 25 + (after.rows ? after.rows.length + 1 : 1) * 32 + 10;
  const totalH = Math.max(height, Math.max(beforeH, afterH));
  
  // 左：执行前
  svgInner += `<text x="${10}" y="18" class="idx-label" font-weight="bold">📥 执行前</text>`;
  svgInner += drawTableRaw({ headers: before.headers || [], rows: before.rows || [], startX: 10, startY: 25, colW: Math.max(60, halfW / Math.max(before.headers ? before.headers.length : 1, 1)), cellH: 28 });
  
  // 右：执行后
  const rightX = halfW + 20;
  svgInner += `<text x="${rightX}" y="18" class="idx-label" font-weight="bold">📤 执行后</text>`;
  svgInner += drawTableRaw({ headers: after.headers || [], rows: after.rows || [], startX: rightX, startY: 25, colW: Math.max(60, halfW / Math.max(after.headers ? after.headers.length : 1, 1)), cellH: 28 });
  
  // 中间箭头
  const arrowY = totalH / 2;
  svgInner += `<line x1="${halfW + 5}" y1="${arrowY}" x2="${rightX - 5}" y2="${arrowY}" stroke="var(--color-pointer)" stroke-width="2" marker-end="url(#arrow-red)"/>`;
  svgInner += `<text x="${(halfW + rightX) / 2}" y="${arrowY - 5}" text-anchor="middle" class="idx-label">SQL</text>`;
  
  return svgWrap(width, totalH + 10, svgInner);
}

/** 单元格文本渲染：支持 {val, color, bold} 对象；✓/✗ 自动语义着色 */
function cellText(cell, x, y, colW, cellH) {
  const isObj = typeof cell === 'object' && cell !== null;
  const val = isObj ? (cell.val !== undefined ? cell.val : '') : (cell !== undefined ? cell : '');
  let fill = '';
  if (isObj && cell.color) fill = cell.color;
  else if (val === '✓') fill = 'var(--color-done)';
  else if (val === '✗') fill = 'var(--color-pointer)';
  const bold = (isObj && cell.bold) || fill ? ' font-weight="bold"' : '';
  return `<text x="${x + colW/2}" y="${y + cellH/2 + 4}" text-anchor="middle" class="node-val" font-size="10"${fill ? ` fill="${fill}"` : ''}${bold}>${esc(val)}</text>`;
}

/** 内部表格绘制（不含 width 计算）；表头主色淡底、斑马纹、✓/✗ 着色，层次分明 */
function drawTableRaw({ headers = [], rows = [], startX = 0, startY = 0, colW = 80, cellH = 28, zebra = true } = {}) {
  let svg = '';
  headers.forEach((h, i) => {
    const x = startX + i * colW;
    svg += `<rect x="${x}" y="${startY}" width="${colW}" height="${cellH}" fill="var(--pico-primary)" opacity="0.12" stroke="var(--color-border)"/>`;
    svg += `<text x="${x + colW/2}" y="${startY + cellH/2 + 4}" text-anchor="middle" class="node-val" font-size="10" font-weight="bold" fill="var(--pico-primary)">${esc(h)}</text>`;
  });
  rows.forEach((row, ri) => {
    const y = startY + (ri + 1) * cellH;
    if (zebra && ri % 2 === 1) {
      svg += `<rect x="${startX}" y="${y}" width="${headers.length * colW}" height="${cellH}" fill="var(--color-tag-bg)" opacity="0.6"/>`;
    }
    row.forEach((cell, ci) => {
      const x = startX + ci * colW;
      svg += `<rect x="${x}" y="${y}" width="${colW}" height="${cellH}" fill="none" stroke="var(--color-border)"/>`;
      svg += cellText(cell, x, y, colW, cellH);
    });
  });
  return svg;
}

// ============================================================
// GROUP BY 分组框选
// ============================================================
function drawGroupBy({ before = {}, after = {}, groups = [], width = 600, height = 0 } = {}) {
  let svgInner = ARROW_MARKER;
  const colW = 80, cellH = 28, startX = 10, startY = 25;
  
  // 原始表
  const headers = before.headers || [];
  const rows = before.rows || [];
  svgInner += `<text x="${startX}" y="18" class="idx-label" font-weight="bold">📥 原始表</text>`;
  
  // 分组框选（用不同颜色框）
  groups.forEach((g, gi) => {
    const colors = ['var(--color-highlight)', 'var(--color-done)', 'var(--color-pointer)', '#8b5cf6'];
    const color = colors[gi % colors.length];
    const minRow = Math.min(...g.rowIndices);
    const maxRow = Math.max(...g.rowIndices);
    svgInner += `<rect x="${startX}" y="${startY + (minRow + 1) * cellH}" 
      width="${headers.length * colW}" height="${(maxRow - minRow + 1) * cellH}" 
      fill="${color}" opacity="0.1" stroke="${color}" stroke-width="2" rx="4" stroke-dasharray="5,3"/>`;
    svgInner += `<text x="${startX + headers.length * colW + 5}" y="${startY + (minRow + 1) * cellH + cellH}" class="idx-label" fill="${color}">${g.label || '组'+(gi+1)}</text>`;
  });
  
  svgInner += drawTableRaw({ headers, rows, startX, startY, colW, cellH });
  
  // 结果表
  const resY = startY + (rows.length + 1) * cellH + 40;
  svgInner += `<text x="${startX}" y="${resY - 7}" class="idx-label" font-weight="bold">📤 聚合结果</text>`;
  svgInner += drawTableRaw({ headers: after.headers || [], rows: after.rows || [], startX, startY: resY, colW, cellH });
  
  const totalH = Math.max(height, resY + (after.rows ? after.rows.length + 1 : 1) * cellH + 20);
  return svgWrap(width, totalH, svgInner);
}

// ============================================================
// 窗口函数 Partition/Order/新列
// frames: [{type:'partition'|'order'|'result', desc, table}]
// ============================================================
function drawWindowFunc({ frames = [], width = 0, height = 0 } = {}) {
  const cellH = 28;
  // 按最多列数自适应：宽度至少容纳内容（每列 90px），显式 width 更大则跟随
  const maxCols = Math.max(...frames.map(f => (f.table && f.table.headers ? f.table.headers.length : 1)), 1);
  const finalW = Math.max(width, 10 + maxCols * 90);
  const colW = Math.floor((finalW - 20) / maxCols);
  let svgInner = ARROW_MARKER;
  let currentY = 25;
  
  frames.forEach((frame, fi) => {
    const { type, desc, table } = frame;
    const headers = table.headers || [];
    const rows = table.rows || [];
    const frameH = (rows.length + 1) * cellH + 50;
    
    if (desc) {
      svgInner += `<text x="10" y="${currentY}" class="idx-label" font-weight="bold">${fi + 1}. ${desc}</text>`;
    }
    
    if (type === 'partition') {
      // 画出分区框
      const partitions = frame.partitions || [];
      partitions.forEach((p, pi) => {
        const colors = ['var(--color-highlight)', 'var(--color-done)', 'var(--color-pointer)', '#8b5cf6'];
        const color = colors[pi % colors.length];
        svgInner += `<rect x="10" y="${currentY + 9 + (p.startRow + 1) * cellH}" 
          width="${headers.length * colW}" height="${p.count * cellH}" 
          fill="${color}" opacity="0.1" stroke="${color}" stroke-width="2" rx="4" stroke-dasharray="5,3"/>`;
      });
    }
    
    svgInner += drawTableRaw({ headers, rows, startX: 10, startY: currentY + 9, colW, cellH });
    
    if (type === 'result') {
      // 高亮新增列
      const newColIdx = frame.newColIndex !== undefined ? frame.newColIndex : headers.length - 1;
      const hx = 10 + newColIdx * colW;
      svgInner += `<rect x="${hx}" y="${currentY + 9}" width="${colW}" height="${(rows.length + 1) * cellH}" 
        fill="var(--color-highlight)" opacity="0.15" rx="2"/>`;
    }
    
    currentY += frameH;
  });
  
  return svgWrap(finalW, Math.max(height, currentY + 10), svgInner);
}

// ============================================================
// JOIN 连线匹配
// mode: 'inner'|'left'|'right'|'full'
// left: {headers, rows, name}, right: {headers, rows, name}
// matches: [{leftRow, rightRow}]
// result: {headers, rows}
// ============================================================
function drawJoin({ mode = 'inner', left = {}, right = {}, matches = [], result = {}, width = 600, height = 0 } = {}) {
  let svgInner = ARROW_MARKER;
  const colW = 70, cellH = 26, gap = 20;
  const leftCols = (left.headers || []).length;
  const rightCols = (right.headers || []).length;
  const leftX = 10;
  const rightX = leftX + leftCols * colW + gap;
  const startY = 25;
  
  // 左表
  svgInner += `<text x="${leftX}" y="18" class="idx-label" font-weight="bold">${left.name || '左表'}</text>`;
  svgInner += drawTableRaw({ headers: left.headers || [], rows: left.rows || [], startX: leftX, startY, colW, cellH });
  
  // 右表
  svgInner += `<text x="${rightX}" y="18" class="idx-label" font-weight="bold">${right.name || '右表'}</text>`;
  svgInner += drawTableRaw({ headers: right.headers || [], rows: right.rows || [], startX: rightX, startY, colW, cellH });
  
  // 匹配连线
  matches.forEach((m, mi) => {
    const leftY = startY + (m.leftRow + 1.5) * cellH;
    const rightY = startY + (m.rightRow + 1.5) * cellH;
    const midX = (leftX + leftCols * colW + rightX) / 2;
    svgInner += `<path d="M${leftX + leftCols * colW} ${leftY} Q${midX} ${leftY} ${midX} ${(leftY + rightY) / 2} Q${midX} ${rightY} ${rightX} ${rightY}" 
      fill="none" stroke="var(--color-pointer)" stroke-width="1.5" opacity="0.6"/>`;
  });
  
  // 结果表
  const resY = startY + Math.max(left.rows.length, right.rows.length) * cellH + cellH + 40;
  svgInner += `<text x="${leftX}" y="${resY - 7}" class="idx-label" font-weight="bold">📤 ${mode.toUpperCase()} JOIN 结果</text>`;
  const resCols = (result.headers || []).length;
  const resColW = Math.min(80, (width - 20) / Math.max(resCols, 1));
  svgInner += drawTableRaw({ headers: result.headers || [], rows: result.rows || [], startX: leftX, startY: resY, colW: resColW, cellH });
  
  const totalH = Math.max(height, resY + (result.rows ? result.rows.length + 1 : 1) * cellH + 20);
  return svgWrap(width, totalH, svgInner);
}

// ============================================================
// 子查询逐层展开
// layers: [{label, table: {headers, rows}}]
// ============================================================
function drawSubquery({ layers = [], width = 600, height = 0 } = {}) {
  let svgInner = ARROW_MARKER;
  const colW = 80, cellH = 28;
  let currentY = 25;
  
  layers.forEach((layer, li) => {
    const { label, table } = layer;
    const rows = table.rows || [];
    svgInner += `<text x="10" y="${currentY}" class="idx-label" font-weight="bold">${li + 1}. ${label}</text>`;
    svgInner += drawTableRaw({ headers: table.headers || [], rows, startX: 10, startY: currentY + 9, colW, cellH });
    
    if (li < layers.length - 1) {
      const arrowY = currentY + 9 + (rows.length + 1) * cellH + 10;
      svgInner += `<text x="${width / 2 - 20}" y="${arrowY + 8}" text-anchor="middle" class="ptr-label">↓ 传给外层</text>`;
    }
    
    currentY += 9 + (rows.length + 1) * cellH + 28;
  });
  
  return svgWrap(width, Math.max(height, currentY + 10), svgInner);
}

// ============================================================
// 递归 CTE 逐轮扩展
// frames: [{round, description, table: {headers, rows}}]
// ============================================================
function drawCTE({ frames = [], width = 600, height = 0 } = {}) {
  let svgInner = ARROW_MARKER;
  const colW = 80, cellH = 28;
  let currentY = 25;
  
  frames.forEach((frame, fi) => {
    const { round, description, table } = frame;
    const rows = table.rows || [];
    svgInner += `<text x="10" y="${currentY}" class="idx-label" font-weight="bold">轮次 ${round || fi}：${description}</text>`;
    svgInner += drawTableRaw({ headers: table.headers || [], rows, startX: 10, startY: currentY + 9, colW, cellH });
    currentY += 9 + (rows.length + 1) * cellH + 28;
  });
  
  return svgWrap(width, Math.max(height, currentY + 10), svgInner);
}

// ============================================================
// 字符串函数变换
// input: {headers, rows} output: {headers, rows} colIndex 函数作用列
// ============================================================
function drawStringFunc({ input = {}, output = {}, colIndex = 0, funcName = 'string_func', width = 600, height = 0 } = {}) {
  return simpleTransform({ input, output, colIndex, funcName, width, height, 
    desc: '字符串变换',
    beforeLabel: '📥 原始表',
    afterLabel: `📤 ${funcName} 结果` });
}

// ============================================================
// 日期函数变换
// ============================================================
function drawDateFunc({ input = {}, output = {}, colIndex = 0, funcName = 'date_func', width = 600, height = 0 } = {}) {
  return simpleTransform({ input, output, colIndex, funcName, width, height,
    desc: '日期变换',
    beforeLabel: '📥 原始表',
    afterLabel: `📤 ${funcName} 结果` });
}

// ============================================================
// CASE WHEN 分支决策
// input: {headers, rows} output: {headers, rows}
// conditions: [{col, operator, value, result, rowIndex}]
// ============================================================
function drawConditionFunc({ input = {}, output = {}, width = 600, height = 0 } = {}) {
  return simpleTransform({ input, output, width, height,
    desc: '条件分支',
    beforeLabel: '📥 原始表',
    afterLabel: '📤 CASE WHEN 结果' });
}

/** 简单前后变换通用函数 */
function simpleTransform({ input = {}, output = {}, width = 600, height = 0, beforeLabel = '📥 Before', afterLabel = '📤 After' } = {}) {
  let svgInner = ARROW_MARKER;
  const colW = 80, cellH = 28;
  const inRows = (input.rows || []).length + 1;
  const inX = 10, inY = 25;
  
  svgInner += `<text x="${inX}" y="18" class="idx-label" font-weight="bold">${beforeLabel}</text>`;
  svgInner += drawTableRaw({ headers: input.headers || [], rows: input.rows || [], startX: inX, startY: inY, colW, cellH });
  
  const outY = inY + inRows * cellH + 30;
  svgInner += `<text x="${inX}" y="${outY - 7}" class="idx-label" font-weight="bold">${afterLabel}</text>`;
  svgInner += drawTableRaw({ headers: output.headers || [], rows: output.rows || [], startX: inX, startY: outY, colW, cellH });
  
  // 箭头
  const arrowY = inY + inRows * cellH + 5;
  svgInner += `<line x1="${width / 2}" y1="${arrowY}" x2="${width / 2}" y2="${outY - 12}" stroke="var(--color-pointer)" stroke-width="2" marker-end="url(#arrow-red)"/>`;
  
  const totalH = Math.max(height, outY + (output.rows ? output.rows.length + 1 : 1) * cellH + 20);
  return svgWrap(width, totalH, svgInner);
}

// ============================================================
// UNION / INTERSECT / EXCEPT 集合操作
// mode: 'union'|'union_all'|'intersect'|'except'
// ============================================================
function drawSetOp({ mode = 'union', tables = [], result = {}, width = 600, height = 0 } = {}) {
  let svgInner = ARROW_MARKER;
  const colW = 80, cellH = 28, gap = 20;
  const numTabs = tables.length;
  const totalTabW = numTabs * 3 * colW + (numTabs - 1) * gap;
  const startX = Math.max(10, (width - totalTabW) / 2);
  const startY = 25;
  
  tables.forEach((t, ti) => {
    const tx = startX + ti * (3 * colW + gap);
    svgInner += `<text x="${tx}" y="18" class="idx-label" font-weight="bold">表 ${ti + 1} (${t.rows ? t.rows.length : 0}行)</text>`;
    svgInner += drawTableRaw({ headers: t.headers || [], rows: t.rows || [], startX: tx, startY, colW, cellH });
    if (ti < numTabs - 1) {
      const opX = tx + (t.headers || []).length * colW + 5;
      const opY = startY + 40;
      svgInner += `<text x="${opX}" y="${opY}" class="ptr-label" font-size="14" font-weight="bold">${mode.toUpperCase()}</text>`;
    }
  });
  
  const resY = startY + 80;
  svgInner += `<text x="${startX}" y="${resY - 7}" class="idx-label" font-weight="bold">📤 ${mode.toUpperCase()} 结果 (${result.rows ? result.rows.length : 0}行)</text>`;
  svgInner += drawTableRaw({ headers: result.headers || [], rows: result.rows || [], startX, startY: resY, colW, cellH });
  
  const totalH = Math.max(height, resY + (result.rows ? result.rows.length + 1 : 1) * cellH + 20);
  return svgWrap(width, totalH, svgInner);
}

// ============================================================
// 行转列 / 列转行 (PIVOT)
// direction: 'to_wide'|'to_long'
// ============================================================
function drawPivot({ direction = 'to_wide', input = {}, output = {}, width = 600, height = 0 } = {}) {
  return simpleTransform({ input, output, width, height,
    beforeLabel: `📥 ${direction === 'to_wide' ? '长表' : '宽表'}`,
    afterLabel: `📤 ${direction === 'to_wide' ? '宽表 (PIVOT)' : '长表 (UNPIVOT)'}` });
}

// ============================================================
// 两数之和 / 哈希表查找风格图解
// 布局：数组行（当前索引高亮）+ 补数计算 + HashMap 键值对表
// map: [{key, val}]   highlight: {mapKey}    currentIdx
// ============================================================
function drawTwoSumMap({ arr = [], map = [], highlight = null, currentIdx = -1, complement = null, action = '', width = 560, height = 180 } = {}) {
  const cellW = 48, cellH = 32;
  const arrStartX = 60, arrY = 12;
  let svgInner = ARROW_MARKER;

  // 数组行
  arr.forEach((val, i) => {
    const x = arrStartX + i * cellW;
    const isActive = i === currentIdx;
    svgInner += `<rect x="${x}" y="${arrY}" width="${cellW}" height="${cellH}" class="${isActive ? 'cell-highlight' : 'cell'}" rx="4"/>`;
    svgInner += `<text x="${x + cellW/2}" y="${arrY + cellH/2 + 4}" text-anchor="middle" class="node-val">${val}</text>`;
    svgInner += `<text x="${x + cellW/2}" y="${arrY - 4}" text-anchor="middle" class="idx-label">${i}</text>`;
    if (isActive) {
      svgInner += `<polygon points="${x + cellW/2 - 5},${arrY - 6} ${x + cellW/2 + 5},${arrY - 6} ${x + cellW/2},${arrY - 12}" fill="var(--color-pointer)"/><text x="${x + cellW/2}" y="${arrY - 17}" text-anchor="middle" class="ptr-label">i=${i}</text>`;
    }
  });

  // 补数行
  if (complement !== null && currentIdx >= 0) {
    const compY = arrY + cellH + 25;
    const cx = arrStartX + currentIdx * cellW + cellW / 2;
    const target = arr[currentIdx] + complement;
    svgInner += `<text x="${cx}" y="${compY}" text-anchor="middle" class="idx-label">complement = ${target} - ${arr[currentIdx]} = ${complement}</text>`;
  }

  // HashMap 表
  const mapX = 60, mapY = arrY + cellH + 45;
  const headerW = 100;
  svgInner += `<text x="${mapX}" y="${mapY - 6}" class="idx-label" font-weight="bold">HashMap { val → idx }</text>`;
  
  if (map.length === 0) {
    svgInner += `<text x="${mapX}" y="${mapY + 16}" class="idx-label" fill="var(--color-null)">{ } 空</text>`;
  } else {
    // 表头
    svgInner += `<rect x="${mapX}" y="${mapY}" width="${headerW}" height="22" fill="var(--color-tag-bg)" stroke="var(--color-border)"/><text x="${mapX + headerW/2}" y="${mapY + 15}" text-anchor="middle" class="node-val" font-size="10" font-weight="bold">Key (val)</text>`;
    svgInner += `<rect x="${mapX + headerW}" y="${mapY}" width="${headerW}" height="22" fill="var(--color-tag-bg)" stroke="var(--color-border)"/><text x="${mapX + headerW * 1.5}" y="${mapY + 15}" text-anchor="middle" class="node-val" font-size="10" font-weight="bold">Value (idx)</text>`;
    
    map.forEach((entry, mi) => {
      const ry = mapY + 22 + mi * 22;
      const isHit = highlight && entry.key === highlight;
      const isNew = entry.new;
      const rowFill = isHit ? 'var(--color-highlight)' : (isNew ? 'var(--color-done)' : 'none');
      const rowOpacity = (isHit || isNew) ? 0.2 : 1;
      svgInner += `<rect x="${mapX}" y="${ry}" width="${headerW}" height="22" fill="${rowFill}" opacity="${rowOpacity}" stroke="var(--color-border)"/>`;
      svgInner += `<text x="${mapX + headerW/2}" y="${ry + 15}" text-anchor="middle" class="node-val" font-size="11" fill="${isHit ? 'var(--color-highlight)' : ''}" font-weight="${isHit ? 'bold' : 'normal'}">${entry.key}</text>`;
      svgInner += `<rect x="${mapX + headerW}" y="${ry}" width="${headerW}" height="22" fill="${rowFill}" opacity="${rowOpacity}" stroke="var(--color-border)"/>`;
      svgInner += `<text x="${mapX + headerW * 1.5}" y="${ry + 15}" text-anchor="middle" class="node-val" font-size="11" font-weight="${isNew ? 'bold' : 'normal'}">${entry.val}</text>`;
      if (isNew) {
        svgInner += `<text x="${mapX + headerW * 2 + 6}" y="${ry + 15}" class="idx-label" fill="var(--color-done)" font-size="9">← 新存入</text>`;
      }
    });
  }

  // 动作行
  if (action) {
    const actY = mapY + (map.length + 1) * 22 + 20;
    svgInner += `<text x="${width / 2}" y="${actY}" text-anchor="middle" class="ptr-label">${action}</text>`;
  }

  const totalH = Math.max(height, mapY + (map.length + 1) * 22 + 40);
  return svgWrap(width, totalH, svgInner);
}

// ============================================================
// 表格自适应网页宽度：返回 .frame-card 内容可用宽度，供 draw* 的 width 使用
// 表格因此填满卡片容器，随窗口宽度变化
// ============================================================
function frameCardWidth(el) {
  const card = (typeof el === 'string' ? document.getElementById(el) : el).closest('.frame-card');
  if (!card) return 600;
  const padL = parseFloat(getComputedStyle(card).paddingLeft) || 0;
  const padR = parseFloat(getComputedStyle(card).paddingRight) || 0;
  return Math.max(320, Math.round(card.clientWidth - padL - padR - 2)); // -2 边框
}

/** 窗口 resize 防抖重绘：表格随网页宽度自适应 */
function autoFitResize(renderFn, delay = 150) {
  let t;
  window.addEventListener('resize', () => {
    clearTimeout(t);
    t = setTimeout(renderFn, delay);
  });
}

// ============================================================
// 导出为全局对象
// ============================================================
window.DrawUtils = {
  drawLinkedList,
  drawTree,
  drawGraph,
  drawDPTable,
  drawHashmap,
  drawTwoSumMap,
  drawStack,
  drawTwoPointers,
  drawBinarySearch,
  drawBacktrack,
  drawTable,
  diffTable,
  drawGroupBy,
  drawWindowFunc,
  drawJoin,
  drawSubquery,
  drawCTE,
  drawStringFunc,
  drawDateFunc,
  drawConditionFunc,
  drawSetOp,
  drawPivot,
  frameCardWidth,
  autoFitResize,
};

// ═════════════════════════════════════════════
//  共享双面板拖拽分割条
//  依赖: DOM 中有 #vSplitter 和 .left-panel
// ═════════════════════════════════════════════

var vs = document.getElementById("vSplitter");
var lp = document.querySelector(".left-panel");
var isDraggingV = false;

function setVSplit(px) {
  var bodyW = document.body.clientWidth;
  var maxW = bodyW - vs.offsetWidth - 360;
  px = Math.max(280, Math.min(maxW, px));
  lp.style.flexBasis = px + "px";
  lp.style.flexGrow = "0";
}

setTimeout(function() { setVSplit(document.body.clientWidth * 0.4); }, 100);

vs.addEventListener("mousedown", function(e) {
  isDraggingV = true; document.body.style.cursor = "col-resize";
  document.body.style.userSelect = "none"; e.preventDefault();
});

document.addEventListener("mousemove", function(e) { if (isDraggingV) setVSplit(e.clientX); });

document.addEventListener("mouseup", function() {
  if (isDraggingV) { isDraggingV = false; document.body.style.cursor = ""; document.body.style.userSelect = ""; }
});

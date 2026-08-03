// ═════════════════════════════════════════════
//  共享进度模块 (localStorage) — 纯函数，无自动执行
//  PROBLEM_TYPE / PROBLEM_ID 由父页面定义后调用 initProgress()
// ═════════════════════════════════════════════

var STORAGE_KEY = "algo-practice-progress";
var progressData = null;
try {
  progressData = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
} catch(e) { progressData = {}; }

function saveProgress() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(progressData)); }
  catch(e) { /* noop */ }
}

function markStatus(status) {
  progressData[PROBLEM_TYPE + "/" + PROBLEM_ID] = status;
  saveProgress();
  document.querySelectorAll(".progress-toggle button").forEach(function(b) {
    if (b.classList.contains(status)) {
      b.style.background = "var(--green)"; b.style.color = "#fff";
    } else {
      b.style.background = "transparent"; b.style.color = "";
    }
  });
}

// ⚠️ 调用方必须在 PROBLEM_TYPE / PROBLEM_ID 定义后调用:
//   initProgress();
function initProgress() {
  var saved = progressData[PROBLEM_TYPE + "/" + PROBLEM_ID];
  if (saved) markStatus(saved);
}

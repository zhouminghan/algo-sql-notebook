#!/usr/bin/env bash
# 清掉工作区里的本地垃圾（Python 缓存、系统元数据、临时文件）。
# 这些东西本来就被 .gitignore 忽略，只是让目录看起来干净些。
#
#   bash scripts/clean.sh            # 预览要删什么（dry-run）
#   bash scripts/clean.sh --force    # 真删
set -euo pipefail
cd "$(dirname "$0")/.."

FORCE=0
[ "${1:-}" = "--force" ] && FORCE=1

# 与 scripts/check_site.py 的 JUNK_KINDS 保持一致
PATTERNS=(-name '__pycache__' -o -name '*.py[co]' -o -name '.DS_Store' \
          -o -name '*.log' -o -name '*.tmp' -o -name '*.swp' -o -name '*~')

TARGETS=$(find . -path ./.git -prune -o \( "${PATTERNS[@]}" \) -print 2>/dev/null || true)
COUNT=$(printf '%s\n' "$TARGETS" | grep -c . || true)

if [ "$COUNT" -eq 0 ]; then
  echo "工作区很干净：没有本地垃圾"
  exit 0
fi

printf '%s\n' "$TARGETS" | sed 's/^/  /'
if [ "$FORCE" -eq 1 ]; then
  printf '%s\n' "$TARGETS" | while IFS= read -r p; do rm -rf -- "$p"; done
  echo "已删除 $COUNT 项"
else
  echo
  echo "以上 $COUNT 项将被删除（当前是预览）。加 --force 真正执行：bash scripts/clean.sh --force"
fi

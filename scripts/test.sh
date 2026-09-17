#!/usr/bin/env bash
# 一条命令跑完所有门禁：静态自检 + 运行时冒烟测试
#
#   bash scripts/test.sh            # 全量（106 页）
#   bash scripts/test.sh --fast     # 冒烟只抽 8 页，改小东西时用
#
# 任一环节失败即退出码非 0。
set -euo pipefail
cd "$(dirname "$0")/.."

# 跑门禁本身不产生 __pycache__（否则工作区又会多出本地垃圾）
export PYTHONDONTWRITEBYTECODE=1

echo "══ 1/2 静态自检（结构 / 令牌 / head / 标题层级 / 分类词表 / 404） ══"
python3 scripts/check_site.py

echo
echo "══ 2/2 运行时冒烟（Playwright：全部页面 + 交互 + 断点 + 打印） ══"
if command -v node >/dev/null 2>&1; then
  node scripts/smoke.mjs "$@"
else
  echo "跳过运行时冒烟：未找到 node（静态自检已通过）"
fi

echo
echo "✅ 全部门禁通过"

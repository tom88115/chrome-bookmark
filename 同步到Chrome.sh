#!/bin/bash
# 将 Atlas 的新书签同步到 Chrome
# 只添加 Chrome 没有的书签，不改变原有顺序

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/sync_bookmarks_v2.py"

echo ""
echo "================================================"
echo "  🔖 同步 Atlas 书签到 Chrome"
echo "  (只添加新书签，保持原有顺序)"
echo "================================================"
echo ""

python3 "$PYTHON_SCRIPT"

echo ""
echo "提示：请完全退出 Chrome (Cmd+Q) 后重新打开查看新书签"
echo ""


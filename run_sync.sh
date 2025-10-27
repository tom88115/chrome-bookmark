#!/bin/bash
# 手动运行书签同步

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/sync_bookmarks.py"

echo ""
echo "================================================"
echo "  🔖 正在同步书签..."
echo "================================================"
echo ""

# 确保脚本可执行
chmod +x "$PYTHON_SCRIPT"

# 运行同步脚本
python3 "$PYTHON_SCRIPT"

echo ""
echo "按任意键退出..."
read -n 1 -s


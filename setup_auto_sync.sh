#!/bin/bash
# 设置 macOS 定时任务 - 自动同步书签

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/sync_bookmarks.py"
PLIST_FILE="${HOME}/Library/LaunchAgents/com.bookmarksync.plist"

echo "================================================"
echo "  设置书签自动同步 (每小时执行一次)"
echo "================================================"
echo ""

# 检查 Python 脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ 错误: 找不到同步脚本"
    echo "   路径: $PYTHON_SCRIPT"
    exit 1
fi

# 确保脚本可执行
chmod +x "$PYTHON_SCRIPT"

# 创建 LaunchAgent plist 文件
echo "正在创建定时任务配置..."

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bookmarksync</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${PYTHON_SCRIPT}</string>
    </array>
    
    <key>StartInterval</key>
    <integer>3600</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>${HOME}/bookmark-sync-backups/launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>${HOME}/bookmark-sync-backups/launchd.error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

echo "✓ 配置文件已创建: $PLIST_FILE"
echo ""

# 加载 LaunchAgent
echo "正在启动定时任务..."
launchctl unload "$PLIST_FILE" 2>/dev/null
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ 定时任务设置成功！"
    echo "================================================"
    echo ""
    echo "📋 任务详情:"
    echo "   - 执行频率: 每小时"
    echo "   - 脚本位置: $PYTHON_SCRIPT"
    echo "   - 日志位置: ${HOME}/bookmark-sync-backups/"
    echo ""
    echo "🔧 管理命令:"
    echo "   停止任务: launchctl unload $PLIST_FILE"
    echo "   启动任务: launchctl load $PLIST_FILE"
    echo "   查看状态: launchctl list | grep bookmarksync"
    echo "   立即执行: python3 $PYTHON_SCRIPT"
    echo ""
else
    echo ""
    echo "❌ 启动定时任务失败"
    echo "   请检查权限或手动执行同步脚本"
    exit 1
fi


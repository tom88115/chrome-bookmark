#!/bin/bash
# 创建 macOS 应用程序 - 书签同步工具

APP_NAME="书签同步工具"
APP_DIR="$HOME/Applications/${APP_NAME}.app"
SCRIPT_PATH="/Users/tomnice/cursor/日常提问/bookmark-sync/sync_bookmarks_v2.py"

echo "正在创建 macOS 应用程序..."
echo "应用名称: ${APP_NAME}"
echo ""

# 创建应用程序目录结构
mkdir -p "${APP_DIR}/Contents/MacOS"
mkdir -p "${APP_DIR}/Contents/Resources"

# 创建 Info.plist
cat > "${APP_DIR}/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.bookmarksync.app</string>
    <key>CFBundleName</key>
    <string>书签同步工具</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# 创建启动脚本
cat > "${APP_DIR}/Contents/MacOS/launcher" << EOF
#!/bin/bash

# 显示终端窗口执行同步
osascript <<'APPLESCRIPT'
tell application "Terminal"
    activate
    do script "clear && echo ''; echo '================================================'; echo '  🔖 书签同步工具 V2'; echo '  Atlas → Chrome'; echo '================================================'; echo ''; python3 '${SCRIPT_PATH}'; echo ''; echo '同步完成！请重启 Chrome 浏览器查看新书签'; echo ''; echo '按任意键关闭...'; read -n 1 -s; exit"
end tell
APPLESCRIPT
EOF

# 设置执行权限
chmod +x "${APP_DIR}/Contents/MacOS/launcher"

# 创建图标（使用 emoji 图标）
# 生成一个简单的图标
cat > "/tmp/bookmark_icon.svg" << 'EOF'
<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
  <rect width="512" height="512" rx="100" fill="#4A90E2"/>
  <text x="256" y="380" font-size="300" text-anchor="middle" fill="white">🔖</text>
</svg>
EOF

# 尝试使用 sips 转换图标（如果失败也没关系）
if command -v rsvg-convert &> /dev/null && command -v sips &> /dev/null; then
    rsvg-convert -w 512 -h 512 /tmp/bookmark_icon.svg > /tmp/bookmark_icon.png
    sips -s format icns /tmp/bookmark_icon.png --out "${APP_DIR}/Contents/Resources/AppIcon.icns" 2>/dev/null
fi

echo "✅ 应用程序已创建！"
echo ""
echo "📍 位置: ${APP_DIR}"
echo ""
echo "📋 使用方法："
echo "   1. 双击运行: 打开 Finder，找到'应用程序'文件夹，双击'${APP_NAME}'"
echo "   2. Spotlight: 按 Cmd+Space，输入'书签同步'，回车运行"
echo "   3. 添加到 Dock: 将应用拖到 Dock 栏即可"
echo ""
echo "🔍 正在打开应用程序文件夹..."
open "$HOME/Applications"
echo ""
echo "✨ 现在你可以在 Spotlight 搜索'书签同步'来运行了！"
EOF

chmod +x create_app.sh


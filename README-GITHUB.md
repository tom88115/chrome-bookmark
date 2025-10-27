# 🔖 Chrome & Atlas 书签同步工具

一个智能的浏览器书签同步工具，支持在 Google Chrome 和 OpenAI Atlas 浏览器之间同步书签。采用保守策略，只添加缺失的书签，保持原有顺序不变。

![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## ✨ 功能特性

- ✅ **智能同步** - 自动检测 Atlas 新书签并同步到 Chrome
- ✅ **保持顺序** - 不改变原有书签的顺序
- ✅ **避免重复** - 相同书签不会重复添加
- ✅ **自动备份** - 每次同步前自动备份两个浏览器的书签
- ✅ **文件夹支持** - 保持书签文件夹结构
- ✅ **多种启动方式** - Spotlight、双击、快捷键、终端命令
- ✅ **详细日志** - 记录每次同步的详细信息
- ✅ **安全可靠** - 不修改 Atlas 书签，单向同步更安全

---

## 🎯 使用场景

这个工具适合：

- 你主要在 Atlas 浏览器添加和管理书签
- 偶尔需要在 Chrome 访问相同的书签
- 不想书签顺序被打乱
- 需要在两个浏览器之间保持书签同步

---

## 📦 安装

### 前置要求

- macOS 10.13 或更高版本
- Python 3.x（macOS 自带）
- Google Chrome 浏览器
- OpenAI Atlas 浏览器

### 克隆仓库

```bash
git clone https://github.com/你的用户名/chrome-bookmark.git
cd chrome-bookmark
```

### 设置权限

```bash
chmod +x *.sh *.py
```

---

## 🚀 快速开始

### 方法 1：创建 macOS 应用（推荐）

运行创建脚本，生成可以在 Spotlight 搜索的应用：

```bash
./create_app.sh
```

创建成功后：
1. 按 `Cmd + Space` 打开 Spotlight
2. 输入 `书签同步`
3. 按回车运行

### 方法 2：使用便捷脚本

```bash
./同步到Chrome.sh
```

### 方法 3：直接运行 Python 脚本

```bash
python3 sync_bookmarks_v2.py
```

---

## 📱 使用方式

### 🔍 Spotlight 搜索（最推荐）

1. 先运行 `./create_app.sh` 创建应用
2. 按 `Cmd + Space`
3. 输入 `书签同步` 或 `bookmark`
4. 按回车

### 🖱️ 双击运行

创建应用后，可以在以下位置找到：
- `~/Applications/书签同步工具.app`
- `~/Desktop/书签同步工具.app`（桌面快捷方式）

### ⌨️ 终端运行

```bash
# 使用快捷脚本
./同步到Chrome.sh

# 或直接运行 Python
python3 sync_bookmarks_v2.py

# 创建别名（可选）
echo 'alias sync-bookmark="python3 ~/path/to/sync_bookmarks_v2.py"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🎬 工作原理

```
┌─────────────┐         ┌─────────────┐
│   Atlas     │         │   Chrome    │
│  (源书签)   │         │  (目标)     │
└──────┬──────┘         └──────┬──────┘
       │                       │
       │  ① 读取书签           │
       ├───────────────────────┤
       │                       │
       │  ② 查找 Chrome        │
       │     没有的书签        │
       │                       │
       │  ③ 添加新书签         │
       │     (保持原有顺序)    │
       │                       │
       ├───────────────────────┤
       │                       │
   不修改 ✓                 已更新 ✓
```

### 同步逻辑

1. **扫描** - 读取 Atlas 和 Chrome 的书签文件
2. **比较** - 找出 Atlas 有但 Chrome 没有的书签
3. **添加** - 将新书签添加到 Chrome（保持文件夹结构）
4. **保护** - 不修改 Atlas，不改变 Chrome 原有书签顺序

---

## 📂 项目结构

```
chrome-bookmark/
├── sync_bookmarks_v2.py      # V2 核心同步脚本
├── 同步到Chrome.sh             # 快速运行脚本
├── create_app.sh              # 创建 macOS 应用
├── setup_auto_sync.sh         # 设置自动同步（定时任务）
│
├── README-GITHUB.md           # 项目说明（本文件）
├── 使用说明-V2.md              # 详细使用文档
├── 快速开始.md                 # 新手指南
├── 快速启动指南.md             # 启动方式说明
├── 故障排查.md                 # 问题解决
│
└── sync_bookmarks.py          # V1 旧版本（不推荐使用）
```

---

## 🛡️ 安全保障

### 自动备份

每次同步前自动备份：
```
~/bookmark-sync-backups/
├── chrome_bookmarks_时间戳.json
├── atlas_bookmarks_时间戳.json
└── sync_v2.log
```

### 恢复备份

如果出现问题，可以从备份恢复：

```bash
# 查看备份
ls -lt ~/bookmark-sync-backups/

# 恢复 Chrome 书签
cp ~/bookmark-sync-backups/chrome_bookmarks_时间戳.json \
   ~/Library/Application\ Support/Google/Chrome/Default/Bookmarks

# 重启 Chrome
```

---

## ⚙️ 配置说明

### 修改 Atlas 书签路径

如果脚本找不到 Atlas 书签，编辑 `sync_bookmarks_v2.py`：

```python
self.atlas_path = Path.home() / "你的实际路径/Bookmarks"
```

### 设置自动同步

运行设置脚本，每小时自动同步：

```bash
./setup_auto_sync.sh
```

管理定时任务：

```bash
# 停止
launchctl unload ~/Library/LaunchAgents/com.bookmarksync.plist

# 启动
launchctl load ~/Library/LaunchAgents/com.bookmarksync.plist

# 查看状态
launchctl list | grep bookmarksync
```

---

## 📊 同步示例

### 运行输出

```
============================================================
  🔖 书签同步工具 V2
  Atlas → Chrome
============================================================

✓ Chrome: Bookmarks
✓ Atlas: Bookmarks

📦 创建备份...
✓ 已备份 chrome: chrome_bookmarks_20251027_173855.json
✓ 已备份 atlas: atlas_bookmarks_20251027_173855.json

📖 加载书签...

🔍 发现 3 个新书签需要添加到 Chrome：
  ✓ [1] GitHub - Feishu-MCP
      位置: 书签栏/AI
  ✓ [2] 16软著 - 飞书云文档
      位置: 书签栏
  ✓ [3] gateway.zeabur.cn
      位置: 书签栏

💾 保存更新...
✓ 已保存书签: Bookmarks

============================================================
✅ 同步完成！已添加 3 个新书签到 Chrome
============================================================
```

---

## ❓ 常见问题

### Q1: 同步后 Chrome 没有显示新书签？

**A:** 必须完全退出 Chrome（`Cmd + Q`），然后重新打开。浏览器会缓存书签文件。

---

### Q2: Atlas 的书签会被修改吗？

**A:** 不会。V2 版本完全不修改 Atlas 的书签文件，只读取。

---

### Q3: 会不会删除我的书签？

**A:** 不会。脚本只会**添加**新书签，不会删除或修改现有书签。

---

### Q4: 如果我在 Chrome 也添加了书签怎么办？

**A:** Chrome 的新书签会保留，不会被删除。但不会自动同步到 Atlas（单向同步）。

---

### Q5: 支持 Windows 或 Linux 吗？

**A:** 目前只支持 macOS。因为：
- 使用了 macOS 特定的路径
- Spotlight 集成是 macOS 专属
- Atlas 浏览器路径是 macOS 格式

如需支持其他平台，需要修改路径配置。

---

## 🔧 故障排查

### 找不到 Atlas 书签文件

**解决方法：**

1. 手动查找：
   ```bash
   find ~/Library/Application\ Support -name "Bookmarks" 2>/dev/null
   ```

2. 编辑脚本添加实际路径（见"配置说明"）

### macOS 安全警告

**第一次运行可能提示：**
```
"书签同步工具"无法打开，因为无法验证开发者
```

**解决：**
```bash
xattr -d com.apple.quarantine ~/Applications/书签同步工具.app
```

或右键点击应用 → 选择"打开" → 在弹窗中点击"打开"

---

## 📖 文档

- [使用说明-V2.md](使用说明-V2.md) - 完整使用手册
- [快速开始.md](快速开始.md) - 新手快速入门
- [快速启动指南.md](快速启动指南.md) - 各种启动方式详解
- [故障排查.md](故障排查.md) - 问题解决大全

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果你有好的想法或发现了 Bug，请：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📋 更新日志

### v2.0.0 (2025-10-27)

- ✨ V2 版本重新设计
- ✅ 采用保守单向同步策略
- ✅ 保持书签原有顺序
- ✅ 不修改 Atlas 书签
- ✅ 支持 macOS 应用形式
- ✅ 集成 Spotlight 搜索
- ✅ 自动备份功能
- ✅ 详细的同步日志

### v1.0.0 (2025-10-27)

- 初始版本
- 双向合并同步（已弃用）

---

## 📄 许可证

MIT License

Copyright (c) 2025

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 Star ⭐！

---

## 📞 联系方式

- 问题反馈：[GitHub Issues](https://github.com/你的用户名/chrome-bookmark/issues)
- 功能建议：[GitHub Discussions](https://github.com/你的用户名/chrome-bookmark/discussions)

---

## 🙏 致谢

感谢所有使用和贡献这个项目的人！

---

**祝使用愉快！** 🎉

如果觉得有用，别忘了给个 Star ⭐


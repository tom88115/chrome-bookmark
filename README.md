# 🔖 Chrome & Atlas 书签同步工具

一个智能的浏览器书签同步工具，支持在 Google Chrome 和 OpenAI Atlas 浏览器之间同步书签。

![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## ✨ 功能特性

- ✅ **智能同步** - 自动检测 Atlas 新书签并同步到 Chrome
- ✅ **保持顺序** - 不改变原有书签的顺序  
- ✅ **避免重复** - 相同书签不会重复添加
- ✅ **自动备份** - 每次同步前自动备份
- ✅ **多种启动方式** - Spotlight、双击、快捷键、终端
- ✅ **安全可靠** - 单向同步，不修改 Atlas

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/你的用户名/chrome-bookmark.git
cd chrome-bookmark
chmod +x *.sh *.py
```

### 创建 macOS 应用

```bash
./create_app.sh
```

### 使用

**Spotlight 搜索（推荐）：**
1. 按 `Cmd + Space`
2. 输入 `书签同步`
3. 按回车

**或直接运行：**
```bash
./同步到Chrome.sh
```

## 📖 文档

- [完整文档](README-GITHUB.md) - 详细的功能介绍和使用指南
- [使用说明](使用说明-V2.md) - V2 版本使用手册
- [快速启动](快速启动指南.md) - 各种启动方式详解
- [故障排查](故障排查.md) - 常见问题解决

## 🎯 使用场景

适合主要在 Atlas 浏览器添加书签，偶尔需要在 Chrome 访问相同书签的用户。

## ⚠️ 注意事项

- 同步后需要重启 Chrome 浏览器
- V2 版本采用单向同步（Atlas → Chrome）
- 不会修改 Atlas 的书签

## 📄 许可证

MIT License

---

**祝使用愉快！如果觉得有用，请给个 Star ⭐**

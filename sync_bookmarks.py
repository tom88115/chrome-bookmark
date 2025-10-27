#!/usr/bin/env python3
"""
浏览器书签同步工具 - Chrome & Atlas
支持双向同步，以最新修改时间为准
"""

import json
import shutil
import os
from datetime import datetime
from pathlib import Path
import hashlib
import logging

class BookmarkSyncer:
    def __init__(self):
        # Chrome 书签路径
        self.chrome_path = Path.home() / "Library/Application Support/Google/Chrome/Default/Bookmarks"
        
        # Atlas 书签路径（需要根据实际情况调整）
        # 常见可能的路径
        atlas_paths = [
            # 实际找到的 Atlas 路径
            Path.home() / "Library/Application Support/com.openai.atlas/browser-data/host/user-Am0Q4EbYlB5U8O6IwUFaUZM7__bb9ad6a0-2ac3-437c-a7dd-fd1f6bd9ff0b/Bookmarks",
            Path.home() / "Library/Application Support/Atlas/Default/Bookmarks",
            Path.home() / "Library/Application Support/com.openai.atlas/Default/Bookmarks",
            Path.home() / "Library/Application Support/OpenAI/Atlas/Bookmarks",
        ]
        
        self.atlas_path = None
        for path in atlas_paths:
            if path.exists():
                self.atlas_path = path
                break
        
        # 备份目录
        self.backup_dir = Path.home() / "bookmark-sync-backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # 日志配置
        log_file = self.backup_dir / "sync.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def find_atlas_bookmarks(self):
        """查找 Atlas 书签文件"""
        if self.atlas_path and self.atlas_path.exists():
            return self.atlas_path
        
        # 搜索可能的位置
        app_support = Path.home() / "Library/Application Support"
        if app_support.exists():
            for item in app_support.iterdir():
                if 'atlas' in item.name.lower():
                    possible_bookmark = item / "Default/Bookmarks"
                    if possible_bookmark.exists():
                        self.logger.info(f"找到 Atlas 书签: {possible_bookmark}")
                        return possible_bookmark
                    # 尝试其他可能的路径
                    possible_bookmark = item / "Bookmarks"
                    if possible_bookmark.exists():
                        self.logger.info(f"找到 Atlas 书签: {possible_bookmark}")
                        return possible_bookmark
        
        return None
    
    def backup_file(self, file_path, browser_name):
        """备份书签文件"""
        if not file_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{browser_name}_bookmarks_{timestamp}.json"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.logger.info(f"已备份 {browser_name}: {backup_path}")
        return backup_path
    
    def load_bookmarks(self, file_path):
        """加载书签文件"""
        if not file_path.exists():
            self.logger.warning(f"书签文件不存在: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            self.logger.error(f"读取书签失败 {file_path}: {e}")
            return None
    
    def save_bookmarks(self, file_path, data):
        """保存书签文件"""
        try:
            # 确保父目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 先写入临时文件
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=3)
            
            # 替换原文件
            shutil.move(temp_path, file_path)
            self.logger.info(f"已保存书签: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"保存书签失败 {file_path}: {e}")
            return False
    
    def get_file_hash(self, file_path):
        """计算文件MD5哈希"""
        if not file_path.exists():
            return None
        
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_modification_time(self, file_path):
        """获取文件修改时间"""
        if not file_path.exists():
            return 0
        return file_path.stat().st_mtime
    
    def merge_bookmark_folders(self, target, source, path="root"):
        """递归合并书签文件夹"""
        if not isinstance(target, dict) or not isinstance(source, dict):
            return target
        
        # 处理子节点
        if 'children' in target and 'children' in source:
            target_children = {self.get_bookmark_key(item): item for item in target['children']}
            source_children = {self.get_bookmark_key(item): item for item in source['children']}
            
            # 合并子节点
            merged_keys = set(target_children.keys()) | set(source_children.keys())
            merged_children = []
            
            for key in sorted(merged_keys):
                if key in target_children and key in source_children:
                    # 两边都有，比较时间戳
                    target_item = target_children[key]
                    source_item = source_children[key]
                    
                    target_time = float(target_item.get('date_modified', 0) or target_item.get('date_added', 0))
                    source_time = float(source_item.get('date_modified', 0) or source_item.get('date_added', 0))
                    
                    if source_time > target_time:
                        # 源更新，使用源
                        merged_children.append(source_item)
                        self.logger.debug(f"使用较新的书签: {source_item.get('name', 'unknown')} (来自源)")
                    else:
                        # 目标更新或相同，使用目标
                        merged_children.append(target_item)
                    
                    # 如果是文件夹，递归合并
                    if target_item.get('type') == 'folder' and source_item.get('type') == 'folder':
                        merged_item = merged_children[-1]
                        self.merge_bookmark_folders(merged_item, source_item, f"{path}/{key}")
                
                elif key in source_children:
                    # 只在源中有，添加
                    merged_children.append(source_children[key])
                    self.logger.info(f"添加新书签: {source_children[key].get('name', 'unknown')}")
                else:
                    # 只在目标中有，保留
                    merged_children.append(target_children[key])
            
            target['children'] = merged_children
        
        # 更新其他属性
        if 'date_modified' in source:
            target['date_modified'] = source['date_modified']
        
        return target
    
    def get_bookmark_key(self, bookmark):
        """生成书签的唯一键"""
        if bookmark.get('type') == 'url':
            # URL类型：使用URL作为键
            return f"url:{bookmark.get('url', '')}"
        elif bookmark.get('type') == 'folder':
            # 文件夹类型：使用名称作为键
            return f"folder:{bookmark.get('name', '')}"
        else:
            # 其他类型：使用名称
            return f"other:{bookmark.get('name', '')}"
    
    def sync(self):
        """执行同步"""
        self.logger.info("=" * 60)
        self.logger.info("开始书签同步")
        self.logger.info("=" * 60)
        
        # 1. 查找 Atlas 书签
        atlas_path = self.find_atlas_bookmarks()
        if not atlas_path:
            self.logger.error("❌ 未找到 Atlas 书签文件")
            self.logger.info("\n请手动设置 Atlas 书签路径，可能的位置：")
            app_support = Path.home() / "Library/Application Support"
            if app_support.exists():
                for item in app_support.iterdir():
                    if 'atlas' in item.name.lower() or 'openai' in item.name.lower():
                        self.logger.info(f"  - {item}")
            return False
        
        self.atlas_path = atlas_path
        
        # 2. 检查 Chrome 书签
        if not self.chrome_path.exists():
            self.logger.error(f"❌ Chrome 书签文件不存在: {self.chrome_path}")
            return False
        
        self.logger.info(f"✓ Chrome 书签: {self.chrome_path}")
        self.logger.info(f"✓ Atlas 书签: {self.atlas_path}")
        
        # 3. 检查文件是否相同
        chrome_hash = self.get_file_hash(self.chrome_path)
        atlas_hash = self.get_file_hash(self.atlas_path)
        
        if chrome_hash == atlas_hash:
            self.logger.info("✓ 书签已经同步，无需更新")
            return True
        
        # 4. 备份
        self.logger.info("\n正在备份...")
        self.backup_file(self.chrome_path, "chrome")
        self.backup_file(self.atlas_path, "atlas")
        
        # 5. 加载书签
        self.logger.info("\n正在加载书签...")
        chrome_data = self.load_bookmarks(self.chrome_path)
        atlas_data = self.load_bookmarks(self.atlas_path)
        
        if not chrome_data or not atlas_data:
            self.logger.error("❌ 加载书签失败")
            return False
        
        # 6. 比较修改时间
        chrome_time = self.get_modification_time(self.chrome_path)
        atlas_time = self.get_modification_time(self.atlas_path)
        
        chrome_time_str = datetime.fromtimestamp(chrome_time).strftime("%Y-%m-%d %H:%M:%S")
        atlas_time_str = datetime.fromtimestamp(atlas_time).strftime("%Y-%m-%d %H:%M:%S")
        
        self.logger.info(f"\nChrome 最后修改: {chrome_time_str}")
        self.logger.info(f"Atlas 最后修改: {atlas_time_str}")
        
        # 7. 智能合并
        self.logger.info("\n正在合并书签...")
        
        # 深拷贝数据
        import copy
        merged_chrome = copy.deepcopy(chrome_data)
        merged_atlas = copy.deepcopy(atlas_data)
        
        # 合并根节点
        if 'roots' in chrome_data and 'roots' in atlas_data:
            for root_key in chrome_data['roots']:
                if root_key in atlas_data['roots']:
                    # 双向合并
                    self.merge_bookmark_folders(
                        merged_chrome['roots'][root_key],
                        atlas_data['roots'][root_key],
                        root_key
                    )
                    self.merge_bookmark_folders(
                        merged_atlas['roots'][root_key],
                        chrome_data['roots'][root_key],
                        root_key
                    )
        
        # 8. 保存合并后的书签
        self.logger.info("\n正在保存同步结果...")
        
        chrome_saved = self.save_bookmarks(self.chrome_path, merged_chrome)
        atlas_saved = self.save_bookmarks(self.atlas_path, merged_atlas)
        
        if chrome_saved and atlas_saved:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("✅ 书签同步完成！")
            self.logger.info("=" * 60)
            self.logger.info(f"备份位置: {self.backup_dir}")
            return True
        else:
            self.logger.error("\n❌ 书签保存失败")
            return False

def main():
    """主函数"""
    syncer = BookmarkSyncer()
    
    print("\n" + "=" * 60)
    print("  🔖 浏览器书签同步工具")
    print("  Chrome ⇄ Atlas")
    print("=" * 60 + "\n")
    
    success = syncer.sync()
    
    if not success:
        print("\n❌ 同步失败，请查看日志了解详情")
        print(f"日志位置: {syncer.backup_dir / 'sync.log'}")
        exit(1)
    else:
        print("\n✅ 同步成功！请重启浏览器查看最新书签")
        exit(0)

if __name__ == "__main__":
    main()


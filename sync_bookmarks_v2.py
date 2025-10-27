#!/usr/bin/env python3
"""
浏览器书签同步工具 V2 - Chrome & Atlas
采用保守策略：只添加缺失的书签，不改变原有顺序
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
import logging

class BookmarkSyncerV2:
    def __init__(self):
        # Chrome 书签路径
        self.chrome_path = Path.home() / "Library/Application Support/Google/Chrome/Default/Bookmarks"
        
        # Atlas 书签路径
        self.atlas_path = Path.home() / "Library/Application Support/com.openai.atlas/browser-data/host/user-Am0Q4EbYlB5U8O6IwUFaUZM7__bb9ad6a0-2ac3-437c-a7dd-fd1f6bd9ff0b/Bookmarks"
        
        # 备份目录
        self.backup_dir = Path.home() / "bookmark-sync-backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # 日志配置
        log_file = self.backup_dir / "sync_v2.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def backup_file(self, file_path, browser_name):
        """备份书签文件"""
        if not file_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{browser_name}_bookmarks_{timestamp}.json"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        self.logger.info(f"✓ 已备份 {browser_name}: {backup_path}")
        return backup_path
    
    def load_bookmarks(self, file_path):
        """加载书签文件"""
        if not file_path.exists():
            self.logger.error(f"❌ 书签文件不存在: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            self.logger.error(f"❌ 读取书签失败 {file_path}: {e}")
            return None
    
    def save_bookmarks(self, file_path, data):
        """保存书签文件"""
        try:
            # 先写入临时文件
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=3)
            
            # 替换原文件
            shutil.move(temp_path, file_path)
            self.logger.info(f"✓ 已保存书签: {file_path.name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ 保存书签失败: {e}")
            return False
    
    def get_all_bookmark_urls(self, node, url_set=None):
        """递归获取所有书签 URL"""
        if url_set is None:
            url_set = set()
        
        if isinstance(node, dict):
            if node.get('type') == 'url' and node.get('url'):
                url_set.add(node['url'])
            
            if 'children' in node:
                for child in node['children']:
                    self.get_all_bookmark_urls(child, url_set)
        
        return url_set
    
    def find_folder_by_path(self, root, path_parts):
        """根据路径查找文件夹"""
        if not path_parts:
            return root
        
        if 'children' not in root:
            return None
        
        folder_name = path_parts[0]
        for child in root['children']:
            if child.get('type') == 'folder' and child.get('name') == folder_name:
                if len(path_parts) == 1:
                    return child
                else:
                    return self.find_folder_by_path(child, path_parts[1:])
        
        return None
    
    def create_folder_path(self, root, path_parts):
        """创建文件夹路径（如果不存在）"""
        if not path_parts:
            return root
        
        if 'children' not in root:
            root['children'] = []
        
        folder_name = path_parts[0]
        
        # 查找是否已存在
        target_folder = None
        for child in root['children']:
            if child.get('type') == 'folder' and child.get('name') == folder_name:
                target_folder = child
                break
        
        # 如果不存在，创建新文件夹
        if not target_folder:
            now_timestamp = str(int(datetime.now().timestamp() * 1000000))
            target_folder = {
                'children': [],
                'date_added': now_timestamp,
                'date_last_used': '0',
                'date_modified': now_timestamp,
                'id': str(len(root['children']) + 1),
                'name': folder_name,
                'type': 'folder'
            }
            root['children'].append(target_folder)
            self.logger.info(f"  创建文件夹: {folder_name}")
        
        if len(path_parts) == 1:
            return target_folder
        else:
            return self.create_folder_path(target_folder, path_parts[1:])
    
    def collect_bookmarks_with_path(self, node, path="", bookmarks=None):
        """收集所有书签及其路径"""
        if bookmarks is None:
            bookmarks = []
        
        if isinstance(node, dict):
            if node.get('type') == 'url':
                bookmarks.append({
                    'data': node,
                    'path': path
                })
            
            if 'children' in node:
                current_path = f"{path}/{node.get('name', '')}" if path else node.get('name', '')
                for child in node['children']:
                    self.collect_bookmarks_with_path(child, current_path, bookmarks)
        
        return bookmarks
    
    def sync_atlas_to_chrome(self):
        """单向同步：从 Atlas 添加新书签到 Chrome"""
        self.logger.info("=" * 70)
        self.logger.info("开始书签同步：Atlas → Chrome")
        self.logger.info("=" * 70)
        
        # 检查文件
        if not self.chrome_path.exists():
            self.logger.error(f"❌ Chrome 书签不存在: {self.chrome_path}")
            return False
        
        if not self.atlas_path.exists():
            self.logger.error(f"❌ Atlas 书签不存在: {self.atlas_path}")
            return False
        
        self.logger.info(f"✓ Chrome: {self.chrome_path.name}")
        self.logger.info(f"✓ Atlas: {self.atlas_path.name}")
        
        # 备份
        self.logger.info("\n📦 创建备份...")
        chrome_backup = self.backup_file(self.chrome_path, "chrome")
        atlas_backup = self.backup_file(self.atlas_path, "atlas")
        
        if not chrome_backup or not atlas_backup:
            self.logger.error("❌ 备份失败")
            return False
        
        # 加载书签
        self.logger.info("\n📖 加载书签...")
        chrome_data = self.load_bookmarks(self.chrome_path)
        atlas_data = self.load_bookmarks(self.atlas_path)
        
        if not chrome_data or not atlas_data:
            return False
        
        # 获取所有书签 URL
        chrome_urls = set()
        atlas_bookmarks = []
        
        if 'roots' in chrome_data:
            for root_key in chrome_data['roots']:
                self.get_all_bookmark_urls(chrome_data['roots'][root_key], chrome_urls)
        
        if 'roots' in atlas_data:
            for root_key in atlas_data['roots']:
                bookmarks = self.collect_bookmarks_with_path(atlas_data['roots'][root_key])
                atlas_bookmarks.extend(bookmarks)
        
        # 找出 Atlas 独有的书签
        new_bookmarks = []
        for item in atlas_bookmarks:
            url = item['data'].get('url')
            if url and url not in chrome_urls:
                new_bookmarks.append(item)
        
        if not new_bookmarks:
            self.logger.info("\n✓ 书签已同步，没有需要添加的新书签")
            return True
        
        self.logger.info(f"\n🔍 发现 {len(new_bookmarks)} 个新书签需要添加到 Chrome：")
        
        # 添加新书签到 Chrome
        added_count = 0
        for item in new_bookmarks:
            bookmark = item['data']
            path = item['path']
            
            # 解析路径
            path_parts = [p for p in path.split('/') if p]
            
            # 查找或创建目标文件夹
            if path_parts:
                # 找到对应的根节点
                root_name = path_parts[0]
                target_root = None
                
                # 映射 Atlas 根节点到 Chrome 根节点
                root_mapping = {
                    '书签栏': 'bookmark_bar',
                    'Bookmarks bar': 'bookmark_bar',
                    '其他书签': 'other',
                    'Other bookmarks': 'other',
                }
                
                chrome_root_key = root_mapping.get(root_name, 'bookmark_bar')
                
                if chrome_root_key in chrome_data['roots']:
                    target_root = chrome_data['roots'][chrome_root_key]
                    
                    # 创建子文件夹路径（如果有）
                    if len(path_parts) > 1:
                        target_folder = self.create_folder_path(target_root, path_parts[1:])
                    else:
                        target_folder = target_root
                    
                    # 添加书签
                    if 'children' not in target_folder:
                        target_folder['children'] = []
                    
                    # 创建新书签（复制数据）
                    new_bookmark = {
                        'date_added': bookmark.get('date_added', str(int(datetime.now().timestamp() * 1000000))),
                        'date_last_used': '0',
                        'id': str(len(target_folder['children']) + 1),
                        'name': bookmark['name'],
                        'type': 'url',
                        'url': bookmark['url']
                    }
                    
                    target_folder['children'].append(new_bookmark)
                    added_count += 1
                    
                    # 显示添加的书签
                    folder_path = '/'.join(path_parts[1:]) if len(path_parts) > 1 else '(根目录)'
                    self.logger.info(f"  ✓ [{added_count}] {bookmark['name']}")
                    self.logger.info(f"      位置: {root_name}/{folder_path}")
        
        # 保存 Chrome 书签
        self.logger.info(f"\n💾 保存更新...")
        if self.save_bookmarks(self.chrome_path, chrome_data):
            self.logger.info("\n" + "=" * 70)
            self.logger.info(f"✅ 同步完成！已添加 {added_count} 个新书签到 Chrome")
            self.logger.info("=" * 70)
            self.logger.info(f"📁 备份位置: {self.backup_dir}")
            self.logger.info("\n⚠️  请完全退出并重启 Chrome 浏览器查看新书签")
            return True
        else:
            self.logger.error("\n❌ 保存失败")
            return False

def main():
    print("\n" + "=" * 70)
    print("  🔖 书签同步工具 V2")
    print("  策略：只添加缺失的书签，保持原有顺序")
    print("  方向：Atlas → Chrome")
    print("=" * 70 + "\n")
    
    syncer = BookmarkSyncerV2()
    success = syncer.sync_atlas_to_chrome()
    
    if not success:
        print("\n❌ 同步失败，请查看日志")
        print(f"日志位置: {syncer.backup_dir / 'sync_v2.log'}")
        exit(1)
    else:
        print("\n✅ 同步成功！")
        exit(0)

if __name__ == "__main__":
    main()


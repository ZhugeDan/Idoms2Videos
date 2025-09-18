"""
数据库管理器 - 基于SQLite的缓存系统
"""
import sqlite3
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import shutil
from loguru import logger

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "idiom_cache.db", storage_dir: str = "storage"):
        self.db_path = db_path
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建故事表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    idiom TEXT NOT NULL,
                    story_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(idiom)
                )
            ''')
            
            # 创建场景表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scenes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id INTEGER,
                    scene_text TEXT NOT NULL,
                    scene_order INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            ''')
            
            # 创建图片表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id INTEGER,
                    scene_id INTEGER,
                    image_path TEXT NOT NULL,
                    image_filename TEXT NOT NULL,
                    image_size INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id),
                    FOREIGN KEY (scene_id) REFERENCES scenes (id)
                )
            ''')
            
            # 创建音频表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id INTEGER,
                    audio_path TEXT NOT NULL,
                    audio_filename TEXT NOT NULL,
                    audio_duration REAL,
                    audio_size INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            ''')
            
            # 创建视频表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id INTEGER,
                    video_path TEXT NOT NULL,
                    video_filename TEXT NOT NULL,
                    video_duration REAL,
                    video_size INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories (id)
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stories_idiom ON stories(idiom)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_scenes_story_id ON scenes(story_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_story_id ON images(story_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_audio_story_id ON audio(story_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_story_id ON videos(story_id)')
            
            conn.commit()
            logger.info("数据库初始化完成")
    
    def save_story(self, idiom: str, story_text: str, scenes: List[str]) -> int:
        """保存故事和场景"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 保存故事
            cursor.execute('''
                INSERT OR REPLACE INTO stories (idiom, story_text, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (idiom, story_text))
            
            story_id = cursor.lastrowid
            
            # 删除旧场景
            cursor.execute('DELETE FROM scenes WHERE story_id = ?', (story_id,))
            
            # 保存新场景
            for i, scene in enumerate(scenes):
                cursor.execute('''
                    INSERT INTO scenes (story_id, scene_text, scene_order)
                    VALUES (?, ?, ?)
                ''', (story_id, scene, i + 1))
            
            conn.commit()
            logger.info(f"故事 '{idiom}' 已保存，包含 {len(scenes)} 个场景")
            return story_id
    
    def save_images(self, story_id: int, images: List[Any], idiom: str) -> List[str]:
        """保存图片并返回文件路径列表"""
        image_paths = []
        
        for i, image in enumerate(images):
            # 生成文件名
            filename = f"{idiom}_{i+1:02d}.jpg"
            image_path = self.storage_dir / "images" / filename
            image_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存图片
            if hasattr(image, 'save'):
                image.save(image_path, 'JPEG', quality=95)
            else:
                # 如果是PIL Image对象
                import PIL.Image
                if isinstance(image, PIL.Image.Image):
                    image.save(image_path, 'JPEG', quality=95)
                else:
                    logger.error(f"无法保存图片 {i+1}，类型: {type(image)}")
                    continue
            
            # 获取文件大小
            file_size = image_path.stat().st_size
            
            # 保存到数据库
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO images (story_id, image_path, image_filename, image_size)
                    VALUES (?, ?, ?, ?)
                ''', (story_id, str(image_path), filename, file_size))
            
            image_paths.append(str(image_path))
            logger.info(f"图片已保存: {filename}")
        
        return image_paths
    
    def save_audio(self, story_id: int, audio_path: str, idiom: str) -> str:
        """保存音频文件"""
        # 生成文件名
        filename = f"{idiom}_01.mp3"
        new_audio_path = self.storage_dir / "audio" / filename
        new_audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制音频文件
        shutil.copy2(audio_path, new_audio_path)
        
        # 获取文件信息
        file_size = new_audio_path.stat().st_size
        
        # 保存到数据库
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO audio (story_id, audio_path, audio_filename, audio_size)
                VALUES (?, ?, ?, ?)
            ''', (story_id, str(new_audio_path), filename, file_size))
        
        logger.info(f"音频已保存: {filename}")
        return str(new_audio_path)
    
    def save_video(self, story_id: int, video_path: str, idiom: str) -> str:
        """保存视频文件"""
        # 生成文件名
        filename = f"{idiom}_story.mp4"
        new_video_path = self.storage_dir / "videos" / filename
        new_video_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制视频文件
        shutil.copy2(video_path, new_video_path)
        
        # 获取文件信息
        file_size = new_video_path.stat().st_size
        
        # 保存到数据库
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO videos (story_id, video_path, video_filename, video_size)
                VALUES (?, ?, ?, ?)
            ''', (story_id, str(new_video_path), filename, file_size))
        
        logger.info(f"视频已保存: {filename}")
        return str(new_video_path)
    
    def get_story(self, idiom: str) -> Optional[Dict[str, Any]]:
        """获取故事信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 获取故事基本信息
            cursor.execute('''
                SELECT id, story_text, created_at, updated_at
                FROM stories WHERE idiom = ?
            ''', (idiom,))
            
            story_row = cursor.fetchone()
            if not story_row:
                return None
            
            story_id, story_text, created_at, updated_at = story_row
            
            # 获取场景
            cursor.execute('''
                SELECT scene_text, scene_order
                FROM scenes WHERE story_id = ?
                ORDER BY scene_order
            ''', (story_id,))
            
            scenes = [row[0] for row in cursor.fetchall()]
            
            # 获取图片
            cursor.execute('''
                SELECT image_path, image_filename, image_size
                FROM images WHERE story_id = ?
                ORDER BY id
            ''', (story_id,))
            
            images = [{'path': row[0], 'filename': row[1], 'size': row[2]} 
                     for row in cursor.fetchall()]
            
            # 获取音频
            cursor.execute('''
                SELECT audio_path, audio_filename, audio_size
                FROM audio WHERE story_id = ?
            ''', (story_id,))
            
            audio_row = cursor.fetchone()
            audio = {'path': audio_row[0], 'filename': audio_row[1], 'size': audio_row[2]} if audio_row else None
            
            # 获取视频
            cursor.execute('''
                SELECT video_path, video_filename, video_size
                FROM videos WHERE story_id = ?
            ''', (story_id,))
            
            video_row = cursor.fetchone()
            video = {'path': video_row[0], 'filename': video_row[1], 'size': video_row[2]} if video_row else None
            
            return {
                'id': story_id,
                'idiom': idiom,
                'story_text': story_text,
                'scenes': scenes,
                'images': images,
                'audio': audio,
                'video': video,
                'created_at': created_at,
                'updated_at': updated_at
            }
    
    def list_stories(self, limit: int = 50) -> List[Dict[str, Any]]:
        """列出所有故事"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.idiom, s.story_text, s.created_at, s.updated_at,
                       COUNT(DISTINCT sc.id) as scene_count,
                       COUNT(DISTINCT i.id) as image_count,
                       COUNT(DISTINCT a.id) as audio_count,
                       COUNT(DISTINCT v.id) as video_count
                FROM stories s
                LEFT JOIN scenes sc ON s.id = sc.story_id
                LEFT JOIN images i ON s.id = i.story_id
                LEFT JOIN audio a ON s.id = a.story_id
                LEFT JOIN videos v ON s.id = v.story_id
                GROUP BY s.id, s.idiom, s.story_text, s.created_at, s.updated_at
                ORDER BY s.updated_at DESC
                LIMIT ?
            ''', (limit,))
            
            stories = []
            for row in cursor.fetchall():
                stories.append({
                    'idiom': row[0],
                    'story_text': row[1][:100] + '...' if len(row[1]) > 100 else row[1],
                    'created_at': row[2],
                    'updated_at': row[3],
                    'scene_count': row[4],
                    'image_count': row[5],
                    'audio_count': row[6],
                    'video_count': row[7]
                })
            
            return stories
    
    def delete_story(self, idiom: str) -> bool:
        """删除故事及其所有相关文件"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取故事ID
                cursor.execute('SELECT id FROM stories WHERE idiom = ?', (idiom,))
                story_row = cursor.fetchone()
                if not story_row:
                    return False
                
                story_id = story_row[0]
                
                # 获取所有文件路径
                cursor.execute('SELECT image_path FROM images WHERE story_id = ?', (story_id,))
                image_paths = [row[0] for row in cursor.fetchall()]
                
                cursor.execute('SELECT audio_path FROM audio WHERE story_id = ?', (story_id,))
                audio_paths = [row[0] for row in cursor.fetchall()]
                
                cursor.execute('SELECT video_path FROM videos WHERE story_id = ?', (story_id,))
                video_paths = [row[0] for row in cursor.fetchall()]
                
                # 删除文件
                for path in image_paths + audio_paths + video_paths:
                    try:
                        Path(path).unlink(missing_ok=True)
                    except Exception as e:
                        logger.warning(f"删除文件失败 {path}: {e}")
                
                # 删除数据库记录
                cursor.execute('DELETE FROM stories WHERE id = ?', (story_id,))
                conn.commit()
                
                logger.info(f"故事 '{idiom}' 及其所有文件已删除")
                return True
                
        except Exception as e:
            logger.error(f"删除故事失败: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """获取存储统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 统计故事数量
            cursor.execute('SELECT COUNT(*) FROM stories')
            story_count = cursor.fetchone()[0]
            
            # 统计文件数量
            cursor.execute('SELECT COUNT(*) FROM images')
            image_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM audio')
            audio_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM videos')
            video_count = cursor.fetchone()[0]
            
            # 计算存储大小
            cursor.execute('SELECT SUM(image_size) FROM images')
            image_size = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT SUM(audio_size) FROM audio')
            audio_size = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT SUM(video_size) FROM videos')
            video_size = cursor.fetchone()[0] or 0
            
            total_size = image_size + audio_size + video_size
            
            return {
                'story_count': story_count,
                'image_count': image_count,
                'audio_count': audio_count,
                'video_count': video_count,
                'total_size': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'image_size': image_size,
                'audio_size': audio_size,
                'video_size': video_size
            }

# 创建全局数据库管理器实例
db_manager = DatabaseManager()

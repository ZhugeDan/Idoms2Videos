"""
工具函数
"""
import hashlib
import pickle
import logging
from pathlib import Path
from typing import Any, Optional
import torch
import GPUtil
from loguru import logger

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: Path = Path("./cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_key(self, content: str, prefix: str = "") -> str:
        """生成缓存键"""
        hash_content = f"{prefix}_{content}"
        return hashlib.md5(hash_content.encode()).hexdigest()
    
    def get_cached_result(self, key: str) -> Optional[Any]:
        """获取缓存结果"""
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"读取缓存失败: {e}")
        return None
    
    def save_cache(self, key: str, result: Any) -> bool:
        """保存缓存"""
        try:
            cache_file = self.cache_dir / f"{key}.pkl"
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            return True
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
            return False
    
    def clear_cache(self, prefix: str = ""):
        """清理缓存"""
        if prefix:
            pattern = f"{prefix}_*.pkl"
            for cache_file in self.cache_dir.glob(pattern):
                cache_file.unlink()
        else:
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()

class PerformanceMonitor:
    """性能监控器"""
    
    @staticmethod
    def get_gpu_info():
        """获取GPU信息"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return {
                    'name': gpu.name,
                    'memory_total': gpu.memoryTotal,
                    'memory_used': gpu.memoryUsed,
                    'memory_free': gpu.memoryFree,
                    'temperature': gpu.temperature,
                    'utilization': gpu.load * 100
                }
        except Exception as e:
            logger.warning(f"获取GPU信息失败: {e}")
        return None
    
    @staticmethod
    def get_memory_info():
        """获取内存信息"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percentage': memory.percent
            }
        except Exception as e:
            logger.warning(f"获取内存信息失败: {e}")
        return None
    
    @staticmethod
    def cleanup_gpu_memory():
        """清理GPU内存"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("GPU内存已清理")

class TextProcessor:
    """文本处理器"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本"""
        import re
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。！？""''（）]', '', text)
        return text.strip()
    
    @staticmethod
    def split_sentences(text: str) -> list:
        """分割句子"""
        import re
        sentences = re.split(r'[。！？]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 5) -> list:
        """提取关键词"""
        import jieba
        import jieba.analyse
        
        # 设置停用词
        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个'}
        
        # 提取关键词
        keywords = jieba.analyse.extract_tags(text, topK=max_keywords, withWeight=False)
        
        # 过滤停用词
        filtered_keywords = [kw for kw in keywords if kw not in stopwords]
        
        return filtered_keywords

class FileManager:
    """文件管理器"""
    
    @staticmethod
    def ensure_directory(path: Path):
        """确保目录存在"""
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_unique_filename(base_path: Path, extension: str) -> Path:
        """获取唯一文件名"""
        counter = 1
        while True:
            filename = base_path / f"{base_path.stem}_{counter}{extension}"
            if not filename.exists():
                return filename
            counter += 1
    
    @staticmethod
    def cleanup_temp_files(temp_dir: Path, max_age_hours: int = 24):
        """清理临时文件"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in temp_dir.rglob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                        logger.info(f"已删除过期临时文件: {file_path}")
                    except Exception as e:
                        logger.warning(f"删除文件失败 {file_path}: {e}")

class Logger:
    """日志管理器"""
    
    @staticmethod
    def setup_logger(log_file: Path, log_level: str = "INFO"):
        """设置日志"""
        logger.remove()  # 移除默认处理器
        
        # 添加文件日志
        logger.add(
            log_file,
            rotation="10 MB",
            retention="7 days",
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            encoding="utf-8"
        )
        
        # 添加控制台日志
        logger.add(
            lambda msg: print(msg, end=""),
            level=log_level,
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}"
        )
        
        return logger

# 初始化工具
cache_manager = CacheManager()
performance_monitor = PerformanceMonitor()
text_processor = TextProcessor()
file_manager = FileManager()

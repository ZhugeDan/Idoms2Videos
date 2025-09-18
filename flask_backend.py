#!/usr/bin/env python3
"""
Flask后端模块 - 避免Streamlit依赖
"""
import os
import base64
from pathlib import Path
from PIL import Image
import io
import json
from typing import List, Optional, Dict
import warnings

# 抑制警告信息
warnings.filterwarnings("ignore", message="A matching Triton is not available")
warnings.filterwarnings("ignore", message="torch_dtype is deprecated")
warnings.filterwarnings("ignore", message="Couldn't connect to the Hub")
warnings.filterwarnings("ignore", message="Token indices sequence length is longer than")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

# 导入自定义模块
from config import config
from utils import Logger, PerformanceMonitor, cache_manager
from loguru import logger
from modules.story_generator import DeepSeekStoryGenerator
from modules.image_generator import ImageGenerator
from modules.audio_generator import AudioGenerator
from modules.video_composer import VideoComposer
from simple_video_composer import SimpleVideoComposer
from modules.simple_enhanced_composer import SimpleEnhancedComposer
from modules.scene_extractor import SceneExtractor
from modules.text_segmenter import TextSegmenter

class FlaskBackend:
    """Flask后端处理类"""
    
    def __init__(self):
        self.story_generator = None
        self.scene_extractor = None
        self.image_generator = None
        self.text_segmenter = None
        self.audio_generator = None
        self.video_composer = None
        self.enhanced_video_composer = None
        self.performance_monitor = None
        
        # 初始化日志
        Logger.setup_logger(config.LOG_FILE, config.LOG_LEVEL)
    
    def _initialize_components(self):
        """按需初始化各个组件"""
        try:
            # 检查API密钥
            if not config.DEEPSEEK_API_KEY:
                raise ValueError("请在环境变量中设置 DEEPSEEK_API_KEY")
            
            # 初始化基础组件
            if not self.scene_extractor:
                self.scene_extractor = SceneExtractor()
            
            if not self.text_segmenter:
                self.text_segmenter = TextSegmenter()
            
            if not self.audio_generator:
                self.audio_generator = AudioGenerator()
            
            if not self.video_composer:
                self.video_composer = SimpleVideoComposer()
            
            if not self.enhanced_video_composer:
                self.enhanced_video_composer = SimpleEnhancedComposer()
            
            if not self.performance_monitor:
                self.performance_monitor = PerformanceMonitor()
            
            # 初始化故事生成器
            if not self.story_generator:
                self.story_generator = DeepSeekStoryGenerator(config.DEEPSEEK_API_KEY)
            
            # 初始化图片生成器（按需加载）
            if not self.image_generator:
                self.image_generator = ImageGenerator()
            
            return True
            
        except Exception as e:
            logger.error(f"组件初始化失败: {e}")
            raise
    
    def generate_story_text(self, idiom: str) -> str:
        """生成故事文本"""
        try:
            # 初始化组件
            self._initialize_components()
            
            # 检查缓存
            cache_key = cache_manager.get_cache_key(f"story_{idiom}")
            cached_story = cache_manager.get_cached_result(cache_key)
            
            if cached_story:
                logger.info("使用缓存的故事")
                return cached_story
            
            # 生成新故事
            logger.info(f"开始生成故事: {idiom}")
            story = self.story_generator.generate_story(idiom)
            logger.info("故事生成完成")
            
            # 保存到缓存
            cache_manager.save_cache(cache_key, story)
            
            return story
            
        except Exception as e:
            logger.error(f"生成故事失败: {e}")
            raise
    
    def extract_scenes(self, story_text: str) -> List[str]:
        """提取场景"""
        try:
            logger.info("开始提取场景")
            scenes = self.scene_extractor.extract_scenes(story_text)
            logger.info(f"成功提取 {len(scenes)} 个场景")
            return scenes
            
        except Exception as e:
            logger.error(f"提取场景失败: {e}")
            raise
    
    def generate_story_images(self, scenes: List[str], idiom: str) -> List:
        """生成故事图片"""
        try:
            logger.info(f"开始生成 {len(scenes)} 个场景的图片")
            
            # 检查缓存
            cache_key = cache_manager.get_cache_key(f"images_{idiom}")
            cached_images = cache_manager.get_cached_result(cache_key)
            
            if cached_images:
                logger.info("使用缓存的图片")
                return cached_images
            
            # 生成新图片
            images = []
            for i, scene in enumerate(scenes):
                logger.info(f"生成第 {i+1} 张图片: {scene}")
                image = self.image_generator.generate_image(scene, idiom)
                images.append(image)
            
            # 保存到缓存
            cache_manager.save_cache(cache_key, images)
            
            # 保存图片到output_pic文件夹
            self._save_images_to_output(images, idiom)
            
            logger.info(f"成功生成 {len(images)} 张图片")
            return images
            
        except Exception as e:
            logger.error(f"生成图片失败: {e}")
            raise
    
    def _save_images_to_output(self, images: List, idiom: str) -> List[Path]:
        """保存图片到output_pic文件夹"""
        try:
            # 确保输出目录存在
            config.OUTPUT_PIC_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"开始保存图片到: {config.OUTPUT_PIC_DIR}")
            
            saved_paths = []
            for i, image in enumerate(images):
                try:
                    # 生成文件名：成语_序号.jpg
                    filename = f"{idiom}_{i+1:02d}.jpg"
                    output_path = config.OUTPUT_PIC_DIR / filename
                    
                    # 保存图片
                    if hasattr(image, 'save'):  # PIL.Image对象
                        image.save(output_path, 'JPEG', quality=95)
                    else:
                        # 假设是文件路径
                        import shutil
                        shutil.copy2(image, output_path)
                    
                    saved_paths.append(output_path)
                    logger.info(f"图片已保存: {output_path}")
                    
                except Exception as e:
                    logger.error(f"保存第 {i+1} 张图片失败: {e}")
                    continue
            
            logger.info(f"成功保存 {len(saved_paths)} 张图片")
            return saved_paths
            
        except Exception as e:
            logger.error(f"保存图片过程失败: {e}")
            return []
    
    def generate_story_audio(self, story_text: str, idiom: str):
        """生成故事音频"""
        try:
            # 检查缓存
            cache_key = cache_manager.get_cache_key(f"audio_{idiom}")
            cached_audio = cache_manager.get_cached_result(cache_key)
            
            if cached_audio:
                logger.info("使用缓存的音频")
                return cached_audio
            
            # 生成新音频
            logger.info("开始生成音频")
            segments = self.text_segmenter.segment_text(story_text)
            logger.info(f"文本分段完成，共 {len(segments)} 个段落")
            
            audio = self.audio_generator.generate_story_audio(segments)
            logger.info("音频生成完成")
            
            # 保存到缓存
            cache_manager.save_cache(cache_key, audio)
            
            # 保存音频到output_audio文件夹
            saved_audio_path = self._save_audio_to_output(audio, idiom, 1)
            if saved_audio_path:
                logger.info(f"音频已保存到: {saved_audio_path}")
            
            return audio
            
        except Exception as e:
            logger.error(f"音频生成失败: {e}")
            # 返回一个静音音频作为备用
            from pydub import AudioSegment
            fallback_audio = AudioSegment.silent(duration=5000)  # 5秒静音
            logger.info("使用静音音频作为备用")
            return fallback_audio
    
    def _save_audio_to_output(self, audio, idiom: str, audio_index: int = 1) -> Optional[Path]:
        """保存音频到output_audio文件夹"""
        try:
            # 确保输出目录存在
            config.OUTPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"开始保存音频到: {config.OUTPUT_AUDIO_DIR}")
            
            # 生成文件名：成语_序号.mp3
            filename = f"{idiom}_{audio_index:02d}.mp3"
            output_path = config.OUTPUT_AUDIO_DIR / filename
            
            # 保存音频
            success = self.audio_generator.export_audio(audio, str(output_path))
            
            if success:
                logger.info(f"音频已保存: {output_path}")
                return output_path
            else:
                logger.error(f"音频保存失败: {output_path}")
                return None
            
        except Exception as e:
            logger.error(f"保存音频过程失败: {e}")
            return None
    
    def create_video(self, images: List, audio, idiom: str, 
                    video_style: str = "simple", transition_type: str = "fade") -> str:
        """创建视频"""
        try:
            logger.info(f"开始创建视频，风格: {video_style}")
            
            if video_style == "enhanced":
                # 使用增强版视频合成器
                video_path = self.enhanced_video_composer.create_smooth_story_video(
                    images, audio, f"output/{idiom}_story.mp4", transition_type
                )
            else:
                # 使用简化版视频合成器
                video_path = self.video_composer.create_story_video(
                    images, audio, f"output/{idiom}_story.mp4"
                )
            
            logger.info(f"视频创建完成: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"创建视频失败: {e}")
            raise

# 创建全局后端实例
backend = FlaskBackend()

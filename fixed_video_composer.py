"""
修复版视频合成器 - 解决MoviePy兼容性问题
"""
import os
import numpy as np
from pathlib import Path
from typing import List, Optional, Union
from loguru import logger

# 尝试导入MoviePy，处理版本兼容性
try:
    from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
        MOVIEPY_AVAILABLE = True
    except ImportError:
        MOVIEPY_AVAILABLE = False
        logger.error("MoviePy 未安装或导入失败")

class FixedVideoComposer:
    """修复版视频合成器"""
    
    def __init__(self, fps: int = 24, bitrate: str = "2000k"):
        self.fps = fps
        self.bitrate = bitrate
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_video(self, images: List, audio_path: str, idiom: str) -> str:
        """创建视频 - 修复版"""
        if not MOVIEPY_AVAILABLE:
            logger.error("MoviePy 不可用，无法创建视频")
            return None
        
        try:
            logger.info("开始创建修复版视频...")
            
            # 加载音频
            audio_clip = AudioFileClip(audio_path)
            audio_duration = float(audio_clip.duration)
            
            # 计算每张图片的显示时间
            image_duration = audio_duration / len(images)
            logger.info(f"音频时长: {audio_duration:.2f}秒, 每张图片: {image_duration:.2f}秒")
            
            # 创建图片剪辑
            clips = []
            for i, image in enumerate(images):
                try:
                    # 处理PIL Image对象
                    if hasattr(image, 'save'):
                        # 转换为numpy数组
                        img_array = np.array(image)
                    else:
                        img_array = np.array(image)
                    
                    # 创建图片剪辑
                    clip = ImageClip(img_array, duration=image_duration)
                    
                    # 尝试调整大小（兼容不同版本）
                    try:
                        clip = clip.resize(height=1080)
                    except AttributeError:
                        try:
                            clip = clip.resized(height=1080)
                        except AttributeError:
                            logger.warning(f"无法调整图片 {i+1} 大小，使用原始尺寸")
                    
                    clips.append(clip)
                    logger.info(f"图片 {i+1} 处理完成")
                    
                except Exception as e:
                    logger.error(f"处理图片 {i+1} 失败: {e}")
                    continue
            
            if not clips:
                logger.error("没有可用的图片剪辑")
                return None
            
            # 拼接视频
            logger.info("正在拼接视频...")
            video = concatenate_videoclips(clips, method="compose")
            
            # 添加音频
            logger.info("正在添加音频...")
            final_video = self._add_audio_fixed(video, audio_clip)
            
            if final_video is None:
                logger.error("最终视频对象为None")
                return None
            
            # 导出视频
            output_path = self.output_dir / f"{idiom}_story.mp4"
            logger.info(f"开始导出视频到: {output_path}")
            
            # 使用兼容的参数
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                bitrate=self.bitrate,
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # 清理资源
            final_video.close()
            audio_clip.close()
            
            logger.info(f"视频创建成功: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"创建视频失败: {e}")
            return None
    
    def _add_audio_fixed(self, video, audio_clip):
        """修复版音频添加方法"""
        try:
            # 获取时长
            video_duration = float(video.duration)
            audio_duration = float(audio_clip.duration)
            
            logger.info(f"视频时长: {video_duration:.2f}秒, 音频时长: {audio_duration:.2f}秒")
            
            # 简单的时长匹配
            if abs(audio_duration - video_duration) < 1.0:
                # 时长接近，直接添加
                try:
                    final_video = video.set_audio(audio_clip)
                except AttributeError:
                    try:
                        final_video = video.with_audio(audio_clip)
                    except AttributeError:
                        logger.warning("无法添加音频，返回原视频")
                        return video
            else:
                # 时长不匹配，调整音频
                if audio_duration > video_duration:
                    # 音频太长，截取
                    try:
                        audio_clip = audio_clip.subclip(0, video_duration)
                    except AttributeError:
                        logger.warning("无法截取音频，使用原音频")
                else:
                    # 音频太短，循环播放
                    try:
                        # 计算需要循环的次数
                        loops = int(video_duration / audio_duration) + 1
                        audio_clip = audio_clip.loop(duration=video_duration)
                    except AttributeError:
                        logger.warning("无法循环音频，使用原音频")
                
                # 添加调整后的音频
                try:
                    final_video = video.set_audio(audio_clip)
                except AttributeError:
                    try:
                        final_video = video.with_audio(audio_clip)
                    except AttributeError:
                        logger.warning("无法添加调整后的音频，返回原视频")
                        return video
            
            return final_video
            
        except Exception as e:
            logger.error(f"添加音频失败: {e}")
            return video

# 创建全局实例
fixed_video_composer = FixedVideoComposer()

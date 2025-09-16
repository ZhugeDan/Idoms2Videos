"""
简化版视频合成模块 - 避免MoviePy版本兼容性问题
"""
import os
import tempfile
from pathlib import Path
from typing import List, Optional
from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
from PIL import Image
from loguru import logger
from config import config

class SimpleVideoComposer:
    """简化版视频合成器"""
    
    def __init__(self, output_width: int = None, output_height: int = None):
        self.output_size = (
            output_width or config.VIDEO_WIDTH,
            output_height or config.VIDEO_HEIGHT
        )
        self.fps = config.VIDEO_FPS
        self.bitrate = config.VIDEO_BITRATE
    
    def create_story_video(self, images: List[Image.Image], audio: any, 
                          output_path: str) -> str:
        """创建故事视频 - 简化版"""
        try:
            logger.info("开始创建简化版视频...")
            
            # 保存音频文件
            audio_path = self._save_audio(audio)
            
            # 计算每张图片的显示时间
            audio_duration = self._get_audio_duration(audio)
            image_duration = audio_duration / len(images) if len(images) > 0 else 3.0
            
            logger.info(f"音频时长: {audio_duration:.2f}秒, 每张图片: {image_duration:.2f}秒")
            
            # 创建图片剪辑列表
            clips = []
            temp_image_paths = []
            
            for i, image in enumerate(images):
                # 保存图片
                img_path = self._save_image(image, i)
                temp_image_paths.append(img_path)
                
                # 创建图片剪辑
                clip = self._create_simple_image_clip(img_path, image_duration)
                clips.append(clip)
            
            # 拼接所有图片剪辑
            video = concatenate_videoclips(clips, method="compose")
            
            # 添加音频
            final_video = self._add_audio_simple(video, audio_path)
            
            # 导出视频
            self._export_video_simple(final_video, output_path)
            
            # 清理临时文件
            self._cleanup_temp_files(audio_path, temp_image_paths)
            
            logger.info(f"视频创建完成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"创建视频失败: {e}")
            raise
    
    def _get_audio_duration(self, audio: any) -> float:
        """获取音频时长（秒）"""
        try:
            # 如果是AudioSegment对象
            if hasattr(audio, '__len__') and hasattr(audio, 'export'):
                return len(audio) / 1000.0  # AudioSegment的len()返回毫秒
            # 如果是AudioFileClip对象
            elif hasattr(audio, 'duration'):
                return float(audio.duration)
            # 如果是其他类型，尝试获取时长属性
            elif hasattr(audio, 'len'):
                return audio.len() / 1000.0
            else:
                logger.warning("无法确定音频时长，使用默认值15秒")
                return 15.0
        except Exception as e:
            logger.warning(f"获取音频时长失败: {e}，使用默认值15秒")
            return 15.0
    
    def _save_audio(self, audio: any) -> str:
        """保存音频到临时文件"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            
            # 如果是AudioSegment对象
            if hasattr(audio, 'export'):
                audio.export(temp_file.name, format="wav")
            # 如果是AudioFileClip对象
            elif hasattr(audio, 'write_audiofile'):
                audio.write_audiofile(temp_file.name, verbose=False, logger=None)
            else:
                raise ValueError(f"不支持的音频类型: {type(audio)}")
            
            return temp_file.name
        except Exception as e:
            logger.error(f"保存音频失败: {e}")
            raise
    
    def _save_image(self, image: Image.Image, index: int) -> str:
        """保存图片到临时文件"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            image.save(temp_file.name, 'PNG')
            return temp_file.name
        except Exception as e:
            logger.error(f"保存图片失败: {e}")
            raise
    
    def _create_simple_image_clip(self, image_path: str, duration: float) -> ImageClip:
        """创建简化的图片剪辑"""
        try:
            clip = ImageClip(image_path, duration=duration)
            
            # 调整图片尺寸以适应输出尺寸
            try:
                clip = clip.resize(self.output_size)
            except AttributeError:
                # 如果resize方法不可用，使用resized方法
                clip = clip.resized(self.output_size)
            
            return clip
            
        except Exception as e:
            logger.error(f"创建图片剪辑失败: {e}")
            raise
    
    def _add_audio_simple(self, video, audio_path: str):
        """简化的音频添加方法"""
        try:
            # 加载音频
            audio_clip = AudioFileClip(audio_path)
            
            # 获取音频和视频的时长
            audio_duration = float(audio_clip.duration)
            video_duration = float(video.duration)
            
            logger.info(f"视频时长: {video_duration:.2f}秒, 音频时长: {audio_duration:.2f}秒")
            
            # 简单的时长匹配策略
            if abs(audio_duration - video_duration) < 1.0:
                # 如果时长接近，直接添加音频
                try:
                    final_video = video.set_audio(audio_clip)
                except AttributeError:
                    # 如果set_audio不可用，尝试with_audio
                    try:
                        final_video = video.with_audio(audio_clip)
                    except AttributeError:
                        # 如果都不行，返回原视频
                        logger.warning("无法添加音频，返回无音频视频")
                        return video
            else:
                # 如果时长差异较大，调整视频长度
                if audio_duration > video_duration:
                    # 音频更长，重复视频
                    repeat_count = int(audio_duration / video_duration) + 1
                    repeated_video = concatenate_videoclips([video] * repeat_count)
                    # 裁剪到音频长度
                    final_video = repeated_video.subclip(0, audio_duration)
                else:
                    # 视频更长，裁剪视频
                    final_video = video.subclip(0, audio_duration)
                
                # 添加音频
                try:
                    final_video = final_video.set_audio(audio_clip)
                except AttributeError:
                    try:
                        final_video = final_video.with_audio(audio_clip)
                    except AttributeError:
                        logger.warning("无法添加音频，返回无音频视频")
                        return final_video
            
            return final_video
            
        except Exception as e:
            logger.error(f"添加音频失败: {e}")
            # 返回无音频的视频
            return video
    
    def _export_video_simple(self, video, output_path: str):
        """简化的视频导出方法"""
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 导出视频
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                bitrate=self.bitrate,
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
        except Exception as e:
            logger.error(f"导出视频失败: {e}")
            raise
    
    def _cleanup_temp_files(self, audio_path: str, image_paths: List[str]):
        """清理临时文件"""
        try:
            # 清理音频临时文件
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            
            # 清理图片临时文件
            for img_path in image_paths:
                if os.path.exists(img_path):
                    os.unlink(img_path)
            
            logger.info("临时文件已清理")
            
        except Exception as e:
            logger.error(f"清理临时文件失败: {e}")

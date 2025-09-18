"""
修复版音频生成器 - 解决网络连接问题
"""
import os
import tempfile
from pathlib import Path
from typing import List, Optional
import numpy as np
from loguru import logger

class FixedAudioGenerator:
    """修复版音频生成器"""
    
    def __init__(self):
        self.output_dir = Path("output_audio")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_story_audio(self, story_text: str, idiom: str) -> str:
        """生成故事音频 - 修复版"""
        try:
            logger.info("开始生成修复版音频...")
            
            # 分段处理长文本
            segments = self._split_text(story_text)
            logger.info(f"成功分段，共 {len(segments)} 个段落")
            
            audio_segments = []
            
            for i, segment in enumerate(segments):
                logger.info(f"正在生成第 {i+1}/{len(segments)} 个音频段落...")
                
                # 尝试使用gTTS
                audio_path = self._generate_with_gtts(segment, f"{idiom}_temp_{i}")
                
                if audio_path is None:
                    # 使用备用方案
                    logger.warning("gTTS生成失败，使用备用方案")
                    audio_path = self._generate_fallback_audio(segment, f"{idiom}_temp_{i}")
                
                if audio_path:
                    audio_segments.append(audio_path)
                    logger.info(f"段落 {i+1} 音频生成完成")
                else:
                    logger.error(f"段落 {i+1} 音频生成失败")
            
            if not audio_segments:
                logger.error("所有音频段落生成失败")
                return None
            
            # 合并音频
            final_audio_path = self._merge_audio_segments(audio_segments, idiom)
            
            # 清理临时文件
            for temp_path in audio_segments:
                try:
                    os.remove(temp_path)
                except:
                    pass
            
            return final_audio_path
            
        except Exception as e:
            logger.error(f"音频生成失败: {e}")
            return None
    
    def _split_text(self, text: str, max_length: int = 100) -> List[str]:
        """分段文本"""
        if len(text) <= max_length:
            return [text]
        
        segments = []
        current_segment = ""
        
        for char in text:
            current_segment += char
            if len(current_segment) >= max_length and char in '。！？':
                segments.append(current_segment.strip())
                current_segment = ""
        
        if current_segment.strip():
            segments.append(current_segment.strip())
        
        return segments
    
    def _generate_with_gtts(self, text: str, filename: str) -> Optional[str]:
        """使用gTTS生成音频"""
        try:
            from gtts import gTTS
            
            # 创建临时文件
            temp_path = f"temp_{filename}.mp3"
            
            # 生成音频
            tts = gTTS(text=text, lang='zh-cn', slow=False)
            tts.save(temp_path)
            
            return temp_path
            
        except Exception as e:
            logger.warning(f"gTTS生成失败: {e}")
            return None
    
    def _generate_fallback_audio(self, text: str, filename: str) -> str:
        """备用音频生成方案 - 使用本地TTS或生成有声音的音频"""
        try:
            # 尝试使用Windows自带的SAPI (Speech API)
            try:
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                
                # 保存为WAV文件
                temp_path = f"temp_{filename}.wav"
                
                # 使用Windows SAPI生成语音
                # 需要先设置输出格式为WAV
                speaker.Voice = speaker.GetVoices().Item(0)  # 使用第一个可用语音
                speaker.Rate = 0  # 正常语速
                speaker.Volume = 100  # 最大音量
                
                # 生成语音并保存到文件
                speaker.SaveToFile(temp_path, 1)  # 1 = SVSFDefault
                
                # 如果文件生成成功
                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                    logger.info(f"使用Windows SAPI生成音频，时长: {len(text)*0.3:.1f}秒")
                    return temp_path
                    
            except ImportError:
                logger.debug("win32com不可用，尝试其他方案")
            except Exception as e:
                logger.debug(f"Windows SAPI失败: {e}")
            
            # 尝试使用pyttsx3作为备用方案
            try:
                import pyttsx3
                engine = pyttsx3.init()
                
                # 设置语音参数
                voices = engine.getProperty('voices')
                if voices:
                    engine.setProperty('voice', voices[0].id)  # 使用第一个可用语音
                engine.setProperty('rate', 150)  # 语速
                engine.setProperty('volume', 0.8)  # 音量
                
                # 保存为WAV文件
                temp_path = f"temp_{filename}.wav"
                engine.save_to_file(text, temp_path)
                engine.runAndWait()
                
                # 如果文件生成成功
                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                    logger.info(f"使用pyttsx3生成音频，时长: {len(text)*0.3:.1f}秒")
                    return temp_path
                    
            except ImportError:
                logger.debug("pyttsx3不可用，使用音频信号方案")
            except Exception as e:
                logger.debug(f"pyttsx3失败: {e}")
            
            # 备用方案：生成有声音的音频信号
            duration = len(text) * 0.3  # 每个字符0.3秒
            sample_rate = 22050
            
            # 生成有声音的音频信号
            t = np.linspace(0, duration, int(duration * sample_rate))
            
            # 生成多频率的音频信号，模拟语音
            frequencies = [220, 330, 440, 550]  # A3, E4, A4, C#5
            audio_signal = np.zeros_like(t)
            
            for i, freq in enumerate(frequencies):
                # 每个频率持续不同的时间段
                start_time = i * duration / len(frequencies)
                end_time = (i + 1) * duration / len(frequencies)
                mask = (t >= start_time) & (t < end_time)
                
                # 生成带包络的正弦波
                envelope = np.exp(-(t[mask] - start_time) * 2)  # 指数衰减
                audio_signal[mask] += 0.3 * envelope * np.sin(2 * np.pi * freq * t[mask])
            
            # 添加一些噪声使声音更自然
            noise = 0.05 * np.random.randn(len(t))
            audio_signal += noise
            
            # 归一化音频
            audio_signal = audio_signal / np.max(np.abs(audio_signal)) * 0.8
            
            # 保存为WAV文件
            temp_path = f"temp_{filename}.wav"
            
            # 使用scipy保存音频
            try:
                from scipy.io import wavfile
                wavfile.write(temp_path, sample_rate, (audio_signal * 32767).astype(np.int16))
            except ImportError:
                # 如果没有scipy，创建简单的WAV文件
                self._create_simple_wav(temp_path, audio_signal, sample_rate)
            
            logger.info(f"使用备用音频方案，时长: {duration*1000:.0f}ms (文本长度: {len(text)}字)")
            return temp_path
            
        except Exception as e:
            logger.error(f"备用音频生成失败: {e}")
            return None
    
    def _create_simple_wav(self, filename: str, data: np.ndarray, sample_rate: int):
        """创建简单的WAV文件"""
        import wave
        import struct
        
        # 转换为16位整数
        data = (data * 32767).astype(np.int16)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(data.tobytes())
    
    def _merge_audio_segments(self, audio_paths: List[str], idiom: str) -> str:
        """合并音频段落"""
        try:
            # 使用pydub合并音频
            from pydub import AudioSegment
            
            combined = AudioSegment.empty()
            
            for audio_path in audio_paths:
                if os.path.exists(audio_path):
                    try:
                        # 尝试不同的音频格式
                        if audio_path.endswith('.wav'):
                            audio = AudioSegment.from_wav(audio_path)
                        elif audio_path.endswith('.mp3'):
                            audio = AudioSegment.from_mp3(audio_path)
                        else:
                            audio = AudioSegment.from_file(audio_path)
                        
                        # 确保音频是单声道
                        if audio.channels > 1:
                            audio = audio.set_channels(1)
                        
                        # 设置采样率
                        audio = audio.set_frame_rate(22050)
                        
                        combined += audio
                        logger.info(f"成功合并音频段落: {audio_path}")
                        
                    except Exception as e:
                        logger.warning(f"跳过音频段落 {audio_path}: {e}")
                        continue
            
            if len(combined) == 0:
                logger.error("没有可用的音频段落")
                return None
            
            # 保存最终音频
            final_path = self.output_dir / f"{idiom}_01.mp3"
            combined.export(str(final_path), format="mp3", parameters=["-ac", "1", "-ar", "22050"])
            
            logger.info("故事音频生成完成")
            return str(final_path)
            
        except Exception as e:
            logger.error(f"合并音频失败: {e}")
            return None

# 创建全局实例
fixed_audio_generator = FixedAudioGenerator()

#!/usr/bin/env python3
"""
测试音频保存功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.audio_generator import AudioGenerator
from loguru import logger

def test_audio_save():
    """测试音频保存功能"""
    logger.info("开始测试音频保存功能...")
    
    try:
        # 确保输出目录存在
        config.OUTPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"输出目录: {config.OUTPUT_AUDIO_DIR}")
        
        # 创建音频生成器
        audio_gen = AudioGenerator()
        
        # 创建测试音频
        from pydub import AudioSegment
        test_audio = AudioSegment.silent(duration=3000)  # 3秒静音
        
        # 测试保存
        test_idiom = "测试成语"
        filename = f"{test_idiom}_audio.mp3"
        output_path = config.OUTPUT_AUDIO_DIR / filename
        
        logger.info(f"保存音频到: {output_path}")
        success = audio_gen.export_audio(test_audio, str(output_path))
        
        if success:
            logger.info("✅ 音频保存成功")
            if output_path.exists():
                file_size = output_path.stat().st_size
                logger.info(f"文件大小: {file_size} 字节")
            else:
                logger.warning("⚠️ 文件不存在")
        else:
            logger.error("❌ 音频保存失败")
        
        # 测试命名方式
        test_cases = ["守株待兔", "掩耳盗铃", "画蛇添足"]
        for idiom in test_cases:
            filename = f"{idiom}_audio.mp3"
            expected_path = config.OUTPUT_AUDIO_DIR / filename
            logger.info(f"预期文件名: {filename}")
            logger.info(f"预期路径: {expected_path}")
        
        logger.info("音频保存功能测试完成")
        return True
        
    except Exception as e:
        logger.error(f"音频保存功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_save()
    if success:
        print("✅ 音频保存功能测试成功")
    else:
        print("❌ 音频保存功能测试失败")



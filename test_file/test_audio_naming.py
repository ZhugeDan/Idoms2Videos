#!/usr/bin/env python3
"""
测试音频命名功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.audio_generator import AudioGenerator
from loguru import logger
from pydub import AudioSegment

def test_audio_naming():
    """测试音频命名功能"""
    logger.info("开始测试音频命名功能...")
    
    try:
        # 确保输出目录存在
        config.OUTPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"输出目录: {config.OUTPUT_AUDIO_DIR}")
        
        # 创建音频生成器
        audio_gen = AudioGenerator()
        
        # 创建测试音频
        test_audio = AudioSegment.silent(duration=3000)  # 3秒静音
        
        # 测试不同的成语和序号
        test_cases = [
            ("掩耳盗铃", 1),
            ("守株待兔", 1),
            ("画蛇添足", 1),
            ("掩耳盗铃", 2),  # 测试同一成语的不同序号
            ("守株待兔", 2),
        ]
        
        for idiom, index in test_cases:
            filename = f"{idiom}_{index:02d}.mp3"
            output_path = config.OUTPUT_AUDIO_DIR / filename
            
            logger.info(f"测试保存音频: {filename}")
            success = audio_gen.export_audio(test_audio, str(output_path))
            
            if success:
                logger.info(f"✅ 音频保存成功: {output_path}")
                if output_path.exists():
                    file_size = output_path.stat().st_size
                    logger.info(f"文件大小: {file_size} 字节")
                else:
                    logger.warning("⚠️ 文件不存在")
            else:
                logger.error(f"❌ 音频保存失败: {output_path}")
        
        # 显示目录中的所有音频文件
        logger.info("输出目录中的音频文件:")
        for file in config.OUTPUT_AUDIO_DIR.glob("*.mp3"):
            logger.info(f"  - {file.name}")
        
        logger.info("音频命名功能测试完成")
        return True
        
    except Exception as e:
        logger.error(f"音频命名功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_naming()
    if success:
        print("✅ 音频命名功能测试成功")
        print("音频文件现在使用 成语_序号.mp3 的命名格式")
    else:
        print("❌ 音频命名功能测试失败")


#!/usr/bin/env python3
"""
测试音频生成修复
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.audio_generator import AudioGenerator
from loguru import logger

def test_audio_generation():
    """测试音频生成功能"""
    logger.info("开始测试音频生成修复...")
    
    try:
        # 创建音频生成器
        audio_gen = AudioGenerator()
        
        # 测试文本
        test_texts = [
            "从前有一个农夫，他每天都要到田里干活。",
            "有一天，农夫在田里发现了一只兔子。",
            "兔子撞到了树桩上，农夫很高兴。"
        ]
        
        for i, text in enumerate(test_texts):
            logger.info(f"测试第 {i+1} 个文本: {text}")
            
            try:
                # 生成音频
                audio = audio_gen.text_to_speech(text, 'narration')
                
                # 获取音频信息
                duration = len(audio) / 1000.0
                logger.info(f"音频生成成功，时长: {duration:.2f}秒")
                
                # 保存测试音频
                output_path = f"test_audio_{i+1}.mp3"
                success = audio_gen.export_audio(audio, output_path)
                
                if success:
                    logger.info(f"音频已保存到: {output_path}")
                else:
                    logger.warning(f"音频保存失败: {output_path}")
                    
            except Exception as e:
                logger.error(f"生成第 {i+1} 个音频失败: {e}")
        
        logger.info("音频生成测试完成")
        
    except Exception as e:
        logger.error(f"音频生成测试失败: {e}")

if __name__ == "__main__":
    test_audio_generation()



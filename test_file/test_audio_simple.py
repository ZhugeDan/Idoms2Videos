#!/usr/bin/env python3
"""
简单测试音频生成
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.audio_generator import AudioGenerator
from modules.text_segmenter import TextSegmenter
from loguru import logger

def test_audio_components():
    """测试音频生成组件"""
    logger.info("开始测试音频生成组件...")
    
    try:
        # 测试文本分段器
        logger.info("测试文本分段器...")
        segmenter = TextSegmenter()
        test_text = "从前有一个农夫，他每天都要到田里干活。有一天，农夫在田里发现了一只兔子。"
        
        segments = segmenter.segment_text(test_text)
        logger.info(f"分段结果: {len(segments)} 个段落")
        for i, segment in enumerate(segments):
            logger.info(f"段落 {i+1}: {segment['type']} - {segment['text'][:30]}...")
        
        # 测试音频生成器
        logger.info("测试音频生成器...")
        audio_gen = AudioGenerator()
        
        # 测试单个文本转语音
        test_sentence = "从前有一个农夫"
        logger.info(f"测试文本: {test_sentence}")
        
        audio = audio_gen.text_to_speech(test_sentence, 'narration')
        duration = len(audio) / 1000.0
        logger.info(f"音频生成成功，时长: {duration:.2f}秒")
        
        # 测试完整故事音频生成
        logger.info("测试完整故事音频生成...")
        full_audio = audio_gen.generate_story_audio(segments)
        full_duration = len(full_audio) / 1000.0
        logger.info(f"完整音频生成成功，时长: {full_duration:.2f}秒")
        
        # 保存测试音频
        output_path = "test_audio_output.mp3"
        success = audio_gen.export_audio(full_audio, output_path)
        
        if success:
            logger.info(f"音频已保存到: {output_path}")
        else:
            logger.warning("音频保存失败")
        
        logger.info("音频组件测试完成")
        return True
        
    except Exception as e:
        logger.error(f"音频组件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_components()
    if success:
        print("✅ 音频组件测试成功")
    else:
        print("❌ 音频组件测试失败")



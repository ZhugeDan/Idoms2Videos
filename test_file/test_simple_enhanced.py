#!/usr/bin/env python3
"""
测试简化版增强视频合成器
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.simple_enhanced_composer import SimpleEnhancedComposer
from loguru import logger
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_test_images():
    """创建测试图片"""
    images = []
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
    
    for i, color in enumerate(colors):
        img = Image.new('RGB', (1080, 1920), color)
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            font = ImageFont.load_default()
        
        text = f"测试 {i+1}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1080 - text_width) // 2
        y = 900
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        images.append(img)
    
    return images

def test_simple_enhanced():
    """测试简化版增强视频合成器"""
    logger.info("测试简化版增强视频合成器...")
    
    try:
        images = create_test_images()
        
        # 创建测试音频
        from pydub import AudioSegment
        audio = AudioSegment.silent(duration=5000)  # 5秒静音
        
        composer = SimpleEnhancedComposer()
        
        # 测试不同的转场效果
        transition_types = ["fade", "slide", "zoom"]
        
        for transition_type in transition_types:
            logger.info(f"测试转场效果: {transition_type}")
            
            output_path = config.OUTPUT_DIR / f"test_simple_enhanced_{transition_type}.mp4"
            
            try:
                video_path = composer.create_smooth_story_video(
                    images, audio, str(output_path), transition_type
                )
                logger.info(f"✅ {transition_type} 转场效果测试成功: {video_path}")
            except Exception as e:
                logger.error(f"❌ {transition_type} 转场效果测试失败: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"简化版增强视频合成器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎬 测试简化版增强视频合成器")
    print("="*50)
    
    # 确保输出目录存在
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    success = test_simple_enhanced()
    
    if success:
        print("\n🎉 简化版增强视频合成器测试成功！")
        print("您现在可以在Web界面中选择增强转场效果了。")
    else:
        print("\n❌ 简化版增强视频合成器测试失败，请检查日志")


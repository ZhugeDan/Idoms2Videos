#!/usr/bin/env python3
"""
测试新的视频合成功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.enhanced_video_composer import EnhancedVideoComposer
from modules.story_diffusion_composer import StoryDiffusionComposer
from loguru import logger
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_simple_test_images():
    """创建简单的测试图片"""
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

def test_enhanced_composer():
    """测试增强版视频合成器"""
    logger.info("测试增强版视频合成器...")
    
    try:
        images = create_simple_test_images()
        
        # 创建测试音频
        from pydub import AudioSegment
        audio = AudioSegment.silent(duration=5000)  # 5秒静音
        
        composer = EnhancedVideoComposer()
        output_path = config.OUTPUT_DIR / "test_enhanced_fade.mp4"
        
        # 测试淡入淡出效果
        video_path = composer.create_smooth_story_video(
            images, audio, str(output_path), "fade"
        )
        
        logger.info(f"✅ 增强版视频合成成功: {video_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 增强版视频合成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_story_diffusion_composer():
    """测试StoryDiffusion风格合成器"""
    logger.info("测试StoryDiffusion风格合成器...")
    
    try:
        images = create_simple_test_images()
        
        # 创建测试音频
        from pydub import AudioSegment
        audio = AudioSegment.silent(duration=8000)  # 8秒静音（插值会增加时长）
        
        composer = StoryDiffusionComposer()
        output_path = config.OUTPUT_DIR / "test_story_diffusion.mp4"
        
        video_path = composer.create_story_video(
            images, audio, str(output_path)
        )
        
        logger.info(f"✅ StoryDiffusion风格视频合成成功: {video_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ StoryDiffusion风格视频合成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎬 测试新的视频合成功能")
    print("="*50)
    
    # 确保输出目录存在
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 测试增强版合成器
    enhanced_success = test_enhanced_composer()
    
    # 测试StoryDiffusion合成器
    story_diffusion_success = test_story_diffusion_composer()
    
    print("\n" + "="*50)
    print("测试结果:")
    print(f"增强版视频合成器: {'✅ 成功' if enhanced_success else '❌ 失败'}")
    print(f"StoryDiffusion风格合成器: {'✅ 成功' if story_diffusion_success else '❌ 失败'}")
    
    if enhanced_success and story_diffusion_success:
        print("\n🎉 所有新功能测试通过！")
        print("您现在可以在Web界面中选择不同的视频风格了。")
    else:
        print("\n⚠️ 部分功能测试失败，请检查日志")


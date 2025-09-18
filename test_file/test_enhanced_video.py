#!/usr/bin/env python3
"""
测试增强版视频合成功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.enhanced_video_composer import EnhancedVideoComposer
from modules.story_diffusion_composer import StoryDiffusionComposer
from loguru import logger
import numpy as np
from PIL import Image

def create_test_images():
    """创建测试图片"""
    images = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    for i, color in enumerate(colors):
        # 创建纯色图片
        img = Image.new('RGB', (1080, 1920), color)
        # 添加文字
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            font = ImageFont.load_default()
        
        text = f"场景 {i+1}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1080 - text_width) // 2
        y = (1920 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        images.append(img)
    
    return images

def test_enhanced_video():
    """测试增强版视频合成"""
    logger.info("开始测试增强版视频合成...")
    
    try:
        # 创建测试图片
        images = create_test_images()
        logger.info(f"创建了 {len(images)} 张测试图片")
        
        # 创建测试音频
        from pydub import AudioSegment
        audio = AudioSegment.silent(duration=10000)  # 10秒静音
        
        # 测试不同的转场效果
        transition_types = ["fade", "slide", "zoom", "rotate", "wipe"]
        
        for transition_type in transition_types:
            logger.info(f"测试转场效果: {transition_type}")
            
            composer = EnhancedVideoComposer()
            output_path = config.OUTPUT_DIR / f"test_enhanced_{transition_type}.mp4"
            
            try:
                video_path = composer.create_smooth_story_video(
                    images, audio, str(output_path), transition_type
                )
                logger.info(f"✅ {transition_type} 转场效果测试成功: {video_path}")
            except Exception as e:
                logger.error(f"❌ {transition_type} 转场效果测试失败: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"增强版视频合成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_story_diffusion():
    """测试StoryDiffusion风格视频合成"""
    logger.info("开始测试StoryDiffusion风格视频合成...")
    
    try:
        # 创建测试图片
        images = create_test_images()
        logger.info(f"创建了 {len(images)} 张测试图片")
        
        # 创建测试音频
        from pydub import AudioSegment
        audio = AudioSegment.silent(duration=15000)  # 15秒静音（插值会增加时长）
        
        composer = StoryDiffusionComposer()
        output_path = config.OUTPUT_DIR / "test_story_diffusion.mp4"
        
        try:
            video_path = composer.create_story_video(
                images, audio, str(output_path)
            )
            logger.info(f"✅ StoryDiffusion风格视频测试成功: {video_path}")
            return True
        except Exception as e:
            logger.error(f"❌ StoryDiffusion风格视频测试失败: {e}")
            return False
        
    except Exception as e:
        logger.error(f"StoryDiffusion风格视频合成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始测试增强版视频合成功能...")
    
    # 确保输出目录存在
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 测试增强版视频合成
    enhanced_success = test_enhanced_video()
    
    # 测试StoryDiffusion风格
    story_diffusion_success = test_story_diffusion()
    
    print("\n" + "="*50)
    print("测试结果汇总:")
    print(f"增强版视频合成: {'✅ 成功' if enhanced_success else '❌ 失败'}")
    print(f"StoryDiffusion风格: {'✅ 成功' if story_diffusion_success else '❌ 失败'}")
    
    if enhanced_success and story_diffusion_success:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查日志")


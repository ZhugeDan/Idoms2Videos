#!/usr/bin/env python3
"""
视频风格演示脚本
展示不同视频合成风格的效果对比
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.enhanced_video_composer import EnhancedVideoComposer
from modules.story_diffusion_composer import StoryDiffusionComposer
from simple_video_composer import SimpleVideoComposer
from loguru import logger
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_demo_images():
    """创建演示用的成语故事图片"""
    images = []
    
    # 成语故事场景
    scenes = [
        "一个农夫在田里工作",
        "农夫发现一只兔子撞死在树桩上",
        "农夫捡起兔子，非常高兴",
        "农夫决定每天守在树桩旁等待兔子",
        "农夫荒废了田地，最终一无所获"
    ]
    
    # 创建渐变背景色
    colors = [
        (135, 206, 235),  # 天蓝色 - 田野
        (34, 139, 34),    # 森林绿 - 树桩
        (255, 215, 0),    # 金色 - 高兴
        (255, 165, 0),    # 橙色 - 等待
        (128, 128, 128)   # 灰色 - 失望
    ]
    
    for i, (scene, color) in enumerate(zip(scenes, colors)):
        # 创建图片
        img = Image.new('RGB', (1080, 1920), color)
        draw = ImageDraw.Draw(img)
        
        # 添加场景文字
        try:
            font_large = ImageFont.truetype("arial.ttf", 80)
            font_small = ImageFont.truetype("arial.ttf", 60)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 场景标题
        title = f"场景 {i+1}"
        bbox = draw.textbbox((0, 0), title, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (1080 - text_width) // 2
        y = 200
        draw.text((x, y), title, fill=(255, 255, 255), font=font_large)
        
        # 场景描述
        scene_text = scene
        bbox = draw.textbbox((0, 0), scene_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (1080 - text_width) // 2
        y = 400
        draw.text((x, y), scene_text, fill=(255, 255, 255), font=font_small)
        
        # 添加装饰性元素
        if i == 0:
            # 田野
            draw.ellipse([400, 800, 680, 1000], fill=(34, 139, 34), outline=(0, 100, 0), width=3)
        elif i == 1:
            # 树桩
            draw.rectangle([450, 700, 630, 1200], fill=(139, 69, 19), outline=(101, 67, 33), width=3)
        elif i == 2:
            # 兔子
            draw.ellipse([500, 800, 580, 900], fill=(255, 255, 255), outline=(200, 200, 200), width=2)
        elif i == 3:
            # 等待
            for j in range(5):
                x_pos = 200 + j * 150
                draw.ellipse([x_pos, 800, x_pos + 80, 880], fill=(255, 255, 255), outline=(200, 200, 200), width=2)
        else:
            # 失望
            draw.polygon([(400, 800), (500, 700), (600, 800), (500, 900)], fill=(100, 100, 100), outline=(50, 50, 50), width=3)
        
        images.append(img)
    
    return images

def demo_video_styles():
    """演示不同视频风格"""
    logger.info("开始演示不同视频风格...")
    
    try:
        # 创建演示图片
        images = create_demo_images()
        logger.info(f"创建了 {len(images)} 张演示图片")
        
        # 创建演示音频
        from pydub import AudioSegment
        audio = AudioSegment.silent(duration=12000)  # 12秒静音
        
        # 确保输出目录存在
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # 1. 简单拼接风格 (PPT风格)
        logger.info("生成简单拼接风格视频...")
        simple_composer = SimpleVideoComposer()
        simple_path = config.OUTPUT_DIR / "demo_simple_style.mp4"
        try:
            simple_composer.create_story_video(images, audio, str(simple_path))
            logger.info(f"✅ 简单拼接风格: {simple_path}")
        except Exception as e:
            logger.error(f"❌ 简单拼接风格失败: {e}")
        
        # 2. 增强转场风格 - 淡入淡出
        logger.info("生成增强转场风格视频 (淡入淡出)...")
        enhanced_composer = EnhancedVideoComposer()
        enhanced_path = config.OUTPUT_DIR / "demo_enhanced_fade.mp4"
        try:
            enhanced_composer.create_smooth_story_video(images, audio, str(enhanced_path), "fade")
            logger.info(f"✅ 增强转场风格 (淡入淡出): {enhanced_path}")
        except Exception as e:
            logger.error(f"❌ 增强转场风格失败: {e}")
        
        # 3. 增强转场风格 - 滑动
        logger.info("生成增强转场风格视频 (滑动)...")
        enhanced_slide_path = config.OUTPUT_DIR / "demo_enhanced_slide.mp4"
        try:
            enhanced_composer.create_smooth_story_video(images, audio, str(enhanced_slide_path), "slide")
            logger.info(f"✅ 增强转场风格 (滑动): {enhanced_slide_path}")
        except Exception as e:
            logger.error(f"❌ 增强转场风格 (滑动)失败: {e}")
        
        # 4. StoryDiffusion风格
        logger.info("生成StoryDiffusion风格视频...")
        story_composer = StoryDiffusionComposer()
        story_path = config.OUTPUT_DIR / "demo_story_diffusion.mp4"
        try:
            story_composer.create_story_video(images, audio, str(story_path))
            logger.info(f"✅ StoryDiffusion风格: {story_path}")
        except Exception as e:
            logger.error(f"❌ StoryDiffusion风格失败: {e}")
        
        logger.info("视频风格演示完成！")
        return True
        
    except Exception as e:
        logger.error(f"视频风格演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎬 视频风格演示")
    print("="*50)
    print("将生成以下风格的演示视频:")
    print("1. 简单拼接风格 (PPT风格)")
    print("2. 增强转场风格 (淡入淡出)")
    print("3. 增强转场风格 (滑动)")
    print("4. StoryDiffusion风格 (连贯动画)")
    print("="*50)
    
    success = demo_video_styles()
    
    if success:
        print("\n🎉 视频风格演示完成！")
        print(f"请查看 {config.OUTPUT_DIR} 目录中的演示视频")
        print("\n视频风格对比:")
        print("- 简单拼接: 快速，适合快速预览")
        print("- 增强转场: 顺滑过渡，视觉效果更好")
        print("- StoryDiffusion: 连贯动画，最接近专业效果")
    else:
        print("\n❌ 视频风格演示失败，请检查日志")


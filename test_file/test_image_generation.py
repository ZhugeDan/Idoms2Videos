#!/usr/bin/env python3
"""
测试图片生成模块
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.image_generator import ImageGenerator
from modules.scene_extractor import SceneExtractor
from loguru import logger
import streamlit as st

def test_image_generation():
    """测试图片生成功能"""
    try:
        logger.info("开始测试图片生成模块...")
        
        # 初始化图片生成器
        image_generator = ImageGenerator()
        logger.info("图片生成器初始化成功")
        
        # 测试单张图片生成
        test_prompt = "一个农夫在田地里工作，阳光明媚，卡通风格"
        logger.info(f"测试生成图片: {test_prompt}")
        
        image = image_generator.generate_image(test_prompt)
        if image:
            logger.info("单张图片生成成功")
            # 保存测试图片
            test_output_path = "test_image.jpg"
            image.save(test_output_path)
            logger.info(f"测试图片已保存到: {test_output_path}")
        else:
            logger.error("单张图片生成失败")
            return False
        
        # 测试批量图片生成
        test_scenes = [
            "一个农夫在田地里工作",
            "农夫发现了一只兔子",
            "农夫坐在树下等待",
            "农夫失望地离开"
        ]
        
        logger.info("测试批量图片生成...")
        images = image_generator.generate_story_images(test_scenes)
        
        if images and len(images) > 0:
            logger.info(f"批量图片生成成功，共生成 {len(images)} 张图片")
            
            # 保存所有测试图片
            for i, img in enumerate(images):
                output_path = f"test_image_{i+1}.jpg"
                img.save(output_path)
                logger.info(f"测试图片 {i+1} 已保存到: {output_path}")
            
            return True
        else:
            logger.error("批量图片生成失败")
            return False
            
    except Exception as e:
        logger.error(f"测试图片生成失败: {e}")
        return False
    finally:
        # 清理资源
        if 'image_generator' in locals():
            image_generator.cleanup()

def test_scene_extraction():
    """测试场景提取功能"""
    try:
        logger.info("开始测试场景提取模块...")
        
        # 初始化场景提取器
        scene_extractor = SceneExtractor()
        logger.info("场景提取器初始化成功")
        
        # 测试场景提取
        test_story = """
        从前有一个农夫，他每天都要到田地里去工作。有一天，他在田地里发现了一只兔子撞死在树桩上。
        农夫很高兴，心想：如果每天都有兔子撞死在这里，我就不用工作了。
        于是，农夫每天都坐在树桩旁边等待兔子撞死。但是再也没有兔子撞死了。
        农夫最终失望地离开了，他的田地也荒芜了。
        """
        
        logger.info("测试场景提取...")
        scenes = scene_extractor.extract_scenes(test_story, max_scenes=15)
        
        if scenes and len(scenes) > 0:
            logger.info(f"场景提取成功，共提取 {len(scenes)} 个场景")
            for i, scene in enumerate(scenes):
                logger.info(f"场景 {i+1}: {scene}")
            return scenes
        else:
            logger.error("场景提取失败")
            return None
            
    except Exception as e:
        logger.error(f"测试场景提取失败: {e}")
        return None

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("开始测试图片生成系统")
    logger.info("=" * 50)
    
    # 测试场景提取
    scenes = test_scene_extraction()
    if not scenes:
        logger.error("场景提取测试失败，退出")
        sys.exit(1)
    
    # 测试图片生成
    success = test_image_generation()
    if success:
        logger.info("=" * 50)
        logger.info("所有测试通过！图片生成模块工作正常")
        logger.info("=" * 50)
    else:
        logger.error("=" * 50)
        logger.error("测试失败！图片生成模块存在问题")
        logger.error("=" * 50)
        sys.exit(1)

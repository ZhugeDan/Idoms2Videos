#!/usr/bin/env python3
"""
测试输出文件结构
"""
import sys
import os
import warnings
from pathlib import Path

# 抑制警告信息
warnings.filterwarnings("ignore", message="A matching Triton is not available")
warnings.filterwarnings("ignore", message="torch_dtype is deprecated")
warnings.filterwarnings("ignore", message="Couldn't connect to the Hub")
warnings.filterwarnings("ignore", message="Token indices sequence length is longer than")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from modules.image_generator import ImageGenerator
from modules.scene_extractor import SceneExtractor
from loguru import logger

def test_output_structure():
    """测试输出文件结构"""
    try:
        logger.info("开始测试输出文件结构...")
        
        # 创建必要的目录
        config.create_directories()
        logger.info("目录创建完成")
        
        # 检查目录是否存在
        directories = [
            config.OUTPUT_DIR,
            config.OUTPUT_PIC_DIR,
            config.TEMP_DIR,
            config.CACHE_DIR,
            config.LOG_DIR
        ]
        
        for directory in directories:
            if directory.exists():
                logger.info(f"✅ 目录存在: {directory}")
            else:
                logger.error(f"❌ 目录不存在: {directory}")
                return False
        
        # 测试图片生成和保存
        logger.info("测试图片生成和保存...")
        
        # 初始化组件
        scene_extractor = SceneExtractor()
        image_generator = ImageGenerator()
        
        # 测试场景提取
        test_story = "从前有一个农夫，他每天都要到田地里去工作。有一天，他在田地里发现了一只兔子撞死在树桩上。"
        scenes = scene_extractor.extract_scenes(test_story, max_scenes=3)
        
        if not scenes:
            logger.error("场景提取失败")
            return False
        
        logger.info(f"场景提取成功，共 {len(scenes)} 个场景")
        
        # 生成图片
        images = image_generator.generate_story_images(scenes)
        
        if not images:
            logger.error("图片生成失败")
            return False
        
        logger.info(f"图片生成成功，共 {len(images)} 张")
        
        # 保存图片到output_pic文件夹
        idiom = "守株待兔"
        saved_paths = []
        
        for i, image in enumerate(images):
            filename = f"{idiom}_{i+1:02d}.jpg"
            output_path = config.OUTPUT_PIC_DIR / filename
            
            image.save(output_path, quality=95)
            saved_paths.append(output_path)
            
            logger.info(f"图片已保存: {output_path}")
        
        # 验证文件是否保存成功
        for path in saved_paths:
            if path.exists():
                file_size = path.stat().st_size
                logger.info(f"✅ 文件验证成功: {path.name} ({file_size} bytes)")
            else:
                logger.error(f"❌ 文件保存失败: {path}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"测试输出结构失败: {e}")
        return False
    finally:
        # 清理资源
        if 'image_generator' in locals():
            image_generator.cleanup()

def show_directory_structure():
    """显示目录结构"""
    logger.info("=" * 60)
    logger.info("项目目录结构")
    logger.info("=" * 60)
    
    base_dir = Path(__file__).parent
    
    directories = {
        "output": "视频输出目录",
        "output_pic": "图片输出目录", 
        "temp": "临时文件目录",
        "cache": "缓存目录",
        "logs": "日志目录",
        "models": "模型目录"
    }
    
    for dir_name, description in directories.items():
        dir_path = base_dir / dir_name
        if dir_path.exists():
            file_count = len(list(dir_path.iterdir()))
            logger.info(f"📁 {dir_name}/ - {description} ({file_count} 个文件)")
        else:
            logger.info(f"📁 {dir_name}/ - {description} (不存在)")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("输出文件结构测试")
    logger.info("=" * 60)
    
    # 显示目录结构
    show_directory_structure()
    
    # 测试输出结构
    success = test_output_structure()
    
    if success:
        logger.info("=" * 60)
        logger.info("🎉 输出文件结构测试通过！")
        logger.info("✅ 所有目录创建成功")
        logger.info("✅ 图片保存功能正常")
        logger.info("✅ 文件命名规范正确")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("❌ 输出文件结构测试失败！")
        logger.error("=" * 60)
        sys.exit(1)


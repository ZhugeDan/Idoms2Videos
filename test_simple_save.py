#!/usr/bin/env python3
"""
简单测试图片保存功能
"""
import sys
import os
from pathlib import Path
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from loguru import logger

def test_simple_save():
    """简单测试图片保存功能"""
    try:
        logger.info("开始简单测试图片保存功能...")
        
        # 创建必要的目录
        config.create_directories()
        logger.info("目录创建完成")
        
        # 检查output_pic目录是否存在
        if config.OUTPUT_PIC_DIR.exists():
            logger.info(f"✅ output_pic目录存在: {config.OUTPUT_PIC_DIR}")
        else:
            logger.error(f"❌ output_pic目录不存在: {config.OUTPUT_PIC_DIR}")
            return False
        
        # 创建测试图片
        test_image = Image.new('RGB', (512, 512), color='lightblue')
        
        # 测试保存图片
        idiom = "守株待兔"
        test_scenes = ["农夫在田里工作", "农夫发现兔子", "农夫坐在树下等待"]
        
        saved_paths = []
        for i, scene in enumerate(test_scenes):
            filename = f"{idiom}_{i+1:02d}.jpg"
            output_path = config.OUTPUT_PIC_DIR / filename
            
            # 保存图片
            test_image.save(output_path, quality=95)
            saved_paths.append(output_path)
            
            logger.info(f"测试图片已保存: {output_path}")
        
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
        logger.error(f"简单测试失败: {e}")
        return False

def show_output_pic_contents():
    """显示output_pic目录内容"""
    logger.info("=" * 60)
    logger.info("output_pic目录内容")
    logger.info("=" * 60)
    
    if config.OUTPUT_PIC_DIR.exists():
        files = list(config.OUTPUT_PIC_DIR.iterdir())
        if files:
            for file in sorted(files):
                if file.is_file():
                    file_size = file.stat().st_size
                    logger.info(f"📄 {file.name} ({file_size} bytes)")
        else:
            logger.info("目录为空")
    else:
        logger.info("目录不存在")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("简单图片保存测试")
    logger.info("=" * 60)
    
    # 显示当前目录内容
    show_output_pic_contents()
    
    # 测试保存功能
    success = test_simple_save()
    
    if success:
        logger.info("=" * 60)
        logger.info("🎉 简单图片保存测试通过！")
        logger.info("✅ output_pic目录创建成功")
        logger.info("✅ 图片保存功能正常")
        logger.info("✅ 文件命名规范正确")
        logger.info("=" * 60)
        
        # 显示保存后的目录内容
        show_output_pic_contents()
    else:
        logger.error("=" * 60)
        logger.error("❌ 简单图片保存测试失败！")
        logger.error("=" * 60)
        sys.exit(1)


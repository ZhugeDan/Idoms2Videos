#!/usr/bin/env python3
"""
安全的GPU测试脚本
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.image_generator import ImageGenerator
from loguru import logger

def test_gpu_safe():
    """安全的GPU测试"""
    try:
        logger.info("开始安全GPU测试...")
        
        # 初始化图片生成器
        image_generator = ImageGenerator()
        logger.info("图片生成器初始化成功")
        
        # 使用简短的提示词测试
        test_prompt = "农夫在田里工作"
        logger.info(f"测试生成图片: {test_prompt}")
        
        start_time = time.time()
        image = image_generator.generate_image(test_prompt)
        end_time = time.time()
        
        if image:
            generation_time = end_time - start_time
            logger.info(f"单张图片生成成功，耗时: {generation_time:.2f}秒")
            
            # 保存测试图片
            test_output_path = "gpu_safe_test.jpg"
            image.save(test_output_path)
            logger.info(f"测试图片已保存到: {test_output_path}")
            
            return generation_time
        else:
            logger.error("单张图片生成失败")
            return None
            
    except Exception as e:
        logger.error(f"安全GPU测试失败: {e}")
        return None
    finally:
        # 清理资源
        if 'image_generator' in locals():
            image_generator.cleanup()

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("安全GPU测试")
    logger.info("=" * 60)
    
    # 测试GPU
    generation_time = test_gpu_safe()
    
    if generation_time:
        logger.info("=" * 60)
        logger.info(f"安全GPU测试完成！生成时间: {generation_time:.2f}秒")
        if generation_time < 10:
            logger.info("🚀 GPU加速效果极佳！")
        elif generation_time < 30:
            logger.info("✅ GPU加速效果良好")
        elif generation_time < 60:
            logger.info("⚠️ GPU加速效果一般")
        else:
            logger.info("🐌 GPU加速效果较差，可能需要进一步优化")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("安全GPU测试失败！")
        logger.error("=" * 60)
        sys.exit(1)





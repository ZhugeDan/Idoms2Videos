#!/usr/bin/env python3
"""
高性能GPU测试脚本
"""
import sys
import os
import time
import warnings

# 抑制警告信息
warnings.filterwarnings("ignore", message="A matching Triton is not available")
warnings.filterwarnings("ignore", message="torch_dtype is deprecated")
warnings.filterwarnings("ignore", message="Couldn't connect to the Hub")
warnings.filterwarnings("ignore", message="Token indices sequence length is longer than")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.image_generator import ImageGenerator
from loguru import logger

def test_high_performance():
    """测试高性能GPU生成"""
    try:
        logger.info("开始高性能GPU测试...")
        
        # 初始化图片生成器
        image_generator = ImageGenerator()
        logger.info("图片生成器初始化成功")
        
        # 测试单张图片生成速度
        test_prompt = "农夫在田里工作"
        logger.info(f"测试生成图片: {test_prompt}")
        
        start_time = time.time()
        image = image_generator.generate_image(test_prompt)
        end_time = time.time()
        
        if image:
            generation_time = end_time - start_time
            logger.info(f"单张图片生成成功，耗时: {generation_time:.2f}秒")
            
            # 保存测试图片
            test_output_path = "high_performance_test.jpg"
            image.save(test_output_path)
            logger.info(f"测试图片已保存到: {test_output_path}")
            
            # 测试批量生成速度
            logger.info("测试批量图片生成...")
            test_scenes = [
                "农夫在田里工作",
                "农夫发现兔子",
                "农夫坐在树下等待"
            ]
            
            start_time = time.time()
            images = image_generator.generate_story_images(test_scenes)
            end_time = time.time()
            
            if images and len(images) > 0:
                batch_time = end_time - start_time
                avg_time = batch_time / len(images)
                logger.info(f"批量图片生成成功，共 {len(images)} 张")
                logger.info(f"总耗时: {batch_time:.2f}秒")
                logger.info(f"平均每张: {avg_time:.2f}秒")
                
                # 保存批量图片
                for i, img in enumerate(images):
                    output_path = f"high_performance_batch_{i+1}.jpg"
                    img.save(output_path)
                    logger.info(f"批量图片 {i+1} 已保存到: {output_path}")
                
                return generation_time, avg_time
            else:
                logger.error("批量图片生成失败")
                return generation_time, None
        else:
            logger.error("单张图片生成失败")
            return None, None
            
    except Exception as e:
        logger.error(f"高性能测试失败: {e}")
        return None, None
    finally:
        # 清理资源
        if 'image_generator' in locals():
            image_generator.cleanup()

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("高性能GPU测试")
    logger.info("=" * 60)
    
    # 测试高性能生成
    single_time, avg_time = test_high_performance()
    
    if single_time:
        logger.info("=" * 60)
        logger.info(f"高性能测试完成！")
        logger.info(f"单张图片生成时间: {single_time:.2f}秒")
        
        if avg_time:
            logger.info(f"批量平均生成时间: {avg_time:.2f}秒")
            
            # 性能评估
            if avg_time < 15:
                logger.info("🚀 性能极佳！GPU利用率应该很高")
            elif avg_time < 25:
                logger.info("✅ 性能良好！GPU利用率较高")
            elif avg_time < 40:
                logger.info("⚠️ 性能一般，GPU利用率中等")
            else:
                logger.info("🐌 性能较差，GPU利用率较低")
        
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("高性能测试失败！")
        logger.error("=" * 60)
        sys.exit(1)


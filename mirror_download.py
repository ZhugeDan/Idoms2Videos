"""
使用镜像站点下载Stable Diffusion模型
"""
import os
import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline
from loguru import logger

def download_from_mirror():
    """从镜像站点下载模型"""
    try:
        logger.info("使用镜像站点下载模型...")
        
        # 设置镜像环境变量
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        logger.info("使用 Hugging Face 镜像站点: https://hf-mirror.com")
        
        # 下载模型
        pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="./models",
            local_files_only=False,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        logger.success("镜像下载完成")
        return True
        
    except Exception as e:
        logger.error(f"镜像下载失败: {e}")
        return False

def test_model_loading():
    """测试模型加载"""
    try:
        logger.info("测试模型加载...")
        
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        # 加载模型
        pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="./models",
            local_files_only=True,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        logger.success("模型加载测试成功")
        return True
        
    except Exception as e:
        logger.error(f"模型加载测试失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始使用镜像站点下载模型...")
    
    if download_from_mirror():
        if test_model_loading():
            logger.success("✅ 模型下载并测试成功！")
            return True
    
    logger.error("❌ 镜像下载失败")
    logger.info("其他解决方案:")
    logger.info("1. 检查网络连接")
    logger.info("2. 尝试使用VPN")
    logger.info("3. 手动下载模型文件")
    logger.info("4. 使用其他镜像站点")
    
    return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.success("现在可以正常使用应用了！")
    else:
        logger.error("请尝试其他解决方案。")

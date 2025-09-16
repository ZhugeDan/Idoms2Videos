"""
断点续传下载Stable Diffusion模型
"""
import os
import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline
from loguru import logger
import time

def resume_download_with_retry():
    """使用断点续传重新下载模型"""
    try:
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        
        # 禁用符号链接警告
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        logger.info("开始断点续传下载Stable Diffusion模型...")
        logger.info("如果网络中断，可以重新运行此脚本继续下载")
        
        # 使用断点续传下载
        pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="./models",
            local_files_only=False,
            resume_download=True,  # 启用断点续传
            safety_checker=None,
            requires_safety_checker=False
        )
        
        logger.success("模型下载完成")
        return True
        
    except Exception as e:
        logger.error(f"下载失败: {e}")
        logger.info("可以重新运行此脚本继续下载")
        return False

def check_download_progress():
    """检查下载进度"""
    model_dir = Path("./models/models--runwayml--stable-diffusion-v1-5")
    
    if not model_dir.exists():
        logger.info("模型目录不存在，需要开始下载")
        return False
    
    # 检查不完整的文件
    incomplete_files = list(model_dir.glob("**/*.incomplete"))
    if incomplete_files:
        logger.info(f"发现 {len(incomplete_files)} 个未完成的文件，可以继续下载")
        return False
    
    # 检查关键文件
    snapshot_dir = model_dir / "snapshots"
    if not snapshot_dir.exists():
        logger.info("快照目录不存在，需要继续下载")
        return False
    
    snapshots = list(snapshot_dir.iterdir())
    if not snapshots:
        logger.info("没有找到模型快照，需要继续下载")
        return False
    
    latest_snapshot = snapshots[0]
    required_files = [
        "model_index.json",
        "unet/diffusion_pytorch_model.safetensors",
        "vae/diffusion_pytorch_model.safetensors",
        "text_encoder/pytorch_model.bin",
        "safety_checker/pytorch_model.bin"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (latest_snapshot / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.info(f"缺少 {len(missing_files)} 个关键文件，需要继续下载")
        return False
    
    logger.success("模型下载完整")
    return True

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
    logger.info("开始断点续传下载...")
    
    # 步骤1: 检查当前下载状态
    logger.info("步骤1: 检查下载状态")
    if check_download_progress():
        logger.success("模型已完整，无需下载")
        if test_model_loading():
            logger.success("模型工作正常")
            return True
    
    # 步骤2: 断点续传下载
    logger.info("步骤2: 断点续传下载")
    max_retries = 3
    for attempt in range(max_retries):
        logger.info(f"尝试第 {attempt + 1}/{max_retries} 次下载")
        
        if resume_download_with_retry():
            # 验证下载完整性
            if check_download_progress():
                if test_model_loading():
                    logger.success("下载完成并验证成功")
                    return True
        
        if attempt < max_retries - 1:
            logger.info(f"第 {attempt + 1} 次尝试失败，等待 10 秒后重试...")
            time.sleep(10)
    
    logger.error("多次尝试后下载仍然失败")
    logger.info("建议:")
    logger.info("1. 检查网络连接")
    logger.info("2. 尝试使用VPN")
    logger.info("3. 手动下载模型文件")
    return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.success("问题解决完成！现在可以正常使用应用了。")
    else:
        logger.error("下载失败，请检查网络连接或尝试其他解决方案。")

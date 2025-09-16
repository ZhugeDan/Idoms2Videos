"""
清理不完整的模型文件并重新下载
"""
import os
import shutil
import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline
from loguru import logger

def clean_incomplete_files():
    """清理不完整的下载文件"""
    model_dir = Path("./models/models--runwayml--stable-diffusion-v1-5")
    
    if not model_dir.exists():
        logger.info("模型目录不存在，无需清理")
        return True
    
    # 删除所有.incomplete文件
    incomplete_files = list(model_dir.glob("**/*.incomplete"))
    logger.info(f"找到 {len(incomplete_files)} 个不完整的文件")
    
    for file in incomplete_files:
        try:
            file.unlink()
            logger.info(f"已删除: {file}")
        except Exception as e:
            logger.warning(f"删除失败 {file}: {e}")
    
    return True

def download_model_completely():
    """完全重新下载模型"""
    try:
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        
        # 删除现有模型目录
        model_dir = Path("./models/models--runwayml--stable-diffusion-v1-5")
        if model_dir.exists():
            logger.info("删除现有模型目录...")
            shutil.rmtree(model_dir)
        
        logger.info("开始重新下载Stable Diffusion模型...")
        
        # 下载模型
        pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="./models",
            local_files_only=False,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        logger.success("模型下载完成")
        return True
        
    except Exception as e:
        logger.error(f"下载模型失败: {e}")
        return False

def verify_model_integrity():
    """验证模型完整性"""
    model_dir = Path("./models/models--runwayml--stable-diffusion-v1-5")
    
    if not model_dir.exists():
        logger.error("模型目录不存在")
        return False
    
    # 检查是否有不完整的文件
    incomplete_files = list(model_dir.glob("**/*.incomplete"))
    if incomplete_files:
        logger.error(f"仍有 {len(incomplete_files)} 个不完整的文件")
        return False
    
    # 检查关键文件
    snapshot_dir = model_dir / "snapshots"
    if not snapshot_dir.exists():
        logger.error("快照目录不存在")
        return False
    
    snapshots = list(snapshot_dir.iterdir())
    if not snapshots:
        logger.error("没有找到模型快照")
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
        logger.error(f"缺少关键文件: {missing_files}")
        return False
    
    logger.success("模型完整性验证通过")
    return True

def test_model_loading():
    """测试模型加载"""
    try:
        logger.info("测试模型加载...")
        
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        
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
    logger.info("开始清理和重新下载模型...")
    
    # 步骤1: 清理不完整的文件
    logger.info("步骤1: 清理不完整的文件")
    clean_incomplete_files()
    
    # 步骤2: 重新下载模型
    logger.info("步骤2: 重新下载模型")
    if not download_model_completely():
        logger.error("模型下载失败")
        return False
    
    # 步骤3: 验证模型完整性
    logger.info("步骤3: 验证模型完整性")
    if not verify_model_integrity():
        logger.error("模型完整性验证失败")
        return False
    
    # 步骤4: 测试模型加载
    logger.info("步骤4: 测试模型加载")
    if not test_model_loading():
        logger.error("模型加载测试失败")
        return False
    
    logger.success("所有步骤完成，模型已准备就绪！")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        logger.success("问题解决完成！现在可以正常使用应用了。")
    else:
        logger.error("问题解决失败，请检查网络连接或尝试手动下载模型。")


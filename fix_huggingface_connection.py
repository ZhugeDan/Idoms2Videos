"""
解决Hugging Face连接超时问题的脚本
"""
import os
import sys
import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline
from loguru import logger

def check_model_status():
    """检查模型下载状态"""
    model_dir = Path("./models/models--runwayml--stable-diffusion-v1-5")
    
    if not model_dir.exists():
        logger.error("模型目录不存在")
        return False
    
    # 检查是否有未完成的下载
    incomplete_files = list(model_dir.glob("**/*.incomplete"))
    if incomplete_files:
        logger.warning(f"发现 {len(incomplete_files)} 个未完成的下载文件")
        for file in incomplete_files:
            logger.warning(f"未完成文件: {file}")
        return False
    
    # 检查关键文件是否存在
    snapshot_dir = model_dir / "snapshots"
    if not snapshot_dir.exists():
        logger.error("快照目录不存在")
        return False
    
    # 查找最新的快照
    snapshots = list(snapshot_dir.iterdir())
    if not snapshots:
        logger.error("没有找到模型快照")
        return False
    
    latest_snapshot = snapshots[0]  # 通常只有一个快照
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
    
    logger.success("模型文件完整")
    return True

def download_model_with_retry():
    """重试下载模型"""
    try:
        logger.info("开始下载Stable Diffusion模型...")
        
        # 设置环境变量以使用本地缓存
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        
        # 尝试下载模型
        model_path = "runwayml/stable-diffusion-v1-5"
        cache_dir = "./models"
        
        logger.info(f"下载模型到: {cache_dir}")
        
        # 使用torch_dtype=torch.float16以节省空间
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            cache_dir=cache_dir,
            local_files_only=False,  # 允许从网络下载
            resume_download=True     # 恢复未完成的下载
        )
        
        logger.success("模型下载完成")
        return True
        
    except Exception as e:
        logger.error(f"下载模型失败: {e}")
        return False

def create_local_model_config():
    """创建本地模型配置"""
    # 检查是否有完整的本地模型
    model_dir = Path("./models/models--runwayml--stable-diffusion-v1-5/snapshots")
    
    if not model_dir.exists():
        logger.error("本地模型目录不存在")
        return None
    
    # 找到最新的快照目录
    snapshots = list(model_dir.iterdir())
    if not snapshots:
        logger.error("没有找到模型快照")
        return None
    
    latest_snapshot = snapshots[0]
    local_model_path = str(latest_snapshot.absolute())
    
    logger.info(f"找到本地模型路径: {local_model_path}")
    return local_model_path

def test_local_model_loading(local_path):
    """测试本地模型加载"""
    try:
        logger.info("测试本地模型加载...")
        
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        
        # 尝试加载本地模型
        pipeline = StableDiffusionPipeline.from_pretrained(
            local_path,
            torch_dtype=torch.float16,
            local_files_only=True,  # 只使用本地文件
            safety_checker=None,
            requires_safety_checker=False
        )
        
        logger.success("本地模型加载成功")
        return True
        
    except Exception as e:
        logger.error(f"本地模型加载失败: {e}")
        return False

def update_config_file(local_path):
    """更新配置文件使用本地路径"""
    config_file = Path("config.py")
    
    if not config_file.exists():
        logger.error("配置文件不存在")
        return False
    
    try:
        # 读取配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换模型路径
        old_line = "SD_MODEL_PATH = os.getenv('SD_MODEL_PATH', 'runwayml/stable-diffusion-v1-5')"
        new_line = f"SD_MODEL_PATH = os.getenv('SD_MODEL_PATH', '{local_path}')"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # 写回文件
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.success("配置文件已更新")
            return True
        else:
            logger.warning("未找到需要替换的配置行")
            return False
            
    except Exception as e:
        logger.error(f"更新配置文件失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始解决Hugging Face连接问题...")
    
    # 步骤1: 检查当前模型状态
    logger.info("步骤1: 检查模型状态")
    if check_model_status():
        logger.success("模型已完整，无需下载")
        local_path = create_local_model_config()
        if local_path and test_local_model_loading(local_path):
            logger.success("本地模型工作正常")
            return True
    
    # 步骤2: 尝试重新下载模型
    logger.info("步骤2: 尝试重新下载模型")
    if download_model_with_retry():
        if check_model_status():
            local_path = create_local_model_config()
            if local_path and test_local_model_loading(local_path):
                logger.success("模型下载并测试成功")
                return True
    
    # 步骤3: 提供手动解决方案
    logger.warning("自动下载失败，请尝试手动解决方案:")
    logger.info("1. 访问 https://huggingface.co/runwayml/stable-diffusion-v1-5")
    logger.info("2. 点击 'Files and versions' 标签")
    logger.info("3. 下载所有文件到 ./models/stable-diffusion-v1-5/ 目录")
    logger.info("4. 运行此脚本再次测试")
    
    return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.success("问题解决完成！")
    else:
        logger.error("问题解决失败，请查看上述建议")


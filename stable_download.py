"""
稳定的模型下载脚本 - 使用多种策略确保下载成功
"""
import os
import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline
from loguru import logger
import time
import requests
from huggingface_hub import hf_hub_download, snapshot_download

def download_with_hf_hub():
    """使用huggingface_hub直接下载"""
    try:
        logger.info("方法1: 使用huggingface_hub直接下载...")
        
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        # 使用snapshot_download下载整个模型
        model_path = snapshot_download(
            repo_id="runwayml/stable-diffusion-v1-5",
            cache_dir="./models",
            local_files_only=False,
            resume_download=True
        )
        
        logger.success(f"模型下载完成: {model_path}")
        return True
        
    except Exception as e:
        logger.error(f"huggingface_hub下载失败: {e}")
        return False

def download_with_diffusers():
    """使用diffusers库下载"""
    try:
        logger.info("方法2: 使用diffusers库下载...")
        
        # 设置环境变量
        os.environ['HF_HOME'] = str(Path.cwd() / 'models')
        os.environ['TRANSFORMERS_CACHE'] = str(Path.cwd() / 'models')
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        # 使用diffusers下载
        pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="./models",
            local_files_only=False,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        logger.success("diffusers下载完成")
        return True
        
    except Exception as e:
        logger.error(f"diffusers下载失败: {e}")
        return False

def download_with_requests():
    """使用requests手动下载关键文件"""
    try:
        logger.info("方法3: 使用requests手动下载...")
        
        # 创建模型目录
        model_dir = Path("./models/stable-diffusion-v1-5")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 关键文件列表
        files_to_download = [
            "model_index.json",
            "unet/diffusion_pytorch_model.safetensors",
            "vae/diffusion_pytorch_model.safetensors", 
            "text_encoder/pytorch_model.bin",
            "safety_checker/pytorch_model.bin",
            "scheduler/scheduler_config.json",
            "tokenizer/tokenizer_config.json",
            "tokenizer/vocab.json",
            "tokenizer/merges.txt",
            "feature_extractor/preprocessor_config.json"
        ]
        
        base_url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/"
        
        for file_path in files_to_download:
            try:
                logger.info(f"下载: {file_path}")
                
                # 创建子目录
                file_dir = model_dir / Path(file_path).parent
                file_dir.mkdir(parents=True, exist_ok=True)
                
                # 下载文件
                url = base_url + file_path
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                # 保存文件
                with open(model_dir / file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"✓ {file_path} 下载完成")
                
            except Exception as e:
                logger.warning(f"下载 {file_path} 失败: {e}")
                continue
        
        logger.success("手动下载完成")
        return True
        
    except Exception as e:
        logger.error(f"手动下载失败: {e}")
        return False

def verify_model():
    """验证模型完整性"""
    model_dir = Path("./models")
    
    # 查找模型目录
    if (model_dir / "stable-diffusion-v1-5").exists():
        model_path = model_dir / "stable-diffusion-v1-5"
    elif (model_dir / "models--runwayml--stable-diffusion-v1-5").exists():
        # 查找快照目录
        snapshots_dir = model_dir / "models--runwayml--stable-diffusion-v1-5" / "snapshots"
        if snapshots_dir.exists():
            snapshots = list(snapshots_dir.iterdir())
            if snapshots:
                model_path = snapshots[0]
            else:
                logger.error("没有找到模型快照")
                return False
        else:
            logger.error("没有找到快照目录")
            return False
    else:
        logger.error("没有找到模型目录")
        return False
    
    logger.info(f"验证模型路径: {model_path}")
    
    # 检查关键文件
    required_files = [
        "model_index.json",
        "unet/diffusion_pytorch_model.safetensors",
        "vae/diffusion_pytorch_model.safetensors",
        "text_encoder/pytorch_model.bin",
        "safety_checker/pytorch_model.bin"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (model_path / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"缺少关键文件: {missing_files}")
        return False
    
    logger.success("模型验证通过")
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
    logger.info("开始稳定下载Stable Diffusion模型...")
    
    # 尝试多种下载方法
    download_methods = [
        ("huggingface_hub", download_with_hf_hub),
        ("diffusers", download_with_diffusers),
        ("requests", download_with_requests)
    ]
    
    for method_name, method_func in download_methods:
        logger.info(f"尝试方法: {method_name}")
        
        try:
            if method_func():
                # 验证模型
                if verify_model():
                    # 测试加载
                    if test_model_loading():
                        logger.success(f"使用 {method_name} 方法下载成功！")
                        return True
                    else:
                        logger.warning(f"{method_name} 下载完成但加载失败")
                else:
                    logger.warning(f"{method_name} 下载完成但验证失败")
            else:
                logger.warning(f"{method_name} 下载失败")
        except Exception as e:
            logger.error(f"{method_name} 出现异常: {e}")
        
        # 等待一下再尝试下一个方法
        time.sleep(2)
    
    logger.error("所有下载方法都失败了")
    logger.info("建议:")
    logger.info("1. 检查网络连接")
    logger.info("2. 尝试使用VPN")
    logger.info("3. 手动从 https://huggingface.co/runwayml/stable-diffusion-v1-5 下载")
    return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.success("模型下载完成！现在可以正常使用应用了。")
    else:
        logger.error("模型下载失败，请尝试其他解决方案。")

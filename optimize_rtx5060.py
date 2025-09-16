#!/usr/bin/env python3
"""
RTX 5060显卡优化配置
"""
import torch
import os
from loguru import logger

def check_rtx5060_compatibility():
    """检查RTX 5060兼容性"""
    try:
        if not torch.cuda.is_available():
            logger.error("CUDA不可用")
            return False
        
        # 获取GPU信息
        gpu_name = torch.cuda.get_device_name(0)
        cuda_capability = torch.cuda.get_device_capability(0)
        cuda_version = torch.version.cuda
        torch_version = torch.__version__
        
        logger.info(f"GPU: {gpu_name}")
        logger.info(f"CUDA计算能力: {cuda_capability}")
        logger.info(f"CUDA版本: {cuda_version}")
        logger.info(f"PyTorch版本: {torch_version}")
        
        # RTX 5060是Ada Lovelace架构，计算能力为8.9
        if "RTX 5060" in gpu_name or cuda_capability[0] >= 8:
            logger.info("检测到RTX 5060或兼容显卡")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"检查GPU兼容性失败: {e}")
        return False

def test_cuda_operations():
    """测试CUDA操作"""
    try:
        logger.info("测试CUDA基本操作...")
        
        # 测试基本张量操作
        x = torch.randn(1000, 1000).cuda()
        y = torch.randn(1000, 1000).cuda()
        z = torch.mm(x, y)
        
        logger.info("CUDA基本操作测试成功")
        
        # 测试内存使用
        memory_allocated = torch.cuda.memory_allocated(0) / 1024**3
        memory_reserved = torch.cuda.memory_reserved(0) / 1024**3
        
        logger.info(f"GPU内存使用: {memory_allocated:.2f}GB / {memory_reserved:.2f}GB")
        
        # 清理内存
        del x, y, z
        torch.cuda.empty_cache()
        
        return True
        
    except Exception as e:
        logger.error(f"CUDA操作测试失败: {e}")
        return False

def optimize_for_rtx5060():
    """为RTX 5060优化配置"""
    try:
        logger.info("开始RTX 5060优化配置...")
        
        # 设置环境变量
        os.environ['CUDA_LAUNCH_BLOCKING'] = '1'  # 同步CUDA操作，便于调试
        os.environ['TORCH_USE_CUDA_DSA'] = '1'   # 启用设备端断言
        
        # 设置内存管理
        torch.cuda.empty_cache()
        
        # 设置内存分配策略
        torch.cuda.set_per_process_memory_fraction(0.8)  # 使用80%显存
        
        logger.info("RTX 5060优化配置完成")
        return True
        
    except Exception as e:
        logger.error(f"优化配置失败: {e}")
        return False

def test_stable_diffusion_cuda():
    """测试Stable Diffusion CUDA支持"""
    try:
        logger.info("测试Stable Diffusion CUDA支持...")
        
        from diffusers import StableDiffusionPipeline
        import torch
        
        # 使用较小的模型进行测试
        model_id = "runwayml/stable-diffusion-v1-5"
        
        # 创建管道
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,  # 使用半精度以节省显存
            safety_checker=None,
            requires_safety_checker=False,
            cache_dir="./models"
        )
        
        # 移动到GPU
        pipe = pipe.to("cuda")
        
        # 启用内存优化
        pipe.enable_attention_slicing()
        pipe.enable_sequential_cpu_offload()
        
        logger.info("Stable Diffusion CUDA支持测试成功")
        
        # 清理
        del pipe
        torch.cuda.empty_cache()
        
        return True
        
    except Exception as e:
        logger.error(f"Stable Diffusion CUDA测试失败: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("RTX 5060显卡优化诊断")
    logger.info("=" * 60)
    
    # 检查兼容性
    if not check_rtx5060_compatibility():
        logger.error("RTX 5060兼容性检查失败")
        exit(1)
    
    # 测试CUDA操作
    if not test_cuda_operations():
        logger.error("CUDA操作测试失败")
        exit(1)
    
    # 优化配置
    if not optimize_for_rtx5060():
        logger.error("优化配置失败")
        exit(1)
    
    # 测试Stable Diffusion
    if not test_stable_diffusion_cuda():
        logger.error("Stable Diffusion CUDA测试失败")
        exit(1)
    
    logger.info("=" * 60)
    logger.info("RTX 5060优化完成！现在可以使用GPU加速了")
    logger.info("=" * 60)


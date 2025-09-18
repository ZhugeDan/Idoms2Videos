#!/usr/bin/env python3
"""
GPU利用率优化器
"""
import torch
import os
from loguru import logger

def optimize_gpu_performance():
    """优化GPU性能设置"""
    try:
        logger.info("开始GPU性能优化...")
        
        # 1. 设置CUDA优化环境变量
        os.environ['CUDA_LAUNCH_BLOCKING'] = '0'  # 异步执行，提高吞吐量
        os.environ['TORCH_USE_CUDA_DSA'] = '0'    # 禁用设备端断言，提高性能
        os.environ['CUDA_CACHE_DISABLE'] = '0'    # 启用CUDA缓存
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'  # 优化内存分配
        
        # 2. 设置PyTorch优化
        torch.backends.cudnn.benchmark = True     # 启用cuDNN自动调优
        torch.backends.cudnn.deterministic = False # 允许非确定性算法，提高性能
        torch.backends.cuda.matmul.allow_tf32 = True  # 启用TF32，提高性能
        torch.backends.cudnn.allow_tf32 = True    # 启用cuDNN TF32
        
        # 3. 设置内存管理
        if torch.cuda.is_available():
            # 设置更高的内存使用率
            torch.cuda.set_per_process_memory_fraction(0.95)  # 使用95%显存
            torch.cuda.empty_cache()
            
            # 获取GPU信息
            gpu_name = torch.cuda.get_device_name(0)
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"GPU: {gpu_name}")
            logger.info(f"总显存: {total_memory:.2f}GB")
            logger.info(f"显存使用率: 95%")
        
        logger.info("GPU性能优化完成")
        return True
        
    except Exception as e:
        logger.error(f"GPU性能优化失败: {e}")
        return False

def test_gpu_utilization():
    """测试GPU利用率"""
    try:
        if not torch.cuda.is_available():
            logger.error("CUDA不可用")
            return False
        
        logger.info("测试GPU利用率...")
        
        # 创建大量计算任务来测试GPU利用率
        device = torch.device('cuda')
        
        # 创建大矩阵进行计算
        size = 4096
        a = torch.randn(size, size, device=device, dtype=torch.float16)
        b = torch.randn(size, size, device=device, dtype=torch.float16)
        
        # 执行矩阵乘法
        for i in range(10):
            c = torch.matmul(a, b)
            torch.cuda.synchronize()  # 同步等待完成
        
        # 检查内存使用
        memory_allocated = torch.cuda.memory_allocated(0) / 1024**3
        memory_reserved = torch.cuda.memory_reserved(0) / 1024**3
        
        logger.info(f"GPU内存使用: {memory_allocated:.2f}GB / {memory_reserved:.2f}GB")
        
        # 清理内存
        del a, b, c
        torch.cuda.empty_cache()
        
        logger.info("GPU利用率测试完成")
        return True
        
    except Exception as e:
        logger.error(f"GPU利用率测试失败: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("GPU利用率优化器")
    logger.info("=" * 60)
    
    # 优化GPU性能
    if optimize_gpu_performance():
        logger.info("✅ GPU性能优化成功")
    else:
        logger.error("❌ GPU性能优化失败")
        exit(1)
    
    # 测试GPU利用率
    if test_gpu_utilization():
        logger.info("✅ GPU利用率测试成功")
    else:
        logger.error("❌ GPU利用率测试失败")
        exit(1)
    
    logger.info("=" * 60)
    logger.info("🚀 GPU优化完成！现在应该能获得更高的利用率")
    logger.info("=" * 60)





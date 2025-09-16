#!/usr/bin/env python3
"""
抑制警告信息
"""
import warnings
import os
import sys

def suppress_warnings():
    """抑制各种警告信息"""
    
    # 抑制Triton相关警告
    warnings.filterwarnings("ignore", message="A matching Triton is not available")
    warnings.filterwarnings("ignore", message="No module named 'triton'")
    
    # 抑制torch_dtype弃用警告
    warnings.filterwarnings("ignore", message="torch_dtype is deprecated")
    
    # 抑制Hugging Face连接警告
    warnings.filterwarnings("ignore", message="Couldn't connect to the Hub")
    warnings.filterwarnings("ignore", message="Will try to load from local cache")
    
    # 抑制CLIP token长度警告
    warnings.filterwarnings("ignore", message="Token indices sequence length is longer than the specified maximum")
    warnings.filterwarnings("ignore", message="Running this sequence through the model will result in indexing errors")
    warnings.filterwarnings("ignore", message="The following part of your input was truncated")
    
    # 抑制xformers相关警告
    warnings.filterwarnings("ignore", message="xformers")
    warnings.filterwarnings("ignore", message="flash-attention")
    
    # 设置环境变量抑制警告
    os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    
    # 抑制urllib3警告
    warnings.filterwarnings("ignore", message="urllib3")
    
    print("警告信息已抑制")

if __name__ == "__main__":
    suppress_warnings()


"""
配置文件
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量（如果.env文件存在）
if os.path.exists('.env'):
    load_dotenv()

class Config:
    """应用配置类"""
    
    # API配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'sk-0fbcaf78abf7432294d0883b25b544f6')
    DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
    
    # 模型配置
    SD_MODEL_PATH = os.getenv('SD_MODEL_PATH', 'runwayml/stable-diffusion-v1-5')
    SD_CACHE_DIR = os.getenv('SD_CACHE_DIR', './models')
    
    # 路径配置
    BASE_DIR = Path(__file__).parent
    OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'output')
    OUTPUT_PIC_DIR = BASE_DIR / os.getenv('OUTPUT_PIC_DIR', 'output_pic')
    OUTPUT_AUDIO_DIR = BASE_DIR / os.getenv('OUTPUT_AUDIO_DIR', 'output_audio')
    TEMP_DIR = BASE_DIR / os.getenv('TEMP_DIR', 'temp')
    CACHE_DIR = BASE_DIR / os.getenv('CACHE_DIR', 'cache')
    LOG_DIR = BASE_DIR / os.getenv('LOG_DIR', 'logs')
    
    # 视频配置
    VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1080))
    VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1920))
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', 24))
    VIDEO_BITRATE = os.getenv('VIDEO_BITRATE', '5000k')
    
    # 音频配置
    AUDIO_SAMPLE_RATE = int(os.getenv('AUDIO_SAMPLE_RATE', 44100))
    AUDIO_CHANNELS = int(os.getenv('AUDIO_CHANNELS', 2))
    
    # 图像配置
    IMAGE_WIDTH = int(os.getenv('IMAGE_WIDTH', 512))
    IMAGE_HEIGHT = int(os.getenv('IMAGE_HEIGHT', 512))
    IMAGE_QUALITY = int(os.getenv('IMAGE_QUALITY', 95))
    
    # 生成配置
    MAX_STORY_LENGTH = int(os.getenv('MAX_STORY_LENGTH', 300))
    MAX_SCENES = int(os.getenv('MAX_SCENES', 15))
    INFERENCE_STEPS = int(os.getenv('INFERENCE_STEPS', 30))
    GUIDANCE_SCALE = float(os.getenv('GUIDANCE_SCALE', 7.5))
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOG_DIR / os.getenv('LOG_FILE', 'app.log')
    
    # 性能配置
    ENABLE_MEMORY_EFFICIENT_ATTENTION = os.getenv('ENABLE_MEMORY_EFFICIENT_ATTENTION', 'true').lower() == 'true'
    ENABLE_CPU_OFFLOAD = os.getenv('ENABLE_CPU_OFFLOAD', 'true').lower() == 'true'
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 4))
    
    # RTX显卡优化配置
    ENABLE_RTX_OPTIMIZATION = os.getenv('ENABLE_RTX_OPTIMIZATION', 'true').lower() == 'true'
    USE_FLOAT16_FOR_RTX = os.getenv('USE_FLOAT16_FOR_RTX', 'true').lower() == 'true'
    RTX_MEMORY_FRACTION = float(os.getenv('RTX_MEMORY_FRACTION', 0.8))  # 使用80%显存
    
    @classmethod
    def create_directories(cls):
        """创建必要的目录"""
        for directory in [cls.OUTPUT_DIR, cls.OUTPUT_PIC_DIR, cls.OUTPUT_AUDIO_DIR, cls.TEMP_DIR, cls.CACHE_DIR, cls.LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 未设置")
        
        cls.create_directories()
        return True

# 初始化配置
config = Config()
config.validate_config()

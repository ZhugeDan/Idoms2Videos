# 成语故事短视频生成系统

## 项目简介

这是一个基于AI的成语故事短视频自动生成系统，能够从成语列表自动生成适合儿童阅读的成语故事，并进一步生成插画、音频和短视频，最终发布到抖音、快手等短视频平台。

## 功能特点

- 🎯 **智能故事生成**：使用DeepSeek API生成适合儿童的成语故事
- 🎨 **自动插画生成**：基于Stable Diffusion生成高质量插画
- 🔊 **语音合成**：自动生成旁白和角色配音
- 🎬 **视频制作**：将插画和音频合成为短视频
- 📱 **平台发布**：支持抖音、快手等平台发布
- ⚡ **批量处理**：支持批量处理多个成语
- 🎛️ **用户友好**：提供Web界面进行交互和微调

## 系统要求

### 硬件要求
- **处理器**：AMD Ryzen 9 7845HX 或同等性能
- **内存**：16GB RAM 或更多
- **显卡**：NVIDIA RTX 5060 或更高（支持CUDA）
- **存储**：至少20GB可用空间

### 软件要求
- Python 3.9+
- CUDA 11.8+（用于GPU加速）
- FFmpeg（用于视频处理）

## 安装指南

### 1. 克隆项目

```bash
git clone <repository-url>
cd Idoms2video
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv idiom_story_env

# 激活虚拟环境
# Windows
idiom_story_env\Scripts\activate
# Linux/Mac
source idiom_story_env/bin/activate
```

### 3. 安装依赖

```bash
# 安装PyTorch (CUDA版本)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
pip install -r requirements.txt
```

### 4. 安装FFmpeg

**Windows:**
1. 下载FFmpeg：https://ffmpeg.org/download.html
2. 解压到任意目录
3. 将bin目录添加到系统PATH

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

### 5. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
# 在.env文件中设置你的DeepSeek API密钥
DEEPSEEK_API_KEY=your_actual_api_key_here
```

## 使用方法

### 启动应用

```bash
# 启动Streamlit Web界面
streamlit run main.py
```

### 基本使用流程

1. **配置API密钥**：在侧边栏输入DeepSeek API密钥
2. **输入成语**：选择输入方式并输入成语
3. **生成故事**：系统自动调用DeepSeek生成故事文本
4. **编辑文本**：在编辑界面中微调故事内容
5. **生成插画**：系统提取场景并生成15张插画
6. **合成音频**：生成旁白和角色配音
7. **制作视频**：将插画和音频合成为短视频
8. **准备发布**：生成发布元数据和标签

### 输入方式

- **单个成语**：直接输入一个成语
- **成语列表**：输入多个成语，每行一个
- **文件上传**：上传包含成语的txt或csv文件

## 项目结构

```
Idoms2video/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── utils.py               # 工具函数
├── requirements.txt       # 依赖列表
├── .env.example          # 环境变量示例
├── modules/              # 核心模块
│   ├── __init__.py
│   ├── story_generator.py    # 故事生成模块
│   ├── scene_extractor.py    # 场景提取模块
│   ├── image_generator.py    # 图像生成模块
│   ├── text_segmenter.py     # 文本分段模块
│   ├── audio_generator.py    # 音频生成模块
│   └── video_composer.py     # 视频合成模块
├── output/               # 输出目录
├── temp/                 # 临时文件目录
├── cache/                # 缓存目录
└── logs/                 # 日志目录
```

## 配置说明

### 主要配置项

- `DEEPSEEK_API_KEY`：DeepSeek API密钥
- `MAX_SCENES`：最大场景数量（默认15）
- `VIDEO_WIDTH/HEIGHT`：视频分辨率（默认1080x1920）
- `INFERENCE_STEPS`：图像生成步数（默认30）
- `GUIDANCE_SCALE`：引导强度（默认7.5）

### 性能优化配置

- `ENABLE_MEMORY_EFFICIENT_ATTENTION`：启用内存高效注意力
- `ENABLE_CPU_OFFLOAD`：启用CPU卸载
- `BATCH_SIZE`：批处理大小

## 常见问题

### Q: 如何获取DeepSeek API密钥？
A: 访问DeepSeek官网注册账号，在控制台中创建API密钥。

### Q: 生成速度很慢怎么办？
A: 确保使用GPU加速，调整批处理大小，启用内存优化选项。

### Q: 生成的图像质量不佳？
A: 调整`INFERENCE_STEPS`和`GUIDANCE_SCALE`参数，或更换更好的模型。

### Q: 内存不足怎么办？
A: 启用`ENABLE_CPU_OFFLOAD`，减少批处理大小，或使用更小的图像尺寸。

## 技术支持

- 📧 邮箱：support@example.com
- 💬 QQ群：123456789
- 📖 文档：https://docs.example.com

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本的故事生成和视频制作功能
- 集成DeepSeek和Stable Diffusion
- 提供Web界面

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 致谢

感谢以下开源项目的支持：
- DeepSeek
- Stable Diffusion
- Streamlit
- MoviePy
- PyTorch

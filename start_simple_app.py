#!/usr/bin/env python3
"""
启动简化的自定义前端应用
"""
import subprocess
import sys
import os

def start_simple_app():
    """启动简化的Streamlit应用"""
    print("🎨 启动简化的自定义前端...")
    print("访问地址: http://localhost:8501")
    print("界面特点:")
    print("- 深色主题，符合您的设计风格")
    print("- 左侧图片展示区域")
    print("- 右侧控制面板")
    print("- 支持音频命名格式：成语_序号.mp3")
    print("- 支持增强版视频转场效果")
    print("="*50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "simple_streamlit_frontend.py", 
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    start_simple_app()

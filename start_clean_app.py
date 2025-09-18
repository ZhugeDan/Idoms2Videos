#!/usr/bin/env python3
"""
启动完全干净的自定义前端
没有任何代码标签显示
"""

import subprocess
import sys
import time

def main():
    print("🎨 启动完全干净的自定义前端...")
    print("访问地址: http://localhost:8502")
    print("界面特点:")
    print("- 完全隐藏所有Streamlit代码标签")
    print("- 深色主题，符合您的设计风格")
    print("- 左侧图片展示区域")
    print("- 右侧控制面板")
    print("- 支持音频命名格式：成语_序号.mp3")
    print("- 支持增强版视频转场效果")
    print("=" * 50)
    
    try:
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "clean_streamlit_frontend.py", 
            "--server.port", "8502",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()

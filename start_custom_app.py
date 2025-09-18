#!/usr/bin/env python3
"""
启动自定义前端应用
"""
import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """安装必要的依赖"""
    try:
        import flask
        print("✅ Flask 已安装")
    except ImportError:
        print("📦 正在安装 Flask...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask 安装完成")

def start_streamlit_app():
    """启动Streamlit应用（方案1）"""
    print("🚀 启动Streamlit自定义前端...")
    print("访问地址: http://localhost:8501")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "custom_frontend.py", "--server.port", "8501"])

def start_flask_app():
    """启动Flask应用（方案2）"""
    print("🚀 启动Flask自定义前端...")
    print("访问地址: http://localhost:5000")
    subprocess.run([sys.executable, "web_app.py"])

def main():
    """主函数"""
    print("🎨 成语故事短视频生成器 - 自定义前端")
    print("="*50)
    print("请选择前端方案:")
    print("1. Streamlit自定义前端 (推荐)")
    print("2. Flask独立Web应用")
    print("="*50)
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        start_streamlit_app()
    elif choice == "2":
        install_requirements()
        start_flask_app()
    else:
        print("❌ 无效选择，使用默认方案1")
        start_streamlit_app()

if __name__ == "__main__":
    main()

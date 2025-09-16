"""
成语故事短视频生成系统 - 简化版主程序
"""
import streamlit as st
import os
from pathlib import Path
from typing import List, Optional, Dict

# 导入配置
from config import config

# 设置页面配置
st.set_page_config(
    page_title="成语故事短视频生成器",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.header("⚙️ 配置设置")
        
        # API密钥输入
        api_key = st.text_input(
            "DeepSeek API密钥", 
            value=config.DEEPSEEK_API_KEY,
            type="password",
            help="请输入您的DeepSeek API密钥"
        )
        
        if api_key != config.DEEPSEEK_API_KEY:
            os.environ['DEEPSEEK_API_KEY'] = api_key
            st.rerun()
        
        # 输入方式选择
        st.subheader("📝 输入方式")
        input_method = st.radio(
            "选择输入方式",
            ["单个成语", "成语列表", "从文件读取"],
            help="选择如何输入要处理的成语"
        )
        
        return input_method

def render_main_interface(input_method: str):
    """渲染主界面"""
    st.title("📚 成语故事短视频生成器")
    st.markdown("---")
    
    idioms = []
    
    if input_method == "单个成语":
        st.subheader("📖 单个成语输入")
        idiom = st.text_input("请输入成语", placeholder="例如：守株待兔")
        if idiom:
            idioms = [idiom]
    
    elif input_method == "成语列表":
        st.subheader("📋 成语列表输入")
        idiom_text = st.text_area(
            "请输入成语列表（每行一个）",
            placeholder="守株待兔\n画蛇添足\n亡羊补牢",
            height=200
        )
        if idiom_text:
            idioms = [line.strip() for line in idiom_text.split('\n') if line.strip()]
    
    else:  # 从文件读取
        st.subheader("📁 文件上传")
        uploaded_file = st.file_uploader(
            "上传成语文件", 
            type=['txt', 'csv'],
            help="支持.txt和.csv格式，每行一个成语"
        )
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            idioms = [line.strip() for line in content.split('\n') if line.strip()]
    
    # 显示输入的成语
    if idioms:
        st.success(f"✅ 已加载 {len(idioms)} 个成语")
        
        with st.expander("📋 查看成语列表"):
            for i, idiom in enumerate(idioms, 1):
                st.write(f"{i}. {idiom}")
        
        # 处理按钮
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🚀 开始生成", type="primary", use_container_width=True):
                st.info("功能开发中，请使用完整版main.py")
        
        with col2:
            if st.button("🗑️ 清理缓存", use_container_width=True):
                st.success("缓存已清理")
        
        with col3:
            if st.button("💾 导出结果", use_container_width=True):
                st.info("导出功能开发中...")

def main():
    """主函数"""
    # 渲染侧边栏
    input_method = render_sidebar()
    
    # 渲染主界面
    render_main_interface(input_method)
    
    # 页脚
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "成语故事短视频生成器 v1.0 | 技术支持：DeepSeek + Stable Diffusion"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
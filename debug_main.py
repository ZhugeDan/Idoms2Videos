"""
调试版主程序 - 用于诊断问题
"""
import streamlit as st
import os
from pathlib import Path
from typing import List, Optional, Dict

# 导入配置
from config import config

# 设置页面配置
st.set_page_config(
    page_title="成语故事短视频生成器 - 调试版",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

def debug_process_idiom(idiom: str):
    """调试版处理单个成语"""
    st.write(f"🐛 开始处理成语: {idiom}")
    
    # 步骤1：生成故事文本（模拟）
    st.write("📝 步骤1: 生成故事文本")
    story_text = f"这是一个关于{idiom}的故事。从前有一个小兔子，它总是很着急..."
    st.text_area("生成的故事:", value=story_text, height=200)
    
    # 步骤2：用户确认
    st.write("📝 步骤2: 用户确认")
    col1, col2 = st.columns(2)
    
    with col1:
        confirm_clicked = st.button("✅ 确认并继续", key=f"confirm_{idiom}", type="primary")
    
    with col2:
        regenerate_clicked = st.button("🔄 重新生成", key=f"regenerate_{idiom}")
    
    # 显示按钮状态
    st.write(f"🐛 确认按钮状态: {confirm_clicked}")
    st.write(f"🐛 重新生成按钮状态: {regenerate_clicked}")
    
    # 处理按钮点击
    if regenerate_clicked:
        st.write("🔄 重新生成被点击")
        return {"status": "regenerate"}
    
    if not confirm_clicked:
        st.write("⏳ 等待用户确认")
        return {"status": "waiting_for_confirmation"}
    
    st.write("✅ 用户已确认，继续执行后续步骤")
    
    # 步骤3：提取场景
    st.write("🎬 步骤3: 提取场景")
    scenes = [
        "小兔子在森林里",
        "小兔子看到一棵树",
        "小兔子坐在树下等待",
        "小兔子发现了一个胡萝卜"
    ]
    st.write(f"提取到 {len(scenes)} 个场景:")
    for i, scene in enumerate(scenes, 1):
        st.write(f"{i}. {scene}")
    
    # 步骤4：生成插画
    st.write("🎨 步骤4: 生成插画")
    with st.spinner("正在初始化图像生成器..."):
        import time
        time.sleep(2)  # 模拟加载时间
    st.success("✅ 图像生成器初始化完成")
    
    # 模拟生成插画
    for i, scene in enumerate(scenes, 1):
        st.write(f"正在生成第 {i}/{len(scenes)} 张插画: {scene}")
        time.sleep(1)  # 模拟生成时间
    
    # 步骤5：生成音频
    st.write("🔊 步骤5: 生成音频")
    with st.spinner("正在生成音频..."):
        time.sleep(2)  # 模拟生成时间
    st.success("✅ 音频生成完成")
    
    # 步骤6：合成视频
    st.write("🎬 步骤6: 合成视频")
    with st.spinner("正在合成视频..."):
        time.sleep(3)  # 模拟合成时间
    st.success("✅ 视频合成完成")
    
    return {
        "status": "success",
        "idiom": idiom,
        "story": story_text,
        "scenes": scenes,
        "video_path": f"output/{idiom}_story.mp4"
    }

def main():
    """主函数"""
    st.title("🐛 成语故事短视频生成器 - 调试版")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 配置设置")
        st.write("调试模式 - 显示详细执行步骤")
    
    # 主界面
    st.subheader("📖 单个成语输入")
    idiom = st.text_input("请输入成语", placeholder="例如：守株待兔", key="debug_idiom")
    
    if idiom:
        st.write(f"您输入的成语: {idiom}")
        
        if st.button("🚀 开始生成", type="primary", key="debug_start"):
            result = debug_process_idiom(idiom)
            
            if result["status"] == "success":
                st.success("✅ 视频生成成功！")
                
                # 显示结果
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 生成统计")
                    st.metric("场景数量", len(result["scenes"]))
                    st.metric("故事长度", f"{len(result['story'])} 字")
                
                with col2:
                    st.subheader("🎬 生成视频")
                    st.write(f"视频路径: {result['video_path']}")
                    st.success("视频已生成完成！")
            
            elif result["status"] == "regenerate":
                st.info("🔄 重新生成中...")
                st.rerun()
            
            elif result["status"] == "waiting_for_confirmation":
                st.info("⏳ 等待用户确认...")

if __name__ == "__main__":
    main()


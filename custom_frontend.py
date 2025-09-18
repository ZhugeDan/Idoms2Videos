#!/usr/bin/env python3
"""
自定义前端界面 - 基于您提供的HTML样式
"""
import streamlit as st
import os
from pathlib import Path
from typing import List, Optional, Dict
import base64
from PIL import Image
import io

# 导入后端模块
from main import IdiomStoryVideoGenerator

class CustomFrontend:
    """自定义前端界面"""
    
    def __init__(self):
        self.app = IdiomStoryVideoGenerator()
        self.current_image_index = 0
        self.images = []
        self.story_text = ""
        self.scenes = []
        
    def render_custom_interface(self):
        """渲染自定义界面"""
        # 自定义CSS
        st.markdown(self.get_custom_css(), unsafe_allow_html=True)
        
        # 主容器
        st.markdown("""
        <div class="container">
            <div class="image-section">
                <div class="navigation">
                    <div class="nav-btn" onclick="previousImage()">←</div>
                    <div class="nav-btn" onclick="nextImage()">→</div>
                </div>
                <div id="image-container">
                    <img id="main-image" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAwIiBoZWlnaHQ9IjgwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMWExYTFhIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9veWbvueJhzwvdGV4dD48L3N2Zz4=" alt="成语故事插画" class="portrait">
                </div>
            </div>
            
            <div class="ui-section">
                <div class="dialogue">
                    <div class="dialogue-text" id="story-content">
                        <p>请输入成语，开始生成故事...</p>
                    </div>
                    <div class="exp-notification" id="progress-notification" style="display: none;">
                        正在生成内容...
                    </div>
                </div>
                
                <div class="options">
                    <button class="option-btn" onclick="generateStory()">📚 生成故事</button>
                    <button class="option-btn" onclick="generateImages()">🎨 生成插画</button>
                    <button class="option-btn" onclick="generateAudio()">🔊 生成音频</button>
                    <button class="option-btn" onclick="createVideo()">🎬 创建视频</button>
                </div>
                
                <div class="tools">
                    <button class="tool-btn" onclick="downloadImages()">下载图片</button>
                    <button class="tool-btn" onclick="downloadAudio()">下载音频</button>
                    <button class="tool-btn" onclick="downloadVideo()">下载视频</button>
                    <div style="margin-left: auto; color: #888; font-size: 14px;" id="file-count">0</div>
                </div>
                
                <div class="status-bar">
                    <div class="time-display" id="current-time">00:00</div>
                    <div class="day-counter" id="progress-counter">0</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 隐藏的输入区域
        with st.sidebar:
            st.header("🎯 控制面板")
            idiom = st.text_input("输入成语", placeholder="例如：掩耳盗铃")
            
            if st.button("🚀 开始生成", type="primary"):
                if idiom:
                    self.process_idiom(idiom)
                else:
                    st.error("请输入成语")
            
            # 显示生成的文件
            self.show_generated_files()
    
    def get_custom_css(self):
        """获取自定义CSS样式"""
        return """
        <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #1a1a1a;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }
        
        .container {
            display: flex;
            flex: 1;
            overflow: hidden;
            min-height: 80vh;
        }
        
        .image-section {
            flex: 1;
            background-color: #0f0f0f;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            margin: 10px;
        }
        
        .portrait {
            width: 85%;
            height: auto;
            max-height: 80vh;
            border: 2px solid #3a3a3a;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
            filter: contrast(1.1) brightness(0.9) sepia(0.2);
            border-radius: 8px;
        }
        
        .navigation {
            position: absolute;
            top: 20px;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 20px;
        }
        
        .nav-btn {
            background-color: rgba(40, 40, 40, 0.7);
            color: #b0b0b0;
            border: 1px solid #555;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background-color: rgba(60, 60, 60, 0.9);
            color: #e0e0e0;
        }
        
        .ui-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 20px;
            background: linear-gradient(to bottom, #222222, #151515);
            border-left: 1px solid #333;
            border-radius: 8px;
            margin: 10px;
        }
        
        .dialogue {
            flex: 1;
            padding: 20px;
            background-color: rgba(30, 30, 30, 0.7);
            border: 1px solid #444;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow-y: auto;
            max-height: 400px;
        }
        
        .dialogue-text {
            line-height: 1.6;
            font-size: 16px;
        }
        
        .dialogue-text em {
            color: #a58e6d;
            font-style: normal;
        }
        
        .exp-notification {
            color: #a5c0a0;
            margin: 10px 0;
            font-size: 14px;
        }
        
        .options {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .option-btn {
            background-color: #2a2a2a;
            color: #d0d0d0;
            border: 1px solid #444;
            padding: 12px 15px;
            text-align: left;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }
        
        .option-btn:hover {
            background-color: #353535;
            border-color: #555;
        }
        
        .tools {
            display: flex;
            gap: 10px;
            margin-top: auto;
        }
        
        .tool-btn {
            background-color: #2a2a2a;
            color: #d0d0d0;
            border: 1px solid #444;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .tool-btn:hover {
            background-color: #353535;
        }
        
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #333;
            color: #888;
            font-size: 14px;
        }
        
        .time-display::before {
            content: "时间: ";
        }
        
        .day-counter::before {
            content: "进度: ";
        }
        
        /* 隐藏Streamlit默认样式 */
        .main .block-container {
            padding: 0;
            max-width: 100%;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    
    def get_custom_js(self):
        """获取自定义JavaScript"""
        return """
        <script>
        let currentImageIndex = 0;
        let images = [];
        
        function updateImage() {
            const img = document.getElementById('main-image');
            if (images.length > 0) {
                img.src = images[currentImageIndex];
            }
        }
        
        function previousImage() {
            if (images.length > 0) {
                currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
                updateImage();
            }
        }
        
        function nextImage() {
            if (images.length > 0) {
                currentImageIndex = (currentImageIndex + 1) % images.length;
                updateImage();
            }
        }
        
        function generateStory() {
            // 这里会调用Streamlit后端
            alert('生成故事功能');
        }
        
        function generateImages() {
            alert('生成插画功能');
        }
        
        function generateAudio() {
            alert('生成音频功能');
        }
        
        function createVideo() {
            alert('创建视频功能');
        }
        
        function downloadImages() {
            alert('下载图片功能');
        }
        
        function downloadAudio() {
            alert('下载音频功能');
        }
        
        function downloadVideo() {
            alert('下载视频功能');
        }
        
        // 更新时间显示
        function updateTime() {
            const now = new Date();
            const timeStr = now.toLocaleTimeString('zh-CN', {hour12: false});
            document.getElementById('current-time').textContent = timeStr;
        }
        
        setInterval(updateTime, 1000);
        updateTime();
        </script>
        """
    
    def process_idiom(self, idiom: str):
        """处理成语生成"""
        try:
            # 初始化组件
            self.app._initialize_components()
            
            # 生成故事
            with st.spinner("正在生成故事..."):
                story_text = self.app.generate_story_text(idiom)
                self.story_text = story_text
                
                # 更新界面显示
                st.markdown(f"""
                <script>
                document.getElementById('story-content').innerHTML = `
                    <p><strong>{idiom}</strong> - {story_text[:200]}...</p>
                `;
                </script>
                """, unsafe_allow_html=True)
            
            # 生成图片
            with st.spinner("正在生成插画..."):
                scenes = self.app.extract_scenes(story_text)
                images = self.app.generate_story_images(scenes, idiom)
                self.images = images
                self.scenes = scenes
                
                # 更新图片显示
                if images:
                    self.update_image_display(images[0])
            
            st.success(f"✅ {idiom} 故事生成完成！")
            
        except Exception as e:
            st.error(f"生成失败: {e}")
    
    def update_image_display(self, image):
        """更新图片显示"""
        if hasattr(image, 'save'):
            # PIL.Image对象
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            img_data = f"data:image/jpeg;base64,{img_str}"
        else:
            # 假设是文件路径
            img_data = image
        
        st.markdown(f"""
        <script>
        document.getElementById('main-image').src = '{img_data}';
        </script>
        """, unsafe_allow_html=True)
    
    def show_generated_files(self):
        """显示生成的文件"""
        st.subheader("📁 生成的文件")
        
        # 显示图片文件
        pic_dir = Path("output_pic")
        if pic_dir.exists():
            pic_files = list(pic_dir.glob("*.jpg"))
            if pic_files:
                st.write(f"📸 图片文件 ({len(pic_files)} 个)")
                for file in pic_files[:5]:  # 只显示前5个
                    st.write(f"- {file.name}")
        
        # 显示音频文件
        audio_dir = Path("output_audio")
        if audio_dir.exists():
            audio_files = list(audio_dir.glob("*.mp3"))
            if audio_files:
                st.write(f"🔊 音频文件 ({len(audio_files)} 个)")
                for file in audio_files[:5]:  # 只显示前5个
                    st.write(f"- {file.name}")
        
        # 显示视频文件
        video_dir = Path("output")
        if video_dir.exists():
            video_files = list(video_dir.glob("*.mp4"))
            if video_files:
                st.write(f"🎬 视频文件 ({len(video_files)} 个)")
                for file in video_files[:5]:  # 只显示前5个
                    st.write(f"- {file.name}")

def main():
    """主函数"""
    st.set_page_config(
        page_title="成语故事短视频生成器",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 创建自定义前端
    frontend = CustomFrontend()
    
    # 渲染界面
    frontend.render_custom_interface()
    
    # 添加JavaScript
    st.markdown(frontend.get_custom_js(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

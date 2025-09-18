import streamlit as st
import os
from pathlib import Path

class CleanStreamlitFrontend:
    def __init__(self):
        self.setup_page()
    
    def setup_page(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="成语故事生成器",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="collapsed"  # 隐藏侧边栏
        )
        
        # 隐藏所有Streamlit默认元素
        st.markdown("""
        <style>
        /* 隐藏所有Streamlit默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp > header {visibility: hidden;}
        .stApp > footer {visibility: hidden;}
        .stApp > div[data-testid="stToolbar"] {visibility: hidden;}
        .stApp > div[data-testid="stDecoration"] {visibility: hidden;}
        .stApp > div[data-testid="stStatusBar"] {visibility: hidden;}
        
        /* 隐藏侧边栏 */
        .stApp > div[data-testid="stSidebar"] {visibility: hidden;}
        
        /* 全屏显示 */
        .stApp {
            margin: 0;
            padding: 0;
        }
        
        .main-container {
            width: 100vw;
            height: 100vh;
            margin: 0;
            padding: 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_interface(self):
        """渲染界面"""
        # 自定义CSS
        st.markdown(self.get_custom_css(), unsafe_allow_html=True)
        
        # 主容器
        st.markdown("""
        <div class="main-container">
            <div class="image-section">
                <div class="navigation">
                    <button class="nav-btn" onclick="previousImage()">←</button>
                    <button class="nav-btn" onclick="nextImage()">→</button>
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
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 添加JavaScript功能
        st.markdown("""
        <script>
        function generateStory() {
            alert('生成故事功能 - 请在侧边栏输入成语并点击开始生成');
        }
        
        function generateImages() {
            alert('生成插画功能 - 请先生成故事');
        }
        
        function generateAudio() {
            alert('生成音频功能 - 请先生成故事');
        }
        
        function createVideo() {
            alert('创建视频功能 - 请先生成故事和插画');
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
        
        function previousImage() {
            alert('上一张图片');
        }
        
        function nextImage() {
            alert('下一张图片');
        }
        </script>
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
        
        .main-container {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        .image-section {
            flex: 1;
            background-color: #0f0f0f;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        .portrait {
            width: 85%;
            height: auto;
            border: 2px solid #3a3a3a;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
            filter: contrast(1.1) brightness(0.9) sepia(0.2);
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
        }
        
        .dialogue {
            flex: 1;
            padding: 20px;
            background-color: rgba(30, 30, 30, 0.7);
            border: 1px solid #444;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow-y: auto;
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
        
        .option-btn::before {
            content: attr(data-skill);
            position: absolute;
            right: 15px;
            color: #8a8a8a;
            font-size: 12px;
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
        
        .time-display {
            display: flex;
            align-items: center;
        }
        
        .day-counter::before {
            content: "天数";
            margin-right: 5px;
        }
        </style>
        """
    
    def process_idiom(self, idiom):
        """处理成语生成"""
        try:
            with st.spinner("正在生成故事..."):
                # 模拟生成过程
                import time
                time.sleep(2)  # 模拟处理时间
                st.success(f"故事生成完成：{idiom}")
                
                # 更新界面显示
                st.markdown(f"""
                <script>
                document.getElementById('story-content').innerHTML = '<p><strong>{idiom}</strong> - 这是一个关于{idiom}的精彩故事...</p>';
                </script>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")
    
    def show_generated_files(self):
        """显示生成的文件"""
        st.subheader("📁 生成的文件")
        
        # 检查输出目录
        output_dirs = ['output_pic', 'output_audio', 'output']
        for dir_name in output_dirs:
            if os.path.exists(dir_name):
                files = list(Path(dir_name).glob('*'))
                if files:
                    st.write(f"**{dir_name}**:")
                    for file in files[:5]:  # 只显示前5个文件
                        st.write(f"- {file.name}")
                    if len(files) > 5:
                        st.write(f"... 还有 {len(files) - 5} 个文件")

def main():
    """主函数"""
    frontend = CleanStreamlitFrontend()
    frontend.render_interface()

if __name__ == "__main__":
    main()

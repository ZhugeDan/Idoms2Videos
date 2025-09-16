"""
成语故事短视频生成系统 - 主程序
"""
import streamlit as st
import os
from pathlib import Path
from typing import List, Optional, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import warnings

# 抑制警告信息
warnings.filterwarnings("ignore", message="A matching Triton is not available")
warnings.filterwarnings("ignore", message="torch_dtype is deprecated")
warnings.filterwarnings("ignore", message="Couldn't connect to the Hub")
warnings.filterwarnings("ignore", message="Token indices sequence length is longer than")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

# 导入自定义模块
from config import config
from utils import Logger, PerformanceMonitor, cache_manager
from modules.story_generator import DeepSeekStoryGenerator
from modules.image_generator import ImageGenerator
from modules.audio_generator import AudioGenerator
from modules.video_composer import VideoComposer
from simple_video_composer import SimpleVideoComposer
from modules.scene_extractor import SceneExtractor
from modules.text_segmenter import TextSegmenter

# 设置页面配置
st.set_page_config(
    page_title="成语故事短视频生成器",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化日志
Logger.setup_logger(config.LOG_FILE, config.LOG_LEVEL)

class IdiomStoryVideoGenerator:
    """成语故事短视频生成器主类"""
    
    def __init__(self):
        self.story_generator = None
        self.scene_extractor = None
        self.image_generator = None
        self.text_segmenter = None
        self.audio_generator = None
        self.video_composer = None
        self.performance_monitor = None
        
        # 不预初始化组件，改为按需加载
    
    def _initialize_components(self):
        """按需初始化各个组件"""
        try:
            # 检查API密钥
            if not config.DEEPSEEK_API_KEY:
                st.error("请在环境变量中设置 DEEPSEEK_API_KEY")
                return
            
            # 初始化基础组件
            if not self.scene_extractor:
                self.scene_extractor = SceneExtractor()
            
            if not self.text_segmenter:
                self.text_segmenter = TextSegmenter()
            
            if not self.audio_generator:
                self.audio_generator = AudioGenerator()
            
            if not self.video_composer:
                # 使用简化版视频合成器避免MoviePy兼容性问题
                self.video_composer = SimpleVideoComposer()
            
            if not self.performance_monitor:
                self.performance_monitor = PerformanceMonitor()
            
            # 初始化故事生成器
            if not self.story_generator:
                self.story_generator = DeepSeekStoryGenerator(config.DEEPSEEK_API_KEY)
            
            st.success("✅ 基础组件初始化完成")
            
        except Exception as e:
            st.error(f"❌ 初始化失败: {e}")
    
    def _initialize_image_generator(self):
        """按需初始化图像生成器"""
        if not self.image_generator:
            with st.spinner("正在初始化图像生成器..."):
                self.image_generator = ImageGenerator()
            st.success("✅ 图像生成器初始化完成")
    
    def generate_story_text(self, idiom: str) -> str:
        """生成故事文本"""
        if not self.story_generator:
            raise ValueError("故事生成器未初始化")
        
        # 检查缓存
        cache_key = cache_manager.get_cache_key(f"story_{idiom}")
        cached_result = cache_manager.get_cached_result(cache_key)
        
        if cached_result:
            st.info("📋 使用缓存的故事文本")
            return cached_result
        
        # 生成新故事
        with st.spinner(f"正在为成语'{idiom}'生成故事..."):
            story_text = self.story_generator.generate_story(idiom)
        
        # 保存到缓存
        cache_manager.save_cache(cache_key, story_text)
        
        return story_text
    
    def extract_scenes_from_story(self, story_text: str) -> List[str]:
        """从故事中提取场景"""
        with st.spinner("正在提取故事场景..."):
            scenes = self.scene_extractor.extract_scenes(story_text)
        
        return scenes
    
    def generate_story_images(self, scenes: List[str], idiom: str) -> List:
        """生成故事插画"""
        # 按需初始化图像生成器
        self._initialize_image_generator()
        
        if not self.image_generator:
            raise ValueError("图像生成器初始化失败")
        
        # 检查缓存
        cache_key = cache_manager.get_cache_key(f"images_{idiom}")
        cached_images = cache_manager.get_cached_result(cache_key)
        
        if cached_images:
            st.info("🖼️ 使用缓存的插画")
            # 显示缓存的图片
            self._display_images(cached_images, scenes)
            return cached_images
        
        # 生成新插画
        images = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 创建图片展示区域
        st.subheader("🎨 生成的插画")
        image_columns = st.columns(3)  # 每行显示3张图片
        
        for i, scene in enumerate(scenes):
            status_text.text(f"正在生成第 {i+1}/{len(scenes)} 张插画...")
            
            try:
                image = self.image_generator.generate_image(scene)
                images.append(image)
                progress_bar.progress((i + 1) / len(scenes))
                
                # 在网格中显示图片
                col_idx = i % 3
                with image_columns[col_idx]:
                    st.image(image, caption=f"场景 {i+1}: {scene[:30]}...", use_container_width=True)
                    
            except Exception as e:
                st.error(f"生成第 {i+1} 张插画失败: {e}")
                continue
        
        # 保存到缓存
        cache_manager.save_cache(cache_key, images)
        
        # 保存图片到output_pic文件夹
        saved_paths = self._save_images_to_output(images, idiom)
        
        status_text.text("✅ 所有插画生成完成")
        # 再次整体展示，确保始终能看到插画
        st.image(images, caption=[f"场景 {i+1}" for i in range(len(images))], use_container_width=True)
        
        # 显示保存路径信息
        if saved_paths:
            st.success(f"📁 图片已保存到: {config.OUTPUT_PIC_DIR}")
            for i, path in enumerate(saved_paths):
                st.text(f"场景 {i+1}: {path.name}")
        
        return images
    
    def _save_images_to_output(self, images: List, idiom: str) -> List[Path]:
        """保存图片到output_pic文件夹"""
        try:
            # 确保输出目录存在
            config.OUTPUT_PIC_DIR.mkdir(parents=True, exist_ok=True)
            
            saved_paths = []
            for i, image in enumerate(images):
                # 生成文件名：成语_序号.jpg
                filename = f"{idiom}_{i+1:02d}.jpg"
                output_path = config.OUTPUT_PIC_DIR / filename
                
                # 保存图片
                image.save(output_path, quality=95)
                saved_paths.append(output_path)
                
                logger.info(f"图片已保存: {output_path}")
            
            return saved_paths
            
        except Exception as e:
            logger.error(f"保存图片失败: {e}")
            return []
    
    def _display_images(self, images: List, scenes: List[str]):
        """显示图片网格"""
        st.subheader("🎨 生成的插画")
        image_columns = st.columns(3)  # 每行显示3张图片
        
        for i, (image, scene) in enumerate(zip(images, scenes)):
            col_idx = i % 3
            with image_columns[col_idx]:
                st.image(image, caption=f"场景 {i+1}: {scene[:30]}...", use_container_width=True)
    
    def generate_story_audio(self, story_text: str, idiom: str) -> any:
        """生成故事音频"""
        # 检查缓存
        cache_key = cache_manager.get_cache_key(f"audio_{idiom}")
        cached_audio = cache_manager.get_cached_result(cache_key)
        
        if cached_audio:
            st.info("🔊 使用缓存的音频")
            return cached_audio
        
        # 生成新音频
        with st.spinner("正在生成音频..."):
            segments = self.text_segmenter.segment_text(story_text)
            audio = self.audio_generator.generate_story_audio(segments)
        
        # 保存到缓存
        cache_manager.save_cache(cache_key, audio)
        
        return audio
    
    def create_video(self, images: List, audio: any, idiom: str) -> str:
        """创建视频"""
        with st.spinner("正在合成视频..."):
            output_path = config.OUTPUT_DIR / f"{idiom}_story.mp4"
            video_path = self.video_composer.create_story_video(
                images, audio, str(output_path)
            )
        
        return video_path
    
    def process_single_idiom(self, idiom: str) -> Dict:
        """处理单个成语"""
        try:
            # 初始化基础组件
            self._initialize_components()
            
            # 步骤1：生成故事文本
            story_text = self.generate_story_text(idiom)
            
            # 步骤2：用户微调界面
            st.subheader("📝 故事文本编辑")
            edited_story = st.text_area(
                "编辑故事内容：",
                value=story_text,
                height=300,
                key=f"story_edit_{idiom}",
                help="您可以在此修改故事内容，添加或删除场景描述"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                confirm_clicked = st.button("✅ 确认并继续", key=f"confirm_{idiom}", type="primary")
            
            with col2:
                regenerate_clicked = st.button("🔄 重新生成", key=f"regenerate_{idiom}")
            
            # 处理按钮点击
            if regenerate_clicked:
                cache_key = cache_manager.get_cache_key(f"story_{idiom}")
                cache_manager.clear_cache(cache_key.split('_')[0] + '_')
                return self.process_single_idiom(idiom)
            
            if not confirm_clicked:
                return {"status": "waiting_for_confirmation"}
            
            # 步骤3：提取场景
            scenes = self.extract_scenes_from_story(edited_story)
            
            # 步骤4：生成插画
            images = self.generate_story_images(scenes, idiom)
            
            # 显示插画统计
            st.success(f"✅ 成功生成 {len(images)} 张插画")
            
            # 步骤5：询问是否生成视频
            st.subheader("🎬 视频生成选项")
            col1, col2 = st.columns(2)
            
            with col1:
                generate_video = st.checkbox("生成视频", value=True, help="勾选此项将生成包含音频的完整视频")
            
            with col2:
                generate_audio = st.checkbox("生成音频", value=True, help="勾选此项将生成故事音频")
            
            video_path = None
            audio = None
            
            if generate_audio:
                # 步骤5：生成音频
                audio = self.generate_story_audio(edited_story, idiom)
                st.success("✅ 音频生成完成")
            
            if generate_video and audio:
                # 步骤6：创建视频
                try:
                    video_path = self.create_video(images, audio, idiom)
                    st.success("✅ 视频生成完成")
                except Exception as e:
                    st.error(f"视频生成失败: {e}")
                    st.info("您可以查看生成的插画，视频生成功能暂时不可用")
            
            return {
                "status": "success",
                "idiom": idiom,
                "story": edited_story,
                "scenes": scenes,
                "images": images,
                "video_path": video_path,
                "audio": audio,
                "images_count": len(images)
            }
            
        except Exception as e:
            st.error(f"处理成语'{idiom}'时出错: {e}")
            return {
                "status": "error",
                "idiom": idiom,
                "error": str(e)
            }

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
        
        # 高级设置
        with st.expander("🔧 高级设置"):
            max_scenes = st.slider("最大场景数", 5, 20, config.MAX_SCENES)
            image_quality = st.selectbox("图像质量", ["标准", "高质量", "超高质量"])
            audio_speed = st.slider("语音速度", 0.8, 1.5, 1.0)
            
            # 更新配置
            config.MAX_SCENES = max_scenes
        
        # 系统状态
        st.subheader("💻 系统状态")
        
        # GPU状态
        gpu_info = PerformanceMonitor.get_gpu_info()
        if gpu_info:
            st.metric("GPU使用率", f"{gpu_info['utilization']:.1f}%")
            st.metric("GPU内存", f"{gpu_info['memory_used']}/{gpu_info['memory_total']} MB")
        else:
            st.warning("未检测到GPU")
        
        # 内存状态
        memory_info = PerformanceMonitor.get_memory_info()
        if memory_info:
            st.metric("内存使用率", f"{memory_info['percentage']:.1f}%")
        
        return input_method

def render_main_interface(generator: IdiomStoryVideoGenerator, input_method: str):
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
                if len(idioms) == 1:
                    # 设置状态并跳转到处理界面
                    st.session_state.current_idiom = idioms[0]
                    st.session_state.processing_step = 'processing'
                    st.rerun()
                else:
                    # 批量处理
                    st.info("批量处理功能开发中...")
        
        with col2:
            if st.button("🗑️ 清理缓存", use_container_width=True):
                cache_manager.clear_cache()
                st.success("缓存已清理")
        
        with col3:
            if st.button("💾 导出结果", use_container_width=True):
                st.info("导出功能开发中...")

def render_processing_interface(generator: IdiomStoryVideoGenerator, idiom: str):
    """渲染处理界面"""
    st.title("📚 成语故事短视频生成器")
    st.markdown("---")
    
    st.subheader(f"正在处理成语: {idiom}")
    
    # 返回按钮
    if st.button("← 返回", key="back_to_input"):
        st.session_state.processing_step = 'input'
        st.session_state.current_idiom = None
        st.rerun()
    
    # 处理成语
    try:
        result = generator.process_single_idiom(idiom)
        
        if result["status"] == "success":
            st.success("✅ 处理完成！")
            
            # 显示结果统计
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("场景数量", result["images_count"])
            
            with col2:
                st.metric("故事长度", f"{len(result['story'])} 字")
            
            with col3:
                if result["video_path"]:
                    st.metric("视频状态", "✅ 已生成")
                else:
                    st.metric("视频状态", "❌ 未生成")
            
            # 显示生成的插画
            if "images" in result and result["images"]:
                st.subheader("🎨 生成的插画")
                self._display_images(result["images"], result["scenes"])
            
            # 显示视频（如果生成成功）
            if result["video_path"] and os.path.exists(result["video_path"]):
                st.subheader("🎬 生成的视频")
                st.video(result["video_path"])
            
            # 显示音频（如果生成成功）
            if result["audio"]:
                st.subheader("🔊 生成的音频")
                st.info("音频已生成，可在视频中听到")
            
            # 添加下载按钮
            st.subheader("💾 下载选项")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if result["images"]:
                    # 创建图片压缩包
                    import zipfile
                    import io
                    
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for i, image in enumerate(result["images"]):
                            img_buffer = io.BytesIO()
                            image.save(img_buffer, format='PNG')
                            zip_file.writestr(f"scene_{i+1}.png", img_buffer.getvalue())
                    
                    zip_buffer.seek(0)
                    st.download_button(
                        label="📦 下载插画包",
                        data=zip_buffer.getvalue(),
                        file_name=f"{idiom}_images.zip",
                        mime="application/zip"
                    )
            
            with col2:
                if result["video_path"] and os.path.exists(result["video_path"]):
                    with open(result["video_path"], "rb") as video_file:
                        st.download_button(
                            label="🎬 下载视频",
                            data=video_file.read(),
                            file_name=f"{idiom}_story.mp4",
                            mime="video/mp4"
                        )
            
            with col3:
                if result["story"]:
                    st.download_button(
                        label="📝 下载故事文本",
                        data=result["story"],
                        file_name=f"{idiom}_story.txt",
                        mime="text/plain"
                    )
            
            # 重置状态
            st.session_state.processing_step = 'input'
            st.session_state.current_idiom = None
            
        elif result["status"] == "waiting_for_confirmation":
            st.info("⏳ 等待用户确认...")
            
    except Exception as e:
        st.error(f"处理失败: {e}")
        st.session_state.processing_step = 'input'
        st.session_state.current_idiom = None

def main():
    """主函数"""
    # 初始化会话状态
    if 'generator' not in st.session_state:
        st.session_state.generator = IdiomStoryVideoGenerator()
    
    if 'current_idiom' not in st.session_state:
        st.session_state.current_idiom = None
    
    if 'processing_step' not in st.session_state:
        st.session_state.processing_step = 'input'
    
    # 渲染侧边栏
    input_method = render_sidebar()
    
    # 根据当前步骤渲染界面
    if st.session_state.processing_step == 'input':
        render_main_interface(st.session_state.generator, input_method)
    elif st.session_state.processing_step == 'processing':
        render_processing_interface(st.session_state.generator, st.session_state.current_idiom)
    
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

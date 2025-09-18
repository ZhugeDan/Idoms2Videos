"""
数据库管理界面
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from database_manager import db_manager
import os

def show_database_management():
    """显示数据库管理界面"""
    st.title("📊 数据库管理")
    
    # 获取存储统计
    stats = db_manager.get_storage_stats()
    
    # 显示统计信息
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("故事数量", stats['story_count'])
    
    with col2:
        st.metric("图片数量", stats['image_count'])
    
    with col3:
        st.metric("音频数量", stats['audio_count'])
    
    with col4:
        st.metric("视频数量", stats['video_count'])
    
    # 显示存储大小
    st.subheader("💾 存储使用情况")
    
    size_col1, size_col2, size_col3, size_col4 = st.columns(4)
    
    with size_col1:
        st.metric("图片大小", f"{stats['image_size'] / 1024 / 1024:.1f} MB")
    
    with size_col2:
        st.metric("音频大小", f"{stats['audio_size'] / 1024 / 1024:.1f} MB")
    
    with size_col3:
        st.metric("视频大小", f"{stats['video_size'] / 1024 / 1024:.1f} MB")
    
    with size_col4:
        st.metric("总大小", f"{stats['total_size'] / 1024 / 1024:.1f} MB")
    
    # 故事列表
    st.subheader("📚 故事列表")
    
    stories = db_manager.list_stories(limit=100)
    
    if stories:
        # 创建DataFrame
        df = pd.DataFrame(stories)
        
        # 格式化时间
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # 显示表格
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "idiom": "成语",
                "story_text": "故事内容",
                "created_at": "创建时间",
                "updated_at": "更新时间",
                "scene_count": "场景数",
                "image_count": "图片数",
                "audio_count": "音频数",
                "video_count": "视频数"
            }
        )
        
        # 操作按钮
        st.subheader("🔧 操作")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 刷新数据"):
                st.rerun()
        
        with col2:
            if st.button("🗑️ 清理缓存"):
                # 这里可以添加清理逻辑
                st.info("缓存清理功能待实现")
        
        with col3:
            if st.button("📤 导出数据"):
                st.info("数据导出功能待实现")
        
        # 删除故事
        st.subheader("🗑️ 删除故事")
        
        selected_idiom = st.selectbox(
            "选择要删除的故事:",
            [story['idiom'] for story in stories],
            key="delete_story_select"
        )
        
        if st.button("删除选中的故事", type="secondary"):
            if db_manager.delete_story(selected_idiom):
                st.success(f"故事 '{selected_idiom}' 已删除")
                st.rerun()
            else:
                st.error("删除失败")
    
    else:
        st.info("暂无故事数据")
    
    # 数据库文件信息
    st.subheader("📁 数据库文件信息")
    
    db_path = Path("idiom_cache.db")
    if db_path.exists():
        db_size = db_path.stat().st_size
        st.info(f"数据库文件大小: {db_size / 1024 / 1024:.2f} MB")
        
        # 显示存储目录结构
        storage_dir = Path("storage")
        if storage_dir.exists():
            st.subheader("📂 存储目录结构")
            
            def show_directory_tree(path, level=0):
                indent = "  " * level
                if path.is_dir():
                    st.text(f"{indent}📁 {path.name}/")
                    for child in sorted(path.iterdir()):
                        show_directory_tree(child, level + 1)
                else:
                    size = path.stat().st_size
                    st.text(f"{indent}📄 {path.name} ({size / 1024:.1f} KB)")
            
            show_directory_tree(storage_dir)
    else:
        st.warning("数据库文件不存在")

def show_story_detail(idiom: str):
    """显示故事详情"""
    story = db_manager.get_story(idiom)
    
    if not story:
        st.error(f"未找到故事: {idiom}")
        return
    
    st.title(f"📖 {idiom}")
    
    # 基本信息
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("创建时间", story['created_at'])
    
    with col2:
        st.metric("更新时间", story['updated_at'])
    
    # 故事内容
    st.subheader("📝 故事内容")
    st.text_area("", story['story_text'], height=200, disabled=True)
    
    # 场景列表
    st.subheader("🎬 场景列表")
    for i, scene in enumerate(story['scenes'], 1):
        with st.expander(f"场景 {i}"):
            st.text(scene)
    
    # 图片展示
    if story['images']:
        st.subheader("🖼️ 生成的图片")
        
        for img_info in story['images']:
            img_path = Path(img_info['path'])
            if img_path.exists():
                st.image(str(img_path), caption=img_info['filename'])
            else:
                st.warning(f"图片文件不存在: {img_info['filename']}")
    
    # 音频和视频
    col1, col2 = st.columns(2)
    
    with col1:
        if story['audio']:
            st.subheader("🔊 音频文件")
            audio_info = story['audio']
            st.info(f"文件名: {audio_info['filename']}")
            st.info(f"大小: {audio_info['size'] / 1024:.1f} KB")
            
            audio_path = Path(audio_info['path'])
            if audio_path.exists():
                st.audio(str(audio_path))
            else:
                st.warning("音频文件不存在")
    
    with col2:
        if story['video']:
            st.subheader("🎥 视频文件")
            video_info = story['video']
            st.info(f"文件名: {video_info['filename']}")
            st.info(f"大小: {video_info['size'] / 1024 / 1024:.1f} MB")
            
            video_path = Path(video_info['path'])
            if video_path.exists():
                st.video(str(video_path))
            else:
                st.warning("视频文件不存在")

if __name__ == "__main__":
    st.set_page_config(
        page_title="数据库管理",
        page_icon="📊",
        layout="wide"
    )
    
    show_database_management()

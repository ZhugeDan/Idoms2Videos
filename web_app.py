#!/usr/bin/env python3
"""
独立的Web应用 - 使用Flask + 自定义HTML
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
from pathlib import Path
from PIL import Image
import io
import json

# 导入后端模块
from flask_backend import backend

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/generate-story', methods=['POST'])
def generate_story():
    """生成故事API"""
    try:
        data = request.get_json()
        idiom = data.get('idiom', '')
        
        if not idiom:
            return jsonify({'error': '请输入成语'}), 400
        
        # 生成故事
        story_text = backend.generate_story_text(idiom)
        
        return jsonify({
            'success': True,
            'story': story_text,
            'idiom': idiom
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-images', methods=['POST'])
def generate_images():
    """生成图片API"""
    try:
        data = request.get_json()
        story_text = data.get('story', '')
        idiom = data.get('idiom', '')
        
        if not story_text:
            return jsonify({'error': '故事内容为空'}), 400
        
        # 提取场景
        scenes = backend.extract_scenes(story_text)
        
        # 生成图片
        images = backend.generate_story_images(scenes, idiom)
        
        # 转换图片为base64
        image_data = []
        for i, img in enumerate(images):
            if hasattr(img, 'save'):
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                image_data.append({
                    'index': i,
                    'data': f"data:image/jpeg;base64,{img_str}",
                    'scene': scenes[i] if i < len(scenes) else ""
                })
        
        return jsonify({
            'success': True,
            'images': image_data,
            'scenes': scenes
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    """生成音频API"""
    try:
        data = request.get_json()
        story_text = data.get('story', '')
        idiom = data.get('idiom', '')
        
        if not story_text:
            return jsonify({'error': '故事内容为空'}), 400
        
        # 生成音频
        audio = backend.generate_story_audio(story_text, idiom)
        
        # 音频已经在后端保存了，获取保存路径
        audio_path = f"output_audio/{idiom}_01.mp3"
        
        return jsonify({
            'success': True,
            'audio_path': audio_path,
            'message': '音频生成完成'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-video', methods=['POST'])
def create_video():
    """创建视频API"""
    try:
        data = request.get_json()
        images = data.get('images', [])
        audio_path = data.get('audio_path', '')
        idiom = data.get('idiom', '')
        video_style = data.get('video_style', 'simple')
        transition_type = data.get('transition_type', 'fade')
        
        if not images:
            return jsonify({'error': '没有图片'}), 400
        
        # 创建视频
        video_path = backend.create_video(
            images, audio_path, idiom, video_style, transition_type
        )
        
        return jsonify({
            'success': True,
            'video_path': video_path,
            'message': '视频创建完成'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files')
def get_files():
    """获取生成的文件列表"""
    try:
        files = {
            'images': [],
            'audio': [],
            'videos': []
        }
        
        # 获取图片文件
        pic_dir = Path("output_pic")
        if pic_dir.exists():
            files['images'] = [f.name for f in pic_dir.glob("*.jpg")]
        
        # 获取音频文件
        audio_dir = Path("output_audio")
        if audio_dir.exists():
            files['audio'] = [f.name for f in audio_dir.glob("*.mp3")]
        
        # 获取视频文件
        video_dir = Path("output")
        if video_dir.exists():
            files['videos'] = [f.name for f in video_dir.glob("*.mp4")]
        
        return jsonify(files)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """下载文件"""
    try:
        # 查找文件
        for directory in ["output_pic", "output_audio", "output"]:
            file_path = Path(directory) / filename
            if file_path.exists():
                return send_file(str(file_path), as_attachment=True)
        
        return jsonify({'error': '文件不存在'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 创建模板目录
    os.makedirs('templates', exist_ok=True)
    
    # 运行应用
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
测试修复版组件
"""
from fixed_audio_generator import fixed_audio_generator
from fixed_video_composer import fixed_video_composer
import os

def test_audio_generation():
    """测试音频生成"""
    print("🧪 测试修复版音频生成...")
    
    test_text = "这是一个测试文本，用于验证音频生成功能。"
    idiom = "测试成语"
    
    audio_path = fixed_audio_generator.generate_story_audio(test_text, idiom)
    
    if audio_path and os.path.exists(audio_path):
        print(f"✅ 音频生成成功: {audio_path}")
        return audio_path
    else:
        print("❌ 音频生成失败")
        return None

def test_video_generation():
    """测试视频生成"""
    print("🧪 测试修复版视频生成...")
    
    # 创建测试图片列表（这里用None代替，实际应该是PIL Image对象）
    test_images = [None] * 3  # 模拟3张图片
    
    test_audio = "test_audio.mp3"  # 假设存在音频文件
    
    if os.path.exists(test_audio):
        video_path = fixed_video_composer.create_video(test_images, test_audio, "测试成语")
        
        if video_path and os.path.exists(video_path):
            print(f"✅ 视频生成成功: {video_path}")
            return video_path
        else:
            print("❌ 视频生成失败")
            return None
    else:
        print("⚠️ 测试音频文件不存在，跳过视频测试")
        return None

def main():
    """主测试函数"""
    print("🔧 测试修复版组件...")
    
    # 测试音频生成
    audio_path = test_audio_generation()
    
    # 测试视频生成（如果有音频文件）
    if audio_path:
        test_video_generation()
    
    print("✅ 测试完成!")

if __name__ == "__main__":
    main()

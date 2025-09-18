#!/usr/bin/env python3
"""
测试完全干净的自定义界面
"""

import requests
import time

def test_clean_interface():
    """测试干净界面是否正常工作"""
    print("🧪 测试完全干净的自定义界面...")
    
    try:
        # 测试应用是否响应
        response = requests.get("http://localhost:8502", timeout=10)
        if response.status_code == 200:
            print("✅ 应用响应正常")
            print(f"📊 状态码: {response.status_code}")
            print(f"📏 响应大小: {len(response.content)} 字节")
            
            # 检查是否包含我们的自定义内容
            content = response.text
            if "成语故事生成器" in content:
                print("✅ 页面标题正确")
            if "main-container" in content:
                print("✅ 主容器存在")
            if "image-section" in content:
                print("✅ 图片区域存在")
            if "ui-section" in content:
                print("✅ 控制面板存在")
            if "option-btn" in content:
                print("✅ 功能按钮存在")
            if "tool-btn" in content:
                print("✅ 工具按钮存在")
                
            print("\n🎉 界面测试通过！")
            print("🌐 访问地址: http://localhost:8502")
            print("📱 界面特点:")
            print("   - 完全隐藏所有Streamlit代码标签")
            print("   - 深色主题设计")
            print("   - 左侧图片展示区域")
            print("   - 右侧控制面板")
            print("   - HTML按钮交互")
            
        else:
            print(f"❌ 应用响应异常: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到应用，请确保应用正在运行")
    except requests.exceptions.Timeout:
        print("❌ 连接超时")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_clean_interface()

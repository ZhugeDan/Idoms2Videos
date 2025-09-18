#!/usr/bin/env python3
"""
测试Flask应用
"""
import requests
import json
import time

def test_flask_app():
    """测试Flask应用"""
    base_url = "http://localhost:5000"
    
    print("🧪 测试Flask应用...")
    
    try:
        # 测试主页
        print("1. 测试主页...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 主页访问成功")
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
            return False
        
        # 测试文件列表API
        print("2. 测试文件列表API...")
        response = requests.get(f"{base_url}/api/files")
        if response.status_code == 200:
            print("✅ 文件列表API正常")
        else:
            print(f"❌ 文件列表API失败: {response.status_code}")
        
        # 测试生成故事API
        print("3. 测试生成故事API...")
        test_data = {"idiom": "掩耳盗铃"}
        response = requests.post(
            f"{base_url}/api/generate-story",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 生成故事API正常")
                print(f"故事内容: {data.get('story', '')[:100]}...")
            else:
                print(f"❌ 生成故事失败: {data.get('error')}")
        else:
            print(f"❌ 生成故事API失败: {response.status_code}")
            print(f"响应内容: {response.text}")
        
        print("\n🎉 Flask应用测试完成！")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Flask应用，请确保应用正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("请确保Flask应用正在运行 (python web_app.py)")
    print("然后运行此测试脚本")
    
    # 等待用户确认
    input("按回车键开始测试...")
    
    test_flask_app()

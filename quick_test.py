#!/usr/bin/env python3
"""
快速测试Flask应用
"""
import requests
import json

def quick_test():
    """快速测试"""
    try:
        # 测试生成故事API
        print("🧪 测试生成故事API...")
        
        test_data = {"idiom": "掩耳盗铃"}
        response = requests.post(
            "http://localhost:5000/api/generate-story",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 生成故事成功！")
                print(f"故事内容: {data.get('story', '')[:200]}...")
                return True
            else:
                print(f"❌ 生成故事失败: {data.get('error')}")
                return False
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Flask应用")
        print("请确保Flask应用正在运行: python web_app.py")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    quick_test()

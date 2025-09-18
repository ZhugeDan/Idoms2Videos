"""
测试数据库功能
"""
from database_manager import db_manager
import os

def test_database():
    """测试数据库功能"""
    print("🧪 测试数据库功能...")
    
    # 测试保存故事
    idiom = "刻舟求剑"
    story_text = "从前有个人坐船过河，不小心把剑掉到河里了。他在船上刻了个记号，以为这样就能找到剑。"
    scenes = [
        "一个人坐在船上",
        "剑掉到河里",
        "在船上刻记号",
        "以为能找到剑"
    ]
    
    print(f"📝 保存故事: {idiom}")
    story_id = db_manager.save_story(idiom, story_text, scenes)
    print(f"✅ 故事ID: {story_id}")
    
    # 测试获取故事
    print(f"📖 获取故事: {idiom}")
    story = db_manager.get_story(idiom)
    if story:
        print(f"✅ 找到故事: {story['idiom']}")
        print(f"   场景数量: {len(story['scenes'])}")
    else:
        print("❌ 未找到故事")
    
    # 测试列出故事
    print("📚 列出所有故事:")
    stories = db_manager.list_stories(limit=10)
    for story in stories:
        print(f"  - {story['idiom']}: {story['story_text'][:50]}...")
    
    # 测试存储统计
    print("📊 存储统计:")
    stats = db_manager.get_storage_stats()
    print(f"  故事数量: {stats['story_count']}")
    print(f"  总大小: {stats['total_size'] / 1024:.1f} KB")
    
    print("✅ 数据库测试完成!")

if __name__ == "__main__":
    test_database()

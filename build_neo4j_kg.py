#!/usr/bin/env python3
"""
Neo4j知识图谱构建脚本
用于构建基于诗词数据的Neo4j知识图谱
"""

import os
import json
from typing import List, Dict
from app.core.config import settings
from app.services.neo4j_kg_service import AsyncNeo4jKnowledgeGraphService

async def load_poems_from_json(json_file: str) -> List[Dict]:
    """从JSON文件加载诗词数据"""
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

async def load_poems_from_directory(directory: str) -> List[Dict]:
    """从目录加载所有诗词数据"""
    all_poems = []
    
    # 加载JSON文件
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            poems = await load_poems_from_json(file_path)
            all_poems.extend(poems)
    
    return all_poems

async def build_neo4j_knowledge_graph():
    """构建Neo4j知识图谱"""
    print("开始构建Neo4j知识图谱...")
    
    # 初始化服务
    kg_service = AsyncNeo4jKnowledgeGraphService()
    
    try:
        # 加载诗词数据
        print("加载诗词数据...")
        poems = await load_poems_from_directory(settings.RAW_DATA_PATH)
        print(f"加载了 {len(poems)} 首诗词")
        
        if not poems:
            print("没有找到诗词数据，使用示例数据")
            # 创建一些示例数据
            sample_poems = [
                {
                    "id": "tang001",
                    "title": "静夜思",
                    "author": "李白",
                    "dynasty": "唐代",
                    "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                    "translation": "明亮的月光洒在床前，好像地上泛起了一层白霜。抬起头来望着天上的明月，不由得低头沉思，想起了故乡。",
                    "theme": "思乡",
                    "emotions": ["思念", "孤独"],
                    "background": "李白在旅途中思念家乡所作"
                },
                {
                    "id": "tang002",
                    "title": "春晓",
                    "author": "孟浩然",
                    "dynasty": "唐代",
                    "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
                    "translation": "春天睡醒不觉得天已破晓，到处都能听到鸟儿的啼叫声。想起昨夜的风声雨声，不知吹落了多少花朵。",
                    "theme": "春天",
                    "emotions": ["愉悦", "感慨"],
                    "background": "描绘春日清晨的美景"
                },
                {
                    "id": "tang003",
                    "title": "登鹳雀楼",
                    "author": "王之涣",
                    "dynasty": "唐代",
                    "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
                    "translation": "夕阳依傍着山峦慢慢沉落，滔滔黄河朝着大海汹涌奔流。想要看到千里之外的风光，那就要再登上更高的一层城楼。",
                    "theme": "哲理",
                    "emotions": ["豪迈", "励志"],
                    "background": "诗人登楼远眺有感而发"
                }
            ]
            poems = sample_poems
        
        # 构建知识图谱
        print("构建知识图谱...")
        success = await kg_service.build_knowledge_graph(poems)
        
        if success:
            print("知识图谱构建成功！")
            
            # 显示统计信息
            stats = await kg_service.get_knowledge_graph_statistics()
            print("知识图谱统计信息:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        else:
            print("知识图谱构建失败！")
            
    except Exception as e:
        print(f"构建知识图谱时出错: {e}")
    finally:
        # 关闭连接
        await kg_service.close_connections()

async def main():
    """主函数"""
    print("开始构建Neo4j知识图谱...")
    
    await build_neo4j_knowledge_graph()
    
    print("Neo4j知识图谱构建完成！")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
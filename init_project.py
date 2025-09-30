#!/usr/bin/env python3
"""
项目初始化脚本
用于创建必要的目录结构和初始化数据
"""

import os
import shutil
from app.core.config import settings

def create_directory_structure():
    """创建项目目录结构"""
    directories = [
        settings.RAW_DATA_PATH,
        settings.PROCESSED_DATA_PATH,
        settings.KNOWLEDGE_GRAPH_PATH,
        settings.VECTOR_DB_PATH
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"创建目录: {directory}")

def create_sample_data():
    """创建示例数据文件"""
    # 创建示例诗词数据
    sample_poems = [
        {
            "id": "tang001",
            "title": "静夜思",
            "author": "李白",
            "dynasty": "唐代",
            "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
            "translation": "明亮的月光洒在床前，好像地上泛起了一层白霜。抬起头来望着天上的明月，不由得低头沉思，想起了故乡。",
            "theme": "思乡",
            "emotions": ["思念", "孤独"]
        },
        {
            "id": "tang002",
            "title": "春晓",
            "author": "孟浩然",
            "dynasty": "唐代",
            "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
            "translation": "春天睡醒不觉得天已破晓，到处都能听到鸟儿的啼叫声。想起昨夜的风声雨声，不知吹落了多少花朵。",
            "theme": "春天",
            "emotions": ["愉悦", "感慨"]
        }
    ]
    
    # 保存示例数据
    import json
    sample_file = os.path.join(settings.RAW_DATA_PATH, "sample_poems.json")
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_poems, f, ensure_ascii=False, indent=2)
    
    print(f"创建示例数据文件: {sample_file}")

def main():
    """主函数"""
    print("开始初始化古诗词RAG项目...")
    
    # 创建目录结构
    create_directory_structure()
    
    # 创建示例数据
    create_sample_data()
    
    print("项目初始化完成！")
    print("\n下一步操作：")
    print("1. 安装依赖: pip install -r requirements.txt")
    print("2. 配置环境变量: 复制 .env.example 为 .env 并填写配置")
    print("3. 运行后端服务: python run.py")
    print("4. 运行前端界面: streamlit run frontend/streamlit_app.py")

if __name__ == "__main__":
    main()
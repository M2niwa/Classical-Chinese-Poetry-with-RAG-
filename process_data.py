#!/usr/bin/env python3
"""
数据处理脚本
用于处理原始数据并构建向量数据库
"""

import os
import json
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.core.config import settings
from app.utils.pdf_processor import PDFProcessor

def load_poems_from_json(json_file: str) -> List[Dict]:
    """从JSON文件加载诗词数据"""
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_poems_from_directory(directory: str) -> List[Dict]:
    """从目录加载所有诗词数据"""
    all_poems = []
    
    # 加载JSON文件
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            poems = load_poems_from_json(file_path)
            all_poems.extend(poems)
    
    return all_poems

def create_documents_from_poems(poems: List[Dict]) -> List[Document]:
    """从诗词数据创建文档"""
    documents = []
    
    for poem in poems:
        # 创建文档内容
        content = f"诗词标题: {poem['title']}\n作者: {poem['author']}\n朝代: {poem['dynasty']}\n内容: {poem['content']}"
        if poem.get('translation'):
            content += f"\n译文: {poem['translation']}"
        if poem.get('annotation'):
            content += f"\n注释: {poem['annotation']}"
        if poem.get('background'):
            content += f"\n创作背景: {poem['background']}"
        
        # 创建文档
        doc = Document(
            page_content=content,
            metadata={
                "id": poem["id"],
                "title": poem["title"],
                "author": poem["author"],
                "dynasty": poem["dynasty"],
                "theme": poem.get("theme", ""),
                "emotions": ",".join(poem.get("emotions", []))
            }
        )
        documents.append(doc)
    
    return documents

def build_vector_database():
    """构建向量数据库"""
    print("开始构建向量数据库...")
    
    # 初始化嵌入模型
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base=settings.OPENAI_API_BASE,
        model=settings.EMBEDDING_MODEL
    )
    
    # 加载诗词数据
    print("加载诗词数据...")
    poems = load_poems_from_directory(settings.RAW_DATA_PATH)
    print(f"加载了 {len(poems)} 首诗词")
    
    if not poems:
        print("没有找到诗词数据，使用示例数据")
        # 创建一些示例文档
        sample_docs = [
            Document(
                page_content="静夜思 李白 床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                metadata={"id": "tang001", "title": "静夜思", "author": "李白", "dynasty": "唐代"}
            ),
            Document(
                page_content="春晓 孟浩然 春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
                metadata={"id": "tang002", "title": "春晓", "author": "孟浩然", "dynasty": "唐代"}
            )
        ]
        documents = sample_docs
    else:
        # 创建文档
        documents = create_documents_from_poems(poems)
    
    # 分割文档
    print("分割文档...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(documents)
    print(f"分割成 {len(splits)} 个文档片段")
    
    # 创建向量数据库
    print("创建向量数据库...")
    vector_store = FAISS.from_documents(splits, embeddings)
    
    # 保存向量数据库
    print("保存向量数据库...")
    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    vector_store.save_local(settings.VECTOR_DB_PATH)
    
    print("向量数据库构建完成！")

def process_pdf_files():
    """处理PDF文件"""
    print("处理PDF文件...")
    
    pdf_dir = os.path.join(settings.RAW_DATA_PATH, "pdf")
    if not os.path.exists(pdf_dir):
        print(f"PDF目录不存在: {pdf_dir}")
        return
    
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"处理PDF文件: {pdf_path}")
            
            try:
                poems = PDFProcessor.process_poetry_collection(pdf_path)
                if poems:
                    # 保存提取的诗词数据
                    output_file = os.path.join(
                        settings.PROCESSED_DATA_PATH, 
                        f"{os.path.splitext(filename)[0]}_extracted.json"
                    )
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(poems, f, ensure_ascii=False, indent=2)
                    print(f"保存提取数据到: {output_file}")
            except Exception as e:
                print(f"处理PDF文件失败 {pdf_path}: {e}")

def main():
    """主函数"""
    print("开始数据处理...")
    
    # 处理PDF文件
    process_pdf_files()
    
    # 构建向量数据库
    build_vector_database()
    
    print("数据处理完成！")

if __name__ == "__main__":
    main()
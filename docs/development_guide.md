# Development Guide for Classical Chinese Poetry RAG System 古典诗词RAG系统开发指南

## Project Overview 项目概述

This project is a Retrieval-Augmented Generation (RAG) system for classical Chinese poetry with the following core features:
本项目是一个古典诗词检索增强生成系统，具有以下核心功能：

- Poetry retrieval (keyword + semantic search) 诗词检索（关键词+语义搜索）
- Sentiment analysis 情感分析
- Knowledge graph visualization 知识图谱展示
- Educational scenario adaptation 教学场景适配
- Multimodal content support 多模态内容支持

## Technology Architecture 技术架构

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Streamlit     │    │    FastAPI       │    │  LangChain RAG   │
│   Frontend      │◄──►│   Backend API    │◄──►│   Framework      │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌──────────────────┐
                    │ Vector Database  │    │  Large Language  │
                    │ (FAISS/Chroma)   │    │  Model (OpenAI)  │
                    └──────────────────┘    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Knowledge Graph  │
                    │ (Neo4j)          │
                    └──────────────────┘
```

## Environment Setup 环境搭建

### 1. Python Environment Preparation Python环境准备

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. Environment Variable Configuration 环境变量配置

Copy [.env.example](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/.env.example) to `.env` and fill in the configuration:
复制 [.env.example](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/.env.example) 文件为 `.env` 并填写相应配置：

```bash
cp .env.example .env
```

Main parameters to configure 需要配置的主要参数：
- `OPENAI_API_KEY`: OpenAI API key OpenAI API密钥
- `OPENAI_API_BASE`: API base URL (proxy support) API基础URL（支持代理）
- `OPENAI_MODEL`: Model name to use 使用的模型名称
- `NEO4J_URI`: Neo4j database URI Neo4j数据库URI
- `NEO4J_USER`: Neo4j username Neo4j用户名
- `NEO4J_PASSWORD`: Neo4j password Neo4j密码
- `REDIS_HOST`: Redis host Redis主机
- `REDIS_PORT`: Redis port Redis端口

## Data Preparation 数据准备

### 1. Data Sources 数据源

You can obtain classical Chinese poetry data from the following public datasets:
可以从以下公开数据集获取古典诗词数据：

- [Chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) GitHub repository [Chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) GitHub仓库
- Ancient literature digitization projects 古籍数字化项目
- Public poetry datasets from educational departments 教育部门公开的诗词数据集

### 2. Data Processing Workflow 数据处理流程

```python
# Example: Processing poetry data
from app.utils.pdf_processor import PDFProcessor

# Process PDF files
poems = PDFProcessor.process_poetry_collection("data/raw/sample.pdf")
```

```python
# 示例：处理诗词数据
from app.utils.pdf_processor import PDFProcessor

# 处理PDF文件
poems = PDFProcessor.process_poetry_collection("data/raw/sample.pdf")
```

## Core Module Development 核心模块开发

### 1. RAG Service Implementation RAG服务实现

Implemented in [app/services/rag_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/rag_service.py):
在 [app/services/rag_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/rag_service.py) 中实现：

- Document loading and chunking 文档加载和分块
- Vectorization processing 向量化处理
- Similarity retrieval 相似性检索
- Answer generation 答案生成

### 2. Knowledge Graph Construction 知识图谱构建

Implemented in [app/services/neo4j_kg_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/neo4j_kg_service.py):
在 [app/services/neo4j_kg_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/neo4j_kg_service.py) 中实现：

- Entity recognition and extraction 实体识别和抽取
- Relationship construction 关系构建
- Graph storage and querying 图谱存储和查询

### 3. Sentiment Analysis Service 情感分析服务

Implemented in [app/services/sentiment_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/sentiment_service.py):
在 [app/services/sentiment_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/sentiment_service.py) 中实现：

- Using pre-trained models for sentiment analysis 使用预训练模型进行情感分析
- Result visualization 结果可视化

### 4. Cache Warmup Service 缓存预热服务

Implemented in [app/services/cache_warmup_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/cache_warmup_service.py):
在 [app/services/cache_warmup_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/cache_warmup_service.py) 中实现：

- Cache preheating for common queries 常见查询的缓存预热
- RAG search cache preheating RAG搜索缓存预热
- Cache statistics collection 缓存统计信息收集

### 5. Model Optimization Service 模型优化服务

Implemented in [app/services/model_optimization_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/model_optimization_service.py):
在 [app/services/model_optimization_service.py](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/app/services/model_optimization_service.py) 中实现：

- Optimized embedding models 优化的嵌入模型
- Optimized language models 优化的语言模型
- Prompt template optimization 提示模板优化
- Model performance benchmarking 模型性能基准测试

## Running the Project 运行项目

### 1. Start Backend Service 启动后端服务

```bash
python run.py
```

Or start directly with uvicorn:
或者使用uvicorn直接启动：

```bash
uvicorn app.main:app --reload
```

### 2. Start Frontend Interface 启动前端界面

```bash
streamlit run frontend/streamlit_app.py
```

## API Interface Documentation API接口说明

### Poetry Query 诗词查询
```
POST /api/v1/query
{
  "query": "Li Bai's homesick poems",
  "top_k": 5,
  "use_rag": true
}
```

```
POST /api/v1/query
{
  "query": "李白的思乡诗",
  "top_k": 5,
  "use_rag": true
}
```

### Get Poem Details 获取诗词详情
```
GET /api/v1/poems/{poem_id}
```

### Get Poet Information 获取诗人信息
```
GET /api/v1/poets/{poet_name}
```

## Development Task Breakdown 开发任务分解

1. **Data Collection and Processing Module 数据收集与处理模块**
   - Implement PDF parser 实现PDF解析器
   - Build poetry data structure 构建诗词数据结构
   - Data cleaning and standardization 数据清洗和标准化

2. **Vector Database Integration 向量数据库集成**
   - Select appropriate vector database (FAISS/Chroma) 选择合适的向量数据库（FAISS/Chroma）
   - Implement document embedding and storage 实现文档嵌入和存储
   - Build retrieval interface 构建检索接口

3. **RAG Process Implementation RAG流程实现**
   - Integrate LangChain 集成LangChain
   - Implement retrieval and generation process 实现检索和生成流程
   - Optimize prompt templates 优化提示词模板

4. **Knowledge Graph Construction 知识图谱构建**
   - Design graph data structure 设计图谱数据结构
   - Implement entity relationship extraction 实现实体关系抽取
   - Build query interface 构建查询接口

5. **Sentiment Analysis Module 情感分析模块**
   - Integrate pre-trained models 集成预训练模型
   - Implement sentiment classification 实现情感分类
   - Result visualization 结果可视化

6. **Frontend Interface Enhancement 前端界面完善**
   - Optimize user experience 优化用户体验
   - Implement knowledge graph visualization 实现知识图谱可视化
   - Add interactive features 添加交互功能

## Performance Optimization Recommendations 性能优化建议

1. **Retrieval Optimization 检索优化**
   - Use hybrid retrieval (keyword + semantic) 使用混合检索（关键词+语义）
   - Implement re-ranking mechanism 实现重排序机制
   - Cache popular query results 缓存热门查询结果

2. **Model Optimization 模型优化**
   - Fine-tune embedding models to adapt to classical poetry domain 微调嵌入模型以适应古典诗词领域
   - Use more efficient model inference 使用更高效的模型推理
   - Implement model caching 实现模型缓存

3. **System Optimization 系统优化**
   - Asynchronous processing of time-consuming operations 异步处理耗时操作
   - Implement data preloading 实现数据预加载
   - Optimize database queries 优化数据库查询

## Deployment Recommendations 部署建议

1. **Containerized Deployment 容器化部署**
   - Use Docker to package the application 使用Docker打包应用
   - Configure Nginx reverse proxy 配置Nginx反向代理
   - Implement load balancing 实现负载均衡

2. **Cloud Service Deployment 云服务部署**
   - Select appropriate cloud service provider 选择合适的云服务商
   - Configure CDN to accelerate static resources 配置CDN加速静态资源
   - Implement auto-scaling 实现自动扩缩容

## Future Extension Directions 后续扩展方向

1. **Functional Extensions 功能扩展**
   - Poetry creation assistance 诗词创作辅助
   - Poetry comparison analysis 诗词对比分析
   - Learning path recommendation 学习路径推荐

2. **Technical Upgrades 技术升级**
   - Integrate multimodal models 集成多模态模型
   - Implement voice interaction 实现语音交互
   - Support more languages 支持更多语言

3. **Application Scenarios 应用场景**
   - Educational training systems 教育培训系统
   - Cultural dissemination platforms 文化传播平台
   - Research and analysis tools 研究分析工具
# Classical Chinese Poetry RAG System 古典诗词RAG系统

A Retrieval-Augmented Generation (RAG) system for classical Chinese poetry with knowledge graph integration, semantic search, and educational applications. 一个集成知识图谱、语义搜索和教育应用的古典诗词检索增强生成系统。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-blue)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-orange)](https://github.com/hwchase17/langchain)

## Features 功能特性

### Multi-dimensional Poetry Database 多维度诗词数据库
- Integration of 100,000+ classical Chinese poems covering Tang poetry, Song lyrics, Yuan opera, and ancient texts
- 整合超过10万首古典诗词，涵盖唐诗、宋词、元曲和古文
- Complete information for each poem: annotations, author biographies, creation background, artistic features, and appreciation interpretation
- 每首诗词的完整信息：注释、作者生平、创作背景、艺术特色和赏析解读

### Knowledge Graph Integration 知识图谱集成
- Depth integration with Neo4j graph database for cultural knowledge representation
- 基于Neo4j图数据库的深度文化知识表示集成
- Enhanced entity types: Poet, Poem, Dynasty, Theme, Emotion, and more
- 增强的实体类型：诗人、诗词、朝代、主题、情感等
- Complex relationship modeling: creation, influence, thematic connections, and emotional expressions
- 复杂关系建模：创作、影响、主题关联和情感表达

### Hybrid Retrieval Mechanism 混合检索机制
- Combined keyword search with semantic vector search for optimal results
- 结合关键词搜索和语义向量搜索以获得最佳结果
- Re-ranking technology to improve search result relevance
- 重排序技术提升搜索结果相关性

### Educational Scenario Adaptation 教学场景适配
- Specialized prompt engineering for educational contexts
- 面向教学场景的专用提示工程
- Instructions like "provide annotations suitable for middle school students"
- "提供适合中学生的注释"等指令

### Multimodal Content Support 多模态内容支持
- Integration of poetry illustrations, calligraphy works, and recitation audio
- 整合诗词配图、书法作品和朗诵音频
- Visual knowledge graph representation for enhanced learning experience
- 可视化知识图谱表示提升学习体验

## Architecture 架构

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Streamlit  │    │   FastAPI    │    │ LangChain    │
│   Frontend  │◄──►│   Backend    │◄──►│ RAG Framework│
└─────────────┘    └──────────────┘    └──────────────┘
                     │                     │
                     ▼                     ▼
           ┌─────────────────┐   ┌─────────────────┐
           │ Vector Database │   │ LLM (OpenAI)    │
           │ (FAISS/Chroma)  │   │ Compatible      │
           └─────────────────┘   └─────────────────┘
                     │
                     ▼
           ┌─────────────────┐
           │ Knowledge Graph │
           │ (Neo4j)         │
           └─────────────────┘
                     │
                     ▼
           ┌─────────────────┐
           │ Cache (Redis)   │
           └─────────────────┘
```

## Tech Stack 技术栈

- **Backend**: FastAPI + LangChain
- **Vector Database**: FAISS/Chroma
- **LLM**: OpenAI API compatible (with proxy support)
- **Frontend**: Streamlit
- **Knowledge Graph**: Neo4j
- **Cache**: Redis
- **Data Processing**: pandas, PyPDF2
- **Sentiment Analysis**: SnowNLP

## Quick Start 快速开始

### 1. Environment Setup 环境准备

```bash
# Clone the repository
git clone <your-repo-url>
cd chinese-poetry-rag

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

### 2. Project Initialization 项目初始化

```bash
# Initialize project structure and sample data
python init_project.py
```

### 3. Environment Configuration 环境配置

Copy [.env.example](file:///d%3A/Users/79472/Desktop/%E5%AE%9E%E9%AA%8C%E4%B8%8E%E6%96%87%E6%A1%A3/RAG-test/.env.example) to `.env` and fill in the configuration:

```bash
cp .env.example .env
```

Edit `.env` file to configure:
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_API_BASE`: API base URL (proxy support)
- `OPENAI_MODEL`: Model name to use
- `NEO4J_URI`: Neo4j database URI
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port

### 4. Run the Application 运行应用

```bash
# Start backend service
python run.py

# In a new terminal, start frontend interface
streamlit run frontend/streamlit_app.py
```

## Project Structure 项目结构

```
.
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variable example
├── app/                                # FastAPI application
│   ├── __init__.py
│   ├── main.py                         # Application entry point
│   ├── api/                            # API routes
│   │   ├── __init__.py
│   │   └── routes.py                   # API route definitions
│   ├── core/                           # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py                   # Configuration management
│   │   └── logger.py                   # Logging configuration
│   ├── models/                         # Data models
│   │   ├── __init__.py
│   │   └── schemas.py                  # Pydantic models
│   ├── services/                       # Business logic
│   │   ├── __init__.py
│   │   ├── rag_service.py              # RAG core service
│   │   ├── neo4j_kg_service.py         # Neo4j knowledge graph service
│   │   └── sentiment_service.py        # Sentiment analysis service
│   └── utils/                          # Utility functions
│       ├── __init__.py
│       └── pdf_processor.py            # PDF processing utilities
├── data/                               # Data directory
│   ├── raw/                            # Raw data
│   ├── processed/                      # Processed data
│   └── knowledge_graph/                # Knowledge graph data
├── frontend/                           # Frontend interface
│   └── streamlit_app.py                # Streamlit frontend application
├── notebooks/                          # Jupyter notebooks
│   └── data_exploration.ipynb          # Data exploration notebook
└── docs/                               # Documentation
    ├── architecture.png                # Architecture diagram
    └── technical_documentation.md      # Technical documentation
```

## API Endpoints API接口

- `POST /api/v1/query` - Poetry query 诗词查询
- `GET /api/v1/poems/{poem_id}` - Get poem details 获取诗词详情
- `GET /api/v1/poets/{poet_name}` - Get poet information 获取诗人信息
- `POST /api/v1/sentiment` - Sentiment analysis 情感分析
- `GET /api/v1/themes/{theme}` - Search by theme 按主题搜索
- `GET /api/v1/emotions/{emotion}` - Search by emotion 按情感搜索
- `GET /api/v1/kg/statistics` - Knowledge graph statistics 知识图谱统计

## Development 开发

For detailed development guidelines, please refer to [docs/development_guide.md](docs/development_guide.md)

详细的开发指南，请参考 [docs/development_guide.md](docs/development_guide.md)

## License 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 详情请见 [LICENSE](LICENSE) 文件。
# Classical Chinese Poetry RAG System Project Structure 古诗词RAG系统项目结构

```
.
├── README.md                           # Project documentation 项目说明文档
├── requirements.txt                    # Python dependencies Python依赖包
├── .env.example                        # Environment variable example 环境变量示例文件
├── app/                                # FastAPI application FastAPI应用主目录
│   ├── __init__.py
│   ├── main.py                         # Application entry point 应用入口点
│   ├── api/                            # API routes API路由
│   │   ├── __init__.py
│   │   └── routes.py                   # API route definitions API路由定义
│   ├── core/                           # Core configuration 核心配置
│   │   ├── __init__.py
│   │   ├── config.py                   # Configuration management 配置管理
│   │   ├── logger.py                   # Logging configuration 日志配置
│   │   └── cache_manager.py            # Cache management 缓存管理
│   ├── models/                         # Data models 数据模型
│   │   ├── __init__.py
│   │   └── schemas.py                  # Pydantic models Pydantic模型
│   ├── services/                       # Business logic layer 业务逻辑层
│   │   ├── __init__.py
│   │   ├── rag_service.py              # RAG core service RAG核心服务
│   │   ├── neo4j_kg_service.py         # Neo4j knowledge graph service Neo4j知识图谱服务
│   │   └── sentiment_service.py        # Sentiment analysis service 情感分析服务
│   └── utils/                          # Utility functions 工具函数
│       ├── __init__.py
│       └── pdf_processor.py            # PDF processing utilities PDF处理工具
├── data/                               # Data directory 数据目录
│   ├── raw/                            # Raw data 原始数据
│   ├── processed/                      # Processed data 处理后的数据
│   └── knowledge_graph/                # Knowledge graph data 知识图谱数据
├── docs/                               # Documentation 文档
│   ├── technical_documentation.md      # Technical documentation 技术文档
│   ├── development_guide.md            # Development guide 开发指南
│   └── architecture.png                # Architecture diagram 架构图
├── frontend/                           # Frontend interface 前端界面
│   └── streamlit_app.py                # Streamlit frontend application Streamlit前端应用
├── notebooks/                          # Jupyter notebooks Jupyter笔记本
│   └── data_exploration.ipynb          # Data exploration notebook 数据探索笔记本
├── init_project.py                     # Project initialization script 项目初始化脚本
├── run.py                              # Application startup script 应用启动脚本
├── build_neo4j_kg.py                   # Neo4j knowledge graph builder Neo4j知识图谱构建器
└── process_data.py                     # Data processing script 数据处理脚本
```
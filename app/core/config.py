import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings:
    # API配置
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # OpenAI API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # 数据目录配置
    RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw")
    PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", "data/processed")
    KNOWLEDGE_GRAPH_PATH = os.getenv("KNOWLEDGE_GRAPH_PATH", "data/knowledge_graph")
    
    # 向量数据库配置
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "data/vector_db")
    
    # 代理配置
    HTTP_PROXY = os.getenv("HTTP_PROXY", "")
    HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")
    
    # RAG配置
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))
    
    # 前端配置
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))
    
    # Neo4j配置
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    # Redis配置
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

settings = Settings()
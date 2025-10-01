import asyncio
import logging
from typing import Dict, Any, List, Optional
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.models.schemas import Poem, SearchResult

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelOptimizationService:
    """模型优化服务"""
    
    def __init__(self):
        """初始化模型优化服务"""
        self.embeddings_cache = {}
        self.model_cache = {}
        self.prompt_cache = {}
        
    def get_optimized_embeddings(self) -> OpenAIEmbeddings:
        """获取优化的嵌入模型"""
        cache_key = f"embeddings_{settings.EMBEDDING_MODEL}"
        
        if cache_key not in self.embeddings_cache:
            self.embeddings_cache[cache_key] = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_API_BASE,
                model=settings.EMBEDDING_MODEL,
                # 优化参数
                chunk_size=1000,  # 增加批处理大小
                max_retries=3,    # 增加重试次数
            )
            
        return self.embeddings_cache[cache_key]
    
    def get_optimized_llm(self, temperature: float = 0.7) -> ChatOpenAI:
        """获取优化的语言模型"""
        cache_key = f"llm_{settings.OPENAI_MODEL}_{temperature}"
        
        if cache_key not in self.model_cache:
            self.model_cache[cache_key] = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_API_BASE,
                model_name=settings.OPENAI_MODEL,
                temperature=temperature,
                # 优化参数
                request_timeout=30,    # 设置请求超时
                max_retries=2,         # 设置重试次数
                streaming=False,       # 关闭流式输出以提高性能
            )
            
        return self.model_cache[cache_key]
    
    def get_optimized_prompt(self, prompt_type: str = "default") -> ChatPromptTemplate:
        """获取优化的提示模板"""
        cache_key = f"prompt_{prompt_type}"
        
        if cache_key not in self.prompt_cache:
            if prompt_type == "poetry_analysis":
                template = """你是一个古诗词专家，请根据以下诗词信息回答用户的问题。

相关诗词信息:
{context}

用户问题: {question}

请用简洁明了的语言回答，适合初中生理解。回答时请注意：
1. 保持语言通俗易懂
2. 适当添加注释帮助理解
3. 回答长度控制在200字以内"""
            elif prompt_type == "detailed_analysis":
                template = """你是一个古诗词研究专家，请对以下诗词进行详细分析。

诗词信息:
{context}

分析要求: {question}

请从以下几个方面进行分析：
1. 诗歌主题和情感
2. 艺术手法和修辞
3. 语言特色和风格
4. 文化背景和意义

请提供深入而全面的分析。"""
            else:
                template = """你是一个古诗词专家，请根据以下诗词信息回答用户的问题。

相关诗词信息:
{context}

用户问题: {question}

请用简洁明了的语言回答，适合初高中学生理解，但如果用户提供了年龄或年级，依照对应年龄的理解能力进行解析。"""
            
            self.prompt_cache[cache_key] = ChatPromptTemplate.from_template(template)
            
        return self.prompt_cache[cache_key]
    
    async def optimize_vector_store(self, vector_store: FAISS) -> FAISS:
        """优化向量数据库"""
        try:
            # 优化向量存储的索引
            if hasattr(vector_store, 'index') and hasattr(vector_store.index, 'make_direct_map'):
                vector_store.index.make_direct_map()
                logger.info("向量存储索引优化完成")
            
            return vector_store
        except Exception as e:
            logger.warning(f"向量存储优化失败: {e}")
            return vector_store
    
    def get_model_performance_config(self) -> Dict[str, Any]:
        """获取模型性能配置"""
        return {
            "embedding_model": {
                "model_name": settings.EMBEDDING_MODEL,
                "batch_size": 1000,
                "max_retries": 3,
                "timeout": 30
            },
            "language_model": {
                "model_name": settings.OPENAI_MODEL,
                "temperature": 0.7,
                "max_tokens": 500,
                "timeout": 30,
                "max_retries": 2
            },
            "optimization_features": {
                "caching_enabled": True,
                "batch_processing": True,
                "connection_pooling": True,
                "request_timeout": 30
            }
        }
    
    async def benchmark_models(self) -> Dict[str, Any]:
        """基准测试模型性能"""
        results = {
            "embeddings": {},
            "language_models": {}
        }
        
        try:
            # 测试嵌入模型性能
            embeddings = self.get_optimized_embeddings()
            test_texts = ["春风吹又生", "明月几时有", "床前明月光"]
            
            start_time = asyncio.get_event_loop().time()
            for text in test_texts:
                await asyncio.get_event_loop().run_in_executor(None, embeddings.embed_query, text)
            
            end_time = asyncio.get_event_loop().time()
            results["embeddings"]["avg_response_time"] = (end_time - start_time) / len(test_texts)
            results["embeddings"]["test_samples"] = len(test_texts)
            
            # 测试语言模型性能
            llm = self.get_optimized_llm()
            test_prompt = self.get_optimized_prompt()
            
            chain = (
                {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
                | test_prompt
                | llm
                | StrOutputParser()
            )
            
            test_context = "《静夜思》是李白的代表作之一。"
            test_question = "这首诗表达了什么情感？"
            
            start_time = asyncio.get_event_loop().time()
            await chain.ainvoke({"context": test_context, "question": test_question})
            end_time = asyncio.get_event_loop().time()
            
            results["language_models"]["avg_response_time"] = end_time - start_time
            
        except Exception as e:
            logger.error(f"模型基准测试失败: {e}")
        
        return results

# 全局实例
model_optimization_service = ModelOptimizationService()
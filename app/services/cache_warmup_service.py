import asyncio
import logging
from typing import List, Dict, Any
from app.core.cache_manager import cache_manager
from app.services.neo4j_kg_service import kg_service
from app.services.rag_service import RAGService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheWarmupService:
    """缓存预热服务"""
    
    def __init__(self):
        """初始化缓存预热服务"""
        self.rag_service = RAGService()
        self.neo4j_service = kg_service
    
    async def warmup_common_queries(self):
        """预热常见查询的缓存"""
        logger.info("开始缓存预热...")
        
        # 预热热门诗人信息
        popular_poets = ["李白", "杜甫", "白居易", "王维", "苏轼", "辛弃疾"]
        for poet in popular_poets:
            try:
                await self.neo4j_service.get_poet_info(poet)
                logger.info(f"预热诗人信息缓存: {poet}")
            except Exception as e:
                logger.warning(f"预热诗人 {poet} 信息失败: {e}")
        
        # 预热热门主题搜索
        popular_themes = ["思乡", "离别", "爱情", "山水", "哲理", "咏史"]
        for theme in popular_themes:
            try:
                await self.neo4j_service.search_poems_by_theme(theme, limit=5)
                logger.info(f"预热主题搜索缓存: {theme}")
            except Exception as e:
                logger.warning(f"预热主题 {theme} 搜索失败: {e}")
        
        # 预热热门情感搜索
        popular_emotions = ["思念", "愉悦", "忧愁", "愤怒", "感慨"]
        for emotion in popular_emotions:
            try:
                await self.neo4j_service.get_poems_by_emotion(emotion, limit=5)
                logger.info(f"预热情感搜索缓存: {emotion}")
            except Exception as e:
                logger.warning(f"预热情感 {emotion} 搜索失败: {e}")
        
        # 预热知识图谱统计信息
        try:
            await self.neo4j_service.get_knowledge_graph_statistics()
            logger.info("预热知识图谱统计信息缓存")
        except Exception as e:
            logger.warning(f"预热知识图谱统计信息失败: {e}")
        
        logger.info("缓存预热完成")
    
    async def warmup_rag_searches(self):
        """预热RAG搜索缓存"""
        logger.info("开始RAG搜索缓存预热...")
        
        # 预热常见搜索查询
        common_queries = [
            "李白的思乡诗",
            "杜甫的忧国忧民诗",
            "描写春天的古诗",
            "表达离别之情的诗句",
            "山水田园诗代表作"
        ]
        
        for query in common_queries:
            try:
                # 预热搜索结果
                results = await self.rag_service.async_search(query, top_k=3)
                logger.info(f"预热RAG搜索缓存: {query}")
                
                # 预热生成的答案
                if results:
                    await self.rag_service.async_generate_answer(query, results[:2])
                    logger.info(f"预热RAG答案生成缓存: {query}")
            except Exception as e:
                logger.warning(f"预热RAG搜索 {query} 失败: {e}")
        
        logger.info("RAG搜索缓存预热完成")
    
    async def warmup_all_caches(self):
        """预热所有缓存"""
        logger.info("开始全面缓存预热...")
        
        # 并发执行不同的预热任务
        await asyncio.gather(
            self.warmup_common_queries(),
            self.warmup_rag_searches()
        )
        
        logger.info("全面缓存预热完成")
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        # 这里可以实现缓存命中率、缓存大小等统计信息
        # 由于Redis客户端限制，这里简化实现
        return {
            "status": "Cache statistics collection not implemented",
            "note": "Redis client does not support direct statistics collection in this implementation"
        }
    
    async def clear_expired_cache(self):
        """清理过期缓存"""
        # Redis会自动清理过期缓存，这里可以实现手动清理逻辑
        logger.info("Redis会自动清理过期缓存")
        pass

# 全局实例
cache_warmup_service = CacheWarmupService()
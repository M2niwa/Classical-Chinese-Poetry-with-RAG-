from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.models.schemas import QueryRequest, QueryResponse, Poem
from app.services.rag_service import RAGService
from app.services.knowledge_graph_service import KnowledgeGraphService
from app.services.sentiment_service import SentimentService
from app.services.neo4j_kg_service import kg_service as neo4j_kg_service

class SentimentRequest(BaseModel):
    text: str

router = APIRouter()

# 初始化服务
rag_service = RAGService()
kg_service = KnowledgeGraphService()
sentiment_service = SentimentService()
neo4j_service = neo4j_kg_service

@router.post("/query", response_model=QueryResponse)
async def query_poems(request: QueryRequest):
    """诗词查询接口"""
    try:
        # 执行RAG检索（异步）
        results = await rag_service.async_search(request.query, request.top_k)
        
        # 生成答案（异步）
        answer = None
        if request.use_rag:
            answer = await rag_service.async_generate_answer(request.query, results)
        
        # 获取知识图谱信息（使用Neo4j）
        kg_data = await neo4j_service.get_related_entities(request.query)
        
        # 情感分析
        sentiment = None
        if results:
            # 对第一个结果进行情感分析
            sentiment = sentiment_service.analyze_sentiment(results[0].poem.content)
        
        return QueryResponse(
            results=results,
            knowledge_graph=kg_data,
            sentiment_analysis=sentiment,
            generated_answer=answer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/poems/{poem_id}")
async def get_poem(poem_id: str):
    """获取特定诗词详情"""
    poem = await rag_service.async_get_poem_by_id(poem_id)
    if not poem:
        raise HTTPException(status_code=404, detail="Poem not found")
    return poem

@router.get("/poets/{poet_name}")
async def get_poet_info(poet_name: str):
    """获取诗人信息及作品列表"""
    poet_info = await neo4j_service.get_poet_info(poet_name)
    if not poet_info:
        raise HTTPException(status_code=404, detail="Poet not found")
    return poet_info

@router.post("/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    """情感分析接口"""
    try:
        result = sentiment_service.analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/themes/{theme}")
async def search_poems_by_theme(theme: str, limit: int = 10):
    """根据主题搜索诗词"""
    try:
        poems = await neo4j_service.search_poems_by_theme(theme, limit)
        return poems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emotions/{emotion}")
async def search_poems_by_emotion(emotion: str, limit: int = 10):
    """根据情感搜索诗词"""
    try:
        poems = await neo4j_service.get_poems_by_emotion(emotion, limit)
        return poems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kg/statistics")
async def get_kg_statistics():
    """获取知识图谱统计信息"""
    try:
        stats = await neo4j_service.get_knowledge_graph_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
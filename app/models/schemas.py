from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Poem(BaseModel):
    """诗词数据模型"""
    id: str
    title: str
    author: str
    dynasty: str
    content: str
    translation: Optional[str] = None
    annotation: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None
    emotions: Optional[List[str]] = None

class SearchResult(BaseModel):
    """检索结果模型"""
    poem: Poem
    similarity_score: float
    source: str

class KnowledgeGraphNode(BaseModel):
    """知识图谱节点模型"""
    id: str
    name: str
    type: str  # poet, poem, dynasty, theme
    properties: Dict[str, Any]

class KnowledgeGraphEdge(BaseModel):
    """知识图谱边模型"""
    source: str
    target: str
    relation: str
    weight: float

class QueryRequest(BaseModel):
    """查询请求模型"""
    query: str
    top_k: int = 5
    use_rag: bool = True

class QueryResponse(BaseModel):
    """查询响应模型"""
    results: List[SearchResult]
    knowledge_graph: Optional[Dict[str, List]] = None
    sentiment_analysis: Optional[Dict[str, Any]] = None
    generated_answer: Optional[str] = None
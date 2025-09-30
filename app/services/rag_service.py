import os
import json
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.core.async_service import async_service
from app.models.schemas import Poem, SearchResult

class RAGService:
    """RAG核心服务"""
    
    def __init__(self):
        """初始化RAG服务"""
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE
        )
        
        # 初始化语言模型
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE,
            model_name=settings.OPENAI_MODEL,
            temperature=0.7
        )
        
        # 加载向量数据库
        self.vector_store = self._load_vector_store()
        
        # 初始化重排序器
        self._init_reranker()
        
        # 加载诗词数据
        self.poems_data = self._load_poems_data()
    
    def _load_vector_store(self):
        """加载向量数据库"""
        try:
            if os.path.exists(settings.VECTOR_DB_PATH):
                return FAISS.load_local(settings.VECTOR_DB_PATH, self.embeddings, allow_dangerous_deserialization=True)
            else:
                # 创建新的向量数据库
                return self._create_vector_store()
        except Exception as e:
            print(f"加载向量数据库失败: {e}")
            return None
    
    def _create_vector_store(self):
        """创建向量数据库"""
        # 这里应该从数据源创建向量数据库
        # 暂时返回None
        return None
    
    def _init_reranker(self):
        """初始化重排序器"""
        # TODO: 实现重排序逻辑
        pass
    
    def _load_poems_data(self) -> Dict[str, dict]:
        """加载诗词数据"""
        poems = {}
        
        # 加载示例数据
        sample_file = os.path.join(settings.RAW_DATA_PATH, "sample_poems.json")
        if os.path.exists(sample_file):
            with open(sample_file, 'r', encoding='utf-8') as f:
                sample_poems = json.load(f)
                for poem in sample_poems:
                    poems[poem["id"]] = poem
        
        return poems
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """搜索相关诗词"""
        results = []
        
        # 如果有向量数据库，执行向量搜索
        if self.vector_store:
            try:
                docs = self.vector_store.similarity_search_with_score(query, k=top_k)
                for doc, score in docs:
                    # 这里需要根据实际文档结构提取诗词信息
                    poem_data = {
                        "id": doc.metadata.get("id", "unknown"),
                        "title": doc.metadata.get("title", "未知"),
                        "author": doc.metadata.get("author", "未知"),
                        "dynasty": doc.metadata.get("dynasty", "未知"),
                        "content": doc.page_content
                    }
                    poem = Poem(**poem_data)
                    results.append(SearchResult(
                        poem=poem,
                        similarity_score=float(score),
                        source="向量检索"
                    ))
            except Exception as e:
                print(f"向量搜索失败: {e}")
        
        # 如果没有足够的结果，从本地数据中搜索
        if len(results) < top_k:
            # 简单的文本匹配
            query_lower = query.lower()
            matched_poems = []
            
            for poem_id, poem_data in self.poems_data.items():
                # 检查标题、作者、内容是否匹配查询
                if (query_lower in poem_data["title"].lower() or 
                    query_lower in poem_data["author"].lower() or 
                    query_lower in poem_data["content"].lower() or
                    any(keyword in poem_data["content"].lower() for keyword in query_lower.split())):
                    
                    matched_poems.append(poem_data)
            
            # 添加匹配的诗词到结果中
            for i, poem_data in enumerate(matched_poems[:top_k - len(results)]):
                poem = Poem(**poem_data)
                results.append(SearchResult(
                    poem=poem,
                    similarity_score=1.0 - (i * 0.1),  # 简单的相似度计算
                    source="关键词匹配"
                ))
        
        # 按相似度排序
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return results[:top_k]
    
    async def async_search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """异步搜索相关诗词"""
        # 使用异步服务包装同步搜索方法
        return await async_service.run_in_threadpool(self.search, query, top_k)
    
    def generate_answer(self, query: str, search_results: List[SearchResult]) -> str:
        """基于检索结果生成答案"""
        if not search_results:
            return "未找到相关诗词。"
        
        # 构建上下文
        context = "\n".join([
            f"诗词: {result.poem.title}\n作者: {result.poem.author}\n朝代: {result.poem.dynasty}\n内容: {result.poem.content}\n译文: {result.poem.translation or '无'}"
            for result in search_results
        ])
        
        # 创建提示模板
        template = """你是一个古诗词专家，请根据以下诗词信息回答用户的问题。

相关诗词信息:
{context}

用户问题: {question}

请用简洁明了的语言回答，适合初中生理解。"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # 创建处理链
        chain = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        try:
            answer = chain.invoke({"context": context, "question": query})
            return answer
        except Exception as e:
            print(f"生成答案失败: {e}")
            return "生成答案时出现错误。"
    
    async def async_generate_answer(self, query: str, search_results: List[SearchResult]) -> str:
        """异步生成答案"""
        # 使用异步服务包装同步生成方法
        return await async_service.run_in_threadpool(self.generate_answer, query, search_results)
    
    def get_poem_by_id(self, poem_id: str) -> Poem:
        """根据ID获取诗词"""
        poem_data = self.poems_data.get(poem_id)
        if poem_data:
            return Poem(**poem_data)
        return None
    
    async def async_get_poem_by_id(self, poem_id: str) -> Poem:
        """异步根据ID获取诗词"""
        # 使用异步服务包装同步方法
        return await async_service.run_in_threadpool(self.get_poem_by_id, poem_id)


import networkx as nx
from typing import Dict, List

class KnowledgeGraphService:
    """知识图谱服务"""
    
    def __init__(self):
        """初始化知识图谱服务"""
        self.graph = nx.Graph()
        self._build_knowledge_graph()
    
    def _build_knowledge_graph(self):
        """构建知识图谱"""
        # 添加示例节点和边
        # 诗人节点
        self.graph.add_node("李白", type="poet", dynasty="唐代", style="浪漫主义")
        self.graph.add_node("杜甫", type="poet", dynasty="唐代", style="现实主义")
        self.graph.add_node("孟浩然", type="poet", dynasty="唐代", style="山水田园")
        
        # 诗词节点
        self.graph.add_node("静夜思", type="poem", theme="思乡", emotion="思念")
        self.graph.add_node("春晓", type="poem", theme="春天", emotion="愉悦")
        
        # 朝代节点
        self.graph.add_node("唐代", type="dynasty", period="618-907")
        
        # 添加关系边
        self.graph.add_edge("李白", "静夜思", relation="创作")
        self.graph.add_edge("孟浩然", "春晓", relation="创作")
        self.graph.add_edge("李白", "唐代", relation="朝代")
        self.graph.add_edge("杜甫", "唐代", relation="朝代")
        self.graph.add_edge("孟浩然", "唐代", relation="朝代")
        self.graph.add_edge("静夜思", "思乡", relation="主题")
        self.graph.add_edge("春晓", "春天", relation="主题")
    
    def get_related_entities(self, query: str) -> Dict[str, List]:
        """获取相关实体"""
        # 简单的实体匹配
        related_entities = {
            "nodes": [],
            "edges": []
        }
        
        query_lower = query.lower()
        
        # 查找匹配的节点
        for node, attrs in self.graph.nodes(data=True):
            if query_lower in node.lower() or any(query_lower in str(v).lower() for v in attrs.values()):
                related_entities["nodes"].append({
                    "id": node,
                    "name": node,
                    "type": attrs.get("type", "unknown"),
                    "properties": attrs
                })
        
        # 查找相关的边
        for source, target, attrs in self.graph.edges(data=True):
            if query_lower in source.lower() or query_lower in target.lower():
                related_entities["edges"].append({
                    "source": source,
                    "target": target,
                    "relation": attrs.get("relation", "related")
                })
        
        return related_entities
    
    def get_poet_info(self, poet_name: str) -> Dict:
        """获取诗人信息"""
        if self.graph.has_node(poet_name):
            node_attrs = self.graph.nodes[poet_name]
            # 获取诗人的作品
            works = []
            for neighbor in self.graph.neighbors(poet_name):
                edge_data = self.graph.get_edge_data(poet_name, neighbor)
                if edge_data and edge_data.get("relation") == "创作":
                    works.append(neighbor)
            
            return {
                "name": poet_name,
                "dynasty": node_attrs.get("dynasty", "未知"),
                "style": node_attrs.get("style", "未知"),
                "lifetime": node_attrs.get("lifetime", "未知"),
                "bio": node_attrs.get("bio", f"{poet_name}是{node_attrs.get('dynasty', '某朝代')}著名诗人。"),
                "work_count": len(works),
                "works": works
            }
        
        return None


from snownlp import SnowNLP
from typing import Dict

class SentimentService:
    """情感分析服务"""
    
    def __init__(self):
        """初始化情感分析服务"""
        pass
    
    def analyze_sentiment(self, text: str) -> Dict:
        """分析文本情感"""
        try:
            # 使用SnowNLP进行情感分析
            s = SnowNLP(text)
            sentiment_score = s.sentiments
            
            # 判断情感倾向
            if sentiment_score > 0.6:
                sentiment = "积极"
            elif sentiment_score < 0.4:
                sentiment = "消极"
            else:
                sentiment = "中性"
            
            return {
                "sentiment": sentiment,
                "positive_prob": sentiment_score,
                "negative_prob": 1 - sentiment_score
            }
        except Exception as e:
            print(f"情感分析失败: {e}")
            return {
                "sentiment": "未知",
                "positive_prob": 0.0,
                "negative_prob": 0.0
            }
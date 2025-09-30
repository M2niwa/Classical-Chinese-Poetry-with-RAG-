from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.cache_manager import cache_manager
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncNeo4jKnowledgeGraphService:
    """异步Neo4j知识图谱服务"""
    
    def __init__(self):
        """初始化Neo4j连接"""
        # Neo4j连接配置
        self.neo4j_uri = settings.NEO4J_URI
        self.neo4j_user = settings.NEO4J_USER
        self.neo4j_password = settings.NEO4J_PASSWORD
        
        # 初始化连接
        self._init_connections()
    
    def _init_connections(self):
        """初始化数据库连接"""
        try:
            # 初始化Neo4j驱动
            self.neo4j_driver = GraphDatabase.driver(
                self.neo4j_uri, 
                auth=(self.neo4j_user, self.neo4j_password)
            )
            
            logger.info("数据库连接初始化成功")
        except Exception as e:
            logger.error(f"数据库连接初始化失败: {e}")
            raise
    
    # 缓存相关方法已移至cache_manager
    
    # 缓存相关方法已移至cache_manager
    
    # 缓存相关方法已移至cache_manager
    
    async def close_connections(self):
        """关闭数据库连接"""
        if self.neo4j_driver:
            await self.neo4j_driver.close()
    
    @cache_manager.cache(ttl=86400)  # 缓存24小时
    async def build_knowledge_graph(self, poems_data: List[Dict]) -> bool:
        """构建知识图谱"""
        try:
            async with self.neo4j_driver.session() as session:
                # 清空现有数据
                await session.run("MATCH (n) DETACH DELETE n")
                
                # 创建索引
                await session.run("CREATE INDEX IF NOT EXISTS FOR (p:Poet) ON (p.name)")
                await session.run("CREATE INDEX IF NOT EXISTS FOR (p:Poem) ON (p.title)")
                await session.run("CREATE INDEX IF NOT EXISTS FOR (d:Dynasty) ON (d.name)")
                await session.run("CREATE INDEX IF NOT EXISTS FOR (t:Theme) ON (t.name)")
                await session.run("CREATE INDEX IF NOT EXISTS FOR (e:Emotion) ON (e.name)")
                await session.run("CREATE INDEX IF NOT EXISTS FOR (i:Image) ON (i.name)")
                
                # 批量创建节点和关系
                for poem_data in poems_data:
                    # 创建诗人节点
                    await session.run("""
                        MERGE (poet:Poet {name: $author})
                        SET poet.dynasty = $dynasty
                        """, 
                        author=poem_data.get("author", ""),
                        dynasty=poem_data.get("dynasty", "")
                    )
                    
                    # 创建诗词节点
                    await session.run("""
                        MERGE (poem:Poem {title: $title, id: $id})
                        SET poem.content = $content,
                            poem.translation = $translation,
                            poem.annotation = $annotation,
                            poem.background = $background
                        """,
                        title=poem_data.get("title", ""),
                        id=poem_data.get("id", ""),
                        content=poem_data.get("content", ""),
                        translation=poem_data.get("translation", ""),
                        annotation=poem_data.get("annotation", ""),
                        background=poem_data.get("background", "")
                    )
                    
                    # 创建朝代节点
                    if poem_data.get("dynasty"):
                        await session.run("""
                            MERGE (dynasty:Dynasty {name: $dynasty})
                            """,
                            dynasty=poem_data.get("dynasty", "")
                        )
                    
                    # 创建主题节点
                    if poem_data.get("theme"):
                        await session.run("""
                            MERGE (theme:Theme {name: $theme})
                            """,
                            theme=poem_data.get("theme", "")
                        )
                    
                    # 创建情感节点
                    emotions = poem_data.get("emotions", [])
                    for emotion in emotions:
                        await session.run("""
                            MERGE (emotion:Emotion {name: $emotion})
                            """,
                            emotion=emotion
                        )
                    
                    # 创建创作关系
                    await session.run("""
                        MATCH (poet:Poet {name: $author})
                        MATCH (poem:Poem {title: $title, id: $id})
                        MERGE (poet)-[:CREATED]->(poem)
                        """,
                        author=poem_data.get("author", ""),
                        title=poem_data.get("title", ""),
                        id=poem_data.get("id", "")
                    )
                    
                    # 创建朝代关系
                    if poem_data.get("dynasty"):
                        await session.run("""
                            MATCH (poem:Poem {title: $title, id: $id})
                            MATCH (dynasty:Dynasty {name: $dynasty})
                            MERGE (poem)-[:BELONGS_TO]->(dynasty)
                            """,
                            title=poem_data.get("title", ""),
                            id=poem_data.get("id", ""),
                            dynasty=poem_data.get("dynasty", "")
                        )
                    
                    # 创建主题关系
                    if poem_data.get("theme"):
                        await session.run("""
                            MATCH (poem:Poem {title: $title, id: $id})
                            MATCH (theme:Theme {name: $theme})
                            MERGE (poem)-[:HAS_THEME]->(theme)
                            """,
                            title=poem_data.get("title", ""),
                            id=poem_data.get("id", ""),
                            theme=poem_data.get("theme", "")
                        )
                    
                    # 创建情感关系
                    for emotion in emotions:
                        await session.run("""
                            MATCH (poem:Poem {title: $title, id: $id})
                            MATCH (emotion:Emotion {name: $emotion})
                            MERGE (poem)-[:EXPRESSES]->(emotion)
                            """,
                            title=poem_data.get("title", ""),
                            id=poem_data.get("id", ""),
                            emotion=emotion
                        )
                
                return True
                
        except Exception as e:
            logger.error(f"构建知识图谱失败: {e}")
            return False
    
    @cache_manager.cache(ttl=3600)  # 缓存1小时
    async def get_related_entities(self, query: str, max_depth: int = 2) -> Dict:
        """获取相关实体"""
        try:
            async with self.neo4j_driver.session() as session:
                # 查询相关实体
                result = await session.run("""
                    CALL db.index.fulltext.queryNodes('entityIndex', $query) 
                    YIELD node, score
                    WHERE score > 0.1
                    WITH node, score
                    LIMIT 10
                    MATCH (node)-[r*1..$max_depth]-(related)
                    RETURN node, collect(DISTINCT related) as related_entities, 
                           collect(DISTINCT type(r[0])) as relationships, score
                    """,
                    query=query,
                    max_depth=max_depth
                )
                
                records = await result.data()
                entities_data = {
                    "nodes": [],
                    "edges": [],
                    "query": query
                }
                
                for record in records:
                    # 处理主节点
                    node = record["node"]
                    entities_data["nodes"].append({
                        "id": node.get("id", node.get("name", "")),
                        "name": node.get("name", node.get("title", "")),
                        "type": list(node.labels)[0] if node.labels else "Unknown",
                        "properties": dict(node)
                    })
                    
                    # 处理相关实体
                    for related in record["related_entities"]:
                        entities_data["nodes"].append({
                            "id": related.get("id", related.get("name", "")),
                            "name": related.get("name", related.get("title", "")),
                            "type": list(related.labels)[0] if related.labels else "Unknown",
                            "properties": dict(related)
                        })
                
                return entities_data
                
        except Exception as e:
            logger.error(f"查询相关实体失败: {e}")
            return {"nodes": [], "edges": [], "query": query}
    
    @cache_manager.cache(ttl=7200)  # 缓存2小时
    async def get_poet_info(self, poet_name: str) -> Dict:
        """获取诗人信息"""
        try:
            async with self.neo4j_driver.session() as session:
                # 查询诗人详细信息
                result = await session.run("""
                    MATCH (poet:Poet {name: $poet_name})
                    OPTIONAL MATCH (poet)-[:CREATED]->(poem:Poem)
                    OPTIONAL MATCH (poet)--(dynasty:Dynasty)
                    OPTIONAL MATCH (poem)-[:HAS_THEME]->(theme:Theme)
                    OPTIONAL MATCH (poem)-[:EXPRESSES]->(emotion:Emotion)
                    RETURN poet,
                           collect(DISTINCT poem) as poems,
                           collect(DISTINCT theme) as themes,
                           collect(DISTINCT emotion) as emotions,
                           collect(DISTINCT dynasty) as dynasties
                    """,
                    poet_name=poet_name
                )
                
                record = await result.single()
                if not record:
                    return {}
                
                poet = record["poet"]
                poems = record["poems"]
                themes = record["themes"]
                emotions = record["emotions"]
                dynasties = record["dynasties"]
                
                poet_info = {
                    "name": poet.get("name", ""),
                    "dynasty": dynasties[0].get("name", "") if dynasties else "",
                    "bio": poet.get("bio", f"{poet_name}是著名的古代诗人。"),
                    "lifetime": poet.get("lifetime", "生卒年不详"),
                    "style": poet.get("style", "风格不详"),
                    "work_count": len(poems),
                    "works": [poem.get("title", "") for poem in poems[:10]],  # 限制显示前10个作品
                    "themes": [theme.get("name", "") for theme in themes],
                    "emotions": [emotion.get("name", "") for emotion in emotions]
                }
                
                return poet_info
                
        except Exception as e:
            logger.error(f"查询诗人信息失败: {e}")
            return {}
    
    @cache_manager.cache(ttl=3600)  # 缓存1小时
    async def search_poems_by_theme(self, theme: str, limit: int = 10) -> List[Dict]:
        """根据主题搜索诗词"""
        try:
            async with self.neo4j_driver.session() as session:
                result = await session.run("""
                    MATCH (theme:Theme {name: $theme})<-[:HAS_THEME]-(poem:Poem)
                    OPTIONAL MATCH (poem)<-[:CREATED]-(poet:Poet)
                    RETURN poem, poet
                    LIMIT $limit
                    """,
                    theme=theme,
                    limit=limit
                )
                
                records = await result.data()
                poems = []
                
                for record in records:
                    poem = record["poem"]
                    poet = record.get("poet", {})
                    
                    poems.append({
                        "id": poem.get("id", ""),
                        "title": poem.get("title", ""),
                        "author": poet.get("name", "") if poet else "",
                        "dynasty": poet.get("dynasty", "") if poet else "",
                        "content": poem.get("content", ""),
                        "theme": theme
                    })
                
                return poems
                
        except Exception as e:
            logger.error(f"按主题搜索诗词失败: {e}")
            return []
    
    @cache_manager.cache(ttl=3600)  # 缓存1小时
    async def get_poems_by_emotion(self, emotion: str, limit: int = 10) -> List[Dict]:
        """根据情感搜索诗词"""
        try:
            async with self.neo4j_driver.session() as session:
                result = await session.run("""
                    MATCH (emotion:Emotion {name: $emotion})<-[:EXPRESSES]-(poem:Poem)
                    OPTIONAL MATCH (poem)<-[:CREATED]-(poet:Poet)
                    RETURN poem, poet
                    LIMIT $limit
                    """,
                    emotion=emotion,
                    limit=limit
                )
                
                records = await result.data()
                poems = []
                
                for record in records:
                    poem = record["poem"]
                    poet = record.get("poet", {})
                    
                    poems.append({
                        "id": poem.get("id", ""),
                        "title": poem.get("title", ""),
                        "author": poet.get("name", "") if poet else "",
                        "dynasty": poet.get("dynasty", "") if poet else "",
                        "content": poem.get("content", ""),
                        "emotion": emotion
                    })
                
                return poems
                
        except Exception as e:
            logger.error(f"按情感搜索诗词失败: {e}")
            return []
    
    @cache_manager.cache(ttl=1800)  # 缓存30分钟
    async def get_knowledge_graph_statistics(self) -> Dict:
        """获取知识图谱统计信息"""
        try:
            async with self.neo4j_driver.session() as session:
                # 查询各类节点数量
                poet_count = await session.run("MATCH (p:Poet) RETURN count(p) as count")
                poem_count = await session.run("MATCH (p:Poem) RETURN count(p) as count")
                dynasty_count = await session.run("MATCH (d:Dynasty) RETURN count(d) as count")
                theme_count = await session.run("MATCH (t:Theme) RETURN count(t) as count")
                emotion_count = await session.run("MATCH (e:Emotion) RETURN count(e) as count")
                
                stats = {
                    "poets": (await poet_count.single())["count"],
                    "poems": (await poem_count.single())["count"],
                    "dynasties": (await dynasty_count.single())["count"],
                    "themes": (await theme_count.single())["count"],
                    "emotions": (await emotion_count.single())["count"]
                }
                
                return stats
                
        except Exception as e:
            logger.error(f"获取知识图谱统计信息失败: {e}")
            return {}

# 全局实例
kg_service = AsyncNeo4jKnowledgeGraphService()
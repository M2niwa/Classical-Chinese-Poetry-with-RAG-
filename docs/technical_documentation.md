# Technical Documentation for Classical Chinese Poetry RAG System 古典诗词RAG系统技术文档

## System Architecture 系统架构

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
                    │  Neo4j Knowledge │
                    │     Graph        │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Redis Cache    │
                    │ (High Performance)│
                    └──────────────────┘
```

## Core Implementation 核心实现

### 1. Neo4j Knowledge Graph Service Neo4j知识图谱服务

#### Entity Types 实体类型
- **Poet (诗人)**: Contains attributes like name, dynasty, biography, and style
- **Poem (诗词)**: Contains attributes like title, content, translation, annotation, background, etc.
- **Dynasty (朝代)**: Contains attributes like name and period
- **Theme (主题)**: Classification of poem themes
- **Emotion (情感)**: Emotional types expressed in poems

#### Relationship Types 关系类型
- **CREATED**: Poet creates poem 诗人创作诗词
- **BELONGS_TO**: Poem belongs to dynasty 诗词属于朝代
- **HAS_THEME**: Poem has specific theme 诗词具有特定主题
- **EXPRESSES**: Poem expresses specific emotion 诗词表达特定情感

#### Core Methods 核心方法
- `build_knowledge_graph()`: Build knowledge graph 构建知识图谱
- `get_related_entities()`: Get related entities 获取相关实体
- `get_poet_info()`: Get poet information 获取诗人信息
- `search_poems_by_theme()`: Search poems by theme 按主题搜索诗词
- `get_poems_by_emotion()`: Get poems by emotion 按情感搜索诗词
- `get_knowledge_graph_statistics()`: Get graph statistics 获取图谱统计信息

### 2. Redis Caching Mechanism Redis缓存机制

#### Caching Strategy 缓存策略
- Using MD5 hash to generate cache keys 使用MD5哈希生成缓存键
- Different TTL expiration times for different query types 为不同类型的查询设置不同的TTL过期时间
- Cache decorator implementation to simplify caching logic 缓存装饰器实现简化缓存逻辑

#### Cache Time Settings 缓存时间设置
- Knowledge graph construction results: 24 hours 知识图谱构建结果：24小时
- Related entity queries: 1 hour 相关实体查询：1小时
- Poet information queries: 2 hours 诗人信息查询：2小时
- Theme/emotion searches: 1 hour 主题/情感搜索：1小时
- Statistics: 30 minutes 统计信息：30分钟

### 3. Asynchronous Support 异步支持

#### Async Service Wrapper 异步服务包装器
- Using `ThreadPoolExecutor` to handle synchronous blocking operations 使用`ThreadPoolExecutor`处理同步阻塞操作
- Implementing concurrency control to avoid resource exhaustion 实现并发控制避免资源耗尽
- Providing thread pool management and coroutine concurrency control 提供线程池管理和协程并发控制

#### Async API Endpoints 异步API端点
- All API endpoints support asynchronous processing 所有API端点均支持异步处理
- RAG retrieval and generation processes are asynchronous RAG检索和生成过程异步化
- Neo4j queries are asynchronous Neo4j查询异步化

## Technology Stack 技术栈详解

### Backend Framework 后端框架
- **FastAPI**: High-performance asynchronous web framework 高性能异步Web框架
- **LangChain**: RAG framework integration RAG框架集成
- **Pydantic**: Data validation and serialization 数据验证和序列化

### Databases 数据库
- **Neo4j**: Graph database for storing knowledge graphs 图数据库，存储知识图谱
- **FAISS/Chroma**: Vector database 向量数据库
- **Redis**: High-performance cache 高性能缓存

### Large Language Models 大语言模型
- **OpenAI API Compatible Interface**: Supports proxy configuration OpenAI API兼容接口，支持代理配置
- **Sentence Transformers**: Local embedding models 本地嵌入模型

### Frontend 前端界面
- **Streamlit**: Rapid prototyping 快速原型开发
- **Matplotlib**: Data visualization 数据可视化

## API Documentation API接口文档

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

### Sentiment Analysis 情感分析
```
POST /api/v1/sentiment
{
  "text": "Before my bed, the bright moonlight"
}
```

```
POST /api/v1/sentiment
{
  "text": "床前明月光，疑是地上霜"
}
```

### Theme Search 主题搜索
```
GET /api/v1/themes/{theme}?limit=10
```

### Emotion Search 情感搜索
```
GET /api/v1/emotions/{emotion}?limit=10
```

### Knowledge Graph Statistics 知识图谱统计
```
GET /api/v1/kg/statistics
```

## Performance Optimization 性能优化

### Cache Optimization 缓存优化
1. Multi-level caching strategy 多级缓存策略
2. Intelligent cache key generation 智能缓存键生成
3. Automatic expiration mechanism 自动过期机制

### Asynchronous Optimization 异步优化
1. Thread pool for handling blocking operations 线程池处理阻塞操作
2. Coroutine concurrency control 协程并发控制
3. Connection pool reuse 连接池复用

### Database Optimization 数据库优化
1. Neo4j index optimization Neo4j索引优化
2. Query result caching 查询结果缓存
3. Batch operation optimization 批量操作优化

## Deployment Configuration 部署配置

### Environment Variables 环境变量配置
```
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI API Configuration
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

```
# API配置
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI API配置
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Neo4j配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Extension Recommendations 扩展建议

### Functional Extensions 功能扩展
1. Add more entity types (imagery, allusions, etc.) 添加更多实体类型（意象、典故等）
2. Implement more complex graph query algorithms 实现更复杂的图谱查询算法
3. Increase multimodal content support 增加多模态内容支持

### Performance Optimization 性能优化
1. Implement distributed caching 实现分布式缓存
2. Optimize vector retrieval algorithms 优化向量检索算法
3. Add query result re-ranking 添加查询结果重排序

### Technical Upgrades 技术升级
1. Integrate more powerful graph databases 集成更强大的图数据库
2. Use dedicated vector databases 使用专门的向量数据库
3. Implement model fine-tuning functionality 实现模型微调功能
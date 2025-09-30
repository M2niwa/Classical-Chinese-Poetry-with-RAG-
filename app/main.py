from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="古诗词RAG系统",
        description="基于RAG技术的古诗词检索与分析系统",
        version="1.0.0"
    )
    
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 包含路由
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        return {"message": "欢迎使用古诗词RAG系统"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app

app = create_app()
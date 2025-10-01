import hashlib
import json
import redis
import logging
from typing import Any, Callable, Optional, Dict
from functools import wraps
from app.core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        """初始化缓存管理器"""
        self.redis_client = None
        self._init_redis()
    
    def _init_redis(self):
        """初始化Redis连接"""
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            # 测试连接
            self.redis_client.ping()
            logger.info("Redis连接成功")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            self.redis_client = None
    
    def _generate_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """生成缓存键"""
        # 将参数序列化为字符串
        args_str = str(args)
        kwargs_str = str(sorted(kwargs.items())) if kwargs else ""
        key_string = f"{func_name}:{args_str}:{kwargs_str}"
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """从缓存获取数据"""
        if not self.redis_client:
            return None
            
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"从缓存获取数据失败: {e}")
        return None
    
    def set(self, key: str, data: Any, ttl: int = 3600) -> bool:
        """设置缓存数据"""
        if not self.redis_client:
            return False
            
        try:
            self.redis_client.setex(
                key, 
                ttl, 
                json.dumps(data, ensure_ascii=False)
            )
            return True
        except Exception as e:
            logger.warning(f"设置缓存数据失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        if not self.redis_client:
            return False
            
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"删除缓存数据失败: {e}")
            return False
    
    def cache(self, ttl: int = 3600):
        """缓存装饰器"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # 生成缓存键
                cache_key = self._generate_cache_key(func.__name__, *args, **kwargs)
                
                # 尝试从缓存获取数据
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.info(f"使用缓存结果: {func.__name__}")
                    return cached_result
                
                # 执行函数
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                # 缓存结果
                self.set(cache_key, result, ttl)
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                # 生成缓存键
                cache_key = self._generate_cache_key(func.__name__, *args, **kwargs)
                
                # 尝试从缓存获取数据
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.info(f"使用缓存结果: {func.__name__}")
                    return cached_result
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 缓存结果
                self.set(cache_key, result, ttl)
                return result
            
            # 根据函数类型返回相应的包装器
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        
        return decorator
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        if not self.redis_client:
            return {"status": "Redis未连接"}
        
        try:
            info = self.redis_client.info()
            return {
                "status": "连接正常",
                "used_memory": info.get("used_memory_human", "未知"),
                "connected_clients": info.get("connected_clients", "未知"),
                "total_commands_processed": info.get("total_commands_processed", "未知")
            }
        except Exception as e:
            return {"status": f"获取信息失败: {e}"}
    
    def clear_all_cache(self) -> bool:
        """清空所有缓存"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            logger.info("已清空所有缓存")
            return True
        except Exception as e:
            logger.error(f"清空缓存失败: {e}")
            return False

# 全局缓存管理器实例
import asyncio
cache_manager = CacheManager()
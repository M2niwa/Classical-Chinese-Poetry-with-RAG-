import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Awaitable
import functools

class AsyncService:
    """异步服务包装器，用于处理同步阻塞操作"""
    
    def __init__(self, max_workers: int = 10):
        """初始化异步服务"""
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def run_in_threadpool(self, func: Callable, *args, **kwargs) -> Any:
        """
        在线程池中运行同步函数
        
        Args:
            func: 要运行的同步函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            函数执行结果
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            functools.partial(func, *args, **kwargs)
        )
    
    async def run_cpu_bound(self, func: Callable, *args, **kwargs) -> Any:
        """
        运行CPU密集型任务
        
        Args:
            func: 要运行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            函数执行结果
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,  # 使用默认的ThreadPoolExecutor
            functools.partial(func, *args, **kwargs)
        )
    
    async def gather_with_concurrency(self, n: int, *coros: Awaitable) -> list:
        """
        限制并发数量执行协程
        
        Args:
            n: 最大并发数
            *coros: 要执行的协程
            
        Returns:
            协程执行结果列表
        """
        semaphore = asyncio.Semaphore(n)
        
        async def sem_coro(coro):
            async with semaphore:
                return await coro
                
        return await asyncio.gather(*(sem_coro(c) for c in coros))
    
    def close(self):
        """关闭线程池"""
        self.executor.shutdown(wait=True)

# 全局实例
async_service = AsyncService()
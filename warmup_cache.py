#!/usr/bin/env python3
"""
缓存预热脚本
用于在系统启动时预热常用查询的缓存
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.cache_warmup_service import cache_warmup_service

async def main():
    """主函数"""
    print("开始缓存预热...")
    try:
        await cache_warmup_service.warmup_all_caches()
        print("缓存预热完成!")
    except Exception as e:
        print(f"缓存预热失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
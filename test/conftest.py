# conftest.py — 测试全局配置
# 职责：提供共享的 pytest 异步 fixtures，包括测试用 HTTP 客户端

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.main import app


@pytest_asyncio.fixture
async def async_client():
    """创建异步 HTTP 测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# test_stats.py — 统计 API 端点测试
# 职责：测试 GET /api/v1/stats 的统计数据返回

import pytest


@pytest.mark.asyncio
async def test_get_stats(async_client):
    """GET /api/v1/stats 应返回访客数、设计数、点赞数、覆盖区域数"""
    pytest.skip("TODO: 统计端点实现后补充")

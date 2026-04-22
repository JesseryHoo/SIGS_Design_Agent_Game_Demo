# test_session_service.py — 会话服务业务逻辑测试
# 职责：测试会话创建和查询逻辑

import pytest


@pytest.mark.asyncio
async def test_create_session():
    """create_session 应生成 UUID session_id 并插入 users 表"""
    pytest.skip("TODO: 会话服务实现后补充")


@pytest.mark.asyncio
async def test_get_session():
    """get_session 对有效的 session_id 应返回用户数据"""
    pytest.skip("TODO: 会话服务实现后补充")

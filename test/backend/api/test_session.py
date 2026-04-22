# test_session.py — 会话 API 端点测试
# 职责：测试 POST /api/v1/sessions 的创建和响应格式

import pytest


@pytest.mark.asyncio
async def test_create_session_returns_session_id(async_client):
    """POST /api/v1/sessions 应返回包含 session_id 的新会话"""
    pytest.skip("TODO: 会话服务实现后补充")


@pytest.mark.asyncio
async def test_create_session_response_format(async_client):
    """POST /api/v1/sessions 响应应符合统一格式 {code, message, data}"""
    pytest.skip("TODO: 会话服务实现后补充")

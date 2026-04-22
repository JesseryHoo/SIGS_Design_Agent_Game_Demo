# test_auth.py — API Key 认证中间件测试
# 职责：测试认证通过、认证失败、缺少 Key 等场景

import pytest


@pytest.mark.asyncio
async def test_api_key_required(async_client):
    """不带 X-API-Key 的 /api/v1/* 请求应返回 401"""
    pytest.skip("TODO: 认证中间件实现后补充")


@pytest.mark.asyncio
async def test_api_key_invalid(async_client):
    """错误的 API Key 应返回 401"""
    pytest.skip("TODO: 认证中间件实现后补充")


@pytest.mark.asyncio
async def test_api_key_valid(async_client):
    """正确的 API Key 应正常通过"""
    pytest.skip("TODO: 认证中间件实现后补充")

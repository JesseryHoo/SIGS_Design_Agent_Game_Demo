# test_error_handler.py — 全局异常处理中间件测试
# 职责：测试参数验证错误和未处理异常的错误响应

import pytest


@pytest.mark.asyncio
async def test_validation_error_returns_40001(async_client):
    """请求参数验证失败应返回错误码 40001"""
    pytest.skip("TODO: 异常处理器实现后补充")


@pytest.mark.asyncio
async def test_unhandled_error_returns_50001(async_client):
    """未处理异常应返回错误码 50001 且不泄露内部细节"""
    pytest.skip("TODO: 异常处理器实现后补充")

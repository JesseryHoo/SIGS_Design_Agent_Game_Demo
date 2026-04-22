# test_connection.py — 数据库连接测试
# 职责：测试数据库会话生成和连接初始化

import pytest


@pytest.mark.asyncio
async def test_get_db_session():
    """get_db_session 应生成异步数据库会话"""
    pytest.skip("TODO: 使用测试数据库后补充")


@pytest.mark.asyncio
async def test_init_db():
    """init_db 应验证数据库连通性"""
    pytest.skip("TODO: 使用测试数据库后补充")

# test_serve.py — 数据库服务工具函数测试
# 职责：测试建表和连通性检查功能

import pytest


@pytest.mark.asyncio
async def test_create_tables():
    """create_tables 应在数据库中创建所有 ORM 表"""
    pytest.skip("TODO: 使用测试数据库后补充")


@pytest.mark.asyncio
async def test_check_connection():
    """check_connection 在数据库可达时应返回 True"""
    pytest.skip("TODO: 使用测试数据库后补充")

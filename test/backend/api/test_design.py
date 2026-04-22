# test_design.py — 设计流程 API 端点测试
# 职责：测试创意输入、设计确认、状态查询、列表、地图光点、点赞等 8 个端点

import pytest


@pytest.mark.asyncio
async def test_submit_creative_input(async_client):
    """POST /api/v1/designs/input 应接受情绪标签和用户文字"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_confirm_design(async_client):
    """POST /api/v1/designs/confirm 应更新设计并触发图生图"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_get_design(async_client):
    """GET /api/v1/designs/{id} 应返回完整设计详情"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_get_design_status(async_client):
    """GET /api/v1/designs/{id}/status 应返回生成状态"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_list_designs(async_client):
    """GET /api/v1/designs 应返回分页设计列表"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_get_map_points(async_client):
    """GET /api/v1/designs/map 应返回位置光点数据"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_like_design(async_client):
    """POST /api/v1/designs/{id}/like 应递增点赞数"""
    pytest.skip("TODO: 点赞服务实现后补充")


@pytest.mark.asyncio
async def test_unlike_design(async_client):
    """DELETE /api/v1/designs/{id}/like 应递减点赞数"""
    pytest.skip("TODO: 点赞服务实现后补充")

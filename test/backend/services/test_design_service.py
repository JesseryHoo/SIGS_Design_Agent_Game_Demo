# test_design_service.py — 设计服务业务逻辑测试
# 职责：测试创意输入提交、设计确认、查询、列表等核心流程

import pytest


@pytest.mark.asyncio
async def test_submit_input():
    """submit_input 应保存用户输入并调用 agent 服务"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_confirm_design():
    """confirm_design 应更新记录并触发图生图"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_get_design():
    """get_design 应根据 id 返回完整设计记录"""
    pytest.skip("TODO: 设计服务实现后补充")


@pytest.mark.asyncio
async def test_list_designs():
    """list_designs 应返回带排序的分页结果"""
    pytest.skip("TODO: 设计服务实现后补充")

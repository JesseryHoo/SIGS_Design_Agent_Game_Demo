# stats.py — 统计数据 API 端点
# 职责：返回平台参与统计数据（GET /stats）

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_db
from backend.schemas.common import api_success

stats_router = APIRouter()


@stats_router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
):
    """获取参与统计数据"""
    # TODO: 从数据库查询真实统计数据
    return api_success(data={
        "total_visitors": 0,
        "total_designs": 0,
        "total_likes": 0,
        "areas_covered": 0,
    })

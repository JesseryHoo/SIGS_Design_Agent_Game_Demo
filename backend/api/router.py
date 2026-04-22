# router.py — 顶层 API 路由
# 职责：将所有子路由（sessions、designs、stats）挂载到 /api/v1 前缀下

from fastapi import APIRouter

from backend.api.design import design_router
from backend.api.session import session_router
from backend.api.stats import stats_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(session_router, tags=["sessions"])
api_router.include_router(design_router, tags=["designs"])
api_router.include_router(stats_router, tags=["stats"])

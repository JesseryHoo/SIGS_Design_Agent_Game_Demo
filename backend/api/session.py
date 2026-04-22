# session.py — 会话管理 API 端点
# 职责：处理访客会话创建（POST /sessions）

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_db
from backend.schemas.common import api_success
from backend.schemas.session import SessionCreateRequest
from backend.services import session_service

session_router = APIRouter()


@session_router.post("/sessions")
async def create_session(
    request: SessionCreateRequest = None,
    db: AsyncSession = Depends(get_db),
):
    """创建访客会话"""
    result = await session_service.create_session(db)
    return api_success(data=result)

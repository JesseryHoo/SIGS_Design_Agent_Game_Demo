# session_service.py — 会话管理业务逻辑
# 职责：处理访客会话的创建和查询

from sqlalchemy.ext.asyncio import AsyncSession


async def create_session(db: AsyncSession) -> dict:
    """创建新的访客会话，返回包含 session_id 的会话数据

    TODO: 1. 生成 UUID 作为 session_id
          2. 插入 users 表
          3. 返回会话信息
    """
    raise NotImplementedError("TODO: 实现会话创建逻辑")


async def get_session(db: AsyncSession, session_id: str) -> dict | None:
    """通过 session_id 查询用户，返回用户数据或 None

    TODO: 根据 session_id 查询 users 表，返回用户数据
    """
    raise NotImplementedError("TODO: 实现会话查询逻辑")

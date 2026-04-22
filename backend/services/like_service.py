# like_service.py — 点赞业务逻辑
# 职责：处理设计点赞和取消点赞操作

from sqlalchemy.ext.asyncio import AsyncSession


async def like_design(db: AsyncSession, user_id: str, design_id: str) -> dict:
    """用户点赞设计

    TODO: 1. 检查是否已点赞（防止重复）
          2. 插入 likes 记录
          3. 递增 designs 表的 likes_count
          4. 返回成功确认
    """
    raise NotImplementedError("TODO: 实现点赞逻辑")


async def unlike_design(db: AsyncSession, user_id: str, design_id: str) -> dict:
    """用户取消点赞

    TODO: 1. 查找并删除已有的 likes 记录
          2. 递减 designs 表的 likes_count
          3. 返回成功确认
    """
    raise NotImplementedError("TODO: 实现取消点赞逻辑")

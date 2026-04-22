# stats.py — 统计数据响应模型
# 职责：定义平台参与统计数据的响应格式

from pydantic import BaseModel


class StatsResponse(BaseModel):
    """参与统计响应 — 包含访客数、设计数、点赞数、覆盖区域数"""
    total_visitors: int
    total_designs: int
    total_likes: int
    areas_covered: int

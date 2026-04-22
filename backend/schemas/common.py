# common.py — 通用响应与错误码定义
# 职责：定义统一的 API 响应格式、错误码常量、分页模型

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

# 错误码常量
SUCCESS = 0
BAD_PARAMS = 40001
AUTH_ERROR = 40101
NOT_FOUND = 40401
SERVER_ERROR = 50001


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: int = SUCCESS
    message: str = "success"
    data: Optional[T] = None


class PaginationParams(BaseModel):
    """分页请求参数"""
    page: int = 1
    page_size: int = 20


class PaginatedData(BaseModel, Generic[T]):
    """分页响应数据"""
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


def api_success(data: object = None) -> dict:
    """构造成功响应"""
    return {"code": SUCCESS, "message": "success", "data": data}


def api_error(code: int, message: str) -> dict:
    """构造错误响应"""
    return {"code": code, "message": message, "data": None}

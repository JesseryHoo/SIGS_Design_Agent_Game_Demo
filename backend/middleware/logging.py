# logging.py — 请求日志中间件
# 职责：记录每个请求的方法、路径、响应状态码和耗时

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from backend.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件 — 记录请求方法、路径、状态码和耗时"""

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info("%s %s -> %d (%.2fs)", request.method, request.url.path, response.status_code, duration)
        return response

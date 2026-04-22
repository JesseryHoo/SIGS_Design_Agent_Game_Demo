# main.py — FastAPI 应用入口
# 职责：创建应用实例、注册中间件、挂载路由、提供前端静态文件服务

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from backend.api.router import api_router
from backend.config import settings
from backend.middleware.auth import APIKeyMiddleware
from backend.middleware.error_handler import add_error_handlers
from backend.middleware.logging import LoggingMiddleware
from backend.utils.logger import get_logger

logger = get_logger(__name__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SIGS 校园共创平台服务启动...")
    yield
    logger.info("服务关闭...")


app = FastAPI(
    title="SIGS Design Agent Game",
    description="AR 校园探索与共创平台",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APIKeyMiddleware)
app.add_middleware(LoggingMiddleware)
add_error_handlers(app)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return RedirectResponse(url="/pages/landing.html")


if FRONTEND_DIR.exists():
    app.mount("", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

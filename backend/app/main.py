#app/main.py
# 项目入口，整合所有路由
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import init_db

# 导入路由
from app.api.v1.auth import router as auth_router
from app.api.v1.llm_models import router as llm_models_router
from app.api.v1.chat import router as chat_router
from app.api.v1.user import router as user_router
from app.api.v1.conversation import router as conversation_router

from contextlib import asynccontextmanager
import inspect

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化 DB（支持 sync 或 async init_db）
    if inspect.iscoroutinefunction(init_db):
        await init_db()
    else:
        init_db()
    yield
    # 可在此添加关闭/清理逻辑

# 初始化FastAPI应用（使用 lifespan 替代 on_event）
app = FastAPI(title="LLM调用平台", version="1.0", lifespan=lifespan)

# ========== 新增：配置CORS ==========
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173"],  # 允许前端域名
    allow_origins=["*"],  # 允许前端域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
)

# 注册路由（带版本前缀）
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(llm_models_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(conversation_router, prefix=settings.API_V1_STR)

# 根路径
@app.get("/")
async def root():
    return {
        "message": "LLM调用平台后端服务正常运行",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

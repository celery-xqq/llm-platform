#全局配置
#app/core/config.py
import os
from typing import List, Optional

class Settings():
    # 项目基本配置
    APP_NAME = "LLM PLATFORM"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-strong-secret-key-1234567890abcdef"  # 生产环境替换为随机值
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 7  # Token有效期7天
    
    # 跨域配置
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]  # 前端地址


    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # 数据库配置
    #DATABASE_URL: str = "sqlite:///./llm_platform.db"  # 开发环境

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./llm_platform.db")

# 全局配置实例
settings = Settings()
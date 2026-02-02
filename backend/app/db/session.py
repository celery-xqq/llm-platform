#数据库会话
#app/db/session.py
# 数据库连接会话，FastAPI依赖注入用
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# 1. 导入Base（基础）
from app.db.base import Base
# 2. 导入所有模型（登记）
from app.models.user import User
from app.models.llm_model import LLMModel
from app.models.conversation import Conversation
from app.models.chat_message import ChatMessage

# 处理可能的 async 驱动（例如 sqlite+aiosqlite），为同步操作回退到同步驱动 URL
_db_url = settings.DATABASE_URL
# 如果使用 sqlite+aiosqlite，则去掉 "+aiosqlite" 以使用同步 sqlite 驱动，避免在同步上下文中触发 greenlet 错误
if "+aiosqlite" in _db_url:
    _sync_db_url = _db_url.replace("+aiosqlite", "")
else:
    _sync_db_url = _db_url

# 创建引擎（连接数据库）
engine = create_engine(
    _sync_db_url,
    # SQLite需要的特殊参数（生产环境PostgreSQL可去掉）
    connect_args={"check_same_thread": False} if "sqlite" in _sync_db_url else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    数据库会话依赖项（FastAPI专用）
    每次请求创建一个会话，请求结束关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库（创建所有表）"""
    Base.metadata.create_all(bind=engine)  # 创建所有表
# 用户表（认证必备）
#app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, comment="用户名")
    hashed_password = Column(String(255), comment="密码哈希")
    is_admin = Column(Boolean, default=False, comment="是否管理员")
    is_active = Column(Boolean, default=True, comment="是否启用")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
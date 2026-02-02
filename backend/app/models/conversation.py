# app/models/conversation.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.db.base import Base
import uuid


def gen_uuid():
    return str(uuid.uuid4())


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=gen_uuid)

    user_id = Column(String(36), index=True, nullable=False)
    model_id = Column(String(36), index=True, nullable=False)

    title = Column(String(100), nullable=True)

    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

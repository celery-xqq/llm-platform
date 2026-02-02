#app/models/chat_message.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.db.base import Base
import uuid


def gen_uuid():
    return str(uuid.uuid4())


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=gen_uuid)

    conversation_id = Column(String(36), index=True, nullable=False)

    role = Column(String(20), nullable=False)  # user / assistant / system
    content = Column(Text, nullable=False)

    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    #update_time = Column(DateTime, onupdate=datetime.now, comment="更新时间")

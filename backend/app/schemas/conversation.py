from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConversationResponse(BaseModel):
    id: str
    title: Optional[str]
    model_id: str
    create_time: datetime

    class Config:
        from_attributes = True

# 新增：请求体模型 - 接收前端传递的标题
class ConversationTitleUpdate(BaseModel):
    title: str  # 前端传递的新标题
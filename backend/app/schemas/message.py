#app/schemas/message.py
from pydantic import BaseModel
from typing import Optional, List
class MessageOut(BaseModel):
    id: str
    role: str
    content: str

    class Config:
        from_attributes = True
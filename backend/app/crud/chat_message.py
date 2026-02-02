#app.crud.chat_message.py
from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage


def create_message(
    db: Session,
    conversation_id: str,
    role: str,
    content: str
):
    msg = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_messages(
    db: Session,
    conversation_id: str,
    limit: int = 20
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.create_time.asc())
        .limit(limit)
        .all()
    )

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


def delete_messages_by_conversation(db: Session, conversation_id: str) -> int:
    """
    删除指定会话下的所有消息。
    返回被删除的消息数量（或 0）。
    """
    # 使用 query.delete 提高效率
    deleted = db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id).delete(synchronize_session=False)
    db.commit()
    return deleted

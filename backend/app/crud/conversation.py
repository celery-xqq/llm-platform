#app/crud/conversation.py
from sqlalchemy.orm import Session
from app.models.conversation import Conversation


def create_conversation(
    db: Session,
    user_id: str,
    model_id: str,
    title: str | None = None
):
    conv = Conversation(
        user_id=user_id,
        model_id=model_id,
        title=title
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def get_conversation(db: Session, conversation_id: str):
    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )


def list_conversations(db: Session, user_id: str):
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.create_time.desc())
        .all()
    )


def update_conversation_title(db: Session, conversation_id: str, title: str) -> Conversation | None:
    """
    更新会话标题
    :param db: 数据库会话
    :param conversation_id: 会话ID
    :param title: 新标题
    :return: 更新后的会话对象（不存在返回None）
    """
    conv = db.query(Conversation).filter_by(id=conversation_id).first()
    if conv:
        conv.title = title  # 给会话对象赋值新标题
        db.commit()  # 提交事务到数据库
        db.refresh(conv)  # 刷新对象，获取最新数据库数据
    return conv
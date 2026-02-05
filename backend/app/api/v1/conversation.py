#app/api/v1/conversation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.conversation import (
    list_conversations,
    update_conversation_title,
    get_conversation,
    delete_conversation,
)
from app.schemas.conversation import ConversationResponse, ConversationTitleUpdate
from app.schemas.message import MessageOut
from app.crud.chat_message import get_messages

router = APIRouter(prefix="/conversations", tags=["会话"])


#会话列表
@router.get("/", response_model=list[ConversationResponse])
def get_conversations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    print("current_user:", current_user)
    #return list_conversations(db, current_user.id)
    return list_conversations(db, current_user.get("id"))

#获取会话消息列表
@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
def get_conversation_messages(
    conversation_id: str, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user) #这样普通用户也能获取消息
):
    return get_messages(db, conversation_id)

# 新增：更新会话标题接口（PATCH 方法）
@router.patch("/{conversation_id}/title", response_model=ConversationResponse)
def update_conversation_title_api(
    conversation_id: str,
    title_data: ConversationTitleUpdate,  # 接收前端传递的标题
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    更新指定会话的标题
    :param conversation_id: 要更新的会话ID
    :param title_data: 包含新标题的请求体
    :param db: 数据库会话
    :param current_user: 当前登录用户
    :return: 更新后的会话信息
    """
    # 1. 调用CRUD更新标题
    updated_conv = update_conversation_title(
        db=db,
        conversation_id=conversation_id,
        title=title_data.title.strip()  # 去除标题前后空格
    )
    
    # 2. 处理会话不存在的场景，抛出404异常
    if not updated_conv:
        raise HTTPException(status_code=404, detail="会话不存在或已被删除")
    
    # 3. 验证当前用户是否有权限（可选，增强安全性，防止修改他人会话）
    user_id = current_user.get("id")
    if updated_conv.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权修改该会话标题")
    
    # 4. 返回更新后的会话对象
    return updated_conv


# 删除会话（及其消息）
@router.delete("/{conversation_id}", status_code=204)
def delete_conversation_api(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    删除指定会话及其所有消息。仅允许会话所有者删除。
    成功返回 204 No Content；会话不存在返回 404；无权限返回 403。
    """
    conv = get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="会话不存在或已被删除")

    # 权限校验：仅允许创建者删除
    user_id = current_user.get("id")
    if conv.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权删除该会话")

    deleted = delete_conversation(db, conversation_id)
    if not deleted:
        # 理论上已经通过 get_conversation 判断过存在，但额外兜底
        raise HTTPException(status_code=404, detail="会话删除失败或不存在")

    # 返回 204 无内容
    return
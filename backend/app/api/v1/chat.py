#app/api/v1/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest, ChatResponse
from app.crud.llm_model import get_llm_model
from app.crud.conversation import create_conversation, get_conversation
from app.crud.chat_message import create_message, get_messages

from app.services.llm.adapter import DynamicLLMAdapter
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/chat", tags=["对话"])

dynamic_adapter = DynamicLLMAdapter()


@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # 1️⃣ 模型
    model = get_llm_model(db, chat_request.model_id)
    if not model:
        raise HTTPException(404, "模型不存在或已禁用")

    # 2️⃣ 会话
    if chat_request.conversation_id:
        conversation = get_conversation(db, chat_request.conversation_id)
        if not conversation:
            raise HTTPException(404, "会话不存在")
    else:
        conversation = create_conversation(
            db=db,
            #user_id=current_user.id,
            user_id=current_user.get("id"),
            model_id=chat_request.model_id
        )

    # 3️⃣ 保存用户消息
    create_message(
        db,
        conversation.id,
        "user",
        chat_request.content
    )

    # 4️⃣ 取上下文
    history = get_messages(db, conversation.id, limit=20)

    messages = [
        {"role": m.role, "content": m.content}
        for m in history
    ]

    # 5️⃣ 调 adapter
    model_config = {
        "id": model.id,
        "name": model.name,
        "type": model.type,
        "model_key": model.model_key,
        "base_url": model.base_url,
        "real_model_name": model.real_model_name
    }

    result = await dynamic_adapter.chat(
        messages=messages,
        model_config=model_config,
        chat_request=chat_request
    )

    # 6️⃣ 保存 assistant
    if result.success:
        create_message(
            db,
            conversation.id,
            "assistant",
            result.content
        )

    result.conversation_id = conversation.id
    return result

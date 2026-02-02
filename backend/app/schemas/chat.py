from pydantic import BaseModel, Field
from typing import Dict
from typing import Optional, List


# ====================== 对话相关 Schema ======================
class ChatRequest(BaseModel):
    """发起对话的请求参数（核心：传模型ID而非硬编码模型名）"""
    model_id: str = Field(..., description="数据库中的模型ID")

    #delete
    # messages: List[Dict[str, str]] = Field(
    #     ..., 
    #     description="对话消息列表，格式：[{\"role\": \"user/assistant\", \"content\": \"内容\"}]"
    # )

    #add
    content: str = Field(..., description="用户输入的对话内容")
    conversation_id: Optional[str] = None
    
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="随机性（0-2）")
    max_tokens: Optional[int] = Field(None, description="最大生成Token数")

class ChatResponse(BaseModel):
    """对话响应的统一格式（前端只需解析这个格式）"""
    success: bool = Field(..., description="调用是否成功")
    content: Optional[str] = Field(None, description="模型回复内容（成功时返回）")

    #add
    conversation_id: Optional[str] = None

    model_id: str = Field(..., description="调用的模型ID")
    model_name: str = Field(..., description="调用的模型展示名")

    error: Optional[str] = Field(None, description="错误信息（失败时返回）")
    usage: Optional[Dict[str, int]] = Field(
        None, 
        description="Token使用量，格式：{\"prompt_tokens\": 10, \"completion_tokens\": 20, \"total_tokens\": 30}"
    )

    class Config:
        from_attributes = True

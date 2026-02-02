#app/schemas/llm_model.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from app.models.llm_model import LLMType  # 导入模型类型枚举

# ====================== 模型配置相关 Schema ======================
class LLMModelCreate(BaseModel):
    """创建模型配置的请求参数"""
    name: str = Field(..., description="模型展示名（如OpenAI GPT-3.5）")
    description: Optional[str] = Field(None, description="模型描述")
    type: LLMType = Field(..., description="模型类型（openai/baidu/tencent/local）")
    #model_key: Optional[str] = Field(None, description="API Key/密钥")
    #创建时 默认空字符串，保证后端 always 有字段：
    model_key: str = Field("", description="API Key/密钥（可为空）")
    base_url: HttpUrl = Field(..., description="模型调用地址（Base URL）")
    real_model_name: str = Field(..., description="真实模型名（如gpt-3.5-turbo、glm-4）")
    is_active: bool = Field(default=True, description="是否启用")
    extra_config: Optional[Dict] = Field(None, description="扩展配置（JSON格式）")

class LLMModelUpdate(BaseModel):
    """更新模型配置的请求参数（仅更新传入的字段）"""
    name: Optional[str] = Field(None, description="模型展示名")
    description: Optional[str] = Field(None, description="模型描述")
    model_key: Optional[str] = Field(None, description="API Key/密钥")
    base_url: Optional[HttpUrl] = Field(None, description="模型调用地址")
    real_model_name: Optional[str] = Field(None, description="真实模型名")
    is_active: Optional[bool] = Field(None, description="是否启用")
    extra_config: Optional[Dict] = Field(None, description="扩展配置")

class LLMModelResponse(BaseModel):
    """模型配置的响应参数（隐藏敏感字段）"""
    id: str
    name: str
    description: Optional[str]
    type: LLMType
    base_url: str  # HttpUrl转成普通字符串返回
    real_model_name: str
    is_active: bool

    class Config:
        from_attributes = True  # 支持从SQLAlchemy模型实例转换


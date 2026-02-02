#模型配置表
#app/models/llm_model.py
from sqlalchemy import Column, String, Text, Boolean, Enum
from app.db.base import Base
import enum

# 模型类型枚举（覆盖主流大模型）
class LLMType(str, enum.Enum):
    OPENAI = "openai"          # OpenAI/兼容OpenAI的模型（智谱、通义千问等）
    BAIDU = "baidu"            # 百度文心一言（单独适配）
    TENCENT = "tencent"        # 腾讯混元（单独适配）
    LOCAL = "local"            # 本地模型（vLLM/Ollama等）

class LLMModel(Base):
    """大模型配置表（核心：存储所有可调用的模型信息）"""
    __tablename__ = "llm_models"

    # 主键
    id = Column(String(36), primary_key=True, index=True, comment="模型ID（UUID）")
    # 基础信息
    name = Column(String(100), unique=True, index=True, comment="模型展示名（如OpenAI GPT-3.5）")
    description = Column(Text, nullable=True, comment="模型描述")
    type = Column(Enum(LLMType), comment="模型类型（openai/baidu/tencent/local）")
    # 核心配置
    #model_key = Column(String(255), comment="API Key/密钥（加密存储，生产环境需加密）")
    model_key = Column(String(255),nullable=True,comment="API Key（部分模型无需）")

    base_url = Column(String(500), comment="模型调用地址（Base URL）")
    real_model_name = Column(String(100), comment="真实模型名（如gpt-3.5-turbo、glm-4）")
    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    # 扩展配置（JSON格式存储，适配不同模型的特殊参数）
    extra_config = Column(Text, nullable=True, comment="扩展配置（JSON）")
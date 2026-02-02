#app/services/llm/adapter.py
#适配层（支持动态加载模型配置）
from openai import AsyncOpenAI, OpenAI
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
# 从 schemas 导入统一的 ChatRequest/ChatResponse
from app.schemas.chat import ChatRequest, ChatResponse
from urllib.parse import urlparse, urljoin  # 新增：URL解析工具

class DynamicLLMAdapter:
    """动态适配层：从数据库加载模型配置"""
    def __init__(self):
        # 缓存客户端（key=模型ID），避免重复创建
        self.client_cache: Dict[str, Union[AsyncOpenAI, OpenAI]] = {}
    
    def _normalize_base_url(self, base_url: str) -> str:
        """
        标准化base_url：兼容两种格式
        - 输入1: http://xxx/v1 → 返回: http://xxx/v1
        - 输入2: http://xxx/v1/chat/completions → 返回: http://xxx/v1
        """
        # 移除末尾的斜杠（避免拼接错误）
        base_url = base_url.rstrip("/")
        
        # 如果地址包含 /chat/completions，截取前面的基础地址
        if "/chat/completions" in base_url:
            normalized_url = base_url[:base_url.index("/chat/completions")]
            return normalized_url
        else:
            return base_url

    def _create_client(self, model_config: Dict) -> Union[AsyncOpenAI, OpenAI]:
        print("Creating client:", model_config["name"], model_config.get("model_key"))

        """
        根据模型配置创建客户端
        - model_config['type'] : 模型类型
        - model_config['model_key'] : 可选 api_key
        - model_config['base_url'] : 模型服务地址
        """
        # 目前只处理OpenAI兼容模型，其他类型（百度/腾讯）可扩展
        if model_config["type"] != "openai":
            raise ValueError(f"暂不支持的模型类型：{model_config['type']}")
        
        # 标准化base_url（核心：兼容两种格式）
        normalized_base_url = self._normalize_base_url(model_config["base_url"])
        
        #model_key一定要传，如果不设置，那就是空字符串
        return AsyncOpenAI(
            api_key=model_config["model_key"],
            base_url=normalized_base_url
        )

    async def chat(
        self,
        messages: list,
        model_config: Dict,
        chat_request: ChatRequest
    ) -> ChatResponse:
        """
        发起异步对话调用
        :param chat_request: 统一的对话请求（来自schemas）
        :param model_config: 从数据库读取的模型配置
        :return: 统一的对话响应（来自schemas）
        """
        try:
            # 1. 获取/创建客户端
            if chat_request.model_id not in self.client_cache:
                self.client_cache[chat_request.model_id] = self._create_client(model_config)
            client = self.client_cache[chat_request.model_id]

            # 2. 调用大模型（OpenAI兼容接口）
            response = await client.chat.completions.create(
                model=model_config["real_model_name"],
                messages=messages,
                temperature=chat_request.temperature,
                max_tokens=chat_request.max_tokens
            )

            # 3. 构造统一响应（返回schemas定义的ChatResponse）
            return ChatResponse(
                success=True,
                content=response.choices[0].message.content,
                model_id=chat_request.model_id,
                model_name=model_config["name"],
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
        except Exception as e:
            return ChatResponse(
                success=False,
                model_id=chat_request.model_id,
                model_name=model_config.get("name", ""),
                error=str(e)
            )
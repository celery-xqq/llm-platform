# 用户相关的请求/响应模型
#app/schemas/user.py
from pydantic import BaseModel, Field
from typing import Optional, List

# 创建用户的请求模型
class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

# 用户登录的请求模型
class UserLogin(BaseModel):
    username: str
    password: str

# 基础用户模型（返回给前端的字段）
class UserResponse(BaseModel):
    id: str
    username: str
    is_admin: bool = False
    is_active: bool = True

    class Config:
        from_attributes = True  # 支持从ORM模型（User）转换

# ========== 新增：用户列表响应模型 ==========
class UserListResponse(BaseModel):
    data: List[UserResponse]
    total: int
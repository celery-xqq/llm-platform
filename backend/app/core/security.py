#安全工具
#app/core/security.py
# 认证相关工具（JWT生成/验证、密码加密/验证）
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

# 新增：导入数据库依赖和用户CRUD
from app.db.session import get_db
from app.crud.user import get_user_by_id
from sqlalchemy.orm import Session

# OAuth2令牌获取方式（从Authorization头获取Bearer Token）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """生成JWT Token（使用时区感知时间并将 exp 转为时间戳）"""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Token负载，exp 使用整数时间戳
    to_encode = {"exp": int(expire.timestamp()), "sub": str(subject)}
    # 加密生成Token
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)  # 新增：依赖注入数据库会话
) -> Dict[str, Any]:
    """
    获取当前登录用户（从数据库真实查询）
    依赖项：验证Token有效性，返回用户信息
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码Token（sub是用户ID）
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # ====================== 核心修改：从数据库查询真实用户 ======================
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise credentials_exception
    
    # 构造用户信息返回（和原有格式兼容）
    user = {
        "id": db_user.id,
        "username": db_user.username,
        "is_admin": db_user.is_admin,
        "is_active": db_user.is_active
    }
    return user

async def get_current_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    仅管理员可访问的依赖项
    基于get_current_user，额外校验是否是管理员
    """
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无管理员权限"
        )
    return current_user
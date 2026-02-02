# 认证接口（登录、创建用户）
#app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.db.session import get_db
from app.crud.user import get_user_by_username, create_user
from app.core.config import settings
# 新增：从独立文件导入密码验证函数
from app.core.password import verify_password
from app.core.security import create_access_token, get_current_admin

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login")
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """用户登录，返回Token"""
    # 校验用户是否存在
    user = get_user_by_username(db, user_login.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    # 校验密码
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    # 生成Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }
    }

@router.post("/create-user", response_model=UserResponse)
async def create_new_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    """创建用户（仅管理员）"""
    existing_user = get_user_by_username(db, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    return create_user(db, user_create)
# app/api/v1/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import get_users, delete_user, get_user_by_id
from app.schemas.user import UserResponse, UserListResponse
from app.core.security import get_current_admin  # 管理员权限校验

router = APIRouter(prefix="/users", tags=["用户管理"])

# ========== 获取所有用户（仅管理员可访问） ==========
@router.get("/", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)  # 仅管理员可访问
):
    """获取所有用户（分页，需管理员权限）"""
    users = get_users(db, skip=skip, limit=limit)
    return users

# ========== 可选：删除用户接口（前端用户管理页会用到） ==========
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    
    # ========== 新增：禁止删除admin账号 ==========
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    # 判断用户名是否为admin，禁止删除
    if user.username == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # 403表示禁止操作
            detail="禁止删除管理员admin账号"
        )
    
    """删除用户（需管理员权限）"""
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return None
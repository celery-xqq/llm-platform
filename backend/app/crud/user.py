# 用户CRUD操作
#app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import uuid

# 新增：从独立文件导入密码哈希函数
from app.core.password import get_password_hash

def create_user(db: Session, user: UserCreate) -> User:
    """创建用户"""
    #uuid.uuid4() 生成的 ID 重复概率极低，你的用户创建场景完全不用担心重复问题
    db_user = User(
        id=str(uuid.uuid4()),
        username=user.username,
        hashed_password=get_password_hash(user.password),
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: str) -> User:
    """根据用户ID查询用户"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    """根据用户名查询用户"""
    return db.query(User).filter(User.username == username).first()


# ========== 新增：获取所有用户 ==========
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """获取所有用户（支持分页）"""
    return db.query(User).offset(skip).limit(limit).all()

# ========== 可选：删除用户（前端用户管理页会用到） ==========
def delete_user(db: Session, user_id: str) -> bool:
    """删除用户"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
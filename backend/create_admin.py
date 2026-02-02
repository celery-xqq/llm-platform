# 方式1：通过Python脚本恢复
#create_admin.py
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.models.user import User

db: Session = next(get_db())
# 创建admin账号（密码123456，可根据实际情况修改）
admin_user = UserCreate(
    username="admin",
    password="123456",  # 注意：生产环境请使用强密码
    is_admin=True
)

# 判断旧管理员是否存在
old_admin = db.query(User).filter(User.username == admin_user.username).first()
if old_admin:
    print(f"ℹ️ 管理员账号 {old_admin.username} 已存在")
else:
    print(f"ℹ️ 未找到管理员账号：{admin_user.username}，直接创建新账号")
    create_user(db, admin_user)
    print(f"✅ 管理员账号创建成功，用户名：{admin_user.username}，密码：{admin_user.password}（请尽快修改密码）")

db.close()
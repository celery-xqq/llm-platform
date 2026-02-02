"""简化的管理员重建脚本：复用项目已存在的会话与创建用户逻辑"""
#recreate_admin.py
import os
import sys

from app.db.session import SessionLocal, init_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.user import create_user
from sqlalchemy.exc import SQLAlchemyError

def main():
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")

    # 确保表已创建
    #init_db()

    try:
        with SessionLocal() as db:
            old = db.query(User).filter(User.username == ADMIN_USERNAME).first()
            if old:
                db.delete(old)
                db.commit()
                print(f"ℹ️ 已删除旧管理员：{ADMIN_USERNAME} (id={old.id})")

            user_in = UserCreate(
                username=ADMIN_USERNAME,
                password=ADMIN_PASSWORD,
                is_admin=True
            )
            new_user = create_user(db, user_in)
            print("✅ 管理员创建/重建成功")
            print(f"   用户名：{new_user.username}")
            print(f"   用户ID：{new_user.id}")
    except SQLAlchemyError as e:
        print(f"❌ 数据库错误：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

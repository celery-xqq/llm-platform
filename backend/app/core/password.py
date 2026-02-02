# /app/core/password.py
from passlib.context import CryptContext

# 密码加密上下文（独立出来，避免循环导入）
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    default="pbkdf2_sha256",
    deprecated="auto",
    bcrypt__rounds=12
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"密码验证失败：{str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)
#数据库基类
#app/db/base.py
# 所有ORM模型的基类
from sqlalchemy.ext.declarative import declarative_base

# 全局Base，所有模型都继承这个类
Base = declarative_base()
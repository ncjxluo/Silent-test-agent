# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 11:29
# @Author  : lwc
# @File    : str_db.py
# @Description : tortoise-orm 框架链接数据库，并返回数据库对象

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from src.utils.str_config import StrConfig

str_config = StrConfig()
# IP = str_config.get_config().get("db").get("host")
# PORT = str_config.get_config().get("db").get("port")
# UNAME = str_config.get_config().get("db").get("user")
# PASSWD = str_config.get_config().get("db").get("password")
# SCHEMA = str_config.get_config().get("db").get("schema")
#
#

IP = str_config.get_config().get("db").get("host")
PORT = str_config.get_config().get("db").get("port")
UNAME = str_config.get_config().get("db").get("user")
PASSWD = str_config.get_config().get("db").get("password")
SCHEMA = str_config.get_config().get("db").get("schema")

#DATABASE_URL = f"mysql://{UNAME}:{PASSWD}@{IP}:{PORT}/{SCHEMA}?minsize=5&maxsize=20"

DATABASE_URL = f"mysql+asyncmy://{UNAME}:{PASSWD}@{IP}:{PORT}/{SCHEMA}"

engine = create_async_engine(DATABASE_URL,
            echo=False,                # 是否展示sql
            future=True,              # 开启未来模式
            pool_size=100,             # 连接池中保持的连接数量
            max_overflow=30,          # 在pool_size之外最多还能开多少连接（峰值负载时）
            pool_recycle=3600,        # 连接回收时间（秒），防止 MySQL 空闲断开
            pool_timeout=30)          # 获取连接超时)


async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,    # 手动控制 flush
    autocommit=False,   # 手动控制提交
)

# async def init_db():
#     """
#     用来初始化 Tortoise ORM 框架 并自动创建表
#     """
#
#     await Tortoise.init(
#         db_url=DATABASE_URL,
#         modules={'models': ['src.models']},
#         timezone="Asia/Shanghai"
#     )
#     # await Tortoise.generate_schemas()
#
#
# async def close_db():
#     """
#     关闭数据库连接
#     """
#     await Tortoise.close_connections()
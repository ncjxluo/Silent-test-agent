# -*- coding: utf-8 -*-
# @Time    : 2025/10/17 11:18
# @Author  : lwc
# @File    : create_temp_data.py
# @Description :
from src.utils.str_db import init_db,close_db
from src.models.user_template import UserTable


async def create_sql_temp_data():
    count = 0
    await init_db()
    users = await UserTable.all()
    for user in users:
        pass
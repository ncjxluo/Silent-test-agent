# -*- coding: utf-8 -*-
# @Time    : 2025/10/31 15:23
# @Author  : lwc
# @File    : str_sys_user_role.py
# @Description : 定义用户 角色 关系表

from sqlmodel import Field,SQLModel
from datetime import datetime
from typing import Optional


class StrSysUserRole(SQLModel, table=True):

    __tablename__ = 'str_sys_user_role'

    user_key: str = Field(max_length=100, primary_key=True, description="用户的key值")
    role_key: str = Field(max_length=100, primary_key=True, description="角色的key值")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
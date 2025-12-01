# -*- coding: utf-8 -*-
# @Time    : 2025/10/31 17:28
# @Author  : lwc
# @File    : str_sys_role_menu.py
# @Description : 角色和菜单的关系表

from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime


class StrSysRoleMenu(SQLModel, table=True):

    __tablename__ = 'str_sys_role_menu'

    menu_key: str = Field(max_length=100, primary_key=True, description="菜单的key值")
    role_key: str = Field(max_length=100, primary_key=True, description="角色的key值")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
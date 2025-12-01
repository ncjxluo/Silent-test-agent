# -*- coding: utf-8 -*-
# @Time    : 2025/10/31 17:15
# @Author  : lwc
# @File    : str_sys_menu.py
# @Description : 系统的菜单表

import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime


class StrSysMenu(SQLModel, table=True):

    __tablename__ = 'str_sys_menu'

    menu_key: str = Field(max_length=100,default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="菜单的uuid，作为唯一标识符")
    menu_parent_key: str = Field(max_length=60, default="0", description="菜单的父级ID")
    menu_name: str = Field(max_length=60, default=None, description="菜单的名字")
    menu_path: str = Field(max_length=60, default=None, description="前端路由路径")
    menu_router_name: str = Field(max_length=60, default=None, description="前端路由名字")
    menu_component: str = Field(max_length=60, default=None, description="前端组件路径")
    menu_icon: str = Field(max_length=64, default=None, description="图标")
    menu_type: str = Field(max_length=20, default="menu", description="菜单类型: menu菜单 link外链")
    menu_order: Optional[int] = Field(sa_type=SMALLINT,default=1, description="排序")
    is_visible: int = Field(sa_type=SMALLINT,default=1, description="是否可见,1=是 0=否")
    permission_code: Optional[str] = Field(max_length=20, default=None, description="接口权限")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())


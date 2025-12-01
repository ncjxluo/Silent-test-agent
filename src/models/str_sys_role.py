# -*- coding: utf-8 -*-
# @Time    : 2025/10/31 14:39
# @Author  : lwc
# @File    : str_sys_role.py
# @Description : 定义系统角色表

import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime


class StrSysRole(SQLModel, table=True):

    __tablename__ = 'str_sys_role'

    id: Optional[int] = Field(default=None, primary_key=True)
    role_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="角色的uuid，作为唯一标识符")
    role_name: str = Field(max_length=60,default=None, description="角色的名字或者说是标题")
    description: Optional[str] = Field(max_length=300,default=None,description="角色的描述")
    is_delete: Optional[int] = Field(sa_type=SMALLINT,default=0, description="角色的删除状态,1=删除 0=未删除")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

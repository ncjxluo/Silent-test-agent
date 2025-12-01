# -*- coding: utf-8 -*-
# @Time    : 2025/11/3 19:19
# @Author  : lwc
# @File    : str_sys_dept.py
# @Description : 部门表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime

class StrSysDept(SQLModel, table=True):

    __tablename__ = 'str_sys_dept'

    id: Optional[int] = Field(default=None, primary_key=True)
    dept_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="部门的uuid，作为唯一标识符")
    dept_name: str = Field(max_length=40,default=None, description="部门的名字")
    status: Optional[int] = Field(sa_type=SMALLINT,default=1,description="部门的启用状态,1=启用 0=禁用")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
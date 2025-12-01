# -*- coding: utf-8 -*-
# @Time    : 2025/10/30 17:06
# @Author  : lwc
# @File    : str_sys_user.py
# @Description : 定义系统用户表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime


class StrSysUser(SQLModel, table=True):

    __tablename__ = 'str_sys_user'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="用户的uuid，作为唯一标识符")
    nickname: str = Field(max_length=40,default=None, description="用户的昵称,也是用户的登录名")
    username: str = Field(max_length=30,default=None, description="用户的真实姓名,也是用户的登录名")
    passwd: str = Field(max_length=30, default_factory=lambda: "str@123456",description="用户的登录密码")
    avatar: Optional[str] = Field(max_length=200,default=None, description="用户的头像")
    email: Optional[str] = Field(max_length=64,default=None,description="用户的邮箱")
    phone: Optional[str] = Field(max_length=64,default=None,description="用户的电话")
    status: Optional[int] = Field(sa_type=SMALLINT,default=1,description="用户的启用状态,1=启用 0=禁用")
    dept_key: Optional[str] = Field(max_length=100,default=None,description="用户所属的部门")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

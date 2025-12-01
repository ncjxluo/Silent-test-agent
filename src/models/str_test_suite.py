# -*- coding: utf-8 -*-
# @Time    : 2025/11/3 11:35
# @Author  : lwc
# @File    : str_test_suite.py
# @Description : 测试套件，其实应该是测试任务表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime


class StrTestSuite(SQLModel, table=True):

    __tablename__ = 'str_test_suite'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_key: str = Field( max_length=100, description="执行这个任务的用户id")
    suite_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()),description="测试任务的key")
    suite_name: str = Field(max_length=100, description="测试任务的名字.如哪个agent")
    status: str = Field(max_length=20, description="测试任务的状态")
    type: str = Field(max_length=20, description="测试任务的类别")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())


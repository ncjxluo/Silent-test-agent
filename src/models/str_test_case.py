# -*- coding: utf-8 -*-
# @Time    : 2025/11/3 11:36
# @Author  : lwc
# @File    : str_test_case.py
# @Description : 测试执行过程的表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from sqlalchemy import TEXT
from datetime import datetime


class StrTestCase(SQLModel, table=True):

    __tablename__ = 'str_test_case'

    id: Optional[int] = Field(default=None, primary_key=True)
    suite_key: str = Field(max_length=100, index=True , description="测试任务的key")
    plan_key: str = Field(max_length=100, index=True , description="测试计划的key")
    case_key: str = Field(max_length=100, index=True, description="测试步骤的的key")
    case_status: Optional[int] = Field(default=None, description="这个case成功或失败的标志，0为成功，1为失败")
    remarks: Optional[str] = Field(max_length=100, description="执行的备注")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

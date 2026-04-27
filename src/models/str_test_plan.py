# -*- coding: utf-8 -*-
# @Time    : 2025/11/3 11:36
# @Author  : lwc
# @File    : str_test_plan.py
# @Description : 测试计划的表，每一个xml就是计划

import uuid
from sqlmodel import Field,SQLModel,TEXT
from typing import Optional
from datetime import datetime


class StrTestPlan(SQLModel, table=True):

    __tablename__ = 'str_test_plan'

    id: Optional[int] = Field(default=None, primary_key=True)
    suite_key: str = Field(max_length=100,
                           index=True, default_factory=lambda: str(uuid.uuid4()),
                           description="测试任务的key")
    plan_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()),
                           description="测试计划的key")
    plan_name: str = Field(max_length=100, description="测试计划的名字")
    case_content:str = Field(sa_type=TEXT, description="用例的xml")
    doc_content:str = Field(sa_type=TEXT, description="接口的yaml列表")
    plan_task_sum: Optional[str] = Field(max_length=20, default="0", description="测试任务的总数量")
    status: str = Field(max_length=20, description="测试计划的状态")
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), sa_column_kwargs={
        "onupdate": lambda: int(datetime.now().timestamp() * 1000)
    })
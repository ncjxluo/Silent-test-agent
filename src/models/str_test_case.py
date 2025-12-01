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
    step_id: Optional[str] = Field(max_length=20, description="步骤的序号")
    step_name: Optional[str] = Field(max_length=80, description="步骤的名字")
    user_variables: Optional[str] = Field(sa_type=TEXT, description="用户定义的变量")
    request_url: Optional[str] = Field(sa_type=TEXT, description="请求的路径")
    request_param: Optional[str] = Field(sa_type=TEXT, description="请求的参数")
    real_response: Optional[str] = Field(sa_type=TEXT, description="请求真实的返回值")
    response_time: Optional[str] = Field(max_length=100, description="真实响应的耗时")
    assert_res_sign: Optional[str] = Field(sa_type=TEXT, description="响应的断言标志")
    assert_res_details: Optional[str] = Field(sa_type=TEXT, description="断言的详情")
    assert_ver_sign: Optional[str] = Field(sa_type=TEXT, description="结构自主比对的断言")
    assert_time_sign: Optional[str] = Field(max_length=100, description="响应时长的体验感受")
    remarks: Optional[str] = Field(max_length=100, description="执行的备注")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

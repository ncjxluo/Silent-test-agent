# -*- coding: utf-8 -*-
# @Time    : 2025/9/9 18:15
# @Author  : lwc
# @File    : result_reporting_listener.py
# @Description : 结果上报监听器

from src.components.listener.listener import Listener

from src.components.context import ctx
import uuid
import json
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
from src.models.str_test_suite import StrTestSuite
from src.models.str_test_plan import StrTestPlan
from src.models.str_test_case import StrTestCase
from src.models.str_test_case_step import StrTestCaseStep
from src.utils.str_db import async_session
from sqlmodel import select, and_, desc, func
import src.storage.global_context as global_context


class ResultReportingListener(Listener):

    def __init__(self, name):
        super().__init__(name)


    async def execute(self):
        local_ctx = ctx.get()
        query = (
            select(StrTestPlan)
            .join(StrTestSuite, StrTestPlan.suite_key == StrTestSuite.suite_key)  # type: ignore
            .where(
                and_(
                    StrTestSuite.user_key == 'a',
                    StrTestSuite.suite_name == global_context.global_storage['suite_name'],
                    StrTestSuite.status == "running",
                    StrTestSuite.type == "api",
                    StrTestPlan.plan_name == self.name
                )
            )
            .order_by(desc(StrTestSuite.created_at))
        )
        async with async_session() as session:
            result = await session.execute(query)
            res = result.first()[0]
            case_steps = list()
            case_status = 0
            case_id = str(uuid.uuid4())
            step_id = 1
            for key, value in local_ctx.items():
                if "_sampler" in key:
                    if "assert_data" not in local_ctx.get(key):
                        assert_res_sign = "该接口没有添加断言控制器"
                        assert_res_details = "该接口没有添加断言控制器"
                        assert_ver_sign = "该接口没有添加断言控制器"
                        assert_time_sign = "该接口没有添加断言控制器"
                    else:
                        assert_res_sign = local_ctx.get(key).get("assert_data").get("res_sign")
                        assert_res_details = json.dumps(local_ctx.get(key).get("assert_data").get("res_details"))
                        assert_ver_sign = json.dumps(local_ctx.get(key).get("assert_data").get("ver_sign"))
                        assert_time_sign = local_ctx.get(key).get("assert_data").get("time_sign")
                    if assert_res_sign == '整体断言:失败':
                        case_status = 1
                    case_step = StrTestCaseStep(
                        case_key = case_id,
                        step_id = step_id,
                        step_name = key,
                        user_variables = json.dumps(local_ctx.get("user_variable")),
                        request_url = local_ctx.get(key).get("req").get("url"),
                        request_param = json.dumps(local_ctx.get(key).get("req").get("params")),
                        real_response = local_ctx.get(key).get("last_response"),
                        response_time=local_ctx.get(key).get("last_response_time"),
                        assert_res_sign=assert_res_sign,
                        assert_res_details=assert_res_details,
                        assert_ver_sign=assert_ver_sign,
                        assert_time_sign=assert_time_sign
                    )
                    case_steps.append(case_step)
                    step_id = step_id + 1
            case = StrTestCase(
                suite_key=res.suite_key,
                plan_key=res.plan_key,
                case_key=case_id,
                case_status=case_status
            )
            session.add(case)
            session.add_all(case_steps)
            await session.commit()


    # async def to_db(self, data_list):
    #     """
    #     批量提交报告到数据库
    #     :param data_list: 一个需要向数据库提交的数据列表
    #     :return:
    #     """
    #     async with async_session() as session:
    #         session.add_all(data_list)
    #         await session.commit()









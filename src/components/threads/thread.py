# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:12
# @Author  : lwc
# @File    : thread.py
# @Description :

from src.components.basenode import BaseNode
from src.models.str_test_suite import StrTestSuite
from src.models.str_test_plan import StrTestPlan
from src.utils.str_db import async_session
import src.storage.global_context as global_context
from sqlmodel import select, and_, desc, func

class Thread(BaseNode):

    async def execute(self):
        raise NotImplementedError


    @staticmethod
    async def set_task_sum(count):
        """
        在这里汇报任务总数
        :param count: 要汇报的任务数量
        :return:
        """
        async with async_session() as session:
            query = (
                select(StrTestSuite).where(
                    and_(
                        StrTestSuite.user_key == 'a',
                        StrTestSuite.suite_name == global_context.global_storage['suite_name'],
                        StrTestSuite.status == "running",
                        StrTestSuite.type == "api",
                    )
                ).order_by(desc(StrTestSuite.created_at)).limit(1)
            )
            result = await session.execute(query)
            suite: StrTestSuite = result.first()[0]

            query = (
                select(StrTestPlan).where(
                    and_(
                        StrTestPlan.suite_key == suite.suite_key,
                        StrTestPlan.plan_name == global_context.global_storage['plan_name'],
                        StrTestPlan.status == "running"
                    )
                ).order_by(desc(StrTestPlan.created_at)).limit(1)
            )
            result = await session.execute(query)
            plan: StrTestPlan = result.first()[0]
            plan.plan_task_sum = count + int(plan.plan_task_sum)
            session.add(plan)
            await session.commit()
# -*- coding: utf-8 -*-
# @Time    : 2025/9/5 17:31
# @Author  : lwc
# @File    : testpaln.py
# @Description : 定义测试计划的类，继承基础类

from src.components.basenode import BaseNode
from src.models.str_test_suite import StrTestSuite
from src.models.str_test_plan import StrTestPlan
from src.utils.str_db import async_session
from sqlmodel import select, and_, desc, func
import uuid
from datetime import datetime
import src.storage.global_context as global_context


class TestPlan(BaseNode):

    async def execute(self):
        print(f"[TestPlan] Start: {self.name}")
        await self.before_hook()
        for child in self.children:
            await child.execute()
        await self.end_hook()


    async def before_hook(self):
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

            plan = StrTestPlan(
                suite_key = suite.suite_key,
                plan_name = self.name,
                status = "running"
            )
            session.add(plan)
            await session.commit()
            global_context.global_storage["plan_name"] = self.name


    async def end_hook(self):
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
                        StrTestPlan.plan_name == self.name,
                        StrTestPlan.status == "running"
                    )
                ).order_by(desc(StrTestPlan.created_at)).limit(1)
            )

            result = await session.execute(query)
            plan: StrTestPlan = result.first()[0]

            plan.status = "finish"
            plan.updated_at = datetime.now()

            session.add(plan)
            await session.commit()

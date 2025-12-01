# -*- coding: utf-8 -*-
# @Time    : 2025/10/14 17:54
# @Author  : lwc
# @File    : main.py.py
# @Description : 接口自动化测试执行的主入口

import time
from datetime import datetime
import asyncio
from src.components.paser.api_parser import ApiParser
from src.utils.str_config import StrConfig
import src.storage.global_context as global_context
from src.components.paser.str_parser import StrParser
from src.utils.str_db import async_session
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_get_path import get_realpath
from sqlmodel import select, and_, desc, func
from src.models.str_test_suite import StrTestSuite
import concurrent.futures
import os
import argparse


@str_log_decorate
async def before_run(name) -> None:
    """
    测试框架启动前需要执行的动作
    :return:
    """
    # 初始化数据库
    # start_time = time.time()
    print(name)
    global_context.global_storage["suite_name"] = name


    str_config = StrConfig()
    global_context.global_storage.get("env")["env"] = str_config.get_config().get("env")
    api_parser = ApiParser()
    api_parser.parser_api()
    # operations = ["testcases/permission/grant_auth.xml"]
    # parser = StrParser()
    # # for item in operations:
    # #     path = get_realpath(item)
    # #     testplan = parser.parse(path)
    # #     await testplan.execute()
    # end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    # print("测试前置钩子结束：" + end_time)
    # print('程序耗时{:.2f}'.format(time.time() - start_time))


@str_log_decorate
async def run(task):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("开始执行测试计划：" + start_time)
    start_time = time.time()
    # operations = ["testcases/sql/mysql_testcase.xml"]
    # operations = task
    parser = StrParser()
    path = get_realpath(task)
    testplan = parser.parse(path)
    await testplan.execute()
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("测试计划结束：" + end_time)
    print('程序耗时{:.2f}'.format(time.time() - start_time))

# async def run() -> None:
#     start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#     print("开始执行测试计划：" + start_time)
#     start_time = time.time()
#     # operations = ["testcases/sql/mysql_testcase.xml"]
#     operations = [
#         "testcases/sql/mysqlgather/mysql_testcase1.xml",
#         "testcases/sql/mysqlgather/mysql_testcase2.xml"
#     ]
#     # operations = [
#     #     "testcases/sql/mysqlgather/mysql_testcase1.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase2.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase3.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase4.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase5.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase6.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase7.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase8.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase9.xml",
#     #     "testcases/sql/mysqlgather/mysql_testcase10.xml"
#     # ]
#     tasks = [(op, i) for i, op in enumerate(operations)]
#     with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
#         results = list(executor.map(process_worker, tasks))
#         print("\n=== 执行结果 ===")
#         for result in results:
#             print(result)
#     # process_list = []
#     # for i in range(len(operations)):
#     #     process_list.append(multiprocessing.Process(target=process_worker, args=(operations[i],i)))
#     # for p in process_list:
#     #     p.start()
#     # for p in process_list:
#     #     p.join()
#     end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#     print("测试计划结束：" + end_time)
#     print('程序耗时{:.2f}'.format(time.time() - start_time))


# def process_worker(args):
#     start_time = time.time()
#     test_task, index = args
#     print(f"[{time.time() - start_time:.3f}s] 进程{index}启动 PID:{os.getpid()}")
#     str_config = StrConfig()
#     global_context.global_storage.get("env")["env"] = str_config.get_config().get("env")
#     api_parser = ApiParser()
#     api_parser.parser_api()
#     parser = StrParser()
#     path = get_realpath(test_task)
#     testplan = parser.parse(path)
#     asyncio.run(testplan.execute())


# async def end_run(name) -> None:
#     """
#     测试框架运行完成后需要执行的动作
#     :return:
#     """
#     async with async_session() as session:
#         query = (
#             select(StrTestSuite).where(
#                 and_(
#                     StrTestSuite.user_key == 'a',
#                     StrTestSuite.suite_name == f"agent{global_context.global_storage['suite_name']}",
#                     StrTestSuite.status == "running",
#                     StrTestSuite.type == "api",
#                 )
#             ).order_by(desc(StrTestSuite.created_at)).limit(1)
#         )
#         result = await session.execute(query)
#         suite = result.first()[0]
#         print(suite)
#         if suite:
#             suite.status = 'finish'
#             suite.updated_at = datetime.now()
#             session.add(suite)
#             await session.commit()


async def main(name, task):
    await before_run(name)
    await run(task)
    # await end_run(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--name")
    parser.add_argument("--task")
    args = parser.parse_args()
    asyncio.run(main(args.name, args.task))
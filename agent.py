# -*- coding: utf-8 -*-
# @Time    : 2025/11/21 14:22
# @Author  : lwc
# @File    : main.py
# @Description : 接口agent的入口

import subprocess
import time
from collections import deque
from src.models.str_test_suite import StrTestSuite
from src.utils.str_helper import get_local_ip
from sqlmodel import SQLModel, select, and_, desc, create_engine, Session
from src.utils.str_config import StrConfig
from datetime import datetime

MAX_JOBS = 5

running_jobs = []       # 运行任务的列表
task_queue = deque()       # 等待执行的任务队列

str_config = StrConfig()

IP = str_config.get_config().get("db").get("host")
PORT = str_config.get_config().get("db").get("port")
UNAME = str_config.get_config().get("db").get("user")
PASSWD = str_config.get_config().get("db").get("password")
SCHEMA = str_config.get_config().get("db").get("schema")

DATABASE_URL = f"mysql+pymysql://{UNAME}:{PASSWD}@{IP}:{PORT}/{SCHEMA}"

engine = create_engine(DATABASE_URL)


def try_start_new_job(suite_name, task_file):
    global running_jobs

    # 清除已结束的子进程
    running_jobs = [p for p in running_jobs if p.poll() is None]

    # 如果有空闲槽位，立刻启动任务
    if len(running_jobs) < MAX_JOBS:
        print(f"启动任务: {task_file}")
        p = subprocess.Popen(["python3", "interfaceMain.py","--name",suite_name, "--task", task_file])
        running_jobs.append(p)
    else:
        # 没槽位，加入队列
        print(f"队列等待: {task_file}")
        task_queue.append(task_file)


def monitor_jobs():
    """循环监控：有空位就从队列中取任务执行"""
    while running_jobs or task_queue:
        # 清理已结束的进程
        alive_jobs = []
        for p in running_jobs:
            if p.poll() is None:
                alive_jobs.append(p)
            else:
                print(f"任务完成 PID: {p.pid}")
        running_jobs[:] = alive_jobs

        # 尝试从队列启动新的任务
        while task_queue and len(running_jobs) < MAX_JOBS:
            task_file = task_queue.popleft()
            try_start_new_job(task_file)

        time.sleep(5)  # 避免空转 CPU


def before_run():
    suite_name = f'agent{get_local_ip()}'
    with Session(engine) as session:
        suite = StrTestSuite(
            user_key="a",
            suite_name=suite_name,
            status="running",
            type="api"  # todo 未完成
        )
        session.add(suite)
        session.commit()
    return suite_name


def end_run(suite_name) -> None:
    """
    测试框架运行完成后需要执行的动作
    :return:
    """
    with Session(engine) as session:
        query = select(StrTestSuite).where(
                and_(
                    StrTestSuite.user_key == 'a',
                    StrTestSuite.suite_name == suite_name,
                    StrTestSuite.status == "running",
                    StrTestSuite.type == "api",
                )
            ).order_by(desc(StrTestSuite.created_at)).limit(1)

        suite = session.exec(query).first()
        # suite = result.first()
        print(suite)
        if suite:
            suite.status = 'finish'
            suite.updated_at = datetime.now()
            session.add(suite)
            session.commit()


if __name__ == "__main__":
    suite_name = before_run()
    # operations = [
    #     "testcases/sql/mysqlgather/mysql_testcase1.xml",
    #     "testcases/sql/oraclegather/oracle_testcase1.xml",
    # ]
    operations = [
            "testcases/permission/grant_auth.xml"
        ]
    for item in operations:
        task_file = item
        try_start_new_job(suite_name, task_file)

    monitor_jobs()
    end_run(suite_name)

# -*- coding: utf-8 -*-
# @Time    : 2025/9/5 17:45
# @Author  : lwc
# @File    : thread_group.py
# @Description :
import time

import asyncio
from src.components.config_element.db_data_set import DBDataSet
from src.components.threads.thread import Thread
from src.utils.str_config import StrConfig
from concurrent.futures import ThreadPoolExecutor
from src.components.config_element.csv_data_set import CSVDataSet
from src.components.context import ctx
from src.utils.str_log import Log
import ast

class ThreadGroup(Thread):

    def __init__(self, name: str = "ThreadGroup", error_operation: str = "continue", threads: int = 1, ramp_up:int=0, enabled:str="True" ) -> None:
        super().__init__(name)
        self.error_operation = error_operation
        self.threads = int(threads)
        self.ramp_up = int(ramp_up)
        self.enabled = ast.literal_eval(enabled)

    async def execute(self) -> None:
        if self.enabled:
            print(f"[ThreadGroup] Start: {self.name}")
            str_config = StrConfig()
            max_threads = self.threads
            config_max_threads = str_config.get_config().get("threads").get("max-threads")
            if self.threads > config_max_threads:
                max_threads = config_max_threads
            count = 1
            for child in self.children:
                if isinstance(child, CSVDataSet):
                    count = child.data_queue.qsize()
                if isinstance(child, DBDataSet):
                    count = child.data_queue.qsize()
            await self.set_task_sum(count)
            sleep_time = self.ramp_up / max_threads
            tasks = []
            semaphore = asyncio.Semaphore(self.threads)
            if max_threads == 1:
                for x in range(count):
                    await self.run()
                    await asyncio.sleep(sleep_time)
            else:
                for x in range(count):
                    task = asyncio.create_task(self.run_with_semaphore(semaphore))
                    tasks.append(task)
                    await asyncio.sleep(sleep_time)
                if tasks:
                    # 捕获所有协程异常
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for res in results:
                        if isinstance(res, Exception):
                            Log().get_logger().exception("excute 出错了")
                            Log().get_logger().exception(res)
                # await asyncio.gather(*tasks)
        else:
            print(f"[ThreadGroup] enabled: {self.name}")

    async def run_with_semaphore(self, semaphore):
        async with semaphore:
            await self.run()

    async def run(self):
        token = ctx.set({})
        try:
            for child in self.children:
                 await child.execute()
        finally:
            ctx.reset(token)
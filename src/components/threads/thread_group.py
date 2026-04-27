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
                    # await self.run()
                    try:
                        await self.run()
                    except Exception as e:
                        Log().get_logger().exception(f"任务 {x} 执行失败", exc_info=True)
                    await asyncio.sleep(sleep_time)
            else:
                for x in range(count):
                    task = asyncio.create_task(self.run_with_semaphore(semaphore))
                    tasks.append(task)
                    await asyncio.sleep(sleep_time)
                if tasks:
                    # 捕获所有协程异常
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for i, res in enumerate(results):
                        if isinstance(res, Exception):
                            print(f"\n{'=' * 60}")
                            print(f"任务 {i} 执行失败:")
                            print(f"{'=' * 60}")
                            import traceback
                            traceback.print_exception(type(res), res, res.__traceback__)
                            print(f"{'=' * 60}\n")
                            # 方式1：直接使用 exception 并传入 exc_info
                            # Log().get_logger().exception(
                            #     f"任务 {i} 执行失败",
                            #     exc_info=res  # 关键：传入异常对象
                            # )
                            #
                            # # 或者方式2：打印完整堆栈
                            # import traceback
                            # tb_str = ''.join(traceback.format_exception(
                            #     type(res), res, res.__traceback__
                            # ))
                            # Log().get_logger().error(f"任务 {i} 失败:\n{tb_str}")
                    # for res in results:
                    #     if isinstance(res, Exception):
                    #         Log().get_logger().exception("excute 出错了")
                    #         Log().get_logger().exception(res)
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
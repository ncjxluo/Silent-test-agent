# -*- coding: utf-8 -*-
# @Time    : 2025/10/10 18:51
# @Author  : lwc
# @File    : constant_timer.py
# @Description : 定时器之固定定时器
import asyncio

from src.components.timer.timer import Timer
import time


class ConstantTimer(Timer):

    def __init__(self, name: str = "ConstantTimer", pause_time: str = 0.3) -> None:
        super().__init__(name)
        self.pause_time = int(pause_time)

    async def execute(self) -> None:
        # print("我要开始睡眠")
        await asyncio.sleep(self.pause_time)
        # time.sleep(self.pause_time)
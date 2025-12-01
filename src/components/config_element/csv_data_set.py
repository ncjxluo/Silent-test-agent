# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 13:14
# @Author  : lwc
# @File    : csv_data_set.py
# @Description : 配置元件之csv数据读取器

import csv
import queue
from src.components.config_element.config_element import ConfigElement
from src.components.context import ctx
from itertools import zip_longest
from src.utils.str_get_path import get_realpath
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
import os

class CSVDataSet(ConfigElement):

    def __init__(self, name: str, filename: str, **kwargs:dict) -> None:
        super().__init__(name)
        self.filename = filename
        self.data_queue = queue.Queue()
        filepath = get_realpath(f"template/{self.filename}")
        self.string_prop = kwargs.get("variableNames").split(",")

        with open(filepath, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                result = dict(zip_longest(self.string_prop, row, fillvalue=None))
                self.data_queue.put(result)


    async def execute(self) -> None:

        if self.data_queue.empty():
            # self.print_thread_info("[csv读取器]",f"[CSVDataSet] {self.name}: no data found")
            return
        value = self.data_queue.get()
        local_ctx = ctx.get().copy()
        if "user_variable" not in local_ctx:
            local_ctx["user_variable"] = value
        else:
            for key, value in value.items():
                local_ctx["user_variable"][key] = value
        ctx.set(local_ctx)
        for child in self.children:
            await child.execute()
# -*- coding: utf-8 -*-
# @Time    : 2025/9/16 11:32
# @Author  : lwc
# @File    : jdbc_data_set.py
# @Description : 配置元件之mysql读取器

from src.components.config_element.config_element import ConfigElement
from src.components.context import ctx
from itertools import zip_longest
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
import queue
import pymysql


class DBDataSet(ConfigElement):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name)

        conn = pymysql.connect(
            host=kwargs.get("ip"),
            port=int(kwargs.get("port")),
            user=kwargs.get("username"),
            password=kwargs.get("password"),
            db=kwargs.get("database"),
            charset="utf8mb4"
        )

        self.data_queue = queue.Queue()
        self.string_prop = kwargs.get("variableNames").split(",")
        cursor = conn.cursor()
        cursor.execute(kwargs.get("sql"))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            result = dict(zip_longest(self.string_prop, row, fillvalue=None))
            self.data_queue.put(result)


    async def execute(self) -> None:
        if self.data_queue.empty():
            # self.print_thread_info("[csv读取器]", f"[CSVDataSet] {self.name}: no data found")
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
# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 10:17
# @Author  : lwc
# @File    : cache_data_set.py
# @Description : 配置元件之cache数据读取器

from src.components.config_element.config_element import ConfigElement
import src.storage.global_context as global_context
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
from src.components.context import ctx
import threading

class CacheDataSet(ConfigElement):

    def __init__(self, name: str, **kwargs:dict) -> None:
        super().__init__(name)
        self.__dict__.update(kwargs)


    async def execute(self) -> None:
        local_ctx = ctx.get()
        for key, value in self.__dict__.items():
            if "c:" in key:
                key_value = key.split(":")
                if value != "all":
                    local_ctx[key_value[1]] = global_context.global_storage.get(key_value[1]).get(value)
                else:
                    local_ctx[key_value[1]] = global_context.global_storage.get(key_value[1]).get(key_value[1])

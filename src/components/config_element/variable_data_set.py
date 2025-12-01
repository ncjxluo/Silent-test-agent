# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 19:25
# @Author  : lwc
# @File    : variable_data_set.py
# @Description : 配置元件变量读取器

from src.components.config_element.config_element import ConfigElement
import src.storage.global_context as global_context
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
from src.components.context import ctx

class VariableDataSet(ConfigElement):

    def __init__(self, name: str, **kwargs:dict) -> None:
        super().__init__(name)
        self.__dict__.update(kwargs)


    async def execute(self) -> None:
        local_ctx = ctx.get().copy()
        if "user_variable" not in local_ctx:
            local_ctx["user_variable"] = {}
        for key, value in self.__dict__.items():
            if "u:" in key:
                key_value = key.split(":")
                local_ctx["user_variable"][key_value[1]] = value
        ctx.set(local_ctx)
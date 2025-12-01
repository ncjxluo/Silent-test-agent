# -*- coding: utf-8 -*-
# @Time    : 2025/9/19 15:53
# @Author  : lwc
# @File    : variable_rename.py
# @Description :

from src.components.pre_processors.pre_processors import PreProcessors
from src.components.context import ctx
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log


class VariableRename(PreProcessors):

    def __init__(self, name: str, **kwargs:dict) -> None:
        super().__init__(name)
        self.__dict__.update(kwargs)


    async def execute(self) -> None:
        local_ctx = ctx.get()
        if "variable_rename" not in local_ctx:
            local_ctx["variable_rename"] = {}

        for key, value in self.__dict__.items():
            if "vr:" in key:
                key_value = key.split(":")
                local_ctx["variable_rename"][key_value[1]] = value
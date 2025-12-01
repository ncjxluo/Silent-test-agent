# -*- coding: utf-8 -*-
# @Time    : 2025/9/14 16:08
# @Author  : lwc
# @File    : variable_modifier.py
# @Description :

from src.components.pre_processors.pre_processors import PreProcessors
from src.components.context import ctx
import jmespath
from typing import Any
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log


class VariableModifier(PreProcessors):

    def __init__(self, name: str, **kwargs:dict) -> None:
        super().__init__(name)
        self.__dict__.update(kwargs)


    async def execute(self) -> None:
        local_ctx = ctx.get()
        for key, value in self.__dict__.items():
            if "vm:" in key:
                key_value = key.split(":")
                path_list = key_value[1].removeprefix("$.").split(".")
                self.modifier_data(local_ctx.get("user_variable"), path_list, value)


    def modifier_data(self, obj, path_list, value):
        if not path_list:
            return
        key = path_list[0]
        rest = path_list[1:]
        if not rest:
            if key == "[]":
                if isinstance(obj, list):
                    for i in range(len(obj)):
                        if isinstance(value, dict) and isinstance(obj[i], dict):
                            obj[i].update(value)
                        else:
                            obj[i] = value
            else:
                obj[key] = value
            return
        if key == "[]":
            if isinstance(obj, list):
                for item in obj:
                    self.modifier_data(item, rest, value)
        else:
            if key not in obj:
                if isinstance(obj, list):
                    return
                else:
                    obj[key] = {} if rest[0] != "[]" else []
            self.modifier_data(obj[key], rest, value)

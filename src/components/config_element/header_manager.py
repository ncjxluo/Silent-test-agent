# -*- coding: utf-8 -*-
# @Time    : 2025/9/10 18:37
# @Author  : lwc
# @File    : header_manager.py
# @Description : 配置元件之信息头管理器

from src.components.config_element.config_element import ConfigElement
from src.components.context import ctx
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log


class HeaderManager(ConfigElement):

    def __init__(self, name: str, **kwargs:dict) -> None:
        super().__init__(name)
        self.__dict__.update(kwargs)


    async def execute(self):

        local_ctx = ctx.get()
        if "user_headers" not in local_ctx:
            local_ctx["user_headers"] = {}

        for key, value in self.__dict__.items():
            if "h:" in key:
                key_value = key.split(":")
                local_ctx["user_headers"][key_value[1]] = value
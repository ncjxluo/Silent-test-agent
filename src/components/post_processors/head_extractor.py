# -*- coding: utf-8 -*-
# @Time    : 2025/9/10 18:47
# @Author  : lwc
# @File    : head_extractor.py
# @Description :

from src.components.post_processors.post_processors import PostProcessors
from src.components.context import ctx
import json
from typing import Any
import jmespath
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log


class HeadExtractor(PostProcessors):

    def __init__(self, name: str = "", parentname: str = "", **kwargs) -> None:
        super().__init__(name)
        self.parentname = parentname
        self.__dict__.update(kwargs)


    async def execute(self) -> None:
        local_ctx = ctx.get()
        if "user_headers" not in local_ctx:
            local_ctx["user_headers"] = {}
        last_response = json.loads(local_ctx.get(f"{self.parentname}_sampler").get("last_response"))
        for key, value in self.__dict__.items():
            if "h:" in key:
                ey_value = key.split(":")
                self.header_set(last_response, value.removeprefix("$."), ey_value[1], local_ctx)
            # self.print_thread_info("[head提取器]",f"当前上下文缓存中的数据(header提取器中输出):{local_ctx}")


    @staticmethod
    def header_set(data: dict, path: str, key: str, local_ctx: Any, default: Any = "路径查找失败") -> None:
        # self.print_thread_info("[head提取器]",f"header的值{data}")
        result = jmespath.search(path, data)
        # self.print_thread_info("[head提取器]",f"header提取的值{result}")
        local_ctx["user_headers"][key] = result if result is not None else default
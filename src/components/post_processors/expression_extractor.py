# -*- coding: utf-8 -*-
# @Time    : 2025/9/10 17:39
# @Author  : lwc
# @File    : expression_extractor.py
# @Description : 表达式提取器

from src.components.post_processors.post_processors import PostProcessors
from src.components.context import ctx
import json
from typing import Any
import jmespath
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log


class ExpressionExtractor(PostProcessors):
    def __init__(self, name: str = "", parentname: str = "", **kwargs) -> None:
        super().__init__(name)
        self.parentname = parentname
        self.__dict__.update(kwargs)


    async def execute(self) -> None:
        local_ctx = ctx.get()
        if "user_variable" not in local_ctx:
            local_ctx["user_variable"] = {}
        if local_ctx.get("loop") is not None and local_ctx.get("loop") != 0:
            sampler_name = f"{self.parentname}_sampler_loop{local_ctx.get('loop')}"
        else:
            sampler_name = f"{self.parentname}_sampler"
        last_response = json.loads(local_ctx.get(sampler_name).get("last_response"))
        for key, value in self.__dict__.items():
            if "e:" in key:
                ey_value = key.split(":")
                self.ctx_set(last_response, value.removeprefix("$."), ey_value[1],local_ctx)


    @staticmethod
    def ctx_set(data:dict, path:str, key:str, local_ctx:Any, default:Any="路径查找失败") -> None:
        result = jmespath.search(path, data)
        local_ctx["user_variable"][key] = result if result is not None else default




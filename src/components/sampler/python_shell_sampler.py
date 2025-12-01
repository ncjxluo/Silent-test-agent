# -*- coding: utf-8 -*-
# @Time    : 2025/9/14 15:27
# @Author  : lwc
# @File    : python_shell_sampler.py
# @Description : python脚本取样器，传入python代码

from src.components.sampler.sampler import Sampler
from src.utils.str_log_decorate import str_log_decorate
from src.components.context import ctx
import textwrap

class PythonShellSampler(Sampler):

    def __init__(self, name, **kwargs:dict):
        super().__init__(name)
        self.__dict__.update(kwargs)


    async def execute(self):
        local_ctx = ctx.get()
        for key, value in self.__dict__.items():
            temp_vars = {}
            if "p:code" in key:
                script = textwrap.dedent(value)
                exec(script, {}, temp_vars)
                for key1, value1 in temp_vars.items():
                    if "<module" not in str(value1):
                        local_ctx["user_variable"][key1] = value1
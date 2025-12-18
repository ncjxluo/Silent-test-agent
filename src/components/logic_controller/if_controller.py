# -*- coding: utf-8 -*-
# @Time    : 2025/10/10 19:02
# @Author  : lwc
# @File    : if_controller.py
# @Description : 逻辑控制器之if控制器

import re
from string import Template
import json
from src.components.logic_controller.logic_controller import LogicController
import ast
from src.components.context import ctx
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log

class IfController(LogicController):

    def __init__(self, name: str = "IfController", condition: str = "", is_variable:str = "False", variable_position:str = "") -> None:
        super().__init__(name)
        self.condition = condition
        self.is_variable = ast.literal_eval(is_variable)
        self.variable_position = variable_position
        self.global_variables = ["user_variable", "user_headers", "env"]


    async def execute(self) -> None:
        if self.is_variable:
            local_ctx = ctx.get()
            condition = self.condition
            if any(self.variable_position == item for item in ["CSVDataSet", "VariableDataSet", "ExpressionExtractor"]):
                condition = self.substitute(condition, local_ctx.get("user_variable"))
            elif self.variable_position == "HeaderManager":
                condition = self.substitute(condition, local_ctx.get("user_headers"))
            elif self.variable_position == "CacheDataSet":
                condition = self.substitute(condition, local_ctx.get("env"))
            else:
                for item in self.global_variables:
                    condition = self.substitute(condition, local_ctx.get(item))
        else:
            condition = self.condition

        if "路径查找失败" in condition:
            condition = "1 != 1"

        if eval(condition):
            for child in self.children:
                await child.execute()


    def substitute(self, data, values):
        if isinstance(data, dict):
            return {k: self.substitute(v, values) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.substitute(v, values) for v in data]
        elif isinstance(data, str):
            tmp_data = Template(data).safe_substitute(values)  # 替换所有占位符
            return self.smart_parse(tmp_data)
        else:
            return data

    @staticmethod
    def smart_parse(s: str):
        try:
            return ast.literal_eval(s)
        except Exception:
            return s
# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:10
# @Author  : lwc
# @File    : config_element.py
# @Description : 配置元件的基类

from src.components.basenode import BaseNode


class ConfigElement(BaseNode):

    async def execute(self):
        raise NotImplementedError
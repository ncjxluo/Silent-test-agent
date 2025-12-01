# -*- coding: utf-8 -*-
# @Time    : 2025/10/10 19:01
# @Author  : lwc
# @File    : logic_controller.py
# @Description :

from src.components.basenode import BaseNode

class LogicController(BaseNode):

    async def execute(self):
        raise NotImplementedError
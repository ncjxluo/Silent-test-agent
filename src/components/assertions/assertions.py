# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:09
# @Author  : lwc
# @File    : assertions.py
# @Description :

from src.components.basenode import BaseNode

class Assertion(BaseNode):

    async def execute(self):
        raise NotImplementedError
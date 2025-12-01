# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:19
# @Author  : lwc
# @File    : pre_processors.py
# @Description :

from src.components.basenode import BaseNode


class PreProcessors(BaseNode):

    async def execute(self):
        raise NotImplementedError
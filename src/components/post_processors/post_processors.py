# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:18
# @Author  : lwc
# @File    : post_processors.py
# @Description :

from src.components.basenode import BaseNode


class PostProcessors(BaseNode):

    async def execute(self):
        raise NotImplementedError
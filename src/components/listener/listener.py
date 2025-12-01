# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:18
# @Author  : lwc
# @File    : listener.py
# @Description :

from src.components.basenode import BaseNode
from src.components.context import ctx


class Listener(BaseNode):

    async def execute(self):
        raise NotImplementedError
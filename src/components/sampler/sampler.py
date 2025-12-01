# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 15:11
# @Author  : lwc
# @File    : sampler.py
# @Description :

from src.components.basenode import BaseNode

class Sampler(BaseNode):

    async def execute(self):
        raise NotImplementedError
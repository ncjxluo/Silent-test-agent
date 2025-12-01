# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 13:12
# @Author  : lwc
# @File    : context.py
# @Description : 创建一个全局的上下文管理器

import contextvars

ctx = contextvars.ContextVar("ctx", default={})
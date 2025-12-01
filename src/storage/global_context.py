# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 17:33
# @Author  : lwc
# @File    : global_context.py
# @Description : 存储重要的缓存信息，如 实例 schema信息，接口的信息

env = dict()
interface = dict()
instance = dict()

global_storage = {
    "env": env,
    "interface": interface,
    "instance": instance,
    "suite_name": "",
    "plan_name": ""
}
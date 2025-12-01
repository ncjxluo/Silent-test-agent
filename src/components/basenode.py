# -*- coding: utf-8 -*-
# @Time    : 2025/9/5 14:42
# @Author  : lwc
# @File    : basenode.py
# @Description : 组件最基础的类
# import threading

class BaseNode:

    def __init__(self, name: str = "BaseNode") -> None:
        self.name = name
        self.children = []
        # self.debug = False

    def add_child(self, child) -> None:
        self.children.append(child)

    async def execute(self) -> None:
        raise NotImplementedError

    # def print_thread_info(self, name, result):
    #     if self.debug:
    #         current_thread = threading.current_thread()
    #         print(f"[{name}] 线程名: {current_thread.name}, 线程ID: {current_thread.ident}, 内容：{result}")

# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 11:02
# @Author  : lwc
# @File    : str_get_path.py
# @Description : 获取真实的路径

import os


def get_rootpath() -> str:
    """
    获取根路径
    :return: 返回获取运行文件的上级路径
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_realpath(path: str) -> str:
    """
    获取真实路径
    :param path: 传入路径
    :return: 返回拼接后的路径
    """
    return str(os.path.join(get_rootpath(), *filter(None, path.split("/"))))
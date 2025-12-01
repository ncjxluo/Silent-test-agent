# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 11:27
# @Author  : lwc
# @File    : str_config.py
# @Description : 读取项目的配置信息

from .str_get_path import get_realpath
import json

class StrConfig:

    def __init__(self) -> None:
        """
        定义配置文件从哪里获取，拿到他的真实路径
        """
        self.config_path = get_realpath("config/config.json")

    def get_config(self) -> dict:
        """
        获取配置信息
        :return: 配置信息
        """
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f).get("str-config")
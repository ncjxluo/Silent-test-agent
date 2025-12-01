# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 11:09
# @Author  : lwc
# @File    : str_log.py
# @Description : 定义一个日志对象，用于返回日志的对象

from loguru import logger
from .str_get_path import get_realpath, get_rootpath
import sys


class Log:
    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            log_dir = get_rootpath()
            logger.remove()
            logger.add(sys.stderr, level="INFO")
            logger.add(f"{log_dir}/logs/info.log", level="INFO", rotation="10 MB", retention="7 days", filter=lambda record: record["level"].name == "INFO")
            logger.add(f"{log_dir}/logs/error.log", level="ERROR", rotation="10 MB", retention="7 days")
            cls._instance.logger =  logger
        return cls._instance


    def get_logger(self) -> logger:
        """
        :return: 返回一个日志对象
        """
        return self.logger
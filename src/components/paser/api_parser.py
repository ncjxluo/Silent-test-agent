# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 17:37
# @Author  : lwc
# @File    : api_parser.py
# @Description : 解析api接口信息的解析器

from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_get_path import get_realpath
from typing import Union
from prance import ResolvingParser
from collections.abc import Generator
import os
import src.storage.global_context as global_context


class ApiParser:

    def __init__(self):
        self.path = get_realpath('apispecs')


    def cache_api(self, key: str, value: Union[dict, str]) -> None:
        """
        缓存接口定义文件中的operationId和文件路径
        :return:
        """
        global_context.global_storage.get("interface")[key] = value



    def parser_api(self) -> None:
        """
        读取接口描述文件,调用方法缓存api的信息
        :return: 无
        """
        for file in self.get_api():
            data = dict()
            parser_data = ResolvingParser(file)
            for item in parser_data.specification['paths'].keys():
                data["openapi"] = parser_data.specification['openapi']
                data["info"] = parser_data.specification['info']
                data["servers"] = parser_data.specification['servers']
                data["requestpath"] = item
                request_method = list(parser_data.specification.get("paths").get(item).keys())[0]
                data["requestmethod"] = request_method
                for item_key in parser_data.specification.get("paths").get(item).get(request_method).keys():
                    if item_key =="requestBody":
                        acppept = list(parser_data.specification.get("paths").get(item).get(request_method).get("requestBody").get("content").keys())[0]
                        data["accept"] = acppept
                        data["parameters"] = parser_data.specification.get("paths").get(item).get(request_method).get("requestBody").get("content").get(acppept).get("schema").get("properties")
                    elif item_key == "parameters":
                        data["accept"] = "application/json"
                        data["parameters"] = parser_data.specification.get("paths").get(item).get(request_method).get(item_key)
                    else:
                        data[item_key] = parser_data.specification.get("paths").get(item).get(request_method).get(item_key)
                self.cache_api(data.get("operationId"), data)


    def get_api(self, path: str = None) -> Generator[str]:
        """
        递归读取接口描述文件目录,持续获得所有的描述文件
        :return: 返回一个生成器对象
        """
        if path is None:
            path = self.path
        with os.scandir(path) as entrys:
            for entry in entrys:
                if entry.is_dir():
                    yield from self.get_api(entry.path)
                else:
                    yield entry.path


if __name__ == '__main__':
    api_parser = ApiParser()
    api_parser.parser_api()
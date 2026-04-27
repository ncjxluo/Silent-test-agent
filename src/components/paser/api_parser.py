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
import yaml
import src.storage.global_context as global_context


class ApiParser:

    def cache_api(self, key: str, value: Union[dict, str]) -> None:
        """
        缓存接口定义文件中的operationId和接口解析后的数据
        :return:
        """
        global_context.global_storage.get("interface")[key] = value



    # def parser_api(self, api_str_list: list) -> None:
    #     """
    #     读取接口描述文件,调用方法缓存api的信息
    #     :return: 无
    #     """
    #     for openapi_str in api_str_list:
    #         data = dict()
    #         # yaml_str = yaml.dump(openapi_str, default_flow_style=False, allow_unicode=True)
    #         parser_data = ResolvingParser(spec_string=openapi_str)
    #         print(parser_data)
    #         for item in parser_data.specification['paths'].keys():
    #             data["openapi"] = parser_data.specification['openapi']
    #             data["info"] = parser_data.specification['info']
    #             data["servers"] = parser_data.specification['servers']
    #             data["requestpath"] = item
    #             request_method = list(parser_data.specification.get("paths").get(item).keys())[0]
    #             data["requestmethod"] = request_method
    #             for item_key in parser_data.specification.get("paths").get(item).get(request_method).keys():
    #                 if item_key =="requestBody":
    #                     acppept = list(parser_data.specification.get("paths").get(item).get(request_method).get("requestBody").get("content").keys())[0]
    #                     data["accept"] = acppept
    #                     data["parameters"] = parser_data.specification.get("paths").get(item).get(request_method).get("requestBody").get("content").get(acppept).get("schema").get("properties")
    #                 elif item_key == "parameters":
    #                     data["accept"] = "application/json"
    #                     data["parameters"] = parser_data.specification.get("paths").get(item).get(request_method).get(item_key)
    #                 else:
    #                     data[item_key] = parser_data.specification.get("paths").get(item).get(request_method).get(item_key)
    #             self.cache_api(data.get("operationId"), data)
    def parser_api(self, api_str_list: list) -> None:
        """
        读取接口描述文件,调用方法缓存api的信息
        :return: 无
        """
        for openapi_str in api_str_list:
            data = dict()
            yaml_str = yaml.safe_load(openapi_str)
            for item in yaml_str.get('paths').keys():
                data["openapi"] = yaml_str.get('openapi')
                data["info"] = yaml_str.get('info')
                data["servers"] = yaml_str.get('servers')
                data["requestpath"] = item
                request_method = list(yaml_str.get("paths").get(item).keys())[0]
                data["requestmethod"] = request_method
                for item_key in yaml_str.get("paths").get(item).get(request_method).keys():
                    if item_key == "requestBody":
                        acppept = list(
                            yaml_str.get("paths").get(item).get(request_method).get("requestBody").get(
                                "content").keys())[0]
                        data["accept"] = acppept
                        data["parameters"] = yaml_str.get("paths").get(item).get(request_method).get(
                            "requestBody").get("content").get(acppept).get("schema").get("properties")
                    elif item_key == "parameters":
                        data["accept"] = "application/json"
                        data["parameters"] = yaml_str.get("paths").get(item).get(request_method).get(item_key)
                    else:
                        data[item_key] = yaml_str.get("paths").get(item).get(request_method).get(item_key)
                self.cache_api(data.get("operationId"), data)



    # def get_api(self, path: str = None) -> Generator[str]:
    #     """
    #     递归读取接口描述文件目录,持续获得所有的描述文件
    #     :return: 返回一个生成器对象
    #     """
    #     if path is None:
    #         path = self.path
    #     with os.scandir(path) as entrys:
    #         for entry in entrys:
    #             if entry.is_dir():
    #                 yield from self.get_api(entry.path)
    #             else:
    #                 yield entry.path


if __name__ == '__main__':
    api_parser = ApiParser()
    # api_parser.parser_api()
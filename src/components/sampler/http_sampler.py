# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 13:22
# @Author  : lwc
# @File    : http_sampler.py
# @Description :
import json

from src.components.sampler.sampler import Sampler
from src.components.assertions.assertions import Assertion
from src.components.config_element.config_element import ConfigElement
from src.components.listener.listener import Listener
from src.components.post_processors.post_processors import PostProcessors
from src.components.pre_processors.pre_processors import PreProcessors
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
from src.components.context import ctx
import threading
from typing import Optional, Tuple, Dict, Any
from string import Template
import ast
import time
import re
from datetime import datetime
from src.utils.str_client import get_client
from src.storage.global_context import interface


class HttpSampler(Sampler):
    def __init__(self, name, **kwargs:dict):
        super().__init__(name)
        # self.url = url
        self.__dict__.update(kwargs)
        self.config_element = []
        self.pre_processors = []
        self.post_processors = []
        self.assertions = []
        # print(self.children)


    async def execute(self):
        await self.before_run()
        await self.run()
        await self.end_run()


    async def before_run(self):
        for child in self.children:

            if isinstance(child, Assertion):
                self.assertions.append(child)
            elif isinstance(child, ConfigElement):
                self.config_element.append(child)
            elif isinstance(child, PreProcessors):
                self.pre_processors.append(child)
            elif isinstance(child, PostProcessors):
                self.post_processors.append(child)

        if self.config_element:
            for child in self.config_element:
                await child.execute()

        if self.pre_processors:
            for child in self.pre_processors:
                await child.execute()


    async def run(self):
        local_ctx = ctx.get()
        sampler_dic = {}
        for key,value in self.__dict__.items():
            if "h:" in key:
                key_value = key.split(":")
                sampler_dic[key_value[1]] = value
        # self.print_thread_info("[取样器]",f"当前上下文缓存中的数据:{local_ctx}")
        req_data,res_data,header_data = self.assemble_data(local_ctx, sampler_dic)
        await self.send_request(local_ctx, req_data, res_data,header_data)


    async def end_run(self):
        if self.post_processors:
            for child in self.post_processors:
                await child.execute()

        if self.assertions:
            for child in self.assertions:
                await child.execute()


    def assemble_data(self, local_ctx, sampler_dic) -> Tuple[dict, dict, dict]:
        """
        组装请求的参数
        :param local_ctx: 上下文对象
        :param sampler_dic: 取样器内部的变量
        :return:
        """
        req_data = dict()
        res_data = dict()
        header_data = dict()
        # 获取接口的operationId
        req_data["operationId"] = local_ctx.get("interface").get("operationId")
        # 获取接口的请求方法
        req_data["method"] = local_ctx.get("interface").get("requestmethod")
        # 获取接口的url
        req_data["url"] = self.substitute(local_ctx.get("interface").get("servers")[0].get("url")
                         + local_ctx.get("interface").get("requestpath"), local_ctx.get("env"))
        # 获取接口的描述
        req_data["desc"] = local_ctx.get("interface").get("description")
        # 获取接口的参数
        req_data["params"] = dict()
        interface_params = local_ctx.get("interface").get("parameters")

        if req_data.get("method").upper() == "GET":
            for item in interface_params:
                req_data["params"][item.get("name")] = item.get("example")
        elif req_data.get("method").upper() == "POST":
            for key, value in interface_params.items():
                req_data["params"][key] = value.get("example")

        if local_ctx.get("variable_rename"):
            req_data["params"] = self.substitute(req_data["params"], local_ctx.get("variable_rename"))

        # print(f'替换前{req_data["params"]}')

        if sampler_dic:
            # self.print_thread_info("[取样器]","根据规则，优先替换取样器内部的环境变量")
            req_data["params"] = self.substitute(req_data["params"], sampler_dic)

        # print(f'接口请求参数{req_data["params"]}')
        if "user_variable" in local_ctx:
            req_data["params"] = self.substitute(req_data["params"], local_ctx.get("user_variable"))

        res_data["response"] = self.deep_get_dict(local_ctx.get("interface").get("responses"), "*.content.*.schema.items.properties.data.properties")
        res_data["expectation"] = dict()
        for key, value in local_ctx.get("user_variable").items():
            if "expect" in key:
                res_data["expectation"][key] = value
        if local_ctx.get("user_headers"):
            pattern = r"\$\{.*?\}"
            for key, value in local_ctx.get("user_headers").items():
                if re.search(pattern, value):
                    header_data[key] = self.substitute(value, local_ctx.get("user_variable"))
                else:
                    header_data[key] = value
        local_ctx.pop("interface", None)
        return req_data,res_data,header_data


    async def send_request(self, local_ctx, req_data: dict, res_data:dict, header_data:dict):
        response = None
        req_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        client = await get_client()
        if req_data.get("method").upper() == "GET":
            response = await client.get(req_data.get("url"), headers=header_data, params=req_data.get("params"))
        elif req_data.get("method").upper() == "POST":
            response = await client.post(req_data.get("url"), headers=header_data, json=req_data.get("params"))
        # if self.name == "获取结果":
        #     print(response.text)
        if local_ctx.get("loop") is not None and local_ctx.get("loop") != 0:
            sampler_name = f"{self.name}_sampler_loop{local_ctx.get('loop')}"
        else:
            sampler_name = f"{self.name}_sampler"
        local_ctx[sampler_name] = {"req": req_data,
                                     "req_time": req_time,
                                     "expectation_response": res_data,
                                     "last_response": response.text,
                                     "last_response_time": f"{response.elapsed.total_seconds() * 1000:.3f}"}


    def substitute(self, data, values):
        if isinstance(data, dict):
            return {k: self.substitute(v, values) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.substitute(v, values) for v in data]
        elif isinstance(data, str):
            tmp_data = Template(data).safe_substitute(values)  # 替换所有占位符
            return self.smart_parse(tmp_data)
        else:
            return data


    @staticmethod
    def deep_get_dict(dic_data:dict, path:str) -> Optional[dict]:
        """
        根据path路径获取字典的数据,path允许使用*表示不确定的层级，但是使用*，只会取第一个
        :param dic_data: 字典
        :param path: get数据的路径
        :return:
        """
        cur_data = dic_data
        path = path.split(".")
        for p in path:
            if p == "*":  # 不确定的 key，就取第一个
                if isinstance(cur_data, dict):
                    cur_data = cur_data[next(iter(cur_data))]
                else:
                    return None
            else:
                cur_data = cur_data.get(p)
                if cur_data is None:
                    return None
        return cur_data

    @staticmethod
    def smart_parse(s: str):
        try:
            return ast.literal_eval(s)
        except Exception:
            return s
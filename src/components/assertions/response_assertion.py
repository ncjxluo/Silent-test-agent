# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 13:23
# @Author  : lwc
# @File    : response_assertion.py
# @Description :
from time import sleep
from typing import Any
from src.components.assertions.assertions import Assertion
from src.components.context import ctx
from src.utils.str_config import StrConfig
from decimal import Decimal
import ast,json,re
from src.utils.str_log_decorate import str_log_decorate
from src.utils.str_log import Log
from string import Template
import jmespath
from typing import Tuple, Dict, List


class ResponseAssertion(Assertion):

    def __init__(self, name, parentname, assert_type:str ="included", **kwargs):
        super().__init__(name)
        self.parentname = parentname
        self.assert_type = assert_type
        self.__dict__.update(kwargs)


    async def execute(self):

        local_ctx = ctx.get()
        str_config = StrConfig().get_config()
        res_content = list()
        assert_template = "整体断言:{result}"
        assert_details_template = "{content}"
        if local_ctx.get("loop") is not None and local_ctx.get("loop") != 0:
            sampler_name = f"{self.parentname}_sampler_loop{local_ctx.get('loop')}"
        else:
            sampler_name = f"{self.parentname}_sampler"

        last_response = json.loads(local_ctx.get(sampler_name).get("last_response"))

        if not last_response:
            res_details = assert_details_template.format(content=res_content)
            res_sign = assert_template.format(result="失败")
            assert_data = {
                "res_sign": res_sign,
                "res_details": res_details,
                "ver_sign": "没有获取到响应",
                "time_sign": "没有获取到响应"
            }
            # self.print_thread_info("[响应断言器]", f"断言的结果:{assert_data}")
            local_ctx[sampler_name]["assert_data"] = assert_data
        else:
            if self.__dict__.get("selfVerification") == "true":
                ver_sign = self.struct_assert(local_ctx, last_response,sampler_name)
            else:
                ver_sign = "自主校验功能未打开"

            time_sign = self.apdex_assert(local_ctx, str_config,sampler_name)
            total_result = self.core_assert(local_ctx, last_response,sampler_name)

            if all(total_result.get(k).get("overall") for k in total_result.keys()):
                assert_data = {
                    "res_sign": assert_template.format(result="成功"),
                    "res_details": assert_details_template.format(content=total_result),
                    "ver_sign": ver_sign,
                    "time_sign": time_sign
                }
            else:
                assert_data = {
                    "res_sign": assert_template.format(result="失败"),
                    "res_details": assert_details_template.format(content=total_result),
                    "ver_sign": ver_sign,
                    "time_sign": time_sign
                }
        local_ctx[sampler_name]["assert_data"] = assert_data


    def struct_assert(self, local_ctx, last_response, sampler_name):
        if last_response.get("data"):
            res_data = last_response.get("data")
            ver_dict = self.deep_verification(res_data,
                                              local_ctx.get(sampler_name).get(
                                                  "expectation_response").get("response"),
                                              "", {})
            if not ver_dict:
                ver_sign = "数据类型校验通过"
            else:
                ver_sign = f"数据类型校验告警,{ver_dict}"
        else:
            ver_sign = "响应体中缺少data"
        return ver_sign


    def apdex_assert(self, local_ctx, str_config,sampler_name):
        res_time = local_ctx.get(sampler_name).get("last_response_time")

        if Decimal(res_time) < Decimal(str_config.get("interface").get("apdex").get("perfect")):
            time_sign = "完美"
        elif Decimal(res_time) < Decimal(str_config.get("interface").get("apdex").get("excellent")):
            time_sign = "优秀"
        elif Decimal(res_time) < Decimal(str_config.get("interface").get("apdex").get("tolerable")):
            time_sign = "可容忍"
        elif Decimal(res_time) < Decimal(str_config.get("interface").get("apdex").get("intolerable")):
            time_sign = "糟糕的"
        else:
            time_sign = "体验度断言失败"
        return time_sign


    def core_assert(self, local_ctx, last_response,sampler_name):
        """
        核心断言函数，要对比真实数据和预期的结果是否一致
        :return:
        """
        value_pattern = r"\$\{.*?\}"
        total_result = {}
        for key, value in self.__dict__.items():
            if "a:" in key:
                key_value = key.split(":")
                path = key_value[1]
                if re.search(value_pattern, value):
                    real_values = self.substitute(value, local_ctx.get("user_variable"))
                else:
                    real_values = value
                expect_values = real_values.split(" or ")
                if len(path.split(".")) > 1:
                    res, details = self.path_assert(last_response, path.removeprefix("$."), expect_values)
                elif self.assert_type == "included":
                    res, details = self.included_assert(path, local_ctx.get(sampler_name).get("last_response"), expect_values)
                elif self.assert_type == "match":
                    res, details = self.match_assert(path, last_response.get(path), expect_values)
                else:
                    res, details = False, {}
                total_result[path] = {"overall": res, "details":details}
        return total_result


    def included_assert(self, path, last_response, except_values) -> Tuple[bool, Dict]:
        return_dic = {}
        res = []
        for i, except_value in enumerate(except_values):
            a_temp = f'"{path}":"{except_value}'
            if a_temp not in last_response:
                res.append(f"期望: {a_temp},匹配结果: 匹配失败")
            else:
                res.append(f"期望: {a_temp},匹配结果: 匹配成功")
        return_dic[0] = res
        overall = self.check_overall(return_dic)
        return overall, return_dic


    def match_assert(self, path, last_response, except_values):
        return_dic = {}
        res = []
        for i, except_value in enumerate(except_values):
            if not re.search(except_value, last_response):
                res.append(f"期望: {path}:{except_value},匹配结果: 匹配失败")
            else:
                res.append(f"期望: {path}:{except_value},匹配结果: 匹配成功")
        return_dic[0] = res
        overall = self.check_overall(return_dic)
        return overall, return_dic


    def deep_verification(self, data, rules, parent_key, exception_dict):
        exception_dict = exception_dict

        if "response" in rules:
            rules = rules.get('response')

        if isinstance(data, str):
            rule1 = rules.get("data")
            flag, msg = self.check(data, rule1)
            if not flag:
                exception_dict["data"] = msg

        for key, value in data.items():
            if key in rules:
                if isinstance(value, dict):
                    parent_key = parent_key
                    if "properties" in rules.get(key):
                        self.deep_verification(value, rules.get(key).get("properties"), key, exception_dict)
                    else:
                        self.deep_verification(value, rules.get(key), key, exception_dict)
                else:
                    rule1 = rules.get(key)
                    flag, msg = self.check(value, rule1)
                    if not flag:
                        if parent_key == "":
                            exception_dict[key] = msg
                        else:
                            exception_dict[f"{parent_key}.{key}"] = msg
            else:
                exception_dict[key] = "该字段未在接口文档描述中出现"
        return exception_dict

    @staticmethod
    def check(value, rule):
        nullable = False
        if "nullable" in rule:
            nullable = rule.get("nullable")
        field_type = rule.get("type")
        res_msg = f"该字段类型不符合要求,期望{field_type},得到{type(value)}"
        if not nullable and (value is None or value == "" or value == "null"):
            return False, f"该字段不能为空,值{value}"
        if field_type == "string":
            if not isinstance(value, str):
                return False, res_msg
        elif field_type == "integer":
            if not isinstance(value, int):
                return False, res_msg
        elif field_type == "boolean":
            if not isinstance(value, bool):
                return False, res_msg
        elif field_type == "array":
            if not isinstance(value, list):
                return False, res_msg
        return True, ""


    def path_assert(self, data: dict, path: str, except_values: list) -> Tuple[bool, Dict]:

        path_search_result = jmespath.search(path, data)
        if path_search_result is None:
            return False, {}

        return_dic = {}
        self.assert_date(except_values, path_search_result, return_dic)
        overall = self.check_overall(return_dic)

        return overall, return_dic


    def assert_date(self, except_values, path_search_result, return_dic):
        if isinstance(path_search_result, list):
            for i, item in enumerate(path_search_result):
                if isinstance(item, list):
                    return_dic[i] = {}
                    self.assert_date(except_values, item, return_dic[i])
                else:
                    return_dic[i] = self.check_value(except_values, item)
        else:
            return_dic[0] = self.check_value(except_values, path_search_result)


    def check_overall(self, dic):
        if isinstance(dic, dict):
            return all(self.check_overall(v) for v in dic.values())
        elif isinstance(dic, list):
            return any("匹配成功" in r for r in dic)
        return False


    @staticmethod
    def check_value(except_values, real_result):
        res_list = list()
        for except_value in except_values:
            if real_result is None:
                res_list.append(f"期望: {except_value} ==>真实返回: {real_result},匹配结果: 匹配失败")
            elif isinstance(real_result, str):
                if except_value in real_result or re.search(except_value, real_result):
                    res_list.append(f"期望: {except_value} ==>真实返回: {real_result},匹配结果: 匹配成功")
                else:
                    res_list.append(f"期望: {except_value} ==>真实返回: {real_result},匹配结果: 匹配失败")
            else:
                if real_result == except_value:
                    res_list.append(f"期望: {except_value} ==>真实返回: {real_result},匹配结果: 匹配成功")
                else:
                    res_list.append(f"期望: {except_value} ==>真实返回: {real_result},匹配结果: 匹配失败")
        return res_list


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
    def smart_parse(s: str):
        try:
            return ast.literal_eval(s)
        except Exception:
            return s
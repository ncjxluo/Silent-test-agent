# -*- coding: utf-8 -*-
# @Time    : 2026/4/11 22:37
# @Author  : lwc
# @File    : deepdiff_response_assertion.py
# @Description : 深度对比断言

from src.components.assertions.assertions import Assertion
from src.components.context import ctx
import json
from deepdiff import DeepDiff


class DeepDiffResponseAssertion(Assertion):

    def __init__(self, name, parentname, comparison_name, **kwargs):
        super().__init__(name)
        self.parentname = parentname
        self.comparison_name = comparison_name
        self.__dict__.update(kwargs)


    async def execute(self):
        local_ctx = ctx.get()
        assert_template = "整体断言:{result}"
        assert_details_template = "{content}"
        # 由于无法控制循环次数一直，不能支持这种情况下的结果比对
        current_sampler_name = f"{self.parentname}_sampler"
        current_last_response = json.loads(local_ctx.get(current_sampler_name).get("last_response"))
        benchmark_sampler_name = f"{self.comparison_name}_sampler"
        benchmark_last_response = json.loads(local_ctx.get(benchmark_sampler_name).get("last_response"))
        if not current_last_response or not benchmark_last_response:
            res_details = assert_details_template.format(content={})
            res_sign = assert_template.format(result="失败")
            assert_data = {
                "res_sign": res_sign,
                "res_details": res_details,
                "ver_sign": "没有获取到响应",
                "time_sign": "没有获取到响应"
            }
            # self.print_thread_info("[响应断言器]", f"断言的结果:{assert_data}")
            local_ctx[current_sampler_name]["assert_data"] = assert_data
        else:
            result = DeepDiff(current_last_response, benchmark_last_response, ignore_order=True,
                              exclude_obj_callback=self.exclude_obj_callback)
            current_res_time = local_ctx.get(current_sampler_name).get("last_response_time")
            benchmark_res_time = local_ctx.get(benchmark_sampler_name).get("last_response_time")
            if not result:
                assert_data = {
                    "res_sign": assert_template.format(result="成功"),
                    "res_details": assert_details_template.format(content="响应完全一致"),
                    "ver_sign": "对比断言无自主校验功能",
                    "time_sign": f"当前响应时间:{current_res_time},对比响应时间:{benchmark_res_time}"
                }
            else:
                assert_data = {
                    "res_sign": assert_template.format(result="失败"),
                    "res_details": assert_details_template.format(content=result),
                    "ver_sign": "对比断言无自主校验功能",
                    "time_sign": f"当前响应时间:{current_res_time},对比响应时间:{benchmark_res_time}"
                }
        local_ctx[current_sampler_name]["assert_data"] = assert_data


    def exclude_obj_callback(self, obj, path):
        ignore_fields = {"id", "key", "connect_id", "schema_id", "time"}
        return any(field in path for field in ignore_fields)


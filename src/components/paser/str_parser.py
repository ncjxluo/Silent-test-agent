# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 13:24
# @Author  : lwc
# @File    : str_parser.py
# @Description :

from src.utils.str_log_decorate import str_log_decorate
import xml.etree.ElementTree as ET
from src.components.testpaln import TestPlan
from src.components.threads.thread_group import ThreadGroup
from src.components.threads.before_thread_group import BeforeThreadGroup
from src.components.threads.end_thread_group import EndThreadGroup
from src.components.assertions.response_assertion import ResponseAssertion
from src.components.config_element.csv_data_set import CSVDataSet
from src.components.sampler.http_sampler import HttpSampler
from src.components.sampler.python_shell_sampler import PythonShellSampler
from src.components.config_element.cache_data_set import CacheDataSet
from src.components.config_element.header_manager import HeaderManager
from src.components.config_element.variable_data_set import VariableDataSet
from src.components.post_processors.expression_extractor import ExpressionExtractor
from src.components.post_processors.head_extractor import HeadExtractor
from src.components.listener.result_reporting_listener import ResultReportingListener
from src.components.pre_processors.variable_modifier import VariableModifier
from src.components.config_element.db_data_set import DBDataSet
from src.components.pre_processors.variable_rename import VariableRename
from src.components.timer.constant_timer import ConstantTimer
from src.components.logic_controller.if_controller import IfController
from src.components.logic_controller.while_controller import WhileController


class StrParser:
    NODE_MAP = {
        "TestPlan": TestPlan,
        "ThreadGroup": ThreadGroup,
        "BeforeThreadGroup": BeforeThreadGroup,
        "EndThreadGroup": EndThreadGroup,
        "CSVDataSet": CSVDataSet,
        "HttpSampler": HttpSampler,
        "ResponseAssertion": ResponseAssertion,
        "CacheDataSet": CacheDataSet,
        "VariableDataSet": VariableDataSet,
        "ResultReportingListener": ResultReportingListener,
        "ExpressionExtractor": ExpressionExtractor,
        "HeaderManager": HeaderManager,
        "HeadExtractor": HeadExtractor,
        "PythonShellSampler": PythonShellSampler,
        "VariableModifier": VariableModifier,
        "DBDataSet": DBDataSet,
        "VariableRename": VariableRename,
        "ConstantTimer": ConstantTimer,
        "IfController": IfController,
        "WhileController": WhileController
    }

    @str_log_decorate
    def parse(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        return self._parse_node(root)


    def _parse_node(self, elem):
        cls = self.NODE_MAP.get(elem.tag)
        obj = None
        if cls:
            kwargs = dict(elem.attrib)
            for child in elem:
                if "Prop" in child.tag:
                    kwargs[child.get("name")] = child.text
            obj = cls(**kwargs)
            for child_elem in elem:
                child_obj = self._parse_node(child_elem)
                if child_obj is not None:
                    obj.add_child(child_obj)
        return obj

# -*- coding: utf-8 -*-
# @Time    : 2026/4/8 17:12
# @Author  : lwc
# @File    : str_es.py
# @Description :

from src.utils.str_config import StrConfig
from elasticsearch import AsyncElasticsearch

str_config = StrConfig()
IP = str_config.get_config().get("es").get("host")
PORT = str_config.get_config().get("es").get("port")
UNAME = str_config.get_config().get("es").get("user")
PASSWD = str_config.get_config().get("es").get("password")


def get_es_client() -> AsyncElasticsearch:
    """
    异步 ES 客户端连接池
    返回一个单例的 ES 实例
    """
    # print("我执行了")
    return AsyncElasticsearch(
        hosts=[f"http://{UNAME}:{PASSWD}@{IP}:{PORT}"],
        connections_per_node=40,      # 连接池大小
        max_pending_requests=100,
        request_timeout=10,
        retry_on_timeout=True,
        keep_alive="30s",
    )

# 创建全局单例（只创建一次）
es = get_es_client()
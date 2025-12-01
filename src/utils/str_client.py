# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 15:50
# @Author  : lwc
# @File    : str_session.py
# @Description : 发送请求的异步客户端对象
import httpx
from typing import Optional

# 增加一个静态类型的校验，为了close中可以没有经过，并且有提示
client : Optional[httpx.AsyncClient] = None


async def get_client() -> httpx.AsyncClient:
    """
    得到一个全局的client，这样可以复用连接池
    :return: 返回一个httpx的异步客户端对象
    """
    global client
    if client is None:
        limits = httpx.Limits(
            max_connections = 50,
            max_keepalive_connections= 10,
            keepalive_expiry = 300
        )
        timeout = httpx.Timeout(
            connect=20,
            read=60,
            write=60,
            pool=60
        )

        client = httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            proxy=None
        )
    return client


async def close_client():
    """
    关闭httpx的异步客户端对象
    :return:
    """
    await client.aclose()

# -*- coding: utf-8 -*-
# @Time    : 2025/10/15 11:03
# @Author  : lwc
# @File    : log_decorate.py
# @Description : 记录日志的装饰器

from functools import wraps
from .str_log import Log
import inspect
import traceback
import time

str_logger = Log().get_logger()

def str_log_decorate(func):

    if inspect.isasyncgenfunction(func):
        @wraps(func)
        async def async_gen_wrapper(*args, **kwargs):
            start_time = time.time()
            str_logger.info(f"{func.__name__} 开始")
            try:
                async for item in func(*args, **kwargs):
                    yield item
                str_logger.info(f"{func.__name__} 结束, 耗时:{time.time()-start_time:.2f}s")
            except Exception:
                str_logger.error(f"{func.__name__} 异常")
                str_logger.error(traceback.format_exc())
                raise

        return async_gen_wrapper
    elif inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            str_logger.info(f"{func.__name__} 开始")
            try:
                result = await func(*args, **kwargs)
                str_logger.info(f"{func.__name__} 结束, 耗时:{time.time()-start_time:.2f}s")
                return result
            except Exception:
                str_logger.error(f"{func.__name__} 异常")
                str_logger.error(traceback.format_exc())
                raise
        return async_wrapper
    elif inspect.isgeneratorfunction(func):
        @wraps(func)
        def gen_wrapper(*args, **kwargs):
            start_time = time.time()
            str_logger.info(f"{func.__name__} 开始")
            try:
                for item in func(*args, **kwargs):
                    yield item
                str_logger.info(f"{func.__name__} 结束, 耗时:{time.time()-start_time:.2f}s")
            except Exception:
                str_logger.error(f"{func.__name__} 异常")
                str_logger.error(traceback.format_exc())
                raise

        return gen_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            str_logger.info(f"{func.__name__} 开始")
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                str_logger.info('程序耗时{:.2f}'.format(time.time() - start_time))
                str_logger.info(f"{func.__name__} 结束, 耗时:{time.time()-start_time:.2f}s")
                return result
            except Exception:
                str_logger.error(f"{func.__name__} 异常")
                str_logger.error(traceback.format_exc())
                raise

        return sync_wrapper
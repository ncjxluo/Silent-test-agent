# -*- coding: utf-8 -*-
# @Time    : 2025/11/21 18:49
# @Author  : lwc
# @File    : str_helper.py
# @Description :
import socket
import psutil
import time

def get_local_ip():
    """获取本机IP地址（局域网IP）"""
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个外部地址（这里用Google DNS）
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return socket.gethostname()


def get_local_cpu():
    return str(psutil.cpu_percent(interval=1))


def get_local_memory():
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    return str(mem_percent)


def get_local_io():
    disk_io = psutil.disk_io_counters()
    # 获取磁盘繁忙度（需要先获取一次做基准）
    io_time_1 = disk_io.read_time + disk_io.write_time
    time.sleep(0.1)
    disk_io_2 = psutil.disk_io_counters()
    io_time_2 = disk_io_2.read_time + disk_io_2.write_time
    io_util = min(100, (io_time_2 - io_time_1) / 10.0)
    return str(io_util)
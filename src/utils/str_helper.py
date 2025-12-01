# -*- coding: utf-8 -*-
# @Time    : 2025/11/21 18:49
# @Author  : lwc
# @File    : str_helper.py
# @Description :
import socket

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
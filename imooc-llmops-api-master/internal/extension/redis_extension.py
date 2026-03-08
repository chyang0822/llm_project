#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/16 15:37
@Author  : thezehui@gmail.com
@File    : redis_extension.py
"""
import redis
from redis.connection import Connection, SSLConnection

# redis客户端
redis_client = redis.Redis()


def init_app(app):
    """初始化redis客户端（兼容FastAPI）"""
    # 1.获取配置（FastAPI使用conf属性）
    config = app.conf if hasattr(app, 'conf') else app.config
    
    # 2.检测不同的场景使用不同的连接方式
    connection_class = Connection
    if getattr(config, "REDIS_USE_SSL", False):
        connection_class = SSLConnection

    # 3.创建redis连接池
    redis_client.connection_pool = redis.ConnectionPool(**{
        "host": getattr(config, "REDIS_HOST", "localhost"),
        "port": getattr(config, "REDIS_PORT", 6379),
        "username": getattr(config, "REDIS_USERNAME", None),
        "password": getattr(config, "REDIS_PASSWORD", None),
        "db": getattr(config, "REDIS_DB", 0),
        "encoding": "utf-8",
        "encoding_errors": "strict",
        "decode_responses": False
    }, connection_class=connection_class)

    # 4.保存到app扩展（FastAPI需要先创建extensions字典）
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    app.extensions["redis"] = redis_client

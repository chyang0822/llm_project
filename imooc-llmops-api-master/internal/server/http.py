#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 15:10
@Author  : thezehui@gmail.com
@File    : http.py
"""
import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import Config
from internal.exception import CustomException
from internal.extension import logging_extension, redis_extension, celery_extension
from internal.middleware import Middleware
from internal.router import Router
from pkg.response import HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(FastAPI):
    """Http服务引擎"""

    def __init__(
            self,
            conf: Config,
            db: SQLAlchemy,
            middleware: Middleware,
            router: Router,
            **kwargs,
    ):
        # 1.调用父类构造函数初始化，添加文档配置
        super().__init__(
            title="LLMOps API",
            description="LLMOps平台API文档",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
            **kwargs
        )

        # 2.保存配置
        self.conf = conf
        self.db = db
        self.middleware_handler = middleware

        # 3.初始化扩展
        redis_extension.init_app(self)
        celery_extension.init_app(self)
        logging_extension.init_app(self)

        # 4.添加CORS中间件
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 5.注册异常处理器
        self.add_exception_handler(Exception, self._exception_handler)

        # 6.注册应用路由
        router.register_router(self)

    async def _exception_handler(self, request: Request, exc: Exception):
        """全局异常处理器"""
        # 1.日志记录异常信息
        logging.error("An error occurred: %s", exc, exc_info=True)

        # 2.异常信息是不是我们的自定义异常，如果是可以提取message和code等信息
        if isinstance(exc, CustomException):
            return JSONResponse(
                status_code=200,
                content={
                    "code": exc.code.value,
                    "message": exc.message,
                    "data": exc.data if exc.data is not None else {},
                }
            )

        # 3.如果不是我们的自定义异常，则有可能是程序、数据库抛出的异常，也可以提取信息，设置为FAIL状态码
        if os.getenv("ENVIRONMENT") == "development":
            raise exc
        else:
            return JSONResponse(
                status_code=200,
                content={
                    "code": HttpCode.FAIL.value,
                    "message": str(exc),
                    "data": {},
                }
            )

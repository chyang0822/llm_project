#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/19 16:46
@Author  : thezehui@gmail.com
@File    : celery_extension.py
"""
from celery import Task, Celery


def init_app(app):
    """Celery配置服务初始化（兼容FastAPI）"""
    
    # 获取配置（FastAPI使用conf属性）
    config = app.conf if hasattr(app, 'conf') else app.config
    app_name = getattr(app, 'title', 'llmops')  # FastAPI使用title属性

    class AppTask(Task):
        """定义AppTask，确保Celery可以访问应用配置"""
        _app = app
        
        def __call__(self, *args, **kwargs):
            # FastAPI不需要app_context
            return self.run(*args, **kwargs)

    # 1.创建Celery应用并配置
    celery_app = Celery(app_name, task_cls=AppTask)
    celery_config = getattr(config, "CELERY", {})
    celery_app.config_from_object(celery_config)
    celery_app.set_default()

    # 2.将celery挂载到app的扩展中
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    app.extensions["celery"] = celery_app

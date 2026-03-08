#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 15:18
@Author  : thezehui@gmail.com
@File    : app.py
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import dotenv

from config import Config
from internal.middleware import Middleware
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from app.http.module import injector

# 1.将env加载到环境变量中
dotenv.load_dotenv()

# 2.构建LLMOps项目配置
conf = Config()

app = Http(
    conf=conf,
    db=injector.get(SQLAlchemy),
    middleware=injector.get(Middleware),
    router=injector.get(Router),
)

celery = app.extensions.get("celery") if hasattr(app, "extensions") else None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

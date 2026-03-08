#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/09 0:49
@Author  : thezehui@gmail.com
@File    : analysis_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from injector import inject

from fastapi import Depends
from internal.dependencies import get_current_user, get_api_key_user
from internal.model import Account

from internal.service import AnalysisService
from pkg.response import success_json


@inject
@dataclass
class AnalysisHandler:
    """统计分析处理器"""
    analysis_service: AnalysisService

    async def get_app_analysis(self, app_id: UUID):
        """根据传递的应用id获取应用的统计信息"""
        app_analysis = self.analysis_service.get_app_analysis(app_id, current_user)
        return success_json(app_analysis)

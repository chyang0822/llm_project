#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/02 15:27
@Author  : thezehui@gmail.com
@File    : language_model_handler.py
"""
import io
from dataclasses import dataclass

from flask import send_file
from injector import inject

from fastapi import Depends
from internal.dependencies import get_current_user, get_api_key_user
from internal.model import Account

from internal.service import LanguageModelService
from pkg.response import success_json


@inject
@dataclass
class LanguageModelHandler:
    """语言模型处理器"""
    language_model_service: LanguageModelService
    async def get_language_models(self):
        """获取所有的语言模型提供商信息"""
        return success_json(self.language_model_service.get_language_models())
    async def get_language_model(self, provider_name: str, model_name: str):
        """根据传递的提供商名字+模型名字获取模型详细信息"""
        return success_json(self.language_model_service.get_language_model(provider_name, model_name))

    async def get_language_model_icon(self, provider_name: str):
        """根据传递的提供者名字获取指定提供商的icon图标"""
        icon, mimetype = self.language_model_service.get_language_model_icon(provider_name)
        return send_file(io.BytesIO(icon), mimetype)

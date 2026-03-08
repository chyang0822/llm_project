#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/02 10:45
@Author  : thezehui@gmail.com
@File    : ai_handler.py
"""
from dataclasses import dataclass

from fastapi import Depends, Request
from injector import inject

from internal.dependencies import get_current_user
from internal.model import Account
from internal.schema.ai_schema import OptimizePromptReq, GenerateSuggestedQuestionsReq
from internal.service import AIService
from pkg.response import validate_error_json, compact_generate_response, success_json


@inject
@dataclass
class AIHandler:
    """AI辅助模块处理器"""
    ai_service: AIService

    async def optimize_prompt(self, request: Request, current_user: Account = Depends(get_current_user)):
        """根据传递的预设prompt进行优化"""
        # 1.从request中获取表单数据并校验
        form_data = await request.form()
        req = OptimizePromptReq(formdata=form_data)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务优化prompt
        resp = self.ai_service.optimize_prompt(req.prompt.data)

        return compact_generate_response(resp)

    async def generate_suggested_questions(self, request: Request, current_user: Account = Depends(get_current_user)):
        """根据传递的消息id生成建议问题列表"""
        # 1.从request中获取表单数据并校验
        form_data = await request.form()
        req = GenerateSuggestedQuestionsReq(formdata=form_data)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务生成建议问题列表
        suggested_questions = self.ai_service.generate_suggested_questions_from_message_id(
            req.message_id.data,
            current_user,
        )

        return success_json(suggested_questions)

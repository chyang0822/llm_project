#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/25 0:16
@Author  : thezehui@gmail.com
@File    : auth_handler.py
"""
from dataclasses import dataclass

from fastapi import Depends, Request
from injector import inject

from internal.dependencies import get_current_user
from internal.model import Account
from internal.schema.auth_schema import PasswordLoginReq, PasswordLoginResp
from internal.service import AccountService
from pkg.response import success_message, validate_error_json, success_json


@inject
@dataclass
class AuthHandler:
    """LLMOps平台自有授权认证处理器"""
    account_service: AccountService

    async def password_login(self, request: Request):
        """账号密码登录"""
        # 1.从request中获取表单数据并校验
        form_data = await request.form()
        req = PasswordLoginReq(formdata=form_data)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务登录账号
        credential = self.account_service.password_login(req.email.data, req.password.data)

        # 3.创建响应结构并返回
        resp = PasswordLoginResp()

        return success_json(resp.dump(credential))

    async def logout(self, current_user: Account = Depends(get_current_user)):
        """退出登录，用于提示前端清除授权凭证"""
        return success_message("退出登陆成功")

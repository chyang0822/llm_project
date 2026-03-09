#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI 版本的认证处理器
"""
from dataclasses import dataclass
from fastapi import Depends, Form
from pydantic import ValidationError
from injector import inject

from internal.dependencies import get_current_user
from internal.model import Account
from internal.schema.auth_schema_fastapi import PasswordLoginReqFastAPI, PasswordLoginResp
from internal.service import AccountService
from pkg.response import success_message, success_json, fail_message, validate_error_json


@inject
@dataclass
class AuthHandlerFastAPI:
    """LLMOps平台自有授权认证处理器 - FastAPI 版本"""
    account_service: AccountService

    async def password_login(
        self,
        email: str = Form(..., description="登录邮箱"),
        password: str = Form(..., description="账号密码")
    ):
        """账号密码登录 - FastAPI 版本"""
        try:
            # 1.验证请求数据
            req = PasswordLoginReqFastAPI(email=email, password=password)
            
            # 2.调用服务登录账号
            credential = self.account_service.password_login(req.email, req.password)
            
            # 3.创建响应结构并返回
            resp = PasswordLoginResp(
                access_token=credential.access_token,
                expire_at=credential.expire_at
            )
            
            return success_json(resp.model_dump())
            
        except ValidationError as e:
            # 处理验证错误
            errors = {}
            for error in e.errors():
                field = error['loc'][0]
                errors[field] = [error['msg']]
            return validate_error_json(errors)
        except Exception as e:
            return fail_message(str(e))

    async def logout(self, current_user: Account = Depends(get_current_user)):
        """退出登录，用于提示前端清除授权凭证"""
        return success_message("退出登陆成功")

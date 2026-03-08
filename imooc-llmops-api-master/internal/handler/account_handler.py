#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/25 22:43
@Author  : thezehui@gmail.com
@File    : account_handler.py
"""
from dataclasses import dataclass

from fastapi import Depends, Request
from injector import inject

from internal.dependencies import get_current_user
from internal.model import Account
from internal.schema.account_schema import GetCurrentUserResp, UpdatePasswordReq, UpdateNameReq, UpdateAvatarReq
from internal.service import AccountService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AccountHandler:
    """账号设置处理器"""
    account_service: AccountService

    async def get_current_user(self, current_user: Account = Depends(get_current_user)):
        """获取当前登录账号信息"""
        resp = GetCurrentUserResp()
        return success_json(resp.dump(current_user))

    async def update_password(self, request: Request, current_user: Account = Depends(get_current_user)):
        """更新当前登录账号密码"""
        # 1.从request中获取表单数据并校验
        form_data = await request.form()
        req = UpdatePasswordReq(formdata=form_data)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新账号密码
        self.account_service.update_password(req.password.data, current_user)

        return success_message("更新账号密码成功")

    async def update_name(self, request: Request, current_user: Account = Depends(get_current_user)):
        """更新当前登录账号名称"""
        # 1.从request中获取表单数据并校验
        form_data = await request.form()
        req = UpdateNameReq(formdata=form_data)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新账号名称
        self.account_service.update_account(current_user, name=req.name.data)

        return success_message("更新账号名称成功")

    async def update_avatar(self, request: Request, current_user: Account = Depends(get_current_user)):
        """更新当前账号头像信息"""
        # 1.从request中获取表单数据并校验
        form_data = await request.form()
        req = UpdateAvatarReq(formdata=form_data)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新账号名称
        self.account_service.update_account(current_user, avatar=req.avatar.data)

        return success_message("更新账号头像成功")

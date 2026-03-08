#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/25 10:42
@Author  : thezehui@gmail.com
@File    : middleware.py
"""
from dataclasses import dataclass
from typing import Optional

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from injector import inject

from internal.exception import UnauthorizedException
from internal.model import Account
from internal.service import JwtService, AccountService, ApiKeyService

security = HTTPBearer()


@inject
@dataclass
class Middleware:
    """应用中间件，提供认证依赖注入"""
    jwt_service: JwtService
    api_key_service: ApiKeyService
    account_service: AccountService

    async def get_current_user(
        self, 
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Account:
        """获取当前登录用户（用于llmops路由）"""
        # 1.提取token
        access_token = credentials.credentials
        
        # 2.解析token信息得到用户信息并返回
        try:
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            account = self.account_service.get_account(account_id)
            if not account:
                raise UnauthorizedException("用户不存在")
            return account
        except Exception as e:
            raise HTTPException(status_code=401, detail="该接口需要授权才能访问，请登录后尝试")

    async def get_api_key_user(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Account:
        """获取API Key用户（用于openapi路由）"""
        # 1.提取api_key
        api_key = credentials.credentials
        
        # 2.解析得到API秘钥记录
        try:
            api_key_record = self.api_key_service.get_api_by_by_credential(api_key)
            
            # 3.判断Api秘钥记录是否存在，如果不存在则抛出错误
            if not api_key_record or not api_key_record.is_active:
                raise UnauthorizedException("该秘钥不存在或未激活")
            
            # 4.获取秘钥账号信息并返回
            return api_key_record.account
        except Exception as e:
            raise HTTPException(status_code=401, detail="该秘钥不存在或未激活")

    async def optional_auth(
        self,
        request: Request,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Optional[Account]:
        """可选认证（某些接口可能不需要强制登录）"""
        if not credentials:
            return None
        
        try:
            return await self.get_current_user(request, credentials)
        except:
            return None

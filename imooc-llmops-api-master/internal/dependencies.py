#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 15:01
@Author  : thezehui@gmail.com
@File    : dependencies.py
FastAPI依赖注入辅助函数
"""
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from internal.model import Account

security = HTTPBearer()


def get_jwt_service():
    """获取JWT服务 - 延迟导入避免循环依赖"""
    from app.http.module import injector
    from internal.service import JwtService
    return injector.get(JwtService)


def get_account_service():
    """获取账号服务 - 延迟导入避免循环依赖"""
    from app.http.module import injector
    from internal.service import AccountService
    return injector.get(AccountService)


def get_api_key_service():
    """获取API Key服务 - 延迟导入避免循环依赖"""
    from app.http.module import injector
    from internal.service import ApiKeyService
    return injector.get(ApiKeyService)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Account:
    """获取当前登录用户（用于需要认证的路由）"""
    try:
        # 延迟导入服务
        jwt_service = get_jwt_service()
        account_service = get_account_service()
        
        # 1.提取token
        access_token = credentials.credentials
        
        # 2.解析token信息得到用户信息
        payload = jwt_service.parse_token(access_token)
        account_id = payload.get("sub")
        
        # 3.获取账号信息
        account = account_service.get_account(account_id)
        if not account:
            raise HTTPException(status_code=401, detail="用户不存在")
        
        return account
    except Exception as e:
        raise HTTPException(status_code=401, detail="该接口需要授权才能访问，请登录后尝试")


async def get_api_key_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Account:
    """获取API Key用户（用于openapi路由）"""
    try:
        # 延迟导入服务
        api_key_service = get_api_key_service()
        
        # 1.提取api_key
        api_key = credentials.credentials
        
        # 2.解析得到API秘钥记录
        api_key_record = api_key_service.get_api_by_by_credential(api_key)
        
        # 3.判断Api秘钥记录是否存在
        if not api_key_record or not api_key_record.is_active:
            raise HTTPException(status_code=401, detail="该秘钥不存在或未激活")
        
        # 4.获取秘钥账号信息并返回
        return api_key_record.account
    except Exception as e:
        raise HTTPException(status_code=401, detail="该秘钥不存在或未激活")


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Account]:
    """可选认证（某些接口可能不需要强制登录）"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except:
        return None

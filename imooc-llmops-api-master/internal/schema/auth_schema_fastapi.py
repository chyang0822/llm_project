#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI 版本的认证 Schema
"""
from pydantic import BaseModel, Field, field_validator
import re

from pkg.password import password_pattern


class PasswordLoginReqFastAPI(BaseModel):
    """账号密码登录请求结构 - FastAPI 版本"""
    email: str = Field(..., description="登录邮箱", min_length=5, max_length=254)
    password: str = Field(..., description="账号密码", min_length=8, max_length=16)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """验证邮箱格式"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError("登录邮箱格式错误")
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """验证密码格式"""
        if not re.match(password_pattern, v):
            raise ValueError("密码最少包含一个字母，一个数字，并且长度为8-16")
        return v


class PasswordLoginResp(BaseModel):
    """账号密码授权认证响应结构"""
    access_token: str
    expire_at: int

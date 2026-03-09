#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CORS 配置管理
"""
import os
from typing import List


class CORSConfig:
    """CORS 配置类"""
    
    @staticmethod
    def get_allowed_origins() -> List[str]:
        """根据环境获取允许的源"""
        environment = os.getenv("ENVIRONMENT", "development")
        
        if environment == "production":
            # 生产环境：从环境变量读取或使用默认值
            origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
            return [origin.strip() for origin in origins if origin.strip()]
        
        elif environment == "staging":
            # 预发布环境
            return [
                "https://staging.your-domain.com",
                "https://test.your-domain.com",
            ]
        
        else:
            # 开发环境：允许本地开发
            return [
                "http://localhost:5173",  # Vite 默认端口
                "http://localhost:3000",  # 常用开发端口
                "http://127.0.0.1:5173",
                "http://127.0.0.1:3000",
                "http://localhost:8080",
                "http://127.0.0.1:8080",
            ]
    
    @staticmethod
    def get_allowed_methods() -> List[str]:
        """获取允许的HTTP方法"""
        return ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    
    @staticmethod
    def get_allowed_headers() -> List[str]:
        """获取允许的请求头"""
        return [
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "User-Agent",
            "DNT",
            "Cache-Control",
            "X-Requested-With",
        ]
    
    @staticmethod
    def get_expose_headers() -> List[str]:
        """获取暴露的响应头"""
        return [
            "Content-Length",
            "Content-Range",
            "X-Total-Count",
        ]
    
    @staticmethod
    def get_max_age() -> int:
        """获取预检请求缓存时间（秒）"""
        return 600  # 10分钟
    
    @staticmethod
    def allow_credentials() -> bool:
        """是否允许携带凭证"""
        return True

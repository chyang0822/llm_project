#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 AuthHandler - FastAPI 版本
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
import dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient

dotenv.load_dotenv()

from config import Config
from internal.handler.auth_handler import AuthHandler
from internal.service import AccountService
from app.http.module import injector


class TestAuthHandler:
    """AuthHandler 单元测试类"""
    
    @pytest.fixture(scope="class")
    def app(self):
        """创建测试应用"""
        conf = Config()
        app = FastAPI(title="LLMOps API Test")
        
        account_service = injector.get(AccountService)
        auth_handler = AuthHandler(account_service=account_service)
        
        app.post("/auth/password-login")(auth_handler.password_login)
        app.post("/auth/logout")(auth_handler.logout)
        
        return app
    
    @pytest.fixture(scope="class")
    def client(self, app):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_password_login_invalid_email(self, client):
        """测试无效邮箱格式"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "invalid-email",
                "password": "Test1234"
            }
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["code"] == "validate_error"
        assert "email" in result["data"]
    
    def test_password_login_invalid_password_too_short(self, client):
        """测试密码太短"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "test@example.com",
                "password": "123"
            }
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["code"] == "validate_error"
        assert "password" in result["data"]
    
    def test_password_login_invalid_password_no_letter(self, client):
        """测试密码没有字母"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "test@example.com",
                "password": "12345678"
            }
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["code"] == "validate_error"
        assert "password" in result["data"]
    
    def test_password_login_invalid_password_no_number(self, client):
        """测试密码没有数字"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "test@example.com",
                "password": "abcdefgh"
            }
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["code"] == "validate_error"
        assert "password" in result["data"]
    
    def test_password_login_missing_email(self, client):
        """测试缺少邮箱字段"""
        response = client.post(
            "/auth/password-login",
            data={
                "password": "Test1234"
            }
        )
        
        assert response.status_code == 422
        result = response.json()
        assert "detail" in result
    
    def test_password_login_missing_password(self, client):
        """测试缺少密码字段"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "test@example.com"
            }
        )
        
        assert response.status_code == 422
        result = response.json()
        assert "detail" in result
    
    def test_password_login_empty_fields(self, client):
        """测试空字段"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "",
                "password": ""
            }
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["code"] == "validate_error"
    
    # 注意：以下测试需要数据库中有对应的测试账号
    @pytest.mark.skip(reason="需要数据库中有测试账号")
    def test_password_login_success(self, client):
        """测试成功登录"""
        response = client.post(
            "/auth/password-login",
            data={
                "email": "test@example.com",
                "password": "Test1234"
            }
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["code"] == 0
        assert "access_token" in result["data"]
        assert "expire_at" in result["data"]
    
    @pytest.mark.skip(reason="需要先成功登录")
    def test_logout_success(self, client):
        """测试退出登录"""
        # 先登录获取 token
        login_response = client.post(
            "/auth/password-login",
            data={
                "email": "test@example.com",
                "password": "Test1234"
            }
        )
        
        if login_response.status_code == 200 and login_response.json().get("code") == 0:
            token = login_response.json()["data"]["access_token"]
            
            # 使用 token 退出登录
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            result = response.json()
            assert result["code"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 password_login 接口 - FastAPI 版本
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import dotenv
from fastapi.testclient import TestClient

dotenv.load_dotenv()

try:
    import multipart
except ImportError:
    print("\n" + "=" * 60)
    print("❌ 错误：缺少 python-multipart 库")
    print("=" * 60)
    print("\n请运行：pip install python-multipart")
    print("\n" + "=" * 60)
    sys.exit(1)

from fastapi import FastAPI
from config import Config
from internal.handler.auth_handler_fastapi import AuthHandlerFastAPI
from internal.service import AccountService
from app.http.module import injector

conf = Config()
app = FastAPI(title="LLMOps API Test")

account_service = injector.get(AccountService)
auth_handler = AuthHandlerFastAPI(account_service=account_service)

app.post("/auth/password-login")(auth_handler.password_login)
app.post("/auth/logout")(auth_handler.logout)

client = TestClient(app)


def test_password_login_invalid_email():
    """测试无效邮箱格式"""
    print("\n=== 测试无效邮箱格式 ===")
    
    login_data = {
        "email": "invalid-email",
        "password": "Test1234"
    }
    
    print(f"请求数据: {login_data}")
    
    response = client.post(
        "/auth/password-login",
        data=login_data
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    result = response.json()
    print("✓ 无效邮箱测试通过")


def test_password_login_invalid_password():
    """测试无效密码格式"""
    print("\n=== 测试无效密码格式 ===")
    
    login_data = {
        "email": "test@example.com",
        "password": "123"
    }
    
    print(f"请求数据: {login_data}")
    
    response = client.post(
        "/auth/password-login",
        data=login_data
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    result = response.json()
    print("✓ 无效密码测试通过")


def test_password_login_missing_fields():
    """测试缺少必填字段"""
    print("\n=== 测试缺少必填字段 ===")
    
    login_data = {
        "email": "test@example.com"
    }
    
    print(f"请求数据: {login_data}")
    
    response = client.post(
        "/auth/password-login",
        data=login_data
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    assert response.status_code == 422
    print("✓ 缺少字段测试通过")


if __name__ == "__main__":
    print("=" * 60)
    print("开始测试 password_login 接口 (FastAPI 版本)")
    print("=" * 60)
    
    try:
        test_password_login_invalid_email()
        test_password_login_invalid_password()
        test_password_login_missing_fields()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

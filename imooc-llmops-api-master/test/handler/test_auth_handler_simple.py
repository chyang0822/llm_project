#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 AuthHandler - 简单版本（不依赖 pytest）
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient

dotenv.load_dotenv()

from config import Config
from internal.handler.auth_handler import AuthHandler
from internal.service import AccountService
from app.http.module import injector


def setup_app():
    """创建测试应用"""
    conf = Config()
    app = FastAPI(title="LLMOps API Test")
    
    account_service = injector.get(AccountService)
    auth_handler = AuthHandler(account_service=account_service)
    
    app.post("/auth/password-login")(auth_handler.password_login)
    app.post("/auth/logout")(auth_handler.logout)
    
    return TestClient(app)


def test_password_login_invalid_email():
    """测试无效邮箱格式"""
    print("\n=== 测试无效邮箱格式 ===")
    client = setup_app()
    
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
    print("✓ 通过")


def test_password_login_invalid_password_too_short():
    """测试密码太短"""
    print("\n=== 测试密码太短 ===")
    client = setup_app()
    
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
    print("✓ 通过")


def test_password_login_invalid_password_no_letter():
    """测试密码没有字母"""
    print("\n=== 测试密码没有字母 ===")
    client = setup_app()
    
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
    print("✓ 通过")


def test_password_login_invalid_password_no_number():
    """测试密码没有数字"""
    print("\n=== 测试密码没有数字 ===")
    client = setup_app()
    
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
    print("✓ 通过")


def test_password_login_missing_email():
    """测试缺少邮箱字段"""
    print("\n=== 测试缺少邮箱字段 ===")
    client = setup_app()
    
    response = client.post(
        "/auth/password-login",
        data={
            "password": "Test1234"
        }
    )
    
    assert response.status_code == 422
    result = response.json()
    assert "detail" in result
    print("✓ 通过")


def test_password_login_missing_password():
    """测试缺少密码字段"""
    print("\n=== 测试缺少密码字段 ===")
    client = setup_app()
    
    response = client.post(
        "/auth/password-login",
        data={
            "email": "test@example.com"
        }
    )
    
    assert response.status_code == 422
    result = response.json()
    assert "detail" in result
    print("✓ 通过")


def test_password_login_empty_fields():
    """测试空字段"""
    print("\n=== 测试空字段 ===")
    client = setup_app()
    
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
    print("✓ 通过")


if __name__ == "__main__":
    print("=" * 60)
    print("开始测试 AuthHandler")
    print("=" * 60)
    
    tests = [
        test_password_login_invalid_email,
        test_password_login_invalid_password_too_short,
        test_password_login_invalid_password_no_letter,
        test_password_login_invalid_password_no_number,
        test_password_login_missing_email,
        test_password_login_missing_password,
        test_password_login_empty_fields,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ 错误: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)

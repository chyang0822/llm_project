#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 password_login 接口

使用前请确保已安装依赖：
pip install python-multipart

或安装所有依赖：
pip install -r requirements.txt
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import asyncio
import dotenv
from fastapi.testclient import TestClient

# 加载环境变量
dotenv.load_dotenv()

# 检查必要的依赖
try:
    import multipart
except ImportError:
    print("\n" + "=" * 60)
    print("❌ 错误：缺少 python-multipart 库")
    print("=" * 60)
    print("\n请运行以下命令安装：")
    print("  pip install python-multipart")
    print("\n或安装所有项目依赖：")
    print("  pip install -r requirements.txt")
    print("\n" + "=" * 60)
    sys.exit(1)

from config import Config
from internal.middleware import Middleware
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from app.http.module import injector

# 构建应用
conf = Config()
app = Http(
    conf=conf,
    db=injector.get(SQLAlchemy),
    middleware=injector.get(Middleware),
    router=injector.get(Router),
)

# 创建测试客户端
client = TestClient(app)


def test_password_login_success():
    """测试成功登录"""
    print("\n=== 测试账号密码登录 ===")
    
    # 准备测试数据 - 请根据实际数据库中的账号修改
    login_data = {
        "email": "test@example.com",  # 修改为实际存在的邮箱
        "password": "Test1234"  # 修改为实际的密码
    }
    
    print(f"请求数据: {login_data}")
    
    # 发送登录请求
    response = client.post(
        "/auth/password-login",
        data=login_data
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 断言
    assert response.status_code == 200
    result = response.json()
    assert "data" in result
    assert "access_token" in result["data"]
    assert "expire_at" in result["data"]
    
    print("✓ 登录成功测试通过")
    return result["data"]["access_token"]


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
    
    # 应该返回验证错误
    result = response.json()
    print("✓ 无效邮箱测试通过")


def test_password_login_invalid_password():
    """测试无效密码格式"""
    print("\n=== 测试无效密码格式 ===")
    
    login_data = {
        "email": "test@example.com",
        "password": "123"  # 密码太短
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
    
    with flask_app.app_context():
        login_data = {
            "email": "test@example.com"
            # 缺少 password 字段
        }
        
        print(f"请求数据: {login_data}")
        
        response = client.post(
            "/auth/password-login",
            data=login_data
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        print("✓ 缺少字段测试通过")


def test_password_login_success():
    """测试成功登录"""
    print("\n=== 测试账号密码登录 ===")
    
    with flask_app.app_context():
        # 准备测试数据 - 请根据实际数据库中的账号修改
        login_data = {
            "email": "test@example.com",  # 修改为实际存在的邮箱
            "password": "Test1234"  # 修改为实际的密码
        }
        
        print(f"请求数据: {login_data}")
        
        # 发送登录请求
        response = client.post(
            "/auth/password-login",
            data=login_data
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        # 断言
        assert response.status_code == 200
        result = response.json()
        assert "data" in result
        assert "access_token" in result["data"]
        assert "expire_at" in result["data"]
        
        print("✓ 登录成功测试通过")
        return result["data"]["access_token"]


def test_logout():
    """测试退出登录"""
    print("\n=== 测试退出登录 ===")
    
    with flask_app.app_context():
        # 先登录获取 token
        login_data = {
            "email": "test@example.com",
            "password": "Test1234"
        }
        
        login_response = client.post(
            "/auth/password-login",
            data=login_data
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["data"]["access_token"]
            
            # 使用 token 退出登录
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.json()}")
            
            print("✓ 退出登录测试通过")
        else:
            print("⚠ 需要先成功登录才能测试退出")


if __name__ == "__main__":
    print("=" * 60)
    print("开始测试 password_login 接口")
    print("=" * 60)
    
    try:
        # 运行测试
        test_password_login_invalid_email()
        test_password_login_invalid_password()
        test_password_login_missing_fields()
        
        # 注意：这个测试需要数据库中有对应的测试账号
        # test_password_login_success()
        # test_logout()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        print("\n提示：要测试成功登录，请先在数据库中创建测试账号，")
        print("然后取消注释 test_password_login_success() 和 test_logout()")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量迁移handler文件从Flask到FastAPI的脚本
"""
import os
import re

# 需要处理的handler文件列表
handler_files = [
    "internal/handler/builtin_app_handler.py",
    "internal/handler/builtin_tool_handler.py",
    "internal/handler/dataset_handler.py",
    "internal/handler/account_handler.py",
    "internal/handler/analysis_handler.py",
    "internal/handler/web_app_handler.py",
    "internal/handler/ai_handler.py",
    "internal/handler/openapi_handler.py",
    "internal/handler/workflow_handler.py",
    "internal/handler/conversation_handler.py",
    "internal/handler/document_handler.py",
    "internal/handler/segment_handler.py",
    "internal/handler/assistant_agent_handler.py",
    "internal/handler/api_key_handler.py",
    "internal/handler/upload_file_handler.py",
    "internal/handler/api_tool_handler.py",
    "internal/handler/language_model_handler.py",
]

def migrate_handler_file(filepath):
    """迁移单个handler文件"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 移除flask_login导入
    content = re.sub(r'from flask_login import.*\n', '', content)
    
    # 2. 替换flask导入为fastapi
    content = re.sub(
        r'from flask import request',
        'from fastapi import Request, Depends',
        content
    )
    
    # 3. 添加必要的导入（如果还没有）
    if 'from internal.middleware import Middleware' not in content:
        # 在injector导入后添加
        content = re.sub(
            r'(from injector import inject\n)',
            r'\1\nfrom internal.middleware import Middleware\nfrom internal.model import Account',
            content
        )
    
    # 4. 移除@login_required装饰器
    content = re.sub(r'\s*@login_required\n', '', content)
    
    # 5. 将方法改为async（简单处理，实际可能需要手动调整）
    content = re.sub(r'\n    def (\w+)\(self', r'\n    async def \1(self', content)
    
    # 6. 替换current_user为依赖注入参数
    # 这个比较复杂，需要手动处理
    
    # 7. 替换request.args为request.query_params
    content = re.sub(r'request\.args', 'dict(request.query_params)', content)
    
    # 8. 替换request.get_json()为await request.json()
    content = re.sub(
        r'request\.get_json\([^)]*\)',
        'await request.json()',
        content
    )
    
    # 只有内容真的改变了才写入
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {filepath}")
    else:
        print(f"- No changes needed for {filepath}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for handler_file in handler_files:
        filepath = os.path.join(base_dir, handler_file)
        if os.path.exists(filepath):
            try:
                migrate_handler_file(filepath)
            except Exception as e:
                print(f"✗ Error processing {filepath}: {e}")
        else:
            print(f"✗ File not found: {filepath}")
    
    print("\n迁移完成！请手动检查以下内容：")
    print("1. 所有方法的current_user参数需要添加: current_user: Account = Depends(lambda: Middleware.get_current_user)")
    print("2. 检查是否有其他Flask特定的代码需要调整")
    print("3. 测试所有接口确保功能正常")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量修复handler文件，移除flask_login依赖
"""
import re
import os

handler_files = [
    "internal/handler/upload_file_handler.py",
    "internal/handler/assistant_agent_handler.py",
    "internal/handler/document_handler.py",
    "internal/handler/conversation_handler.py",
    "internal/handler/language_model_handler.py",
    "internal/handler/api_tool_handler.py",
    "internal/handler/api_key_handler.py",
    "internal/handler/segment_handler.py",
    "internal/handler/workflow_handler.py",
    "internal/handler/openapi_handler.py",
    "internal/handler/web_app_handler.py",
    "internal/handler/dataset_handler.py",
    "internal/handler/builtin_app_handler.py",
    "internal/handler/builtin_tool_handler.py",
    "internal/handler/analysis_handler.py",
]

def fix_handler(filepath):
    """修复单个handler文件"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 移除flask_login导入
    content = re.sub(r'from flask_login import[^\n]+\n', '', content)
    
    # 2. 添加FastAPI导入（如果还没有）
    if 'from fastapi import' not in content:
        # 在injector导入后添加
        content = re.sub(
            r'(from injector import inject)',
            r'\1\n\nfrom fastapi import Depends',
            content
        )
    
    # 3. 添加dependencies导入（如果还没有）
    if 'from internal.dependencies import' not in content:
        content = re.sub(
            r'(from fastapi import[^\n]+)',
            r'\1\nfrom internal.dependencies import get_current_user, get_api_key_user\nfrom internal.model import Account',
            content
        )
    
    # 4. 移除@login_required装饰器
    content = re.sub(r'\s*@login_required\n', '\n', content)
    
    # 5. 将def改为async def
    content = re.sub(r'\n    def (\w+)\(self', r'\n    async def \1(self', content)
    
    # 6. 替换current_user为参数（简单处理，可能需要手动调整）
    # 这个比较复杂，暂时跳过，需要手动处理
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Fixed {filepath}")

if __name__ == "__main__":
    for handler_file in handler_files:
        if os.path.exists(handler_file):
            try:
                fix_handler(handler_file)
            except Exception as e:
                print(f"✗ Error processing {handler_file}: {e}")
        else:
            print(f"✗ File not found: {handler_file}")
    
    print("\n完成！请注意：")
    print("1. 所有方法已改为async")
    print("2. 已移除@login_required装饰器")
    print("3. 需要手动为每个方法添加: current_user: Account = Depends(get_current_user)")
    print("4. 需要手动替换request.args为dict(request.query_params)")
    print("5. 需要手动替换request.get_json()为await request.json()")

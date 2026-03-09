# FastAPI 接口迁移指南

## 当前状态

### ✅ 已完成迁移
- **auth_handler.py** - 认证处理器（已完全迁移到 FastAPI）
- **auth_schema.py** - 认证 Schema（已完全迁移到 Pydantic）

### ⚠️ 需要迁移的 Handler

以下 handler 文件仍在使用 Flask-WTF 或混合使用 Flask/FastAPI：

1. **account_handler.py** - 账号设置处理器
   - 使用 `Request.form()` + Flask-WTF
   - 需要迁移 3 个方法

2. **app_handler.py** - 应用处理器
   - 使用 `Request.form()` + Flask-WTF
   - 需要迁移多个方法

3. **dataset_handler.py** - 知识库处理器
   - 使用 `from flask import request`
   - 需要迁移多个方法

4. **document_handler.py** - 文档处理器
5. **segment_handler.py** - 分段处理器
6. **api_tool_handler.py** - API 工具处理器
7. **workflow_handler.py** - 工作流处理器
8. **ai_handler.py** - AI 辅助处理器
9. **api_key_handler.py** - API 密钥处理器
10. **conversation_handler.py** - 会话处理器
11. **assistant_agent_handler.py** - 辅助 Agent 处理器
12. **web_app_handler.py** - WebApp 处理器
13. **builtin_tool_handler.py** - 内置工具处理器
14. **language_model_handler.py** - 语言模型处理器

## 迁移步骤

### 1. Handler 迁移模式

#### 原代码（Flask-WTF）：
```python
from fastapi import Request
from internal.schema.xxx_schema import XxxReq

async def some_method(self, request: Request):
    # 从 request 中获取表单数据
    form_data = await request.form()
    req = XxxReq(formdata=form_data)
    if not req.validate():
        return validate_error_json(req.errors)
    
    # 使用 req.field.data 访问数据
    result = self.service.do_something(req.field.data)
    return success_json(result)
```

#### 新代码（FastAPI + Pydantic）：
```python
from fastapi import Form
from pydantic import ValidationError
from internal.schema.xxx_schema import XxxReqFastAPI

async def some_method(
    self,
    field1: str = Form(...),
    field2: int = Form(...)
):
    try:
        # 使用 Pydantic 验证
        req = XxxReqFastAPI(field1=field1, field2=field2)
        
        # 直接使用 req.field 访问数据
        result = self.service.do_something(req.field1)
        return success_json(result)
        
    except ValidationError as e:
        errors = {}
        for error in e.errors():
            field = error['loc'][0]
            errors[field] = [error['msg']]
        return validate_error_json(errors)
```

### 2. Schema 迁移模式

#### 原代码（Flask-WTF + Marshmallow）：
```python
from flask_wtf import FlaskForm
from marshmallow import Schema, fields
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class XxxReq(FlaskForm):
    field1 = StringField("field1", validators=[
        DataRequired("字段不能为空"),
        Length(min=1, max=100)
    ])

class XxxResp(Schema):
    field1 = fields.String()
    field2 = fields.Integer()
```

#### 新代码（Pydantic）：
```python
from pydantic import BaseModel, Field, field_validator

class XxxReqFastAPI(BaseModel):
    field1: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('field1')
    @classmethod
    def validate_field1(cls, v):
        if not v:
            raise ValueError("字段不能为空")
        return v

class XxxResp(BaseModel):
    field1: str
    field2: int
```

### 3. 特殊情况处理

#### JSON 请求体
```python
# 原代码
async def method(self, request: Request):
    data = await request.json()

# 新代码
from pydantic import BaseModel

class RequestModel(BaseModel):
    field1: str
    field2: int

async def method(self, data: RequestModel):
    # 直接使用 data.field1, data.field2
```

#### Query 参数
```python
# 原代码
async def method(self, request: Request):
    req = XxxReq(request.query_params)

# 新代码
from fastapi import Query

async def method(
    self,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    # 直接使用 page, limit
```

#### 文件上传
```python
# 原代码
async def method(self, request: Request):
    form_data = await request.form()
    file = form_data.get("file")

# 新代码
from fastapi import File, UploadFile

async def method(self, file: UploadFile = File(...)):
    # 直接使用 file
```

## 迁移优先级

### 高优先级（核心功能）
1. ✅ auth_handler.py - 已完成
2. account_handler.py - 账号管理
3. app_handler.py - 应用管理

### 中优先级（常用功能）
4. dataset_handler.py - 知识库
5. document_handler.py - 文档
6. conversation_handler.py - 会话
7. api_key_handler.py - API 密钥

### 低优先级（辅助功能）
8. workflow_handler.py - 工作流
9. ai_handler.py - AI 辅助
10. 其他 handler

## 测试策略

### 单元测试结构
```python
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

class TestXxxHandler:
    @pytest.fixture(scope="class")
    def app(self):
        # 创建测试应用
        app = FastAPI()
        handler = XxxHandler(...)
        app.post("/xxx")(handler.method)
        return app
    
    @pytest.fixture(scope="class")
    def client(self, app):
        return TestClient(app)
    
    def test_method_success(self, client):
        response = client.post("/xxx", data={...})
        assert response.status_code == 200
    
    def test_method_validation_error(self, client):
        response = client.post("/xxx", data={...})
        assert response.status_code == 200
        assert response.json()["code"] == "validate_error"
```

### 运行测试
```bash
# 运行所有测试
pytest test/handler/

# 运行特定测试
pytest test/handler/test_auth_handler.py -v

# 运行特定测试方法
pytest test/handler/test_auth_handler.py::TestAuthHandler::test_password_login_invalid_email -v
```

## 迁移检查清单

对于每个 handler，确保：

- [ ] 移除 `from flask import request`
- [ ] 移除 `from flask_wtf import FlaskForm`
- [ ] 将 `Request.form()` 改为 `Form` 参数
- [ ] 将 `Request.json()` 改为 Pydantic 模型
- [ ] 将 `Request.query_params` 改为 `Query` 参数
- [ ] 更新对应的 Schema 文件
- [ ] 创建单元测试
- [ ] 运行测试确保通过
- [ ] 更新文档

## 常见问题

### Q: 如何处理复杂的表单验证？
A: 使用 Pydantic 的 `@field_validator` 或 `@model_validator`

### Q: 如何处理文件上传？
A: 使用 FastAPI 的 `File` 和 `UploadFile`

### Q: 如何处理可选字段？
A: 使用 `Optional[Type] = None` 或 `Type | None = None`

### Q: 如何保持向后兼容？
A: 可以暂时保留旧的 handler，创建新的 FastAPI 版本，逐步迁移

## 下一步

1. 按优先级迁移 handler
2. 为每个迁移的 handler 创建单元测试
3. 更新 API 文档
4. 删除不再使用的 Flask 依赖

## 参考资料

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
- [已完成的迁移示例](./internal/handler/auth_handler.py)

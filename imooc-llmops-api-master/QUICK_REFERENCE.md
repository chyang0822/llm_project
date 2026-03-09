# FastAPI 迁移快速参考

## 🎯 当前状态

### ✅ 已完成
- **auth_handler.py** - 认证处理器
- **auth_schema.py** - 认证 Schema
- **单元测试** - 7/7 通过
- **调试配置** - 完整配置

### ⚠️ 待迁移（14个 Handler）
account_handler, app_handler, dataset_handler, document_handler, segment_handler, api_tool_handler, workflow_handler, ai_handler, api_key_handler, conversation_handler, assistant_agent_handler, web_app_handler, builtin_tool_handler, language_model_handler

## 🚀 快速开始

### 运行测试
```bash
# 单元测试
python test/handler/test_auth_handler_simple.py

# 快速测试
python test_password_login_fastapi.py
```

### VSCode 调试
```
按 F5 -> 选择配置：
- 测试 AuthHandler 单元测试
- 调试 AuthHandler 单元测试
- 测试 password_login_fastapi 接口
```

## 📝 迁移模板

### Handler 迁移
```python
# 之前
async def method(self, request: Request):
    form_data = await request.form()
    req = XxxReq(formdata=form_data)
    if not req.validate():
        return validate_error_json(req.errors)

# 之后
async def method(
    self,
    field1: str = Form(...),
    field2: int = Form(...)
):
    try:
        req = XxxReqFastAPI(field1=field1, field2=field2)
    except ValidationError as e:
        errors = {error['loc'][0]: [error['msg']] for error in e.errors()}
        return validate_error_json(errors)
```

### Schema 迁移
```python
# 之前
from flask_wtf import FlaskForm
from wtforms import StringField

class XxxReq(FlaskForm):
    field = StringField("field", validators=[...])

# 之后
from pydantic import BaseModel, Field, field_validator

class XxxReqFastAPI(BaseModel):
    field: str = Field(...)
    
    @field_validator('field')
    @classmethod
    def validate_field(cls, v):
        # 验证逻辑
        return v
```

### 单元测试模板
```python
def test_method_name():
    """测试描述"""
    client = setup_app()
    response = client.post("/endpoint", data={...})
    assert response.status_code == 200
    assert response.json()["code"] == expected_code
```

## 📚 文档

- **FASTAPI_MIGRATION_SUMMARY.md** - 完整总结
- **FASTAPI_MIGRATION_GUIDE.md** - 详细指南
- **MIGRATION_COMPLETE.md** - 迁移说明

## 🔧 调试配置

### launch.json 配置
1. 启动后端
2. 调试后端
3. 启动前端
4. 测试 password_login_fastapi 接口
5. 调试 password_login 接口
6. 测试 AuthHandler 单元测试 ⭐
7. 调试 AuthHandler 单元测试 ⭐
8. 启动前后端

## ✅ 测试清单

- [x] 无效邮箱格式
- [x] 密码太短
- [x] 密码没有字母
- [x] 密码没有数字
- [x] 缺少邮箱字段
- [x] 缺少密码字段
- [x] 空字段验证

## 🎓 最佳实践

1. **先迁移 Schema，再迁移 Handler**
2. **每个方法迁移后立即创建测试**
3. **使用 field_validator 进行复杂验证**
4. **保持接口行为一致**
5. **添加完整的类型提示**

## 🐛 常见问题

### Q: 如何处理文件上传？
```python
from fastapi import File, UploadFile

async def method(self, file: UploadFile = File(...)):
    content = await file.read()
```

### Q: 如何处理 JSON 请求？
```python
class RequestModel(BaseModel):
    field1: str
    field2: int

async def method(self, data: RequestModel):
    # 直接使用 data.field1
```

### Q: 如何处理 Query 参数？
```python
from fastapi import Query

async def method(
    self,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    # 直接使用 page, limit
```

## 📊 进度追踪

- ✅ 已迁移: 1/15 (6.7%)
- ⚠️ 待迁移: 14/15 (93.3%)
- 🎯 目标: 100% FastAPI

## 🔗 相关链接

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
- [已完成示例](./internal/handler/auth_handler.py)

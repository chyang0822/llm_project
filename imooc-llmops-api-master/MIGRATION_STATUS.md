# FastAPI 迁移进度

## ✅ 已完成的核心迁移

### 1. 基础架构
- ✅ `requirements.txt` - 替换Flask依赖为FastAPI
- ✅ `app/http/app.py` - 主应用入口改用FastAPI
- ✅ `app/http/module.py` - 移除Flask-Login和Flask-Migrate依赖
- ✅ `internal/server/http.py` - HTTP服务器类改用FastAPI
- ✅ `internal/router/router.py` - 路由系统改用FastAPI装饰器
- ✅ `pkg/response/response.py` - 响应模块适配FastAPI
- ✅ `.vscode/launch.json` - 调试配置适配FastAPI

### 2. 认证系统
- ✅ `internal/dependencies.py` - 创建统一的依赖注入辅助函数
- ✅ `internal/middleware/middleware.py` - 改用FastAPI依赖注入
- ✅ `internal/model/account.py` - 移除Flask-Login的UserMixin

### 3. Handler层（已完成）
- ✅ `internal/handler/auth_handler.py` - 认证处理器
- ✅ `internal/handler/account_handler.py` - 账号处理器
- ✅ `internal/handler/app_handler.py` - 应用处理器

## 🔄 待完成的Handler迁移

以下handler文件需要按照相同模式更新（移除flask_login导入，改为async方法，使用Depends(get_current_user)）：

### 需要认证的Handler
- ⏳ `internal/handler/builtin_tool_handler.py`
- ⏳ `internal/handler/api_tool_handler.py`
- ⏳ `internal/handler/upload_file_handler.py`
- ⏳ `internal/handler/dataset_handler.py`
- ⏳ `internal/handler/document_handler.py`
- ⏳ `internal/handler/segment_handler.py`
- ⏳ `internal/handler/ai_handler.py`
- ⏳ `internal/handler/api_key_handler.py`
- ⏳ `internal/handler/builtin_app_handler.py`
- ⏳ `internal/handler/workflow_handler.py`
- ⏳ `internal/handler/language_model_handler.py`
- ⏳ `internal/handler/assistant_agent_handler.py`
- ⏳ `internal/handler/analysis_handler.py`
- ⏳ `internal/handler/conversation_handler.py`

### 特殊Handler（可能不需要认证或使用API Key认证）
- ⏳ `internal/handler/oauth_handler.py` - OAuth认证
- ⏳ `internal/handler/openapi_handler.py` - 使用API Key认证
- ⏳ `internal/handler/web_app_handler.py` - 使用Token认证

## 📝 迁移模板

### 标准Handler迁移步骤

**旧的Flask代码：**
```python
from flask_login import login_required, current_user
from flask import request

@inject
@dataclass
class SomeHandler:
    some_service: SomeService
    
    @login_required
    def some_method(self, param_id: UUID):
        req = SomeReq(request.args)
        data = request.get_json()
        # ... 业务逻辑
        result = self.some_service.do_something(param_id, current_user)
        return success_json(result)
```

**新的FastAPI代码：**
```python
from fastapi import Request, Depends
from internal.dependencies import get_current_user
from internal.model import Account

@inject
@dataclass
class SomeHandler:
    some_service: SomeService
    
    async def some_method(
        self, 
        param_id: UUID,
        request: Request,
        current_user: Account = Depends(get_current_user)
    ):
        req = SomeReq(dict(request.query_params))
        data = await request.json()
        # ... 业务逻辑
        result = self.some_service.do_something(param_id, current_user)
        return success_json(result)
```

### 关键变更点

1. **导入变更**
   ```python
   # 移除
   from flask_login import login_required, current_user
   from flask import request
   
   # 添加
   from fastapi import Request, Depends
   from internal.dependencies import get_current_user
   from internal.model import Account
   ```

2. **装饰器变更**
   ```python
   # 移除
   @login_required
   
   # 改为在参数中使用Depends
   current_user: Account = Depends(get_current_user)
   ```

3. **方法签名变更**
   ```python
   # 旧
   def method_name(self, param: Type):
   
   # 新
   async def method_name(self, param: Type, current_user: Account = Depends(get_current_user)):
   ```

4. **请求数据获取**
   ```python
   # 旧
   req = SomeReq(request.args)
   data = request.get_json()
   
   # 新
   req = SomeReq(dict(request.query_params))
   data = await request.json()
   ```

## 🚀 快速启动

### 开发模式
```bash
# 方式1：使用VSCode调试
按F5，选择 "FastAPI: Run with Uvicorn"

# 方式2：命令行启动
python app/http/app.py

# 方式3：使用uvicorn
uvicorn app.http.app:app --host 0.0.0.0 --port 8000 --reload
```

### 访问API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ⚠️ 已知问题

1. **其他Handler未完成迁移** - 需要按照模板逐个更新
2. **数据库迁移** - 需要使用Alembic替代Flask-Migrate
3. **测试用例** - 需要更新为FastAPI的TestClient

## 📚 参考资源

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [FastAPI依赖注入](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [从Flask迁移到FastAPI](https://fastapi.tiangolo.com/alternatives/#flask)

## 🔧 下一步工作

1. 按照模板逐个迁移剩余的handler文件
2. 测试所有API接口确保功能正常
3. 更新测试用例
4. 更新部署配置（使用uvicorn替代gunicorn+flask）

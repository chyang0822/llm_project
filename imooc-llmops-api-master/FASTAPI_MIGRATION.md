# FastAPI 迁移说明

## 已完成的迁移

本项目已从 Flask 成功迁移到 FastAPI。主要变更包括：

### 1. 依赖更新
- 移除：Flask, Flask-CORS, Flask-Migrate, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- 添加：FastAPI, Uvicorn, python-jose (用于JWT)

### 2. 核心文件变更

#### app/http/app.py
- 使用 FastAPI 替代 Flask
- 使用 uvicorn 作为 ASGI 服务器
- 移除 Flask-Login 和 Flask-Migrate 依赖

#### internal/server/http.py
- Http 类继承自 FastAPI 而非 Flask
- 使用 FastAPI 的 CORSMiddleware
- 使用 FastAPI 的异常处理机制
- 移除 Flask 特定的配置方式

#### internal/middleware/middleware.py
- 使用 FastAPI 的依赖注入系统 (Depends)
- 使用 HTTPBearer 进行认证
- 提供 `get_current_user` 和 `get_api_key_user` 作为依赖函数
- 移除 Flask-Login 的 request_loader

#### internal/router/router.py
- 使用 FastAPI 的路由装饰器 (@app.get, @app.post)
- 使用 Depends 进行认证依赖注入
- 移除 Flask Blueprint

#### internal/handler/*.py
- 所有 handler 方法改为 async 函数
- 移除 @login_required 装饰器，改用 Depends(get_current_user)
- 使用 FastAPI 的 Request 对象
- 参数通过函数签名直接注入

#### pkg/response/response.py
- 使用 JSONResponse 替代 Flask 的 jsonify
- 使用 StreamingResponse 替代 Flask 的 stream_with_context

### 3. 认证机制变更

**Flask 方式：**
```python
@login_required
def some_handler(self):
    user = current_user
```

**FastAPI 方式：**
```python
async def some_handler(self, current_user: Account = Depends(get_current_user)):
    # user 通过依赖注入获得
```

### 4. 请求数据获取变更

**Flask 方式：**
```python
req = SomeReq(request.args)  # GET 参数
data = request.get_json()     # POST JSON
```

**FastAPI 方式：**
```python
req = SomeReq(dict(request.query_params))  # GET 参数
data = await request.json()                 # POST JSON
```

### 5. 启动方式变更

**Flask 方式：**
```bash
python app/http/app.py
# 或
flask run
```

**FastAPI 方式：**
```bash
python app/http/app.py
# 或
uvicorn app.http.app:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 数据库迁移

由于移除了 Flask-Migrate，需要直接使用 Alembic：

```bash
# 生成迁移
alembic revision --autogenerate -m "migration message"

# 执行迁移
alembic upgrade head
```

### 7. 其他注意事项

1. **所有 handler 方法现在都是 async**：如果调用同步的服务方法，FastAPI 会自动在线程池中运行
2. **Session 管理**：需要确保 SQLAlchemy session 在异步环境中正确管理
3. **Celery 集成**：保持不变，但需要确保任务调用方式兼容
4. **测试**：需要使用 FastAPI 的 TestClient 替代 Flask 的 test_client

### 8. 待完成的工作

由于项目较大，以下 handler 文件需要按照相同模式更新（将 @login_required 改为 Depends，方法改为 async）：

- builtin_tool_handler.py
- api_tool_handler.py
- upload_file_handler.py
- dataset_handler.py
- document_handler.py
- segment_handler.py
- oauth_handler.py
- account_handler.py
- ai_handler.py
- api_key_handler.py
- openapi_handler.py
- builtin_app_handler.py
- workflow_handler.py
- language_model_handler.py
- assistant_agent_handler.py
- analysis_handler.py
- web_app_handler.py
- conversation_handler.py

### 9. 迁移模板

其他 handler 可以参考以下模板进行迁移：

```python
# 旧的 Flask 方式
@login_required
def some_method(self, param_id: UUID):
    req = SomeReq(request.args)
    # ...
    return success_json(data)

# 新的 FastAPI 方式
async def some_method(
    self, 
    param_id: UUID,
    request: Request,
    current_user: Account = Depends(lambda: Middleware.get_current_user)
):
    req = SomeReq(dict(request.query_params))
    # ...
    return success_json(data)
```

## 优势

1. **性能提升**：FastAPI 基于 ASGI，性能优于 Flask 的 WSGI
2. **自动文档**：访问 `/docs` 可查看自动生成的 Swagger UI 文档
3. **类型检查**：更好的类型提示和验证
4. **异步支持**：原生支持 async/await
5. **现代化**：更符合现代 Python Web 开发标准

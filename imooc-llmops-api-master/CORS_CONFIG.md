# CORS 跨域配置说明

## 📍 当前配置位置

### 后端（FastAPI）
- **文件**: `internal/server/http.py`
- **行数**: 58-64
- **配置**:
```python
self.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ⚠️ 允许所有源（开发环境可以，生产环境不安全）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 前端（Vue）
- **API 前缀**: `src/config/index.ts`
  ```typescript
  export const apiPrefix: string = 'http://localhost:8000'
  ```

- **请求配置**: `src/utils/request.ts`
  ```typescript
  const baseFetchOptions = {
    mode: 'cors',
    credentials: 'include',
  }
  ```

## ⚠️ 安全问题

### 当前配置的问题
```python
allow_origins=["*"]  # 允许任何域名访问
```

**风险**:
1. 任何网站都可以调用你的 API
2. 可能导致 CSRF 攻击
3. 数据泄露风险
4. 不符合生产环境安全标准

## ✅ 推荐配置

### 方案 1: 使用新的 CORS 配置类（推荐）

#### 1. 使用配置类

修改 `internal/server/http.py`:

```python
from internal.config.cors_config import CORSConfig

# 在 Http 类的 __init__ 方法中
self.add_middleware(
    CORSMiddleware,
    allow_origins=CORSConfig.get_allowed_origins(),
    allow_credentials=CORSConfig.allow_credentials(),
    allow_methods=CORSConfig.get_allowed_methods(),
    allow_headers=CORSConfig.get_allowed_headers(),
    expose_headers=CORSConfig.get_expose_headers(),
    max_age=CORSConfig.get_max_age(),
)
```

#### 2. 配置环境变量

在 `.env` 文件中添加：

```bash
# 开发环境
ENVIRONMENT=development

# 生产环境
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# 预发布环境
ENVIRONMENT=staging
```

### 方案 2: 直接修改（简单快速）

修改 `internal/server/http.py`:

```python
import os

# 根据环境配置
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins = [
        "https://your-production-domain.com",
        "https://www.your-production-domain.com",
    ]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

self.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

## 🔧 配置说明

### allow_origins
- **作用**: 允许哪些域名访问
- **开发环境**: `["http://localhost:5173", "http://localhost:3000"]`
- **生产环境**: `["https://your-domain.com"]`
- **不推荐**: `["*"]` （允许所有域名）

### allow_credentials
- **作用**: 是否允许携带凭证（cookies、Authorization header）
- **值**: `True` 或 `False`
- **注意**: 当设置为 `True` 时，`allow_origins` 不能为 `["*"]`

### allow_methods
- **作用**: 允许的 HTTP 方法
- **推荐**: `["GET", "POST", "PUT", "DELETE", "OPTIONS"]`
- **不推荐**: `["*"]` （虽然方便，但不够明确）

### allow_headers
- **作用**: 允许的请求头
- **推荐**: 明确列出需要的头
  ```python
  ["Content-Type", "Authorization", "Accept", "Origin"]
  ```
- **可以用**: `["*"]` （相对安全）

### expose_headers
- **作用**: 允许前端访问的响应头
- **示例**: `["Content-Length", "X-Total-Count"]`

### max_age
- **作用**: 预检请求（OPTIONS）的缓存时间（秒）
- **推荐**: `600` (10分钟)

## 🚀 实施步骤

### 步骤 1: 备份当前配置
```bash
cp internal/server/http.py internal/server/http.py.backup
```

### 步骤 2: 选择方案并修改

#### 使用方案 1（推荐）:
```python
# 在 internal/server/http.py 中
from internal.config.cors_config import CORSConfig

self.add_middleware(
    CORSMiddleware,
    allow_origins=CORSConfig.get_allowed_origins(),
    allow_credentials=CORSConfig.allow_credentials(),
    allow_methods=CORSConfig.get_allowed_methods(),
    allow_headers=CORSConfig.get_allowed_headers(),
    expose_headers=CORSConfig.get_expose_headers(),
    max_age=CORSConfig.get_max_age(),
)
```

#### 使用方案 2（简单）:
直接在 `http.py` 中修改 `allow_origins`

### 步骤 3: 配置环境变量

在 `.env` 文件中:
```bash
ENVIRONMENT=development
```

### 步骤 4: 测试

```bash
# 启动后端
python app/http/app.py

# 启动前端
cd imooc-llmops-ui-master
npm run dev

# 测试跨域请求是否正常
```

## 🧪 测试跨域配置

### 测试脚本

创建 `test_cors.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>CORS Test</title>
</head>
<body>
    <h1>CORS 测试</h1>
    <button onclick="testCORS()">测试跨域请求</button>
    <div id="result"></div>

    <script>
        async function testCORS() {
            try {
                const response = await fetch('http://localhost:8000/ping', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                });
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    '<p style="color: green;">✓ 跨域请求成功！</p>' +
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    '<p style="color: red;">✗ 跨域请求失败：' + error.message + '</p>';
            }
        }
    </script>
</body>
</html>
```

## 📊 不同环境的配置对比

| 环境 | allow_origins | 说明 |
|------|--------------|------|
| 开发环境 | `["http://localhost:*"]` | 允许本地开发 |
| 测试环境 | `["https://test.domain.com"]` | 只允许测试域名 |
| 预发布环境 | `["https://staging.domain.com"]` | 只允许预发布域名 |
| 生产环境 | `["https://domain.com"]` | 只允许生产域名 |

## 🐛 常见问题

### Q1: 前端报错 "CORS policy: No 'Access-Control-Allow-Origin' header"
**原因**: 后端没有正确配置 CORS
**解决**: 检查后端 CORS 配置，确保包含前端域名

### Q2: 前端报错 "CORS policy: Credentials flag is 'true'"
**原因**: `allow_credentials=True` 时，`allow_origins` 不能为 `["*"]`
**解决**: 明确指定允许的域名

### Q3: OPTIONS 请求失败
**原因**: 预检请求被拦截
**解决**: 确保 `allow_methods` 包含 `"OPTIONS"`

### Q4: 自定义请求头被拦截
**原因**: `allow_headers` 没有包含该请求头
**解决**: 在 `allow_headers` 中添加该请求头

## 📝 最佳实践

1. ✅ **开发环境**: 使用 `localhost` 和具体端口
2. ✅ **生产环境**: 只允许特定域名
3. ✅ **使用环境变量**: 不同环境不同配置
4. ✅ **明确指定**: 不要使用 `["*"]`
5. ✅ **定期审查**: 检查是否有不必要的域名

## 🔗 相关资源

- [FastAPI CORS 文档](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS)
- [CORS 配置类](./internal/config/cors_config.py)

---

**当前状态**: ⚠️ 使用 `allow_origins=["*"]`（不安全）
**推荐操作**: 使用方案 1 或方案 2 进行配置

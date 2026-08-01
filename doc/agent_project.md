# FastAPI 项目结构说明

## 目录结构

```
agent/
├── app/                          # 应用主目录
│   ├── __init__.py
│   ├── main.py                   # FastAPI 应用入口，定义 app 实例
│   ├── crud.py                   # 数据库增删改查操作
│   ├── api/                      # API 层
│   │   ├── __init__.py
│   │   ├── deps.py               # 依赖注入（数据库会话、认证等）
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py            # API 路由聚合
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── users.py      # 用户相关接口
│   │           └── items.py     # 项目相关接口
│   ├── core/                     # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py             # 应用配置类
│   │   └── settings.py          # 环境变量配置
│   ├── db/                       # 数据库相关
│   │   ├── __init__.py
│   │   └── session.py           # 数据库连接和会话管理
│   ├── models/                   # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   └── models.py            # 数据模型定义
│   ├── schemas/                  # Pydantic 数据模型
│   │   ├── __init__.py
│   │   └── schemas.py           # 请求/响应数据验证模型
│   ├── services/                 # 业务逻辑层
│   │   └── __init__.py
│   └── utils/                    # 工具函数
│       └── __init__.py
├── tests/                        # 测试目录
│   ├── __init__.py
│   └── api/
│       └── __init__.py
├── doc/                         # 项目文档
├── .gitignore                   # Git 忽略配置
└── requirements.txt             # Python 依赖清单
```

## 启动命令

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 FastAPI 服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 运行测试

```bash
python test_api.py
```

## 核心模块说明

### 1. app/main.py
应用入口文件，包含 FastAPI 实例配置、CORS 中间件、路由注册等。

### 2. app/api/v1/
采用 RESTful API 设计风格，支持版本控制，便于后期升级兼容。

### 3. app/models/
使用 SQLAlchemy ORM 定义数据库表结构，支持多种数据库。

### 4. app/schemas/
使用 Pydantic 进行数据验证和序列化，确保 API 输入输出数据的规范性。
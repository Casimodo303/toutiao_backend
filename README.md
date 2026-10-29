# 头条资讯系统 · 后端服务（Toutiao Backend）

> 基于 **FastAPI + SQLAlchemy（异步）+ MySQL + Redis** 构建的仿今日头条新闻资讯系统后端，配套 Vue 3 移动端前端（位于 `.toutiao_frontend/`）。

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688?logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-8.1-DC382D?logo=redis&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-42B883?logo=vuedotjs&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [接口一览](#接口一览)
- [认证与响应格式](#认证与响应格式)
- [缓存设计](#缓存设计)
- [数据库表](#数据库表)
- [配置说明](#配置说明)
- [常见问题](#常见问题)
- [相关文档](#相关文档)
- [开发约定](#开发约定)
- [License](#license)

---

## 项目简介

这是一个面向移动端的新闻资讯应用后端 API 服务，提供新闻浏览、用户账号、收藏、浏览历史等核心能力：

- 全异步 IO：`FastAPI` + `AsyncSession` + `aiomysql`，单进程即可支撑较高并发；
- 分层清晰：`routers`（路由）→ `crud`（数据访问）→ `models`（ORM 模型），`schemas` 负责请求/响应校验；
- 热点数据走 Redis 缓存（分类、列表），缓存故障自动降级，不影响主流程；
- 统一响应体 `{code, message, data}`，全局异常处理器兜底；
- 自带 Swagger / ReDoc 交互文档，开箱可用。

## 功能特性

| 模块 | 能力 |
| --- | --- |
| 👤 用户管理 | 注册、登录、获取/更新个人信息、修改密码 |
| 📰 新闻模块 | 分类列表、分页 + 分类筛选的新闻列表、新闻详情（自动浏览量 +1、相关推荐） |
| ⭐ 收藏模块 | 收藏/取消收藏、收藏状态检查、收藏列表分页、清空收藏 |
| 🕘 浏览历史 | 记录浏览、历史列表分页、按 ID 删除单条、清空历史 |
| ⚡ 缓存模块 | 新闻分类、新闻列表热点数据缓存，失败自动降级 |
| 🛡️ 全局异常 | HTTP 异常 / 数据库完整性 / SQLAlchemy / 未知异常统一封装 |

## 技术栈

| 分类 | 选型 | 版本 |
| --- | --- | --- |
| 语言 | Python | 3.13 |
| Web 框架 | FastAPI | 0.142.2 |
| ASGI 服务器 | Uvicorn | 0.54.0 |
| ORM | SQLAlchemy（异步） | 2.1.4 |
| 数据库 | MySQL | 8.0+ |
| 数据库驱动 | aiomysql / PyMySQL | 0.3.2 / 1.2.3 |
| 缓存 | Redis（redis-py asyncio） | 8.1.0 |
| 数据校验 | Pydantic | 2.13.5 |
| 密码加密 | passlib + bcrypt | 1.7.4 / 3.2.2 |
| 前端（附带） | Vue 3 + Vite 7 + Vant 4 + Pinia 3 | — |

## 项目结构

```text
toutiao_backend/
├── main.py                     # 应用入口：FastAPI 实例化、CORS、全局异常、路由挂载
├── config/
│   ├── db_conf.py              # 异步数据库引擎、会话工厂、get_db 依赖
│   └── cache_conf.py           # Redis 客户端与缓存读写封装（失败降级）
├── models/                     # SQLAlchemy ORM 模型
│   ├── users.py                # User / UserToken
│   ├── news.py                 # Category / News
│   ├── favorite.py             # Favorite
│   └── history.py              # History
├── schemas/                    # Pydantic 请求/响应模型
├── crud/                       # 数据访问层（纯数据库操作）
├── routers/                    # API 路由层（参数校验、权限、响应组装）
│   ├── users.py                # /api/user/*
│   ├── news.py                 # /api/news/*
│   ├── favorite.py             # /api/favorite/*
│   └── history.py              # /api/history/*
├── cache/news.py               # 新闻相关缓存键与读写封装
├── utils/
│   ├── auth.py                 # Token 校验依赖 get_current_user
│   ├── security.py             # bcrypt 密码哈希 / 校验
│   ├── response.py             # success_response 统一成功响应
│   ├── exception.py            # 各异常处理函数
│   └── exception_handlers.py   # 异常处理器注册
├── static/favicon.ico          # 站点图标
├── .material/                  # 设计文档、API 规范、建表 SQL
├── .toutiao_frontend/          # 配套 Vue 3 前端
├── test_main.http              # 接口调试请求样例
└── requirements.txt            # Python 依赖清单
```

## 快速开始

### 环境要求

- Python **3.11+**（开发环境为 3.13）
- MySQL **8.0+**
- Redis **5.0+**（已验证兼容 phpStudy 自带的 Redis 3.0.504）
- Node.js **18+**（仅前端需要）

### 1. 获取代码

```bash
git clone https://github.com/Casimodo303/toutiao_backend.git
cd toutiao_backend
```

### 2. 初始化 MySQL 数据库

`.material/database.sql` 已包含建库、建表与索引定义：

```bash
mysql -u root -p < .material/database.sql
```

> 脚本会创建数据库 `news_app`（字符集 `utf8mb4`）及 `user`、`user_token`、`news_category`、`news`、`favorite`、`history` 六张表。

### 3. 修改配置文件

**数据库** `config/db_conf.py`：

```python
ASYNC_DATABASE_URL = 'mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4'
```

按实际环境替换用户名、密码、主机、端口。

**缓存** `config/cache_conf.py`：

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DATABASE = 0
```

> 若 Redis 版本较旧（如 3.x）报 `unknown command 'HELLO'`，保持已有的 `protocol=2` 即可解决。
> 缓存异常只会打印 warning 并降级查库，不会导致接口 500。

### 4. 创建虚拟环境并安装依赖

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 5. 启动服务

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

启动后可访问：

| 地址 | 说明 |
| --- | --- |
| <http://127.0.0.1:8000/> | 根路由健康检查 |
| <http://127.0.0.1:8000/docs> | Swagger UI 交互文档 |
| <http://127.0.0.1:8000/redoc> | ReDoc 文档 |

### 6.（可选）启动前端

前端已配置后端地址 `http://127.0.0.1:8000`，CORS 已允许 `5173` 端口：

```bash
cd .toutiao_frontend
npm install
npm run dev
```

访问 <http://127.0.0.1:5173> 即可联调。

## 接口一览

基础 URL：`http://127.0.0.1:8000`

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 | 需认证 |
| --- | --- | --- | :---: |
| POST | `/api/user/register` | 用户注册（返回 token） | ❌ |
| POST | `/api/user/login` | 用户登录（返回 token） | ❌ |
| GET | `/api/user/info` | 获取当前用户信息 | ✅ |
| PUT | `/api/user/update` | 更新昵称、头像、性别、简介、手机号 | ✅ |
| PUT | `/api/user/password` | 修改密码（`oldPassword` / `newPassword`） | ✅ |

### 新闻模块 `/api/news`

| 方法 | 路径 | 说明 | 需认证 |
| --- | --- | --- | :---: |
| GET | `/api/news/categories` | 获取新闻分类列表（`skip`、`limit`） | ❌ |
| GET | `/api/news/list` | 新闻列表（`categoryId`、`page`、`pageSize`） | ❌ |
| GET | `/api/news/detail` | 新闻详情（`id`），自动 +1 浏览量并返回 `relatedNews` | ❌ |

### 收藏模块 `/api/favorite`

| 方法 | 路径 | 说明 | 需认证 |
| --- | --- | --- | :---: |
| GET | `/api/favorite/check` | 检查收藏状态（`newsId`） | ✅ |
| POST | `/api/favorite/add` | 添加收藏（body：`newsId`） | ✅ |
| DELETE | `/api/favorite/remove` | 取消收藏（`newsId`） | ✅ |
| GET | `/api/favorite/list` | 收藏列表（`page`、`pageSize`） | ✅ |
| DELETE | `/api/favorite/clear` | 清空全部收藏 | ✅ |

### 浏览历史模块 `/api/history`

| 方法 | 路径 | 说明 | 需认证 |
| --- | --- | --- | :---: |
| POST | `/api/history/add` | 添加浏览记录（body：`newsId`） | ✅ |
| GET | `/api/history/list` | 历史列表（`page`、`pageSize`） | ✅ |
| DELETE | `/api/history/delete/{history_id}` | 删除单条历史记录 | ✅ |
| DELETE | `/api/history/clear` | 清空全部历史 | ✅ |

> 完整请求/响应示例见 [`.material/API接口规范文档.md`](.material/API接口规范文档.md)。

## 认证与响应格式

### 认证

1. 注册 / 登录成功后返回 `token`；
2. 需要认证的接口在请求头携带：

```http
Authorization: <token>
```

令牌同时兼容 `Bearer <token>` 写法（`utils/auth.py` 会自动剥离前缀）。令牌存入 `user_token` 表，**有效期 7 天**，过期或缺失返回 `401`。

> 重复登录会刷新同一用户的令牌，旧令牌随即失效。

### 统一响应体

```json
{
  "code": 200,
  "message": "获取新闻列表成功",
  "data": {
    "list": [],
    "total": 0,
    "hasMore": false
  }
}
```

异常同样遵循该结构（`data` 通常为 `null`）：

| 状态码 | 场景 |
| --- | --- |
| 400 | 参数错误、用户名已存在、旧密码错误等业务校验失败 |
| 401 | 未提供令牌 / 令牌无效或过期 / 用户名或密码错误 |
| 404 | 新闻、收藏、历史记录不存在 |
| 500 | 数据库或未捕获的服务器异常 |

开发模式下（`utils/exception.py` 中 `DEBUG_MODE = True`）500 响应会附带 `error_type`、`error_detail`、`traceback`，**上线前请置为 `False`**。

## 缓存设计

Redis 仅缓存读多写少的热点数据，键与过期时间如下：

| 数据 | 缓存键 | 过期时间 |
| --- | --- | --- |
| 新闻分类 | `news:categories` | 7200 s（2 h） |
| 新闻列表 | `news:list:{category_id}:{page}:{size}` | 600 s（10 min） |
| 新闻详情 | `news:detail:{news_id}` | 1800 s（30 min） |
| 用户历史 | `history:list:{user_id}` | 3600 s（1 h） |
| 验证码 | `code:{phone}` | 120 s（预留） |

策略：**Cache-Aside + 失效优先**。读缓存未命中则查库并回填；缓存读写异常被 `try/except` 捕获并记录 warning，降级为直接访问数据库。

## 数据库表

| 表名 | 说明 |
| --- | --- |
| `user` | 用户信息（密码 bcrypt 加密存储） |
| `user_token` | 登录令牌及过期时间，级联删除 |
| `news_category` | 新闻分类与排序 |
| `news` | 新闻正文、封面、作者、浏览量、发布时间 |
| `favorite` | 用户-新闻收藏关系，联合唯一约束 |
| `history` | 用户浏览记录及浏览时间 |

建表与初始化数据详见 [`.material/database.sql`](.material/database.sql)。

## 配置说明

| 配置项 | 位置 | 说明 |
| --- | --- | --- |
| `ASYNC_DATABASE_URL` | `config/db_conf.py` | MySQL 异步连接串，含连接池（`pool_size=10`、`max_overflow=20`、`pool_pre_ping=True`） |
| `REDIS_HOST` / `PORT` / `DATABASE` | `config/cache_conf.py` | Redis 连接信息，`protocol=2` 兼容旧版服务端 |
| `DEBUG_MODE` | `utils/exception.py` | 是否在错误响应中返回堆栈，生产环境置 `False` |
| `allow_origins` | `main.py` | CORS 白名单，默认放行 `127.0.0.1:5173`、`localhost:5173` |

> ⚠️ **安全提示**：当前数据库账号密码、`.toutiao_frontend/src/config/api.js` 中的 AI API Key 均为硬编码。提交公开仓库前，建议改为环境变量（如 `python-dotenv` + `.env`），并立即吊销已泄露的 Key。

## 常见问题

**1. `RuntimeError: 'cryptography' package is required` 或 bcrypt 报错**
`passlib 1.7.4` 与 `bcrypt >= 4.1` 存在兼容问题，本项目已锁定 `bcrypt==3.2.2`，请勿随意升级。

**2. 启动报 `Can't connect to MySQL server`**
确认 MySQL 已启动、`news_app` 数据库已创建、`db_conf.py` 中的账号密码与本机一致。

**3. Redis 连接报 `unknown command 'HELLO'`**
旧版 Redis 不支持 RESP3，已通过 `protocol=2` 规避；若仍报错请检查 Redis 是否启动。

**4. 前端请求被浏览器拦截（CORS）**
确认前端运行在 `5173` 端口，或在 `main.py` 的 `allow_origins` 中补充你的源。

**5. 修改模型后表结构未更新**
项目未接入 Alembic，表结构以 `.material/database.sql` 为准；模型变更需手动同步 SQL 或自行引入迁移工具。

**6. 端口 8000 被占用**
改用 `uvicorn main:app --reload --port 8001`，并同步修改前端 `src/config/api.js` 中的 `baseURL`。

## 相关文档

- [项目后端设计说明文档](.material/项目后端设计说明文档.md) — 架构、模块划分与缓存策略
- [API 接口规范文档](.material/API接口规范文档.md) — 全量接口的请求/响应示例
- [database.sql](.material/database.sql) — 建库建表脚本
- [test_main.http](test_main.http) — IDE 内快速调试请求

## 开发约定

- **分层职责**：路由只做参数校验与响应组装，SQL 一律写在 `crud/`；
- **全异步**：数据库、Redis 操作均使用 `async/await`，禁止在异步函数中调用同步阻塞驱动；
- **命名**：数据库字段用蛇形命名，对外 JSON 用驼峰（通过 `alias` 转换，如 `categoryId`、`pageSize`）；
- **响应**：成功统一走 `success_response()`，失败统一 `raise HTTPException`，由全局处理器封装；
- **注释**：每个模块头部保留「名称 / 作用 / 主要依赖」说明块。

## License

本项目仅用于学习与技术交流，遵循 [MIT License](https://opensource.org/licenses/MIT)。

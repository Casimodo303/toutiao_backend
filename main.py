#===============================================================
# 名称：main.py
# 作用：主模块，FastAPI实例化，对挂载路由注册，注册全局异常，实现跨域链接中间件(Vue)
# 主要依赖：router/(news, users), utils/exception_handlers
#===============================================================
# 三方库
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 本地库
from routers import news,users
from utils.exception_handlers import register_exception_handlers

# FastAPI实例化
app = FastAPI()

# 注册异常处理器（全局异常处理）
register_exception_handlers(app)

# 跨域链接中间件(其实可以塞到FastAPI实例化里，看着比较简洁)
# 作用:由于后端FastAPI端口为8000，前端Vue端口为5173，浏览器识别为跨域拒绝调用，所以通过中间件使后端允许前端的权限
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],    # 允许访问的源
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=['*'],    # 允许所有请求方法
    allow_headers=['*']     # 允许所有请求头
    # 注意：真实项目开发应当避免使用'*'
)

# 根路由测试
@app.get("/")
async def root():
    return {'message': 'Hello World'}

# 挂载路由/注册路由
app.include_router(news.router)

# 挂载路由/注册路由
app.include_router(users.router)

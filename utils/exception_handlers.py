# 三方库
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# 本地库
from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, general_exception_handler

# 注册全局异常处理
def register_exception_handlers(app):
    # 注册顺序规范： 子类在前，父类在后；具体在前，抽象在后
    app.add_exception_handler(HTTPException, http_exception_handler)        # 业务逻辑错误
    app.add_exception_handler(IntegrityError, integrity_error_handler)      # 数据库完整性错误
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)    # 数据库错误
    app.add_exception_handler(Exception, general_exception_handler)         # 其他错误
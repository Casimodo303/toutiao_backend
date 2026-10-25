#===============================================================
# 名称：utils/exception.py
# 作用：路由返回体封装(可在router模块被调用，实现返回体的复写)
# 主要依赖：
#===============================================================
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str="success", data=None):
    content = {
        'code': 200,
        'message': message,
        'data': data
    }
    # 目标：将任何FastAPI， Pydantic, ORM对象，都要正常响应 code, message, data
    return JSONResponse(content=jsonable_encoder(content))


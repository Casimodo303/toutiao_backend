#===============================================================
# 名称：utils/auth.py
# 作用：验证 Token (已被封装成依赖项，可被多接口复用)
# 主要依赖：
#===============================================================
# 标准库
from typing import Optional

# 三方库
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

# 本地库
from config.db_conf import get_db
from crud import users

# 根据 Token 查询用户，返回用户
async def get_current_user(
        authorization: Optional[str] = Header(None, alias='Authorization'),
        db: AsyncSession = Depends(get_db)
):
    # 取请求头中的 token：兼容前端两种写法 'Bearer xxx' / 直接传 'xxx'
    token = (authorization or '').strip()
    if token.lower().startswith('bearer '):
        token = token[7:].strip()

    # 没带 token 时返回 401（而不是让 Header(...) 抛 422）
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='未提供令牌')

    # 查库校验 token 是否存在且未过期
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='无效的令牌或令牌已过期')
    return user

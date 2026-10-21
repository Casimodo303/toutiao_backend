# 三方库
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

# 本地库
from config.db_conf import get_db
from crud import users

# 整合，根据 Token 查询用户，返回用户
async def get_current_user(authorization: str = Header(..., alias='Authorization'), db: AsyncSession = Depends(get_db)):
    token = authorization.replace('Bearer', '')

    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHDRIZED, detail='无效的令牌或令牌已过期')
    return user

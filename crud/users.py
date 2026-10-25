#===============================================================
# 名称：crud/users.py
# 作用：为用户提供数据库增删改查的方法
# 主要依赖：models/users, schemas/users, utils/seurity
#===============================================================
# 官方库
import uuid
from datetime import datetime, timedelta

# 三方库
from fastapi import HTTPException
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

# 本地库
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security


# 查询对应用户名用户
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 新增用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密再添加
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)   # 从数据库中读回最新的user
    return user

# 新增token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token + 设置过期时间
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)  # 设置七天有限期
    # 查库看当前用户是否已有token，有：更新，没有：新增
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token

# 验证用户是否存在
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

# 查询对应Token用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')

    # 获取更新后的用户信息
    update_user = await get_user_by_username(db, username)
    return update_user

# 修改密码
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if security.verify_password(new_password, user.password):
        return 1
    if not security.verify_password(old_password, user.password):
        return 2

    hash_new_password = security.get_hash_password(new_password)
    user.password = hash_new_password
    db.add(user) # 让SQLAlchemy接管user，防止万一会话关闭新密码没有提交上去
    await db.commit()
    await db.refresh(user)
    return 3






















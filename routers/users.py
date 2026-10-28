#===============================================================
# 名称：routers/users.py
# 作用：为用户提供后端路由接口
# 主要依赖：crud/users, config/db_conf, schemas/users, utils/(auth, response)
#===============================================================
# 三方库
from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status

# 本地库
from crud import users
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePwdRequest
from config.db_conf import get_db
from utils.response import success_response
from utils.auth import get_current_user

# 创建APIRouter实例
router = APIRouter(prefix='/api/user', tags=['users'])


# 用户注册路由
@router.post('/register')
async def register(user_data: UserRequest = Body(...), db = Depends(get_db)):
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户已存在')
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    # return {
    #     'code': 200,
    #     'message': '注册成功',
    #     'data': {
    #         'token': token,
    #         'userInfo': {
    #             'id': user.id,
    #             'username': user.username,
    #             'bio': user.bio,
    #             'avatar': user.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message='注册成功', data=response_data)

# 用户登录路由
@router.post('/login')
async def login(user_data: UserRequest, db = Depends(get_db)):
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='用户名或密码错误')
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message='登录成功', data=response_data)

# 用户查询路由
@router.get('/info')
async def get_user_info(user = Depends(get_current_user)):
    return success_response(message='获取用户信息成功', data=UserInfoResponse.model_validate(user))

# 用户信息修改路由
@router.put('/update')
async def update_user_info(
        user_data: UserUpdateRequest,
        user= Depends(get_current_user),
        db = Depends(get_db)
):
    update_user = await users.update_user(db, user.username, user_data)
    return success_response(message='更新用户信息成功', data=UserInfoResponse.model_validate(update_user))

# 密码修改路由
@router.put('/password')
async def update_password(
        password_data: UserChangePwdRequest,
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    res_change_pwd = await users.change_password(db, user, password_data.old_password, password_data.new_password)
    if res_change_pwd == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码与新密码不能相同")
    elif res_change_pwd == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")
    return success_response(message='修改密码成功')














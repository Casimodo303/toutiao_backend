# 官方库
from typing import Optional

# 三方库
from pydantic import BaseModel, Field, ConfigDict


# 用户注册校验类
class UserRequest(BaseModel):
    username: str
    password: str

# user_info 对应的基础类
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description='昵称')
    avatar: Optional[str] = Field(None, max_length=255, description='头像URL')
    gender: Optional[str] = Field(None, max_length=10, description='性别')
    bio: Optional[str] = Field(None, max_length=500, description='个人简介')

# user_info 数据类型
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象中取值
    )


# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias='userInfo')

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # 允许字段名兼容
        from_attributes=True  # 允许从 ORM 对象中取值
    )

# 更新用户 信息模型类
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None









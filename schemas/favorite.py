#===============================================================
# 名称：schemas/favorite.py
# 作用：为收藏提供校验类
# 主要依赖：
#===============================================================
# 标准库
from datetime import datetime

# 三方库
from pydantic import BaseModel, Field, ConfigDict

# 本地库
from schemas.news import NewsItemBase

# 收藏状态类
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool =Field(..., alias='isFavorite')

# 添加收藏类
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId')

# 收藏新闻模型类
class FavoriteNewsItemRequest(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 收藏列表类
class FavoriteListRequest(BaseModel):
    list: list[FavoriteNewsItemRequest]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
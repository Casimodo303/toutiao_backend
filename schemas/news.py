#===============================================================
# 名称：schemas/users.py
# 作用：为用户提供校验类
# 主要依赖：
#===============================================================
# 官方库
from datetime import datetime
from typing import Optional

# 三方库
from pydantic import BaseModel, Field, ConfigDict

# 新闻模型类
class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
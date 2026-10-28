#===============================================================
# 名称：schemas/history.py
# 作用：为历史提供校验类
# 主要依赖：
#===============================================================
# 标准库
from datetime import datetime

# 三方库
from pydantic import BaseModel, Field, ConfigDict

# 本地库
from schemas.news import NewsItemBase

# 添加浏览历史类
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId')

# 历史新闻模型类
class HistoryNewsItemRequest(NewsItemBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 历史列表类
class HistoryListRequest(BaseModel):
    list: list[HistoryNewsItemRequest]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
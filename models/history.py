#===============================================================
# 名称：models/history.py
# 作用：为历史提供数据库模型类
# 主要依赖：
#===============================================================
# 官方库
from datetime import datetime

# 三方库
from sqlalchemy import ForeignKey, DateTime, Index, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 本地库
from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass

class History(Base):
    __tablename__ = 'history'

    __table_args__ = (
        Index('fk_history_news_idx', 'news_id'),
        Index('fk_history_user_idx', 'user_id'),
        Index('idx_view_time', 'view_time')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='历史ID')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment='用户ID')
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment='新闻ID')
    view_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, comment='浏览时间')

    def __repr__(self):
        return f'<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})'


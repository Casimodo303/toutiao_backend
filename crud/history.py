#===============================================================
# 名称：crud/history.py
# 作用：为历史提供数据库增删改查的方法
# 主要依赖：models/(history, news)
#===============================================================
# 标准库
from datetime import datetime

# 三方库
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

# 本地库
from models.history import History
from models.news import News


# 添加浏览历史
async def add_news_history(db, user_id, news_id):
    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    existing = (await db.execute(stmt)).scalars().first()

    if existing:
        # 已浏览过：只刷新浏览时间
        existing.view_time = datetime.now()
        await db.commit()
        await db.refresh(existing)
        return existing

    # 首次浏览：新增
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


# 删除历史（按历史记录ID删除，一条记录只删一条，不会误删同一条新闻的其他记录）
async def remove_history_by_id(
        db: AsyncSession,
        user_id: int,
        history_id: int
):
    stmt = delete(History).where(History.user_id == user_id, History.id == history_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# 查询浏览历史列表
async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page:int = 1,
        page_size: int = 10
):
    # 获取总量 + 历史的新闻列表
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one_or_none()

    # 获取历史列表（联表查询）
    offset = (page - 1) * page_size
    query = (select(News, History.view_time, History.id.label("history_id"))
             .join(History, History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset(offset).limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()
    return rows, total

# 删除浏览历史列表
async def remove_all_history(
        db: AsyncSession,
        user_id: int
):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0

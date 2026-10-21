# 三方库
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

# 本地库
from models.news import Category, News

# 查询新闻分类表
async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 查询新闻列表
async def get_news_list(db: AsyncSession, category_id: int, skip: int=0, limit: int=10):
    # 查询的是指定分类的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 查询新闻分类总条数
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 用scalar效果一样，scalar_one只是怕万一有同名列

# 查询单条新闻
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  # 可能查不到

# 修改新闻浏览量(即浏览一次就+1)
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result= await db.execute(stmt)
    await db.commit()
    # 额外操作：检查数据库是否真的命中了数据，健壮性
    return result.rowcount > 0

# 查询相关新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int=5):
    # order_by: 排序，按浏览量和发布时间推荐
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id,
    ).order_by(
        News.views.desc(),   # 浏览量降序排，默认降序
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all() # 可以这样返回，不过会返回很多没有用的数据
    related_news = result.scalars().all()
    # 用列表推导式推导出核心数据
    return [{
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'image': news.image,
        'author': news.author,
        'publishTime': news.publish_time,
        'categoryId': news.category_id,
        'views': news
    } for news in related_news]





#===============================================================
# 名称：crud/news.py
# 作用：为新闻提供数据库增删改查的方法
# 主要依赖：models/news, cache/news, schemas/news
#===============================================================
# 三方库
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

# 本地库
from models.news import Category, News
from cache import news
from schemas.news import NewsItemBase

# 查询新闻分类表
async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):
    # 先尝试从缓存中获取数据
    cached_categories = await news.get_cached_categories()
    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories =  result.scalars().all()
    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await news.set_cache_categories(categories)
    # 返回数据
    return categories

# 查询新闻列表
async def get_news_list(db: AsyncSession, category_id: int, skip: int=0, limit: int=10):
    # 先尝试从缓存中取
    page = skip // limit + 1
    cached_list = await news.get_cache_news_list(category_id, page, limit)
    if cached_list:
        return cached_list
    # 查询的是指定分类的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list =  result.scalars().all()
    # 写入缓存
    if news_list:
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await news.set_cache_news_list(category_id, page, limit, news_data)
    # 返回数据
    return news_list

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
        'id': new.id,
        'title': new.title,
        'content': new.content,
        'image': new.image,
        'author': new.author,
        'publishTime': new.publish_time,
        'categoryId': new.category_id,
        'views': new.views
    } for new in related_news]

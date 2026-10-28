#===============================================================
# 名称：routers/news.py
# 作用：为新闻提供后端路由接口
# 主要依赖：crud/news, config/db_conf
#===============================================================
# 三方库
from fastapi import APIRouter, Depends, Query, HTTPException

# 本地库
from crud import news
from config.db_conf import get_db

# 创建APIRouter实例
router = APIRouter(prefix='/api/news', tags=['news'])


# 新闻分类接口路由
@router.get('/categories')
async def get_categories(skip: int=0,limit: int=100, db = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        'code': 200,
        'message': '获取新闻分类成功',
        'data': categories
    }

# 新闻分类列表路由
@router.get('/list')
async def get_news(
        category_id: int = Query(..., alias='categoryId'), # 由于前端用的驼峰，所以后端用全小写的时候要添加别名
        page: int =  Query(1, ge=1),
        page_size: int = Query(10, le=100,alias='pageSize'),
        db = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    # 是否还有更多：（跳过的（skip） + 当前列表里面的数量） < 总量（total）
    has_more = (offset + len(news_list)) < total
    return {
        'code': 200,
        'message': '获取新闻列表成功',
        'data': {
            'list': news_list,
            'total': total,
            'hasMore': has_more
        }
    }

# 新闻详情内容路由(响应结果：新闻详情+增加1浏览量+相关新闻)
@router.get('/detail')
async def read_news_detail(news_id: int = Query(..., alias='id'), db = Depends(get_db)):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail: # 新闻可能不存在
        raise HTTPException(status_code=404, detail='新闻不存在')
    news_views = await news.increase_news_views(db, news_id)
    await db.refresh(news_detail)
    if not news_views:
        raise HTTPException(status_code=404, detail='新闻不存在')
    related_news = await news.get_related_news(db, news_id, news_detail.category_id)
    return {
        'code': 200,
        'message': '获取新闻内容成功',
        'data': {
            'id': news_detail.id,
            'title': news_detail.title,
            'content': news_detail.content,
            'image': news_detail.image,
            'author': news_detail.author,
            'publishTime': news_detail.publish_time,
            'categoryId': news_detail.category_id,
            'views': news_detail.views,
            'relatedNews': related_news
        }
    }


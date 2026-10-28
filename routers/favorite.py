#===============================================================
# 名称：routers/favorite.py
# 作用：为收藏提供后端路由接口
# 主要依赖：crud/users, config/db_conf, schemas/users, utils/(auth, response)
#===============================================================
# 三方库
from fastapi import APIRouter, Query, Depends, Body, HTTPException
from starlette import status

# 本地库
from crud import favorite
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListRequest
from config.db_conf import get_db
from utils.response import success_response
from utils.auth import get_current_user

# 创建APIRouter实例
router = APIRouter(prefix='/api/favorite', tags=['favorite'])

# 查询收藏状态路由
@router.get('/check')
async def check_favorite(
        news_id: int = Query(..., alias='newsId'),
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorited))

# 添加收藏路由
@router.post('/add')
async def add_favorite(
        data: FavoriteAddRequest,
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="收藏成功", data=result)

# 删除收藏路由
@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    result = favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detial="收藏记录不存在")
    return success_response(message="取消收藏成功")

# 获取收藏列表路由
@router.get("/list")
async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1,le=100, alias="pageSize"),
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [{
         **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news, favorite_time, favorite_id, in rows]
    has_more = total > page * page_size
    data = FavoriteListRequest(list=favorite_list, total=total, hasMore=has_more)
    return success_response(message="获取收藏列表成功", data=data)

# 清空收藏列表路由
@router.delete("/clear")
async def clear_favorite(
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    count = await favorite.remove_all_favorite(db, user.id)
    return success_response(message=f"清空了{count}条收藏")
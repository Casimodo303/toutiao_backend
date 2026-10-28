#===============================================================
# 名称：routers/history.py
# 作用：为历史提供后端路由接口
# 主要依赖：crud/history, config/db_conf, schemas/history, utils/(auth, response)
#===============================================================
# 三方库
from fastapi import APIRouter, Query, Depends, HTTPException
from starlette import status

# 本地库
from crud import history
from schemas.history import HistoryAddRequest, HistoryListRequest
from config.db_conf import get_db
from utils.response import success_response
from utils.auth import get_current_user

# 创建APIRouter实例
router = APIRouter(prefix='/api/history', tags=['history'])


# 添加历史路由
@router.post('/add')
async def add_history(
        data: HistoryAddRequest,
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    result = await history.add_news_history(db, user.id, data.news_id)
    data = {'historyId': result.id, 'viewTime': result.view_time}
    return success_response(message="添加成功", data=data)

# 删除历史路由（按历史记录ID删除）
@router.delete("/delete/{history_id}")
async def remove_history_by_path(
        history_id: int,
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    result = await history.remove_history_by_id(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在")
    return success_response(message="取消浏览历史成功")

# 获取浏览历史列表
@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1,le=100, alias="pageSize"),
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    rows, total = await history.get_history_list(db, user.id, page, page_size)
    history_list = [{
         **{k: v for k, v in news.__dict__.items() if not k.startswith('_')},
        "view_time": view_time,
        "history_id": history_id
    } for news, view_time, history_id in rows]
    has_more = total > page * page_size
    data = HistoryListRequest(list=history_list, total=total, hasMore=has_more)
    return success_response(message="获取历史列表成功", data=data)

# 清空历史列表路由
@router.delete("/clear")
async def clear_history(
        user = Depends(get_current_user),
        db = Depends(get_db)
):
    count = await history.remove_all_history(db, user.id)
    return success_response(message=f"清空了{count}条浏览历史")




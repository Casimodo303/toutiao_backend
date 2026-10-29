#===============================================================
# 名称：cache/news.py
# 作用：为新闻模块提供缓存
# 主要依赖：config/cache_conf
#===============================================================
# 三方库
from typing import List, Dict, Any, Optional

# 本地库
from config.cache_conf import get_json_cache, set_cache

# 新闻分类缓存key
CATEGORIES_KEY = "news:categories"
# 新闻列表缓存key
NEWS_LIST_PREFIX = "news_list:"

# 设置新闻分类缓存
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)

# 读取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)


# 设置新闻列表缓存
async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]], expire: int=600):
      category_part = category_id if category_id is not None else "all"
      key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
      return await set_cache(key, news_list, expire)

# 读取新闻列表缓存
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
      category_part = category_id if category_id is not None else "all"
      key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
      return await get_json_cache(key)
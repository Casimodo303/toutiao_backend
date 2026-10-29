#===============================================================
# 名称：config/cache_conf.py
# 作用：通过redis，完成成对数据缓存的配置
# 主要依赖：
#===============================================================
# 标准库
import json
import logging
from typing import Any

# 三方库
import redis.asyncio as redis

# 缓存日志：使用 logging 而不是 print，
# 因为 print 在 stdout 失效（如 IDE/后台启动的进程）时会抛 OSError，
# 把“本应被忽略的缓存异常”变成接口 500
logger = logging.getLogger(__name__)

# IP地址
REDIS_HOST = "localhost"
# 端口号
REDIS_PORT = 6379
# 默认隔离数据库
REDIS_DATABASE = 0

# 创建Redis的连接对象
redis_client =  redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DATABASE,
    decode_responses=True, # 是否要将字节解码为字符串
    protocol=2  # 强制使用 RESP2：redis-py 8 默认 RESP3，连接时会先发 HELLO 3，
                # 而 phpStudy 自带的 Redis 3.0.504 不支持 HELLO 命令，会直接报错
)

# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600): # 键，值，过期时间
    try:
        if isinstance(value, (dict, list)):
            # 如果为字典或者列表，先转字符串
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:  # 缓存失败不能影响主流程
        logger.warning("设置缓存失败 key=%s: %r", key, e)
        return None


# 读取缓存（字符串）
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        logger.warning("获取缓存失败 key=%s: %r", key, e)
        return None

# 读取缓存（列表或字符串）
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.warning("获取 JSON 缓存失败 key=%s: %r", key, e)
        return None

"""
过期时间配置：
    新闻分类    7200
    新闻列表    600
    新闻详情    1800
    验证码      120
"""

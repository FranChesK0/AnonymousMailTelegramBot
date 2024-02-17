import pickle
import datetime
from typing import Any, Optional

from redis.asyncio import Redis

from core import settings

redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    db=settings.redis.db,
)


async def get_value(key: str) -> Any:
    """
    Returns the value of the passed key from the redis database.\n
    Note: If the key is not in the redis database, None is returned.
    :param key: A key for the search.
    :return: Value of the key.
    """
    value = await redis.get(f"{settings.redis.prefix}-{key}")
    return value if value is None else pickle.loads(value)


async def set_value(
    key: str, value: Any, expire: Optional[int | datetime.timedelta] = None
) -> None:
    """
    Sets the key value pair in the redis database.
    :param key: A key to set.
    :param value: Value of the key.
    :param expire: Allows setting the storage time for the value.
    :return:
    """
    await redis.set(f"{settings.redis.prefix}-{key}", pickle.dumps(value), ex=expire)


async def delete_values(*keys: str) -> int:
    """
    Deletes the key value pair from the redis database.
    :param keys: Keys to delete.
    :return: Number of deleted keys.
    """
    if not keys:
        return 0
    return int(await redis.delete(*map(lambda k: f"{settings.redis.prefix}-{k}", keys)))


async def get_keys(key_pattern: Optional[str] = None) -> list[str]:
    """
    Returns a list of redis database keys.
    :param key_pattern: Allows filtering keys by pattern.
    :return: List of keys.
    """
    keys = []
    async for key in redis.scan_iter(f"{settings.redis.prefix}-{key_pattern or '*'}"):
        keys.append(key.decode().removeprefix(f"{settings.redis.prefix}-"))
    return keys

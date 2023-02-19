from aioredis import Redis
import json
from typing import Dict, List, Optional, Any
import pickle


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def process(self) -> str:
        await self._redis.set("my-key", "value")
        return await self._redis.get("my-key")

    async def set(self, key: str, value: Any) -> None:
        if type(value) in [str, int, float]:
            await self._redis.set(key, value)
        elif type(value) is Dict:
            await self._redis.set(key, json.dumps(value, ensure_ascii=False).encode("utf-8"))
        else:
            await self._redis.set(key, pickle.dumps(value))

    async def get(self, key: str, get_type: Optional[type] = None) -> Any:
        res = await self._redis.get(key)

        if not get_type:
            return res
        elif get_type is Dict:
            if res:
                return json.loads(await self._redis.get(key))
        elif get_type is tuple:
            if res:
                return pickle.loads(res)

        return None

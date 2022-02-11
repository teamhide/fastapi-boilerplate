import aioredis

from core.config import config

redis = aioredis.from_url(url=f"redis://{config.REDIS_HOST}")

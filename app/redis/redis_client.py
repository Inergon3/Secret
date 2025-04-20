from app.config import REDIS_PORT, REDIS_HOST
from redis.asyncio import Redis

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
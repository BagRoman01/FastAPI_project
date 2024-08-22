from fastapi import FastAPI
from app.api.endpoints.authentication import auth
from app.api.endpoints.currency import currency
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(this_app: FastAPI):
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    pong = await redis.ping()
    print(f"Connected to Redis: {pong}")
    cache_backend = FastAPICache.get_backend()
    print(f"Cache Backend Initialized: {cache_backend}")
    # Check cache keys
    all_keys = await redis.keys('*')
    print(f"Current Redis Keys: {all_keys}")

    yield

    print('Clear cache!')
    await FastAPICache.clear()


app = FastAPI(lifespan=lifespan)

app.include_router(auth)
app.include_router(currency)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)


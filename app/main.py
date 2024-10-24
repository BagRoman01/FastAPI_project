from fastapi import FastAPI
from app.api.endpoints.authentication import auth
from app.api.endpoints.currency import currency
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings


# @asynccontextmanager
# async def lifespan(this_app: FastAPI):
#     redis = aioredis.from_url("redis://" + settings.REDIS_HOST, encoding="utf-8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     pong = await redis.ping()
#     print(f"Connected to Redis: {pong}")
#     cache_backend = FastAPICache.get_backend()
#     print(f"Cache Backend Initialized: {cache_backend}")
#
#     yield
#
#     print('Clear cache!')
#     await FastAPICache.clear()


# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(auth)
app.include_router(currency)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).strip().rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
print([str(origin).strip().rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS])

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from redis.exceptions import ConnectionError as RedisConnectionError

from app.api.v1 import router as api_router
from app.utils.logger import user_logger, error_logger


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"],
    storage_uri=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)
app = FastAPI(docs_url="/docs", root_path="/api")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(api_router)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирование всех входящих запросов."""
    user_logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений."""
    error_logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Внутренняя ошибка сервера. Пожалуйста, попробуйте позже."},
    )


@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429, content={"error": f"Превышен лимит запросов: {exc.detail}"}
    )


@app.exception_handler(RedisConnectionError)
async def redis_connection_error_handler(request: Request, exc: RedisConnectionError):
    error_logger.error(f"Ошибка подключения к Redis: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Внутренняя ошибка сервера. Пожалуйста, попробуйте позже."},
    )


if __name__ == "__main__":
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        exit()

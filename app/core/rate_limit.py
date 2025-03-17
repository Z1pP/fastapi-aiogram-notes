import redis
from datetime import datetime, timedelta
from functools import wraps
from fastapi import HTTPException


class RateLimiterDecorator:
    def __init__(
        self,
        rate_limit: int = 15,
        time_window: timedelta = timedelta(seconds=60),
        *,
        use_redis: bool = False,
        redis_host: str = "localhost",
        redis_port: int = 6379
    ):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.use_redis = use_redis
        self.request_count = {}

        if self.use_redis:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

    def is_rate_limited(self, key: str) -> bool:
        current_time = datetime.now()

        if self.use_redis:
            # Redis implementation
            request_count = self.redis_client.get(key)
            if not request_count:
                self.redis_client.setex(key, int(self.time_window.total_seconds()), 1)
                return False

            request_count = int(request_count)
            if request_count >= self.rate_limit:
                return True

            self.redis_client.incr(key)
            return False
        else:
            # In-memory implementation
            if key not in self.request_count:
                self.request_count[key] = []

            # Remove old requests outside the time window
            self.request_count[key] = [
                timestamp
                for timestamp in self.request_count[key]
                if current_time - timestamp <= self.time_window
            ]

            if len(self.request_count[key]) >= self.rate_limit:
                return True

            self.request_count[key].append(current_time)
            return False

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_ip = kwargs.get("request").client.host

            if self.is_rate_limited(key=user_ip):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later.",
                )

            return await func(*args, **kwargs)

        return wrapper


limiter = RateLimiterDecorator()

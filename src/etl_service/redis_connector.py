import redis  # type: ignore


def get_redis_client(redis_host: str, redis_port: int) -> redis.Redis:
    return redis.Redis(host=redis_host, port=redis_port)

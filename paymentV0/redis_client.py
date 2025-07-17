import redis

# 本地 Redis 默认配置
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def set_idempotency_key(key: str, value: str, ttl: int = 600):
    if not r.exists(key):
        r.set(key, value, ex=ttl)
        return True
    return False

def get_value(key: str):
    return r.get(key)


import os
import json
import redis
import hashlib
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST: str = os.getenv("REDIS_HOST", "")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

r: redis.Redis = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True,
    decode_responses=True
)

def _get_cache_key(a: str, b: str) -> str:
    combo: str = f"{a}|{b}"
    return f"combo:{hashlib.sha256(combo.encode()).hexdigest()}"

def get_cached_response(a: str, b: str):
    return r.get(_get_cache_key(a, b))

def cache_response(a: str, b: str, response: dict, ttl: int = 3600) -> None:
    r.setex(_get_cache_key(a,b), ttl, json.dumps(response))
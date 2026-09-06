from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
import json
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis Cache setup
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def cache_get(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def cache_set(key: str, data: dict, expire_seconds: int = 300):
    redis_client.setex(key, expire_seconds, json.dumps(data))
